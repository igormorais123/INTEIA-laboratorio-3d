import {drawBrand} from './identity.js';
import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';

/** INTEIA development bay. Original scene inspired by publicly visible F1 garages. */
export function createGarage({scene,renderer,studio,camera,mechanics}) {
 const root=new THREE.Group();root.name='INTEIA development garage';scene.add(root);
 const walls=[],roof=[],entrance=[],screenUpdates=[];let section='Architecture',serial=0;
 const mat=(color,metalness=.0,roughness=.5)=>new THREE.MeshStandardMaterial({color,metalness,roughness});
 const white=mat('#d5d9db',.18,.36),charcoal=mat('#242b31',.35,.42),black=mat('#101419',.15,.55),steel=mat('#8f9da4',.82,.28),red=mat('#981b25',.32,.3),rubber=mat('#17191c',.05,.84);
 const led=new THREE.MeshBasicMaterial({color:new THREE.Color('#fff9ec').multiplyScalar(2.4)});
 function box(w,h,d,x,y,z,m=white,rounded=false,parent=root){const geo=rounded?new RoundedBoxGeometry(w,h,d,2,Math.min(.018,w/7,h/7,d/7)):new THREE.BoxGeometry(w,h,d);const o=new THREE.Mesh(geo,m);o.name=section+' '+(++serial);o.userData.section=section;o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;parent.add(o);return o;}
 function cylinder(r1,r2,h,x,y,z,m=steel,parent=root){const o=new THREE.Mesh(new THREE.CylinderGeometry(r1,r2,h,24),m);o.name=section+' '+(++serial);o.userData.section=section;o.position.set(x,y,z);o.castShadow=o.receiveShadow=true;parent.add(o);return o;}
 function tube(points,r=.018,m=black,parent=root){const curve=new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p)));const o=new THREE.Mesh(new THREE.TubeGeometry(curve,40,r,8,false),m);o.name=section+' cable '+(++serial);o.userData.section=section;parent.add(o);return o;}
 function label(text,w,h,x,y,z,rotation=0,bg='#e0e3e4',fg='#26313b',font=50){const c=document.createElement('canvas');c.width=1024;c.height=Math.round(1024*h/w);const ctx=c.getContext('2d');ctx.fillStyle=bg;ctx.fillRect(0,0,c.width,c.height);ctx.fillStyle=fg;ctx.font=`500 ${font}px Arial`;ctx.textBaseline='middle';ctx.textAlign='center';ctx.fillText(text,512,c.height/2,960);const t=new THREE.CanvasTexture(c);t.colorSpace=THREE.SRGBColorSpace;t.anisotropy=8;const o=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:t}));o.position.set(x,y,z);o.rotation.y=rotation;root.add(o);return o;}
 // Seamless epoxy working floor and flush inspection plates.
 box(11,.10,15,0,-.068,0,mat('#969d9f',.16,.4));
 box(3.4,.012,7.6,0,-.007,0,mat('#515b61',.3,.32));
 for(const x of [-1.77,1.77])box(.035,.003,8.2,x,.003,0,red);
 for(const z of [-4.1,4.1])box(3.58,.003,.035,0,.003,z,red);
 for(const x of [-1.05,1.05])for(const z of [-1.65,1.65]){
  box(.72,.006,.80,x,-.001,z,steel);for(const dx of [-.28,.28])for(const dz of [-.32,.32]){const screw=cylinder(.014,.014,.004,x+dx,.004,z+dz,black);}
 }
 // Modular rear cabinetry and wall panels, with narrow shadow gaps.
 const rear=box(11,3.8,.14,0,1.85,-6.5,white);walls.push({o:rear,axis:'z',limit:-6.4});
 const side=box(.14,3.8,13,-5.5,1.85,0,white);walls.push({o:side,axis:'x',limit:-5.4});
 for(let x=-5.2;x<5.5;x+=1.3)box(.012,3.6,.025,x,1.85,-6.40,charcoal);
 box(11,.16,.04,0,.15,-6.39,charcoal);box(11,.045,.04,0,2.65,-6.39,red);
 const brandCanvas=document.createElement('canvas');brandCanvas.width=2048;brandCanvas.height=400;drawBrand(brandCanvas.getContext('2d'),2048,400);
 const brandTexture=new THREE.CanvasTexture(brandCanvas);brandTexture.colorSpace=THREE.SRGBColorSpace;brandTexture.anisotropy=8;
 const brandPlate=new THREE.Mesh(new THREE.PlaneGeometry(3.7,.723),new THREE.MeshBasicMaterial({map:brandTexture,transparent:true,depthWrite:false}));brandPlate.name='INTEIA identity';brandPlate.position.set(0,3.08,-6.38);root.add(brandPlate);
 function cabinet(x,z,w=1.35){
  box(w,.95,.72,x,.53,z,charcoal,true);box(w+.05,.065,.78,x,1.035,z,steel,true);
  for(let i=0;i<5;i++){box(w-.06,.135,.025,x,.21+i*.16,z+.375,white,true);box(w-.18,.018,.022,x,.254+i*.16,z+.393,steel);}
  for(const dx of [-w*.37,w*.37])for(const dz of [-.25,.25])cylinder(.026,.026,.10,x+dx,.05,z+dz,black);
 }
 for(const x of [-3.5,-2.08,-.66,.76,2.18])cabinet(x,-5.77);
 // Workstation displays use real viewer controls or explicitly empty data panels.
 function screen(x,y,z,w,h,kind,rotation=0){
  const group=new THREE.Group();group.position.set(x,y,z);group.rotation.y=rotation;root.add(group);
  box(w+.05,h+.05,.055,0,0,0,black,true,group);
  const c=document.createElement('canvas');c.width=1024;c.height=576;const ctx=c.getContext('2d'),tex=new THREE.CanvasTexture(c);tex.colorSpace=THREE.SRGBColorSpace;tex.anisotropy=8;
  const face=new THREE.Mesh(new THREE.PlaneGeometry(w,h),new THREE.MeshBasicMaterial({map:tex,toneMapped:false}));face.position.z=.031;group.add(face);
  function draw(){ctx.fillStyle='#101a23';ctx.fillRect(0,0,1024,576);ctx.fillStyle='#c62938';ctx.fillRect(32,32,5,44);ctx.fillStyle='#dfe9ef';ctx.font='500 30px Arial';ctx.fillText(kind==='setup'?'CONFIGURAÇÃO  /  CARRO 3D':kind==='plan'?'PLANO DE AVALIAÇÃO':'AQUISIÇÃO DE DADOS',56,65);ctx.strokeStyle='#2a3d4a';ctx.lineWidth=1;for(let i=0;i<6;i++){ctx.beginPath();ctx.moveTo(36,136+i*56);ctx.lineTo(988,136+i*56);ctx.stroke();}
   ctx.font='24px Arial';ctx.fillStyle='#9daeb9';
   if(kind==='setup'){const rows=[['COMPONENTES',String(mechanics.records.length)],['MONTAGEM',`${Math.round((1-mechanics.amount)*100)}%`],['DIREÇÃO',document.getElementById('steering-value').textContent],['ASA TRASEIRA',document.getElementById('drs-value').textContent]];rows.forEach(([k,v],i)=>{ctx.fillStyle='#9daeb9';ctx.fillText(k,44,170+i*70);ctx.fillStyle='#ecf1f3';ctx.fillText(v,720,170+i*70);});}
   else if(kind==='plan'){['01   INSPEÇÃO DO CONJUNTO','02   AJUSTES DE GEOMETRIA','03   ESTUDO DO FLUXO','04   COMPARAÇÃO VISUAL'].forEach((t,i)=>ctx.fillText(t,44,175+i*67));}
   else{ctx.font='34px Arial';ctx.fillStyle='#becbd4';ctx.fillText('Aguardando dados de ensaio',44,242);ctx.font='24px Arial';ctx.fillStyle='#7d929f';ctx.fillText('Nenhuma telemetria conectada',44,293);}
   ctx.fillStyle='#7f97a7';ctx.font='20px Arial';ctx.fillText(kind==='setup'?'ESTADO DO VISUALIZADOR':'PAINEL CENOGRÁFICO / SEM DADOS DE PISTA',36,543);tex.needsUpdate=true;
  }draw();if(kind==='setup')screenUpdates.push(draw);return group;
 }
 for(const [i,kind] of ['plan','setup','data'].entries())screen(-2.35+i*1.65,1.77,-6.28,1.5,.84,kind);
 section='Engineering workstation';
 // Engineer island on the far side: monitors, input devices and chairs.
 box(.88,.07,4.1,-4.45,1.02,-1.5,steel,true);
 for(const z of [-3.15,.1])box(.65,1,.065,-4.45,.49,z,charcoal);
 for(const z of [-2.7,-1.35,0]){
  const s=screen(-4.75,1.52,z,.94,.53,'data',Math.PI/2);cylinder(.024,.024,.34,-4.7,1.21,z,steel);box(.35,.02,.31,-4.57,1.066,z,black,true);
  box(.18,.02,.48,-4.2,1.066,z,black,true);
  // Chair seat, back, central lift and five-spoke castor base.
  box(.48,.09,.47,-3.7,.55,z,charcoal,true);box(.075,.48,.48,-3.48,.83,z,black,true);cylinder(.045,.055,.40,-3.7,.31,z,steel);
  for(let a=0;a<5;a++){const angle=a*Math.PI*2/5,px=-3.7+Math.cos(angle)*.26,pz=z+Math.sin(angle)*.26;tube([[-3.7,.12,z],[px,.10,pz]],.015,steel);const wheel=cylinder(.045,.045,.045,px,.07,pz,rubber);wheel.rotation.z=Math.PI/2;}
 }
 section='Tool trolley';
 // Detailed mobile tool trolley parked beside the work envelope.
 cabinet(3.58,-2.25,1.05);
 for(const x of [3.15,4.0])for(const z of [-2.52,-1.98]){const wheel=cylinder(.075,.075,.045,x,.06,z,rubber);wheel.rotation.z=Math.PI/2;}
 tube([[3.1,.72,-2.60],[3.1,1.12,-2.60],[4.05,1.12,-2.60],[4.05,.72,-2.60]],.018,steel);
 for(let i=0;i<6;i++){const x=3.22+i*.12;box(.035,.018,.24,x,1.08,-2.26,steel,true);cylinder(.032,.032,.024,x,1.085,-2.10,steel);}
 // Wheel-gun body, grip and air hose, resting on trolley.
 cylinder(.055,.05,.23,3.62,1.13,-2.20,charcoal).rotation.z=Math.PI/2;box(.05,.14,.075,3.62,1.09,-2.20,red,true);
 tube([[3.62,1.03,-2.2],[3.9,.45,-2.5],[4.15,.03,-2.4],[4.3,.03,-1.8],[4.0,.03,-1.3]],.012,black);
 section='Tyre storage';
 // Tyre storage rack, four separate slicks with recessed hubs.
 const rackX=4.42,rackZ=-4.76;
 for(const x of [rackX-.52,rackX+.52])for(const z of [rackZ-.53,rackZ+.53])box(.035,2.35,.035,x,1.17,z,steel);
 for(const y of [.16,1.22]){box(1.16,.035,1.18,rackX,y,rackZ,steel);for(const dz of [-.29,.29]){
  const profile=[[.19,-.13],[.29,-.17],[.335,-.15],[.35,-.10],[.35,.10],[.335,.15],[.29,.17],[.19,.13],[.19,-.13]].map(p=>new THREE.Vector2(...p));const tire=new THREE.Mesh(new THREE.LatheGeometry(profile,48),rubber);tire.rotation.x=Math.PI/2;tire.position.set(rackX,y+.39,rackZ+dz);tire.castShadow=true;root.add(tire);
  const hub=new THREE.Mesh(new THREE.TorusGeometry(.19,.015,8,40),steel);hub.position.copy(tire.position);hub.position.z+=.075;root.add(hub);
 }}
 label('PNEUS / RESERVA',1.05,.19,rackX,2.47,rackZ+.55,0,'#242b31','#dfe6ea',54);
 section='Service jack';
 // Front jack kept safely to one side; low wheeled chassis and long handle.
 box(.55,.10,.54,4.55,.12,.3,charcoal,true);for(const x of [4.26,4.84]){const wheel=cylinder(.09,.09,.06,x,.10,.3,rubber);wheel.rotation.z=Math.PI/2;}
 tube([[4.55,.18,.3],[4.55,.42,.55],[4.55,1.15,1.4]],.025,steel);box(.38,.045,.09,4.55,1.15,1.4,red,true);
 section='Overhead services';
 // Overhead service spine with coiled leads and broad workshop luminaires.
 for(const x of [-2.1,2.1])roof.push(box(.045,.08,10,x,3.23,-.5,steel));
 for(const z of [-4.2,-1.8,.6,3]){
  roof.push(box(4.65,.07,.36,0,3.25,z,charcoal,true));roof.push(box(4.40,.015,.26,0,3.205,z,led));
 }
 roof.push(tube([[-2.1,3.18,-1.7],[-2.1,2.4,-1.7],[-2.45,1.7,-1.6],[-2.5,1.05,-1.6]],.016,black));
 const coil=[];for(let i=0;i<160;i++){const t=i/159;coil.push([-2.1+Math.sin(t*50)*.07,2.9-t*.95,1+Math.cos(t*50)*.07]);}roof.push(tube(coil,.012,red));
 // Pit entrance frame remains open; no foreground wall hides the vehicle.
 for(const x of [-5.35,5.35])entrance.push(box(.20,3.6,.22,x,1.8,5.5,charcoal));
 roof.push(box(10.9,.20,.22,0,3.6,5.5,charcoal));
 const garageLights=new THREE.Group();root.add(garageLights);
 const key=new THREE.DirectionalLight('#fff8ed',2);key.position.set(2.5,7,3);key.castShadow=true;key.shadow.mapSize.set(2048,2048);Object.assign(key.shadow.camera,{left:-9,right:9,top:9,bottom:-9,near:.1,far:30});key.shadow.camera.updateProjectionMatrix();key.shadow.normalBias=.006;key.shadow.bias=-.0001;key.shadow.radius=4;key.shadow.blurSamples=8;garageLights.add(key);
 const fill=new THREE.DirectionalLight('#dce9f4',1.1);fill.position.set(-4,3,-4);garageLights.add(fill);garageLights.add(new THREE.HemisphereLight('#f2f6ff','#5d6060',.7));
 // The car reflects the actual bay and its luminous panels.
 const environmentScene=new THREE.Scene();environmentScene.background=new THREE.Color('#a2a9ad');environmentScene.add(root.clone(true));
 const pmrem=new THREE.PMREMGenerator(renderer),env=pmrem.fromScene(environmentScene,.045);pmrem.dispose();
 const studioLights=scene.getObjectByName('Studio lighting');let enabled=false,saved=null,timer=0;root.visible=false;
 return {getExportScene(){const out=root.clone(true);out.traverse(o=>o.visible=true);return out;},get enabled(){return enabled;},root,setEnabled(on){if(on===enabled)return;enabled=on;root.visible=on;document.body.classList.toggle('garage-active',on);document.getElementById('garage-toggle').setAttribute('aria-pressed',String(on));
  if(on){saved={background:scene.background,fog:scene.fog,environment:scene.environment,intensity:scene.environmentIntensity,floor:studio.floor.material.color.clone(),lights:studioLights.visible};studioLights.visible=false;scene.background=new THREE.Color('#6e777c');scene.fog=new THREE.Fog('#6e777c',28,65);scene.environment=env.texture;scene.environmentIntensity=.85;studio.floor.material.color.set('#969d9f');}
  else if(saved){scene.background=saved.background;scene.fog=saved.fog;scene.environment=saved.environment;scene.environmentIntensity=saved.intensity;studio.floor.material.color.copy(saved.floor);studioLights.visible=saved.lights;}
 },update(dt){if(!enabled)return;for(const w of walls)w.o.visible=camera.position[w.axis]>w.limit;roof.forEach(o=>o.visible=camera.position.y<3.10);entrance.forEach(o=>o.visible=camera.position.z<5.25);timer+=dt;if(timer>1){screenUpdates.forEach(fn=>fn());timer=0;}}};
}
