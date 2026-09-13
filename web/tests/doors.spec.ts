import {addDoorKit} from './shared-fixture';
import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createHouseRuntime} from '../lib/house/runtime';
import {createDoorView} from '../lib/house/door-view';
import {toWorld} from '../lib/house/placement';

const safe={x:0,y:1,height:0};
test('single and double doors block the passage when shut, and reopen from either side',()=>{
 for(const [id,start,end] of [
  ['living_door',{x:5,y:3.15,height:0},{x:8,y:3.15,height:0}],
  ['front_doors',{x:-5,y:2.35,height:0},{x:-8,y:2.35,height:0}],
 ] as const){
  const v=createHouseRuntime('hall'),key='hall:'+id;
  const cross=(a:typeof safe,b:typeof safe)=>{
   v.activate(a===start?'hall':id==='living_door'?'living_room':'front_exterior');
   return v.moveWalker(a,b.x-a.x,b.y-a.y);
  };
  expect(v.doors.items.find(d=>d.key===key)!.target).toBe(0);
  expect(v.doors.items.find(d=>d.key===key)!.amount).toBe(0);
  expect(Math.abs(cross(start,end).x-end.x)).toBeGreaterThan(1);
  expect(Math.abs(cross(end,start).x-start.x)).toBeGreaterThan(.5);
  v.doors.toggle(key);v.doors.update(1,safe);
  expect(cross(start,end).x).toBeCloseTo(end.x);
  expect(cross(end,start).x).toBeCloseTo(start.x);
 }
});
test('swing pauses before the walker, resumes after stepping back, and can reverse',()=>{
 const v=createHouseRuntime('hall'),door=v.doors.items.find(d=>d.def.id==='living_door')!;
 v.doors.toggle(door.key);v.doors.update(1,safe);
 const walker={x:5.8,y:3.15,height:0};expect(v.navigation.canStand(walker,0)).toBe(true);
 v.doors.toggle(door.key);v.doors.update(1,walker);
 expect(door.blocked).toBe(true);expect(door.amount).toBeGreaterThan(0);
 expect(v.navigation.canStand(walker,0)).toBe(true);
 v.doors.update(1,safe);expect(door.amount).toBe(0);
 v.doors.toggle(door.key);v.doors.update(.2,safe);expect(door.amount).toBeGreaterThan(0);expect(door.amount).toBeLessThan(1);
 v.doors.toggle(door.key);v.doors.update(1,safe);expect(door.amount).toBe(0);
});
test('door state survives unloading and its collision respects room rotation and floor',()=>{
 const v=createHouseRuntime('hall'),door=v.doors.items[0];
 v.requireLoadedRooms();v.setRoomLoaded('hall',true);v.setRoomLoaded('hall',false);v.setRoomLoaded('hall',true);
 expect(door.amount).toBe(0);
 // Mutate this instance placement only for this isolated runtime.
 const saved={...door.room,position:[...door.room.position]};
 try{
  door.room.position=[12,-8,4];door.room.yaw=Math.PI/2;
  const p=toWorld({x:5.96,y:3.15,height:0},door.room);
  expect(v.doors.blocks(p)).toBe(true);expect(v.doors.blocks({...p,height:8})).toBe(false);
 }finally{Object.assign(door.room,saved);}
});
test('real compact GLB has pivoted leaves matching collision, selectable from both rooms',async()=>{
 const v=createHouseRuntime('hall'),scene=new THREE.Scene(),visual=createDoorView(scene,v.doors);
 const roots=new Map<string,THREE.Group>();
 for(const room of v.rooms){
  const filename=v.definitions[room.definition].asset.split('/').at(-1)!.replace('.glb','_compact.glb');
  const bytes=await readFile('../generated/models/rooms/'+filename);
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
  await addDoorKit(gltf.scene,v.definitions[room.definition]);
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);roots.set(room.id,root);visual.attach(room.id,root);
 }
 const camera=new THREE.PerspectiveCamera(68,1,.05,60);
 const aim=(x:number,y:number,tx:number,ty:number)=>{camera.position.set(x,1.62,-y);camera.lookAt(tx,1.45,-ty);};
 for(const door of v.doors.items){
  v.activate(door.room.id);
  for(const amount of [1,0,.5]){
   door.amount=amount;visual.sync();scene.updateMatrixWorld(true);
   for(const leaf of door.def.leaves){
    const owner=roots.get(door.room.id)!,node=owner.getObjectByName(leaf.node)!;
    const box=new THREE.Box3().setFromObject(node).applyMatrix4(owner.matrixWorld.clone().invert());expect(box.max.y).toBeCloseTo(leaf.max[2],4);
    if(amount===1){expect(box.min.x).toBeCloseTo(leaf.min[0],4);expect(-box.max.z).toBeCloseTo(leaf.min[1],4);}
    const mid=box.getCenter(new THREE.Vector3());expect(v.doors.blocks(toWorld({x:mid.x,y:-mid.z,height:leaf.min[2]},door.room))).toBe(true);
   }
  }
  door.amount=1;door.target=1;
 }
 visual.sync();
 for(const [x,y,tx,ty,key] of [[7.8,3.15,6.4,3.15,'hall:living_door'],[4.4,3.15,6.4,3.15,'hall:living_door'],[-8,2.35,-6.4,2.35,'hall:front_doors'],[-4.7,2.35,-6.4,2.35,'hall:front_doors']] as const){
  aim(x,y,tx,ty);expect(visual.target(camera)?.key).toBe(key);
  v.doors.toggle(key);v.doors.update(1,safe);visual.sync();expect(visual.target(camera)?.key).toBe(key);
 }
 aim(0,1,6.4,3.15);expect(visual.target(camera)).toBeNull();
 // An opaque obstruction must prevent interaction through a wall.
 aim(7.8,3.15,6.4,3.15);
 const wall=new THREE.Mesh(new THREE.BoxGeometry(.1,4,4),new THREE.MeshBasicMaterial());wall.position.set(7,1.5,-3.15);scene.add(wall);
 expect(visual.target(camera)).toBeNull();scene.remove(wall);wall.geometry.dispose();wall.material.dispose();
 visual.detach('hall');expect(visual.target(camera)).toBeNull();
 scene.remove(roots.get('hall')!); // As done by room unloading.
 visual.attach('hall',roots.get('hall')!);scene.add(roots.get('hall')!);
 expect(visual.target(camera)?.key).toBe('hall:living_door');
});
