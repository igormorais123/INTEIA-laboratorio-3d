// Renderiza demonstrações em WAV (48 kHz, mono, 16 bits) dos bancos calibrados usando os módulos do site
// (reprodutor com fase travada + seguidor de curva), para audição lado a lado com as referências.
// Saída: ferramentas/som/.demos/<motor>-<nome>.wav (fora do Git). Uso: node ferramentas/som/renderizar_demos.mjs [v12_90s|v6_2026]
import {existsSync, mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {ENGINE_PROFILES} from '../../web/src/sound/engine-profiles.mjs';
import {createPhasePlayer} from '../../web/src/sound/phase-player.mjs';
import {parseBank} from '../../web/src/sound/bank-format.mjs';
import {CURVE_PRESETS, createRpmFollower, evaluateCurve, presetCurve} from '../../web/src/sound/rpm-curve.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const assets = join(here, '..', '..', 'web', 'assets');
const outDir = join(here, '.demos');
const SR = 48000, BLOCK = 128, GAIN = 0.85;
mkdirSync(outDir, {recursive: true});

function writeWav(path, samples) {
  const buffer = Buffer.alloc(44 + samples.length * 2);
  buffer.write('RIFF', 0); buffer.writeUInt32LE(36 + samples.length * 2, 4); buffer.write('WAVE', 8);
  buffer.write('fmt ', 12); buffer.writeUInt32LE(16, 16); buffer.writeUInt16LE(1, 20); buffer.writeUInt16LE(1, 22);
  buffer.writeUInt32LE(SR, 24); buffer.writeUInt32LE(SR * 2, 28); buffer.writeUInt16LE(2, 32); buffer.writeUInt16LE(16, 34);
  buffer.write('data', 36); buffer.writeUInt32LE(samples.length * 2, 40);
  for (let i = 0; i < samples.length; i++) buffer.writeInt16LE(Math.max(-32768, Math.min(32767, Math.round(samples[i] * 32767))), 44 + i * 2);
  writeFileSync(path, buffer);
}

function loadBank(profile) {
  const manifestPath = join(assets, profile.bank.replace('./assets/', ''));
  if (!existsSync(manifestPath)) return null;
  const manifest = JSON.parse(readFileSync(manifestPath, 'utf8'));
  const bin = readFileSync(join(assets, manifest.bin));
  return parseBank(manifest, bin.buffer.slice(bin.byteOffset, bin.byteOffset + bin.byteLength));
}

/** Toca uma sequência de alvos de RPM (função t → rpm alvo) pelo seguidor físico e pelo reprodutor. */
function renderTargets(profile, bank, seconds, targetAt) {
  const player = createPhasePlayer({bank, profile, sampleRate: SR});
  const follower = createRpmFollower(profile, {physical: true});
  const total = Math.round(seconds * SR);
  const out = new Float32Array(total);
  let previous = follower.step(targetAt(0), 0);
  for (let start = 0; start < total; start += BLOCK) {
    const frames = Math.min(BLOCK, total - start);
    const t = (start + frames) / SR;
    const next = follower.step(targetAt(t), frames / SR);
    const state = {rpmFrom: previous.rpm, rpmTo: next.rpm, load: next.load, running: next.running, cranking: next.cranking, limiter: next.limiter};
    const block = player.render(new Float32Array(frames), state, GAIN);
    out.set(block, start);
    previous = next;
  }
  // Fade curto nas pontas para não estalar no reprodutor de áudio
  const fade = Math.round(SR * 0.01);
  for (let i = 0; i < fade; i++) { out[i] *= i / fade; out[total - 1 - i] *= i / fade; }
  return out;
}

const wanted = process.argv[2];
const written = [];
for (const profile of Object.values(ENGINE_PROFILES)) {
  if (wanted && profile.id !== wanted) continue;
  const bank = loadBank(profile);
  if (!bank) { console.log(`${profile.id}: banco ausente, pulado`); continue; }
  for (const [id, preset] of Object.entries(CURVE_PRESETS)) {
    const curve = presetCurve(id);
    const lead = 0.4, tail = 0.6;
    const samples = renderTargets(profile, bank, lead + curve.durationS + tail, (t) => (t < lead ? 0 : evaluateCurve(curve, t - lead)));
    const path = join(outDir, `${profile.id}-curva-${id}.wav`);
    writeWav(path, samples);
    written.push([path, preset.label]);
  }
  for (const rpm of [profile.idleRpm, 6000, 7000, 9000, 12000, Math.min(15000, profile.limitRpm)]) {
    const samples = renderTargets(profile, bank, 3.0, () => rpm);
    const path = join(outDir, `${profile.id}-fixo-${rpm}.wav`);
    writeWav(path, samples);
    written.push([path, `${rpm} RPM fixo`]);
  }
  // Rampa completa da marcha lenta ao limite e volta (12 s), a mais reveladora para julgar o timbre
  const sweep = renderTargets(profile, bank, 12.5, (t) => (t < 0.5 ? 0 : t < 6.5 ? profile.idleRpm + ((profile.limitRpm - profile.idleRpm) * (t - 0.5)) / 6 : profile.limitRpm - ((profile.limitRpm - profile.idleRpm) * (t - 6.5)) / 6));
  const sweepPath = join(outDir, `${profile.id}-varredura-${profile.idleRpm}-${profile.limitRpm}.wav`);
  writeWav(sweepPath, sweep);
  written.push([sweepPath, `varredura ${profile.idleRpm}→${profile.limitRpm}→${profile.idleRpm} RPM`]);
}
for (const [path, label] of written) console.log(`${label.padEnd(44)} ${path}`);
console.log(`${written.length} demonstrações em ${outDir}`);
