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
