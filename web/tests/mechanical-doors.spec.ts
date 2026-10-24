import {test,expect} from '@playwright/test';
import * as THREE from 'three';
import {loadDoorKit} from './shared-fixture';

test('mechanical doors have distinct solid relief levels on both faces',async()=>{
 const kit=await loadDoorKit();kit.updateMatrixWorld(true);
 for(const [name,center,base,minProjection] of [
  ['Security_leaf',.2,.115,.17],['Dungeon_leaf',0,.041,.13],
  ['Lab_leaf',0,.041,.14],['Metal_leaf',0,.041,.085],
  ['Dungeon_reinforced_leaf',0,.041,.06],
 ] as const){
  const mesh=kit.getObjectByName(name) as THREE.Mesh,p=mesh.geometry.attributes.position;
  mesh.geometry.computeBoundingBox();const box=mesh.geometry.boundingBox!;
  expect(box.max.z-center-base,name+' front relief').toBeGreaterThan(minProjection);
  expect(center-box.min.z-base,name+' back relief').toBeGreaterThan(minProjection);
  expect(box.max.z-center).toBeCloseTo(center-box.min.z,5);
  const depths=new Set();for(let i=0;i<p.count;i++)depths.add(Math.round((p.getZ(i)-center)*1000));
  expect(depths.size,name+' separate cases, seams and bars').toBeGreaterThan(5);
 }
});

test('security bars and wheel project beyond the underlying door panel',async()=>{
 const kit=await loadDoorKit(),mesh=kit.getObjectByName('Security_leaf')!;mesh.updateMatrixWorld(true);
 const height=89*1.8/66*1.2;
 for(const side of [-1,1])for(const [u,v,min] of [[.2,.22,.15],[.5,.33,.19],[.42,.60,.23]]){
  const origin=new THREE.Vector3(-.9+u*1.8,.03+(1-v)*height,.2+side*1);
  const hit=new THREE.Raycaster(origin,new THREE.Vector3(0,0,-side),0,2).intersectObject(mesh,true)[0];
  expect(hit).toBeTruthy();expect(Math.abs(hit.point.z-.2)).toBeGreaterThan(min);
 }
});
