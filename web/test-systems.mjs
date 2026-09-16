import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import * as THREE from 'three';
import {POWER_FUEL_LAYOUT, SURVIVAL_CELL_LAYOUT, SUSPENSION_LAYOUT, SYSTEM_CATALOG, SYSTEM_IDS, advanceLocalSpin} from './src/systems.js';

const expected = [
  ['aero', '0:14'], ['structure', '4:47'], ['suspension', '5:19'],
  ['steering', '7:52'], ['brakes', '8:57'], ['power', '11:32'],
  ['ers', '14:14'], ['cooling', '14:54'], ['fuel', '15:39'],
  ['transmission', '16:42'], ['safety', '17:03'], ['cockpit', '17:51'],
  ['wheel', '19:17'], ['sensors', '22:11'],
];

assert.equal(SYSTEM_CATALOG.length, 14, 'o catálogo deve ter 14 camadas');
assert.equal(SYSTEM_IDS.length, 14, 'a lista de IDs deve acompanhar o catálogo');
assert.deepEqual(SYSTEM_IDS, expected.map(([id]) => id), 'IDs fora da ordem factual do vídeo');
assert.equal(new Set(SYSTEM_IDS).size, SYSTEM_IDS.length, 'IDs duplicados');

const timestamp = /^\d{1,2}:\d{2}$/;
const color = /^#[0-9a-f]{6}$/i;
for (const [index, system] of SYSTEM_CATALOG.entries()) {
  assert.equal(system.id, expected[index][0], `ID inválido na camada ${index + 1}`);
  assert.equal(system.number, String(index + 1).padStart(2, '0'), `numeração inválida em ${system.id}`);
  assert.equal(system.chapter, expected[index][1], `timestamp inválido em ${system.id}`);
  assert.match(system.chapter, timestamp, `timestamp malformado em ${system.id}`);
  assert.equal(typeof system.label, 'string');
  assert.ok(system.label.trim().length >= 3, `rótulo vazio em ${system.id}`);
  assert.equal(typeof system.short, 'string');
  assert.ok(system.short.trim().length >= 2, `rótulo curto vazio em ${system.id}`);
  assert.equal(typeof system.description, 'string');
  assert.ok(system.description.trim().length >= 40, `descrição insuficiente em ${system.id}`);
  assert.match(system.color, color, `cor inválida em ${system.id}`);
}

assert.equal(Object.isFrozen(SYSTEM_CATALOG), true, 'catálogo deve ser imutável');
assert.equal(Object.isFrozen(SYSTEM_IDS), true, 'IDs devem ser imutáveis');

