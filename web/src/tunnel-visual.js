import {createFlowDetail} from './flow-detail.js';
import * as THREE from 'three';
// Art-directed smoke paths: a visual envelope, not a CFD solution.
export function createTunnelVisual({scene, size, studio, camera}) {
 const root=new THREE.Group();root.name='Wind tunnel visual chamber';root.visible=false;scene.add(root);
 const metal=new THREE.MeshStandardMaterial({color:0x343d43,metalness:.7,roughness:.36});
 const dark=new THREE.MeshStandardMaterial({color:0x20282e,metalness:.3,roughness:.58});
 const light=new THREE.MeshBasicMaterial({color:0xdce5e9});
 function box(w,h,d,x,y,z,mat=metal){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.receiveShadow=true;root.add(m);return m;}
 box(7,.12,14,0,-.08,0,dark);
 box(2.6,.025,12,0,-.005,0,new THREE.MeshStandardMaterial({color:0x121719,roughness:.64,metalness:.1}));
 for(const x of [-3.3,3.3]){box(.1,.16,14,x,.06,0);box(.018,.012,13,x,.16,0,new THREE.MeshBasicMaterial({color:0x59717d}));}
 const roof=[];
 for(const z of [-6,-3,0]){box(.08,2.85,.1,-3.4,1.40,z);roof.push(box(6.8,.08,.1,0,2.85,z),box(5.8,.018,.04,0,2.79,z,light));}
 const sideWall=box(.08,3.8,14,-3.46,1.85,0,dark);
 const rearWall=box(6.9,3.8,.12,0,1.85,-7,dark);
 const grille=new THREE.LineSegments(new THREE.BufferGeometry(),new THREE.LineBasicMaterial({color:0x4c6373,transparent:true,opacity:.18}));
 const gp=[];for(let x=-3.3;x<=3.3;x+=.16)gp.push(x,0,-6.92,x,3.7,-6.92);for(let y=0;y<3.8;y+=.16)gp.push(-3.3,y,-6.92,3.3,y,-6.92);grille.geometry.setAttribute('position',new THREE.Float32BufferAttribute(gp,3));root.add(grille);
 const lamp=new THREE.PointLight(0xe8f0f5,10,12,2);lamp.position.set(0,3,0);root.add(lamp);

 const tunnelKey=new THREE.DirectionalLight(0xf4f6ff,1.05);tunnelKey.position.set(3,5,1);tunnelKey.castShadow=true;
 tunnelKey.shadow.mapSize.set(2048,2048);Object.assign(tunnelKey.shadow.camera,{left:-7,right:7,top:7,bottom:-7,near:.1,far:25});tunnelKey.shadow.camera.updateProjectionMatrix();tunnelKey.shadow.normalBias=.003;tunnelKey.shadow.bias=-.00008;tunnelKey.shadow.radius=5;tunnelKey.shadow.blurSamples=8;root.add(tunnelKey);
 const rim=new THREE.DirectionalLight(0xa9c7e0,.85);rim.position.set(-3,2,-4);root.add(rim);
 const ambient=new THREE.HemisphereLight(0xe6edf5,0x303a40,.38);root.add(ambient);
 const studioLights=scene.getObjectByName('Studio lighting');
 const uniforms={time:{value:0},strength:{value:.105},turbulence:{value:1}};

 const flow=new THREE.Group();root.add(flow);
 // Overlapping soft, textured puffs: no opaque polylines or ribbon geometry.
 const puffGeo=new THREE.BufferGeometry(),puffData=[];
 let rng=21731;const random=()=>{rng=(1664525*rng+1013904223)>>>0;return rng/4294967296;};
 for(let i=0;i<7200;i++)puffData.push(random(),random(),random());
 puffGeo.setAttribute('position',new THREE.Float32BufferAttribute(puffData,3));
 const puffMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,uniforms,vertexShader:`
 uniform float time;uniform float turbulence;varying float fade;varying float seed;varying float downstream;
 void main(){seed=position.z;float t=fract(position.x+time*.023);float z=6.-12.*t;
 float lane=floor(position.y*5.);float x=(lane-2.)*.72;float y=.36;
 float near=exp(-pow((z+.1)/2.6,4.));
 // Center smoke rides above the body envelope; lateral smoke moves outside wheels.
 float mid=1.-smoothstep(.1,.6,abs(x));
 x+=sign(x)*near*.72;y+=near*(mid*1.02+(1.-mid)*.20);
 float wake=smoothstep(1.7,5.,-z);downstream=wake;
 float spread=.045+wake*.28;
 float theta=position.z*62.83+z*2.-time*.23;
 x+=sin(theta)*spread*(.5+turbulence*.5);y+=cos(theta*1.17)*spread*.6;
 x+=wake*sin(z*2.7-time*.31+lane)*.22*turbulence;
 y+=wake*(.12+sin(z*3.-time*.4+lane)*.16*turbulence);
 vec4 mv=modelViewMatrix*vec4(x,y,z,1.);gl_Position=projectionMatrix*mv;
 gl_PointSize=clamp((.38+wake*.72)*(.8+seed*.7)*850./(-mv.z),2.,190.);
 fade=smoothstep(0.,.05,t)*(1.-smoothstep(.78,1.,t))*(.012-wake*.007)*( .75+seed*.5);
 }`,fragmentShader:`
 varying float fade;varying float seed;varying float downstream;uniform float strength;uniform float time;
 float hash(vec2 p){return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453);}
 float noise(vec2 p){vec2 i=floor(p),f=fract(p);f=f*f*(3.-2.*f);return mix(mix(hash(i),hash(i+vec2(1,0)),f.x),mix(hash(i+vec2(0,1)),hash(i+vec2(1,1)),f.x),f.y);}
 void main(){vec2 p=gl_PointCoord-.5;float r=length(p)*2.;
 float cloud=noise(p*5.+seed*20.+vec2(time*.09,0.))*.6+noise(p*11.+seed*43.)*.3+noise(p*23.+seed*73.)*.1;
 float a=exp(-r*r*2.4)*(1.-smoothstep(.45,1.,r))*(.35+cloud*.9);
 vec3 color=mix(vec3(.53,.62,.68),vec3(.89,.94,.96),cloud);
 gl_FragColor=vec4(color,a*fade*strength*6.*(1.+downstream*.35));}`});
 const puffs=new THREE.Points(puffGeo,puffMaterial);puffs.frustumCulled=false;flow.add(puffs);
 for(let i=-2;i<=2;i++){
 const nozzle=new THREE.Mesh(new THREE.CylinderGeometry(.018,.028,.30,12),metal);
 nozzle.rotation.x=Math.PI/2;nozzle.position.set(i*.72,.36,5.96);root.add(nozzle);
 }
 const detail=createFlowDetail({parent:flow,size});
 let saved;
 return {setEnabled(on){root.visible=on;if(on){saved={environmentIntensity:scene.environmentIntensity,lightsVisible:studioLights?.visible,background:scene.background,fog:scene.fog,color:studio.floor.material.color.clone()};if(studioLights)studioLights.visible=false;scene.environmentIntensity=.67;scene.background=new THREE.Color('#080e16');scene.fog=new THREE.Fog('#080e16',16,40);studio.floor.material.color.set('#101820');}else if(saved){scene.environmentIntensity=saved.environmentIntensity;if(studioLights)studioLights.visible=saved.lightsVisible;scene.background=saved.background;scene.fog=saved.fog;studio.floor.material.color.copy(saved.color);}},update(dt,r,invalid,reduced,settings={}){uniforms.strength.value=.060*(settings.density??1)*(settings.detail!==false&&settings.region&&settings.region!=="all"?.08:1);detail.update(dt,r,invalid,reduced,settings);roof.forEach(o=>o.visible=camera.position.y<2.85&&(settings.region!=="floor"||settings.detail===false));uniforms.turbulence.value=settings.turbulence??1;sideWall.visible=camera.position.x>-3.4;rearWall.visible=grille.visible=camera.position.z>-6.9;flow.visible=!invalid&&r.speed>0;if(!reduced&&!settings.paused)uniforms.time.value+=dt*r.speed*.08*(settings.tempo??1);flow.rotation.y=-r.yawDeg*Math.PI/180;}};
}
