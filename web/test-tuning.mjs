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
