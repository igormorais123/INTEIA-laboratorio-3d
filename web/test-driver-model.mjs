import assert from 'node:assert/strict';
import * as THREE from 'three';
import {createSennaDriver} from './src/senna-driver.js';
// Canvas rasterization is reviewed in the browser; this test validates geometry and fit.
const context=new Proxy({createImageData:(w,h)=>({data:new Uint8ClampedArray(w*h*4)})},{get:(o,k)=>k in o?o[k]:()=>{}});
globalThis.document={createElement:()=>({width:1,height:1,getContext:()=>context})};
const model=new THREE.Group(),mechanics={motionAvailable:true,isolated:false},driver=createSennaDriver(model,mechanics);
model.updateMatrixWorld(true);const box=new THREE.Box3().setFromObject(driver.helmet.root),rest=driver.helmet.root.position.clone();
assert.ok(box.max.y<.90&&box.min.y>.45,'Capacete fora da faixa de encaixe revisada');
assert.ok(driver.root.getObjectByName('Perna -1')&&driver.root.getObjectByName('Perna 1'));
assert.ok(driver.root.getObjectByName('Cinto do ombro 1')&&driver.root.getObjectByName('Fecho central'));
let meshes=0,vertices=0;driver.root.traverse(o=>{if(!o.isMesh)return;meshes++;for(const key of ['position','normal']){const a=o.geometry.attributes[key];for(const value of a.array)assert.ok(Number.isFinite(value),'Geometria invalida');}vertices+=o.geometry.attributes.position.count;});
for(let i=0;i<20;i++){driver.setFit({height:.015,foreAft:-.015,pitch:.1});driver.setFit({height:0,foreAft:0,pitch:0});}
assert.equal(driver.helmet.root.position.distanceTo(rest),0);
mechanics.isolated=true;driver.update();assert.equal(driver.root.visible,false);mechanics.isolated=false;driver.update();assert.equal(driver.root.visible,true);
console.log({pilot:true,helmet:true,meshes,vertices,fitCycles:20,drift:0});driver.dispose();

