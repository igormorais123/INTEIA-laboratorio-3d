# Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar os módulos puros (sem DOM e sem Web Audio) que calculam afinação, curva RPM × tempo e reproduzem um banco de loops com fase travada ao virabrequim, todos testados no Node.

**Architecture:** Quatro módulos ES em `web/src/sound/`: `tuning.mjs` (RPM → Hz → nota), `engine-profiles.mjs` (dados dos motores), `rpm-curve.mjs` (curva PCHIP + seguidor com inércia) e `phase-player.mjs` (leitura dos loops pelo ângulo θ, mistura bilinear RPM × carga, limitador e teto −1 dBFS), mais `pitch.mjs` (YIN) para o afinador e os testes. Os testes usam um banco sintético de pulsos (`web/test-fixtures/sound-bank.mjs`); o banco calibrado real é o Plano 2.

**Tech Stack:** Node.js ≥ 24, ES modules, `node:assert/strict`, sem dependências novas.

**Status:** concluído em 16–17/09/2026 (commits e2eda44, b8886cf, db923db). Continuação: `docs/estudio-som/HANDOFF.md`.

**Spec:** `docs/superpowers/specs/2026-09-16-estudio-som-v12-design.md`

## Global Constraints

- Node `>=24`; `web/package.json` é `"type": "module"`; testes são scripts `node test-*.mjs` com `node:assert/strict`, encadeados em `npm test`.
- Nenhuma dependência nova.
- Módulos de `web/src/sound/` não usam DOM, `window` nem Web Audio (rodam no Node e dentro do AudioWorklet).
- Afinação: `f0 = (RPM / 60) × (cilindros / 2)`; nota = `69 + 12 × log2(f0 / 440)`.
- V12 anos 90: 12 cilindros, 65°, ordem 1-7-5-11-3-9-6-12-2-8-4-10, marcha lenta 4.000, limite 17.000 RPM.
- V6 2026: 6 cilindros, 90°, ordem 1-4-2-5-3-6, marcha lenta 4.000, limite 15.000 RPM.
- Curva: ponto inicial fixo em (0, 0); eixo padrão 0–12.000 RPM; duração padrão 3 s, limitada a 0,5–30 s; JSON `{version: 1, durationS, maxRpm, points}`.
- Saída do reprodutor nunca acima de −1 dBFS.
- Textos e mensagens em português brasileiro; commits no estilo do repositório (frase em português, imperativo) com as linhas de atribuição da sessão.
- Trabalhar no branch `estudio-som-v12`.

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `web/src/sound/tuning.mjs` | Conversões RPM ↔ Hz ↔ nota |
| `web/src/sound/engine-profiles.mjs` | Perfis V12/V6 e janelas de ignição |
| `web/src/sound/rpm-curve.mjs` | Curva editável, PCHIP, seguidor com inércia, presets, JSON |
| `web/src/sound/pitch.mjs` | Detector YIN de f0 |
| `web/src/sound/phase-player.mjs` | Reprodutor de loops com fase travada |
| `web/test-fixtures/sound-bank.mjs` | Banco sintético só para testes |
| `web/test-tuning.mjs`, `web/test-rpm-curve.mjs`, `web/test-sound-player.mjs` | Testes |
| `web/package.json` | Encadear os testes novos em `npm test` |

## Planos seguintes (fora deste plano)

- **Plano 2 — Bancos calibrados:** `ferramentas/som/` (referências, order tracking, modelo físico offline, calibração) → `web/assets/som-v12-v1.*`, `som-v6-v1.*`, formato do `.bin`/manifesto e `test-sound-bank.mjs`. Ajusta `maxRiseRpmPerS`/`maxFallRpmPerS` dos perfis.
- **Plano 3 — V12 3D:** `ferramentas/v12/gerar_v12.py` → `web/assets/v12-v1.glb` + manifesto, `test-v12.mjs`.
- **Plano 4 — Aba 07 Som:** `engine-worklet.js`, `curve-editor.js`, `sound-studio.js`, template, build, camadas turbo/MGU-K, estalos ao aliviar sincronizados a θ, afinador medido, verificação no navegador.

---

### Task 1: Afinação (`tuning.mjs`)

**Files:**
- Create: `web/src/sound/tuning.mjs`
- Test: `web/test-tuning.mjs`
- Modify: `web/package.json` (script `test`)

