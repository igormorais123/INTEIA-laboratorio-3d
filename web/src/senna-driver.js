import * as THREE from 'three';
import {RoundedBoxGeometry} from 'three/addons/geometries/RoundedBoxGeometry.js';
import {createHelmet1991} from './helmet-1991.js';

// Seated study fitted to the actual steering grips: x ±.088, y .591, z .521.
export function createSennaDriver(model, mechanics) {
 const root=new THREE.Group();root.name='Piloto · postura de cockpit';model.add(root);
 const body=new THREE.Group();body.name='Macacão, luvas e botas';root.add(body);
 const geometries=[],materials=[],textures=[];
 const mat=(name,options)=>{const m=new THREE.MeshPhysicalMaterial({name,...options});materials.push(m);return m;};
 const canvas=document.createElement('canvas');canvas.width=canvas.height=256;const ctx=canvas.getContext('2d');ctx.fillStyle='#888';ctx.fillRect(0,0,256,256);
 for(let i=0;i<256;i+=4){ctx.fillStyle='#999';ctx.fillRect(i,0,1,256);ctx.fillStyle='#777';ctx.fillRect(0,i,256,1);}
 const weave=new THREE.CanvasTexture(canvas);weave.wrapS=weave.wrapT=THREE.RepeatWrapping;weave.repeat.set(9,14);textures.push(weave);
 const suit=mat('Tecido do macacão',{color:'#8f1325',roughness:.93,bumpMap:weave,bumpScale:.00032});
 const stretch=mat('Painéis elásticos',{color:'#600f1a',roughness:1,bumpMap:weave,bumpScale:.0002});
 const seam=mat('Costuras',{color:'#b4484f',roughness:.9});
 const gloves=mat('Luvas de competição',{color:'#ddd7c8',roughness:.9,bumpMap:weave,bumpScale:.00018});
 const black=mat('Cintos e sola',{color:'#131619',roughness:.84});
 const silver=mat('Fecho do cinto',{color:'#929b9c',metalness:.85,roughness:.31});
 function mesh(name,g,m,parent=body){geometries.push(g);const o=new THREE.Mesh(g,m);o.name=name;o.castShadow=true;o.receiveShadow=true;parent.add(o);return o;}
 const V=a=>new THREE.Vector3(...a);
 // Continuous fabric surfaces with changing cross-sections and restrained folds.
 function loft(name,points,widths,depths,material,fold=.001){
  const curve=new THREE.CatmullRomCurve3(points.map(V)),n=48,sides=32,positions=[],uv=[],indices=[],up=new THREE.Vector3(1,0,0);
  for(let j=0;j<=n;j++){
   const t=j/n,p=curve.getPoint(t),tangent=curve.getTangent(t),side=up.clone().addScaledVector(tangent,-up.dot(tangent)).normalize(),front=new THREE.Vector3().crossVectors(side,tangent).normalize();
   const index=Math.min(widths.length-2,Math.floor(t*(widths.length-1))),f=t*(widths.length-1)-index,w=THREE.MathUtils.lerp(widths[index],widths[index+1],f),d=THREE.MathUtils.lerp(depths[index],depths[index+1],f);
   for(let i=0;i<=sides;i++){const a=i/sides*Math.PI*2,wrinkle=fold*Math.sin(t*65+a*3)*Math.pow(Math.sin(Math.PI*t),2),v=p.clone().addScaledVector(side,Math.cos(a)*(w+wrinkle)).addScaledVector(front,Math.sin(a)*(d+wrinkle));positions.push(v.x,v.y,v.z);uv.push(i/sides,t);}
  }
  for(let j=0;j<n;j++)for(let i=0;i<sides;i++){const a=j*(sides+1)+i,b=a+sides+1;indices.push(a,b,a+1,a+1,b,b+1);}
  for(const end of [0,n]){const center=curve.getPoint(end/n),k=positions.length/3;positions.push(center.x,center.y,center.z);uv.push(.5,end/n);for(let i=0;i<sides;i++){const a=end*(sides+1)+i;if(end===0)indices.push(k,a,a+1);else indices.push(k,a+1,a);}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(positions,3));g.setAttribute('uv',new THREE.Float32BufferAttribute(uv,2));g.setIndex(indices);g.computeVertexNormals();return mesh(name,g,material);
 }
 function piping(name,points,r,material=seam){return mesh(name,new THREE.TubeGeometry(new THREE.CatmullRomCurve3(points.map(V)),48,r,6,false),material);}
 function rounded(name,dimensions,position,material){const o=mesh(name,new RoundedBoxGeometry(...dimensions,4,Math.min(...dimensions)*.22),material);o.position.set(...position);return o;}
 loft('Tronco reclinado',[[0,.355,.48],[0,.398,.39],[0,.481,.25],[0,.558,.135],[0,.595,.115]],[.083,.101,.113,.131,.077],[.064,.072,.085,.074,.048],suit,.0015);
 loft('Gola',[[0,.577,.108],[0,.616,.084],[0,.644,.082]],[.070,.064,.056],[.045,.043,.04],stretch,.0003);
 const chestCurve=new THREE.CatmullRomCurve3([[0,.355,.48],[0,.398,.39],[0,.481,.25],[0,.558,.135],[0,.595,.115]].map(V));
 function chest(t,x){const p=chestCurve.getPoint(t),tan=chestCurve.getTangent(t),front=new THREE.Vector3().crossVectors(new THREE.Vector3(1,0,0),tan).normalize(),ws=[.083,.101,.113,.131,.077],ds=[.064,.072,.085,.074,.048],i=Math.min(3,Math.floor(t*4)),f=t*4-i,w=THREE.MathUtils.lerp(ws[i],ws[i+1],f),d=THREE.MathUtils.lerp(ds[i],ds[i+1],f);p.x=x;p.addScaledVector(front,d*Math.sqrt(Math.max(0,1-(x/w)**2))+.003);return p.toArray();}
 piping('Zíper',Array.from({length:20},(_,i)=>chest(.08+.86*i/19,0)),.0012,silver);
 for(const side of [-1,1]){
  const p=a=>[a[0]*side,a[1],a[2]];
  loft('Manga '+side,[p([.113,.555,.145]),p([.132,.526,.216]),p([.131,.466,.318]),p([.111,.516,.411]),p([.087,.565,.494])],[.052,.048,.041,.037,.027],[.052,.048,.035,.032,.024],suit,.0013);
  piping('Costura da manga '+side,[p([.146,.57,.15]),p([.17,.511,.234]),p([.159,.464,.326]),p([.136,.52,.419]),p([.109,.561,.493])],.0008);
  loft('Perna '+side,[p([.066,.356,.465]),p([.066,.389,.659]),p([.073,.475,.87]),p([.07,.459,1.05]),p([.064,.403,1.28])],[.062,.059,.045,.036,.029],[.061,.062,.048,.04,.032],suit,.0014);
  piping('Costura da perna '+side,[p([.109,.354,.49]),p([.123,.40,.675]),p([.115,.476,.87]),p([.101,.454,1.10]),p([.092,.405,1.28])],.0009);
  loft('Bota '+side,[p([.064,.403,1.25]),p([.063,.435,1.30]),p([.062,.463,1.355]),p([.062,.466,1.422])],[.028,.036,.036,.025],[.032,.039,.032,.018],stretch,.0003);
  rounded('Sola '+side,[.071,.011,.185],p([.062,.409,1.354]),black).rotation.x=-.32;
  for(let i=0;i<4;i++)piping('Costura da bota '+side+' '+i,[p([.038,.466,1.31+i*.022]),p([.061,.473,1.314+i*.022]),p([.084,.466,1.31+i*.022])],.0008);
  rounded('Palma da luva '+side,[.042,.063,.025],p([.088,.586,.50]),gloves).rotation.z=-side*.10;
  for(let i=0;i<4;i++){const y=.565+i*.014;piping('Dedo '+side+' '+i,[p([.105,y,.50]),p([.111,y,.518]),p([.099,y,.539]),p([.084,y,.540])],.0061,gloves);}
  piping('Polegar '+side,[p([.073,.602,.49]),p([.061,.584,.511]),p([.069,.574,.525])],.008,gloves);
  rounded('Punho '+side,[.052,.027,.033],p([.087,.555,.492]),stretch);
 }
 function ribbon(name,points,width){const curve=new THREE.CatmullRomCurve3(points.map(V)),vertices=[],idx=[];
  for(let j=0;j<=32;j++){const p=curve.getPoint(j/32);vertices.push(p.x-width/2,p.y,p.z,p.x+width/2,p.y,p.z);if(j<32){const a=j*2;idx.push(a,a+1,a+2,a+1,a+3,a+2);}}
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(vertices,3));g.setIndex(idx);g.computeVertexNormals();const m=black.clone();m.side=THREE.DoubleSide;materials.push(m);return mesh(name,g,m);
 }
 for(const side of [-1,1]){
  ribbon('Cinto do ombro '+side,Array.from({length:16},(_,i)=>chest(.91-.76*i/15,side*(.061-.04*i/15))),.025);
  ribbon('Cinto abdominal '+side,[chest(.14,side*.082),chest(.15,side*.05),chest(.15,side*.01)],.029);
 }
 rounded('Fecho central',[.038,.025,.013],chest(.15,0),silver).rotation.x=-.55;
 const helmet=createHelmet1991({detail:96});helmet.root.scale.setScalar(.84);root.add(helmet.root);
 const fit={height:0,foreAft:0,pitch:0};
 function applyFit(){helmet.root.position.set(0,.653+fit.height,.068+fit.foreAft);helmet.root.rotation.set(.14+fit.pitch,0,0);}
 applyFit();
 root.userData.references=['https://www.mercedesamgf1.com/news/onwards-to-bahrain-w14-completes-initial-running','https://commons.wikimedia.org/wiki/Category:Helmets_of_Ayrton_Senna_in_1991'];
 return {root,body,helmet,fit,setFit(values){Object.assign(fit,values);applyFit();},update(){root.visible=mechanics.motionAvailable&&!mechanics.isolated;},dispose(){root.removeFromParent();helmet.dispose();geometries.forEach(g=>g.dispose());materials.forEach(m=>m.dispose());textures.forEach(t=>t.dispose());}};
}
