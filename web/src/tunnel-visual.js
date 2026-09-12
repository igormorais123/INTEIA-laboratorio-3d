import * as THREE from 'three';
// Art-directed smoke paths: a visual envelope, not a CFD solution.
export function createTunnelVisual({scene, size, studio, camera}) {
 const root=new THREE.Group();root.name='Wind tunnel visual chamber';root.visible=false;scene.add(root);
 const metal=new THREE.MeshStandardMaterial({color:0x222d37,metalness:.7,roughness:.36});
 const dark=new THREE.MeshStandardMaterial({color:0x131b22,metalness:.3,roughness:.58});
 const light=new THREE.MeshBasicMaterial({color:0xccefff});
 function box(w,h,d,x,y,z,mat=metal){const m=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),mat);m.position.set(x,y,z);m.receiveShadow=true;root.add(m);return m;}
 box(7,.12,14,0,-.08,0,dark);
 box(2.6,.025,12,0,-.005,0,new THREE.MeshStandardMaterial({color:0x30383d,roughness:.5,metalness:.25}));
 for(const x of [-3.3,3.3]){box(.1,.16,14,x,.06,0);box(.018,.012,13,x,.16,0,new THREE.MeshBasicMaterial({color:0x59717d}));}
 for(const z of [-6,-3,0,3,6]){box(.08,2.85,.1,-3.4,1.40,z);box(6.8,.08,.1,0,2.85,z);box(5.8,.018,.04,0,2.79,z,light);}
 const sideWall=box(.08,3.8,14,-3.46,1.85,0,dark);
 const rearWall=box(6.9,3.8,.12,0,1.85,-7,dark);
 const grille=new THREE.LineSegments(new THREE.BufferGeometry(),new THREE.LineBasicMaterial({color:0x4c6373,transparent:true,opacity:.18}));
 const gp=[];for(let x=-3.3;x<=3.3;x+=.16)gp.push(x,0,-6.92,x,3.7,-6.92);for(let y=0;y<3.8;y+=.16)gp.push(-3.3,y,-6.92,3.3,y,-6.92);grille.geometry.setAttribute('position',new THREE.Float32BufferAttribute(gp,3));root.add(grille);
 const lamp=new THREE.PointLight(0xbadfff,12,12,2);lamp.position.set(0,3,0);root.add(lamp);
 const uniforms={time:{value:0},strength:{value:.17},turbulence:{value:1}};
 const smokeMat=new THREE.ShaderMaterial({transparent:true,depthWrite:false,side:THREE.DoubleSide,uniforms,vertexShader:`varying vec2 vUv;void main(){vUv=uv;gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}`,fragmentShader:`varying vec2 vUv;uniform float time;uniform float strength;void main(){float edge=pow(sin(vUv.y*3.14159),3.8);float pulse=.6+.15*sin(vUv.x*32.-time*3.)+.10*sin(vUv.x*73.-time*3.1);float ends=smoothstep(0.,.04,vUv.x)*(1.-smoothstep(.88,1.,vUv.x));gl_FragColor=vec4(.74,.86,.92,edge*pulse*ends*strength);}`});
 const flow=new THREE.Group();root.add(flow);
 for(let lane=0;lane<11;lane++){
 const x=(lane%6-3)*.5,y=.30+Math.floor(lane/6)*.65;
 const positions=[],uv=[],indices=[],steps=170;
 for(let j=0;j<=steps;j++){const t=j/steps,z=6-t*12,near=Math.exp(-Math.pow(z/2.2,4));const px=x+Math.sign(x||.01)*near*Math.exp(-y)*.65,py=y+near*Math.exp(-x*x/.8)*.48;
 for(let k=0;k<2;k++){positions.push(px,py+(k-.5)*.075,z);uv.push(t,k);}if(j<steps){const a=j*2;indices.push(a,a+1,a+2,a+1,a+3,a+2);}}
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));geo.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));geo.setIndex(indices);const mesh=new THREE.Mesh(geo,smokeMat);mesh.frustumCulled=false;flow.add(mesh);
 }

 // Soft camera-facing smoke puffs provide depth; seeded layout is reproducible.
 const puffGeo=new THREE.BufferGeometry(),puffData=[];
 for(let i=0;i<2400;i++)puffData.push((i*.61803398875)%1,(i*.754877666)%1,(i*.569840296)%1);
 puffGeo.setAttribute('position',new THREE.Float32BufferAttribute(puffData,3));
 const puffMaterial=new THREE.ShaderMaterial({transparent:true,depthWrite:false,uniforms,vertexShader:`
 uniform float time;uniform float turbulence;varying float fade;varying float seed;
 void main(){seed=position.z;float t=fract(position.x+time*.027);float z=6.-12.*t;
 float lane=floor(position.y*7.);float x=(lane-3.)*.48;float y=.4+mod(lane,2.)*.43;
 float near=exp(-pow(z/2.2,4.));x+=sign(x+.001)*near*.5;y+=near*exp(-x*x/.8)*.45;
 float wake=smoothstep(1.8,4.5,-z);float theta=z*5.+position.z*6.283-time*.6;
 x+=wake*sin(theta)*(.13+position.z*.2)*turbulence;y+=wake*cos(theta)*.17*turbulence;
 vec4 mv=modelViewMatrix*vec4(x,y,z,1.);gl_Position=projectionMatrix*mv;
 gl_PointSize=clamp((.24+wake*.85)*650./(-mv.z),1.,180.);
 fade=smoothstep(0.,.04,t)*(1.-smoothstep(.8,1.,t))*wake*.014;
 }`,fragmentShader:`varying float fade;varying float seed;uniform float strength;
 void main(){vec2 p=gl_PointCoord-.5;float r=length(p)*2.;float a=exp(-r*r*5.)*(1.-smoothstep(.55,1.,r));gl_FragColor=vec4(.68,.79,.85,a*fade*strength*4.);}`});
 const puffs=new THREE.Points(puffGeo,puffMaterial);puffs.frustumCulled=false;flow.add(puffs);
 let saved;
 return {setEnabled(on){root.visible=on;if(on){saved={background:scene.background,fog:scene.fog,color:studio.floor.material.color.clone()};scene.background=new THREE.Color('#080e16');scene.fog=new THREE.Fog('#080e16',16,40);studio.floor.material.color.set('#101820');}else if(saved){scene.background=saved.background;scene.fog=saved.fog;studio.floor.material.color.copy(saved.color);}},update(dt,r,invalid,reduced,settings={}){uniforms.strength.value=.17*(settings.density??1);uniforms.turbulence.value=settings.turbulence??1;sideWall.visible=camera.position.x>-3.4;rearWall.visible=grille.visible=camera.position.z>-6.9;flow.visible=!invalid&&r.speed>0;if(!reduced&&!settings.paused)uniforms.time.value+=dt*r.speed*.08*(settings.tempo??1);flow.rotation.y=-r.yawDeg*Math.PI/180;}};
}
