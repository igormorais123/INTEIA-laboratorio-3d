import {glyphs} from './identity.js';
import * as THREE from 'three';
import {DecalGeometry} from 'three/addons/geometries/DecalGeometry.js';

// One outlined INTEIA signature on the right sidepod, attached to the moving body.
export function applyInteiaBranding(model, mechanics) {
  const canvas=document.createElement('canvas');canvas.width=1536;canvas.height=320;
  const ctx=canvas.getContext('2d');ctx.scale(3.6,3.6);ctx.translate(29,12);
  ctx.transform(1,0,-Math.tan(12*Math.PI/180),1,0,0);ctx.fillStyle='#f5f5f2';
  for(const [,path] of glyphs)ctx.fill(new Path2D(path),'evenodd');
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
  project('main_body',[2,.32,-.55],[-1,0,0],[0,Math.PI/2,0],.76,.22);
  document.body.dataset.inteiaDecals=String(decals.length);
  return {decals,dispose(){decals.forEach(d=>{d.removeFromParent();d.geometry.dispose();});material.dispose();map.dispose();}};
}
