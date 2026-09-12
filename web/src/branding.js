import * as THREE from 'three';
import {DecalGeometry} from 'three/addons/geometries/DecalGeometry.js';

// Text-only INTEIA wordmark, projected onto existing panels and attached to each moving mesh.
export function applyInteiaBranding(model, mechanics) {
  const canvas=document.createElement('canvas');canvas.width=2048;canvas.height=512;
  const ctx=canvas.getContext('2d');ctx.fillStyle='#ffffff';ctx.textAlign='center';ctx.textBaseline='middle';
  ctx.font='700 340px Arial, sans-serif';ctx.fillText('INTEIA',1024,274,1910);
  const map=new THREE.CanvasTexture(canvas);map.colorSpace=THREE.SRGBColorSpace;map.anisotropy=8;
  const material=new THREE.MeshStandardMaterial({name:'INTEIA | assinatura branca',map,roughness:.35,metalness:0,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-4});
  const decals=[];model.updateMatrixWorld(true);
  const offset=model.position;
  function project(source,origin,direction,rotation,width,height,depth){
    const record=mechanics.records.find(r=>r.source===source);if(!record)return;
    const ray=new THREE.Raycaster(new THREE.Vector3(...origin).add(offset),new THREE.Vector3(...direction));
    const hit=ray.intersectObject(record.root,true).find(h=>h.object.isMesh&&!h.object.userData.inteiaDecal);if(!hit)return;
    const geo=new DecalGeometry(hit.object,hit.point,new THREE.Euler(...rotation),new THREE.Vector3(width,height,depth));
    if(!geo.attributes.position.count){geo.dispose();return;}
    geo.applyMatrix4(hit.object.matrixWorld.clone().invert());
    const decal=new THREE.Mesh(geo,material);decal.name='INTEIA / '+source+' / '+decals.length;
    decal.userData={inteiaDecal:true,recordId:record.id};decal.renderOrder=2;decal.receiveShadow=true;
    hit.object.add(decal);decals.push(decal);
  }
  project('main_body',[2,.54,-.35],[-1,0,0],[0,Math.PI/2,0],1.0,.25,.16);
  project('main_body',[-2,.54,-.35],[1,0,0],[0,-Math.PI/2,0],1.0,.25,.16);
  project('main_body',[0,2,1.45],[0,-1,0],[-Math.PI/2,0,Math.PI/2],.62,.155,.12);
  project('rear_wing_main_part',[0,2,-2.13],[0,-1,0],[-Math.PI/2,0,0],.85,.13,.12);
  document.body.dataset.inteiaDecals=String(decals.length);
  return {decals,dispose(){decals.forEach(d=>{d.removeFromParent();d.geometry.dispose();});material.dispose();map.dispose();}};
}
