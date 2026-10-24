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

test('plain laboratory metal door is neutral gray on both faces and all edges',async()=>{
 const kit=await loadDoorKit(),mesh=kit.getObjectByName('Metal_leaf') as THREE.Mesh;
 const colors=mesh.geometry.attributes.color;
 for(let i=0;i<colors.count;i++){
  expect(colors.getX(i)).toBeCloseTo(colors.getY(i),6);
  expect(colors.getY(i)).toBeCloseTo(colors.getZ(i),6);
 }
 // Bottom face is solid gray metal, rather than source floor pixels or blue core.
 mesh.updateMatrixWorld(true);
 for(const side of [-1,1]){
  const hit=new THREE.Raycaster(new THREE.Vector3(0,-.47,side),new THREE.Vector3(0,0,-side),0,2).intersectObject(mesh,true)[0];
  expect(hit).toBeTruthy();expect(colors.getX(hit.face!.a)).toBeGreaterThan(.03);
 }
});

test('meteor laboratory door has a cyan core instead of blue exposed edges',async()=>{
 const kit=await loadDoorKit(),mesh=kit.getObjectByName('Lab_leaf') as THREE.Mesh;
 mesh.updateMatrixWorld(true);
 const palette=mesh.geometry.attributes.color;
 for(let i=0;i<palette.count;i++)expect(palette.getY(i)+1e-6).toBeGreaterThanOrEqual(palette.getZ(i));
 for(const [origin,direction] of [
  [new THREE.Vector3(.7,0,0),new THREE.Vector3(-1,0,0)],
  [new THREE.Vector3(-.7,0,0),new THREE.Vector3(1,0,0)],
  [new THREE.Vector3(0,.7,0),new THREE.Vector3(0,-1,0)],
  [new THREE.Vector3(0,-.7,0),new THREE.Vector3(0,1,0)],
 ]){
  const hit=new THREE.Raycaster(origin,direction,0,1).intersectObject(mesh,true)[0];
  expect(hit).toBeTruthy();const colors=mesh.geometry.attributes.color,i=hit.face!.a;
  expect(colors.getY(i)).toBeGreaterThan(.15);
  expect(colors.getY(i)).toBeCloseTo(colors.getZ(i),5);
  expect(colors.getX(i)).toBeLessThan(.001);
 }
});
