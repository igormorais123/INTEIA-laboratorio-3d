import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {MeshoptDecoder} from 'three/addons/libs/meshopt_decoder.module.js';

// Catálogo dos 14 sistemas na ordem dos capítulos do vídeo de referência (Animagraffs, 2021).
// A geometria vem de web/assets/sistemas-v1.glb, gerada por ferramentas/gerar_sistemas.py (Blender 5.2):
// malhas originais INTEIA em escala do carro v2, com materiais físicos e peças nomeadas.
// É uma camada didática de estudo, não CAD de fabricante nem homologação.
export const SYSTEM_CATALOG=Object.freeze([
 {id:'aero',number:'01',label:'Aerodinâmica',short:'AERO',chapter:'0:14',color:'#52c8df',description:'O que a carroceria esconde: túneis venturi do assoalho, cercas de borda, palhetas do difusor, asa de viga, atuador hidráulico do DRS, defletores laterais e ajustadores do flap. As fitas de fluxo são trajetórias ilustrativas; não é CFD nem mistura DRS histórico com active aero 2026.'},
 {id:'structure',number:'02',label:'Estrutura central / survival cell didática',short:'ESTRUTURA',chapter:'4:47',color:'#c5a7ff',description:'Célula de sobrevivência em sanduíche de carbono e colmeia, com janela de corte no núcleo, anteparas, prisioneiros do motor, insertos de titânio das ancoragens e plank com pastilhas. Motor e câmbio são membros estruturais aparafusados atrás dela; nada aqui é homologação.'},
 {id:'suspension',number:'03',label:'Suspensão',short:'SUSPENSÃO',chapter:'5:19',color:'#f1bd68',description:'Wishbones em perfil de asa, uprights usinados, push-rod dianteiro e pull-rod traseiro acionando balancins, barras de torção, amortecedores inboard, elemento heave com pilha Belleville e barras antirrolagem. Os pontos de ancoragem são compartilhados com direção, freios e cabos de retenção; não é cinemática real.'},
 {id:'steering',number:'04',label:'Direção',short:'DIREÇÃO',chapter:'7:52',color:'#ff8c6b',description:'Coluna em carbono com duas juntas universais, pinhão e cremalheira na antepara dianteira, barras de direção em perfil de asa até os braços dos uprights, servo hidráulico e linhas de assistência. Sem torque real nem simulação hidráulica.'},
 {id:'brakes',number:'05',label:'Freios',short:'FREIOS',chapter:'8:57',color:'#ff665d',description:'Discos carbono-carbono ventilados, campânulas, pinças monobloco de seis pistões montadas baixas, tambores e dutos de refrigeração, pedal usinado, dois cilindros mestres com barra de balanço, brake-by-wire traseiro e linhas rígidas e trançadas. Pressão e calor são apenas ilustrativos.'},
 {id:'power',number:'06',label:'Unidade de potência',short:'V6 TURBO',chapter:'11:32',color:'#ff9f58',description:'V6 de 90° com cárter seco, cabeçotes e tampas de comando, turbo dividido (compressor à frente, turbina atrás, eixo comum pelo vale) com MGU-H legado 2021 coaxial, dois plenums com seis trompetas, snorkel do airbox, dutos do intercooler, coletores 3-em-1 em Inconel, wastegates e escapamento. Em 2026 o MGU-H é removido; a contagem e o material dos plenums/trompetas são hipótese: não são verificáveis neste frame.'},
 {id:'ers',number:'07',label:'ERS híbrido',short:'ERS',chapter:'14:14',color:'#ffe36b',description:'No modo padrão do vídeo, a arquitetura 2021 combina energy store sob o tanque, control electronics/inverter, MGU-K engrenado ao virabrequim e MGU-H legado para recuperação e entrega de energia por cabos laranja de alta tensão; o modo 2026 remove o MGU-H.'},
 {id:'cooling',number:'08',label:'Refrigeração',short:'COOLING',chapter:'14:54',color:'#66e0b2',description:'Configuração assimétrica hipotética: intercooler ar-ar inclinado e arrefecedor do câmbio no sidepod esquerdo; radiador de água, arrefecedor de óleo e arrefecedor de baixa temperatura do ERS no direito, com tanques, mangueiras e abraçadeiras. Circuitos separados de água, óleo, ERS e hidráulica; não é simulação térmica, de pressão ou vazão.'},
 {id:'fuel',number:'09',label:'Célula de combustível',short:'COMBUSTÍVEL',chapter:'15:39',color:'#e6c06d',description:'Uma única célula flexível/bladder em Kevlar e nitrílica fica atrás do piloto, em contenção estrutural didática e à frente do motor, com anteparas e portinholas, copo coletor, bombas de elevação, medidor de vazão FIA, acoplamento de abastecimento, válvula autosselante e linhas seguras fora do cockpit; não é geometria homologada.'},
 {id:'transmission',number:'10',label:'Câmbio e diferencial',short:'TRANSMISSÃO',chapter:'16:42',color:'#b7c2cc',description:'Carcaça estrutural com janela de corte, embreagem multidisco, oito pares em tomada constante mais ré com anéis de engate e tambor seletor, pinhão e coroa, diferencial autoblocante e semieixos com juntas tripóide e homocinética. As engrenagens giram nas relações de cada par; são representativas, não relações reais.'},
 {id:'safety',number:'11',label:'Segurança',short:'SAFETY',chapter:'17:03',color:'#ff4d67',description:'Halo em titânio com pilar central, estrutura principal de capotamento no airbox, cone de impacto dianteiro, estrutura de impacto traseira, tubos anti-intrusão laterais, três cabos de retenção por roda, encosto de cabeça removível, extintor e chaves externas formam uma camada de proteção, não homologada.'},
 {id:'cockpit',number:'12',label:'Cockpit e retenção',short:'COCKPIT',chapter:'17:51',color:'#d9a8ff',description:'Assento moldado, arnês de seis pontos com fecho rotativo, HANS com tirantes, acelerador e batente, acolchoados de perna, hidratação, painel de chaves e rádio formam uma leitura do espaço do piloto; não representa homologação nem ergonomia validada.'},
 {id:'wheel',number:'13',label:'Volante e comandos',short:'VOLANTE',chapter:'19:17',color:'#8db5ff',description:'Corpo de carbono com empunhaduras, display, quinze LEDs de troca, botões, seletores rotativos, borboletas de marcha e de embreagem, engate rápido, placa eletrônica e conector. Separe as camadas com o controle de peças; não simula uma ECU real.'},
 {id:'sensors',number:'14',label:'Sensores',short:'SENSORES',chapter:'22:11',color:'#7ee5f2',description:'Tubo de Pitot, sensores de velocidade de roda com anéis dentados, câmeras infravermelhas de pneu, lasers de altura, ECU padrão, gravador de acidentes, IMU, células de carga, termopares, transceptor e antena com chicote e fluxos de dados carro → box; esquema didático, não telemetria real.'}
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
 const root=new THREE.Group();root.name='Sistemas internos · camada didática';root.visible=false;scene.add(root);
 const groups=new Map();
 for(const system of SYSTEM_CATALOG){const group=new THREE.Group();group.name=`Sistema · ${system.label}`;group.userData.systemId=system.id;group.visible=false;root.add(group);groups.set(system.id,group);}
 const materials=[],textures=[],parts=[],spinners=[],flows=[],eraNodes=[],coverNodes=[],pulseMaterials=[],carriers=[],translucent=new Map();
 let enabled=false,active='overview',currentView='hero',ghostEntries=[],ghostOn=false,previous={},disposed=false,paused=false;
 let state='idle',loadPromise=null,gltfScene=null,flowsOn=true,coversOpen=false,schematic=false,ghostWanted=true,explodeAmount=0,revealEnabled=true,revealing=false,picked=null;
 const reducedMotion=typeof window!=='undefined'&&typeof window.matchMedia==='function'?window.matchMedia('(prefers-reduced-motion: reduce)'):{matches:false};
 const onVisibilityChange=()=>{paused=document.hidden;};
 if(typeof document!=='undefined')document.addEventListener('visibilitychange',onVisibilityChange,{passive:true});
 const meta=id=>SYSTEM_CATALOG.find(system=>system.id===id)||SYSTEM_CATALOG[0];
 const colors=Object.fromEntries(SYSTEM_CATALOG.map(system=>[system.id,new THREE.Color(system.color)]));
 const schematicMaterials=Object.fromEntries(SYSTEM_CATALOG.map(system=>{const m=new THREE.MeshStandardMaterial({name:`Esquema · ${system.label}`,color:colors[system.id],metalness:.25,roughness:.45,emissive:colors[system.id],emissiveIntensity:.18});materials.push(m);return [system.id,m];}));
 const flowMap=flowTexture();textures.push(flowMap);
 const flowMaterials={};
 const flowMaterial=kind=>{if(!flowMaterials[kind]){const base=new THREE.Color({air:'#bfe6ff',charge:'#ffd7a6',exhaust:'#ff8a4d',water:'#63b8ff',oil:'#ffb347',fuel:'#ffd24d',hv:'#ff9a3c',hyd:'#c78bff',data:'#6ff7e6',brake:'#ff6b6b'}[kind]||'#ffffff');const map=flowMap.clone();map.needsUpdate=true;textures.push(map);const m=new THREE.MeshBasicMaterial({name:`Fluxo animado · ${kind}`,color:base,map,alphaMap:map,transparent:true,opacity:.95,depthWrite:false,side:THREE.DoubleSide,toneMapped:false});materials.push(m);flowMaterials[kind]={material:m,map,speed:FLOW_SPEEDS[kind]??.5};}return flowMaterials[kind];};

 const ui={list:document.getElementById('system-list'),detail:document.getElementById('system-detail'),title:document.getElementById('system-title'),kicker:document.getElementById('system-kicker'),description:document.getElementById('system-description'),chapter:document.getElementById('system-chapter'),count:document.getElementById('system-part-count'),overview:document.getElementById('system-overview'),back:document.getElementById('system-close'),hint:document.querySelector('.hint'),context:document.getElementById('system-context'),chapters:[...document.querySelectorAll('.system-chapters a')],views:[...document.querySelectorAll('[data-view]')],
  flows:document.getElementById('system-flows'),covers:document.getElementById('system-covers'),schematic:document.getElementById('system-schematic'),ghost:document.getElementById('system-ghost'),explode:document.getElementById('system-explode'),explodeValue:document.getElementById('system-explode-value'),part:document.getElementById('system-part'),status:document.getElementById('system-status')};
 let ersContext='legacy2021',contextToggle=null;
 if(ui.detail&&!document.getElementById('ers-context-toggle')){contextToggle=document.createElement('button');contextToggle.id='ers-context-toggle';contextToggle.type='button';contextToggle.className='wide';contextToggle.setAttribute('aria-pressed','false');ui.detail.append(contextToggle);}
 const originalHint=ui.hint?.textContent||'';
 const systemsHint='SISTEMAS: USE TAB E SETAS PARA ESCOLHER · ENTER/ESPAÇO PARA ABRIR · CLIQUE EM UMA PEÇA PARA LER O NOME';
 if(ui.detail&&ui.list&&ui.detail.parentElement===ui.list.parentElement)ui.detail.parentElement.insertBefore(ui.detail,ui.list);
 const cardFor=id=>ui.list?.querySelector(`[data-system="${id}"]`);
 const syncView=name=>ui.views.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.view===name)));
 const setStatus=text=>{if(ui.status){ui.status.textContent=text;ui.status.hidden=!text;}};

 // ------------------------------------------------------------------ carregamento do asset
 function attachPart(mesh,systemId){
  const data=mesh.userData||{};
  const entry={object:mesh,system:systemId,part:data.part||mesh.name,base:mesh.position.clone(),explode:Array.isArray(data.explode)?new THREE.Vector3(...data.explode):new THREE.Vector3(),original:mesh.material,era:data.era||null,hideGroup:data.hide_group||null,flow:data.flow||null};
  parts.push(entry);mesh.userData.systemPart=entry;
  mesh.castShadow=false;mesh.receiveShadow=true;mesh.renderOrder=10;
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
   if(/^Disco carbono-carbono/.test(m.name)){m.emissive=new THREE.Color('#ff5a1e');m.emissiveIntensity=0;pulseMaterials.push({material:m,kind:'disc'});}
   if(/^LED /.test(m.name))pulseMaterials.push({material:m,kind:'led',base:m.emissiveIntensity});
  }});
 }
 function distribute(gltf){
  gltfScene=gltf.scene;
  const stray=[];
  for(const child of [...gltfScene.children]){
   const id=/^system_(\w+)$/.exec(child.name)?.[1];
   const group=id?groups.get(id):null;
   if(!group){stray.push(child.name);continue;}
   for(const node of [...child.children])group.add(node);
   child.traverse(node=>{if(node.isMesh)attachPart(node,id);});
  }
  for(const [id,group] of groups)group.traverse(node=>{if(node.isMesh&&!node.userData.systemPart)attachPart(node,id);});
  if(stray.length)console.warn('Sistemas: nós fora do contrato ignorados',stray);
  prepareMaterials(root);
  applyEra();applyCovers();applyExplode();applyFlows();
  root.updateMatrixWorld(true);
  window.viewerInfo&&(window.viewerInfo.systemsParts=parts.length,window.viewerInfo.systemsLoaded=true);
 }
 function load(){
  if(loadPromise)return loadPromise;
  state='loading';setStatus('Carregando os sistemas em 3D…');
  loadPromise=(async()=>{
   const response=await fetch(assetUrl);if(!response.ok)throw new Error('Sistemas HTTP '+response.status);
   const bytes=await response.arrayBuffer();await MeshoptDecoder.ready;
   const gltf=await new GLTFLoader().setMeshoptDecoder(MeshoptDecoder).parseAsync(bytes,assetUrl.replace(/[^/]+$/,''));
   if(disposed)return;
   distribute(gltf);state='ready';setStatus('');
   if(enabled){show(active,false);}
  })().catch(error=>{console.error(error);state='failed';setStatus('Não foi possível carregar os sistemas. Recarregue a página para tentar novamente.');});
  return loadPromise;
 }

 // ------------------------------------------------------------------ estados visuais
 function applyEra(){for(const entry of eraNodes)entry.object.visible=entry.era!=='2021'||ersContext==='legacy2021';}
 function applyCovers(){for(const entry of coverNodes)entry.object.visible=!coversOpen&&(entry.era!=='2021'||ersContext==='legacy2021');}
 function applyExplode(){for(const entry of parts){if(entry.explode.lengthSq()===0)continue;entry.object.position.copy(entry.base).addScaledVector(entry.explode,explodeAmount*1.6);}}
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
 function setPicked(entry){picked=entry;highlight(entry,Boolean(entry));if(ui.part){ui.part.hidden=!entry;ui.part.textContent=entry?`Peça: ${entry.part} · ${meta(entry.system).label}`:'';}}

 function setERSContext(mode){ersContext=mode==='current2026'?'current2026':'legacy2021';applyEra();applyCovers();applyFlows();if(active==='ers'||active==='power'){updateUI(active);frame(active,directions[currentView],false);}}
 function updateUI(id=active){
  if(disposed)return;
  const overview=id==='overview',system=overview?null:meta(id),rovingId=overview?SYSTEM_CATALOG[0]?.id:id;syncView(currentView);if(ui.title)ui.title.textContent=overview?'Visão geral dos sistemas':system.label;if(ui.kicker)ui.kicker.textContent=overview?'CAMADAS INTERNAS / VISÃO DIDÁTICA':`${system.number} / ${system.short}`;if(ui.description)ui.description.textContent=overview?'Catorze sistemas modelados em escala real dentro do carro fantasma. Selecione uma camada para estudá-la isolada, com fluxos, tampas abertas e peças separadas. Não é CAD nem validação física.':`${system.description} Simplificação didática; conexões indicam função, não escala homologada.${id==='ers'||id==='power'?` Contexto ativo: ${ersContext==='legacy2021'?'arquitetura do vídeo / 2021 (MGU-H legado visível)':'arquitetura atual / 2026 (MGU-H removido)'}.`:''}`;if(ui.chapter)ui.chapter.textContent=overview?'14 sistemas · vídeo de referência':`Capítulo ${system.chapter} · vídeo de referência`;const count=overview?parts.length:parts.filter(entry=>entry.system===id).length;if(ui.count)ui.count.textContent=overview?(count?`${count} PEÇAS · 14 CAMADAS`:'14 CAMADAS'):`${system.number} / 14${count?` · ${count} PEÇAS`:''}`;if(contextToggle){contextToggle.hidden=id!=='ers'&&id!=='power';contextToggle.textContent=ersContext==='legacy2021'?'Ver contexto atual 2026':'Voltar ao vídeo / 2021';contextToggle.setAttribute('aria-pressed',String(ersContext==='current2026'));}if(ui.overview){ui.overview.setAttribute('aria-pressed',String(overview));ui.overview.textContent=overview?'Todos os sistemas visíveis':'Mostrar todos os sistemas';ui.overview.style.color=overview?'#fff':'';ui.overview.style.backgroundColor=overview?'var(--red)':'';}if(ui.hint)ui.hint.style.textShadow=enabled?'0 1px 3px var(--paper),0 0 8px var(--paper)':'';SYSTEM_CATALOG.forEach((item,index)=>{const card=cardFor(item.id);if(card){const selected=!overview&&item.id===id;card.setAttribute('aria-pressed',String(selected));card.tabIndex=item.id===rovingId?0:-1;const chapterLink=ui.chapters[index];if(chapterLink){if(selected)chapterLink.setAttribute('aria-current','true');else chapterLink.removeAttribute('aria-current');}}});if(overview)ui.chapters.forEach(link=>link.removeAttribute('aria-current'));if(ui.detail)ui.detail.style.setProperty('--system-color',overview?'#d92135':system.color);
  ui.flows?.setAttribute('aria-pressed',String(flowsOn));ui.covers?.setAttribute('aria-pressed',String(coversOpen));ui.schematic?.setAttribute('aria-pressed',String(schematic));ui.ghost?.setAttribute('aria-pressed',String(ghostWanted));if(ui.flows)ui.flows.disabled=overview;if(ui.explode){ui.explode.value=Math.round(explodeAmount*100);ui.explode.disabled=overview;}if(ui.explodeValue)ui.explodeValue.textContent=Math.round(explodeAmount*100)+'%';
 }
 function objectFor(id){return id==='overview'?root:groups.get(id);}
 function geometryBounds(object){const bounds=new THREE.Box3().makeEmpty();object.traverse(node=>{if(!node.visible||node.userData.systemTag||(!node.isMesh&&!node.isLine&&!node.isPoints))return;const entry=node.userData.systemPart;if(entry?.flow)return;bounds.expandByObject(node);});return bounds;}
 function viewportAspect(){const width=canvas?.clientWidth||canvas?.width,height=canvas?.clientHeight||canvas?.height;return width>0&&height>0?width/height:Math.max(camera?.aspect??1,.5);}
 const directions={hero:[1,.35,1.18],side:[1,.12,0],front:[0,.16,1],rear:[0,.18,-1],top:[.001,1,0],bottom:[.001,-1,0]};
 function frame(id,direction=directions[currentView],animate=true){if(disposed||typeof moveCamera!=='function')return;const object=objectFor(id);if(!object)return;object.updateMatrixWorld(true);const bounds=geometryBounds(object);if(bounds.isEmpty()){if(state!=='ready'){const target=new THREE.Vector3(0,.45,0);moveCamera(target.clone().addScaledVector(new THREE.Vector3(...direction).normalize(),mobile?6.8:6.4),target,animate);}return;}const target=bounds.getCenter(new THREE.Vector3());if(id==='overview')target.y=.45;const dir=new THREE.Vector3(...direction).normalize(),worldUp=new THREE.Vector3(0,1,0),right=new THREE.Vector3().crossVectors(worldUp,dir);if(right.lengthSq()<1e-6)right.set(1,0,0);else right.normalize();const up=new THREE.Vector3().crossVectors(dir,right).normalize(),halfVertical=Math.tan(THREE.MathUtils.degToRad(camera?.fov??45)/2),halfHorizontal=halfVertical*Math.max(viewportAspect(),.1);let required=0;for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const offset=new THREE.Vector3(x,y,z).sub(target),depth=offset.dot(dir);required=Math.max(required,depth+Math.abs(offset.dot(right))/halfHorizontal,depth+Math.abs(offset.dot(up))/halfVertical);}const size=bounds.getSize(new THREE.Vector3()),minimum=id==='overview'?(mobile?6.8:6.4):(mobile?1.6:1.2),distance=THREE.MathUtils.clamp(Math.max(required*1.18,size.length()*1.08,minimum),minimum,30);moveCamera(target.clone().addScaledVector(dir,distance),target,animate);}
 function show(id='overview',animate=true){if(disposed)return;if(!groups.has(id)&&id!=='overview')id='overview';setEnabled(true);const previousActive=active;active=id;setPicked(null);if(id!==previousActive&&explodeAmount){explodeAmount=0;applyExplode();}groups.forEach((group,key)=>{group.visible=id==='overview'||key===id;});applyFlows();if(previousActive!==id)for(const entry of carriers)if(entry.system===previousActive)entry.object.material=materialFor(entry);updateUI(id);frame(id,directions[currentView],animate);}
 function view(name){if(disposed||!enabled)return;currentView=directions[name]?name:'hero';syncView(currentView);frame(active,directions[currentView],false);}
 function captureGhost(){if(disposed||ghostEntries.length||!model?.traverse)return;model.traverse(object=>{if(!object.isMesh)return;const original=object.material;const cloneMaterial=material=>{if(!material?.clone)return material;const clone=material.clone();if('color' in clone)clone.color.set('#8b9aa4');if('map' in clone)clone.map=null;if('emissive' in clone){clone.emissive.set('#22303a');clone.emissiveIntensity=.16;}clone.transparent=true;clone.opacity=.105;clone.depthWrite=false;clone.depthTest=true;return clone;};ghostEntries.push({object,original,ghost:Array.isArray(original)?original.map(cloneMaterial):cloneMaterial(original)});});}
 function setGhost(on){if(disposed)return;captureGhost();if(on&&!ghostOn){ghostEntries.forEach(entry=>{entry.object.material=entry.ghost;});ghostOn=true;}else if(!on&&ghostOn){ghostEntries.forEach(entry=>{entry.object.material=entry.original;});ghostOn=false;}}
 function setEnabled(on){if(disposed||on===enabled)return;enabled=on;root.visible=on;document.body.classList.toggle('systems-active',on);if(ui.hint)ui.hint.textContent=on?systemsHint:originalHint;if(on){load();previous={model:model?.visible,driver:driver?.root.visible,engine:engine?.root.visible};if(garage?.enabled)garage.setEnabled(false);if(model)model.visible=true;if(driver?.root)driver.root.visible=false;if(engine?.root)engine.root.visible=false;setGhost(ghostWanted);}else{setGhost(false);setPicked(null);if(model)model.visible=previous.model??true;if(driver?.root)driver.root.visible=previous.driver??true;if(engine?.root)engine.root.visible=previous.engine??false;root.visible=false;}}

 // ------------------------------------------------------------------ interação
 const ray=new THREE.Raycaster(),pointer=new THREE.Vector2();let down=null;
 const onPointerDown=event=>{down=[event.clientX,event.clientY];};
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
 return {root,groups,show,view,activate:show,deactivate:()=>setEnabled(false),setPaused(value){paused=Boolean(value);},setERSContext,load,reset:()=>{explodeAmount=0;applyExplode();show('overview',false);},
  setRevealInExplode(value){revealEnabled=Boolean(value);},
  get active(){return enabled?active:null;},get enabled(){return enabled;},get state(){return state;},get ready(){return state==='ready';},get revealing(){return revealing;},get context(){return ersContext;},get parts(){return parts;},get paused(){return paused||reducedMotion.matches;},
  update(dt,now=performance.now()/1000){
   if(disposed)return;
   // Revelação dos sistemas ao desmontar o carro na bancada Carro: a carroceria se afasta e os conjuntos ficam no lugar.
   const wantReveal=!enabled&&revealEnabled&&Boolean(mechanics)&&mechanics.amount>.02&&!mechanics.isolated;
   if(wantReveal&&state==='idle')load();
   const canReveal=wantReveal&&state==='ready';
   if(canReveal!==revealing){revealing=canReveal;if(revealing){groups.forEach(group=>{group.visible=true;});for(const flow of flows)flow.object.visible=false;}else if(!enabled){for(const flow of flows)flow.object.visible=false;}}
   root.visible=enabled||revealing;
   if(window.viewerInfo){window.viewerInfo.systemsRevealing=revealing;window.viewerInfo.systemsFlowsVisible=flows.reduce((n,f)=>n+(f.object.visible?1:0),0);window.viewerInfo.systemsActiveId=enabled?active:null;}
   if(!root.visible||paused||reducedMotion.matches||document.hidden)return;
   const step=Math.min(Math.max(dt,0),.05);time+=step;
   for(const s of spinners)s.object.quaternion.copy(advanceLocalSpin(s.object.quaternion,s.axis,step*s.rate));
   for(const kind of Object.keys(flowMaterials)){const f=flowMaterials[kind];f.map.offset.y=(f.map.offset.y-step*f.speed)%1;}
   for(const p of pulseMaterials){if(p.kind==='disc')p.material.emissiveIntensity=enabled&&(active==='brakes')?.25+.25*(.5+.5*Math.sin(time*2.2)):0;else if(p.kind==='led')p.material.emissiveIntensity=p.base*(.6+.4*(.5+.5*Math.sin(time*4+p.material.id)));}
  },
  dispose(){if(disposed)return;setEnabled(false);document.removeEventListener('visibilitychange',onVisibilityChange);canvas?.removeEventListener('pointerdown',onPointerDown);canvas?.removeEventListener('pointerup',onPointerUp);ui.overview?.removeEventListener('click',onOverviewClick);ui.back?.removeEventListener('click',onBackClick);contextToggle?.removeEventListener('click',onContextToggle);ui.flows?.removeEventListener('click',onFlows);ui.covers?.removeEventListener('click',onCovers);ui.schematic?.removeEventListener('click',onSchematic);ui.ghost?.removeEventListener('click',onGhost);ui.explode?.removeEventListener('input',onExplode);SYSTEM_CATALOG.forEach(system=>{const card=cardFor(system.id);card?.removeEventListener('click',onSystemClick);card?.removeEventListener('keydown',onSystemKey);});ghostEntries.forEach(entry=>{for(const material of [].concat(entry.ghost)){if(material&&material!==entry.original&&material.dispose)material.dispose();}});const geometries=new Set();root.traverse(node=>{if(node.isMesh)geometries.add(node.geometry);});geometries.forEach(geometry=>geometry.dispose());materials.forEach(material=>material.dispose());textures.forEach(texture=>texture.dispose());root.removeFromParent();disposed=true;}};
}
