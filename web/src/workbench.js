import * as THREE from 'three';
import {GLTFExporter} from 'three/addons/exporters/GLTFExporter.js';

export function createWorkbench({scene,model,driver,engine,garage,controls,camera,moveCamera,closeEngine,showCar}){
 const $=id=>document.getElementById(id),inspection=new THREE.Group();inspection.name='Bancada de inspeção';scene.add(inspection);
 let active='car',mode='isolated',currentObject=null,target=new THREE.Vector3(),radius=1;
 const panels=[...document.querySelectorAll('.panel > .block')];
 for(const panel of panels){const title=panel.querySelector('h3')?.textContent||'';panel.dataset.labPanel=title.startsWith('MOTOR')?'engine':panel.id==='air-panel'?'air':title.startsWith('CAPACETE')?'helmet':title.startsWith('PILOTO')?'driver':title.startsWith('AMBIENTES')?'world':'car';}
 const tabs=[...document.querySelectorAll('[data-lab-tab]')];
 let bounds=null;
 function frame(object){bounds=new THREE.Box3().setFromObject(object);target=bounds.getCenter(new THREE.Vector3());view('hero');}
 function view(name){
  const directions={hero:[1,.32,1.35],side:[1,.1,0],front:[0,.08,1],rear:[0,.1,-1],top:[.001,1,0],bottom:[.001,-1,0]},direction=new THREE.Vector3(...directions[name]).normalize();
  if(bounds){const right=new THREE.Vector3().crossVectors(new THREE.Vector3(0,1,0),direction).normalize(),up=new THREE.Vector3().crossVectors(direction,right),tan=Math.tan(THREE.MathUtils.degToRad(camera.fov/2));radius=0;
   for(const x of [bounds.min.x,bounds.max.x])for(const y of [bounds.min.y,bounds.max.y])for(const z of [bounds.min.z,bounds.max.z]){const p=new THREE.Vector3(x,y,z).sub(target);radius=Math.max(radius,p.dot(direction)+Math.max(Math.abs(p.dot(right))/(tan*camera.aspect),Math.abs(p.dot(up))/tan));}radius=Math.max(radius*1.16,mode==='cockpit'?1.2:.5);
  }
  moveCamera(target.clone().addScaledVector(direction,radius),target);
  document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===name)));
 }
 function rebuild(){
  inspection.clear();currentObject=null;
  if((active!=='helmet'&&active!=='driver')||mode==='cockpit')return;
  const clone=(active==='helmet'?driver.helmet.root:driver.root).clone(true);clone.visible=true;
  if(active==='helmet'){clone.position.set(0,0,0);clone.rotation.set(0,0,0);}
  inspection.add(clone);inspection.position.set(0,0,0);inspection.updateMatrixWorld(true);
  const b=new THREE.Box3().setFromObject(inspection),center=b.getCenter(new THREE.Vector3());inspection.position.set(-center.x,-b.min.y+.015,-center.z);currentObject=clone;inspection.updateMatrixWorld(true);frame(inspection);
 }
 function refreshPanels(){for(const p of panels)if(p.dataset.labPanel!=='air')p.hidden=p.dataset.labPanel!==active;document.querySelector('.panel-heading h2').textContent={car:'Carro',engine:'Motor V6',helmet:'Capacete',driver:'Piloto',world:'Ambientes'}[active];document.querySelector('.panel-heading .badge').style.display=active==='car'?'':'none';}
 function setTab(next){
  if(document.body.classList.contains('wind-active'))$('wind-toggle').click();closeEngine();
  active=next;mode='isolated';document.body.dataset.labTab=active;inspection.visible=false;inspection.clear();model.visible=true;controls.autoRotate=false;$('orbit').setAttribute('aria-pressed','false');
  $('reset').click();garage.setEnabled(active==='car'||active==='engine'||active==='world');
  tabs.forEach(t=>{const on=t.dataset.labTab===active;t.setAttribute('aria-selected',String(on));t.tabIndex=on?0:-1;});
  document.querySelector('.panel').setAttribute('aria-labelledby','tab-'+active);refreshPanels();
  if(active==='helmet'||active==='driver'){rebuild();}else if(active==='engine')$('engine-open').click();else showCar();
 }
 tabs.forEach((t,i)=>{t.onclick=()=>setTab(t.dataset.labTab);t.onkeydown=e=>{let n=null;if(e.key==='ArrowRight')n=(i+1)%tabs.length;if(e.key==='ArrowLeft')n=(i+tabs.length-1)%tabs.length;if(e.key==='Home')n=0;if(e.key==='End')n=tabs.length-1;if(n!==null){e.preventDefault();tabs[n].focus();setTab(tabs[n].dataset.labTab);}};});
 function cockpit(){mode='cockpit';inspection.visible=false;model.visible=true;garage.setEnabled(true);model.updateMatrixWorld(true);frame(driver.helmet.root);}
 for(const prefix of ['helmet','driver']){$(prefix+'-cockpit').onclick=cockpit;$(prefix+'-isolated').onclick=()=>{mode='isolated';garage.setEnabled(false);rebuild();};}
 for(const [id,key,scale] of [['fit-height','height',.001],['fit-depth','foreAft',.001],['fit-pitch','pitch',Math.PI/180]]){
  $(id).oninput=()=>{driver.setFit({[key]:Number($(id).value)*scale});$(id+'-value').textContent=$(id).value+(key==='pitch'?'°':' mm');if(mode==='isolated')rebuild();};
 }
 $('fit-reset').onclick=()=>{driver.setFit({height:0,foreAft:0,pitch:0});for(const id of ['fit-height','fit-depth','fit-pitch']){$(id).value=0;$(id+'-value').textContent=id==='fit-pitch'?'0°':'0 mm';}if(mode==='isolated')rebuild();};
 async function downloadModel(kind){const button=$(kind+'-export'),status=$(kind+'-export-status');button.disabled=true;status.textContent='Preparando modelo…';
  try{const object=(kind==='helmet'?driver.helmet.root:driver.root).clone(true);object.visible=true;object.position.set(0,0,0);object.rotation.set(0,0,0);const data=await new GLTFExporter().parseAsync(object,{binary:true});const url=URL.createObjectURL(new Blob([data],{type:'model/gltf-binary'})),a=document.createElement('a');a.href=url;a.download=kind==='helmet'?'INTEIA-capacete-1991.glb':'INTEIA-piloto-cockpit.glb';a.click();setTimeout(()=>URL.revokeObjectURL(url),10000);status.textContent='Modelo exportado com materiais e texturas.';}catch(error){console.error(error);status.textContent='Não foi possível exportar.';}finally{button.disabled=false;}
 }
 $('helmet-export').onclick=()=>downloadModel('helmet');$('driver-export').onclick=()=>downloadModel('driver');
 $('world-box').onclick=()=>{if(document.body.classList.contains('wind-active'))$('wind-toggle').click();garage.setEnabled(true);$('garage-view').click();};
 $('world-studio').onclick=()=>{if(document.body.classList.contains('wind-active'))$('wind-toggle').click();garage.setEnabled(false);showCar();};
 $('world-tunnel').onclick=()=>{if(!document.body.classList.contains('wind-active'))$('wind-toggle').click();};
 $('world-export').onclick=()=>$('garage-export').click();
 refreshPanels();
 return {get inspecting(){return active==='helmet'||active==='driver';},view,setTab,
  update(){const isolated=(active==='helmet'||active==='driver')&&mode==='isolated';inspection.visible=isolated;model.visible=!isolated;if(isolated)engine.root.visible=false;},
  reset(){if(active==='helmet'||active==='driver'){if(mode==='isolated')rebuild();else cockpit();}}
 };
}
