import * as THREE from 'three';
import {describePart} from './parts-info.js';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';
import {fetchBakedOcclusion,tryAttachBakedOcclusion,patchBakedOcclusion} from './baked-ao.js';

// Catálogo dos 14 sistemas na ordem dos capítulos do vídeo de referência (Animagraffs, 2021).
// A geometria vem de web/assets/sistemas-v1.glb, gerada por ferramentas/gerar_sistemas.py (Blender 5.2):
// malhas originais INTEIA em escala do carro v2, com materiais físicos e peças nomeadas.
// É uma camada didática de estudo, não CAD de fabricante nem homologação.
export const SYSTEM_CATALOG=Object.freeze([
 {id:'aero',spread:[0,-.9,0],number:'01',label:'Aerodinâmica',short:'AERO',chapter:'0:14',color:'#52c8df',howItWorks:'As asas, o assoalho e o difusor desviam o ar para criar uma diferença de pressão que empurra o carro contra a pista. Essa carga dá aderência nas curvas e cobra arrasto nas retas. Os túneis do assoalho aceleram o ar por baixo e o difusor o desacelera na saída, o que suga o carro contra o chão com menos arrasto do que as asas cobrariam pela mesma carga.',observe:'Siga as fitas de ar do bico ao difusor e veja como os túneis do assoalho se estreitam antes de abrir na saída. Abra a vista explodida para separar asa de viga, defletores e o atuador hidráulico do flap traseiro.',description:'Tudo o que a carroceria esconde e que produz carga aerodinâmica: túneis do assoalho, cercas de borda, palhetas do difusor, asa de viga, atuador hidráulico do flap traseiro, defletores e ajustadores da asa dianteira. As fitas mostram o caminho do ar.'},
 {id:'structure',spread:[0,1.0,0],number:'02',label:'Estrutura central / survival cell',short:'ESTRUTURA',chapter:'4:47',color:'#c5a7ff',howItWorks:'A célula de sobrevivência é a espinha do carro: um casco de carbono e colmeia que protege o piloto e recebe as cargas de todos os outros sistemas. Na frente ancoram suspensão e direção; atrás, o motor se aparafusa direto nela e o câmbio completa a estrutura até a asa traseira.',observe:'Observe a janela de corte que revela o núcleo em colmeia e os insertos de titânio onde a suspensão se prende. Com a vista explodida, veja os prisioneiros que unem a célula ao motor.',description:'A célula de sobrevivência: sanduíche de carbono e colmeia com janela de corte no núcleo, anteparas, prisioneiros do motor, insertos de titânio das ancoragens da suspensão e prancha com patins. Motor e câmbio se aparafusam atrás dela e completam a estrutura.'},
 {id:'suspension',spread:[0,.5,1.1],number:'03',label:'Suspensão',short:'SUSPENSÃO',chapter:'5:19',color:'#f1bd68',howItWorks:'Cada roda é guiada por dois wishbones até o upright. O movimento vertical sobe pelo push-rod na frente e pelo pull-rod atrás até os balancins, que acionam barras de torção, amortecedores e o elemento de heave dentro da carroceria, controlando rolagem, mergulho e a altura do assoalho.',observe:'Compare os dois eixos: na frente a haste sobe em diagonal até o balancim no alto do chassi; atrás ela desce até a carcaça do câmbio. Clique nos balancins e amortecedores para ler a função de cada peça.',description:'Wishbones em perfil de asa, uprights usinados, push-rod dianteiro e pull-rod traseiro acionando balancins, barras de torção, amortecedores internos, elemento de heave com molas de prato e barras antirrolagem. Os pontos de ancoragem são compartilhados com direção, freios e cabos de retenção.'},
 {id:'steering',spread:[0,.7,1.7],number:'04',label:'Direção',short:'DIREÇÃO',chapter:'7:52',color:'#ff8c6b',howItWorks:'Ao girar o volante, a coluna com juntas universais aciona o pinhão, que desloca a cremalheira na antepara dianteira. As barras de direção levam esse deslocamento aos uprights e esterçam as rodas, com assistência hidráulica para reduzir o esforço do piloto.',observe:'Acompanhe a cadeia volante, coluna, cremalheira, barras e uprights. Note que as barras de direção seguem quase paralelas aos wishbones, com o mesmo perfil de asa.',description:'Coluna de carbono com duas juntas universais, pinhão e cremalheira na antepara dianteira, barras de direção em perfil de asa até os uprights, servo hidráulico e linhas de assistência.'},
 {id:'brakes',spread:[0,-.6,.9],number:'05',label:'Freios',short:'FREIOS',chapter:'8:57',color:'#ff665d',howItWorks:'O pedal pressiona dois cilindros mestres, um por eixo, e a barra de balanço reparte a força entre frente e trás. As pinças apertam os discos de carbono, que podem superar 1.000 °C em frenagens intensas; no eixo traseiro o brake-by-wire combina o freio hidráulico com a recuperação de energia do MGU-K.',observe:'Siga as linhas do pedal até as pinças e compare os dutos de refrigeração dianteiros e traseiros. Clique em um disco para ver sua construção ventilada.',description:'Discos carbono-carbono ventilados, campanas, pinças monobloco de seis pistões, tambores e dutos de refrigeração, pedal usinado no pé esquerdo, dois cilindros mestres com barra de balanço, brake-by-wire traseiro e linhas rígidas e trançadas.'},
 {id:'power',spread:[0,1.3,-.4],number:'06',label:'Unidade de potência',short:'V6 TURBO',chapter:'11:32',color:'#ff9f58',howItWorks:'O V6 turbo de 1,6 litro queima combustível e entrega torque ao câmbio. A turbina, movida pelos gases de escape, aciona o compressor que enche os cilindros de ar, e a wastegate controla a pressão desviando parte dos gases. Nesta montagem os dois ficam separados nas pontas do motor, ligados por um eixo que atravessa o vale entre as bancadas, o que afasta o ar frio da admissão do calor do escape.',observe:'Abra as tampas para ver os dois plenums e as seis trompetas e siga as fitas de admissão, carga e escape. Use o seletor de época para acompanhar o eixo do turbo: com o MGU-H ele também gera energia elétrica; sem ele, o conjunto apenas comprime o ar.',description:'V6 de 1,6 litro a 90° com cárter seco, cabeçotes e tampas de comando, turbo dividido (compressor à frente, turbina atrás, eixo comum pelo vale do motor), dois plenums com seis trompetas, duto do airbox, dutos do intercooler, coletores em Inconel, wastegates e escapamento. Na versão 2021 o MGU-H fica acoplado ao eixo do turbo; em 2026 ele deixa de existir.'},
 {id:'ers',spread:[0,-.8,-.3],number:'07',label:'ERS híbrido',short:'ERS',chapter:'14:14',color:'#ffe36b',howItWorks:'O ERS recupera energia nas frenagens pelo MGU-K, guarda-a no energy store e devolve essa energia às rodas na aceleração. A eletrônica de controle e o inversor administram esse fluxo pelos cabos de alta tensão. Em 2026 o MGU-K chega a 350 kW e responde por cerca de metade da potência do carro.',observe:'Alterne entre 2021 e 2026 e compare os caminhos de energia: com MGU-H há duas fontes de recuperação; sem ele, tudo passa pelo MGU-K. Abra a tampa do energy store para ver as células.',description:'O sistema híbrido: energy store sob o tanque, eletrônica de controle e inversor, MGU-K engrenado ao virabrequim e, na versão 2021, o MGU-H no turbo. Cabos laranja de alta tensão ligam tudo; as fitas mostram a recuperação na frenagem e a entrega na aceleração.'},
 {id:'cooling',spread:[0,-.4,-1.1],number:'08',label:'Refrigeração',short:'REFRIGERAÇÃO',chapter:'14:54',color:'#66e0b2',howItWorks:'O ar que entra pelos sidepods atravessa radiadores e arrefecedores que retiram calor da água do motor, do óleo, do ar comprimido pelo turbo e dos componentes elétricos do ERS. Cada fluido circula em seu próprio circuito até o trocador certo.',observe:'Compare os dois sidepods: intercooler e arrefecedor do câmbio de um lado, radiador de água e arrefecedores de óleo e do ERS do outro. Siga as fitas para ver cada circuito separado.',description:'Refrigeração assimétrica: intercooler ar-ar inclinado e arrefecedor do câmbio no sidepod esquerdo; radiador de água, arrefecedor de óleo e arrefecedor de baixa temperatura do ERS no direito, com tanques, mangueiras e abraçadeiras. Circuitos separados de água, óleo, ERS e hidráulica.'},
 {id:'fuel',spread:[0,.8,.3],number:'09',label:'Célula de combustível',short:'COMBUSTÍVEL',chapter:'15:39',color:'#e6c06d',howItWorks:'O combustível fica numa célula flexível entre o piloto e o motor, o ponto mais protegido do carro. Chicanas internas impedem que ele se desloque nas curvas, o pote coletor garante alimentação contínua e as bombas o enviam ao motor passando pelo medidor de vazão. Em 2026 o combustível é totalmente sustentável.',observe:'Veja o nível de combustível dentro da célula e o pote coletor no fundo. Siga a fita de combustível até o motor e note que a linha passa fora do cockpit.',description:'Célula flexível em Kevlar atrás do piloto e à frente do motor, com chicanas internas, pote coletor, bombas de elevação, medidor de vazão, acoplamento de abastecimento, válvula autosselante e linhas de combustível fora do cockpit.'},
 {id:'transmission',spread:[0,.4,-1.5],number:'10',label:'Câmbio e diferencial',short:'TRANSMISSÃO',chapter:'16:42',color:'#b7c2cc',howItWorks:'A embreagem multidisco liga o motor à caixa de oito marchas, onde pares de engrenagens em tomada constante são engatados pelo tambor seletor em milissegundos. Pinhão e coroa viram o movimento em 90°, e o diferencial reparte o torque entre os semieixos para que as rodas girem em velocidades diferentes nas curvas.',observe:'Abra a carcaça e observe as engrenagens girando em cada relação. Siga o caminho da embreagem às marchas, ao diferencial, às juntas tripoide e às rodas.',description:'Carcaça estrutural com janela de corte, embreagem multidisco, oito pares de engrenagens em tomada constante mais ré com anéis de engate e tambor seletor, pinhão e coroa, diferencial e semieixos com juntas tripoide. As engrenagens giram nas relações de cada par.'},
 {id:'safety',spread:[0,1.5,.4],number:'11',label:'Segurança',short:'SEGURANÇA',chapter:'17:03',color:'#ff4d67',howItWorks:'O halo e a estrutura de capotamento protegem a cabeça do piloto; o cone do nariz e a estrutura traseira absorvem energia em batidas; os tubos laterais resistem à intrusão. Dois cabos por roda impedem que ela se solte, e o extintor e as chaves externas permitem o socorro rápido.',observe:'Localize o cone de impacto dentro do nariz e a luz de chuva na estrutura traseira. Na vista explodida, veja os dois cabos de retenção de cada roda, que seguem caminhos diferentes para que um segure se o outro romper.',description:'Halo e encosto de cabeça exatamente como se veem por fora do carro, estrutura principal de capotamento no airbox, cone de impacto dentro do nariz, estrutura de impacto traseira com a luz de chuva, tubos anti-intrusão laterais, dois cabos de retenção por roda, extintor e chaves externas.'},
 {id:'cockpit',spread:[0,1.0,1.2],number:'12',label:'Cockpit e retenção',short:'COCKPIT',chapter:'17:51',color:'#d9a8ff',hero:[.9,.9,-1],howItWorks:'O piloto viaja quase deitado num assento moldado ao corpo. O arnês de seis pontos e o HANS prendem tronco e cabeça nas desacelerações, enquanto os acolchoados apoiam as pernas. Pedais, hidratação, painel de chaves e rádio ficam ao alcance sem mudar a postura.',observe:'Observe a postura reclinada e a posição do HANS entre capacete e ombros. Clique no fecho rotativo do arnês, que solta os seis cintos com um único giro.',description:'Assento moldado dentro da cavidade do cockpit, arnês de seis pontos com fecho rotativo, HANS com tirantes, acelerador no pé direito, acolchoados de perna, hidratação, painel de chaves e rádio.'},
 {id:'wheel',spread:[0,1.3,1.5],number:'13',label:'Volante e comandos',short:'VOLANTE',chapter:'19:17',color:'#8db5ff',hero:[-.3,.3,-1],howItWorks:'O volante é o painel de controle do carro: além de esterçar, concentra marchas, embreagem, mapas de motor, energia, equilíbrio de freio e rádio. O display mostra marcha e alertas e os LEDs indicam o momento da troca. Em 2026 surgem comandos de override manual e de aerodinâmica ativa.',observe:'Clique em cada botão e seletor para ler a função. Procure os botões OT e AA e as borboletas atrás das empunhaduras.',description:'Volante de 2026: corpo de carbono achatado com empunhaduras verticais, display de telemetria com quinze LEDs, botões coloridos com legendas (N, P, OT de override manual, AA de aerodinâmica ativa), balancins de freio, três seletores grandes, rolos de polegar, borboletas de marcha e de embreagem, engate rápido e cabo helicoidal. Clique em cada comando para ler o que ele faz.'},
 {id:'sensors',spread:[0,-1.0,-.7],number:'14',label:'Sensores',short:'SENSORES',chapter:'22:11',color:'#7ee5f2',howItWorks:'Centenas de sensores medem pressão, temperatura, velocidade das rodas, altura do assoalho, cargas e movimentos do carro. A ECU padrão reúne esses sinais, o gravador guarda os dados de acidentes e o transceptor envia a telemetria ao box em tempo real.',observe:'Encontre o tubo de Pitot no nariz, as câmeras infravermelhas voltadas para os pneus e os lasers sob o assoalho. Siga as fitas de dados até a antena.',description:'Tubo de Pitot, sensores de velocidade de roda com anéis dentados, câmeras infravermelhas de pneu, lasers de altura, ECU padrão, gravador de acidentes, unidade inercial, células de carga, termopares, transceptor e antena com chicote. As fitas mostram os dados indo do carro para o box.'}
]);
export const SYSTEM_IDS=Object.freeze(SYSTEM_CATALOG.map(system=>system.id));
export const SYSTEMS_ASSET='./assets/sistemas-v1.glb';
export const HIDE_GROUPS=Object.freeze({plenum_lid:'tampas dos plenums',es_lid:'tampa do energy store',gearbox_case:'carcaça do câmbio',fuel_liquid:'nível de combustível'});
export const FLOW_SPEEDS=Object.freeze({air:.55,charge:.5,exhaust:.7,water:.35,oil:.25,fuel:.3,hv:.9,hyd:.4,data:1.2,brake:.4});

