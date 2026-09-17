// Voz completa do motor, sem DOM e sem Web Audio: reprodutor com fase travada + seguidor de RPM + partida,
// desvio natural de rotação, camadas em tempo real (turbo e MGU-K no V6, estalos ao aliviar) e ambiente do
// box (reflexões e cauda curta). É o mesmo código que roda no AudioWorklet do site e nos demos do Node.
import {createPhasePlayer, OUTPUT_CEILING} from './phase-player.mjs';
import {createCurve, createRpmFollower, evaluateCurve} from './rpm-curve.mjs';
import {firingIntervalDeg} from './engine-profiles.mjs';

const CRANK_SECONDS = 0.7;

function lcg(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }

// Ressonador de 2 polos (passa-banda) para tons "de ar": ruído filtrado em vez de senóide pura.
function createResonator(sampleRate) {
  let y1 = 0, y2 = 0;
  return {
    tick(input, hz, q) {
      const w = (2 * Math.PI * Math.min(hz, sampleRate * 0.45)) / sampleRate, r = Math.exp(-w / (2 * q));
      const a1 = -2 * r * Math.cos(w), a2 = r * r, gain = (1 - r) * 0.5;
      const y = gain * input - a1 * y1 - a2 * y2;
      y2 = y1; y1 = y;
      return y;
    },
  };
}

// Ambiente do box: quatro reflexões primeiras com perda de agudos, dois pentes curtos e um passa-tudo.
function createAmbience(sampleRate) {
  const ms = (v) => Math.round((v / 1000) * sampleRate);
  const taps = [[ms(7.1), 0.5], [ms(11.3), 0.42], [ms(16.7), 0.33], [ms(23.3), 0.26]];
  const size = ms(60), line = new Float32Array(size); let write = 0, lp = 0;
  const combs = [[ms(29.7), 0.58], [ms(37.1), 0.55], [ms(41.1), 0.52]].map(([len, fb]) => ({buffer: new Float32Array(len), index: 0, fb, damp: 0}));
  const allpass = {buffer: new Float32Array(ms(5.0)), index: 0, g: 0.5};
  return {
    tick(x) {
      line[write] = x;
      let early = 0;
      for (const [delay, gain] of taps) early += line[(write - delay + size) % size] * gain;
      lp += (early - lp) * 0.35;
      let tail = 0;
      for (const comb of combs) {
        const y = comb.buffer[comb.index];
        comb.damp += (y - comb.damp) * 0.3;
        comb.buffer[comb.index] = lp * 0.4 + comb.damp * comb.fb;
        comb.index = (comb.index + 1) % comb.buffer.length;
        tail += y;
      }
      const ap = allpass.buffer[allpass.index], v = tail * 0.33 + ap * allpass.g;
      allpass.buffer[allpass.index] = v; allpass.index = (allpass.index + 1) % allpass.buffer.length;
      const out = ap - allpass.g * v;
      write = (write + 1) % size;
      return lp * 0.6 + out;
    },
  };
}

/**
 * createEngineVoice({bank, profile, sampleRate, seed}) → {setState, setCurve, play, stop, render(out) → status}
 * Estado: {mode: 'curve'|'free', power, throttle 0..1, fixedRpm|null, physical, volume 0..1, loop, ambience 0..1}.
 */
