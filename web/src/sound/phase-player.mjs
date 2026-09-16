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
