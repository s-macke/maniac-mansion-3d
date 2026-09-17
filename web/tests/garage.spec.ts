import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

test('outdoor path connects pool to forecourt and covered garage in both directions',()=>{
 const v=createHouseRuntime('garage'),garage=v.rooms.find(r=>r.id==='garage')!,pool=v.rooms.find(r=>r.id==='pool')!;
 const at=(x:number,y:number)=>toWorld({x,y,height:0},garage),deck=toWorld({x:18.5,y:5.2,height:0},pool);
 expect(v.zoneAt(v.START)).toBe('Garage forecourt');expect(v.navigation.canStand(v.START,0)).toBe(true);
 let pos=deck;
 for(const q of [at(1.5,4),at(6,4),at(10.8,4),at(6,2.2),at(6,5.8),at(2,4),deck]){
  pos=v.moveWalker(pos,q.x-pos.x,q.y-pos.y);expect(Math.hypot(pos.x-q.x,pos.y-q.y)).toBeLessThan(.03);expect(pos.height).toBe(0);
 }
 expect(v.zoneAt(at(7,4))).toBe('Garage');
 for(const q of [at(14.2,4),at(7,.5),at(7,7.5),at(4.05,.9)])expect(v.navigation.canStand(q,0)).toBe(false);
 const wall=v.moveWalker(at(2,1),-5,0);expect(wall.x).toBeGreaterThan(at(4,1).x);
 expect(v.navigation.canStand(at(8,4),3.3)).toBe(false);
 v.requireLoadedRooms();v.setRoomLoaded('pool',true);expect(v.moveWalker(deck,-3,0).x).toBeGreaterThan(at(0,4).x);
 v.setRoomLoaded('garage',true);expect(v.moveWalker(deck,-3,0).x).toBeCloseTo(at(1.5,4).x);
});

test('actual meshes leave the fence opening and vehicle entrance clear, with a solid roof',async()=>{
 const v=createHouseRuntime(),scene=new THREE.Scene();
 for(const room of v.rooms.filter(r=>['pool','garage'].includes(r.id))){
  const def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);
 }
 scene.updateMatrixWorld(true);const ray=new THREE.Raycaster();
 for(const [x,dir] of [[-24.87,-1],[-32.87,1]]){
  ray.set(new THREE.Vector3(x,1.62,-38.9),new THREE.Vector3(dir,0,0));ray.far=8;expect(ray.intersectObjects(scene.children,true)).toHaveLength(0);
 }
 ray.set(new THREE.Vector3(-34.37,6,-38.9),new THREE.Vector3(0,-1,0));ray.far=4;
 expect(ray.intersectObjects(scene.children,true).length).toBeGreaterThan(0);
});
