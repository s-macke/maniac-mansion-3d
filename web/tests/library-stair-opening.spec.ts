import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createHouseRuntime} from '../lib/house/runtime';

test('library stairs enter a real enclosed ceiling opening without a new destination',async()=>{
 const v=createHouseRuntime('library'),def=v.definitions.library;
 expect(v.graph.outgoing('library').map(e=>e.to.room.id)).toEqual(['living_room']);
 const bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
 const scene=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;
 scene.updateMatrixWorld(true);
 const up=(x:number,y:number,z:number,far:number)=>{
  const ray=new THREE.Raycaster(new THREE.Vector3(x,z,-y),new THREE.Vector3(0,1,0),0,far);
  return ray.intersectObject(scene,true);
 };
 // This corner is inside the square opening but outside the spiral's radius.
 expect(up(1.3,1.65,3,.4)).toHaveLength(0);
 expect(up(1.8,1.65,3,.4).length).toBeGreaterThan(0);
 const cap=up(1.3,1.65,3,3);
 expect(cap.length).toBeGreaterThan(0);expect(cap[0].point.y).toBeCloseTo(5.75,2);
 // Solid continuation treads are present above the ceiling.
 const angle=-Math.PI/2+23.5*Math.PI*2/25;
 const tread=up(-.1+Math.cos(angle),3.05+Math.sin(angle),3.17,.3);
 expect(tread.length).toBeGreaterThan(0);
});
