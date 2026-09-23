// Oclusão de ambiente assada no Blender (Cycles/OptiX), um byte por vértice.
// Gerada por ferramentas/realismo (exportar_malhas.mjs -> assar_oclusao.py) na mesma
// ordem de malhas e vértices que o GLTFLoader entrega. Cópia idêntica na aula
// (src/fx/baked-ao.js).
//
// attachBakedOcclusion(root, buffer) logo após carregar o GLB, antes de qualquer malha
// ser acrescentada; patchBakedOcclusion(root) depois dos demais patches de material.
// Malha sem o atributo (decalque, peça trocada) lê 0 = sem oclusão e nunca escurece.
import * as THREE from 'three';

export const bakedOcclusionUniforms = {
  // Expoente sobre a visibilidade: 1 = bake puro; acima de 1 aprofunda as frestas.
  uBakedAO: {value: 2},
  // Parte da oclusão aplicada também à luz direta (as luzes de preenchimento não têm sombra).
  uBakedAODirect: {value: .65},
};

// Busca o bake de um GLB (<nome>.ao.bin ao lado dele). Ausente ou inválido: null, e a peça segue sem ele.
export async function fetchBakedOcclusion(glbUrl, signal) {
  try {
    const response = await fetch(glbUrl.replace(/\.glb$/, '.ao.bin'), {signal});
    if (!response.ok || (response.headers.get('content-type') || '').includes('text/html')) return null;
    return await response.arrayBuffer();
  } catch { return null; }
}

// Anexa sem derrubar a carga: um bake que não corresponde ao GLB só é ignorado.
export function tryAttachBakedOcclusion(root, buffer) {
  if (!buffer) return false;
  try { attachBakedOcclusion(root, buffer); return true; } catch (error) { console.warn(error); return false; }
}

export function attachBakedOcclusion(root, buffer) {
  const bytes = new Uint8Array(buffer);
  const magic = String.fromCharCode(...bytes.subarray(0, 4));
  if (magic !== 'AOV1') throw new Error('Oclusão assada: formato desconhecido.');
  const view = new DataView(buffer), count = view.getUint32(4, true);
  const meshes = [];
  root.traverse(o => { if (o.isMesh) meshes.push(o); });
  if (meshes.length !== count) throw new Error(`Oclusão assada: ${count} malhas no bake, ${meshes.length} no modelo.`);
  let offset = 8 + count * 4;
  meshes.forEach((mesh, k) => {
    const n = view.getUint32(8 + k * 4, true);
    if (mesh.geometry.attributes.position.count !== n) throw new Error(`Oclusão assada: malha ${mesh.name} com ${mesh.geometry.attributes.position.count} vértices, bake com ${n}.`);
  });
  const shared = new Set();
  for (const [k, mesh] of meshes.entries()) {
    const n = view.getUint32(8 + k * 4, true);
    // Geometria compartilhada entre instâncias recebe cópia: cada posição tem seu bake.
    if (shared.has(mesh.geometry)) mesh.geometry = mesh.geometry.clone();
    shared.add(mesh.geometry);
    mesh.geometry.setAttribute('bakedOcclusion', new THREE.BufferAttribute(bytes.slice(offset, offset + n), 1, true));
    offset += n;
  }
  return meshes.length;
}

const VERTEX_HEAD = '\nattribute float bakedOcclusion;\nvarying float vBakedOcclusion;\n';
const FRAGMENT_HEAD = '\nvarying float vBakedOcclusion;\nuniform float uBakedAO, uBakedAODirect;\n';
const FRAGMENT_APPLY = `#include <aomap_fragment>
{
  float bakedVisibility = pow(1.0 - vBakedOcclusion, uBakedAO);
  reflectedLight.indirectDiffuse *= bakedVisibility;
  float bakedDirect = mix(1.0, bakedVisibility, uBakedAODirect);
  reflectedLight.directDiffuse *= bakedDirect;
  reflectedLight.directSpecular *= bakedDirect;
#if defined( USE_CLEARCOAT )
  clearcoatSpecularIndirect *= bakedVisibility;
  clearcoatSpecularDirect *= bakedDirect;
#endif
#if defined( USE_SHEEN )
  sheenSpecularIndirect *= bakedVisibility;
#endif
#if defined( USE_ENVMAP ) && defined( STANDARD )
  reflectedLight.indirectSpecular *= computeSpecularOcclusion(saturate(dot(geometryNormal, geometryViewDir)), bakedVisibility, material.roughness);
#endif
}`;

