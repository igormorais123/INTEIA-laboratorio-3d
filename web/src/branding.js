import * as THREE from 'three';
import {DecalGeometry} from 'three/addons/geometries/DecalGeometry.js';

// Text-only INTEIA wordmark, projected onto existing panels and attached to each moving mesh.
export function applyInteiaBranding(model, mechanics) {
  const canvas=document.createElement('canvas'),ctx=canvas.getContext('2d');
  const font='700 300px Arial, sans-serif';ctx.font=font;
  const metrics=ctx.measureText('INTEIA'),padding=32;
  canvas.width=Math.ceil(metrics.width+padding*2);
  canvas.height=Math.ceil(metrics.actualBoundingBoxAscent+metrics.actualBoundingBoxDescent+padding*2);
  ctx.font=font;ctx.fillStyle='#ffffff';ctx.textBaseline='alphabetic';
  ctx.fillText('INTEIA',padding,padding+metrics.actualBoundingBoxAscent);
  const aspect=canvas.width/canvas.height;
  const map=new THREE.CanvasTexture(canvas);map.colorSpace=THREE.SRGBColorSpace;map.anisotropy=8;
  const material=new THREE.MeshStandardMaterial({name:'INTEIA | assinatura branca',map,roughness:.35,metalness:0,transparent:true,depthWrite:false,polygonOffset:true,polygonOffsetFactor:-4});
  const decals=[];model.updateMatrixWorld(true);
  const offset=model.position;
  function project(source,origin,direction,rotation,width,depth){
    const record=mechanics.records.find(r=>r.source===source);if(!record)return;
    const ray=new THREE.Raycaster(new THREE.Vector3(...origin).add(offset),new THREE.Vector3(...direction));
    const hit=ray.intersectObject(record.root,true).find(h=>h.object.isMesh&&!h.object.userData.inteiaDecal);if(!hit)return;
    const geo=new DecalGeometry(hit.object,hit.point,new THREE.Euler(...rotation),new THREE.Vector3(width,width/aspect,depth));
    if(!geo.attributes.position.count){geo.dispose();return;}
    geo.applyMatrix4(hit.object.matrixWorld.clone().invert());
    const decal=new THREE.Mesh(geo,material);decal.name='INTEIA / '+source+' / '+decals.length;
    decal.userData={inteiaDecal:true,recordId:record.id};decal.renderOrder=2;decal.receiveShadow=true;
    hit.object.add(decal);decals.push(decal);
  }
  project('main_body',[2,.32,-.55],[-1,0,0],[0,Math.PI/2,0],.90,.5);
  project('main_body',[-2,.32,-.55],[1,0,0],[0,-Math.PI/2,0],.90,.5);
  project('main_body',[0,2,1.75],[0,-1,0],[-Math.PI/2,0,Math.PI/2],.36,.25);
  // Keep the wordmarks outside the central wing supports.
  project('rear_wing_main_part',[.32,2,-2.13],[0,-1,0],[-Math.PI/2,0,0],.36,.15);
  project('rear_wing_main_part',[-.32,2,-2.13],[0,-1,0],[-Math.PI/2,0,0],.36,.15);
  document.body.dataset.inteiaDecals=String(decals.length);
  return {decals,dispose(){decals.forEach(d=>{d.removeFromParent();d.geometry.dispose();});material.dispose();map.dispose();}};
}
