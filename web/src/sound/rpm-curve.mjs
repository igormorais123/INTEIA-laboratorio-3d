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
