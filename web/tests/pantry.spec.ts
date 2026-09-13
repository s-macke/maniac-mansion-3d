import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {addDoorKit} from './shared-fixture';
import {createDoorView} from '../lib/house/door-view';
const safe={x:0,y:1,height:0};
test('pantry connects through a closed shared door and returns to dining',()=>{
 const v=createHouseRuntime('pantry');expect(v.zoneAt(v.START)).toBe('Pantry');expect(v.navigation.canStand(v.START,0)).toBe(true);
 const before={x:-3.72,y:37,height:0},after={x:-3.72,y:40,height:0};
 expect(v.moveWalker(before,0,3).y).toBeLessThan(38.5);
 expect(v.moveWalker(after,0,-3).y).toBeGreaterThan(38.5);
 v.doors.toggle('dining_room:pantry_door');v.doors.update(1,safe);
 expect(v.moveWalker(before,0,3).y).toBeCloseTo(40);expect(v.moveWalker(after,0,-3).y).toBeCloseTo(37);
 const port=v.definitions.pantry.ports.find(p=>p.id==='pool_door')!;expect(port.state).toBe('open');
 const room=v.rooms.find(r=>r.id==='pantry')!,near=toWorld({x:-.8,y:4.8,height:0},room),outside=toWorld({x:-.8,y:6.5,height:0},room);
 const stopped=v.moveWalker(near,outside.x-near.x,outside.y-near.y);expect(Math.hypot(stopped.x-outside.x,stopped.y-outside.y)).toBeGreaterThan(1);
 v.requireLoadedRooms();v.setRoomLoaded('dining_room',true);expect(v.moveWalker(before,0,3).y).toBeLessThan(38.5);
 v.setRoomLoaded('pantry',true);expect(v.moveWalker(before,0,3).y).toBeCloseTo(40);
 expect(v.navigation.canStand(after,3.36)).toBe(false);
});
test('actual shared door blocks the sightline when closed and leaves a clear passage when open',async()=>{
 const v=createHouseRuntime(),scene=new THREE.Scene(),visual=createDoorView(scene,v.doors);
 for(const room of v.rooms.filter(r=>['dining_room','pantry'].includes(r.id))){
  const def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');await addDoorKit(gltf.scene,def);
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);visual.attach(room.id,root);
 }
 const door=v.doors.items.find(d=>d.key==='dining_room:pantry_door')!,camera=new THREE.PerspectiveCamera(68,1,.05,60),ray=new THREE.Raycaster();
 for(const amount of [0,1]){
  door.amount=amount;door.target=amount;visual.sync();scene.updateMatrixWorld(true);
  for(const [y,dir] of [[37.0,1],[40.0,-1]]){
   camera.position.set(-3.72,1.62,-y);camera.lookAt(-3.72,1.62,-38.5);camera.updateMatrixWorld(true);expect(visual.target(camera)?.key).toBe(door.key);
   ray.set(camera.position,new THREE.Vector3(0,0,-dir));ray.far=1.9;const hits=ray.intersectObjects(scene.children,true);
   if(amount===1)expect(hits).toHaveLength(0);else expect(hits[0]?.object.userData.doorKey).toBe(door.key);
  }
 }
});
