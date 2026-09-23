// Bancada 3D do V12 da aba 07: carrega o GLB sob demanda e move virabrequim, bielas, pistões e comandos a
// partir do ângulo θ que o reprodutor de som informa, de modo que a imagem e o áudio andem no mesmo tempo.
// O movimento não vem gravado no arquivo; quem move é `v12-kinematics.mjs`.
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {poseV12} from './v12-kinematics.mjs';
import {fetchBakedOcclusion, tryAttachBakedOcclusion, patchBakedOcclusion} from '../baked-ao.js';

const ASSET = './assets/v12-v1.glb';
const MANIFEST = './assets/v12-v1.manifest.json';

export function createV12View({onStatus = () => {}} = {}) {
  const observer = {fn: onStatus};
  const root = new THREE.Group();
  root.name = 'Bancada do V12';
  root.visible = false;
  const cutPlane = new THREE.Plane(new THREE.Vector3(1, 0, 0), 0);
  const cutMaterials = new Map();
  const airboxMeshes = [];
  let manifest = null, nodes = null, loading = null, disposed = false;
  let state = 'idle';                 // idle | loading | ready | failed
  let theta = 0, cut = 0, airbox = true, wanted = false;

  const setState = (next, message) => { state = next; observer.fn(next, message); };

  async function load() {
    if (loading) return loading;
    setState('loading');
    loading = (async () => {
      const [gltf, data, bakedAO] = await Promise.all([
        new GLTFLoader().loadAsync(ASSET),
        fetch(MANIFEST).then((r) => { if (!r.ok) throw new Error(`manifesto ${r.status}`); return r.json(); }),
        fetchBakedOcclusion(ASSET),
      ]);
      if (disposed) return;
      manifest = data;
      const scene = gltf.scene;
      tryAttachBakedOcclusion(scene, bakedAO);
      const map = new Map();
      scene.traverse((o) => {
        if (o.name) map.set(o.name, o);
        if (o.isMesh) { o.castShadow = true; o.receiveShadow = true; }
      });
      nodes = (name) => map.get(name);
      // Os nomes com espaço são higienizados ao carregar, então as peças são reconhecidas pelos extras do
      // próprio nó, não pelo nome. Fundidos e carenagens aceitam corte; as móveis ficam inteiras.
      scene.traverse((o) => {
        if (!o.isMesh) return;
        if (o.userData?.hide_group === 'airbox') airboxMeshes.push(o);
        if (!o.userData?.cut) return;
        const seccionar = (material) => {
          if (!cutMaterials.has(material)) {
            const copy = material.clone();
            copy.side = THREE.DoubleSide;
            cutMaterials.set(material, copy);
          }
          return cutMaterials.get(material);
        };
        o.material = Array.isArray(o.material) ? o.material.map(seccionar) : seccionar(o.material);
      });
      // Depois das cópias de corte: todas recebem a oclusão assada no Cycles.
      patchBakedOcclusion(scene);
      // Apoia o motor no piso do box e o centra na origem.
      poseV12(nodes, manifest, 0);
      scene.updateMatrixWorld(true);
      const box = new THREE.Box3().setFromObject(scene);
      const center = box.getCenter(new THREE.Vector3());
      scene.position.set(-center.x, -box.min.y + 0.01, -center.z);
      root.add(scene);
      applyPose();
      applyAirbox();
      applyCut();
      setState('ready');
      root.visible = wanted;
    })().catch((error) => {
      console.error(error);
      setState('failed', error.message);
    });
    return loading;
  }

  function applyPose() {
    if (!manifest) return;
    poseV12(nodes, manifest, theta);
  }
  function applyAirbox() {
    for (const mesh of airboxMeshes) mesh.visible = airbox;
  }
  function applyCut() {
    // O plano varre a metade esquerda do motor: 0 mostra tudo, 1 abre até o eixo do virabrequim.
    // O plano vive no espaço do mundo, por isso a bancada fica sempre centrada na origem.
    cutPlane.constant = 0.26 * (1 - cut);
    const planes = cut <= 0 ? null : [cutPlane];
    for (const material of cutMaterials.values()) {
      // Ligar ou desligar o corte troca o programa do material; sem isto o three mantém o anterior.
      const antes = material.clippingPlanes ? material.clippingPlanes.length : 0;
      material.clippingPlanes = planes;
      if (antes !== (planes ? planes.length : 0)) material.needsUpdate = true;
    }
  }

  return {
    root,
    set onStatus(fn) { observer.fn = typeof fn === 'function' ? fn : () => {}; },
    get state() { return state; },
    get manifest() { return manifest; },
    get thetaDeg() { return theta; },
    get wanted() { return wanted; },
    get counts() { return {cut: cutMaterials.size, airbox: airboxMeshes.length}; },
    load,
    setVisible(visible) {
      wanted = Boolean(visible);
      root.visible = wanted && state === 'ready';
      if (wanted && state === 'idle') load();
    },
    setPose(thetaDeg) { theta = thetaDeg; applyPose(); },
    setAirbox(visible) { airbox = visible; applyAirbox(); },
    setCut(amount) { cut = Math.max(0, Math.min(1, amount)); applyCut(); },
    dispose() {
      disposed = true;
      root.traverse((o) => { if (o.isMesh) { o.geometry.dispose(); [].concat(o.material).forEach((mat) => mat.dispose()); } });
      cutMaterials.clear();
      root.clear();
    },
  };
}
