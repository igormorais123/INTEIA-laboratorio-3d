import * as THREE from 'three';

// Explanatory paths shaped to the model envelope, not measured streamlines.
export function createFlowDetail({parent,size}) {
 const root=new THREE.Group();root.name='Illustrative flow detail';parent.add(root);
 const W=size.x*.5,L=size.z*.5,H=size.y;
 const colors={body:0xa6d8e7,wheels:0xe8ba79,floor:0x9bddc7};
 const paths=[];
 function path(points,category){paths.push({curve:new THREE.CatmullRomCurve3(points.map(p=>new THREE.Vector3(...p))),category});}
 for(const sign of [-1,1]){
  for(let row=0;row<3;row++){
   const x=sign*(W*.51+row*.085),y=H*(.24+row*.11);
   path([[x,y,L+2.3],[x,y,L+ .4],[sign*W*.95,y+.10,L*.68],[sign*W*.92,y+.12,0],[sign*W*.78,y+.10,-L*.72],[sign*W*.88,y+.2,-L-1],[sign*W*.94,y+.16,-L-2.3]],'body');
  }
  // Paired, gradually expanding curls downstream of each rear wheel.
  for(let strand=0;strand<3;strand++){
   const points=[];
   for(let i=0;i<=70;i++){
    const t=i/70,z=-L*.62-t*3.0,r=.025+t*.18;
    const angle=t*14+strand*2.094;
    points.push([sign*(W*.79+Math.sin(angle)*r),H*.25+Math.cos(angle)*r+t*.1,z]);
   }path(points,'wheels');
  }
  for(let row=0;row<2;row++){
   const x=sign*W*(.27+row*.18);
   path([[x,.07,L+1.4],[x,.07,L*.65],[x,.075,0],[x,.11,-L*.63],[x*1.25,.30,-L],[x*1.6,.42,-L-1.5]],'floor');
  }
 }
 for(let row=0;row<3;row++){
  const x=(row-1)*W*.2;
  path([[x,H*.34,L+2.3],[x,H*.34,L*.97],[x,H*.45,L*.5],[x,H*1.02,.15],[x,H*1.04,-L*.62],[x,H*.99,-L],[x*1.4,H*.85,-L-2.2]],'body');
 }
 const segments=90,trailSteps=7,packets=8;
 const basePositions=[],baseColors=[];
 for(const p of paths){p.samples=p.curve.getSpacedPoints(500);const color=new THREE.Color(colors[p.category]);for(let j=0;j<segments;j++){for(const t of [j/segments,(j+1)/segments]){const q=p.curve.getPoint(t);basePositions.push(q.x,q.y,q.z);baseColors.push(color.r,color.g,color.b,1);}}}
 const baseGeo=new THREE.BufferGeometry();baseGeo.setAttribute('position',new THREE.Float32BufferAttribute(basePositions,3));baseGeo.setAttribute('color',new THREE.Float32BufferAttribute(baseColors,4));
 const base=new THREE.LineSegments(baseGeo,new THREE.LineBasicMaterial({vertexColors:true,transparent:true,opacity:.26,depthWrite:false}));root.add(base);
 const positions=new Float32Array(paths.length*packets*trailSteps*6),colours=new Float32Array(positions.length/3*4);
 const geo=new THREE.BufferGeometry();geo.setAttribute('position',new THREE.BufferAttribute(positions,3).setUsage(THREE.DynamicDrawUsage));geo.setAttribute('color',new THREE.BufferAttribute(colours,4).setUsage(THREE.DynamicDrawUsage));
 const material=new THREE.LineBasicMaterial({vertexColors:true,transparent:true,opacity:.95,depthWrite:false});
 const trails=new THREE.LineSegments(geo,material);trails.frustumCulled=false;root.add(trails);
 const cones=[];const coneGeometry=new THREE.ConeGeometry(.024,.095,8);const coneMaterials=Object.fromEntries(Object.entries(colors).map(([k,color])=>[k,new THREE.MeshBasicMaterial({color,transparent:true,opacity:.85})]));
 for(const p of paths)for(const t of [.32,.73]){const cone=new THREE.Mesh(coneGeometry,coneMaterials[p.category]);cone.position.copy(p.curve.getPoint(t));cone.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0),p.curve.getTangent(t).normalize());root.add(cone);cones.push({cone,category:p.category});}
 const q=new THREE.Vector3();let phase=0;
 function sample(p,t){const f=THREE.MathUtils.clamp(t,0,1)*500,i=Math.min(499,Math.floor(f));return q.lerpVectors(p.samples[i],p.samples[i+1],f-i);}
 return {update(dt,r,invalid,reduced,settings){root.visible=!invalid&&r.speed>0&&settings.detail!==false;if(!root.visible)return;if(!reduced&&!settings.paused)phase+=dt*r.speed*.004*(settings.tempo??1);
  const selected=settings.region||'all';cones.forEach(({cone,category})=>cone.visible=selected==='all'||selected===category);base.visible=true;let at=0,ci=0;
  paths.forEach((p,pi)=>{const color=new THREE.Color(colors[p.category]),shown=selected==='all'||selected===p.category;for(let i=0;i<segments*2;i++)baseGeo.attributes.color.array[(pi*segments*2+i)*4+3]=shown?1:0;
   for(let k=0;k<packets;k++){const head=(k/packets+phase+pi*.137)%1;
    for(let j=0;j<trailSteps;j++)for(let e=0;e<2;e++){
     const t=head-(j+e)*.006,pt=sample(p,Math.max(0,t));const fade=shown&&t>=0?(1-j/trailSteps)*.85:0;
     positions[at]=pt.x;positions[at+1]=pt.y;positions[at+2]=pt.z;
     colours[ci++]=color.r;colours[ci++]=color.g;colours[ci++]=color.b;colours[ci++]=fade;at+=3;
    }
   }
  });baseGeo.attributes.color.needsUpdate=true;geo.attributes.position.needsUpdate=true;geo.attributes.color.needsUpdate=true;
 }};
}
