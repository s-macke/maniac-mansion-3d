import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
async function load(room:string){
 const b=await readFile(`../generated/models/rooms/${room}_v1_compact.glb`);
 const root=(await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength) as ArrayBuffer,'')).scene;
 root.updateMatrixWorld(true);return root;
}
test('security stairs keep white step faces on both sides of the portal and timber uprights',async()=>{
 const lower=await load('security_hall'),upper=await load('windowed_hall');
 for(const i of [2,6,8]){
  const y=1.15+3.95*i/10,z=1.68*(i+1)/10;
  const upperX=2.9+3.5*(i+.5)/10,upperZ=-1.68*i/10;
  for(const [root,origin,direction] of [
   [lower,new THREE.Vector3(5.8,z+.05,-y-.20),new THREE.Vector3(0,-1,0)],
   [lower,new THREE.Vector3(5.8,z-.08,-y+.05),new THREE.Vector3(0,0,-1)],
   [upper,new THREE.Vector3(upperX,upperZ+.05,-5.3),new THREE.Vector3(0,-1,0)],
  ] as const){
   const hit=new THREE.Raycaster(origin,direction,0,.10).intersectObject(root,true)[0];expect(hit).toBeTruthy();
   const colors=(hit.object as THREE.Mesh).geometry.attributes.color,k=hit.face!.a;
   expect(colors.getX(k)).toBeGreaterThan(.2);
   expect(colors.getX(k)).toBeCloseTo(colors.getY(k),4);expect(colors.getY(k)).toBeCloseTo(colors.getZ(k),4);
  }
  const post=new THREE.Raycaster(new THREE.Vector3(5,z+.3,-y-.09),new THREE.Vector3(1,0,0),0,.3).intersectObject(lower,true)[0];
  expect(post).toBeTruthy();expect(post.distance).toBeLessThan(.24);
 }
});
