import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

// Peças sobressalentes do Box INTEIA: pneus por composto e condição, asas de baixa e alta carga, asa de viga
// dupla e venezianas de arrefecimento. O asset web/assets/sobressalentes-v1.glb traz um nó por peça, com extras
// {slot, variant, target, mode}. No modo `geometry` a malha do nó alvo do carro é trocada no lugar (mesma origem,
// mesmo pivô de giro, mesma explosão e seleção); no modo `attach` a peça é anexada ao nó alvo.

export const SPARES_ASSET='./assets/sobressalentes-v1.glb';

export const SPARE_SLOTS=Object.freeze([
 {id:'tyres',label:'Pneus',variants:[['original','Originais do carro'],['macio','Macio · faixa vermelha'],['medio','Médio · faixa amarela'],['duro','Duro · faixa branca'],['intermediario','Intermediário · faixa verde'],['chuva','Chuva extrema · faixa azul']]},
 {id:'rear_wing',label:'Asa traseira',variants:[['original','Original (carga média)'],['baixa','Baixa carga · pista rápida'],['alta','Alta carga · pista travada']]},
 {id:'front_wing',label:'Flap dianteiro',variants:[['original','Original (carga média)'],['baixa','Baixa carga'],['alta','Alta carga']]},
 {id:'beam_wing',label:'Asa de viga',variants:[['original','Simples'],['dupla','Dupla']]},
 {id:'cooling',label:'Arrefecimento',variants:[['original','Fechado'],['aberto','Venezianas abertas']]},
]);

export const SPARE_PRESETS=Object.freeze([
 {id:'rapida',label:'Pista rápida',hint:'Retas longas: asas finas, pouco arrasto, pneu médio.',setup:{tyres:'medio',rear_wing:'baixa',front_wing:'baixa',beam_wing:'original',cooling:'original'}},
 {id:'travada',label:'Pista travada',hint:'Curvas lentas: máxima carga aerodinâmica e pneu macio.',setup:{tyres:'macio',rear_wing:'alta',front_wing:'alta',beam_wing:'dupla',cooling:'original'}},
 {id:'intermediaria',label:'Pista úmida',hint:'Pista secando: pneu intermediário e carga alta.',setup:{tyres:'intermediario',rear_wing:'alta',front_wing:'original',beam_wing:'dupla',cooling:'original'}},
 {id:'chuva',label:'Chuva',hint:'Chuva forte: pneu de chuva extrema e asas de alta carga.',setup:{tyres:'chuva',rear_wing:'alta',front_wing:'alta',beam_wing:'dupla',cooling:'original'}},
 {id:'calor',label:'Calor extremo',hint:'Pista quente: pneu duro e venezianas abertas na tampa do motor.',setup:{tyres:'duro',rear_wing:'original',front_wing:'original',beam_wing:'original',cooling:'aberto'}},
 {id:'original',label:'Carro original',hint:'Configuração de fábrica do laboratório.',setup:{tyres:'original',rear_wing:'original',front_wing:'original',beam_wing:'original',cooling:'original'}},
]);

export const SPARE_INFO=Object.freeze({
 tyres:{
  macio:['Composto mais aderente e mais rápido por volta, mas que se desgasta em poucas voltas.','A faixa vermelha identifica o composto; é o pneu da classificação e dos trechos finais de corrida.'],
  medio:['Equilíbrio entre aderência e durabilidade; o pneu mais usado no primeiro stint.','A faixa amarela marca o médio; em muitas corridas ele decide a estratégia de uma ou duas paradas.'],
  duro:['Composto mais durável e mais lento para aquecer; aguenta stints longos e pista quente.','A faixa branca é do duro; em circuitos abrasivos como Barcelona ele pode fazer mais de 40 voltas.'],
  intermediario:['Pneu com sulcos leves para pista úmida ou secando; dispersa cerca de 30 litros de água por segundo a 300 km/h.','A faixa verde identifica o intermediário, o pneu mais versátil em transição de chuva para seco.'],
  chuva:['Pneu de chuva extrema com sulcos profundos que expulsam 85 litros de água por segundo em velocidade máxima.','A faixa azul marca o pneu de chuva; abaixo de certa quantidade de água ele superaquece e o piloto pede o intermediário.'],
 },
 rear_wing:{
  baixa:['Plano principal fino e flap curto: menos carga na traseira e muito menos arrasto para velocidade máxima na reta.','Em Monza a asa é a mais plana do ano; a velocidade final passa de 350 km/h com esse pacote.'],
  alta:['Plano principal espesso e arqueado, flap longo e aba Gurney: máxima carga traseira para curvas lentas.','Em Mônaco a asa é a mais inclinada da temporada; a aba Gurney no bordo de fuga acrescenta carga sem aumentar o tamanho da asa.'],
 },
 front_wing:{
  baixa:['Flap dianteiro com menos ângulo e corda menor para equilibrar o carro com a asa traseira de pista rápida.','O ajuste do flap é a mudança mais comum nos boxes: um clique altera o equilíbrio entre dianteira e traseira.'],
  alta:['Flap dianteiro com mais ângulo e corda maior para gerar carga na frente em curvas lentas e em pista molhada.','Em chuva os pilotos pedem mais asa dianteira para o carro girar; o excesso, porém, provoca perda de aderência traseira.'],
 },
 beam_wing:{dupla:['Dois elementos acima da estrutura traseira que ajudam a extrair o ar do difusor e somam carga em curvas lentas.','A asa de viga dupla voltou com o regulamento de 2022; equipes a trocam por uma simples nas pistas de reta longa.']},
 cooling:{aberto:['Venezianas abertas na tampa do motor liberam ar quente dos radiadores em circuitos de calor extremo.','Cada abertura custa velocidade na reta, por isso as equipes têm várias tampas com níveis diferentes de abertura.']},
});

