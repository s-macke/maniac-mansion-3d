import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {canStand,floorHeight} from '../lib/rooms/observatory';
import {createHouseRuntime} from '../lib/house/runtime';
test('round boundary and hatch block walking without enclosing the telescope slit',async()=>{
 const v=createHouseRuntime('observatory'),def=v.definitions.observatory;
 expect(v.graph.outgoing('observatory').map(e=>e.to.room.id)).toEqual(['typewriter_room']);
 expect(canStand({x:0,y:4.2})).toBe(true);expect(canStand({x:3.6,y:7.8})).toBe(false);
 expect(Number.isNaN(floorHeight({x:4,y:8}))).toBe(true);expect(canStand({x:-2.5,y:3.7})).toBe(false);
 for(let i=0;i<32;i++)expect(canStand({x:4.1*Math.cos(i*Math.PI/16),y:4.2+4.1*Math.sin(i*Math.PI/16)})).toBe(false);
 const b=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
 const shell=(await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength) as ArrayBuffer,'')).scene;shell.updateMatrixWorld(true);
 const ray=new THREE.Raycaster();
 const hits=(x:number,y:number,z:number,dx:number,dy:number,dz:number,far=12)=>{
  ray.set(new THREE.Vector3(x,z,-y),new THREE.Vector3(dx,dz,-dy).normalize());ray.far=far;return ray.intersectObject(shell,true);
 };
 // Physical aperture: this line of sight leaves the dome, while the opposite ray hits its shell.
 expect(hits(0,4.2,1.62,3,3,1.9)).toHaveLength(0);
 expect(hits(0,4.2,1.62,-3,-3,1.9).length).toBeGreaterThan(0);
 // Camera/body clearance at the actual access portal, not a black hatch painted over a floor.
 expect(hits(-2.5,3.7,-.35,0,0,1,.7)).toHaveLength(0);
 for(let i=0;i<16;i++){
  const x=2.8*Math.cos(i*Math.PI/8),y=4.2+2.8*Math.sin(i*Math.PI/8);
  if(!canStand({x,y}))continue;
  const floor=hits(x,y,1.62,0,0,-1,1.8);expect(floor.length).toBeGreaterThan(0);expect(floor[0].point.y).toBeCloseTo(0);
  expect(hits(x,y,1.62,0,0,1,.35)).toHaveLength(0);
 }
});

test('den access matches the right-hand pot and closes the mistaken left ceiling hole',async()=>{
 const v=createHouseRuntime(),def=v.definitions.typewriter_room;
 const hatch=def.ports.find(p=>p.id==='observatory_hatch')!;
 expect(hatch.position).toEqual([3.1,4.3,3.36]);
 const b=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
 const shell=(await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength) as ArrayBuffer,'')).scene;shell.updateMatrixWorld(true);
 const ray=new THREE.Raycaster(new THREE.Vector3(-3.65,2.8,-4.3),new THREE.Vector3(0,1,0),0,.7);
 expect(ray.intersectObject(shell,true).length).toBeGreaterThan(0);
 ray.ray.origin.x=3.1;expect(ray.intersectObject(shell,true)).toHaveLength(0);
});
