// Exporta a geometria de um GLB exatamente como o GLTFLoader do site a entrega:
// mesma ordem de malhas (traverse), mesma ordem de vértices, posições no mundo.
// O Blender assa a oclusão nesses vértices e devolve um byte por vértice.
//
// node ferramentas/realismo/exportar_malhas.mjs <entrada.glb> <saida.bin>
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';
import {pathToFileURL} from 'node:url';

const require = createRequire(path.resolve('web/package.json'));
const THREE = await import(pathToFileURL(require.resolve('three')).href);
const {GLTFLoader} = await import(pathToFileURL(require.resolve('three/addons/loaders/GLTFLoader.js')).href);
const {MeshoptDecoder} = await import(pathToFileURL(require.resolve('three/addons/libs/meshopt_decoder.module.js')).href);

export async function loadGeometryOnly(file) {
  const b = fs.readFileSync(file), len = b.readUInt32LE(12), j = JSON.parse(b.subarray(20, 20 + len));
  // Materiais e imagens não importam para a oclusão e o Node não decodifica WebP.
  j.materials = [{}]; delete j.images; delete j.textures; delete j.samplers;
  j.extensionsUsed = (j.extensionsUsed || []).filter(e => /meshopt|quantization/i.test(e));
  j.extensionsRequired = (j.extensionsRequired || []).filter(e => /meshopt|quantization/i.test(e));
  for (const m of j.meshes) for (const p of m.primitives) p.material = 0;
  const json = Buffer.from(JSON.stringify(j)), pad = Buffer.alloc(Math.ceil(json.length / 4) * 4, 32); json.copy(pad);
  const tail = b.subarray(20 + len), out = Buffer.alloc(20 + pad.length + tail.length);
  b.copy(out, 0, 0, 12); out.writeUInt32LE(out.length, 8); out.writeUInt32LE(pad.length, 12); out.writeUInt32LE(0x4e4f534a, 16);
  pad.copy(out, 20); tail.copy(out, 20 + pad.length);
  await MeshoptDecoder.ready;
  const g = await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(out.buffer.slice(out.byteOffset, out.byteOffset + out.length), '');
  g.scene.updateMatrixWorld(true);
  const meshes = [];
  g.scene.traverse(o => { if (o.isMesh) meshes.push(o); });
  return {THREE, scene: g.scene, meshes};
}

if (import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  const [input, output] = process.argv.slice(2);
  const {meshes} = await loadGeometryOnly(input);
  const header = [], chunks = [];
  const v = new THREE.Vector3();
  for (const mesh of meshes) {
    const g = mesh.geometry, pos = g.attributes.position, n = pos.count;
    const world = new Float32Array(n * 3), normals = new Float32Array(n * 3), nrm = g.attributes.normal;
    const normalMatrix = new THREE.Matrix3().getNormalMatrix(mesh.matrixWorld);
    for (let i = 0; i < n; i++) {
      v.fromBufferAttribute(pos, i).applyMatrix4(mesh.matrixWorld); world.set([v.x, v.y, v.z], i * 3);
      // Normais de sombreamento: o Blender usa para orientar faces com enrolamento invertido.
      if (nrm) { v.fromBufferAttribute(nrm, i).applyMatrix3(normalMatrix).normalize(); normals.set([v.x, v.y, v.z], i * 3); }
    }
    let index;
    if (g.index) index = Uint32Array.from(g.index.array);
    else { index = new Uint32Array(n); for (let i = 0; i < n; i++) index[i] = i; }
    header.push({name: mesh.name, vertices: n, indices: index.length});
    chunks.push(Buffer.from(world.buffer), Buffer.from(normals.buffer), Buffer.from(index.buffer));
  }
  const head = Buffer.from(JSON.stringify({meshes: header}));
  const size = Buffer.alloc(4); size.writeUInt32LE(head.length);
  fs.writeFileSync(output, Buffer.concat([size, head, ...chunks]));
  const verts = header.reduce((s, m) => s + m.vertices, 0), tris = header.reduce((s, m) => s + m.indices, 0) / 3;
  console.log(JSON.stringify({input, meshes: header.length, vertices: verts, triangles: tris}));
}
