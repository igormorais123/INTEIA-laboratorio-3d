import assert from 'node:assert/strict';
import {createHash} from 'node:crypto';
import {readFileSync} from 'node:fs';
import * as THREE from 'three';
import {
  FLOW_SPEEDS,
  HIDE_GROUPS,
  SYSTEM_CATALOG,
  SYSTEM_IDS,
  SYSTEMS_ASSET,
  advanceLocalSpin,
} from './src/systems.js';

const expected = [
  ['aero', '0:14'], ['structure', '4:47'], ['suspension', '5:19'],
  ['steering', '7:52'], ['brakes', '8:57'], ['power', '11:32'],
  ['ers', '14:14'], ['cooling', '14:54'], ['fuel', '15:39'],
  ['transmission', '16:42'], ['safety', '17:03'], ['cockpit', '17:51'],
  ['wheel', '19:17'], ['sensors', '22:11'],
];

assert.deepEqual(SYSTEM_IDS, expected.map(([id]) => id), 'IDs fora da ordem do catálogo');
assert.equal(new Set(SYSTEM_IDS).size, 14, 'IDs duplicados');
for (const system of SYSTEM_CATALOG) assert.ok(Array.isArray(system.spread) && system.spread.length === 3 && system.spread.some((v) => v !== 0), `${system.id} sem vetor de explosão`);
assert.equal(Object.isFrozen(SYSTEM_CATALOG), true, 'catálogo mutável');
assert.equal(Object.isFrozen(SYSTEM_IDS), true, 'lista de IDs mutável');
assert.equal(Object.isFrozen(HIDE_GROUPS), true, 'grupos ocultáveis mutáveis');
assert.equal(Object.isFrozen(FLOW_SPEEDS), true, 'velocidades de fluxo mutáveis');
assert.equal(SYSTEMS_ASSET, './assets/sistemas-v1.glb');

