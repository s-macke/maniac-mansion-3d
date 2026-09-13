import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {addDoorKit} from './shared-fixture';
import {createDoorView} from '../lib/house/door-view';
const routes=[
 {key:'living_room:right_double_door',x:19.2,y:3.15,h:0,dx:1,dy:0},
 {key:'hall:landing_left',x:-6.4,y:8.5,h:3.36,dx:1,dy:0},
 {key:'hall:landing_right',x:6.4,y:8.5,h:3.36,dx:1,dy:0},
 {key:'hall:landing_center',x:.2,y:9.75,h:3.36,dx:0,dy:1},
 {key:'security_hall:medical_door',x:-2.8,y:15.3,h:3.36,dx:0,dy:1},
 {key:'security_hall:arcade_door',x:3.4,y:15.3,h:3.36,dx:0,dy:1},
];
test('every new doorway starts closed and permits passage both ways after opening',()=>{
 for(const r of routes){
  const v=createHouseRuntime(),a={x:r.x-r.dx*1.3,y:r.y-r.dy*1.3,height:r.h},b={x:r.x+r.dx*1.3,y:r.y+r.dy*1.3,height:r.h};
  const cross=(p:typeof a,q:typeof a)=>v.moveWalker(p,q.x-p.x,q.y-p.y);
  expect(v.doors.items.find(d=>d.key===r.key)?.amount,r.key).toBe(0);
  expect(Math.hypot(cross(a,b).x-b.x,cross(a,b).y-b.y),r.key).toBeGreaterThan(.5);
  v.doors.toggle(r.key);v.doors.update(1,{x:0,y:1,height:0});
  for(const [p,q] of [[a,b],[b,a]]){const end=cross(p,q);expect(Math.hypot(end.x-q.x,end.y-q.y),r.key).toBeLessThan(.02);expect(end.height).toBeCloseTo(r.h);}
 }
});
test('first floor spawns require the correct level and loaded rooms; upper stair has a closed boundary',()=>{
 for(const id of ['plant_room','music_room','security_hall','medical_room','arcade']){
  const v=createHouseRuntime(id);expect(v.START.height).toBe(3.36);expect(v.navigation.canStand(v.START,3.36),id).toBe(true);
  v.requireLoadedRooms();expect(v.navigation.canStand(v.START,3.36)).toBe(false);v.setRoomLoaded(id,true);expect(v.navigation.canStand(v.START,3.36)).toBe(true);expect(v.navigation.canStand(v.START,0),id).toBe(false);
 }
 const v=createHouseRuntime('security_hall');let p={x:6.025,y:10.65,height:3.36};
 p=v.moveWalker(p,0,4.2);expect(p.y).toBeCloseTo(14.85);expect(p.height).toBeCloseTo(6.72);
 const stopped=v.moveWalker(p,0,2);expect(stopped.y).toBeLessThan(15);expect(stopped.height).toBeCloseTo(6.72);
 p=v.moveWalker(p,0,-4.2);expect(p.y).toBeCloseTo(10.65);expect(p.height).toBeCloseTo(3.36);
});
test('actual room and shared meshes leave every new open threshold clear, including the facade',async()=>{
 const v=createHouseRuntime(),scene=new THREE.Scene(),view=createDoorView(scene,v.doors);
 for(const room of v.rooms){
  const def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
  await addDoorKit(gltf.scene,def);
  const root=new THREE.Group();root.position.set(room.position[0],room.position[2],-room.position[1]);root.rotation.y=room.yaw;root.add(gltf.scene);scene.add(root);view.attach(room.id,root);
 }
 const ray=new THREE.Raycaster();scene.updateMatrixWorld(true);
 // The visible floor must match navigation: roofs and lower-room ceilings cannot cut through an upstairs room.
 for(const room of v.rooms.filter(r=>['library','plant_room','music_room','security_hall','medical_room','arcade'].includes(r.id))){
  const def=v.definitions[room.definition];
  for(const x of [def.bounds.min[0]+.9,0,def.bounds.max[0]-.9])for(const y of [.9,def.bounds.max[1]/2,def.bounds.max[1]-.9]){
   if(room.id==='security_hall'&&x>5)continue;
   const p={x:room.position[0]+x,y:room.position[1]+y,height:room.position[2]};if(!v.navigation.canStand(p,p.height))continue;
   ray.set(new THREE.Vector3(p.x,p.height+1.62,-p.y),new THREE.Vector3(0,-1,0));ray.far=1.8;
   const hits=ray.intersectObjects(scene.children,true);expect(hits.length,room.id+' floor').toBeGreaterThan(0);
   expect.soft(hits[0]?.point.y,room.id+' floor at '+x+','+y).toBeCloseTo(p.height,2);
  }
 }
 // Stair treads track the continuous navigation ramp, with clear headroom throughout.
 for(let i=0;i<=20;i++){
  const y=10.95+3.9*i/20,p={x:6.025,y,height:3.36+3.36*i/20};
  const h=v.navigation.floorHeight(p,p.height);
  ray.set(new THREE.Vector3(p.x,h+1.62,-y),new THREE.Vector3(0,-1,0));ray.far=2;
  const below=ray.intersectObjects(scene.children,true);expect(below.length).toBeGreaterThan(0);expect(Math.abs(below[0].point.y-h)).toBeLessThan(.2);
  ray.set(new THREE.Vector3(p.x,h+1.62,-y),new THREE.Vector3(0,1,0));ray.far=.55;expect(ray.intersectObjects(scene.children,true).map(h=>h.object.name),'stair headroom').toEqual([]);
 }
 for(const r of routes){
  const shoot=()=>{scene.updateMatrixWorld(true);ray.set(new THREE.Vector3(r.x-r.dx*1.3+r.dy*.12,r.h+1.62,-r.y+r.dy*1.3+r.dx*.12),new THREE.Vector3(r.dx,0,-r.dy));ray.far=2.6;return ray.intersectObjects(scene.children,true);};
  const camera=new THREE.PerspectiveCamera(68,1,.05,60);
  const select=()=>{for(const side of [-1,1]){camera.position.set(r.x-r.dx*1.3*side,r.h+1.62,-r.y+r.dy*1.3*side);camera.lookAt(r.x,r.h+1.45,-r.y);expect(view.target(camera)?.key,r.key+' target').toBe(r.key);}};
  expect(shoot().length,r.key+' closed').toBeGreaterThan(0);select();
  v.doors.toggle(r.key);v.doors.update(1,{x:0,y:1,height:0});view.sync();
  expect.soft(shoot().map(h=>h.object.name),r.key+' open').toEqual([]);select();
  for(const side of [-1,1])for(const offset of [-.15,.15])for(const height of [.4,1.62,2.1]){
   ray.set(new THREE.Vector3(r.x-r.dx*1.3*side+r.dy*offset,r.h+height,-r.y+r.dy*1.3*side+r.dx*offset),new THREE.Vector3(r.dx*side,0,-r.dy*side));ray.far=2.6;
   expect.soft(ray.intersectObjects(scene.children,true).map(h=>h.object.name),r.key+' open clearance').toEqual([]);
  }
 }
});

