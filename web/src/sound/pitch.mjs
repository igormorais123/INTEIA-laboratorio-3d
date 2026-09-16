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
