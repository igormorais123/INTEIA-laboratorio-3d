import assert from 'node:assert/strict';
import {ENGINE_PROFILES, firingIntervalDeg, firingWindowAt, cylinderAt} from './src/sound/engine-profiles.mjs';
import {createCurve, evaluateCurve, createRpmFollower, simulateCurve, curveToJSON, curveFromJSON, CURVE_PRESETS, presetCurve, MIN_POINT_GAP_S, TECH_MAX_RATE_RPM_PER_S} from './src/sound/rpm-curve.mjs';

const {v12_90s: v12, v6_2026: v6} = ENGINE_PROFILES;

// Perfis
assert.equal(Object.isFrozen(ENGINE_PROFILES), true);
for (const p of [v12, v6]) {
  assert.equal(p.firingOrder.length, p.cylinders, `${p.id}: ordem de ignição completa`);
  assert.deepEqual([...p.firingOrder].sort((a, b) => a - b), Array.from({length: p.cylinders}, (_, i) => i + 1), `${p.id}: cada cilindro uma vez`);
  assert.ok(p.idleRpm > p.crankingRpm && p.limitRpm > p.idleRpm);
  assert.ok(Object.isFrozen(p) && Object.isFrozen(p.firingOrder));
}
assert.equal(firingIntervalDeg(v12), 60);
assert.equal(firingIntervalDeg(v6), 120);
assert.equal(cylinderAt(v12, 0), 1);
assert.equal(cylinderAt(v12, 61), 7);
assert.equal(cylinderAt(v12, 719.9), 10);
assert.equal(cylinderAt(v6, 250), 2);
assert.equal(firingWindowAt(v6, 720 + 130), 1, 'ângulo acima de 720° volta ao ciclo');

// Criação e saneamento
const linear = createCurve();
assert.deepEqual(curveToJSON(linear), {version: 1, durationS: 3, maxRpm: 12000, points: [[0, 0], [3, 12000]]});
const messy = createCurve({durationS: 2, maxRpm: 12000, points: [[1, 20000], [0, 5000], [1.005, 3000], [-1, 7], [0.5, 6000], [NaN, 1]]});
assert.deepEqual(messy.points, [[0, 0], [0.5, 6000], [1, 12000]], 'ponto inicial fixo, ordenação, limites e espaçamento mínimo');
assert.ok(messy.points.every((p, i, all) => i === 0 || p[0] - all[i - 1][0] >= MIN_POINT_GAP_S));
assert.equal(createCurve({durationS: 99}).durationS, 30);

// PCHIP sem overshoot
const plateau = createCurve({durationS: 3, maxRpm: 12000, points: [[1, 6000], [2, 6000], [3, 12000]]});
for (let i = 0; i <= 3000; i++) {
  const t = i / 1000, y = evaluateCurve(plateau, t);
  assert.ok(y >= 0 && y <= 12000);
  if (t >= 1 && t <= 2) assert.ok(Math.abs(y - 6000) < 1e-6, `platô preservado em t=${t}`);
}
const peak = createCurve({durationS: 3, maxRpm: 12000, points: [[1, 8000], [1.2, 11000], [3, 9000]]});
for (let i = 0; i <= 3000; i++) assert.ok(evaluateCurve(peak, i / 1000) <= 11000 + 1e-6, 'nenhum pico acima do ponto desenhado');
let previous = -1;
for (let i = 0; i <= 3000; i++) { const y = evaluateCurve(linear, i / 1000); assert.ok(y >= previous - 1e-9, 'rampa crescente continua monotônica'); previous = y; }
assert.equal(evaluateCurve(linear, 1.5), 6000);
assert.equal(evaluateCurve(linear, 10), 12000);

// Seguidor: inércia, teto técnico, limitador, partida e carga
const follower = createRpmFollower(v12);
const first = follower.step(12000, 0.01);
assert.equal(first.rpm, 400, 'subida limitada a 40.000 RPM/s');
assert.equal(first.rateLimited, true);
assert.equal(first.cranking, true);
assert.equal(first.running, false);
assert.equal(first.load, 1, 'subindo no limite = acelerador pisado');
const free = createRpmFollower(v12, {physical: false});
assert.equal(free.step(12000, 0.01).rpm, Math.min(12000, TECH_MAX_RATE_RPM_PER_S * 0.01));
const limiter = createRpmFollower(v6, {physical: false});
let state;
for (let i = 0; i < 200; i++) state = limiter.step(20000, 0.001);
assert.equal(state.rpm, 15000, 'giro cortado no limite do perfil');
assert.equal(state.limiter, true);
assert.equal(state.running, true);
for (let i = 0; i < 20; i++) state = limiter.step(0, 0.001);
assert.ok(state.load < 0.5, 'descendo = acelerador aliviado');
for (let i = 0; i < 2000; i++) state = limiter.step(0, 0.001);
assert.equal(state.rpm, 0);
assert.equal(state.running, false, 'abaixo da marcha lenta o motor apaga');
assert.equal(state.cranking, false);

// Simulação da rampa padrão
const frames = simulateCurve(linear, v12);
assert.equal(frames.length, 3001);
assert.ok(frames.every((f) => f.rpm <= f.target + 1e-6));
const startIndex = frames.findIndex((f) => f.running);
assert.ok(Math.abs(frames[startIndex].rpm - v12.idleRpm) < 10, 'explosões começam ao cruzar a marcha lenta');
assert.ok(Math.abs(frames.at(-1).rpm - 12000) < 1e-6);
const step = simulateCurve(createCurve({durationS: 1, maxRpm: 12000, points: [[0.01, 12000], [1, 12000]]}), v6);
assert.ok(step.some((f) => f.rateLimited), 'degrau impossível marcado');
assert.ok(step.every((f, i) => i === 0 || f.rpm - step[i - 1].rpm <= v6.maxRiseRpmPerS * 0.001 + 1e-6));

// JSON e presets
assert.deepEqual(curveToJSON(curveFromJSON(JSON.stringify(curveToJSON(plateau)))), curveToJSON(plateau));
assert.throws(() => curveFromJSON({version: 2, points: []}), /Versão/);
for (const id of Object.keys(CURVE_PRESETS)) {
  const curve = presetCurve(id);
  assert.ok(curve.points.length >= 2, `${id}: pontos`);
  assert.ok(curve.points.every(([, rpm]) => rpm <= 12000));
}

console.log('Curva RPM: perfis, PCHIP, inércia, limitador, partida, carga, JSON e presets OK.');
