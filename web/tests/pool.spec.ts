import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {addDoorKit} from './shared-fixture';
import {createDoorView} from '../lib/house/door-view';
const safe={x:0,y:1,height:0};
test('pool doorway starts closed, opens both ways, and waits for the deck asset',()=>{
 const v=createHouseRuntime('pool');expect(v.zoneAt(v.START)).toBe('Pool deck');expect(v.navigation.canStand(v.START,0)).toBe(true);
 const inside={x:-4.87,y:40.9,height:0},outside={x:-7.87,y:40.9,height:0};
 v.activate('pantry');expect(v.moveWalker(inside,-3,0).x).toBeGreaterThan(-6.37);v.activate('pool');expect(v.moveWalker(outside,3,0).x).toBeLessThan(-6.37);
 v.doors.toggle('pantry:pool_door');v.doors.update(1,safe);
 v.activate('pantry');expect(v.moveWalker(inside,-3,0).x).toBeCloseTo(outside.x);v.activate('pool');expect(v.moveWalker(outside,3,0).x).toBeCloseTo(inside.x);
 v.requireLoadedRooms();v.setRoomLoaded('pantry',true);expect(v.moveWalker(inside,-3,0).x).toBeGreaterThan(-6.5);
 v.setRoomLoaded('pool',true);expect(v.moveWalker(inside,-3,0).x).toBeCloseTo(outside.x);
});
test('deck circuit is continuous while water, fences and ladder stay solid',()=>{
 const v=createHouseRuntime('pool'),room=v.rooms.find(r=>r.id==='pool')!;
 const at=(x:number,y:number)=>toWorld({x,y,height:0},room);let pos=at(2,3.2);
 for(const q of [at(2,1),at(18.5,1),at(18.5,9.7),at(2,9.7),at(2,3.2)]){
  pos=v.moveWalker(pos,q.x-pos.x,q.y-pos.y);expect(Math.hypot(pos.x-q.x,pos.y-q.y)).toBeLessThan(.03);expect(pos.height).toBe(0);
 }
 for(const q of [at(8,5),at(8,11.3),at(11,8.6),at(8,-.2)])expect(v.navigation.canStand(q,0)).toBe(false);
 const fence=v.moveWalker(at(18.5,2),-3,0);expect(fence.x).toBeGreaterThan(at(20,2).x);
 const edge=v.moveWalker(at(3,5),-6,0);expect(edge.x).toBeGreaterThan(at(5,5).x);
 expect(v.navigation.canStand(at(2,3),-2.8)).toBe(false);
});
test('actual shared door blocks the sightline when closed and leaves a clear passage when open',async()=>{
 const v=createHouseRuntime(),scene=new THREE.Scene(),visual=createDoorView(scene,v.doors);
 for(const room of v.rooms.filter(r=>['pantry','pool'].includes(r.id))){
  const def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');await addDoorKit(gltf.scene,def);
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);visual.attach(room.id,root);
 }
 const door=v.doors.items.find(d=>d.key==='pantry:pool_door')!,camera=new THREE.PerspectiveCamera(68,1,.05,60),ray=new THREE.Raycaster();
 for(const amount of [0,1]){
  door.amount=amount;door.target=amount;visual.sync();scene.updateMatrixWorld(true);
  for(const [x,dir] of [[-4.87,-1],[-7.87,1]]){
   camera.position.set(x,1.62,-40.9);camera.lookAt(-6.37,1.62,-40.9);camera.updateMatrixWorld(true);expect(visual.target(camera)?.key).toBe(door.key);
   ray.set(camera.position,new THREE.Vector3(dir,0,0));ray.far=1.9;const hits=ray.intersectObjects(scene.children,true);
   if(amount===1)expect(hits).toHaveLength(0);else expect(hits[0]?.object.userData.doorKey).toBe(door.key);
  }
 }
});
