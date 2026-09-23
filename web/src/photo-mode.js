// Foto realista: com a cena parada, a imagem é refinada por traçado de caminhos na GPU
// (three-gpu-pathtracer). Luz indireta, reflexos entre peças e sombras suaves convergem em
// algumas centenas de amostras; ao girar a câmera, o refino recomeça do zero.
//
// O traçador lê materiais PBR e luzes direcionais, retangulares e pontuais. Ao entrar:
// - o ambiente do box (PMREM) é trocado pelo HDR equiretangular do Cycles, o mesmo em origem;
// - telas, LEDs e letreiros (MeshBasicMaterial) viram emissivos equivalentes;
// e tudo volta ao sair. Os ajustes feitos por shader no tempo real não entram no traçado.
import * as THREE from 'three';
import {RGBELoader} from 'three/addons/loaders/RGBELoader.js';
import {WebGLPathTracer, DenoiseMaterial} from 'three-gpu-pathtracer';
import {FullScreenQuad} from 'three/addons/postprocessing/Pass.js';

const MAX_SAMPLES = 600;
const DECAL_LIFT = .0025;

// Suavização final: o filtro de bordas do three-gpu-pathtracer preserva pontos muito brilhantes
// (vagalumes do verniz) como se fossem bordas. Aqui o pixel central que destoa da vizinhança é
// trocado pela média dela e os vizinhos têm o brilho limitado antes de pesar.
function denoiser() {
  const material = new DenoiseMaterial({sigma: 3, kSigma: 1, threshold: .12});
  material.fragmentShader = material.fragmentShader
    .replace('vec4 centrPx = texture2D( tex, uv );', `vec4 centrPx = texture2D( tex, uv );
					{
						vec2 px = 1.0 / vec2( textureSize( tex, 0 ) );
						vec3 ring = vec3( 0.0 );
						float peak = 0.0;
						for ( int i = - 1; i <= 1; i ++ ) for ( int j = - 1; j <= 1; j ++ ) if ( i != 0 || j != 0 ) {
							vec3 c = min( texture2D( tex, uv + vec2( i, j ) * px ).rgb, vec3( 4.0 ) );
							ring += c; peak = max( peak, dot( c, vec3( .2126, .7152, .0722 ) ) );
						}
						ring /= 8.0;
						float lc = dot( centrPx.rgb, vec3( .2126, .7152, .0722 ) ), lr = dot( ring, vec3( .2126, .7152, .0722 ) );
						// Só ponto isolado: mais claro que a média e que todos os vizinhos (traço de letra tem vizinho claro).
						if ( lc > lr * 1.5 + .04 && lc > peak * 1.25 ) centrPx.rgb = ring;
					}`)
    .replace('vec4 walkPx = texture2D( tex, uv + d / size );', 'vec4 walkPx = texture2D( tex, uv + d / size ); walkPx.rgb = min( walkPx.rgb, vec3( 4.0 ) );');
  material.needsUpdate = true;
  return new FullScreenQuad(material);
}

