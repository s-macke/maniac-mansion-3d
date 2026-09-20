import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

test('medical desk lamp is baked locally with valid colors and no runtime lights',async()=>{
 const bytes=await readFile('../generated/models/rooms/medical_room_v1_compact.glb');
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
 expect(gltf.parser.json.extensionsUsed??[]).not.toContain('KHR_lights_punctual');
 const near:number[]=[],far:number[]=[];let min=Infinity,max=-Infinity,finite=true;
 gltf.scene.updateMatrixWorld(true);
 gltf.scene.traverse(o=>{
  if(!(o instanceof THREE.Mesh))return;
  const positions=o.geometry.attributes.position,colors=o.geometry.attributes.color;
  expect(colors).toBeTruthy();
  for(let i=0;i<positions.count;i++){
   for(const value of [colors.getX(i),colors.getY(i),colors.getZ(i)]){
    finite&&=Number.isFinite(value);min=Math.min(min,value);max=Math.max(max,value);
   }
   const p=new THREE.Vector3().fromBufferAttribute(positions,i).applyMatrix4(o.matrixWorld),x=p.x,y=-p.z;
   // Compare the same brown desktop surface near the lamp with its distant end.
   if(Math.abs(p.y-1.015)>.002||x< -4.18||x> -1.62||y<4.34||y>5.28)continue;
   if(Math.hypot(x+3.75,y-4.72)<.5)near.push(colors.getX(i));
   if(x> -2.5)far.push(colors.getX(i));
  }
 });
 expect(finite).toBe(true);expect(min).toBeGreaterThanOrEqual(0);expect(max).toBeLessThanOrEqual(1);
 expect(near.length).toBeGreaterThan(5);expect(far.length).toBeGreaterThan(5);
 const mean=(a:number[])=>a.reduce((sum,n)=>sum+n,0)/a.length;
 expect(mean(near)).toBeGreaterThan(mean(far)*1.05);
});
