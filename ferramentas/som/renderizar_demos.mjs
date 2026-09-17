// Renderiza demonstrações em WAV (48 kHz, mono, 16 bits) dos bancos calibrados com a MESMA voz do site
// (engine-voice.mjs: reprodutor com fase travada, seguidor com inércia, partida, desvio de rotação, camadas do
// V6, estalos ao aliviar e ambiente do box), para audição lado a lado com as referências.
// Saída: ferramentas/som/.demos/<motor>-<nome>.wav (fora do Git). Uso: node ferramentas/som/renderizar_demos.mjs [v12_90s|v6_2026]
import {existsSync, mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';
import {ENGINE_PROFILES} from '../../web/src/sound/engine-profiles.mjs';
import {createEngineVoice} from '../../web/src/sound/engine-voice.mjs';
import {parseBank} from '../../web/src/sound/bank-format.mjs';
import {CURVE_PRESETS, curveToJSON, presetCurve} from '../../web/src/sound/rpm-curve.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const assets = join(here, '..', '..', 'web', 'assets');
const outDir = join(here, '.demos');
const SR = 48000, BLOCK = 128, VOLUME = 0.8;
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

/** Toca a voz por `seconds`, chamando `drive(voice, t)` a cada bloco para mexer nos controles como um visitante. */
function renderVoice(profile, bank, seconds, drive) {
  const voice = createEngineVoice({bank, profile, sampleRate: SR});
  voice.setState({volume: VOLUME});
  const total = Math.round(seconds * SR), out = new Float32Array(total);
  for (let start = 0; start < total; start += BLOCK) {
    const frames = Math.min(BLOCK, total - start);
    drive(voice, start / SR);
    const block = new Float32Array(frames);
    voice.render(block);
    out.set(block, start);
  }
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
    const curve = presetCurve(id), lead = 0.3, tail = 1.2;
    let started = false;
    const samples = renderVoice(profile, bank, lead + curve.durationS + 0.7 + tail, (voice, t) => {
      if (!started) { voice.setState({mode: 'curve', power: false}); voice.setCurve(curveToJSON(curve)); started = true; }
      if (t >= lead && !voice.playing && voice.ignition === 'off' && t < lead + 0.1) voice.play();
    });
    written.push([join(outDir, `${profile.id}-curva-${id}.wav`), preset.label, samples]);
  }
  for (const rpm of [profile.idleRpm, 6000, 7000, 9000, 12000, Math.min(15000, profile.limitRpm)]) {
    const samples = renderVoice(profile, bank, 4.0, (voice, t) => { if (t === 0) voice.setState({mode: 'free', fixedRpm: rpm, power: true}); if (t > 3.2 && voice.state.power) voice.setState({power: false}); });
    written.push([join(outDir, `${profile.id}-fixo-${rpm}.wav`), `${rpm} RPM fixo`, samples]);
  }
  // Varredura completa pelo acelerador (marcha lenta → limite → marcha lenta) e desligamento
  const span = profile.limitRpm - profile.idleRpm;
  const sweep = renderVoice(profile, bank, 14.0, (voice, t) => {
    if (t === 0) voice.setState({mode: 'free', fixedRpm: null, throttle: 0, power: true});
    const throttle = t < 1 ? 0 : t < 7 ? (t - 1) / 6 : t < 13 ? 1 - (t - 7) / 6 : 0;
    voice.setState({throttle});
    if (t > 13.2 && voice.state.power) voice.setState({power: false});
  });
  written.push([join(outDir, `${profile.id}-varredura-${profile.idleRpm}-${profile.limitRpm}.wav`), `varredura ${profile.idleRpm}→${profile.limitRpm}→${profile.idleRpm} RPM`, sweep]);
  // Blips no acelerador em ponto morto: o teste clássico de timbre
  const blips = renderVoice(profile, bank, 8.0, (voice, t) => {
    if (t === 0) voice.setState({mode: 'free', fixedRpm: null, throttle: 0, power: true});
    const phase = (t - 1.2) % 1.6, open = t > 1.2 && phase < 0.35;
    voice.setState({throttle: open ? 0.85 : 0});
    if (t > 7.4 && voice.state.power) voice.setState({power: false});
  });
  written.push([join(outDir, `${profile.id}-blips.wav`), 'blips em ponto morto', blips]);
}
for (const [path, label, samples] of written) { writeWav(path, samples); console.log(`${label.padEnd(44)} ${path}`); }
console.log(`${written.length} demonstrações em ${outDir}`);
