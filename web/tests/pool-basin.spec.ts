import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {createPool} from '../lib/house/pool';
import {toWorld} from '../lib/house/placement';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

test('one pool space drains, enables a continuous ladder and refills only from the deck',()=>{
 const v=createHouseRuntime('pool'),pool=createPool(v),r=v.rooms.find(r=>r.id==='pool')!;
 const at=(x:number,y:number,height=0)=>toWorld({x,y,height},r);
 let p=at(11,9.25),yaw=Math.PI+r.yaw;
 expect(v.poolState.drained).toBe(false);expect(pool.target(p,yaw)?.kind).toBe('drain');
 expect(v.navigation.canStand(at(10,5,-2.8),-2.8)).toBe(false);
 expect(pool.begin(pool.target(p,yaw)!,p,yaw)).toBe(true);
 expect(pool.target(p,yaw)?.kind).toBe('down');
 const edge=at(8,1.8),fall=v.moveWalker(edge,0,-2);expect(fall.height).toBe(0); // world yaw is pi
 for(const up of [false,true]){
  yaw=(up?0:Math.PI)+r.yaw;expect(pool.begin(pool.target(p,yaw)!,p,yaw)).toBe(true);
  expect(pool.target(p,yaw)).toBeNull();let prior=p;
  for(let i=0;i<1000&&pool.active;i++){
   p=pool.step(.01)!.walker;expect(Math.hypot(p.x-prior.x,p.y-prior.y,p.height-prior.height)).toBeLessThan(.08);prior=p;
   expect(v.activeRoom).toBe('pool');expect(v.activeSpace).toBe('pool_garage');
  }
  expect(p.height).toBeCloseTo(up?0:-2.8);expect(v.navigation.canStand(p,p.height)).toBe(true);
  if(!up){const floor=at(9,5,-2.8);expect(v.navigation.canStand(floor,-2.8)).toBe(true);expect(pool.target(floor,yaw)).toBeNull();}
 }
 const fill=at(8,1.6);yaw=r.yaw;expect(pool.target(fill,yaw)?.kind).toBe('fill');pool.begin(pool.target(fill,yaw)!,fill,yaw);
 expect(v.poolState.drained).toBe(false);expect(v.navigation.canStand(at(9,5,-2.8),-2.8)).toBe(false);
});

test('pool state belongs to each runtime and survives leaving its space',()=>{
 const a=createHouseRuntime('pool'),b=createHouseRuntime('pool');a.poolState.drained=true;a.activate('hall');a.activate('pool');
 expect(a.poolState.drained).toBe(true);expect(b.poolState.drained).toBe(false);
 const pool=createPool(a);a.requireLoadedRooms();expect(pool.target(a.START,a.START_YAW)).toBeNull();
});

test('one GLB separates wet surfaces and supports the basin below them',async()=>{
 const b=await readFile('../generated/models/rooms/pool_v1.glb');
 const root=(await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength) as ArrayBuffer,'')).scene;root.updateMatrixWorld(true);
 const wet=root.getObjectByName('Pool_water')!;expect(wet).toBeTruthy();
 const ray=new THREE.Raycaster(new THREE.Vector3(8,1,-5),new THREE.Vector3(0,-1,0),0,5);
 expect(ray.intersectObject(wet,true)[0].point.y).toBeGreaterThan(-.4);
 wet.removeFromParent();const hit=ray.intersectObject(root,true)[0];expect(hit.point.y).toBeCloseTo(-2.8);
});