const LOCAL_SPIN_AXES=Object.freeze({x:Object.freeze([1,0,0]),y:Object.freeze([0,1,0]),z:Object.freeze([0,0,1])});
export const advanceLocalSpin=(quaternion,axis='y',angle=0)=>{const values=LOCAL_SPIN_AXES[axis];if(!values)throw new Error(`Eixo de rotação local inválido: ${axis}`);return quaternion.clone().multiply(new THREE.Quaternion().setFromAxisAngle(new THREE.Vector3(...values),angle)).normalize();};

/** Textura de setas para as fitas de fluxo (o deslocamento em V anima o sentido). */
function flowTexture(){
 const c=document.createElement('canvas');c.width=32;c.height=128;const g=c.getContext('2d');
 g.clearRect(0,0,32,128);g.fillStyle='rgba(255,255,255,.18)';g.fillRect(0,0,32,128);
 g.fillStyle='rgba(255,255,255,1)';
 for(const y0 of [0,64]){g.beginPath();g.moveTo(0,y0+40);g.lineTo(16,y0+12);g.lineTo(32,y0+40);g.lineTo(32,y0+54);g.lineTo(16,y0+26);g.lineTo(0,y0+54);g.closePath();g.fill();}
 const t=new THREE.CanvasTexture(c);t.wrapS=t.wrapT=THREE.RepeatWrapping;t.colorSpace=THREE.NoColorSpace;return t;
}

