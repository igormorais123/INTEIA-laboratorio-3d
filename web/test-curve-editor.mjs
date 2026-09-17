// Lógica de edição da curva (sem DOM): inserir, mover sem cruzar vizinhos, apagar, teclado, duração e grade de notas.
import assert from 'node:assert/strict';
import {ENGINE_PROFILES} from './src/sound/engine-profiles.mjs';
import {MIN_POINT_GAP_S} from './src/sound/rpm-curve.mjs';
import {addPoint, createEditorState, movePoint, noteGrid, nudgePoint, removePoint, setDuration, setMaxRpm, stateToCurve} from './src/sound/curve-editor.js';

let state = createEditorState({durationS: 3, maxRpm: 12000, points: [[3, 12000]]});
assert.deepEqual(state.points, [[0, 0], [3, 12000]]);

// Inserir ordena por tempo e devolve o índice
let result = addPoint(state, 1.5, 6000);
assert.equal(result.index, 1);
assert.deepEqual(result.state.points, [[0, 0], [1.5, 6000], [3, 12000]]);
state = result.state;
// Inserir em cima de um ponto existente é recusado
assert.equal(addPoint(state, 1.5 + MIN_POINT_GAP_S / 2, 3000).index, -1);
// Fora do eixo é limitado
result = addPoint(state, 9, 99999);
assert.equal(result.index, -1, 'colide com o último ponto após o clamp'); // t=3 já existe

// Mover não cruza vizinhos nem sai do eixo; o ponto 0 é fixo
state = movePoint(state, 1, 2.999, 20000);
assert.ok(state.points[1][0] <= 3 - MIN_POINT_GAP_S + 1e-9 && state.points[1][0] > 1.5);
assert.equal(state.points[1][1], 12000);
state = movePoint(state, 1, -5, -100);
assert.ok(state.points[1][0] >= MIN_POINT_GAP_S && state.points[1][1] === 0);
assert.deepEqual(movePoint(state, 0, 1, 1000).points[0], [0, 0]);
assert.equal(movePoint(state, 7, 1, 1).points.length, state.points.length);

// Teclado: setas movem em passos; Shift = passo maior
state = movePoint(state, 1, 1.5, 6000);
const nudged = nudgePoint(state, 1, 0.05, 100);
assert.ok(Math.abs(nudged.points[1][0] - 1.55) < 1e-9 && nudged.points[1][1] === 6100);

// Apagar: nunca o ponto 0 nem o último restante
assert.equal(removePoint(state, 0).points.length, 3);
state = removePoint(state, 1);
assert.deepEqual(state.points, [[0, 0], [3, 12000]]);
assert.equal(removePoint(state, 1).points.length, 2, 'a curva mantém pelo menos dois pontos');

// Duração reescala os tempos; RPM máximo limita os pontos e respeita o limite do perfil
state = addPoint(state, 1, 4000).state;
const longer = setDuration(state, 6);
assert.equal(longer.durationS, 6);
assert.deepEqual(longer.points.map((p) => p[0]), [0, 2, 6]);
const capped = setMaxRpm(state, 30000, ENGINE_PROFILES.v6_2026.limitRpm);
assert.equal(capped.maxRpm, 15000);
const lowered = setMaxRpm(state, 5000, 17000);
assert.ok(lowered.points.every((p) => p[1] <= 5000));

// Estado → curva do reprodutor
const curve = stateToCurve(state);
assert.equal(curve.durationS, 3);
assert.equal(curve.points.length, 3);

// Grade de notas: V12 e V6 mostram notas diferentes na mesma altura (uma oitava de diferença)
const gridV12 = noteGrid(ENGINE_PROFILES.v12_90s, 12000), gridV6 = noteGrid(ENGINE_PROFILES.v6_2026, 12000);
assert.ok(gridV12.length > 20 && gridV6.length > 20);
const la4v12 = gridV12.find((l) => l.midi === 69), la4v6 = gridV6.find((l) => l.midi === 69);
assert.ok(la4v12 && la4v6 && Math.abs(la4v6.rpm / la4v12.rpm - 2) < 1e-9, 'Lá 4 exige o dobro de RPM no V6');
assert.ok(gridV12.every((l) => l.rpm > 0 && l.rpm <= 12000));
assert.ok(gridV12.some((l) => l.label.startsWith('Dó')) && gridV12.filter((l) => !l.natural).every((l) => l.label === ''));

console.log('Editor de curva: inserir, mover, apagar, teclado, duração, RPM máximo e grade de notas OK.');
