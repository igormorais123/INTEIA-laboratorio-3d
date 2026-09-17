// Valida referencias.json sem rede: campos obrigatórios, licenças permitidas e hashes bem formados.
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

const manifest = JSON.parse(readFileSync(new URL('./referencias.json', import.meta.url), 'utf8'));
const ALLOWED_LICENSES = new Set(['CC0', 'CC BY-SA 3.0']);
const REQUIRED = ['id', 'file', 'use', 'engine', 'url', 'page', 'author', 'license', 'bytes', 'sha256'];

assert.equal(manifest.version, 1);
assert.ok(typeof manifest.userAgent === 'string' && manifest.userAgent.includes('INTEIA'));
assert.ok(Array.isArray(manifest.references) && manifest.references.length >= 4);

const ids = new Set();
for (const reference of manifest.references) {
  for (const field of REQUIRED) assert.ok(reference[field] !== undefined && reference[field] !== '', `${reference.id ?? '?'}: campo ${field} ausente`);
  assert.ok(!ids.has(reference.id), `id repetido: ${reference.id}`);
  ids.add(reference.id);
  assert.match(reference.id, /^[a-z0-9_]+$/);
  assert.ok(ALLOWED_LICENSES.has(reference.license), `${reference.id}: licença ${reference.license} fora da lista permitida`);
  assert.match(reference.sha256, /^[0-9a-f]{64}$/, `${reference.id}: sha256 inválido`);
  assert.ok(Number.isInteger(reference.bytes) && reference.bytes > 1000, `${reference.id}: bytes inválido`);
  assert.match(reference.url, /^https:\/\//);
  assert.match(reference.file, /\.(ogg|mp3|wav|flac)$/);
}
console.log(`Referências: ${manifest.references.length} fontes válidas (${[...new Set(manifest.references.map((r) => r.license))].join(', ')}).`);
