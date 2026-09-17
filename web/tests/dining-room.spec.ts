import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {addDoorKit} from './shared-fixture';
import {createDoorView} from '../lib/house/door-view';
const safe={x:0,y:1,height:0};
test('hall, kitchen and furnished dining room connect at ground level and return along the same route',()=>{
 const v=createHouseRuntime('dining_room'),room=v.rooms.find(r=>r.id==='dining_room')!;
 expect(v.zoneAt(v.START)).toBe('Dining room');expect(v.navigation.canStand(v.START,0)).toBe(true);
 const at=(x:number,y:number)=>toWorld({x,y,height:0},room),threshold=at(-9.6,2.9);
 expect(threshold.x).toBeCloseTo(-3.72);expect(threshold.y).toBeCloseTo(19.3);
 v.activate('kitchen');expect(v.moveWalker({x:-3.72,y:17.8,height:0},0,4).y).toBeLessThan(19);
 v.activate('dining_room');expect(v.moveWalker(at(-8.7,2.9),0,-4).y).toBeGreaterThan(19.4);
 for(const key of ['hall:kitchen_door','kitchen:dining_door'])v.doors.toggle(key);
 v.doors.update(1,safe);v.activate('hall');let p={x:-3.72,y:5.4,height:0};
 const visit=(q:typeof p)=>{p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(Math.hypot(p.x-q.x,p.y-q.y)).toBeLessThan(.03);expect(p.height).toBe(0);};
 visit({x:-3.72,y:8,height:0});expect(v.zoneAt(p)).toBe('Kitchen');
 visit(at(-8.7,2.9));expect(v.zoneAt(p)).toBe('Dining room');
 for(const q of [at(-8.7,1),at(8.7,1),at(8.7,2.9),at(8.7,4.6),at(-8.7,4.6),at(-8.7,2.9)])visit(q);
 const end=at(12,2.9);const stopped=v.moveWalker(at(8.7,2.9),end.x-at(8.7,2.9).x,end.y-at(8.7,2.9).y);expect(stopped.y).toBeLessThan(at(9.4,2.9).y);
 expect(v.definitions.dining_room.ports.find(p=>p.id==='pantry_door')?.state).toBe('open');
 visit({x:-3.72,y:17.8,height:0});visit({x:-3.72,y:5.4,height:0});expect(v.zoneAt(p)).toBe('Entrance hall');
 v.doors.toggle('kitchen:dining_door');v.doors.update(1,safe);expect(v.moveWalker({x:-3.72,y:17.8,height:0},0,4).y).toBeLessThan(19);
});
test('dining room entry waits for both room assets and walls reject wrong elevations',()=>{
 const v=createHouseRuntime('kitchen'),p={x:-3.72,y:17.8,height:0};
 v.doors.toggle('kitchen:dining_door');v.doors.update(1,safe);v.requireLoadedRooms();v.setRoomLoaded('kitchen',true);
 expect(v.moveWalker(p,0,4).y).toBeLessThan(19);
 v.setRoomLoaded('dining_room',true);expect(v.moveWalker(p,0,2).y).toBeCloseTo(19.8);
 expect(v.navigation.canStand({x:-3.72,y:25},3.36)).toBe(false);
 const room=v.rooms.find(r=>r.id==='dining_room')!;for(const y of [-.1,5.65]){const q=toWorld({x:0,y,height:0},room);expect(v.navigation.canStand(q,0)).toBe(false);}
});
test('actual shared door blocks the sightline when closed and leaves a clear passage when open',async()=>{
 const v=createHouseRuntime(),scene=new THREE.Scene(),visual=createDoorView(scene,v.doors);
 for(const room of v.rooms.filter(r=>['kitchen','dining_room'].includes(r.id))){
  const def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');await addDoorKit(gltf.scene,def);
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);visual.attach(room.id,root);
 }
 const door=v.doors.items.find(d=>d.key==='kitchen:dining_door')!,camera=new THREE.PerspectiveCamera(68,1,.05,60),ray=new THREE.Raycaster();
 for(const amount of [0,1]){
  door.amount=amount;door.target=amount;visual.sync();scene.updateMatrixWorld(true);
  for(const [y,dir] of [[17.8,1],[20.8,-1]]){
   camera.position.set(-3.72,1.62,-y);camera.lookAt(-3.72,1.62,-19.3);camera.updateMatrixWorld(true);expect(visual.target(camera)?.key).toBe(door.key);
   ray.set(camera.position,new THREE.Vector3(0,0,-dir));ray.far=1.9;const hits=ray.intersectObjects(scene.children,true);
   if(amount===1)expect(hits).toHaveLength(0);else expect(hits[0]?.object.userData.doorKey).toBe(door.key);
  }
 }
});
