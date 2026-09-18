// Motor V12 3D: integridade do GLB e do manifesto, contagem das peças, extras de cinemática e a montagem
// biela-manivela conferida contra a geometria exportada (não só contra a fórmula).
import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import fs from 'node:fs';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {ENGINE_PROFILES} from './src/sound/engine-profiles.mjs';
import {pinPosition, pistonDistance, wristPosition, poseV12, strokeOf} from './src/sound/v12-kinematics.mjs';

const MAX_BYTES = 25 * 1024 * 1024;
const TOL = 1e-4;                       // 0,1 mm
const bytes = fs.readFileSync('assets/v12-v1.glb');
const manifest = JSON.parse(fs.readFileSync('assets/v12-v1.manifest.json', 'utf8'));

// ----------------------------------------------------------------- integridade
assert.equal(manifest.asset, 'v12-v1.glb');
assert.equal(bytes.length, manifest.bytes, 'tamanho do GLB diferente do manifesto');
assert.equal(createHash('sha256').update(bytes).digest('hex'), manifest.sha256, 'SHA-256 do GLB diferente do manifesto');
assert.ok(bytes.length <= MAX_BYTES, `GLB com ${(bytes.length / 1048576).toFixed(1)} MiB (limite 25 MiB)`);
assert.match(manifest.license, /original INTEIA/i, 'manifesto sem a procedência da geometria');

// ----------------------------------------------------------------- contagens
const c = manifest.counts;
assert.equal(c.pistons, 12); assert.equal(c.rods, 12); assert.equal(c.trumpets, 12);
assert.equal(c.crankpins, 6); assert.equal(c.valves, 48); assert.equal(c.camshafts, 4);
assert.deepEqual(c.valvesPerBank, {A: 24, B: 24});
assert.ok(manifest.nodes.length >= 60 && manifest.nodes.length <= 90, `${manifest.nodes.length} nós fora da faixa de 60 a 90`);
assert.equal(manifest.cylinders.length, 12);

// A ignição e as bancadas têm de bater com o perfil de som, senão a imagem foge do áudio.
const profile = ENGINE_PROFILES.v12_90s;
assert.deepEqual(manifest.engine.firingOrder, [...profile.firingOrder], 'ordem de ignição diferente do perfil de som');
assert.equal(manifest.engine.cylinders, profile.cylinders);
assert.equal(manifest.engine.bankAngleDeg, profile.bankAngleDeg);
assert.equal(manifest.engine.firingIntervalDeg, 60);
const fires = manifest.cylinders.map((x) => x.firesAtDeg).sort((a, b) => a - b);
fires.forEach((f, i) => assert.equal(f, i * 60, 'ignição não uniforme a cada 60°'));
for (let k = 1; k <= 6; k++) {
  const a = manifest.cylinders[k - 1], b = manifest.cylinders[k + 5];
  assert.ok(Math.abs(Math.abs(a.pinOffsetDeg - b.pinOffsetDeg) - 5) < 1e-6,
    `moente ${k}: bielas separadas em ${Math.abs(a.pinOffsetDeg - b.pinOffsetDeg).toFixed(2)}° (esperado 5°)`);
  assert.equal(a.bank, 'A'); assert.equal(b.bank, 'B');
  assert.ok(Math.abs(a.axisDeg + b.axisDeg) < 1e-9, 'bancadas não simétricas');
}

// ----------------------------------------------------------------- GLB carregado
// O three em Node não monta texturas; o teste lê só a geometria e a hierarquia.
const len = bytes.readUInt32LE(12);
const j = JSON.parse(bytes.subarray(20, 20 + len));
const nodeExtras = new Map(j.nodes.map((n) => [n.name, n.extras || {}]));
j.materials = [{}]; delete j.images; delete j.textures; delete j.samplers;
j.meshes.forEach((mesh) => mesh.primitives.forEach((p) => { p.material = 0; }));
const json = Buffer.from(JSON.stringify(j));
const pad = Buffer.alloc(Math.ceil(json.length / 4) * 4, 32); json.copy(pad);
const tail = bytes.subarray(20 + len);
const out = Buffer.alloc(20 + pad.length + tail.length);
bytes.copy(out, 0, 0, 12);
out.writeUInt32LE(out.length, 8); out.writeUInt32LE(pad.length, 12); out.writeUInt32LE(0x4e4f534a, 16);
pad.copy(out, 20); tail.copy(out, 20 + pad.length);
const gltf = await new GLTFLoader().parseAsync(out.buffer.slice(out.byteOffset, out.byteOffset + out.length), '');
const scene = gltf.scene;
assert.equal(gltf.animations.length, 0, 'o movimento não pode ser gravado no GLB: quem move é o código');

