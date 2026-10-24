import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

test('landing glass panes have convex depth inside the leaded frames',async()=>{
 const bytes=await readFile('../generated/models/rooms/windowed_hall_v1_compact.glb');
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
 const root=gltf.scene;root.updateMatrixWorld(true);
 expect(gltf.parser.json.extensionsUsed??[]).not.toContain('KHR_lights_punctual');
 for(const windowX of [-.35,2,4.35]){
  const cx=windowX-1.3/2+1.3/8,cz=1.85-1.95/2+1.95/12;
  const depth=(x:number)=>new THREE.Raycaster(new THREE.Vector3(x,cz,-5.5),new THREE.Vector3(0,0,-1),0,.4).intersectObject(root,true)[0].distance;
  const center=depth(cx),edge=depth(cx+(1.3/8-.014)*.8);
  expect(center).toBeCloseTo(.224,3);expect(edge-center).toBeGreaterThan(.02);
 }
});
