// Baixa as gravações de referência listadas em referencias.json para .referencias/ (fora do Git)
// e confere bytes e SHA-256. O que já confere não é baixado de novo.
// Uso: node ferramentas/som/baixar-referencias.mjs [id ...]
import {createHash} from 'node:crypto';
import {existsSync, mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {dirname, join} from 'node:path';
import {fileURLToPath} from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const manifest = JSON.parse(readFileSync(join(here, 'referencias.json'), 'utf8'));
const outDir = join(here, '.referencias');
mkdirSync(outDir, {recursive: true});

const sha256 = (buffer) => createHash('sha256').update(buffer).digest('hex');
const wanted = new Set(process.argv.slice(2));

function check(reference, buffer) {
  const problems = [];
  if (buffer.length !== reference.bytes) problems.push(`bytes ${buffer.length} ≠ ${reference.bytes}`);
  const digest = sha256(buffer);
  if (digest !== reference.sha256) problems.push(`sha256 ${digest.slice(0, 16)}… ≠ ${reference.sha256.slice(0, 16)}…`);
  return problems;
}

let failures = 0;
for (const reference of manifest.references) {
  if (wanted.size && !wanted.has(reference.id)) continue;
  const target = join(outDir, reference.file);
  if (existsSync(target) && check(reference, readFileSync(target)).length === 0) {
    console.log(`= ${reference.id}: já conferido`);
    continue;
  }
  process.stdout.write(`↓ ${reference.id} … `);
  let buffer;
  try {
    const response = await fetch(reference.url, {headers: {'User-Agent': manifest.userAgent}, redirect: 'follow'});
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    buffer = Buffer.from(await response.arrayBuffer());
  } catch (error) {
    console.log(`falhou: ${error.message}`);
    failures++;
    continue;
  }
  const problems = check(reference, buffer);
  if (problems.length) {
    console.log(`divergente (${problems.join('; ')}); arquivo descartado`);
    failures++;
    continue;
  }
  writeFileSync(target, buffer);
  console.log(`ok (${(buffer.length / 1e6).toFixed(2)} MB)`);
}
if (failures) {
  console.error(`${failures} referência(s) não conferem. Verifique a rede ou atualize referencias.json se a fonte mudou.`);
  process.exit(1);
}
console.log(`Referências em ${outDir}`);
