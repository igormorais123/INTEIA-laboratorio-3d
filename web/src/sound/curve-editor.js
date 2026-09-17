// Editor da curva RPM × tempo: lógica de edição pura (testável no Node) + montagem em SVG sem dependências.
// Pontos: o primeiro é fixo em (0, 0); os demais são criados por clique, movidos por arraste ou teclado e
// apagados por duplo clique ou Delete. Pontos não cruzam o vizinho no tempo (MIN_POINT_GAP_S).
import {DURATION_RANGE_S, MIN_POINT_GAP_S, createCurve, evaluateCurve, simulateCurve} from './rpm-curve.mjs';
import {NOTE_NAMES, firingHz, hzToNote, midiToHz, rpmForHz} from './tuning.mjs';

const clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));

// ---------------------------------------------------------------- estado (puro)
export function createEditorState(init = {}) {
  const curve = createCurve(init);
  return {durationS: curve.durationS, maxRpm: curve.maxRpm, points: curve.points.map((p) => [...p])};
}

const normalize = (state, points) => createEditorState({durationS: state.durationS, maxRpm: state.maxRpm, points: points.slice(1)});

/** Insere um ponto; devolve o novo estado e o índice do ponto (ou −1 se não coube entre vizinhos). */
export function addPoint(state, t, rpm) {
  t = clamp(t, MIN_POINT_GAP_S, state.durationS); rpm = clamp(rpm, 0, state.maxRpm);
  if (state.points.some((p) => Math.abs(p[0] - t) < MIN_POINT_GAP_S)) return {state, index: -1};
  const next = normalize(state, [...state.points, [t, rpm]]);
  return {state: next, index: next.points.findIndex((p) => Math.abs(p[0] - t) < 1e-9)};
}

/** Move um ponto sem cruzar os vizinhos; o ponto 0 nunca sai de (0, 0). */
export function movePoint(state, index, t, rpm) {
  if (index <= 0 || index >= state.points.length) return state;
  const previous = state.points[index - 1][0], following = index + 1 < state.points.length ? state.points[index + 1][0] : state.durationS + MIN_POINT_GAP_S;
  const boundedT = clamp(t, previous + MIN_POINT_GAP_S, Math.min(state.durationS, following - MIN_POINT_GAP_S));
  const points = state.points.map((p, i) => (i === index ? [boundedT, clamp(rpm, 0, state.maxRpm)] : [...p]));
  return {...state, points};
}

export function removePoint(state, index) {
  if (index <= 0 || index >= state.points.length || state.points.length <= 2) return state;
  return {...state, points: state.points.filter((_, i) => i !== index)};
}

export function nudgePoint(state, index, dtS, dRpm) {
  const p = state.points[index];
  return p && index > 0 ? movePoint(state, index, p[0] + dtS, p[1] + dRpm) : state;
}

export function setDuration(state, durationS) {
  const duration = clamp(Number(durationS) || state.durationS, DURATION_RANGE_S[0], DURATION_RANGE_S[1]);
  const scale = duration / state.durationS;
  return normalize({...state, durationS: duration}, state.points.map(([t, rpm]) => [t * scale, rpm]));
}

export function setMaxRpm(state, maxRpm, limitRpm) {
  const max = clamp(Number(maxRpm) || state.maxRpm, 1000, limitRpm ?? 20000);
  return normalize({...state, maxRpm: max}, state.points.map(([t, rpm]) => [t, Math.min(rpm, max)]));
}

export const stateToCurve = (state) => createCurve(state);

/** Linhas de grade: uma por semitom cuja frequência de ignição cai dentro do eixo; rótulo nas notas naturais. */
export function noteGrid(profile, maxRpm) {
  const lines = [];
  const top = firingHz(maxRpm, profile.cylinders);
  for (let midi = 24; midi <= 120; midi++) {
    const hz = midiToHz(midi);
    if (hz > top) break;
    const rpm = rpmForHz(hz, profile.cylinders);
    if (rpm < maxRpm * 0.04) continue;
    const name = NOTE_NAMES[midi % 12], octave = Math.floor(midi / 12) - 1;
    lines.push({midi, rpm, hz, label: name.includes('#') ? '' : `${name}${octave}`, natural: !name.includes('#')});
  }
  return lines;
}