test('main stairs lead continuously into every first-floor room and back to ground',()=>{
 const v=createHouseRuntime('hall');for(const r of routes){if(r.key!=='hall:landing_center')v.doors.toggle(r.key);}v.doors.update(1,{x:0,y:1,height:0});
 let p={x:-.55,y:1.5,height:0};const stair=Array.from({length:201},(_,i)=>{const t=i/200;return{x:-.55+1.3*Math.sin(t*Math.PI*.8),y:2.15+4.13*t};});
 const go=(x:number,y:number)=>{p=v.moveWalker(p,x-p.x,y-p.y);expect(Math.hypot(p.x-x,p.y-y),JSON.stringify({x,y,actual:p})).toBeLessThan(.06);};
 for(const q of stair)go(q.x,q.y);go(p.x,7.5);
 for(const [x,y] of [[-4.5,8.5],[-8,8.5],[-4.5,8.5],[4.5,8.5],[8,8.5],[4.5,8.5],[.2,8.5],[.2,11.5],[-2.8,13.9],[-2.8,17],[-2.8,13.9],[-2.8,13],[3.4,13],[3.4,13.9],[3.4,17],[3.4,13.9],[3.4,13],[.2,11.5],[.2,8.5],[.2,7.5]]){if(x===.2&&y===11.5&&!v.doors.items.find(d=>d.key==='hall:landing_center')!.amount){v.doors.toggle('hall:landing_center');v.doors.update(1,{x:0,y:1,height:0});}go(x,y);expect(p.height).toBeCloseTo(3.36);}
 for(const q of stair.reverse())go(q.x,q.y);go(p.x,1.5);expect(p.height).toBe(0);
});

test('first-floor room footprints meet at boundaries without overlapping',()=>{
 const v=createHouseRuntime();
 const boxes=v.rooms.filter(r=>r.position[2]===3.36).map(r=>{const g=v.definitions[r.definition].geometry!;return{id:r.id,x0:r.position[0]-Number(g.halfWidth),x1:r.position[0]+Number(g.halfWidth),y0:r.position[1],y1:r.position[1]+Number(g.depth)};});
 boxes.push({id:'landing',x0:-6.4,x1:6.4,y0:5.7,y1:9.75});
 for(let i=0;i<boxes.length;i++)for(const b of boxes.slice(i+1)){const a=boxes[i];const width=Math.min(a.x1,b.x1)-Math.max(a.x0,b.x0),depth=Math.min(a.y1,b.y1)-Math.max(a.y0,b.y0);expect(width<=.001||depth<=.001,a.id+' / '+b.id).toBe(true);}
});
