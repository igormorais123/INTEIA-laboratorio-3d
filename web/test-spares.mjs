import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import {SPARE_SLOTS, SPARE_PRESETS, SPARE_INFO, SPARES_ASSET} from './src/spares.js';

const read = (path) => readFileSync(new URL(path, import.meta.url));
const manifest = JSON.parse(read('./assets/sobressalentes-v1.manifest.json'));
const glb = read('./assets/sobressalentes-v1.glb');

// Asset íntegro e coerente com o manifesto
assert.equal(glb.subarray(0, 4).toString('ascii'), 'glTF', 'GLB inválido');
assert.equal(createHash('sha256').update(glb).digest('hex'), manifest.sha256, 'sha256 do manifesto divergente do GLB');
assert.equal(glb.length, manifest.bytes);
assert.ok(glb.length < 25 * 1024 * 1024, 'GLB acima do limite de 25 MiB do ambiente de publicação');
assert.equal(SPARES_ASSET, './assets/sobressalentes-v1.glb');

// Catálogo do site espelha os slots e variantes do gerador
for (const slot of SPARE_SLOTS) {
  const generated = manifest.slots[slot.id];
  assert.ok(generated, `slot ${slot.id} ausente no manifesto`);
  assert.deepEqual(slot.variants.map(([id]) => id), generated.variants, `variantes de ${slot.id} divergem do manifesto`);
  for (const [variant] of slot.variants) if (variant !== 'original') assert.ok(SPARE_INFO[slot.id]?.[variant]?.length === 2, `${slot.id}/${variant} sem função e curiosidade`);
}
for (const preset of SPARE_PRESETS) {
  for (const slot of SPARE_SLOTS) assert.ok(slot.variants.some(([id]) => id === preset.setup[slot.id]), `preset ${preset.id}: variante inválida em ${slot.id}`);
}

// Nós gerados: alvos existentes no carro v2 e geometria no lugar da peça original
const carTargets = new Set(['front_tire__01', 'front_tire__02', 'rear_tire__01', 'rear_tire__02', 'rear_wing_main_part__01', 'rear_wing_drs__01', 'front_wing_top__01', 'rear_wing_bottom_holder__01', 'main_body__01']);
const byKey = new Map();
for (const entry of manifest.entries) {
  assert.ok(carTargets.has(entry.target), `alvo desconhecido: ${entry.target}`);
  assert.ok(['geometry', 'attach'].includes(entry.mode));
  const key = `${entry.slot}/${entry.variant}`;
  byKey.set(key, (byKey.get(key) || 0) + 1);
}
for (const variant of ['macio', 'medio', 'duro', 'intermediario', 'chuva']) assert.equal(byKey.get(`tyres/${variant}`), 4, `pneus ${variant}: quatro rodas`);
for (const variant of ['baixa', 'alta']) { assert.equal(byKey.get(`rear_wing/${variant}`), 2, `asa traseira ${variant}: plano + flap`); assert.equal(byKey.get(`front_wing/${variant}`), 1); }
assert.equal(byKey.get('beam_wing/dupla'), 1); assert.equal(byKey.get('cooling/aberto'), 1);

const near = (entry, box, tol = .06) => entry.min.every((v, i) => v > box[0][i] - tol) && entry.max.every((v, i) => v < box[1][i] + tol);
for (const entry of manifest.entries) {
  if (entry.slot === 'tyres') {
    const front = entry.target.startsWith('front');
    const z = front ? 1.52 : -1.84, r = front ? .329 : .341;
    assert.ok(Math.abs((entry.min[2] + entry.max[2]) / 2 - z) < .01 && Math.abs((entry.max[1] - entry.min[1]) / 2 - r) < .01, `${entry.node}: pneu fora do cubo da roda`);
  }
  if (entry.target === 'rear_wing_main_part__01') assert.ok(near(entry, [[-.62, .66, -2.42], [.62, .78, -2.0]]), `${entry.node}: plano principal fora do envelope da asa traseira`);
  if (entry.target === 'rear_wing_drs__01') assert.ok(near(entry, [[-.62, .70, -2.45], [.62, .90, -2.18]]), `${entry.node}: flap fora do envelope`);
  if (entry.target === 'front_wing_top__01') assert.ok(near(entry, [[-.66, .12, 2.05], [.66, .32, 2.30]]), `${entry.node}: flap dianteiro fora do envelope`);
  if (entry.target === 'rear_wing_bottom_holder__01') assert.ok(near(entry, [[-.45, .34, -2.40], [.45, .52, -2.05]]), `${entry.node}: asa de viga fora do envelope`);
  if (entry.target === 'main_body__01') assert.ok(near(entry, [[-.35, .70, -1.0], [.35, 1.0, -.45]]), `${entry.node}: venezianas fora da tampa do motor`);
}

// Interface: controles presentes no template
const template = readFileSync(new URL('./src/template-v2.html', import.meta.url), 'utf8');
for (const id of ['spare-presets', 'spare-slots', 'spare-info', 'spare-status']) assert.ok(template.includes(`id="${id}"`), `template sem #${id}`);

console.log(`Sobressalentes: ${manifest.totals.nodes} peças, ${manifest.totals.triangles} triângulos, ${SPARE_SLOTS.length} slots, ${SPARE_PRESETS.length} cenários OK.`);