const source = readFileSync(new URL('./src/systems.js', import.meta.url), 'utf8');
const template = readFileSync(new URL('./src/template-v2.html', import.meta.url), 'utf8');
const workbench = readFileSync(new URL('./src/workbench.js', import.meta.url), 'utf8');
const manifest = JSON.parse(readFileSync(new URL('./assets/power-unit-v1.manifest.json', import.meta.url), 'utf8'));
const tabMarkup = [...template.matchAll(/<button id="tab-[^"]+"[^>]*role="tab"[^>]*>/g)].map(([tag]) => tag);
assert.equal(tabMarkup.length, 6, 'a bancada deve ter seis abas');
assert.equal(tabMarkup.filter(tag => /aria-selected="(?:true|false)"/.test(tag)).length, 6, 'as seis abas devem expor aria-selected');
assert.match(workbench, /panel\.id='lab-panel'/, 'o painel dinâmico deve ter ID estável');
assert.match(workbench, /panel\.setAttribute\('role','tabpanel'\)/, 'o painel dinâmico deve ser um tabpanel');
assert.match(workbench, /tabs\.forEach\(tab=>tab\.setAttribute\('aria-controls','lab-panel'\)\)/, 'as seis abas devem apontar para o tabpanel');
assert.equal((template.match(/class="system-card"/g) || []).length, 14, 'a bancada Sistemas deve ter 14 botões');
const systemsPanelStart = template.indexOf('id="systems-panel"');
const detailIndex = template.indexOf('id="system-detail"');
const listIndex = template.indexOf('id="system-list"');
assert.ok(systemsPanelStart >= 0, 'o painel Sistemas deve ter ID estável');
assert.ok(detailIndex > systemsPanelStart && listIndex > detailIndex, 'o detalhe deve preceder a lista no painel Sistemas');
assert.doesNotMatch(template.slice(systemsPanelStart), /clique para selecionar/i, 'Sistemas não deve anunciar clique para selecionar');
assert.match(source, /const systemsHint='SISTEMAS: USE TAB E SETAS PARA ESCOLHER/, 'Sistemas deve substituir a dica por instruções de teclado');
assert.match(source, /card\.tabIndex=item\.id===rovingId\?0:-1/, 'a seleção deve manter somente um cartão no tab order');
assert.match(source, /card\.tabIndex=index===0\?0:-1/, 'o primeiro cartão deve iniciar com tabindex 0');
assert.match(source, /if\(selected\)chapterLink\.setAttribute\('aria-current','true'\)/, 'o capítulo do sistema selecionado deve ser marcado');
assert.match(source, /if\(overview\)ui\.chapters\.forEach\(link=>link\.removeAttribute\('aria-current'\)\)/, 'a visão geral deve limpar aria-current');
assert.equal((template.match(/data-view="(?:hero|side|front|rear|top|bottom)"/g) || []).length, 6, 'as seis vistas devem permanecer associadas');
assert.match(source, /current2026/, 'o seletor ERS 2021/2026 deve permanecer disponível');
const powerSource = source.slice(source.indexOf('const power='), source.indexOf('const ers='));
const ersSource = source.slice(source.indexOf('const ers='), source.indexOf('const cooling='));
const coolingSource = source.slice(source.indexOf('const cooling='), source.indexOf('const fuel='));
const fuelSource = source.slice(source.indexOf('const fuel='), source.indexOf('const transmission='));
const transmissionSource = source.slice(source.indexOf('const transmission='), source.indexOf('const safety='));
const safetySource = source.slice(source.indexOf('const safety='), source.indexOf('const cockpit='));
const cockpitSource = source.slice(source.indexOf('const cockpit='), source.indexOf('const wheel='));

const vector = (name) => {
  const match = source.match(new RegExp(`(?:\\b(?:const|let|var)\\s+|,)\\s*${name}\\s*=\\s*\\[([^\\]]+)\\]`));
  assert.ok(match, `${name} deve ser declarado como vetor`);
  const values = match[1].split(',').map(Number);
  assert.equal(values.length, 3, `${name} deve ter três coordenadas`);
  assert.ok(values.every(Number.isFinite), `${name} deve conter apenas coordenadas numéricas`);
  return values;
};

const arrayLiteral = (name) => {
  const assignment = source.match(new RegExp(`(?:\\b(?:const|let|var)\\s+|,)\\s*${name}\\s*=\\s*`));
  assert.ok(assignment, `${name} deve ser atribuído a um array`);
  const start = source.indexOf('[', assignment.index + assignment[0].length);
  assert.ok(start >= 0, `${name} deve iniciar com um array`);
  let depth = 0;
  for (let index = start; index < source.length; index += 1) {
    if (source[index] === '[') depth += 1;
    if (source[index] === ']') {
      depth -= 1;
      if (depth === 0) return source.slice(start, index + 1);
    }
  }
  assert.fail(`${name} deve ter um array balanceado`);
};

const numericPoints = (name) => {
  const literal = arrayLiteral(name);
  const point = /\[\s*(-?(?:\d+(?:\.\d*)?|\.\d+))\s*,\s*(-?(?:\d+(?:\.\d*)?|\.\d+))\s*,\s*(-?(?:\d+(?:\.\d*)?|\.\d+))\s*\]/g;
  return [...literal.matchAll(point)].map(([, x, y, z]) => [Number(x), Number(y), Number(z)]);
};

const assertNear = (actual, expected, message) => assert.ok(Math.abs(actual - expected) < 1e-9, `${message}: ${actual} !== ${expected}`);

assert.match(powerSource, /Turbo único · compressor/, 'Power deve ter compressor de turbo único');
assert.match(powerSource, /Turbo único · turbina/, 'Power deve ter turbina do mesmo turbo');
assert.match(powerSource, /Eixo comum do turbo/, 'Power deve ligar compressor e turbina por eixo comum');
assert.match(powerSource, /MGU-H · legado 2021/, 'Power deve representar o MGU-H legado');
assert.match(powerSource, /Acoplamento coaxial MGU-H · eixo do turbo/, 'Power deve ligar MGU-H ao eixo do turbo');
assert.match(powerSource, /addSpinner\(mguh,'y',-1\.4\)/, 'MGU-H deve girar no próprio eixo local');
assert.match(powerSource, /addSpinner\(mguHDrive,'y',-1\.4\)/, 'acoplamento do MGU-H deve girar no próprio eixo local');
assert.match(powerSource, /MGU-H · LEGADO 2021/, 'Power deve exibir identificação textual do MGU-H legado');
assert.match(powerSource, /CONTEXTO 2026 · MGU-H REMOVIDO/, 'Power deve exibir o contexto temporal de 2026');
assert.match(source, /let mguhTag=null,currentContextTag=null/, 'Power deve manter referências explícitas às etiquetas de contexto');
assert.match(source, /function syncERSContextTags\(\)/, 'as etiquetas de contexto devem ter sincronização explícita');
assert.match(source, /mguhTag\.visible=active==='power'&&legacyVisible/, 'a etiqueta legada deve acompanhar o modo 2021 somente em Power');
assert.match(source, /currentContextTag\.visible=active==='power'&&!legacyVisible/, 'a etiqueta 2026 deve acompanhar o modo atual somente em Power');
assert.match(source, /setERSContext\(mode\).*syncERSContextTags\(\)/, 'a troca de contexto deve sincronizar as etiquetas');
assert.match(source, /updateUI\(id\);syncERSContextTags\(\);frame\(id/, 'show deve reaplicar o contexto depois de atualizar a interface');
assert.doesNotMatch(powerSource, /markLegacy\(addTag\(power,'CONTEXTO 2026/, 'a etiqueta 2026 não deve ser marcada como legado');
assert.doesNotMatch(source, /object\.rotation\[axis\]\+=/, 'spinners não devem acumular Euler em eixos diferentes');
for (const axis of ['x', 'y', 'z']) {
  const localAxis = new THREE.Vector3(axis === 'x' ? 1 : 0, axis === 'y' ? 1 : 0, axis === 'z' ? 1 : 0);
  const base = new THREE.Quaternion().setFromEuler(new THREE.Euler(.31, -.22, .47));
  const expectedDirection = localAxis.clone().applyQuaternion(base);
  let animated = base.clone();
  for (let step = 0; step < 240; step += 1) animated = advanceLocalSpin(animated, axis, .017);
  const actualDirection = localAxis.clone().applyQuaternion(animated);
  assert.ok(actualDirection.distanceTo(expectedDirection) < 1e-9, `o eixo local ${axis} deve permanecer invariável após vários passos`);
}
const turboStart = vector('turboAxisStart');
const turboEnd = vector('turboAxisEnd');
assertNear(turboStart[0], 0, 'compressor deve estar central no eixo X');
assertNear(turboEnd[0], 0, 'turbina deve estar central no eixo X');
assertNear(turboStart[1], turboEnd[1], 'compressor e turbina devem compartilhar a altura');
assert.ok(turboStart[2] > turboEnd[2], 'compressor deve estar à frente da turbina no eixo Z');
assert.ok(turboStart[2] - turboEnd[2] > .5, 'eixo comum deve ter comprimento didático mensurável');
assert.match(powerSource, /turboCompressor=torus\([^;]*turboAxisStart[^;]*\[0,0,0\]\),turboTurbine=torus\([^;]*turboAxisEnd[^;]*\[0,0,0\]\)/, 'os dois rotores devem usar a orientação coaxial padrão');
assert.match(powerSource, /turboShaft=beam\(power,turboAxisStart,turboAxisEnd,[^,]+,[^,]+,'Eixo comum do turbo · coaxial em Z'/, 'o eixo comum deve unir os dois centros em Z');
assert.match(powerSource, /Wastegate/, 'Power deve nomear wastegate corretamente');
assert.match(powerSource, /Intercooler didático/, 'Power deve representar intercooler');
assert.match(powerSource, /Compressor → intercooler · ar pressurizado/, 'a admissão deve sair do compressor para o intercooler');
assert.match(powerSource, /Intercooler → manifold dos plenums/, 'a admissão deve sair do intercooler para o manifold');
assert.match(powerSource, /Manifold → plenum \$\{side<0\?'esquerdo':'direito'\} · HIP/, 'o manifold deve ramificar para os dois plenums');
assert.match(powerSource, /Plenum → velocity stack \$\{side\} \$\{z\}/, 'cada plenum deve alimentar suas stacks');
assert.match(powerSource, /pipe\(power,\[\[0,.60,-\.28\],\[0,.74,-\.25\],\[0,.86,-\.20\]\],\.014,powerAir,'Compressor → intercooler/, 'o primeiro caminho de admissão deve ter pontos contínuos');
assert.match(powerSource, /pipe\(power,\[\[0,.86,-\.07\],\[0,.87,-\.34\],\[0,.88,-\.45\]\],\.014,powerAir,'Intercooler → manifold/, 'o segundo caminho de admissão deve terminar no manifold');
assert.match(powerSource, /for\(const side of \[-1,1\]\)\{const plenumCenter=\[side\*\.20,.88,-\.75\]/, 'Power deve declarar os dois plenums por lado');
assert.equal((powerSource.match(/Velocity stack \/ trompeta representativa/g) || []).length, 1, 'Power deve usar um loop determinístico de trompetas');
assert.match(powerSource, /for\(const z of \[-\.95,-\.75,-\.55\]\)/, 'Power deve distribuir três stacks por cabeçote');
assert.match(powerSource, /new THREE\.CylinderGeometry\(\.068,\.032,.12,16,1,true\)/, 'as seis stacks devem ser geometrias cilíndricas sem tampa');
assert.match(powerSource, /Boca aberta da velocity stack/, 'cada stack deve ter boca aberta visual');
assert.match(SYSTEM_CATALOG.find(system => system.id === 'power').description, /contagem e o material.*não são verificáveis/, 'Power deve limitar a inferência dos plenums/stacks');
assert.doesNotMatch(powerSource, /Turbo compressor esquerdo|Turbo compressor direito/, 'Power não deve sugerir twin-turbo');
assert.doesNotMatch(powerSource, /turboCompressor=torus\([^;]*\[-?\.14[\s,]/, 'Power não deve manter compressor lateral');
assert.doesNotMatch(powerSource, /turboTurbine=torus\([^;]*\[\+?\.14[\s,]/, 'Power não deve manter turbina lateral');
assert.match(source, /legacy2021|current2026/, 'ERS deve oferecer contexto temporal explícito');
assert.match(ersSource, /powerCardName='Motor V6 turbo'/, 'ERS deve manter o nome real do cartão Power');
assert.match(ersSource, /MGU-H legado → \$\{powerCardName\}/, 'ERS deve apontar a inspeção para o nome real do cartão Power');
assert.doesNotMatch(ersSource, /cylinder\(ers,[^;]*MGU-H|Acoplamento coaxial MGU-H/, 'ERS não deve duplicar a geometria do MGU-H');
assert.match(ersSource, /Control electronics \/ inverter/, 'ERS deve representar eletrônica de controle/inversor');
assert.match(ersSource, /Recuperação para energy store/, 'ERS deve representar caminho de recuperação');
assert.match(ersSource, /Entrega ao MGU-K/, 'ERS deve representar caminho de entrega');
assert.equal((coolingSource.match(/Circuito (motor \/ óleo|ERS \/ bateria|hidráulica \/ câmbio)/g) || []).length, 3, 'Cooling deve separar três circuitos nomeados');
assert.match(coolingSource, /Fluxo motor \/ óleo/, 'Cooling deve animar fluxo de motor/óleo');
assert.match(coolingSource, /Fluxo ERS \/ bateria/, 'Cooling deve animar fluxo de ERS/bateria');
assert.match(coolingSource, /Fluxo hidráulica \/ câmbio/, 'Cooling deve animar fluxo hidráulica/câmbio');
assert.match(coolingSource, /Intercooler ar-ar · sidepod esquerdo · HIP/, 'Cooling deve marcar intercooler esquerdo como hipótese');
assert.match(coolingSource, /const rightExchangers=\[\['motor \/ óleo',\.34,coolEngineLine\],\['ERS \/ bateria',\.50,coolERSLine\],\['hidráulica \/ câmbio',\.66,coolHydLine\]\]/, 'Cooling deve ter três trocadores nomeados no lado direito');
for (const pathName of ['coolingAir', 'coolingEngine', 'coolingERS', 'coolingHyd']) {
  const path = numericPoints(pathName);
  assert.equal(path.length, 4, `${pathName} deve ter quatro pontos de rota`);
  assert.notDeepEqual(path[0], path.at(-1), `${pathName} não pode ser um caminho degenerado`);
}
assert.match(coolingSource, /pipe\(cooling,coolingAir,[^,]+,coolAirLine,'Ar de admissão → intercooler esquerdo · HIP'/, 'Cooling deve ligar o ar ao intercooler esquerdo');
assert.match(coolingSource, /pipe\(cooling,coolingEngine,[^,]+,coolEngineLine,'Circuito motor \/ óleo → trocador correspondente'/, 'Cooling deve ligar motor/óleo ao trocador correspondente');
assert.match(coolingSource, /pipe\(cooling,coolingERS,[^,]+,coolERSLine,'Circuito ERS \/ bateria → trocador correspondente'/, 'Cooling deve ligar ERS/bateria ao trocador correspondente');
assert.match(coolingSource, /pipe\(cooling,coolingHyd,[^,]+,coolHydLine,'Circuito hidráulica \/ câmbio → trocador correspondente'/, 'Cooling deve ligar hidráulica/câmbio ao trocador correspondente');
assert.ok(numericPoints('coolingEngine').at(-1)[0] > 0, 'o caminho motor/óleo deve chegar ao conjunto direito');
assert.ok(numericPoints('coolingERS').at(-1)[0] > 0, 'o caminho ERS/bateria deve chegar ao conjunto direito');
assert.ok(numericPoints('coolingHyd').at(-1)[0] > 0, 'o caminho hidráulica/câmbio deve chegar ao conjunto direito');
assert.match(SYSTEM_CATALOG.find(system => system.id === 'cooling').description, /assimétrica hipotética.*não é simulação térmica/, 'Cooling deve explicitar hipótese e limite');
assert.match(fuelSource, /Célula única flexível \/ bladder/, 'Fuel deve manter uma única célula flexível');
assert.match(fuelSource, /Contenção estrutural da célula/, 'Fuel deve ter contenção estrutural');
assert.match(fuelSource, /Sensor de pressão do combustível/, 'Fuel deve ter sensor de pressão');
assert.match(fuelSource, /Válvula breakaway auto-selante/, 'Fuel deve ter válvula breakaway auto-selante');
assert.match(fuelSource, /Linha segura de alimentação · .*fora do cockpit/, 'Fuel deve manter linha segura fora do cockpit');
const aabb = ({center, size}) => center.map((value, axis) => [value - size[axis] / 2, value + size[axis] / 2]);
const contains = (outer, inner) => inner.every(([min, max], axis) => min >= outer[axis][0] && max <= outer[axis][1]);
const pointBounds = point => point.map(value => [value, value]);
const powerBlockBounds = aabb(POWER_FUEL_LAYOUT.powerBlock);
const fuelCellBounds = aabb(POWER_FUEL_LAYOUT.fuelCell);
const fuelContainmentBounds = aabb(POWER_FUEL_LAYOUT.fuelContainment);
const survivalCellBounds = aabb(SURVIVAL_CELL_LAYOUT);
const energyStoreBounds = aabb(POWER_FUEL_LAYOUT.energyStore);
const disjoint = (first, second) => first.some(([min, max], axis) => max < second[axis][0] || min > second[axis][1]);
assertNear(POWER_FUEL_LAYOUT.fuelCell.center[2], -.07, 'a célula deve usar o ponto didático centralizado atrás do cockpit');
assertNear(POWER_FUEL_LAYOUT.fuelContainment.center[2], -.07, 'a contenção deve acompanhar o ponto didático do tanque');
assertNear(POWER_FUEL_LAYOUT.energyStore.center[2], -.07, 'a bateria deve acompanhar longitudinalmente o tanque');
assert.ok(contains(fuelContainmentBounds, fuelCellBounds), 'a célula deve estar contida na contenção');
assert.ok(contains(survivalCellBounds, fuelContainmentBounds), 'a contenção do tanque deve estar dentro da survival cell didática');
assert.ok(fuelContainmentBounds[2][1] < POWER_FUEL_LAYOUT.cockpitRegionZ[0], 'o tanque deve ficar atrás da região do cockpit');
assert.ok(survivalCellBounds[2][0] < fuelContainmentBounds[2][0], 'a survival cell deve começar antes do tanque');
assert.ok(fuelContainmentBounds[2][0] > powerBlockBounds[2][1], 'o tanque deve ficar separado e à frente do motor');
assert.ok(energyStoreBounds[1][1] < fuelCellBounds[1][0], 'a bateria didática deve ficar abaixo do tanque');
assert.ok(disjoint(fuelContainmentBounds, powerBlockBounds), 'a contenção do tanque não deve interpenetrar o motor');
assert.ok(disjoint(fuelContainmentBounds, energyStoreBounds), 'a contenção do tanque não deve interpenetrar a bateria');
const separatingGaps = fuelCellBounds.map(([cellMin, cellMax], axis) => [
  powerBlockBounds[axis][0] - cellMax,
  cellMin - powerBlockBounds[axis][1],
]);
const separatingAxes = separatingGaps.filter(([before, after]) => before > 0 || after > 0);
assert.ok(separatingAxes.length > 0, 'a caixa da célula não deve interpenetrar o powerBlock em X/Y/Z');
assert.ok(Math.max(...separatingAxes.flat()) > 0, 'a célula deve manter separação positiva do powerBlock');
const fuelRoute = POWER_FUEL_LAYOUT.fuelRoute;
assert.ok(fuelRoute.length >= 2, 'a rota de combustível deve ter pelo menos dois pontos');
assert.ok(fuelRoute.every(point => point.length === 3 && point.every(Number.isFinite)), 'a rota de combustível deve ter pontos tridimensionais finitos');
assert.deepEqual(fuelRoute[0], POWER_FUEL_LAYOUT.fuelPump, 'a rota de combustível deve iniciar na bomba');
assert.ok(contains(fuelContainmentBounds, pointBounds(fuelRoute[0])), 'a rota deve começar dentro da contenção do tanque');
assert.ok(fuelRoute.some((point, index) => index > 0 && point.some((value, axis) => value !== fuelRoute[index - 1][axis])), 'a rota de combustível não pode ser degenerada');
const motorEndpoint = fuelRoute.at(-1);
assert.ok(motorEndpoint.every((value, axis) => value >= powerBlockBounds[axis][0] && value <= powerBlockBounds[axis][1]), 'a rota de combustível deve terminar na região do motor');
assert.ok(fuelRoute.slice(1).every(point => point[2] < POWER_FUEL_LAYOUT.cockpitRegionZ[0]), 'a rota não deve atravessar a região do cockpit');
assert.doesNotMatch(fuelSource, /z=\+1\.04|\[0,\.39,1\.04\]/, 'Fuel não deve manter a alimentação para a dianteira');
assert.equal(Object.isFrozen(SUSPENSION_LAYOUT), true, 'layout da suspensão deve ser imutável');
for (const layout of [SUSPENSION_LAYOUT.front, SUSPENSION_LAYOUT.rear]) {
  assert.equal(Object.isFrozen(layout), true, 'cada eixo do layout deve ser imutável');
  for (const point of Object.values(layout)) if (Array.isArray(point)) {
    assert.equal(Object.isFrozen(point), true, 'pontos do layout devem ser imutáveis');
    assert.equal(point.length, 3, 'ponto da suspensão deve ter três coordenadas');
    assert.ok(point.every(Number.isFinite), 'ponto da suspensão deve conter coordenadas numéricas');
  }
}
assert.ok(SUSPENSION_LAYOUT.front.rockerHigh[1] > SUSPENSION_LAYOUT.front.uprightLower[1], 'pushrod dianteiro deve subir do ponto inferior do upright ao rocker alto');
assert.ok(SUSPENSION_LAYOUT.rear.uprightUpper[1] > SUSPENSION_LAYOUT.rear.gearboxLow[1], 'pullrod traseiro deve descer do ponto superior do upright ao rocker baixo');
const gearboxBounds = aabb(POWER_FUEL_LAYOUT.gearbox);
assert.ok(SUSPENSION_LAYOUT.rear.gearboxLow.every((value, axis) => value >= gearboxBounds[axis][0] && value <= gearboxBounds[axis][1]), 'ponto baixo do pullrod deve estar vinculado ao envelope do gearbox');
assert.match(source, /SUSPENSION_LAYOUT\.front/, 'Suspensão deve usar o layout dianteiro exportado');
assert.match(source, /SUSPENSION_LAYOUT\.rear/, 'Suspensão deve usar o layout traseiro exportado');
assert.equal(manifest.scope, 'GLB original e didático sem MGU-H; overlay web com referência didática MGU-H legado 2021; não é CAD, engenharia ou homologação.', 'manifesto deve distinguir GLB e overlay web e preservar o limite didático');
assert.equal((transmissionSource.match(/for\(const relation of \[1,2,3,4,5,6,7,8\]\)/g) || []).length, 1, 'Transmission deve iterar oito relações à frente');
assert.match(transmissionSource, /Engrenagem R · ré/, 'Transmission deve representar ré');
assert.match(transmissionSource, /Eixo primário/, 'Transmission deve representar eixo primário');
assert.match(transmissionSource, /Eixo secundário/, 'Transmission deve representar eixo secundário');
assert.match(transmissionSource, /8 F \+ 1 R \/ DIF\./, 'Transmission deve mostrar contador 8 F + 1 R');
assert.match(transmissionSource, /transShellMat=.*opacity:\.20/, 'Transmission deve usar carcaça translúcida para inspeção');
assert.match(transmissionSource, /Janela didática de inspeção das relações · não é corte real/, 'Transmission deve expor janela didática');
assert.equal((transmissionSource.match(/for\(const side of \[-1,1\]\)\{/g) || []).length, 1, 'Transmission deve percorrer as duas saídas do diferencial');
assert.equal((transmissionSource.match(/for\(let roller=0;roller<3;roller\+\+\)/g) || []).length, 1, 'Transmission deve usar três roletes por junta');
assert.match(transmissionSource, /Junta tripóide esquemática/, 'Transmission deve identificar a junta tripóide como esquemática');
assert.match(transmissionSource, /Driveshaft → junta tripóide esquemática/, 'Transmission deve ligar junta tripóide ao driveshaft');
assert.doesNotMatch(transmissionSource, /rolamento real|rolamentos reais/, 'Transmission não deve declarar rolamentos reais');
assert.match(SYSTEM_CATALOG.find(system => system.id === 'transmission').description, /representativos|não relações reais/, 'Transmission deve deixar claro o limite didático');

// Os nomes são templates dentro de loops: validar a expansão determinística,
// não a quantidade de ocorrências textuais no arquivo-fonte.
assert.equal((safetySource.match(/for\(const side of \[-1,1\]\)/g) || []).length, 1, 'Safety deve percorrer os dois lados');
assert.equal((safetySource.match(/for\(const \[z,anchorY,offset\] of \[\[1\.34[\s\S]*?\[-1\.72/g) || []).length, 1, 'Safety deve cobrir os dois eixos');
assert.equal((safetySource.match(/for\(const tether of \[0,1,2\]\)/g) || []).length, 1, 'cada roda deve iterar três cabos');
assert.match(safetySource, /`Cabo de retenção da roda \$\{tether\+1\} \$\{side\} \$\{z\}`/, 'cabos de roda devem ter índice, lado e eixo no nome');
assert.equal(2 * 2 * 3, 12, 'a expansão dos cabos deve produzir três cabos nas quatro rodas');
assert.match(source, /Halo perna central/, 'Halo deve ter perna central separada');
assert.match(source, /Estrutura primária de capotamento/, 'estrutura primária deve permanecer distinta do Halo');
assert.equal((cockpitSource.match(/for\(const side of \[-1,1\]\)\{beam\(cockpit,\[side\*\.20/g) || []).length, 1, 'o loop do arnês deve percorrer os dois lados');
const harnessKinds = [...cockpitSource.matchAll(/`Arnês ([^`]+) \$\{side\}`/g)].map(([_, kind]) => kind).sort();
assert.deepEqual(harnessKinds, ['ombro', 'quadril', 'subabdominal'], 'arnês deve declarar três categorias de pontos');
assert.equal(harnessKinds.length * 2, 6, 'a expansão do arnês deve produzir seis pontos');
assert.match(source, /FHR \/ HANS yoke/, 'FHR/HANS deve ter yoke visual');
assert.match(source, /Headrest \/ apoio de cabeça/, 'headrest deve ser um componente separado');
assert.match(source, /Linha de pressão Pitot/, 'pressão do Pitot deve ter linha própria');
assert.match(source, /ECU \/ unidade de aquisição/, 'ECU deve ser representada');
assert.match(source, /Telemetria carro → box/, 'telemetria deve indicar o sentido carro para box');
assert.match(source, /Microfone\/acústica do motor/, 'microfone deve usar nomenclatura didática');
assert.match(source, /VOLANTE \/ COMANDOS/, 'etiqueta do volante deve ser corrigida');
assert.match(source, /Quick-release/, 'volante deve ter quick-release');
console.log('Sistemas: 14 camadas, IDs únicos, ordem/timestamps do vídeo, descrições, cores e imutabilidade OK.');