// ---------------------------------------------------------------- montagem em SVG
const NS = 'http://www.w3.org/2000/svg';
const W = 640, H = 300, PAD = {left: 58, right: 14, top: 12, bottom: 26};

export function mountCurveEditor(svg, {getState, setState, getProfile, onCommit = () => {}}) {
  svg.setAttribute('viewBox', `0 0 ${W} ${H}`);
  svg.setAttribute('role', 'application');
  svg.setAttribute('aria-label', 'Editor da curva de rotação por tempo. Clique para criar um ponto, arraste para mover, duplo clique ou Delete para apagar; setas movem o ponto focado.');
  const el = (tag, attrs = {}) => { const node = document.createElementNS(NS, tag); for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v); return node; };
  const gGrid = el('g', {class: 'curve-grid'}), gLimit = el('g', {class: 'curve-limit'}), pathReal = el('path', {class: 'curve-real'}), pathCurve = el('path', {class: 'curve-line'}), gPoints = el('g', {class: 'curve-points'}), playhead = el('line', {class: 'curve-playhead', y1: PAD.top, y2: H - PAD.bottom}), gAxis = el('g', {class: 'curve-axis'});
  svg.replaceChildren(gGrid, gLimit, pathReal, pathCurve, gPoints, playhead, gAxis);
  const plotW = W - PAD.left - PAD.right, plotH = H - PAD.top - PAD.bottom;
  const x = (t) => PAD.left + (t / getState().durationS) * plotW;
  const y = (rpm) => PAD.top + (1 - rpm / getState().maxRpm) * plotH;
  const fromPixel = (clientX, clientY) => {
    const rect = svg.getBoundingClientRect();
    const px = ((clientX - rect.left) / rect.width) * W, py = ((clientY - rect.top) / rect.height) * H;
    return {t: clamp(((px - PAD.left) / plotW) * getState().durationS, 0, getState().durationS), rpm: clamp((1 - (py - PAD.top) / plotH) * getState().maxRpm, 0, getState().maxRpm)};
  };
  let focused = -1, dragging = -1, cachedSim = null, simKey = '';

  function pathFor(samples) { return samples.map((p, i) => `${i ? 'L' : 'M'}${x(p[0]).toFixed(1)} ${y(p[1]).toFixed(1)}`).join(' '); }

  function render(playheadT = null) {
    const state = getState(), profile = getProfile(), curve = stateToCurve(state);
    gGrid.replaceChildren();
    for (const line of noteGrid(profile, state.maxRpm)) {
      const yy = y(line.rpm);
      gGrid.append(el('line', {x1: PAD.left, x2: W - PAD.right, y1: yy, y2: yy, class: line.natural ? 'natural' : 'sharp'}));
      if (line.label) { const text = el('text', {x: PAD.left - 6, y: yy + 3, 'text-anchor': 'end'}); text.textContent = `${line.label} · ${Math.round(line.hz)} Hz`; gGrid.append(text); }
    }
    gAxis.replaceChildren();
    for (let i = 0; i <= 4; i++) {
      const t = (state.durationS * i) / 4; const text = el('text', {x: x(t), y: H - 8, 'text-anchor': i === 0 ? 'start' : i === 4 ? 'end' : 'middle'}); text.textContent = `${t.toFixed(1)} s`; gAxis.append(text);
    }
    const rpmText = el('text', {x: PAD.left + 4, y: PAD.top + 10, class: 'axis-title'}); rpmText.textContent = `RPM · até ${state.maxRpm.toLocaleString('pt-BR')}`; gAxis.append(rpmText);
    gLimit.replaceChildren();
    if (profile.limitRpm < state.maxRpm) { const yy = y(profile.limitRpm); gLimit.append(el('line', {x1: PAD.left, x2: W - PAD.right, y1: yy, y2: yy})); const text = el('text', {x: W - PAD.right, y: yy - 4, 'text-anchor': 'end'}); text.textContent = 'limite de giro'; gLimit.append(text); }
    const steps = 160, samples = [];
    for (let i = 0; i <= steps; i++) { const t = (state.durationS * i) / steps; samples.push([t, evaluateCurve(curve, t)]); }
    pathCurve.setAttribute('d', pathFor(samples));
    const key = JSON.stringify([state, profile.id]);
    if (key !== simKey) { simKey = key; cachedSim = simulateCurve(curve, profile, {physical: true, stepS: 0.01}).map((f) => [f.t, f.rpm]); }
    pathReal.setAttribute('d', pathFor(cachedSim));
    gPoints.replaceChildren();
    state.points.forEach((p, i) => {
      const circle = el('circle', {cx: x(p[0]), cy: y(p[1]), r: i === 0 ? 4 : 7, class: i === 0 ? 'fixed' : focused === i ? 'focused' : '', tabindex: i === 0 ? -1 : 0, role: 'slider', 'aria-label': `Ponto ${i}: ${p[0].toFixed(2)} s, ${Math.round(p[1])} RPM`, 'aria-valuenow': Math.round(p[1]), 'aria-valuemin': 0, 'aria-valuemax': state.maxRpm, 'data-index': i});
      gPoints.append(circle);
    });
    setPlayhead(playheadT);
  }
  function setPlayhead(playheadT) {
    if (playheadT === null || playheadT === undefined) playhead.setAttribute('visibility', 'hidden');
    else { playhead.setAttribute('visibility', 'visible'); playhead.setAttribute('x1', x(playheadT)); playhead.setAttribute('x2', x(playheadT)); }
  }

  function commit() { onCommit(getState()); }

  svg.addEventListener('pointerdown', (event) => {
    const target = event.target.closest?.('circle[data-index]');
    if (target) {
      const index = Number(target.dataset.index);
      if (index === 0) return;
      focused = index; dragging = index; svg.setPointerCapture(event.pointerId); target.focus(); render(); event.preventDefault();
      return;
    }
    if (event.target === svg || event.target.closest('g') === gGrid || event.target === pathCurve || event.target === pathReal) {
      const {t, rpm} = fromPixel(event.clientX, event.clientY);
      const result = addPoint(getState(), t, rpm);
      if (result.index >= 0) { setState(result.state); focused = result.index; dragging = result.index; svg.setPointerCapture(event.pointerId); render(); }
    }
  });
  svg.addEventListener('pointermove', (event) => {
    if (dragging < 0) return;
    const {t, rpm} = fromPixel(event.clientX, event.clientY);
    setState(movePoint(getState(), dragging, t, rpm)); render();
  });
  const endDrag = () => { if (dragging >= 0) { dragging = -1; commit(); } };
  svg.addEventListener('pointerup', endDrag); svg.addEventListener('pointercancel', endDrag);
  svg.addEventListener('dblclick', (event) => {
    const target = event.target.closest?.('circle[data-index]'); if (!target) return;
    const index = Number(target.dataset.index); setState(removePoint(getState(), index)); focused = -1; render(); commit();
  });
  svg.addEventListener('focusin', (event) => { const target = event.target.closest?.('circle[data-index]'); if (target) { focused = Number(target.dataset.index); render(); } });
  svg.addEventListener('keydown', (event) => {
    if (focused <= 0) return;
    const state = getState(), big = event.shiftKey, dt = big ? 0.25 : 0.05, dr = big ? 500 : 100;
    let next = null;
    if (event.key === 'ArrowLeft') next = nudgePoint(state, focused, -dt, 0);
    if (event.key === 'ArrowRight') next = nudgePoint(state, focused, dt, 0);
    if (event.key === 'ArrowUp') next = nudgePoint(state, focused, 0, dr);
    if (event.key === 'ArrowDown') next = nudgePoint(state, focused, 0, -dr);
    if (event.key === 'Delete' || event.key === 'Backspace') { next = removePoint(state, focused); focused = -1; }
    if (next) { event.preventDefault(); setState(next); render(); commit(); const circle = gPoints.querySelector(`circle[data-index="${focused}"]`); circle?.focus(); }
  });
  render();
  return {render, setPlayhead, get focused() { return focused; }};
}

/** Texto do afinador para um RPM: frequência de ignição e nota com cents. */
export function describeTuning(profile, rpm) {
  const hz = rpm > 0 ? firingHz(rpm, profile.cylinders) : 0;
  const note = hz > 0 ? hzToNote(hz) : null;
  return {hz, note};
}