export function createSpares({model,mechanics,assetUrl=SPARES_ASSET,onChange=()=>{}}={}){
 const setup=Object.fromEntries(SPARE_SLOTS.map(slot=>[slot.id,'original']));
 const library=new Map();      // `${slot}/${variant}` -> [{target, mode, mesh}]
 const originals=new Map();    // target -> {meshes:[{mesh,geometry,material,visible}]}
 const attached=[];            // {slot, object, parent}
 let state='idle',loadPromise=null,disposed=false,pending=null;

 const targetObject=name=>{const object=model?.getObjectByName(name);if(!object)return null;const meshes=[];if(object.isMesh)meshes.push(object);object.traverse(node=>{if(node!==object&&node.isMesh)meshes.push(node);});return {object,meshes};};

 function load(){
  if(loadPromise)return loadPromise;
  state='loading';
  loadPromise=new Promise((resolve,reject)=>{const loader=new GLTFLoader();loader.load(assetUrl,gltf=>{gltf.scene.traverse(node=>{if(!node.isMesh||!node.userData?.spare)return;const {slot,variant,target,mode}=node.userData;const key=`${slot}/${variant}`;if(!library.has(key))library.set(key,[]);library.get(key).push({target,mode,mesh:node,label:node.userData.label||''});});state='ready';resolve();},undefined,error=>{state='failed';reject(error);});});
  return loadPromise;
 }

 function remember(target){if(originals.has(target))return originals.get(target);const found=targetObject(target);if(!found)return null;const record={object:found.object,meshes:found.meshes.map(mesh=>({mesh,geometry:mesh.geometry,material:mesh.material,visible:mesh.visible}))};originals.set(target,record);return record;}

 function revert(slot){
  for(const [key,items] of library){if(!key.startsWith(slot+'/'))continue;for(const item of items){if(item.mode!=='geometry')continue;const record=originals.get(item.target);if(!record)continue;record.meshes.forEach(entry=>{entry.mesh.geometry=entry.geometry;entry.mesh.material=entry.material;entry.mesh.visible=entry.visible;});}}
  for(let i=attached.length-1;i>=0;i--){if(attached[i].slot!==slot)continue;const {object,parent}=attached[i];parent.remove(object);attached.splice(i,1);}
 }

 function applySlot(slot,variant){
  revert(slot);
  if(variant==='original')return true;
  const items=library.get(`${slot}/${variant}`);
  if(!items)return false;
  for(const item of items){
   if(item.mode==='geometry'){const record=remember(item.target);if(!record||!record.meshes.length)continue;const [first,...rest]=record.meshes;first.mesh.geometry=item.mesh.geometry;if(slot==='tyres')first.mesh.material=item.mesh.material;first.mesh.visible=true;rest.forEach(entry=>{entry.mesh.visible=false;});}
   else{const record=remember(item.target);if(!record)continue;const clone=item.mesh.clone();clone.position.set(0,0,0);clone.quaternion.identity();clone.scale.set(1,1,1);clone.userData={spareAttachment:slot,recordId:record.object.userData.recordId};clone.castShadow=record.object.castShadow;clone.receiveShadow=record.object.receiveShadow;record.object.add(clone);attached.push({slot,object:clone,parent:record.object});}
  }
  return true;
 }

 async function set(slot,variant){
  if(disposed||!SPARE_SLOTS.some(s=>s.id===slot))return false;
  setup[slot]=variant;
  if(state!=='ready'){pending=pending||{};pending[slot]=variant;try{await load();}catch{onChange({...setup},'failed');return false;}if(pending){const queued=pending;pending=null;for(const [s,v] of Object.entries(queued))applySlot(s,v);onChange({...setup},'ready');return true;}}
  const ok=applySlot(slot,variant);
  onChange({...setup},'ready');
  return ok;
 }

 async function preset(id){const found=SPARE_PRESETS.find(p=>p.id===id);if(!found)return false;for(const [slot,variant] of Object.entries(found.setup))setup[slot]=variant;if(state!=='ready'){try{await load();}catch{onChange({...setup},'failed');return false;}}for(const [slot,variant] of Object.entries(found.setup))applySlot(slot,variant);onChange({...setup},'ready');return true;}

 function presetMatching(){return SPARE_PRESETS.find(p=>Object.entries(p.setup).every(([slot,variant])=>setup[slot]===variant))?.id||null;}

 return {
  load,set,preset,presetMatching,
  describe(slot,variant){const info=SPARE_INFO[slot]?.[variant];return info?{funcao:info[0],curiosidade:info[1]}:null;},
  get setup(){return {...setup};},get state(){return state;},get ready(){return state==='ready';},
  reset(){for(const slot of SPARE_SLOTS)applySlot(slot.id,'original'),setup[slot.id]='original';onChange({...setup},state);},
  dispose(){if(disposed)return;disposed=true;for(const slot of SPARE_SLOTS)revert(slot.id);},
 };
}
