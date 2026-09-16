/** Empacotamento meshopt sem perda do asset dos sistemas internos. */
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const toolRoot = process.env.F1_ASSET_TOOL_ROOT;
const file = process.env.SISTEMAS_GLB;
if (!toolRoot) throw new Error('Defina F1_ASSET_TOOL_ROOT com @gltf-transform e meshoptimizer instalados.');
if (!file) throw new Error('Defina SISTEMAS_GLB.');

const require = createRequire(path.join(toolRoot, 'package.json'));
const load = async (name) => import(pathToFileURL(require.resolve(name)).href);
const {NodeIO} = await load('@gltf-transform/core');
const {ALL_EXTENSIONS, EXTMeshoptCompression} = await load('@gltf-transform/extensions');
const {MeshoptEncoder, MeshoptDecoder} = await load('meshoptimizer');
let functions = null;
try {
  functions = await load('@gltf-transform/functions');
} catch {
  // A deduplicação é opcional; a compressão meshopt continua disponível.
}

await Promise.all([MeshoptEncoder.ready, MeshoptDecoder.ready]);
const io = new NodeIO()
  .registerExtensions(ALL_EXTENSIONS)
  .registerDependencies({'meshopt.encoder': MeshoptEncoder, 'meshopt.decoder': MeshoptDecoder});

const document = await io.read(file);
const before = fs.statSync(file).size;
const root = document.getRoot();
const systemNames = (docRoot) => docRoot.listNodes().filter((node) => /^system_/.test(node.getName())).map((node) => node.getName()).sort();
const partCount = (docRoot) => docRoot.listNodes().filter((node) => node.getExtras()?.part).length;
const systemsBefore = systemNames(root);
const partsBefore = partCount(root);

if (functions?.dedup) await document.transform(functions.dedup());
document.createExtension(EXTMeshoptCompression)
  .setRequired(true)
  .setEncoderOptions({method: EXTMeshoptCompression.EncoderMethod.QUANTIZE});

const bytes = await io.writeBinary(document);
const decoded = await io.readBinary(bytes);
const systemsAfter = systemNames(decoded.getRoot());
const partsAfter = partCount(decoded.getRoot());
if (JSON.stringify(systemsBefore) !== JSON.stringify(systemsAfter)) throw new Error('Nós de sistema perdidos na compressão.');
if (partsBefore !== partsAfter) throw new Error(`Peças perdidas na compressão: ${partsBefore} -> ${partsAfter}.`);

const output = Buffer.from(bytes.buffer, bytes.byteOffset, bytes.byteLength);
fs.writeFileSync(file, output);

const manifestPath = file.replace(/\.glb$/i, '.manifest.json');
if (manifestPath === file || !fs.existsSync(manifestPath)) throw new Error(`Manifesto correspondente não encontrado: ${manifestPath}`);
const jsonLength = output.readUInt32LE(12);
const gltf = JSON.parse(output.subarray(20, 20 + jsonLength));
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
manifest.totals = {
  ...manifest.totals,
  meshes: gltf.meshes?.length ?? 0,
  nodes: gltf.nodes?.length ?? 0,
  materials: gltf.materials?.length ?? 0,
  images: gltf.images?.length ?? 0,
  bytes: output.byteLength,
  raw_bytes: manifest.totals?.raw_bytes ?? before,
};
manifest.extensions_required = gltf.extensionsRequired ?? [];
manifest.extensions_used = gltf.extensionsUsed ?? [];
manifest.optimized = true;
manifest.sha256 = createHash('sha256').update(output).digest('hex');
const temporaryManifest = `${manifestPath}.tmp-${process.pid}`;
fs.writeFileSync(temporaryManifest, `${JSON.stringify(manifest, null, 1)}\n`, 'utf8');
fs.renameSync(temporaryManifest, manifestPath);

console.log(`MESHOPT_OK ${JSON.stringify({before, after: output.byteLength, systems: systemsAfter.length, parts: partsAfter})}`);
