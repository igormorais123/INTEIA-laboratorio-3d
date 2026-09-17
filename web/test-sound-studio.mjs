// Aba 07 Som: contratos estáticos do template, do build, do workbench e do worklet; sem metalinguagem no painel.
import assert from 'node:assert/strict';
import {existsSync, readFileSync} from 'node:fs';
import {SOUND_CREDITS} from './src/sound/sound-studio.js';

const read = (path) => readFileSync(new URL(path, import.meta.url), 'utf8');
const template = read('./src/template-v2.html');
const workbench = read('./src/workbench.js');
const app = read('./src/app-v2.js');
const build = read('./build.cjs');
const worklet = read('./src/sound/engine-worklet.js');

// Aba e painel
assert.match(template, /<button id="tab-sound" role="tab" data-lab-tab="sound"[^>]*><span>07<\/span>Som<\/button>/, 'aba 07 Som ausente');
assert.ok(template.includes('id="sound-panel"') && template.includes('SOM / ESTÚDIO DE AFINAÇÃO'));
for (const id of ['sound-status', 'sound-power', 'sound-volume', 'sound-mode-curve', 'sound-mode-free', 'sound-curve', 'sound-play', 'sound-stop', 'sound-loop', 'sound-presets', 'sound-duration', 'sound-maxrpm', 'sound-physical', 'sound-export', 'sound-import', 'sound-throttle', 'sound-fixed', 'tuner-rpm', 'tuner-hz', 'tuner-note', 'tuner-measured', 'tuner-deviation', 'tuner-state', 'sound-cylinders', 'sound-credits', 'sound-credits-list', 'sound-worklet']) {
  assert.ok(template.includes(`id="${id}"`), `template sem #${id}`);
}
assert.equal((template.match(/data-sound-engine="/g) || []).length, 2, 'dois motores selecionáveis');
assert.ok(template.includes('data-sound-engine="v12_90s"') && template.includes('data-sound-engine="v6_2026"'));

// Build injeta o worklet como texto no template
assert.match(template, /<script id="sound-worklet" type="text\/plain">__SOUND_WORKLET__<\/script>/);
assert.match(build, /engine-worklet\.js/); assert.match(build, /__SOUND_WORKLET__/);
assert.match(worklet, /registerProcessor\('inteia-engine'/);
assert.match(worklet, /createEngineVoice/, 'worklet usa a voz compartilhada com os demos');
const voice = read('./src/sound/engine-voice.mjs'); assert.match(voice, /createPhasePlayer/); assert.match(voice, /createRpmFollower/); assert.ok(!/document\.|window\./.test(voice));
assert.ok(!/document\.|window\./.test(worklet), 'worklet não pode tocar no DOM');

// Workbench e app
assert.match(workbench, /startsWith\('SOM'\)\?'sound'/, 'workbench não reconhece o painel de som');
assert.match(workbench, /sound:'Som'/); assert.match(workbench, /active==='sound'/);
assert.match(app, /createSoundStudio\(/); assert.match(app, /soundStudio\?\.update\(now\)/);
assert.match(app, /sound-worklet/);

// Áudio só após clique: nenhum AudioContext criado fora dos manipuladores
const studio = read('./src/sound/sound-studio.js');
assert.match(studio, /async function ensureAudio/);
assert.ok(!/^\s*const context\s*=\s*new/m.test(studio), 'AudioContext não pode nascer no carregamento');
assert.match(studio, /sampleRate: 48000/);
assert.match(studio, /detectFiringHz/);

// Créditos completos
assert.ok(SOUND_CREDITS.length >= 5 && SOUND_CREDITS.every((c) => c.title && c.author && /^(CC0|CC BY-SA 3\.0)$/.test(c.license) && c.url.startsWith('https://')));

// Sem metalinguagem de produção no painel
const panel = template.slice(template.indexOf('id="sound-panel"'), template.indexOf('PERSONALIZAR / SEU DESIGN'));
for (const word of ['vídeo', 'youtube', 'capítulo', 'prompt', 'homolog', 'não é CAD', 'hipótese', 'plano 4', 'todo']) assert.ok(!panel.toLowerCase().includes(word), `painel de som cita "${word}"`);

// Build gerado (quando existe) carrega o worklet e não deixa marcadores
if (existsSync(new URL('./index.html', import.meta.url))) {
  const html = read('./index.html');
  assert.ok(!html.includes('__SOUND_WORKLET__') && !html.includes('__APP__'), 'marcadores não substituídos');
  assert.match(html, /registerProcessor\("inteia-engine"/);
  assert.ok(html.includes('id="tab-sound"'));
}
console.log('Aba 07 Som: aba, painel, worklet no build, workbench, créditos e ausência de metalinguagem OK.');
