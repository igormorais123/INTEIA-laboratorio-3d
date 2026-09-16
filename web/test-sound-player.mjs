import assert from 'node:assert/strict';
import {ENGINE_PROFILES} from './src/sound/engine-profiles.mjs';
import {firingHz} from './src/sound/tuning.mjs';
import {detectPitch} from './src/sound/pitch.mjs';
import {createPhasePlayer, prepareBank, OUTPUT_CEILING} from './src/sound/phase-player.mjs';
import {createTestBank} from './test-fixtures/sound-bank.mjs';

const SR = 48000;
const steady = (rpm, extra = {}) => ({rpmFrom: rpm, rpmTo: rpm, load: 1, running: true, cranking: false, limiter: false, ...extra});
const rms = (x) => Math.sqrt(x.reduce((s, v) => s + v * v, 0) / x.length);
const db = (a, b) => 20 * Math.log10(a / b);

function renderSteady(profile, rpm, {seconds = 0.4, extra = {}, bankOptions = {}, gain = 1} = {}) {
  const player = createPhasePlayer({bank: createTestBank(profile, bankOptions), profile, sampleRate: SR});
  const warm = new Float32Array(2048);
  player.render(warm, steady(rpm, extra), gain);
  return player.render(new Float32Array(Math.round(seconds * SR)), steady(rpm, extra), gain);
}

// Validação do banco
assert.throws(() => prepareBank({sampleRate: SR, loops: []}), /dois pontos/);
const broken = createTestBank(ENGINE_PROFILES.v6_2026);
broken.loops = broken.loops.filter((l) => !(l.rpm === broken.loops[0].rpm && l.load === 'off'));
assert.throws(() => prepareBank(broken), /duas cargas/);
assert.throws(() => createPhasePlayer({bank: createTestBank(ENGINE_PROFILES.v6_2026), profile: ENGINE_PROFILES.v6_2026, sampleRate: 44100}), /48000/);

// Afinação medida a ±1% da fórmula, em pontos do banco e entre pontos
for (const profile of Object.values(ENGINE_PROFILES)) {
  for (const rpm of [4500, 6000, 7000, 9300, 12000]) {
    const out = renderSteady(profile, rpm);
    const expected = firingHz(rpm, profile.cylinders);
    const pitch = detectPitch(out.subarray(0, 8192), SR, {minHz: expected * 0.55, maxHz: expected * 2.5});
    assert.ok(pitch, `${profile.id} ${rpm} RPM: afinação detectada`);
    assert.ok(Math.abs(pitch.hz - expected) / expected < 0.01, `${profile.id} ${rpm} RPM: medido ${pitch.hz.toFixed(1)} Hz, esperado ${expected} Hz`);
  }
}

// Crossfade sem phasing: entre dois pontos o nível não cai mais de 1 dB
for (const profile of Object.values(ENGINE_PROFILES)) {
  const low = rms(renderSteady(profile, 6000)), high = rms(renderSteady(profile, 8000)), middle = rms(renderSteady(profile, 7000));
  assert.ok(db(middle, Math.min(low, high)) > -1, `${profile.id}: queda de ${db(middle, Math.min(low, high)).toFixed(2)} dB no crossfade`);
}

// Carga: aliviado é mais baixo que pisado
{
  const profile = ENGINE_PROFILES.v12_90s;
  assert.ok(rms(renderSteady(profile, 9000, {extra: {load: 0}})) < rms(renderSteady(profile, 9000)) * 0.6);
}

// Limitador: corta metade das explosões sem NaN
{
  const profile = ENGINE_PROFILES.v6_2026;
  const normal = renderSteady(profile, 15000);
  const limited = renderSteady(profile, 15000, {extra: {limiter: true}});
  assert.ok(limited.every(Number.isFinite));
  assert.ok(db(rms(limited), rms(normal)) < -2, `limitador reduziu só ${db(rms(limited), rms(normal)).toFixed(2)} dB`);
}

// Teto de saída mesmo com ganho alto; motor desligado é silêncio
{
  const loud = renderSteady(ENGINE_PROFILES.v12_90s, 12000, {gain: 20});
  assert.ok(loud.every((v) => Number.isFinite(v) && Math.abs(v) <= OUTPUT_CEILING + 1e-6), 'pico acima de −1 dBFS');
  const off = renderSteady(ENGINE_PROFILES.v12_90s, 2000, {extra: {running: false}});
  assert.equal(rms(off), 0);
}

// Partida: toca o motor de arranque só quando existe e o motor está girando sem explosões
{
  const profile = ENGINE_PROFILES.v12_90s;
  const withStarter = renderSteady(profile, 250, {extra: {running: false, cranking: true}, bankOptions: {withStarter: true}});
  const without = renderSteady(profile, 250, {extra: {running: false, cranking: true}});
  assert.ok(rms(withStarter) > 0.05);
  assert.equal(rms(without), 0);
}

// Rampa contínua 4.000 → 12.000 RPM em 1 s: sem NaN nem saltos grandes entre amostras
{
  const profile = ENGINE_PROFILES.v12_90s;
  const player = createPhasePlayer({bank: createTestBank(profile), profile, sampleRate: SR});
  const block = 128;
  let rpm = 4000, maxJump = 0, last = 0;
  for (let i = 0; i < SR / block; i++) {
    const next = Math.min(12000, rpm + (8000 * block) / SR);
    const out = player.render(new Float32Array(block), {rpmFrom: rpm, rpmTo: next, load: 1, running: true, cranking: false, limiter: false});
    for (const v of out) { assert.ok(Number.isFinite(v)); maxJump = Math.max(maxJump, Math.abs(v - last)); last = v; }
    rpm = next;
  }
  assert.ok(maxJump < 0.5, `salto de ${maxJump.toFixed(3)} entre amostras`);
}

console.log('Reprodutor: afinação ±1%, crossfade sem phasing, carga, limitador, teto −1 dBFS, partida e rampa contínua OK.');