const byName = new Map();
scene.traverse((o) => { if (o.name) byName.set(o.name, o); });
const nodes = (name) => byName.get(name);

// ----------------------------------------------------------------- extras de cinemática
const crank = nodes(manifest.engine.crankNode);
assert.ok(crank, 'nó do virabrequim ausente');
assert.equal(nodeExtras.get(manifest.engine.crankNode)?.kinematics, 'crank');
for (const name of manifest.engine.camNodes) {
  assert.ok(nodes(name), `comando ${name} ausente`);
  assert.equal(nodeExtras.get(name)?.kinematics, 'cam');
}
for (const cyl of manifest.cylinders) {
  for (const [name, kind] of [[cyl.piston, 'piston'], [cyl.rod, 'rod']]) {
    assert.ok(nodes(name), `nó ${name} ausente no GLB`);
    const extras = nodeExtras.get(name) || {};
    assert.equal(extras.kinematics, kind, `${name} sem extras de cinemática`);
    assert.equal(extras.cylinder, cyl.cylinder);
    assert.equal(extras.bank, cyl.bank);
    assert.ok(Math.abs(extras.pinOffsetDeg - cyl.pinOffsetDeg) < 1e-6, `${name}: defasagem do moente diferente do manifesto`);
    assert.ok(Math.abs(extras.axisDeg - cyl.axisDeg) < 1e-6, `${name}: eixo do cilindro diferente do manifesto`);
  }
  assert.ok(nodes(cyl.trumpet), `trompeta ${cyl.trumpet} ausente`);
}
// A malha da biela precisa nascer apontando para +Y com o pé pequeno a uma distância de biela do pé grande.
for (const cyl of manifest.cylinders) {
  const rod = nodes(cyl.rod);
  rod.geometry.computeBoundingBox();
  const top = rod.geometry.boundingBox.max.y;
  assert.ok(Math.abs(top - manifest.engine.rodLengthM) < 0.02,
    `${cyl.rod}: malha termina em ${top.toFixed(4)} m, esperado perto de ${manifest.engine.rodLengthM} m`);
}

// O site reconhece as peças pelos extras do nó, porque o carregador higieniza nomes com espaço.
// Sem os extras, o corte do bloco e a abertura do airbox deixam de funcionar sem erro visível.
let comCorte = 0, comAirbox = 0;
scene.traverse((o) => {
  if (!o.isMesh) return;
  if (o.userData?.cut) comCorte++;
  if (o.userData?.hide_group === 'airbox') comAirbox++;
});
assert.equal(comCorte, manifest.nodes.filter((n) => n.cut).length, 'peças cortáveis sem o extra `cut` no GLB');
assert.ok(comCorte >= 10, `só ${comCorte} peças aceitam corte`);
assert.equal(comAirbox, manifest.nodes.filter((n) => n.hideGroup === 'airbox').length, 'airbox sem o extra `hide_group` no GLB');
assert.ok(comAirbox >= 3, `só ${comAirbox} peças no airbox`);
const higienizado = manifest.nodes.filter((n) => n.cut).some((n) => !byName.has(n.node));
assert.ok(higienizado, 'os nomes deixaram de ser higienizados: reveja se a busca por extras ainda é necessária');

// ----------------------------------------------------------------- cinemática montada
const engine = manifest.engine;
const rodEnd = new THREE.Vector3(0, engine.rodLengthM, 0);
const worst = {rod: 0, piston: 0, bore: 0, pin: 0};

