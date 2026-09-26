import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createHouseRuntime} from '../lib/house/runtime';

test('hamster has volume inside its open framed enclosure',async()=>{
 const def=createHouseRuntime('green_bedroom').definitions.green_bedroom;
 const bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
 const scene=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;
 scene.updateMatrixWorld(true);
 for(const x of [-.05,.16,.32]){
  const ray=new THREE.Raycaster(new THREE.Vector3(x,1.13,-3.1),new THREE.Vector3(0,0,-1),0,1);
  const hit=ray.intersectObject(scene,true)[0];expect(hit).toBeDefined();
  // A flat tank-front picture is at Y 3.43; the back wall is at Y 4.06.
  expect(-hit.point.z).toBeGreaterThan(3.5);expect(-hit.point.z).toBeLessThan(3.9);
 }
 const side=new THREE.Raycaster(new THREE.Vector3(-.5,1.13,-3.72),new THREE.Vector3(1,0,0),0,1);
 const hit=side.intersectObject(scene,true)[0];expect(hit).toBeDefined();
 expect(hit.point.x).toBeGreaterThan(-.21);expect(hit.point.x).toBeLessThan(0);
});