**Interfaces:**
- Consumes: nada.
- Produces: `NOTE_NAMES: string[12]`; `firingHz(rpm: number, cylinders: int): number` (lança `RangeError`); `rpmForHz(hz: number, cylinders: int): number`; `midiToHz(midi: number): number`; `hzToNote(hz: number): {midi, nearest, name, octave, cents, label} | null`.

- [x] **Step 1: Escrever o teste que falha**

Criar `web/test-tuning.mjs`:

```js
import assert from 'node:assert/strict';
import {firingHz, rpmForHz, hzToNote, midiToHz, NOTE_NAMES} from './src/sound/tuning.mjs';

// Tabela da especificação (docs/superpowers/specs/2026-09-16-estudio-som-v12-design.md).
const table = [
  [4, 6000, 200, 'Sol 3', 35],
  [12, 6000, 600, 'Ré 5', 37],
  [12, 7000, 700, 'Fá 5', 4],
  [6, 15000, 750, 'Fá# 5', 23],
  [12, 17000, 1700, 'Sol# 6', 40],
];
for (const [cylinders, rpm, hz, label, cents] of table) {
  assert.equal(firingHz(rpm, cylinders), hz, `${cylinders} cilindros a ${rpm} RPM`);
  const note = hzToNote(hz);
  assert.equal(note.label, label, `nota de ${hz} Hz`);
  assert.equal(note.cents, cents, `cents de ${hz} Hz`);
  assert.equal(rpmForHz(hz, cylinders), rpm, `ida e volta de ${hz} Hz`);
}

assert.equal(firingHz(12000, 12), 2 * firingHz(12000, 6), 'V12 uma oitava acima do V6 na mesma rotação');
assert.equal(hzToNote(440).label, 'Lá 4');
assert.equal(hzToNote(261.6255653005986).label, 'Dó 4');
assert.equal(hzToNote(0), null);
assert.ok(Math.abs(midiToHz(69) - 440) < 1e-9);
assert.equal(NOTE_NAMES.length, 12);
assert.throws(() => firingHz(-1, 12), RangeError);
assert.throws(() => firingHz(6000, 0), RangeError);
assert.throws(() => firingHz(6000, 2.5), RangeError);

console.log('Afinação: fórmula RPM → Hz → nota e tabela da especificação OK.');
```

- [x] **Step 2: Rodar e ver falhar**

Run: `cd web && node test-tuning.mjs`
Expected: FAIL com `ERR_MODULE_NOT_FOUND` para `./src/sound/tuning.mjs`.

- [x] **Step 3: Implementar**

Criar `web/src/sound/tuning.mjs`:

```js
// Afinação de motor de 4 tempos com ignição uniforme: cada cilindro explode uma vez a cada 2 voltas.
export const NOTE_NAMES = Object.freeze(['Dó', 'Dó#', 'Ré', 'Ré#', 'Mi', 'Fá', 'Fá#', 'Sol', 'Sol#', 'Lá', 'Lá#', 'Si']);

export function firingHz(rpm, cylinders) {
  if (!Number.isFinite(rpm) || rpm < 0) throw new RangeError(`RPM inválido: ${rpm}`);
  if (!Number.isInteger(cylinders) || cylinders < 1) throw new RangeError(`Cilindros inválidos: ${cylinders}`);
  return (rpm / 60) * (cylinders / 2);
}

export function rpmForHz(hz, cylinders) {
  if (!Number.isFinite(hz) || hz < 0) throw new RangeError(`Frequência inválida: ${hz}`);
  if (!Number.isInteger(cylinders) || cylinders < 1) throw new RangeError(`Cilindros inválidos: ${cylinders}`);
  return (hz * 120) / cylinders;
}

export const midiToHz = (midi) => 440 * 2 ** ((midi - 69) / 12);

export function hzToNote(hz) {
  if (!Number.isFinite(hz) || hz <= 0) return null;
  const midi = 69 + 12 * Math.log2(hz / 440);
  const nearest = Math.round(midi);
  const name = NOTE_NAMES[((nearest % 12) + 12) % 12];
  const octave = Math.floor(nearest / 12) - 1;
  return {midi, nearest, name, octave, cents: Math.round((midi - nearest) * 100), label: `${name} ${octave}`};
}
```

- [x] **Step 4: Rodar e ver passar**

Run: `cd web && node test-tuning.mjs`
Expected: `Afinação: fórmula RPM → Hz → nota e tabela da especificação OK.`

- [x] **Step 5: Encadear no `npm test`**

Em `web/package.json`, trocar o fim do script `test`:

```json
"test": "node test-systems.mjs && node test-spares.mjs && node test-mechanics.mjs && node test-aerodynamics.mjs && node test-power-unit.mjs && node test-driver-model.mjs && node test-tuning.mjs"
```

Run: `cd web && npm test`
Expected: saída termina com a linha de Afinação OK; código de saída 0.

- [x] **Step 6: Commit**

```bash
git add web/src/sound/tuning.mjs web/test-tuning.mjs web/package.json
git commit -m "Adiciona afinação RPM, frequência e nota do estúdio de som"
```

---

### Task 2: Perfis e curva RPM × tempo

**Files:**
- Create: `web/src/sound/engine-profiles.mjs`
- Create: `web/src/sound/rpm-curve.mjs`
- Test: `web/test-rpm-curve.mjs`
- Modify: `web/package.json` (script `test`)

**Interfaces:**
- Consumes: nada.
- Produces:
  - `ENGINE_PROFILES: {v12_90s, v6_2026}` — cada perfil `{id, label, cylinders, bankAngleDeg, firingOrder: int[], crankingRpm, idleRpm, limitRpm, maxRiseRpmPerS, maxFallRpmPerS, layers: string[], bank: string}` (congelado).
  - `firingIntervalDeg(profile): number`; `firingWindowAt(profile, thetaDeg): int`; `cylinderAt(profile, thetaDeg): int`.
  - `createCurve({durationS?, maxRpm?, points?}): {durationS, maxRpm, points: [t, rpm][]}` (congelada; `points[0]` é `[0, 0]`).
  - `evaluateCurve(curve, tS): number`.
  - `createRpmFollower(profile, {physical?}): {step(targetRpm, dtS) → {rpm, load, running, cranking, limiter, rateLimited}, reset()}`.
  - `simulateCurve(curve, profile, {physical?, stepS?}): Array<{t, target, rpm, load, running, cranking, limiter, rateLimited}>`.
  - `curveToJSON(curve)`, `curveFromJSON(json | string)`, `CURVE_PRESETS: {linear, launch, blip, shifts, idle}` (cada `{label, curve}`), `presetCurve(id)`.
  - Constantes `CURVE_VERSION = 1`, `MIN_POINT_GAP_S = 0.01`, `TECH_MAX_RATE_RPM_PER_S = 200000`, `DURATION_RANGE_S = [0.5, 30]`.

- [x] **Step 1: Escrever o teste que falha**

Criar `web/test-rpm-curve.mjs`:

```js
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
```

- [x] **Step 2: Rodar e ver falhar**

Run: `cd web && node test-rpm-curve.mjs`
Expected: FAIL com `ERR_MODULE_NOT_FOUND` para `./src/sound/engine-profiles.mjs`.

- [x] **Step 3: Implementar os perfis**

Criar `web/src/sound/engine-profiles.mjs`:

```js
// Perfis dos motores do estúdio de som. Os valores de inércia são pontos de partida;
// o plano dos bancos calibrados os ajusta e registra no manifesto do banco.
const profile = (data) => Object.freeze({...data, firingOrder: Object.freeze([...data.firingOrder]), layers: Object.freeze([...data.layers])});

export const ENGINE_PROFILES = Object.freeze({
  v12_90s: profile({
    id: 'v12_90s', label: 'V12 anos 90', cylinders: 12, bankAngleDeg: 65,
    firingOrder: [1, 7, 5, 11, 3, 9, 6, 12, 2, 8, 4, 10],
    crankingRpm: 300, idleRpm: 4000, limitRpm: 17000,
    maxRiseRpmPerS: 40000, maxFallRpmPerS: 25000,
    layers: [], bank: './assets/som-v12-v1.json',
  }),
  v6_2026: profile({
    id: 'v6_2026', label: 'V6 2026', cylinders: 6, bankAngleDeg: 90,
    firingOrder: [1, 4, 2, 5, 3, 6],
    crankingRpm: 300, idleRpm: 4000, limitRpm: 15000,
    maxRiseRpmPerS: 30000, maxFallRpmPerS: 20000,
    layers: ['turbo', 'mguk'], bank: './assets/som-v6-v1.json',
  }),
});

export const firingIntervalDeg = (p) => 720 / p.cylinders;

/** Índice da janela de explosão (0..cilindros-1) que contém o ângulo θ do ciclo de 720°. */
export function firingWindowAt(p, thetaDeg) {
  const theta = ((thetaDeg % 720) + 720) % 720;
  return Math.min(p.cylinders - 1, Math.floor(theta / firingIntervalDeg(p)));
}

export const cylinderAt = (p, thetaDeg) => p.firingOrder[firingWindowAt(p, thetaDeg)];
```

