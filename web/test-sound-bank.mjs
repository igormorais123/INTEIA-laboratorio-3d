// Bancos de loops reais (som-v12-v1, som-v6-v1): integridade, cobertura, alinhamento e afinação no reprodutor.
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {existsSync, readFileSync} from 'node:fs';
import {ENGINE_PROFILES, firingIntervalDeg} from './src/sound/engine-profiles.mjs';
import {firingHz} from './src/sound/tuning.mjs';
import {detectFiringHz} from './src/sound/pitch.mjs';
import {createPhasePlayer} from './src/sound/phase-player.mjs';
import {parseBank, validateManifest} from './src/sound/bank-format.mjs';

const SR = 48000;
const MAX_BIN_BYTES = 3 * 1024 * 1024;
const read = (path) => readFileSync(new URL(path, import.meta.url));
const rms = (x) => Math.sqrt(x.reduce((s, v) => s + v * v, 0) / x.length);

// Um ciclo do loop reamostrado numa grade angular comum (interpolação linear), para comparar rotações vizinhas.
function angularCycle(loop, samples) {
  const out = new Float32Array(samples);
  for (let i = 0; i < samples; i++) {
    const position = (i / samples) * loop.samplesPerCycle;
    const j = Math.floor(position), f = position - j;
    out[i] = loop.data[j % loop.samplesPerCycle] * (1 - f) + loop.data[(j + 1) % loop.samplesPerCycle] * f;
  }
  return out;
}

// Atraso (em graus) que maximiza a correlação circular entre dois ciclos na grade angular.
function bestLagDeg(a, b, maxLagDeg) {
  const n = a.length, maxLag = Math.round((maxLagDeg / 720) * n);
  let best = -Infinity, bestLag = 0;
  for (let lag = -maxLag; lag <= maxLag; lag++) {
    let sum = 0;
    for (let i = 0; i < n; i++) sum += a[i] * b[(i + lag + n) % n];
    if (sum > best) { best = sum; bestLag = lag; }
  }
  return (bestLag / n) * 720;
}

