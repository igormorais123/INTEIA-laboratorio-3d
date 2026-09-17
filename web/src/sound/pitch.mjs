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

// Potência de um tom em `hz` por Goertzel (janela Hann), sem depender da grade de bins de uma FFT.
function goertzelPower(samples, sampleRate, hz) {
  const n = samples.length;
  const w = (2 * Math.PI * hz) / sampleRate, coefficient = 2 * Math.cos(w);
  let s0 = 0, s1 = 0, s2 = 0;
  for (let i = 0; i < n; i++) {
    const window = 0.5 - 0.5 * Math.cos((2 * Math.PI * i) / n);
    s0 = samples[i] * window + coefficient * s1 - s2;
    s2 = s1; s1 = s0;
  }
  return s1 * s1 + s2 * s2 - coefficient * s1 * s2;
}

/**
 * Frequência de ignição por soma harmônica: entre minHz e maxHz, escolhe a frequência cujos primeiros
 * harmônicos somam mais energia. Imune às subordens do motor (ordem de bancada, meias ordens), que
 * puxam o YIN para baixo ou o enviesam; é o detector do afinador para sons de motor.
 */
export function detectFiringHz(samples, sampleRate, {minHz = 100, maxHz = 2000, harmonics = 6, stepRatio = 1.004} = {}) {
  if (!(maxHz > minHz) || samples.length < 256) return null;
  const score = (hz) => {
    let total = 0;
    for (let k = 1; k <= harmonics; k++) {
      if (k * hz >= sampleRate / 2) break;
      total += Math.log10(goertzelPower(samples, sampleRate, k * hz) + 1e-20);
    }
    return total;
  };
  let bestHz = minHz, best = -Infinity;
  for (let hz = minHz; hz <= maxHz; hz *= stepRatio) {
    const s = score(hz);
    if (s > best) { best = s; bestHz = hz; }
  }
  // Refino: grade fina (0,05 %) em torno do melhor candidato
  const fine = stepRatio ** 0.125;
  let refinedHz = bestHz, refined = best;
  for (let hz = bestHz / stepRatio; hz <= bestHz * stepRatio; hz *= fine) {
    const s = score(hz);
    if (s > refined) { refined = s; refinedHz = hz; }
  }
  return {hz: refinedHz, score: refined};
}