- [x] **Step 4: Implementar a curva**

Criar `web/src/sound/rpm-curve.mjs`:

```js
// Curva RPM × tempo do estúdio de som: pontos editáveis, interpolação PCHIP monotônica,
// seguidor com limite físico, estado da partida e carga derivada da inclinação.
export const CURVE_VERSION = 1;
export const MIN_POINT_GAP_S = 0.01;
export const TECH_MAX_RATE_RPM_PER_S = 200000;
export const DURATION_RANGE_S = Object.freeze([0.5, 30]);

const clamp = (value, min, max) => Math.min(max, Math.max(min, value));

export function createCurve({durationS = 3, maxRpm = 12000, points} = {}) {
  if (!Number.isFinite(durationS)) throw new RangeError('Duração inválida');
  if (!Number.isFinite(maxRpm) || maxRpm <= 0) throw new RangeError('RPM máximo inválido');
  const duration = clamp(durationS, DURATION_RANGE_S[0], DURATION_RANGE_S[1]);
  const source = points ?? [[duration, maxRpm]];
  const cleaned = source
    .filter((p) => Array.isArray(p) && Number.isFinite(p[0]) && Number.isFinite(p[1]))
    .map(([t, rpm]) => [clamp(t, 0, duration), clamp(rpm, 0, maxRpm)])
    .filter(([t]) => t > 0)
    .sort((a, b) => a[0] - b[0]);
  const result = [[0, 0]];
  for (const point of cleaned) {
    if (point[0] - result[result.length - 1][0] >= MIN_POINT_GAP_S) result.push(point);
  }
  return Object.freeze({durationS: duration, maxRpm, points: Object.freeze(result.map((p) => Object.freeze(p)))});
}

// Fritsch–Carlson: tangentes que preservam a monotonicidade de cada trecho (sem picos inventados).
function tangents(points) {
  const n = points.length;
  const m = new Array(n).fill(0);
  if (n < 2) return m;
  const h = [], d = [];
  for (let i = 0; i < n - 1; i++) {
    h.push(points[i + 1][0] - points[i][0]);
    d.push((points[i + 1][1] - points[i][1]) / h[i]);
  }
  if (n === 2) return [d[0], d[0]];
  for (let i = 1; i < n - 1; i++) {
    if (d[i - 1] === 0 || d[i] === 0 || Math.sign(d[i - 1]) !== Math.sign(d[i])) continue;
    const w1 = 2 * h[i] + h[i - 1], w2 = h[i] + 2 * h[i - 1];
    m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i]);
  }
  // Pontas: fórmula de três pontos com correções que evitam ultrapassar o vizinho.
  const end = (h0, h1, d0, d1) => {
    const t = ((2 * h0 + h1) * d0 - h0 * d1) / (h0 + h1);
    if (Math.sign(t) !== Math.sign(d0)) return 0;
    if (Math.sign(d0) !== Math.sign(d1) && Math.abs(t) > Math.abs(3 * d0)) return 3 * d0;
    return t;
  };
  m[0] = end(h[0], h[1], d[0], d[1]);
  m[n - 1] = end(h[n - 2], h[n - 3], d[n - 2], d[n - 3]);
  return m;
}

export function evaluateCurve(curve, tS) {
  const {points} = curve;
  if (points.length === 1) return 0;
  const t = clamp(tS, 0, curve.durationS);
  const last = points[points.length - 1];
  if (t >= last[0]) return last[1];
  let i = 0;
  while (i < points.length - 2 && t >= points[i + 1][0]) i++;
  const [t0, y0] = points[i], [t1, y1] = points[i + 1];
  const m = tangents(points);
  const h = t1 - t0, s = (t - t0) / h;
  const h00 = 2 * s ** 3 - 3 * s ** 2 + 1, h10 = s ** 3 - 2 * s ** 2 + s, h01 = -2 * s ** 3 + 3 * s ** 2, h11 = s ** 3 - s ** 2;
  return clamp(h00 * y0 + h10 * h * m[i] + h01 * y1 + h11 * h * m[i + 1], 0, curve.maxRpm);
}

/** Segue um RPM alvo respeitando a inércia do perfil (ou só o teto técnico) e o limite de giro. */
export function createRpmFollower(profile, {physical = true} = {}) {
  let rpm = 0;
  const rise = physical ? profile.maxRiseRpmPerS : TECH_MAX_RATE_RPM_PER_S;
  const fall = physical ? profile.maxFallRpmPerS : TECH_MAX_RATE_RPM_PER_S;
  return {
    step(targetRpm, dtS) {
      const target = Math.max(0, targetRpm);
      const wanted = Math.min(target, profile.limitRpm);
      const delta = clamp(wanted - rpm, -fall * dtS, rise * dtS);
      const previous = rpm;
      rpm += delta;
      const running = rpm >= profile.idleRpm;
      const rate = dtS > 0 ? (rpm - previous) / dtS : 0;
      const reference = 0.25 * (rate >= 0 ? profile.maxRiseRpmPerS : profile.maxFallRpmPerS);
      return {
        rpm,
        load: clamp(0.5 + (0.5 * rate) / reference, 0, 1),
        running,
        cranking: !running && rpm > 0,
        limiter: target >= profile.limitRpm && rpm >= profile.limitRpm - 1e-6,
        rateLimited: Math.abs(wanted - previous) > Math.abs(delta) + 1e-9,
      };
    },
    reset() { rpm = 0; },
  };
}

export function simulateCurve(curve, profile, {physical = true, stepS = 0.001} = {}) {
  const follower = createRpmFollower(profile, {physical});
  const frames = [];
  const steps = Math.round(curve.durationS / stepS);
  for (let i = 0; i <= steps; i++) {
    const t = i * stepS;
    const target = evaluateCurve(curve, t);
    frames.push({t, target, ...follower.step(target, i === 0 ? 0 : stepS)});
  }
  return frames;
}

export const curveToJSON = (curve) => ({version: CURVE_VERSION, durationS: curve.durationS, maxRpm: curve.maxRpm, points: curve.points.map((p) => [...p])});

export function curveFromJSON(json) {
  const data = typeof json === 'string' ? JSON.parse(json) : json;
  if (!data || data.version !== CURVE_VERSION) throw new Error('Versão de curva não suportada');
  return createCurve(data);
}

export const CURVE_PRESETS = Object.freeze({
  linear: {label: 'Rampa linear 0–12.000', curve: {durationS: 3, maxRpm: 12000, points: [[3, 12000]]}},
  launch: {label: 'Largada de F1', curve: {durationS: 4, maxRpm: 12000, points: [[0.6, 4200], [1.4, 4200], [1.7, 10500], [2.6, 12000], [4, 12000]]}},
  blip: {label: 'Blip em ponto morto', curve: {durationS: 3, maxRpm: 12000, points: [[0.6, 4200], [1.2, 4200], [1.45, 11000], [2.1, 4200], [3, 4200]]}},
  shifts: {label: 'Trocas de marcha', curve: {durationS: 6, maxRpm: 12000, points: [[0.5, 4200], [1.6, 11500], [1.75, 8500], [2.9, 11500], [3.05, 9000], [4.2, 11500], [4.35, 9400], [6, 11800]]}},
  idle: {label: 'Marcha lenta estável', curve: {durationS: 4, maxRpm: 12000, points: [[0.6, 4200], [4, 4200]]}},
});

export const presetCurve = (id) => createCurve(CURVE_PRESETS[id].curve);
```

