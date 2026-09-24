import {addDoorKit} from './shared-fixture';
import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {readFile} from 'node:fs/promises';
import {createDoorView} from '../lib/house/door-view';

const safe={x:0,y:1,height:0};
test('kitchen threshold aligns with hall, starts closed, opens and traverses both ways',()=>{
 const v=createHouseRuntime('kitchen'),room=v.rooms.find(r=>r.id==='kitchen')!,def=v.definitions.kitchen;
 expect(v.zoneAt(v.START)).toBe('Kitchen');expect(v.navigation.canStand(v.START,0)).toBe(true);
 const at=(x:number,y:number,height=0)=>toWorld({x,y,height},room);
 const port=at(-6.4,2.9);expect(port.x).toBeCloseTo(-3.72);expect(port.y).toBeCloseTo(6.5);
 v.activate('hall');let p={x:-3.72,y:5.4,height:0};expect(v.moveWalker(p,0,2).y).toBeLessThan(6.2);
 v.doors.toggle('hall:kitchen_door');v.doors.update(1,safe);
 const visit=(q:typeof p)=>{p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(Math.hypot(p.x-q.x,p.y-q.y)).toBeLessThan(.03);expect(p.height).toBe(0);};
 visit(at(-5,2.9));expect(v.zoneAt(p)).toBe('Kitchen');
 // Walk the clear floor in front of the fitted cabinets and return through the same physical doorway.
 for(const q of [at(5,2.9),at(5,3.5),at(-5,3.5),at(-5,1),at(5,1),at(-5,2.9)])visit(q);
 visit({x:-3.72,y:5.4,height:0});expect(v.zoneAt(p)).toBe('Entrance hall');
 expect(def.ports.find(p=>p.id==='dining_door')?.state).toBe('open');
 v.activate('kitchen');const start=at(4.5,2.9),end=at(10,2.9);const stopped=v.moveWalker(start,end.x-start.x,end.y-start.y);
 expect(stopped.y).toBeLessThan(at(6.1,2.9).y);
 v.doors.toggle('hall:kitchen_door');v.doors.update(1,safe);
 expect(v.moveWalker(at(-5,2.9),0,-3).y).toBeGreaterThan(6.7);
});
test('kitchen walls, unopened exits, and unloaded neighbors remain solid at both elevations',()=>{
 const v=createHouseRuntime('kitchen'),room=v.rooms.find(r=>r.id==='kitchen')!;
 const at=(x:number,y:number,height=0)=>toWorld({x,y,height},room);
 expect(v.navigation.canStand(at(0,-.2),0)).toBe(false);
 expect(v.navigation.canStand(at(0,6),0)).toBe(false);
 // An overlapping gallery belongs to the hall, never to the kitchen space.
 expect(v.navigation.canStand(at(-4,3,3.36),3.36)).toBe(false);
 expect(v.navigation.floorHeight(at(-4,3),0)).toBe(0);
 expect(v.navigation.canStand(at(2,3,3.36),3.36)).toBe(false);
 v.activate('hall');expect(v.navigation.canStand(at(-4,3,3.36),3.36)).toBe(true);
 expect(v.navigation.floorHeight(at(-4,3,3.36),3.36)).toBe(3.36);
 v.doors.toggle('hall:kitchen_door');v.doors.update(1,safe);v.requireLoadedRooms();v.setRoomLoaded('hall',true);
 expect(v.moveWalker({x:-3.72,y:5.4,height:0},0,3).y).toBeLessThan(6.1);
 v.setRoomLoaded('kitchen',true);expect(v.moveWalker({x:-3.72,y:5.4,height:0},0,3).y).toBeCloseTo(8.4);
 v.setRoomLoaded('hall',false);expect(v.moveWalker(at(-5,2.9),0,-3).y).toBeGreaterThan(6.7);
});
test('exported kitchen doorway is visually clear when open, opaque when closed, and selectable on both sides',async()=>{
 const v=createHouseRuntime(),scene=new THREE.Scene(),visual=createDoorView(scene,v.doors);
 for(const room of v.rooms.filter(r=>['hall','kitchen'].includes(r.id))){
  const filename=v.definitions[room.definition].asset.split('/').at(-1)!.replace('.glb','_compact.glb'),bytes=await readFile('../generated/models/rooms/'+filename);
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
  await addDoorKit(gltf.scene,v.definitions[room.definition]);
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);visual.attach(room.id,root);
 }
 const camera=new THREE.PerspectiveCamera(68,1,.05,60),ray=new THREE.Raycaster();
 for(const amount of [0,1]){
  const door=v.doors.items.find(d=>d.def.id==='kitchen_door')!;door.amount=amount;door.target=amount;visual.sync();scene.updateMatrixWorld(true);
  for(const [y,dir] of [[5.1,1],[7.6,-1]]){
   camera.position.set(-3.72,1.62,-y);camera.lookAt(-3.72,1.62,-6.5);camera.updateMatrixWorld(true);
   expect(visual.target(camera)?.key).toBe(door.key);
   ray.set(new THREE.Vector3(-3.72,1.62,-y),new THREE.Vector3(0,0,-dir));ray.far=Math.abs(y-6.5)+.4;
   const hits=ray.intersectObjects(scene.children,true);
   if(amount===1)expect(hits).toHaveLength(0);else expect(hits[0]?.object.userData.doorKey).toBe(door.key);
  }
 }
});

test('the exported kitchen shell stays 3 cm behind the exterior inner facade plane',async()=>{
 const v=createHouseRuntime(),room=v.rooms.find(r=>r.id==='kitchen')!,exterior=v.rooms.find(r=>r.id==='front_exterior')!;
 const filename=v.definitions.kitchen.asset.split('/').at(-1)!,bytes=await readFile('../generated/models/rooms/'+filename);
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
 // Window scenery is intentionally outside the shell; whole-model bounds include
 // distant sky and projecting window reveals. Measure the solid rear wall itself.
 for(const name of ['Kitchen_window_2_sky','Kitchen_window_3_sky'])gltf.scene.getObjectByName(name)?.removeFromParent();
 gltf.scene.updateMatrixWorld(true);
 const plane=toWorld({x:0,y:0,height:0},exterior).x;
 for(const x of [-5.9,0,5.9]){
  const ray=new THREE.Raycaster(new THREE.Vector3(x,1.4,-8),new THREE.Vector3(0,0,1),0,4);
  const hit=ray.intersectObject(gltf.scene,true)[0];expect(hit).toBeTruthy();
  const wall=toWorld({x:hit.point.x,y:-hit.point.z,height:hit.point.y},room);
  expect(wall.x-plane).toBeGreaterThan(.0299);
  expect(wall.x-plane).toBeCloseTo(.03,4);
 }
 const port=v.definitions.kitchen.ports.find(p=>p.id==='hall_door')!;
 const threshold=toWorld({x:port.position[0],y:port.position[1],height:0},room);
 expect(threshold.x).toBeCloseTo(-3.72);expect(threshold.y).toBeCloseTo(6.5);
});