export function createSystems({scene,model,mechanics,engine,driver,garage,camera,canvas,moveCamera,showCar=()=>{},onClose=showCar,mobile=false,assetUrl=SYSTEMS_ASSET}){
 const root=new THREE.Group();root.name='Sistemas internos';root.visible=false;scene.add(root);
 const groups=new Map();
 for(const system of SYSTEM_CATALOG){const group=new THREE.Group();group.name=`Sistema · ${system.label}`;group.userData.systemId=system.id;group.visible=false;root.add(group);groups.set(system.id,group);}
 const materials=[],textures=[],parts=[],spinners=[],flows=[],eraNodes=[],coverNodes=[],pulseMaterials=[],carriers=[],translucent=new Map();
 let enabled=false,active='overview',currentView='hero',ghostEntries=[],ghostOn=false,previous={},disposed=false,paused=false;
 let state='idle',loadPromise=null,gltfScene=null,flowsOn=false,coversOpen=false,schematic=false,ghostWanted=true,explodeAmount=0,revealSpread=0,revealEnabled=true,revealing=false,picked=null;
 const reducedMotion=typeof window!=='undefined'&&typeof window.matchMedia==='function'?window.matchMedia('(prefers-reduced-motion: reduce)'):{matches:false};
 const onVisibilityChange=()=>{paused=document.hidden;};
 if(typeof document!=='undefined')document.addEventListener('visibilitychange',onVisibilityChange,{passive:true});
 const meta=id=>SYSTEM_CATALOG.find(system=>system.id===id)||SYSTEM_CATALOG[0];
 const colors=Object.fromEntries(SYSTEM_CATALOG.map(system=>[system.id,new THREE.Color(system.color)]));
 const schematicMaterials=Object.fromEntries(SYSTEM_CATALOG.map(system=>{const m=new THREE.MeshStandardMaterial({name:`Esquema · ${system.label}`,color:colors[system.id],metalness:.25,roughness:.45,emissive:colors[system.id],emissiveIntensity:.18});materials.push(m);return [system.id,m];}));
 const flowMap=flowTexture();textures.push(flowMap);
 const flowMaterials={};
 const flowMaterial=kind=>{if(!flowMaterials[kind]){const base=new THREE.Color({air:'#bfe6ff',charge:'#ffd7a6',exhaust:'#ff8a4d',water:'#63b8ff',oil:'#ffb347',fuel:'#ffd24d',hv:'#ff9a3c',hyd:'#c78bff',data:'#6ff7e6',brake:'#ff6b6b'}[kind]||'#ffffff');const map=flowMap.clone();map.needsUpdate=true;textures.push(map);const m=new THREE.MeshBasicMaterial({name:`Fluxo animado · ${kind}`,color:base,map,alphaMap:map,transparent:true,opacity:.95,depthWrite:false,side:THREE.DoubleSide,toneMapped:false});materials.push(m);flowMaterials[kind]={material:m,map,speed:FLOW_SPEEDS[kind]??.5};}return flowMaterials[kind];};

 const ui={reading:document.getElementById('system-reading'),how:document.getElementById('system-how-it-works'),observe:document.getElementById('system-observe'),list:document.getElementById('system-list'),detail:document.getElementById('system-detail'),title:document.getElementById('system-title'),kicker:document.getElementById('system-kicker'),description:document.getElementById('system-description'),chapter:document.getElementById('system-chapter'),count:document.getElementById('system-part-count'),overview:document.getElementById('system-overview'),back:document.getElementById('system-close'),hint:document.querySelector('.hint'),context:document.getElementById('system-context'),chapters:[...document.querySelectorAll('.system-chapters a')],views:[...document.querySelectorAll('[data-view]')],
  flows:document.getElementById('system-flows'),covers:document.getElementById('system-covers'),schematic:document.getElementById('system-schematic'),ghost:document.getElementById('system-ghost'),explode:document.getElementById('system-explode'),explodeValue:document.getElementById('system-explode-value'),part:document.getElementById('system-part'),status:document.getElementById('system-status')};
 let ersContext='legacy2021',contextToggle=null;
 if(ui.detail&&!document.getElementById('ers-context-toggle')){contextToggle=document.createElement('button');contextToggle.id='ers-context-toggle';contextToggle.type='button';contextToggle.className='wide';contextToggle.setAttribute('aria-pressed','false');ui.detail.append(contextToggle);}
 const originalHint=ui.hint?.textContent||'';
 const systemsHint='SISTEMAS: CLIQUE EM UM CARTÃO PARA ISOLAR · CLIQUE EM UMA PEÇA PARA LER O QUE ELA FAZ';
 if(ui.detail&&ui.list&&ui.detail.parentElement===ui.list.parentElement)ui.detail.parentElement.insertBefore(ui.detail,ui.list);
 const cardFor=id=>ui.list?.querySelector(`[data-system="${id}"]`);
 const logicalPartCount=id=>new Set(parts.filter(entry=>!id||entry.system===id).map(entry=>entry.logicalOwner)).size;
 const syncView=name=>ui.views.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.view===name)));
 const setStatus=text=>{if(ui.status){ui.status.textContent=text;ui.status.hidden=!text;}};

 // ------------------------------------------------------------------ carregamento do asset
 function attachPart(mesh,systemId,logicalOwner=mesh.uuid){
  const data=mesh.userData||{};
  const entry={object:mesh,logicalOwner,system:systemId,part:data.part||mesh.name,base:mesh.position.clone(),explode:Array.isArray(data.explode)?new THREE.Vector3(...data.explode):new THREE.Vector3(),original:mesh.material,era:data.era||null,hideGroup:data.hide_group||null,flow:data.flow||null};
  parts.push(entry);mesh.userData.systemPart=entry;
  mesh.castShadow=!entry.flow&&!mesh.material?.transparent;mesh.receiveShadow=true;mesh.renderOrder=10;
  if(typeof data.spin==='number'&&data.spin!==0)spinners.push({object:mesh,rate:data.spin,axis:LOCAL_SPIN_AXES[data.spin_axis]?data.spin_axis:'y'});
  if(entry.flow){const f=flowMaterial(entry.flow);mesh.material=f.material;mesh.renderOrder=14;entry.original=f.material;flows.push({object:mesh,kind:entry.flow,reverse:data.tag==='reverse'});}
  if(entry.era)eraNodes.push(entry);
  if(entry.hideGroup)coverNodes.push(entry);
  if(data.carrier)carriers.push(entry);
  return entry;
 }
 function prepareMaterials(sceneRoot){
  const seen=new Set();
  sceneRoot.traverse(node=>{if(!node.isMesh)return;for(const m of [].concat(node.material)){if(seen.has(m))continue;seen.add(m);materials.push(m);for(const key of Object.keys(m)){const v=m[key];if(v?.isTexture)textures.push(v);}
   if('envMapIntensity' in m)m.envMapIntensity=1.15;
   if(m.transparent){m.depthWrite=false;}
   // A bancada mostra o material frio. Aquecimento exige frenagem, não um pulso decorativo.
   if(/^Disco carbono-carbono/.test(m.name)){m.emissive=new THREE.Color('#000000');m.emissiveIntensity=0;}
   if(/^LED /.test(m.name))pulseMaterials.push({material:m,kind:'led',base:m.emissiveIntensity});
  }});
 }
 function distribute(gltf){
  gltfScene=gltf.scene;
  const ownerId=mesh=>{for(let node=mesh;node;node=node.parent){const index=gltf.parser.associations.get(node)?.nodes;if(Number.isInteger(index))return index;}return mesh.uuid;};
  const stray=[];
  for(const child of [...gltfScene.children]){
   const id=/^system_(\w+)$/.exec(child.name)?.[1];
   const group=id?groups.get(id):null;
   if(!group){stray.push(child.name);continue;}
   for(const node of [...child.children])group.add(node);
  }
  for(const [id,group] of groups)group.traverse(node=>{if(node.isMesh&&!node.userData.systemPart)attachPart(node,id,ownerId(node));});
  if(stray.length)console.warn('Sistemas: nós fora do contrato ignorados',stray);
  prepareMaterials(root);
  applyEra();applyCovers();applyExplode();applyFlows();
  root.updateMatrixWorld(true);
  window.viewerInfo&&(window.viewerInfo.systemsParts=logicalPartCount(),window.viewerInfo.systemsMeshes=parts.length,window.viewerInfo.systemsLoaded=true);
 }
 function load(){
  if(loadPromise)return loadPromise;
  state='loading';setStatus('Carregando os sistemas em 3D…');
  loadPromise=(async()=>{
   const bakedAO=fetchBakedOcclusion(assetUrl);
   const response=await fetch(assetUrl);if(!response.ok)throw new Error('Sistemas HTTP '+response.status);
   const bytes=await response.arrayBuffer();await MeshoptDecoder.ready;
   const gltf=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(bytes,assetUrl.replace(/[^/]+$/,''));
   if(disposed)return;
   // Oclusão assada no Cycles, na ordem de malhas do GLB: antes de distribuir as peças pelos grupos.
   tryAttachBakedOcclusion(gltf.scene,await bakedAO);patchBakedOcclusion(gltf.scene);
   distribute(gltf);state='ready';setStatus('');
   if(enabled){show(active,false);}
  })().catch(error=>{console.error(error);state='failed';setStatus('Não foi possível carregar os sistemas. Recarregue a página para tentar novamente.');});
  return loadPromise;
 }

 // ------------------------------------------------------------------ estados visuais
 function applyEra(){for(const entry of eraNodes)entry.object.visible=entry.era!=='2021'||ersContext==='legacy2021';}
 function applyCovers(){for(const entry of coverNodes)entry.object.visible=!coversOpen&&(entry.era!=='2021'||ersContext==='legacy2021');}
 // Vista explodida: com um sistema isolado, só as peças se afastam; na visão geral (e na revelação pela bancada Carro)
 // cada sistema também se desloca na direção `spread` do catálogo, para os catorze conjuntos serem lidos separados.
 function applyExplode(){
  const spreadMode=enabled?active==='overview':true;
  const amount=enabled?explodeAmount:revealSpread;
  groups.forEach((group,id)=>{const v=(spreadMode&&meta(id).spread)||[0,0,0];group.position.set(v[0]*amount*1.2,v[1]*amount*1.2,v[2]*amount*1.2);});
  const factor=spreadMode?amount*.9:amount*1.6;
  for(const entry of parts){if(entry.explode.lengthSq()===0)continue;entry.object.position.copy(entry.base).addScaledVector(entry.explode,factor);}
 }
 // Tubos, mangueiras, cabos e eixos que conduzem um fluxo ficam translúcidos enquanto os fluxos estão ligados.
 const translucentOf=material=>{if(!translucent.has(material)){const clone=material.clone();clone.transparent=true;clone.opacity=.28;clone.depthWrite=false;clone.name=material.name+' · translúcido';materials.push(clone);translucent.set(material,clone);}return translucent.get(material);};
 function materialFor(entry){if(entry.flow)return entry.original;const base=schematic?schematicMaterials[entry.system]:entry.original;return flowsOn&&active===entry.system&&carriers.includes(entry)?translucentOf(base):base;}
 function applyFlows(){const showFlows=flowsOn&&active!=='overview';for(const flow of flows)flow.object.visible=showFlows&&(flow.object.userData.systemPart.era!=='2021'||ersContext==='legacy2021');for(const entry of carriers)if(entry!==highlighted)entry.object.material=materialFor(entry);}
 function applySchematic(){for(const entry of parts){if(entry.flow||entry===highlighted)continue;entry.object.material=materialFor(entry);}if(picked)highlight(picked,true);}
 let highlighted=null,highlightMaterial=null;
 function highlight(entry,on){
  if(highlighted&&highlighted!==entry){const prev=highlighted;highlighted=null;prev.object.material=materialFor(prev);}
  if(!entry)return;
  if(on){if(!highlightMaterial){highlightMaterial=new THREE.MeshStandardMaterial({name:'Peça selecionada',color:'#ffffff',emissive:'#d92135',emissiveIntensity:.55,metalness:.3,roughness:.4});materials.push(highlightMaterial);}
   highlightMaterial.color.copy(entry.original?.color||new THREE.Color('#ffffff'));entry.object.material=highlightMaterial;highlighted=entry;}
  else{if(highlighted===entry)highlighted=null;entry.object.material=materialFor(entry);}
 }
 function setPicked(entry){
  picked=entry;highlight(entry,Boolean(entry));
  if(!ui.part)return;
  ui.part.hidden=!entry;
  if(!entry){ui.part.replaceChildren();return;}
  const info=describePart(entry.part,entry.system);
  const name=document.createElement('strong');name.textContent=entry.part;
  const system=document.createElement('span');system.className='system-part-system';system.textContent=meta(entry.system).label;
  const funcao=document.createElement('p');funcao.textContent=info.funcao;
  ui.part.replaceChildren(name,system,funcao);
  if(info.curiosidade){const fact=document.createElement('p');fact.className='system-part-fact';const tag=document.createElement('em');tag.textContent='Curiosidade · ';fact.append(tag,info.curiosidade);ui.part.append(fact);}
  ui.part.dataset.generic=String(info.generico);
 }

 function setERSContext(mode){ersContext=mode==='current2026'?'current2026':'legacy2021';applyEra();applyCovers();applyFlows();if(active==='ers'||active==='power'){updateUI(active);frame(active,dirFor(active,currentView),false);}}
 function updateUI(id=active){
  if(disposed)return;
  const overview=id==='overview',system=overview?null:meta(id),rovingId=overview?SYSTEM_CATALOG[0]?.id:id;syncView(currentView);if(ui.title)ui.title.textContent=overview?'Visão geral dos sistemas':system.label;if(ui.kicker)ui.kicker.textContent=overview?'OS CATORZE SISTEMAS':`${system.number} / ${system.short}`;if(ui.description)ui.description.textContent=overview?'Catorze sistemas em escala real dentro do carro. Escolha um para estudá-lo isolado, com fluxos, tampas abertas e vista explodida; clique em qualquer peça para ler o que ela faz.':`${system.description}${id==='ers'||id==='power'?` Versão em exibição: ${ersContext==='legacy2021'?'2021, com MGU-H':'2026, sem MGU-H'}.`:''}`;if(ui.reading)ui.reading.hidden=overview;if(ui.how)ui.how.textContent=system?.howItWorks||'';if(ui.observe)ui.observe.textContent=system?.observe||'';if(ui.chapter)ui.chapter.textContent=overview?'Visão geral':`Sistema ${system.number} de 14`;const count=logicalPartCount(overview?null:id);if(ui.count)ui.count.textContent=overview?(count?`${count} PEÇAS · 14 CAMADAS`:'14 CAMADAS'):`${system.number} / 14${count?` · ${count} PEÇAS`:''}`;if(contextToggle){contextToggle.hidden=id!=='ers'&&id!=='power';contextToggle.textContent=ersContext==='legacy2021'?'Ver versão 2026 (sem MGU-H)':'Ver versão 2021 (com MGU-H)';contextToggle.setAttribute('aria-pressed',String(ersContext==='current2026'));}if(ui.overview){ui.overview.setAttribute('aria-pressed',String(overview));ui.overview.textContent=overview?'Todos os sistemas visíveis':'Mostrar todos os sistemas';ui.overview.style.color=overview?'#fff':'';ui.overview.style.backgroundColor=overview?'var(--red)':'';}if(ui.hint)ui.hint.style.textShadow=enabled?'0 1px 3px var(--paper),0 0 8px var(--paper)':'';SYSTEM_CATALOG.forEach((item,index)=>{const card=cardFor(item.id);if(card){const selected=!overview&&item.id===id;card.setAttribute('aria-pressed',String(selected));card.tabIndex=item.id===rovingId?0:-1;const chapterLink=ui.chapters[index];if(chapterLink){if(selected)chapterLink.setAttribute('aria-current','true');else chapterLink.removeAttribute('aria-current');}}});if(overview)ui.chapters.forEach(link=>link.removeAttribute('aria-current'));if(ui.detail)ui.detail.style.setProperty('--system-color',overview?'#d92135':system.color);
  ui.flows?.setAttribute('aria-pressed',String(flowsOn));ui.covers?.setAttribute('aria-pressed',String(coversOpen));ui.schematic?.setAttribute('aria-pressed',String(schematic));ui.ghost?.setAttribute('aria-pressed',String(ghostWanted));if(ui.flows)ui.flows.disabled=overview;if(ui.explode){ui.explode.value=Math.round(explodeAmount*100);ui.explode.disabled=false;}if(ui.explodeValue)ui.explodeValue.textContent=Math.round(explodeAmount*100)+'%';
 }
 function objectFor(id){return id==='overview'?root:groups.get(id);}
 function geometryBounds(object){const bounds=new THREE.Box3().makeEmpty();object.traverse(node=>{if(!node.visible||node.userData.systemTag||(!node.isMesh&&!node.isLine&&!node.isPoints))return;const entry=node.userData.systemPart;if(entry?.flow)return;bounds.expandByObject(node);});return bounds;}
 function viewportAspect(){const width=canvas?.clientWidth||canvas?.width,height=canvas?.clientHeight||canvas?.height;return width>0&&height>0?width/height:Math.max(camera?.aspect??1,.5);}
 const directions={hero:[1,.35,1.18],side:[1,.12,0],front:[0,.16,1],rear:[0,.18,-1],top:[.001,1,0],bottom:[.001,-1,0]};
 // Vista principal por sistema: o volante e o cockpit são vistos do lugar do piloto (de trás, −Z), não da frente do carro.
 const dirFor=(id,name)=>(name==='hero'&&meta(id)?.hero)||directions[name]||directions.hero;
 function frame(id,direction=dirFor(id,currentView),animate=true){if(disposed||typeof moveCamera!=='function')return;const object=objectFor(id);if(!object)return;object.updateMatrixWorld(true);const bounds=geometryBounds(object);if(bounds.isEmpty()){if(state!=='ready'){const target=new THREE.Vector3(0,.45,0);moveCamera(target.clone().addScaledVector(new THREE.Vector3(...direction).normalize(),mobile?6.8:6.4),target,animate);}return;}const target=bounds.getCenter(new THREE.Vector3());if(id==='overview')target.y=.45;const dir=new THREE.Vector3(...direction).normalize(),worldUp=new THREE.Vector3(0,1,0),right=new THREE.Vector3().crossVectors(worldUp,dir);if(right.lengthSq()<1e-6)right.set(1,0,0);else right.normalize();const up=new THREE.Vector3().crossVectors(dir,right).normalize(),halfVertical=Math.tan(THREE.MathUtils.degToRad(camera?.fov??45)/2),halfHorizontal=halfVertical*Math.max(viewportAspect(),.1);let required=0;for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const offset=new THREE.Vector3(x,y,z).sub(target),depth=offset.dot(dir);required=Math.max(required,depth+Math.abs(offset.dot(right))/halfHorizontal,depth+Math.abs(offset.dot(up))/halfVertical);}const size=bounds.getSize(new THREE.Vector3()),minimum=id==='overview'?(mobile?6.8:6.4):(mobile?1.6:1.2),distance=THREE.MathUtils.clamp(Math.max(required*1.18,size.length()*1.08,minimum),minimum,30);moveCamera(target.clone().addScaledVector(dir,distance),target,animate);}
 function show(id='overview',animate=true){if(disposed)return;if(!groups.has(id)&&id!=='overview')id='overview';setEnabled(true);const previousActive=active;active=id;setPicked(null);if(id!==previousActive&&explodeAmount){explodeAmount=0;applyExplode();}groups.forEach((group,key)=>{group.visible=id==='overview'||key===id;});applyFlows();if(previousActive!==id)for(const entry of carriers)if(entry.system===previousActive)entry.object.material=materialFor(entry);updateUI(id);frame(id,dirFor(active,currentView),animate);}
 function view(name){if(disposed||!enabled)return;currentView=directions[name]?name:'hero';syncView(currentView);frame(active,dirFor(active,currentView),false);}
 function captureGhost(){if(disposed||ghostEntries.length||!model?.traverse)return;model.traverse(object=>{if(!object.isMesh)return;const original=object.material;const cloneMaterial=material=>{if(!material?.clone)return material;const clone=material.clone();if('color' in clone)clone.color.set('#8b9aa4');if('map' in clone)clone.map=null;if('emissive' in clone){clone.emissive.set('#22303a');clone.emissiveIntensity=.16;}clone.transparent=true;clone.opacity=.105;clone.depthWrite=false;clone.depthTest=true;return clone;};ghostEntries.push({object,original,castShadow:object.castShadow,ghost:Array.isArray(original)?original.map(cloneMaterial):cloneMaterial(original)});});}
 function setGhost(on){if(disposed)return;captureGhost();if(on&&!ghostOn){ghostEntries.forEach(entry=>{entry.object.material=entry.ghost;entry.object.castShadow=false;});ghostOn=true;}else if(!on&&ghostOn){ghostEntries.forEach(entry=>{entry.object.material=entry.original;entry.object.castShadow=entry.castShadow;});ghostOn=false;}}
 function setEnabled(on){if(disposed||on===enabled)return;enabled=on;applyExplode();root.visible=on;document.body.classList.toggle('systems-active',on);if(ui.hint)ui.hint.textContent=on?systemsHint:originalHint;if(on){load();previous={model:model?.visible,driver:driver?.root.visible,engine:engine?.root.visible};if(garage?.enabled)garage.setEnabled(false);if(model)model.visible=true;if(driver?.root)driver.root.visible=false;if(engine?.root)engine.root.visible=false;setGhost(ghostWanted);}else{setGhost(false);setPicked(null);if(model)model.visible=previous.model??true;if(driver?.root)driver.root.visible=previous.driver??true;if(engine?.root)engine.root.visible=previous.engine??false;root.visible=false;}}

 // ------------------------------------------------------------------ interação
 const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();let down=null;
 const onPointerDown=event=>{down=[event.clientX,event.clientY];};
 function pickFromEvent(event){if(state!=='ready'||!(enabled||revealing))return null;const rect=canvas.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);ray.setFromCamera(pointer,camera);const visible=[];root.traverse(node=>{if(node.isMesh&&node.visible&&node.userData.systemPart&&!node.userData.systemPart.flow)visible.push(node);});const hit=ray.intersectObjects(visible,false).find(h=>{let o=h.object;while(o&&o!==root){if(!o.visible)return false;o=o.parent;}return true;});const entry=hit?hit.object.userData.systemPart:null;setPicked(entry&&entry.object.visible?entry:null);return picked?{part:picked.part,system:meta(picked.system).label,systemId:picked.system,...describePart(picked.part,picked.system)}:null;}
 const onPointerUp=event=>{if(!enabled||state!=='ready'||!down||Math.hypot(event.clientX-down[0],event.clientY-down[1])>5)return;const rect=canvas.getBoundingClientRect();pointer.set((event.clientX-rect.left)/rect.width*2-1,-(event.clientY-rect.top)/rect.height*2+1);ray.setFromCamera(pointer,camera);const visible=[];root.traverse(node=>{if(node.isMesh&&node.visible&&!node.userData.systemPart?.flow)visible.push(node);});const hits=ray.intersectObjects(visible,false).filter(hit=>{let o=hit.object;while(o&&o!==root){if(!o.visible)return false;o=o.parent;}return true;});setPicked(hits.length?hits[0].object.userData.systemPart:null);};
 canvas?.addEventListener('pointerdown',onPointerDown);canvas?.addEventListener('pointerup',onPointerUp);
 const onSystemClick=event=>show(event.currentTarget.dataset.system);
 const onSystemKey=event=>{const cards=[...ui.list?.querySelectorAll('[data-system]')||[]],index=cards.indexOf(event.currentTarget);if(!cards.length)return;let next=index;if(event.key==='ArrowDown'||event.key==='ArrowRight')next=(index+1)%cards.length;else if(event.key==='ArrowUp'||event.key==='ArrowLeft')next=(index-1+cards.length)%cards.length;else if(event.key==='Home')next=0;else if(event.key==='End')next=cards.length-1;else if(event.key==='Enter'||event.key===' '){event.preventDefault();show(event.currentTarget.dataset.system);return;}else return;event.preventDefault();cards[next].focus();show(cards[next].dataset.system);};
 const onOverviewClick=()=>show('overview');
 const onBackClick=()=>{setEnabled(false);active='overview';updateUI();onClose();};
 const onContextToggle=()=>setERSContext(ersContext==='legacy2021'?'current2026':'legacy2021');
 const onFlows=()=>{flowsOn=!flowsOn;applyFlows();updateUI();};
 const onCovers=()=>{coversOpen=!coversOpen;applyCovers();updateUI();};
 const onSchematic=()=>{schematic=!schematic;applySchematic();updateUI();};
 const onGhost=()=>{ghostWanted=!ghostWanted;if(enabled)setGhost(ghostWanted);updateUI();};
 const onExplode=()=>{explodeAmount=Number(ui.explode.value)/100;applyExplode();if(ui.explodeValue)ui.explodeValue.textContent=Math.round(explodeAmount*100)+'%';};
 if(ui.list)SYSTEM_CATALOG.forEach((system,index)=>{const card=cardFor(system.id);if(!card)return;card.tabIndex=index===0?0:-1;card.addEventListener('click',onSystemClick);card.addEventListener('keydown',onSystemKey);});
 ui.overview?.addEventListener('click',onOverviewClick);
 ui.back?.addEventListener('click',onBackClick);
 contextToggle?.addEventListener('click',onContextToggle);
 ui.flows?.addEventListener('click',onFlows);ui.covers?.addEventListener('click',onCovers);ui.schematic?.addEventListener('click',onSchematic);ui.ghost?.addEventListener('click',onGhost);ui.explode?.addEventListener('input',onExplode);
 setERSContext('legacy2021');
 updateUI('overview');
 let time=0;
 return {root,groups,show,view,activate:show,deactivate:()=>setEnabled(false),setPaused(value){paused=Boolean(value);},setERSContext,load,reset:()=>{explodeAmount=0;revealSpread=0;applyExplode();show('overview',false);},pickFromEvent,clearPick(){setPicked(null);},describe:describePart,systemLabel(id){return meta(id).label;},setSpread(value){revealSpread=Math.min(Math.max(Number(value)||0,0),1);if(!enabled)applyExplode();},get spread(){return revealSpread;},
  setRevealInExplode(value){revealEnabled=Boolean(value);},
  get active(){return enabled?active:null;},get enabled(){return enabled;},get state(){return state;},get ready(){return state==='ready';},get revealing(){return revealing;},get context(){return ersContext;},get parts(){return parts;},get paused(){return paused||reducedMotion.matches;},
  update(dt,now=performance.now()/1000){
   if(disposed)return;
   // Revelação dos sistemas ao desmontar o carro na bancada Carro: a carroceria se afasta e os conjuntos ficam no lugar.
   const wantReveal=!enabled&&revealEnabled&&Boolean(mechanics)&&mechanics.amount>.02&&!mechanics.isolated;
   if(wantReveal&&state==='idle')load();
   const canReveal=wantReveal&&state==='ready';
   if(canReveal!==revealing){revealing=canReveal;if(revealing){groups.forEach(group=>{group.visible=true;});for(const flow of flows)flow.object.visible=false;}else if(!enabled){for(const flow of flows)flow.object.visible=false;}applyExplode();}
   root.visible=enabled||revealing;
   if(window.viewerInfo){window.viewerInfo.systemsRevealing=revealing;window.viewerInfo.systemsFlowsVisible=flows.reduce((n,f)=>n+(f.object.visible?1:0),0);window.viewerInfo.systemsActiveId=enabled?active:null;window.viewerInfo.systemsSpread=revealSpread;}
   if(!root.visible||paused||reducedMotion.matches||document.hidden)return;
   const step=Math.min(Math.max(dt,0),.05);time+=step;
   for(const s of spinners)s.object.quaternion.copy(advanceLocalSpin(s.object.quaternion,s.axis,step*s.rate));
   for(const kind of Object.keys(flowMaterials)){const f=flowMaterials[kind];f.map.offset.y=(f.map.offset.y-step*f.speed)%1;}
   for(const p of pulseMaterials){if(p.kind==='led')p.material.emissiveIntensity=p.base*(.6+.4*(.5+.5*Math.sin(time*4+p.material.id)));}
  },
  dispose(){if(disposed)return;setEnabled(false);document.removeEventListener('visibilitychange',onVisibilityChange);canvas?.removeEventListener('pointerdown',onPointerDown);canvas?.removeEventListener('pointerup',onPointerUp);ui.overview?.removeEventListener('click',onOverviewClick);ui.back?.removeEventListener('click',onBackClick);contextToggle?.removeEventListener('click',onContextToggle);ui.flows?.removeEventListener('click',onFlows);ui.covers?.removeEventListener('click',onCovers);ui.schematic?.removeEventListener('click',onSchematic);ui.ghost?.removeEventListener('click',onGhost);ui.explode?.removeEventListener('input',onExplode);SYSTEM_CATALOG.forEach(system=>{const card=cardFor(system.id);card?.removeEventListener('click',onSystemClick);card?.removeEventListener('keydown',onSystemKey);});ghostEntries.forEach(entry=>{for(const material of [].concat(entry.ghost)){if(material&&material!==entry.original&&material.dispose)material.dispose();}});const geometries=new Set();root.traverse(node=>{if(node.isMesh)geometries.add(node.geometry);});geometries.forEach(geometry=>geometry.dispose());materials.forEach(material=>material.dispose());textures.forEach(texture=>texture.dispose());root.removeFromParent();disposed=true;}};
}