- [x] **Step 5: Rodar e ver passar**

Run: `cd web && node test-rpm-curve.mjs`
Expected: `Curva RPM: perfis, PCHIP, inércia, limitador, partida, carga, JSON e presets OK.`

- [x] **Step 6: Encadear no `npm test`**

Acrescentar ` && node test-rpm-curve.mjs` ao fim do script `test` em `web/package.json`.

Run: `cd web && npm test`
Expected: código de saída 0, com as linhas de Afinação e Curva RPM OK.

- [x] **Step 7: Commit**

```bash
git add web/src/sound/engine-profiles.mjs web/src/sound/rpm-curve.mjs web/test-rpm-curve.mjs web/package.json
git commit -m "Adiciona perfis V6/V12 e curva RPM editável com inércia"
```

---

### Task 3: Detector de f0 e reprodutor com fase travada

**Files:**
- Create: `web/src/sound/pitch.mjs`
- Create: `web/src/sound/phase-player.mjs`
- Create: `web/test-fixtures/sound-bank.mjs`
- Test: `web/test-sound-player.mjs`
- Modify: `web/package.json` (script `test`)

**Interfaces:**
- Consumes: `ENGINE_PROFILES`, `firingIntervalDeg` (Task 2); `firingHz` (Task 1).
- Produces:
  - `detectPitch(samples: Float32Array, sampleRate, {minHz?, maxHz?, threshold?}): {hz, confidence} | null`.
  - Formato de banco em memória: `{sampleRate, loops: [{rpm, load: 'on'|'off', samplesPerCycle, cycles: int, data: Float32Array}], starter?: {data: Float32Array}}`. Cada loop começa no pulso do cilindro 1 e contém `cycles` ciclos inteiros de 720°. O Plano 2 grava bancos neste formato.
  - `prepareBank(bank): {sampleRate, points: [{rpm, on, off}], starter}` (lança erro para banco incompleto).
  - `createPhasePlayer({bank, profile, sampleRate}): {thetaDeg (getter), render(out: Float32Array, state, gain = 1): Float32Array, reset()}` onde `state = {rpmFrom, rpmTo, load, running, cranking, limiter}` — exatamente os campos produzidos por `createRpmFollower().step()` mais `rpmFrom/rpmTo` do bloco.
  - `OUTPUT_CEILING` (−1 dBFS em amplitude linear).
  - Fixture: `createTestBank(profile, {sampleRate?, rpmPoints?, cycles?, withStarter?})`, `pulseCycle(profile, samplesPerCycle, amplitude)`.