export function createPhotoMode({renderer, scene, camera, controls, base = './assets/', onChange = () => {}}) {
  let tracer = null, hdr = null, active = false, building = null, dirty = false, smooth = null;
  const lifted = [];
  const swapped = [];
  const status = {state: 'off', samples: 0};
  const emit = () => onChange({...status, max: MAX_SAMPLES});

  async function environment() {
    if (hdr) return hdr;
    hdr = await new RGBELoader().setDataType(THREE.FloatType).loadAsync(base + 'pitlane-cycles.hdr');
    // Mesma exposição que cycles-finish.js aplica antes do PMREM do tempo real.
    const data = hdr.image.data;
    for (let i = 0; i < data.length; i += 4) { data[i] *= .32; data[i + 1] *= .32; data[i + 2] *= .32; }
    hdr.mapping = THREE.EquirectangularReflectionMapping;
    hdr.needsUpdate = true;
    return hdr;
  }

  function swapBasicMaterials() {
    const cache = new Map();
    scene.traverse(o => {
      if (!o.isMesh || !o.visible) return;
      const convert = m => {
        if (!m?.isMeshBasicMaterial) return m;
        if (!cache.has(m)) {
          // Telas e letreiros (com textura) emitem luz. Fitas de LED sem textura viram superfície clara
          // comum: emissores pequenos e fortes refletidos no verniz geravam chuvisco que não converge.
          const screen = Boolean(m.map);
          const color = m.color.clone(), peak = Math.max(color.r, color.g, color.b);
          if (peak > 1) color.multiplyScalar(1 / peak);
          const e = new THREE.MeshStandardMaterial({color: screen ? 0x000000 : color, emissive: screen ? m.color.clone() : 0x000000,
            emissiveMap: m.map || null, emissiveIntensity: screen ? 1 : 0, transparent: m.transparent, opacity: m.opacity,
            alphaMap: m.alphaMap, side: m.side, roughness: screen ? 1 : .6});
          cache.set(m, e);
        }
        return cache.get(m);
      };
      const original = o.material;
      const next = Array.isArray(original) ? original.map(convert) : convert(original);
      if (next !== original) { swapped.push({mesh: o, original}); o.material = next; }
    });
    return cache;
  }
  let converted = null;

  // Decalques colados na carroceria dependem de polygonOffset, que o traçado ignora: sobem alguns mm.
  function liftDecals() {
    scene.traverseVisible(o => {
      if (!o.isMesh || !o.userData.inteiaDecal || !o.geometry.attributes.normal) return;
      const g = o.geometry.clone(), p = g.attributes.position, n = g.attributes.normal;
      for (let i = 0; i < p.count; i++) p.setXYZ(i, p.getX(i) + n.getX(i) * DECAL_LIFT, p.getY(i) + n.getY(i) * DECAL_LIFT, p.getZ(i) + n.getZ(i) * DECAL_LIFT);
      lifted.push({mesh: o, original: o.geometry}); o.geometry = g;
    });
  }

  function restore() {
    for (const {mesh, original} of lifted) { mesh.geometry.dispose(); mesh.geometry = original; }
    lifted.length = 0;
    for (const {mesh, original} of swapped) mesh.material = original;
    swapped.length = 0;
    converted?.forEach(m => m.dispose());
    converted = null;
  }

  async function build() {
    status.state = 'building'; status.samples = 0; emit();
    restore();
    converted = swapBasicMaterials();
    liftDecals();
    // Montagem síncrona da BVH (o laboratório é um HTML único, sem arquivo de worker):
    // espera dois quadros para a mensagem aparecer antes do trabalho pesado.
    await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    const started = performance.now();
    tracer.setScene(scene, camera);
    status.buildMs = Math.round(performance.now() - started);
    let triangles = 0, meshes = 0;
    scene.traverseVisible(o => { if (o.isMesh) { meshes++; triangles += (o.geometry.index ? o.geometry.index.count : o.geometry.attributes.position.count) / 3; } });
    Object.assign(status, {triangles: Math.round(triangles), meshes});
    tracer.updateEnvironment();
    status.state = 'tracing'; emit();
  }

  async function enter() {
    if (active) return;
    active = true;
    status.state = 'building'; emit();
    try {
      if (!tracer) {
        tracer = new WebGLPathTracer(renderer);
        tracer.bounces = 6;
        tracer.transmissiveBounces = 4;
        tracer.filterGlossyFactor = 1;
        tracer.minSamples = 3;
        tracer.renderDelay = 0;
        tracer.fadeDuration = 300;
        tracer.dynamicLowRes = true;
        tracer.lowResScale = .3;
        tracer.tiles.set(2, 2);
        smooth = denoiser();
        tracer.renderToCanvasCallback = (target, renderer, quad) => {
          // Suavização forte nos primeiros passes, quase nenhuma quando a imagem converge.
          const t = Math.min(1, tracer.samples / MAX_SAMPLES);
          const m = smooth.material;
          m.map = target.texture; m.opacity = quad.material.opacity; m.blending = quad.material.blending;
          m.sigma = 3 - 1.8 * t; m.threshold = .12 - .08 * t;
          const autoClear = renderer.autoClear; renderer.autoClear = false;
          smooth.render(renderer);
          renderer.autoClear = autoClear;
        };
      }
      const env = await environment();
      if (!active) return;
      status.savedEnvironment = scene.environment;
      scene.environment = env;
      building = build();
      await building;
      building = null;
      if (!active) { leave(); return; }
    } catch (error) {
      console.error(error);
      active = false; restore();
      if (status.savedEnvironment) scene.environment = status.savedEnvironment;
      status.state = 'failed'; emit();
    }
  }

  function leave() {
    restore();
    if (status.savedEnvironment) { scene.environment = status.savedEnvironment; status.savedEnvironment = null; }
    status.state = 'off'; status.samples = 0; emit();
  }

  function exit() {
    if (!active) return;
    active = false;
    if (!building) leave();
  }

  // Câmera girada: o refino recomeça. Ao soltar, a cena é reconstruída (paredes do box
  // aparecem ou somem conforme o ponto de vista).
  controls.addEventListener('change', () => { if (active && status.state === 'tracing') tracer.updateCamera(); });
  controls.addEventListener('end', () => { if (active) dirty = true; });

  return {
    get active() { return active; },
    get state() { return status.state; },
    enter, exit,
    toggle() { return active ? exit() : enter(); },
    // Chamado a cada quadro; devolve true quando o traçador desenhou o quadro.
    render() {
      if (!active || status.state !== 'tracing') return false;
      if (dirty && !building) {
        dirty = false;
        building = build().then(() => { if (!active) leave(); }).catch(error => { console.error(error); status.state = 'failed'; emit(); }).finally(() => { building = null; });
        return false;
      }
      tracer.pausePathTracing = tracer.samples >= MAX_SAMPLES;
      tracer.renderSample();
      const samples = Math.floor(tracer.samples);
      if (samples !== status.samples) { status.samples = samples; emit(); }
      return true;
    },
    dispose() { exit(); tracer?.dispose(); hdr?.dispose(); smooth?.material.dispose(); smooth?.dispose(); },
  };
}
