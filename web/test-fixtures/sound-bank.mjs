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