- [x] **Step 1: Criar o banco sintético de teste**

Criar `web/test-fixtures/sound-bank.mjs`:

```js
// Banco sintético para testes: pulsos amortecidos em cada janela de explosão, com o cilindro 1
// levemente acentuado para permitir conferir o alinhamento. Não é o som do produto.
import {firingIntervalDeg} from '../src/sound/engine-profiles.mjs';

export function pulseCycle(profile, samplesPerCycle, amplitude) {
  const data = new Float32Array(samplesPerCycle);
  const window = (firingIntervalDeg(profile) / 720) * samplesPerCycle;
  const pulseLength = Math.max(8, Math.floor(window * 0.6));
  for (let k = 0; k < profile.cylinders; k++) {
    const start = Math.round(k * window);
    const accent = k === 0 ? 1.1 : 1;
    for (let i = 0; i < pulseLength && start + i < samplesPerCycle; i++) {
      const env = Math.sin((Math.PI * i) / pulseLength) * Math.exp((-4 * i) / pulseLength);
      data[start + i] += amplitude * accent * env;
    }
  }
  return data;
}

export function createTestBank(profile, {sampleRate = 48000, rpmPoints = [4000, 6000, 8000, 10000, 12000, 14000, 17000], cycles = 4, withStarter = false} = {}) {
  const loops = [];
  for (const nominal of rpmPoints) {
    const samplesPerCycle = Math.round((120 * sampleRate) / nominal);
    const rpm = (120 * sampleRate) / samplesPerCycle;
    for (const [load, amplitude] of [['on', 0.5], ['off', 0.2]]) {
      const cycleData = pulseCycle(profile, samplesPerCycle, amplitude);
      const data = new Float32Array(samplesPerCycle * cycles);
      for (let c = 0; c < cycles; c++) data.set(cycleData, c * samplesPerCycle);
      loops.push({rpm, load, samplesPerCycle, cycles, data});
    }
  }
  const starter = withStarter ? {data: Float32Array.from({length: sampleRate / 10}, (_, i) => 0.2 * Math.sin((2 * Math.PI * 40 * i) / sampleRate))} : undefined;
  return {sampleRate, loops, starter};
}
```

- [x] **Step 2: Escrever o teste que falha**

Criar `web/test-sound-player.mjs`:

```js
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
```

- [x] **Step 3: Rodar e ver falhar**

Run: `cd web && node test-sound-player.mjs`
Expected: FAIL com `ERR_MODULE_NOT_FOUND` para `./src/sound/pitch.mjs`.

- [x] **Step 4: Implementar o detector**

Criar `web/src/sound/pitch.mjs`:

```js
// Detector de frequência fundamental (YIN) usado pelo afinador e pelos testes do reprodutor.
export function detectPitch(samples, sampleRate, {minHz = 50, maxHz = 2500, threshold = 0.15} = {}) {
  const minLag = Math.max(2, Math.floor(sampleRate / maxHz));
  const maxLag = Math.min(Math.ceil(sampleRate / minHz), Math.floor(samples.length / 2));
  if (maxLag <= minLag + 1) return null;
  const window = samples.length - maxLag;
  const diff = new Float64Array(maxLag + 1);
  for (let lag = 1; lag <= maxLag; lag++) {
    let sum = 0;
    for (let i = 0; i < window; i++) { const d = samples[i] - samples[i + lag]; sum += d * d; }
    diff[lag] = sum;
  }
  const cmnd = new Float64Array(maxLag + 1);
  cmnd[0] = 1;
  let running = 0;
  for (let lag = 1; lag <= maxLag; lag++) { running += diff[lag]; cmnd[lag] = running > 0 ? (diff[lag] * lag) / running : 1; }
  let best = -1;
  for (let lag = minLag; lag < maxLag; lag++) {
    if (cmnd[lag] < threshold) {
      while (lag + 1 < maxLag && cmnd[lag + 1] < cmnd[lag]) lag++;
      best = lag;
      break;
    }
  }
  if (best < 0) {
    let lowest = Infinity;
    for (let lag = minLag; lag < maxLag; lag++) if (cmnd[lag] < lowest) { lowest = cmnd[lag]; best = lag; }
    if (lowest > 0.5) return null;
  }
  const a = cmnd[best - 1], b = cmnd[best], c = cmnd[best + 1];
  const denominator = a - 2 * b + c;
  const offset = denominator !== 0 ? (0.5 * (a - c)) / denominator : 0;
  return {hz: sampleRate / (best + offset), confidence: 1 - cmnd[best]};
}
```

- [x] **Step 5: Implementar o reprodutor**

Criar `web/src/sound/phase-player.mjs`:

```js
// Reprodutor de banco de loops com fase travada ao virabrequim.
// Cada loop guarda ciclos inteiros de 720° começando no pulso do cilindro 1; todos são lidos
// na mesma posição angular, então a mistura entre rotações vizinhas é coerente (sem phasing).
import {firingIntervalDeg} from './engine-profiles.mjs';

export const OUTPUT_CEILING = 10 ** (-1 / 20); // −1 dBFS
const LIMITER_RAMP_S = 0.002;
const STARTER_GAIN_RAMP_S = 0.05;

/**
 * Valida e ordena um banco em memória.
 * banco = {sampleRate, loops: [{rpm, load: 'on'|'off', samplesPerCycle, cycles, data: Float32Array}], starter?: {data: Float32Array}}
 */
export function prepareBank(bank) {
  if (!bank || !Number.isFinite(bank.sampleRate) || !Array.isArray(bank.loops)) throw new Error('Banco inválido');
  const byRpm = new Map();
  for (const loop of bank.loops) {
    if (loop.load !== 'on' && loop.load !== 'off') throw new Error(`Carga inválida: ${loop.load}`);
    if (!Number.isInteger(loop.cycles) || loop.cycles < 1) throw new Error('Loop sem ciclos inteiros');
    if (!(loop.data instanceof Float32Array) || loop.data.length < Math.floor(loop.samplesPerCycle * loop.cycles)) throw new Error('Loop menor que seus ciclos');
    const key = loop.rpm;
    if (!byRpm.has(key)) byRpm.set(key, {});
    byRpm.get(key)[loop.load] = loop;
  }
  const points = [...byRpm.entries()].sort((a, b) => a[0] - b[0]).map(([rpm, loads]) => {
    if (!loads.on || !loads.off) throw new Error(`Ponto ${rpm} RPM sem as duas cargas`);
    return {rpm, on: loads.on, off: loads.off};
  });
  if (points.length < 2) throw new Error('Banco precisa de pelo menos dois pontos de RPM');
  return {sampleRate: bank.sampleRate, points, starter: bank.starter ?? null};
}

// Hermite de 4 pontos com volta ao início do loop.
function readLoop(loop, position) {
  const length = Math.round(loop.samplesPerCycle * loop.cycles);
  const data = loop.data;
  const wrapped = ((position % length) + length) % length;
  const i = Math.floor(wrapped), f = wrapped - i;
  const xm1 = data[(i - 1 + length) % length], x0 = data[i], x1 = data[(i + 1) % length], x2 = data[(i + 2) % length];
  const c1 = 0.5 * (x1 - xm1), c2 = xm1 - 2.5 * x0 + 2 * x1 - 0.5 * x2, c3 = 0.5 * (x2 - xm1) + 1.5 * (x0 - x1);
  return ((c3 * f + c2) * f + c1) * f + x0;
}

export function createPhasePlayer({bank, profile, sampleRate}) {
  const prepared = prepareBank(bank);
  if (prepared.sampleRate !== sampleRate) throw new Error(`Banco em ${prepared.sampleRate} Hz; contexto em ${sampleRate} Hz`);
  const window = firingIntervalDeg(profile);
  const limiterStep = 1 / (LIMITER_RAMP_S * sampleRate);
  const starterStep = 1 / (STARTER_GAIN_RAMP_S * sampleRate);
  let theta = 0, cycle = 0, windowGain = 1, starterGain = 0, starterPosition = 0, firingCount = 0, lastWindow = 0;

  function mixAt(rpm, load) {
    const points = prepared.points;
    let hi = points.findIndex((p) => p.rpm >= rpm);
    if (hi <= 0) hi = hi === 0 ? 1 : points.length - 1;
    const a = points[hi - 1], b = points[hi];
    const w = Math.min(1, Math.max(0, (rpm - a.rpm) / (b.rpm - a.rpm)));
    const cyclePosition = theta / 720;
    const sample = (loop) => readLoop(loop, ((cycle % loop.cycles) + cyclePosition) * loop.samplesPerCycle);
    const at = (p) => load * sample(p.on) + (1 - load) * sample(p.off);
    return (1 - w) * at(a) + w * at(b);
  }

  return {
    get thetaDeg() { return theta; },
    /** out: Float32Array; state: {rpmFrom, rpmTo, load, running, cranking, limiter}; gain: ganho mestre. */
    render(out, state, gain = 1) {
      const frames = out.length;
      for (let n = 0; n < frames; n++) {
        const rpm = state.rpmFrom + ((state.rpmTo - state.rpmFrom) * n) / frames;
        const windowIndex = Math.floor(theta / window);
        if (windowIndex !== lastWindow) { firingCount++; lastWindow = windowIndex; }
        // Limitador: corta a ignição em janelas alternadas, com rampa curta para não estalar.
        const cut = state.limiter && firingCount % 2 === 1;
        windowGain += cut ? -Math.min(windowGain, limiterStep) : Math.min(1 - windowGain, limiterStep);
        let value = state.running ? mixAt(rpm, state.load) * windowGain : 0;
        const starterTarget = state.cranking && prepared.starter ? 1 : 0;
        starterGain += Math.sign(starterTarget - starterGain) * Math.min(Math.abs(starterTarget - starterGain), starterStep);
        if (starterGain > 0 && prepared.starter) {
          const data = prepared.starter.data;
          value += starterGain * data[Math.floor(starterPosition) % data.length];
          starterPosition += 1;
        }
        // Saturação suave com teto em −1 dBFS.
        out[n] = OUTPUT_CEILING * Math.tanh((value * gain) / OUTPUT_CEILING);
        theta += (rpm / 60) * 360 / sampleRate;
        if (theta >= 720) { theta -= 720; cycle++; }
      }
      return out;
    },
    reset() { theta = 0; cycle = 0; windowGain = 1; starterGain = 0; starterPosition = 0; firingCount = 0; lastWindow = 0; },
  };
}
```