export function createEngineVoice({bank, profile, sampleRate, seed = 12345}) {
  const player = createPhasePlayer({bank, profile, sampleRate});
  let follower = createRpmFollower(profile, {physical: true});
  const random = lcg(seed);
  const state = {mode: 'free', power: false, throttle: 0, fixedRpm: null, physical: true, volume: 0.35, loop: false, ambience: 0.22};
  let curve = null, playing = false, t = 0, ignition = 'off', crankT = 0;
  let last = {rpm: 0, load: 0.5, running: false, cranking: false, limiter: false, rateLimited: false};
  let wanderA = 0, wanderB = 0, turbo = 0, wastegate = 0, pop = 0, lastLoad = 0.5;
  const whistle = createResonator(sampleRate), whistle2 = createResonator(sampleRate), mguk = createResonator(sampleRate), ambience = createAmbience(sampleRate);
  const interval = firingIntervalDeg(profile);

  function targetRpm(dt) {
    if (ignition === 'off') return 0;
    if (ignition === 'cranking') { crankT += dt; if (crankT < CRANK_SECONDS) return profile.crankingRpm; ignition = 'running'; }
    if (state.mode === 'curve') {
      if (!playing) return state.power ? profile.idleRpm : 0;
      if (!curve) return profile.idleRpm;
      const value = evaluateCurve(curve, t);
      t += dt;
      if (t > curve.durationS) { if (state.loop) t = 0; else { playing = false; if (!state.power) ignition = 'off'; } }
      return Math.max(value, t < 0.02 ? profile.crankingRpm : 0);
    }
    if (!state.power) return 0;
    if (state.fixedRpm !== null && Number.isFinite(state.fixedRpm)) return state.fixedRpm;
    return profile.idleRpm + state.throttle * (profile.limitRpm - profile.idleRpm);
  }

  // Desvio lento de rotação: maior em marcha lenta e aliviado, quase nulo em carga plena no limite.
  function wander(dt, rpm, load) {
    wanderA += (random() - 0.5) * 0.9 * dt * 60; wanderA *= Math.exp(-dt * 2.2);
    wanderB += (random() - 0.5) * 2.4 * dt * 60; wanderB *= Math.exp(-dt * 7.0);
    const span = Math.max(0, (rpm - profile.idleRpm) / (profile.limitRpm - profile.idleRpm));
    const amount = (0.011 * (1 - span) + 0.0015) * (1.2 - 0.6 * load);
    return 1 + Math.max(-0.03, Math.min(0.03, (wanderA + 0.5 * wanderB) * amount));
  }

  function layers(out, next, dt) {
    const frames = out.length, volume = state.volume, running = next.running;
    if (running && next.load < 0.25 && next.rpm > 0.55 * profile.limitRpm) {
      const windows = (frames * (next.rpm / 60) * 360) / sampleRate / interval;
      if (random() < Math.min(0.5, 0.06 * windows)) pop = 0.6 + 0.4 * random();
    }
    if (pop > 0.001) for (let i = 0; i < frames; i++) { out[i] += (random() * 2 - 1) * pop * 0.16 * volume; pop *= 0.985; }
    if (!profile.layers.length) return;
    const turboTarget = running ? (0.25 + 0.75 * next.load) * (next.rpm / profile.limitRpm) : 0;
    turbo += (turboTarget - turbo) * (1 - Math.exp(-dt / 0.6));
    if (lastLoad - next.load > 0.35 && turbo > 0.3) wastegate = Math.max(wastegate, turbo);
    lastLoad = next.load;
    const whistleHz = 2200 + 8000 * turbo, whistleGain = 0.9 * turbo * volume, mgukHz = ((next.rpm * 3.33) / 60) * 2, mgukGain = running ? 0.35 * volume * (0.4 + 0.6 * next.load) : 0, gateGain = 0.07 * wastegate * volume;
    for (let i = 0; i < frames; i++) {
      const n = random() * 2 - 1;
      let v = whistle.tick(n, whistleHz, 28) * whistleGain + whistle2.tick(n, whistleHz * 1.62, 22) * whistleGain * 0.5 + mguk.tick(n, mgukHz, 18) * mgukGain;
      if (gateGain > 1e-4) v += n * gateGain;
      out[i] += v;
    }
    wastegate *= Math.exp(-dt / 0.25);
  }

  return {
    get state() { return {...state}; },
    get playing() { return playing; },
    get ignition() { return ignition; },
    setState(partial) {
      const physicalChanged = 'physical' in partial && partial.physical !== state.physical;
      Object.assign(state, partial);
      if (physicalChanged && last.rpm < 1) follower = createRpmFollower(profile, {physical: state.physical});
      if ('power' in partial) { if (partial.power) { if (ignition === 'off') { ignition = 'cranking'; crankT = 0; } } else if (!playing) ignition = 'off'; }
    },
    setCurve(json) { curve = createCurve(json); },
    play() { playing = true; t = 0; if (ignition === 'off') { ignition = 'cranking'; crankT = 0; } },
    stop() { playing = false; t = 0; if (!state.power) ignition = 'off'; },
    /** Preenche `out` (Float32Array) e devolve o estado do motor no fim do bloco. */
    render(out) {
      const frames = out.length, dt = frames / sampleRate;
      const next = follower.step(targetRpm(dt), dt);
      if (ignition === 'off' && next.rpm < 1) next.cranking = false;
      const factor = next.running ? wander(dt, next.rpm, next.load) : 1;
      player.render(out, {rpmFrom: last.rpm * (last.factor ?? 1), rpmTo: next.rpm * factor, load: next.load, running: next.running, cranking: next.cranking, limiter: next.limiter}, state.volume);
      layers(out, next, dt);
      const mix = state.ambience;
      for (let i = 0; i < frames; i++) {
        const dry = out[i], wet = ambience.tick(dry);
        out[i] = OUTPUT_CEILING * Math.tanh((dry * (1 - 0.35 * mix) + wet * mix) / OUTPUT_CEILING);
      }
      last = {...next, factor};
      return {rpm: next.rpm, load: next.load, running: next.running, cranking: next.cranking, limiter: next.limiter, rateLimited: next.rateLimited, thetaDeg: player.thetaDeg, t, playing, ignition, power: state.power, mode: state.mode};
    },
  };
}
