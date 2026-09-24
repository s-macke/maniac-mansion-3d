import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

for(const [id,file,rays] of [
 ['living_room','living_room_v4_compact.glb',[[-2.94761,4.9,2.9391,0,1],[-2.80955,4.9,2.47537,0,1],[2.9064,4.9,2.4472,0,1]]],
 ['green_bedroom','green_bedroom_v1_compact.glb',[[3.25,3.4,2.2,0,1]]],
 ['mummy_bathroom','mummy_bathroom_v1_compact.glb',[[3.0,3.5,2.35,1,0]]],
 ['kitchen','kitchen_v4_compact.glb',[[-5.2,4.7,2.4,0,1],[2.6,5.0,2.4,0,1]]],
] as const)test(id+' windows look through the wall onto distant sky',async()=>{
 const bytes=await readFile('../generated/models/rooms/'+file);
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
 gltf.scene.updateMatrixWorld(true);expect(gltf.parser.json.extensionsUsed??[]).not.toContain('KHR_lights_punctual');
 for(const [x,y,z,dx,dy] of rays){
  const ray=new THREE.Raycaster(new THREE.Vector3(x,z,-y),new THREE.Vector3(dx,0,-dy),0,45);
  const hits=ray.intersectObject(gltf.scene,true);
  expect(hits.length).toBeGreaterThan(0);expect(hits[0].distance).toBeGreaterThan(8);
  // The same wall above the aperture stays solid.
  ray.ray.origin.y=id==='living_room'?3.4:2.95;
  const wall=ray.intersectObject(gltf.scene,true);expect(wall.length).toBeGreaterThan(0);expect(wall[0].distance).toBeLessThan(1.5);
 }
});