- [x] **Step 6: Rodar e ver passar**

Run: `cd web && node test-sound-player.mjs`
Expected: `Reprodutor: afinação ±1%, crossfade sem phasing, carga, limitador, teto −1 dBFS, partida e rampa contínua OK.`

- [x] **Step 7: Conferir que os testes pegam erros (mutação manual, não commitar)**

1. Em `phase-player.mjs`, trocar `theta += (rpm / 60) * 360 / sampleRate;` por `* 720`. Rodar o teste → deve falhar com `medido ... Hz, esperado ... Hz`. Desfazer.
2. Trocar `const cut = state.limiter && firingCount % 2 === 1;` por `const cut = false;`. Rodar → deve falhar com `limitador reduziu só 0.00 dB`. Desfazer.

Run: `cd web && git diff --stat src/sound/phase-player.mjs`
Expected: nenhuma alteração pendente de mutação.

- [x] **Step 8: Encadear no `npm test` e rodar tudo**

Acrescentar ` && node test-sound-player.mjs` ao fim do script `test` em `web/package.json`.

Run: `cd web && npm test`
Expected: código de saída 0, com as linhas de Afinação, Curva RPM e Reprodutor OK.

- [x] **Step 9: Commit**

```bash
git add web/src/sound/pitch.mjs web/src/sound/phase-player.mjs web/test-fixtures/sound-bank.mjs web/test-sound-player.mjs web/package.json
git commit -m "Adiciona reprodutor de loops com fase travada e detector de afinação"
```