let checked = 0;
for (const profile of Object.values(ENGINE_PROFILES)) {
  const manifestUrl = new URL(profile.bank, import.meta.url);
  if (!existsSync(manifestUrl)) { console.log(`${profile.id}: banco ainda não gerado (${profile.bank}), pulado`); continue; }
  const manifest = JSON.parse(readFileSync(manifestUrl, 'utf8'));
  const bin = read(new URL(manifest.bin, manifestUrl).href);
  assert.equal(manifest.engine, profile.id);
  assert.ok(validateManifest(manifest));
  assert.equal(bin.length, manifest.bytes, `${profile.id}: bytes do .bin`);
  assert.equal(createHash('sha256').update(bin).digest('hex'), manifest.sha256, `${profile.id}: sha256 do .bin`);
  assert.ok(bin.length <= MAX_BIN_BYTES, `${profile.id}: ${bin.length} bytes acima de 3 MB`);
  assert.equal(manifest.profile.cylinders, profile.cylinders);
  assert.deepEqual(manifest.profile.firingOrder, [...profile.firingOrder]);
  assert.ok(manifest.calibration.maxBandDistanceDb <= manifest.calibration.acceptLimitDb);

  const bank = parseBank(manifest, bin.buffer.slice(bin.byteOffset, bin.byteOffset + bin.byteLength));
  const rpms = [...new Set(bank.loops.map((l) => l.rpm))].sort((a, b) => a - b);
  assert.ok(rpms[0] <= profile.idleRpm + 1e-6, `${profile.id}: primeiro ponto ${rpms[0]} acima da marcha lenta`);
  assert.ok(rpms[rpms.length - 1] >= profile.limitRpm - 1e-6, `${profile.id}: último ponto ${rpms[rpms.length - 1]} abaixo do limite`);
  for (let i = 1; i < rpms.length; i++) assert.ok(rpms[i] / rpms[i - 1] < 1.09, `${profile.id}: salto de ${(rpms[i] / rpms[i - 1] - 1) * 100}% entre pontos`);
  for (const rpm of rpms) {
    const loads = bank.loops.filter((l) => l.rpm === rpm).map((l) => l.load).sort();
    assert.deepEqual(loads, ['off', 'on'], `${profile.id} ${rpm}: cargas`);
  }
  for (const loop of bank.loops) {
    assert.ok(loop.data.length * 1 / SR >= 0.6 - 1e-9, `${profile.id} ${loop.rpm}/${loop.load}: loop menor que 0,6 s`);
    assert.ok(loop.data.every(Number.isFinite));
    assert.ok(Math.max(...loop.data.map(Math.abs)) <= 10 ** (-3 / 20) + 1e-3, `${profile.id}: pico acima de −3 dBFS`);
    // Emenda: o salto entre a última e a primeira amostra não passa do maior salto interno (o loop pode
    // começar numa frente de pulso, então a comparação é com o máximo, não com um percentil)
    let maxStep = 0;
    for (let i = 1; i < loop.data.length; i++) maxStep = Math.max(maxStep, Math.abs(loop.data[i] - loop.data[i - 1]));
    assert.ok(Math.abs(loop.data[loop.data.length - 1] - loop.data[0]) <= maxStep, `${profile.id} ${loop.rpm}/${loop.load}: emenda audível`);
  }
  // Pisado é mais forte que aliviado em todos os pontos
  for (const rpm of rpms) {
    const on = bank.loops.find((l) => l.rpm === rpm && l.load === 'on'), off = bank.loops.find((l) => l.rpm === rpm && l.load === 'off');
    assert.ok(rms(off.data) < rms(on.data), `${profile.id} ${rpm}: aliviado não é mais baixo`);
  }
  // Alinhamento: cada rotação se alinha com a vizinha na grade angular (sem phasing no crossfade).
  const grid = 1440;
  const windowDeg = firingIntervalDeg(profile);
  for (let i = 1; i < rpms.length; i++) {
    const cycle = angularCycle(bank.loops.find((l) => l.rpm === rpms[i] && l.load === 'on'), grid);
    const previous = angularCycle(bank.loops.find((l) => l.rpm === rpms[i - 1] && l.load === 'on'), grid);
    const lagNeighbour = Math.abs(bestLagDeg(previous, cycle, windowDeg / 2));
    assert.ok(lagNeighbour <= windowDeg * 0.15, `${profile.id} ${rpms[i - 1]}→${rpms[i]}: defasagem de ${lagNeighbour.toFixed(1)}°`);
  }
  // Pisado e aliviado do mesmo ponto também se alinham
  for (const rpm of rpms) {
    const on = angularCycle(bank.loops.find((l) => l.rpm === rpm && l.load === 'on'), grid);
    const off = angularCycle(bank.loops.find((l) => l.rpm === rpm && l.load === 'off'), grid);
    const lag = Math.abs(bestLagDeg(on, off, windowDeg / 2));
    assert.ok(lag <= windowDeg * 0.15, `${profile.id} ${rpm}: pisado e aliviado defasados em ${lag.toFixed(1)}°`);
  }
  // Integração com o reprodutor: afinação medida a ±1 % em cinco rotações
  const player = createPhasePlayer({bank, profile, sampleRate: SR});
  for (const rpm of [4500, 6000, 7000, 9300, 12000]) {
    player.reset();
    const state = {rpmFrom: rpm, rpmTo: rpm, load: 1, running: true, cranking: false, limiter: false};
    player.render(new Float32Array(4096), state);
    const out = player.render(new Float32Array(16384), state);
    const expected = firingHz(rpm, profile.cylinders);
    const pitch = detectFiringHz(out.subarray(0, 8192), SR, {minHz: expected * 0.6, maxHz: expected * 1.6});
    assert.ok(pitch, `${profile.id} ${rpm}: afinação não detectada`);
    assert.ok(Math.abs(pitch.hz - expected) / expected < 0.01, `${profile.id} ${rpm}: ${pitch.hz.toFixed(1)} Hz ≠ ${expected.toFixed(1)} Hz`);
  }
  assert.ok(bank.starter && bank.starter.data.length > SR * 0.5, `${profile.id}: loop de partida ausente`);
  checked++;
  console.log(`${profile.id}: ${rpms.length} pontos × 2 cargas, ${(bin.length / 1e6).toFixed(2)} MB, distância máxima ${manifest.calibration.maxBandDistanceDb} dB (limite ${manifest.calibration.acceptLimitDb}).`);
}
console.log(`Bancos de som: ${checked} banco(s) íntegros, alinhados e afinados OK.`);
