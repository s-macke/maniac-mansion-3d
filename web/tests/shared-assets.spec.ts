import {test,expect} from '@playwright/test';
import * as THREE from 'three';
import {createHouseRuntime} from '../lib/house/runtime';
import {instantiateSharedAssets} from '../lib/house/shared-assets';
import {createDoorView} from '../lib/house/door-view';
import {loadDoorKit} from './shared-fixture';
import {readFile} from 'node:fs/promises';

test('all doors reuse twelve library geometries and one material, including mirrored leaves',async()=>{
 const v=createHouseRuntime(),library=await loadDoorKit(),geometry=new Set(),materials=new Set();let count=0,mirrored=0;
 const scene=new THREE.Scene(),visual=createDoorView(scene,v.doors);
 for(const room of v.rooms){
  const def=v.definitions[room.definition],root=new THREE.Group();
  instantiateSharedAssets(root,def,library);scene.add(root);visual.attach(room.id,root);root.updateMatrixWorld(true);
  root.traverse(o=>{if(o instanceof THREE.Mesh){geometry.add(o.geometry);materials.add(o.material);count+=o instanceof THREE.InstancedMesh?o.count:1;if(o.matrixWorld.determinant()<0)mirrored++;}});
  root.traverse(o=>{if(o instanceof THREE.InstancedMesh){const m=new THREE.Matrix4();for(let i=0;i<o.count;i++){o.getMatrixAt(i,m);expect(m.determinant()).toBeGreaterThan(0);}}});
  // Shared doors must not still occupy a second copy in the room GLB.
  const bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const json=JSON.parse(bytes.subarray(20,20+bytes.readUInt32LE(12)).toString());
  expect(json.nodes.some((n:{name?:string})=>n.name?.startsWith('Shared_')||n.name?.startsWith('Door_'))).toBe(false);
 }
 expect(count).toBe(v.rooms.reduce((n,r)=>n+(v.definitions[r.definition].geometry?.sharedAssets?.filter(a=>!a.library||a.library==='doors').length??0),0));expect(geometry.size).toBe(12);expect(materials.size).toBe(1);expect(mirrored).toBeGreaterThan(0);
 const door=v.doors.items.find(d=>d.def.id==='kitchen_door')!;
 expect(door.amount).toBe(0);v.doors.toggle(door.key);v.doors.update(1,{x:0,y:1,height:0});visual.sync();
 const before=scene.getObjectByName('Door_kitchen')!.rotation.y;
 visual.detach('hall');const replacement=new THREE.Group();instantiateSharedAssets(replacement,v.definitions.connected_hall,library);visual.attach('hall',replacement);
 expect(replacement.getObjectByName('Door_kitchen')!.rotation.y).toBe(before);
});

test('loader fetches the kit once, waits for it before entry, and retains it across room unloading',async()=>{
 const {GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js');
 const {createHouseAssets}=await import('../lib/house/assets');
 const v=createHouseRuntime('hall'),library=await loadDoorKit(),templates=new Map<string,THREE.Group>();
 for(const room of v.rooms){
  const def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  templates.set(def.asset,(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene);
 }
 const calls:string[]=[],original=GLTFLoader.prototype.load;let releaseKit:(()=>void)|undefined,ready=false,disposedGeometry=0;const errors:string[]=[];
 library.traverse(o=>{if(o instanceof THREE.Mesh)o.geometry.addEventListener('dispose',()=>disposedGeometry++);});
 GLTFLoader.prototype.load=function(url,onLoad){
  calls.push(url);
  if(url.includes('/shared/'))releaseKit=()=>onLoad({scene:library} as never);
  else queueMicrotask(()=>onLoad({scene:templates.get(new URL(url,'http://localhost/').pathname)!.clone(true)} as never));
 };
 const scene=new THREE.Scene(),assets=createHouseAssets(scene,{changed:()=>{},progress:()=>{},ready:()=>{ready=true;},error:m=>errors.push(m)},v);
 try{
  assets.update(v.START);await new Promise(resolve=>setTimeout(resolve,0));
  expect(ready).toBe(false);expect(v.navigation.canStand(v.START,0)).toBe(false);
  releaseKit!();await expect.poll(()=>ready).toBe(true);expect(errors).toEqual([]);
  expect(calls.filter(url=>url.includes('/shared/'))).toHaveLength(1);
  v.activate('front_exterior');assets.selectSpace(v.activeSpace);
  const camera=new THREE.PerspectiveCamera(68,1000/700,.05,60);camera.rotation.order='YXZ';camera.position.set(-8.5,1.62,-2.35);camera.rotation.set(.3,-Math.PI/2,0);
  expect(assets.doorView.target(camera)?.key).toBe('hall:front_doors');
  v.activate('hall');assets.selectSpace(v.activeSpace);
  v.doors.toggle('hall:kitchen_door');v.doors.update(1,{x:0,y:1,height:0});assets.doorView.sync();
  v.activate('arcade');assets.update(v.START,performance.now()+11000);expect(assets.loadedRooms).not.toContain('hall');expect(disposedGeometry).toBe(0);
  v.activate('hall');assets.update(v.START,performance.now()+12000);await expect.poll(()=>v.navigation.canStand(v.START,0)).toBe(true);
  expect(calls.filter(url=>url.includes('/shared/'))).toHaveLength(1);
  expect(v.doors.items.find(d=>d.def.id==='kitchen_door')!.amount).toBe(1);
  assets.dispose();await expect.poll(()=>disposedGeometry).toBe(12);
 }finally{assets.dispose();GLTFLoader.prototype.load=original;}
});


test('a failed shared kit never makes an indoor room walkable without its doors',async()=>{
 const {GLTFLoader}=await import('three/addons/loaders/GLTFLoader.js');
 const {createHouseAssets}=await import('../lib/house/assets');
 const original=GLTFLoader.prototype.load,v=createHouseRuntime('hall'),errors:string[]=[];let ready=false;
 GLTFLoader.prototype.load=function(url,onLoad,_progress,onError){
  queueMicrotask(()=>{if(url.includes('/shared/'))onError?.(new Error('Test kit failure'));else onLoad({scene:new THREE.Group()} as never);});
 };
 const assets=createHouseAssets(new THREE.Scene(),{changed:()=>{},progress:()=>{},ready:()=>{ready=true;},error:m=>errors.push(m)},v);
 try{
  assets.update(v.START);await expect.poll(()=>errors.length).toBeGreaterThan(0);
  expect(errors.every(m=>m.includes('Door assets could not load'))).toBe(true);
  expect(ready).toBe(false);expect(v.navigation.canStand(v.START,0)).toBe(false);
 }finally{assets.dispose();GLTFLoader.prototype.load=original;}
});