function conferir(theta) {
  poseV12(nodes, manifest, theta);
  scene.updateMatrixWorld(true);
  for (const cyl of manifest.cylinders) {
    const pin = pinPosition(engine, cyl, theta);
    const wrist = wristPosition(engine, cyl, theta);
    // a biela é rígida: a distância entre os centros não muda em nenhum ângulo
    const d = Math.hypot(wrist.x - pin.x, wrist.y - pin.y, wrist.z - pin.z);
    worst.rod = Math.max(worst.rod, Math.abs(d - engine.rodLengthM));
    // o pino do pistão anda sobre o eixo do cilindro, que passa pelo centro do virabrequim
    const a = cyl.axisDeg * Math.PI / 180;
    worst.bore = Math.max(worst.bore, Math.abs(wrist.x * Math.cos(a) - wrist.y * Math.sin(a)));
    // e as peças do GLB estão onde a fórmula diz
    const p = nodes(cyl.piston).getWorldPosition(new THREE.Vector3());
    worst.piston = Math.max(worst.piston, p.distanceTo(new THREE.Vector3(wrist.x, wrist.y, wrist.z)));
    const rod = nodes(cyl.rod);
    const small = rod.localToWorld(rodEnd.clone());
    worst.pin = Math.max(worst.pin, small.distanceTo(new THREE.Vector3(wrist.x, wrist.y, wrist.z)));
    const big = rod.getWorldPosition(new THREE.Vector3());
    worst.pin = Math.max(worst.pin, big.distanceTo(new THREE.Vector3(pin.x, pin.y, pin.z)));
  }
}

for (const theta of [0, 180, 360]) conferir(theta);
for (let theta = 0; theta < 720; theta += 7) conferir(theta);
assert.ok(worst.rod < TOL, `biela estica ${(worst.rod * 1000).toFixed(3)} mm`);
assert.ok(worst.bore < TOL, `pistão sai do eixo do cilindro em ${(worst.bore * 1000).toFixed(3)} mm`);
assert.ok(worst.piston < TOL, `pistão do GLB fora do previsto em ${(worst.piston * 1000).toFixed(3)} mm`);
assert.ok(worst.pin < TOL, `pés da biela fora dos centros em ${(worst.pin * 1000).toFixed(3)} mm`);

// Curso: a diferença entre os extremos é o dobro do raio do moente, em todos os cilindros.
for (const cyl of manifest.cylinders) {
  let lo = Infinity, hi = -Infinity;
  for (let theta = 0; theta < 360; theta += 0.25) {
    const d = pistonDistance(engine, cyl, theta);
    lo = Math.min(lo, d); hi = Math.max(hi, d);
  }
  assert.ok(Math.abs(hi - lo - strokeOf(engine)) < 1e-5, `cilindro ${cyl.cylinder}: curso ${(hi - lo).toFixed(5)} m`);
  // o pistão está no ponto morto superior quando o cilindro explode
  assert.ok(Math.abs(pistonDistance(engine, cyl, cyl.firesAtDeg) - hi) < 1e-9,
    `cilindro ${cyl.cylinder}: não está no ponto morto superior ao explodir`);
}

// Cobertura de todos os nós móveis e ausência de deriva depois de 20 voltas completas.
assert.equal(poseV12(nodes, manifest, 0), 1 + 12 * 2 + 4, 'poseV12 não moveu todas as peças');
poseV12(nodes, manifest, 0); scene.updateMatrixWorld(true);
const before = manifest.cylinders.map((cyl) => nodes(cyl.piston).getWorldPosition(new THREE.Vector3()));
for (let volta = 1; volta <= 20; volta++) poseV12(nodes, manifest, volta * 720);
scene.updateMatrixWorld(true);
let drift = 0;
manifest.cylinders.forEach((cyl, i) => {
  drift = Math.max(drift, nodes(cyl.piston).getWorldPosition(new THREE.Vector3()).distanceTo(before[i]));
});
assert.ok(drift < 1e-6, `deriva de ${drift} m depois de 20 ciclos`);

console.log({motor: 'V12 65° INTEIA', nós: manifest.nodes.length, triângulos: manifest.totals.triangles,
  MB: +(bytes.length / 1e6).toFixed(2), cursoMm: +(strokeOf(engine) * 1000).toFixed(2),
  erroMaximoMm: +(Math.max(worst.rod, worst.piston, worst.bore, worst.pin) * 1000).toFixed(4), ciclos: 20, deriva: drift});