for (const [index, system] of SYSTEM_CATALOG.entries()) {
  assert.equal(system.id, expected[index][0]);
  assert.equal(system.number, String(index + 1).padStart(2, '0'));
  assert.equal(system.chapter, expected[index][1]);
  assert.match(system.color, /^#[0-9a-f]{6}$/i);
  assert.ok(system.label.length >= 3 && system.description.length >= 40);
}
assert.ok(Object.values(FLOW_SPEEDS).every((speed) => Number.isFinite(speed) && speed > 0));

const quarterTurn = advanceLocalSpin(new THREE.Quaternion(), 'y', Math.PI / 2);
assert.ok(Math.abs(quarterTurn.length() - 1) < 1e-12, 'rotação local perdeu normalização');
assert.throws(() => advanceLocalSpin(new THREE.Quaternion(), 'invalid', 1), /inválido/);

const source = readFileSync(new URL('./src/systems.js', import.meta.url), 'utf8');
const template = readFileSync(new URL('./src/template-v2.html', import.meta.url), 'utf8');
assert.match(source, /new GLTFLoader\(\)\.setMeshoptDecoder\(MeshoptDecoder\)/, 'loader deve habilitar meshopt');
assert.match(source, /fetch\(assetUrl\)/, 'asset deve ser carregado pela URL configurável');
assert.equal((template.match(/class="system-card"/g) || []).length, 14, 'painel deve ter 14 cartões');
for (const id of ['system-flows', 'system-covers', 'system-schematic', 'system-ghost', 'system-explode', 'system-part', 'system-status', 'systems-assembly', 'systems-assembly-value', 'selected-info']) {
  assert.match(template, new RegExp(`id="${id}"`), `controle ausente: ${id}`);
}

const glb = readFileSync(new URL('./assets/sistemas-v1.glb', import.meta.url));
const manifest = JSON.parse(readFileSync(new URL('./assets/sistemas-v1.manifest.json', import.meta.url), 'utf8'));
assert.equal(glb.subarray(0, 4).toString(), 'glTF', 'cabeçalho GLB inválido');
assert.equal(glb.readUInt32LE(4), 2, 'versão GLB inválida');
assert.equal(glb.readUInt32LE(8), glb.length, 'tamanho declarado diverge dos bytes');
assert.equal(manifest.totals.systems, 14);
assert.deepEqual(Object.keys(manifest.systems), SYSTEM_IDS);
assert.equal(manifest.totals.parts, Object.values(manifest.systems).reduce((sum, system) => sum + system.parts, 0));
assert.equal(manifest.totals.bytes, glb.length);
assert.equal(manifest.optimized, true, 'asset final deve estar otimizado');
assert.equal(manifest.sha256, createHash('sha256').update(glb).digest('hex'), 'hash do manifesto desatualizado');

const jsonLength = glb.readUInt32LE(12);
assert.equal(glb.readUInt32LE(16), 0x4e4f534a, 'primeiro chunk deve ser JSON');
const gltf = JSON.parse(glb.subarray(20, 20 + jsonLength));
assert.equal(gltf.asset.version, '2.0');
assert.ok(gltf.extensionsRequired?.includes('EXT_meshopt_compression'), 'meshopt deve ser obrigatório no asset final');
assert.equal(gltf.nodes.length, manifest.totals.nodes);
assert.equal(gltf.meshes.length, manifest.totals.meshes);
assert.equal(gltf.materials.length, manifest.totals.materials);
assert.equal(gltf.images.length, manifest.totals.images);

const systemRoots = gltf.nodes.filter((node) => /^system_/.test(node.name)).map((node) => node.name).sort();
assert.deepEqual(systemRoots, SYSTEM_IDS.map((id) => `system_${id}`).sort(), 'raízes dos sistemas divergentes');
const partNodes = gltf.nodes.filter((node) => node.extras?.part);
assert.equal(partNodes.length, manifest.totals.parts, 'peças do GLB divergem do manifesto');

const meshTriangles = gltf.meshes.map((mesh) => mesh.primitives.reduce((sum, primitive) => {
  assert.equal(primitive.mode ?? 4, 4, 'primitiva não triangular');
  const accessor = primitive.indices ?? primitive.attributes.POSITION;
  return sum + gltf.accessors[accessor].count / 3;
}, 0));
const renderedTriangles = gltf.nodes.reduce((sum, node) => sum + (node.mesh === undefined ? 0 : meshTriangles[node.mesh]), 0);
assert.equal(renderedTriangles, manifest.totals.triangles, 'triângulos renderizados divergem do manifesto');

// ---------------------------------------------------------------- contratos didáticos do asset (arquitetura do carro)
const nodesOf = (id) => manifest.systems[id].nodes;
const find = (id, pattern) => nodesOf(id).filter((node) => pattern.test(node.part));
const center = (node) => node.min.map((v, i) => (v + node.max[i]) / 2);
for (const [id, system] of Object.entries(manifest.systems)) {
  assert.ok(system.parts >= 20, `${id} deve ter pelo menos 20 peças nomeadas`);
  assert.ok(system.nodes.every((node) => node.explode?.length === 3 && node.min.every(Number.isFinite)), `${id}: peças sem bounds ou vetor de separação`);
}
// Unidade de potência: um só turbo dividido, coaxial em Z, MGU-H legado 2021 no mesmo eixo; dois plenums, seis trompetas, duas wastegates.
const compressor = find('power', /^Compressor · carcaça/), turbine = find('power', /^Turbina · carcaça/), shaft = find('power', /^Eixo comum do turbo/), mguh = find('power', /^MGU-H · carcaça/);
assert.equal(compressor.length, 1, 'um compressor'); assert.equal(turbine.length, 1, 'uma turbina'); assert.equal(shaft.length, 1, 'um eixo comum'); assert.equal(mguh.length, 1, 'um MGU-H');
assert.equal(find('power', /compressor/i).filter((node) => /esquerd|direit/.test(node.part)).length, 0, 'sem compressores laterais (twin-turbo)');
const cc = center(compressor[0]), tc = center(turbine[0]), mc = center(mguh[0]);
assert.ok(Math.abs(cc[0]) < .02 && Math.abs(tc[0]) < .02 && Math.abs(mc[0]) < .02, 'compressor, turbina e MGU-H na linha de centro');
assert.ok(cc[2] > tc[2] + .5 && mc[2] < cc[2] && mc[2] > tc[2], 'compressor à frente, turbina atrás, MGU-H entre ambos');
assert.ok(shaft[0].min[2] <= tc[2] + .1 && shaft[0].max[2] >= cc[2] - .1, 'o eixo comum liga compressor e turbina');
assert.equal(mguh[0].era, '2021', 'MGU-H marcado como era 2021');
assert.equal(find('power', /^Trompeta de admissão/).length, 6, 'seis trompetas');
assert.equal(find('power', /^Plenum de admissão .* fundo/).length, 2, 'dois plenums');
assert.ok(find('power', /^Plenum de admissão .* tampa/).every((node) => node.hide_group === 'plenum_lid'), 'tampas dos plenums ocultáveis');
assert.equal(find('power', /^Tubo da wastegate/).length, 2, 'duas wastegates');
assert.equal(find('power', /^Primário de escape/).length, 6, 'seis primários de escape');
assert.ok(nodesOf('ers').some((node) => node.era === '2021'), 'ERS deve ter nós exclusivos do contexto 2021');
// Refrigeração assimétrica: intercooler só à esquerda (+X); água, óleo e ERS à direita (−X).
const intercooler = find('cooling', /^Intercooler ar-ar · núcleo/);
assert.equal(intercooler.length, 1, 'um intercooler'); assert.ok(center(intercooler[0])[0] > .3, 'intercooler no sidepod esquerdo (+X: o piloto olha para +Z)');
for (const pattern of [/^Radiador de água do motor · núcleo/, /^Arrefecedor de óleo do motor · núcleo/, /^Arrefecedor de baixa temperatura do ERS · núcleo/]) {
  const core = find('cooling', pattern); assert.equal(core.length, 1, `trocador ausente: ${pattern}`); assert.ok(center(core[0])[0] < -.3, `${pattern} no sidepod direito (−X)`);
}
for (const kind of ['water', 'oil', 'hyd', 'air']) assert.ok(nodesOf('cooling').some((node) => node.flow === kind), `cooling sem fluxo ${kind}`);
// Empacotamento: assento → célula → motor → câmbio; energy store sob a célula.
const bladder = find('fuel', /^Bexiga flexível/)[0], block = find('power', /^Bloco do motor/)[0], gearbox = find('transmission', /^Carcaça do câmbio/)[0], es = find('ers', /^Energy store · caixa/)[0], seat = find('cockpit', /^Assento moldado/)[0];
assert.ok(bladder && block && gearbox && es && seat, 'peças de referência do empacotamento');
assert.ok(bladder.max[2] <= seat.max[2] && bladder.min[2] >= block.max[2] - .02 && block.min[2] >= gearbox.max[2] - .02, 'ordem longitudinal célula → motor → câmbio');
assert.ok(es.max[1] <= bladder.min[1] + .01 && Math.abs(center(es)[2] - center(bladder)[2]) < .15, 'energy store sob a célula');
assert.ok(find('fuel', /^Linha de alimentação/).every((node) => node.max[2] < 0), 'linha de alimentação fora do cockpit');
// Câmbio: oito pares com distância entre centros constante e giro coerente com os dentes; ré; tripóides; carcaça ocultável.
const primary = find('transmission', /^Engrenagem \dª · primário/), secondary = find('transmission', /^Engrenagem \dª · secundário/);
assert.equal(primary.length, 8); assert.equal(secondary.length, 8);
for (let i = 0; i < 8; i += 1) {
  const n1 = Number(/\((\d+) dentes\)/.exec(primary[i].part)[1]), n2 = Number(/\((\d+) dentes\)/.exec(secondary[i].part)[1]);
  assert.equal(n1 + n2, 44, `par ${i + 1}: soma de dentes`); assert.ok(Math.abs(secondary[i].spin * n2 + primary[i].spin * n1) < 1e-6, `par ${i + 1}: relação de giro`);
}
assert.equal(find('transmission', /^Engrenagem intermediária da ré$/).length, 1, 'ré'); assert.equal(find('transmission', /^Copo da junta tripóide/).length, 2, 'tripóides');
assert.ok(find('transmission', /^Carcaça do câmbio/).every((node) => node.hide_group === 'gearbox_case'), 'carcaça ocultável');
// Demais contratos por sistema.
assert.equal(find('safety', /^Cabo de retenção \d /).length, 12, 'três cabos de retenção por roda');
assert.equal(find('safety', /^Halo · arco principal/).length + find('safety', /^Estrutura principal de capotamento/).length, 2, 'Halo e estrutura de capotamento distintos');
assert.equal(find('cockpit', /^Cadarço de (ombro|cintura|virilha)/).length, 6, 'arnês de seis pontos');
assert.equal(find('brakes', /^Disco carbono-carbono/).length, 4, 'quatro discos'); assert.equal(find('brakes', /^Pinça monobloco/).length, 4, 'quatro pinças');
assert.equal(find('brakes', /^Cilindro mestre · circuito/).length, 2, 'dois cilindros mestres'); assert.equal(find('brakes', /^Unidade brake-by-wire/).length, 1, 'brake-by-wire');
assert.ok(find('brakes', /^Disco carbono-carbono/).every((node) => node.spin > 0), 'discos giram');
assert.equal(find('suspension', /^Push-rod /).length, 2); assert.equal(find('suspension', /^Pull-rod /).length, 2); assert.equal(find('suspension', /^Wishbone (superior|inferior) · perna/).length, 16);
assert.ok(find('suspension', /^Push-rod /).every((rod) => rod.max[1] - rod.min[1] > .25), 'push-rod sobe do upright ao balancim');
assert.equal(find('steering', /^Barra de direção · track rod/).length, 2); assert.equal(find('steering', /^Junta universal/).length, 2);
assert.equal(find('sensors', /^Tubo de Pitot/).length, 1); assert.equal(find('sensors', /^Telemetria carro → box/).length, 1);
assert.equal(find('wheel', /^LED de troca/).length, 15); assert.equal(find('wheel', /^Borboleta de marcha/).length, 2);
// Peças visíveis coincidem com o carro v2 e convenção de lados (o piloto olha para +Z: esquerda = +X).
const halo = find('safety', /^Halo · arco principal/)[0];
assert.ok(halo && halo.max[1] < .88 && halo.max[1] > .86 && halo.min[2] < -.27 && halo.max[2] > .93 && Math.abs(halo.max[0] - .306) < .01, 'Halo com a envolvente da carroceria do carro v2');
const headrest = find('safety', /^Encosto de cabeça/)[0];
assert.ok(headrest && headrest.min[1] > .72 && headrest.max[1] < .88 && headrest.max[2] < .43, 'encosto de cabeça na posição da carroceria');
const rainLight = find('safety', /^Luz de chuva/)[0]; assert.ok(rainLight && Math.abs(center(rainLight)[1] - .315) < .01 && center(rainLight)[2] < -2.5, 'luz de chuva no lugar do LED traseiro');
const wheelBody = find('wheel', /^Corpo do volante/)[0]; assert.ok(wheelBody && Math.abs(center(wheelBody)[0]) < .005 && Math.abs(center(wheelBody)[2] - .518) < .01 && wheelBody.min[1] < .53 && wheelBody.max[1] > .656, 'volante centrado no cubo do carro v2');
assert.ok(find('wheel', /^Botão · /).length >= 12, 'volante com pelo menos doze botões legendados'); assert.equal(find('wheel', /^Legenda /).length, find('wheel', /^Botão · /).length, 'cada botão tem legenda');
assert.ok(find('wheel', /^Botão · OT /).length === 1 && find('wheel', /^Botão · AA /).length === 1, 'comandos de 2026: override manual e aerodinâmica ativa');
assert.ok(find('wheel', /^Display LCD/).every((node) => node.min[2] < .52), 'display voltado ao piloto (−Z)'); assert.ok(find('wheel', /^Borboleta de marcha/).every((node) => node.min[2] > .53), 'borboletas atrás do volante (+Z)');
assert.ok(center(find('brakes', /^Pedal de freio · pisadeira/)[0])[0] > .03, 'pedal de freio no pé esquerdo (+X)'); assert.ok(center(find('cockpit', /^Pedal do acelerador · pisadeira/)[0])[0] < -.03, 'acelerador no pé direito (−X)');
for (const id of SYSTEM_IDS) { for (const node of nodesOf(id)) { if (/esquerd/.test(node.part) && !/direit/.test(node.part)) assert.ok(center(node)[0] > -.02, `${node.part}: rotulado esquerdo mas em −X`); if (/direit/.test(node.part) && !/esquerd/.test(node.part)) assert.ok(center(node)[0] < .02, `${node.part}: rotulado direito mas em +X`); } }
assert.equal(find('ers', /^MGU-K · carcaça/).length, 1); assert.equal(find('ers', /^Engrenagem de acionamento do MGU-K/).length, 1);
const app = readFileSync(new URL('./src/app-v2.js', import.meta.url), 'utf8');
assert.match(source, /revealing/, 'sistemas revelados ao desmontar o carro');
assert.match(app, /systems\?\.enabled\|\|systems\?\.revealing/, 'motor do compartimento cede lugar aos sistemas revelados');

console.log(`Sistemas: ${SYSTEM_IDS.length} camadas, ${manifest.totals.parts} peças, ${manifest.totals.triangles} triângulos, meshopt, manifesto e contratos didáticos OK.`);

// Interface sem metalinguagem de produção: nada de vídeo de referência, capítulos, prompt ou ressalvas de modelagem.
{
 const template = readFileSync(new URL('./src/template-v2.html', import.meta.url), 'utf8');
 const systemsPanel = template.slice(template.indexOf('id="systems-panel"'), template.indexOf('PERSONALIZAR / SEU DESIGN'));
 for (const word of ['vídeo', 'youtube', 'capítulo', 'prompt', 'homolog', 'não é CAD', 'didática inspirada']) assert.ok(!systemsPanel.toLowerCase().includes(word), `painel de sistemas ainda cita "${word}"`);
 for (const system of SYSTEM_CATALOG) for (const word of ['vídeo', 'hipótese', 'homolog', 'não é CAD', 'CFD', 'Simplificação', 'não simula', 'não representa']) assert.ok(!system.description.includes(word), `${system.id}: descrição ainda cita "${word}"`);
}
