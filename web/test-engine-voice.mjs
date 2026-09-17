// Voz completa do motor (engine-voice.mjs): partida, modo livre, curva com repetição, teto de saída, desvio de
// rotação dentro do limite e afinação medida por soma harmônica.
import assert from 'node:assert/strict';
import {ENGINE_PROFILES} from './src/sound/engine-profiles.mjs';
import {createEngineVoice} from './src/sound/engine-voice.mjs';
import {OUTPUT_CEILING} from './src/sound/phase-player.mjs';
import {firingHz} from './src/sound/tuning.mjs';
import {detectFiringHz} from './src/sound/pitch.mjs';
import {curveToJSON, presetCurve} from './src/sound/rpm-curve.mjs';
import {createTestBank} from './test-fixtures/sound-bank.mjs';

const SR = 48000, BLOCK = 128;
const run = (voice, seconds, onBlock = () => {}) => {
  const out = new Float32Array(Math.round(seconds * SR)); let status = null;
  for (let start = 0; start < out.length; start += BLOCK) { const frames = Math.min(BLOCK, out.length - start); onBlock(start / SR); status = voice.render(out.subarray(start, start + frames)); }
  return {out, status};
};

for (const profile of Object.values(ENGINE_PROFILES)) {
  const bank = createTestBank(profile, {withStarter: true});
  // Desligado: silêncio absoluto
  let voice = createEngineVoice({bank, profile, sampleRate: SR});
  assert.equal(run(voice, 0.2).out.some((v) => v !== 0), false, `${profile.id}: som com motor desligado`);
  // Ligar: partida (arranque) antes da marcha lenta, depois regime em marcha lenta
  voice.setState({mode: 'free', power: true, volume: 0.5});
  const cranking = run(voice, 0.4).status;
  assert.ok(cranking.cranking && !cranking.running, `${profile.id}: partida não passou pelo motor de arranque`);
  const idle = run(voice, 1.5).status;
  assert.ok(idle.running && Math.abs(idle.rpm / profile.idleRpm - 1) < 0.03, `${profile.id}: marcha lenta em ${idle.rpm}`);
  // Rotação fixa: afinação medida a ±2 % (o desvio natural de rotação é menor que isso)
  voice.setState({fixedRpm: 9000});
  const steady = run(voice, 1.0).out;
  const expected = firingHz(9000, profile.cylinders);
  const pitch = detectFiringHz(steady.subarray(steady.length - 8192), SR, {minHz: expected * 0.6, maxHz: expected * 1.6});
  assert.ok(pitch && Math.abs(pitch.hz / expected - 1) < 0.02, `${profile.id}: ${pitch?.hz} Hz ≠ ${expected} Hz`);
  assert.ok(steady.every((v) => Number.isFinite(v) && Math.abs(v) <= OUTPUT_CEILING + 1e-6), `${profile.id}: saída acima de −1 dBFS ou NaN`);
  // Aliviar em alta rotação e desligar: cai até parar
  voice.setState({fixedRpm: null, throttle: 0.9}); run(voice, 0.5);
  voice.setState({power: false});
  const off = run(voice, 1.2).status;
  assert.ok(!off.running && off.rpm < 1, `${profile.id}: não desligou (${off.rpm} RPM)`);
  // Curva: toca do zero, termina sozinha; com repetição continua tocando
  voice = createEngineVoice({bank, profile, sampleRate: SR});
  voice.setState({mode: 'curve', volume: 0.5});
  voice.setCurve(curveToJSON(presetCurve('linear')));
  voice.play();
  const middle = run(voice, 2.2).status;
  assert.ok(middle.playing && middle.running && middle.rpm > 3000, `${profile.id}: curva não acelerou (${middle.rpm} RPM em t=${middle.t})`);
  const ended = run(voice, 2.5).status;
  assert.ok(!ended.playing, `${profile.id}: curva não terminou`);
  voice.setState({loop: true}); voice.play();
  const looping = run(voice, 4.5).status;
  assert.ok(looping.playing && looping.t < 3, `${profile.id}: repetição não reiniciou a curva`);
}
console.log('Voz do motor: partida, marcha lenta, rotação fixa afinada, desligamento, curva e repetição OK.');