export function patchBakedOcclusionMaterial(material) {
  if (!material?.isMeshStandardMaterial || material.userData.bakedOcclusion) return;
  material.userData.bakedOcclusion = true;
  const previous = material.onBeforeCompile, key = material.customProgramCacheKey;
  material.onBeforeCompile = function (shader, renderer) {
    previous?.call(this, shader, renderer);
    Object.assign(shader.uniforms, bakedOcclusionUniforms);
    shader.vertexShader = shader.vertexShader
      .replace('#include <common>', '#include <common>' + VERTEX_HEAD)
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvBakedOcclusion = bakedOcclusion;');
    shader.fragmentShader = shader.fragmentShader
      .replace('#include <common>', '#include <common>' + FRAGMENT_HEAD)
      .replace('#include <aomap_fragment>', FRAGMENT_APPLY);
  };
  material.customProgramCacheKey = function () { return key.call(this) + '-baked-ao-v1'; };
  material.needsUpdate = true;
}

// Seção SHD1 (opcional) depois dos bytes por vértice: sombra de contato assada no piso.
function readShadow(buffer) {
  const view = new DataView(buffer), count = view.getUint32(4, true);
  let offset = 8 + count * 4;
  for (let k = 0; k < count; k++) offset += view.getUint32(8 + k * 4, true);
  if (offset + 12 > buffer.byteLength) return null;
  const tag = String.fromCharCode(...new Uint8Array(buffer, offset, 4));
  if (tag !== 'SHD1') return null;
  const jsonLength = view.getUint32(offset + 4, true);
  const meta = JSON.parse(new TextDecoder().decode(new Uint8Array(buffer, offset + 8, jsonLength)));
  const pngOffset = offset + 8 + jsonLength, pngLength = view.getUint32(pngOffset, true);
  return {meta, png: new Uint8Array(buffer, pngOffset + 4, pngLength)};
}

// Plano filho do modelo: acompanha o carro. Some ao explodir, isolar ou mover peças,
// porque a sombra só vale para o carro montado.
export async function addContactShadow(model, buffer, {strength = .9, mechanics = null} = {}) {
  const shadow = readShadow(buffer);
  if (!shadow) return null;
  const {meta, png} = shadow;
  const bitmap = await createImageBitmap(new Blob([png], {type: 'image/png'}));
  const texture = new THREE.Texture(bitmap);
  texture.colorSpace = THREE.NoColorSpace;
  texture.flipY = false; // Linha 0 do PNG (topo) = v 0 = minZ.
  texture.needsUpdate = true;
  // Acima de chapas e faixas do piso (até ~8 mm); o pneu esconde a folga no ponto de contato.
  const y = meta.y + .015;
  const geometry = new THREE.BufferGeometry();
  geometry.setAttribute('position', new THREE.Float32BufferAttribute([
    meta.minX, y, meta.minZ, meta.maxX, y, meta.minZ, meta.maxX, y, meta.maxZ, meta.minX, y, meta.maxZ], 3));
  geometry.setAttribute('uv', new THREE.Float32BufferAttribute([0, 0, 1, 0, 1, 1, 0, 1], 2));
  geometry.setIndex([0, 2, 1, 0, 3, 2]);
  const material = new THREE.MeshBasicMaterial({color: 0x000000, alphaMap: texture, transparent: true, depthWrite: false, opacity: strength, toneMapped: false,
    polygonOffset: true, polygonOffsetFactor: -2, polygonOffsetUnits: -8});
  // Curva sobre a oclusão: o miolo sob o carro fica quase preto e a borda continua suave.
  material.onBeforeCompile = shader => {
    shader.fragmentShader = shader.fragmentShader.replace('#include <alphamap_fragment>',
      'diffuseColor.a *= pow(texture2D(alphaMap, vAlphaMapUv).g, .6);');
  };
  material.customProgramCacheKey = () => 'contact-shadow-v1';
  const mesh = new THREE.Mesh(geometry, material);
  mesh.name = 'Sombra de contato';
  mesh.raycast = () => {};
  mesh.userData.contactShadow = true;
  mesh.onBeforeRender = () => {
    if (!mechanics) return;
    const amount = mechanics.amount, moved = !mechanics.motionAvailable && amount < .001;
    material.opacity = mechanics.isolated || moved ? 0 : strength * Math.max(0, 1 - amount * 6);
  };
  model.add(mesh);
  return {mesh, meta, dispose() { model.remove(mesh); geometry.dispose(); material.dispose(); texture.dispose(); bitmap.close?.(); }};
}

export function patchBakedOcclusion(root) {
  root.traverse(o => {
    if (!o.isMesh || !o.geometry.attributes.bakedOcclusion) return;
    for (const material of [].concat(o.material)) patchBakedOcclusionMaterial(material);
  });
}
