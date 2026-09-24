import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

test('attic window opens onto distant sky while walls stay complete and bulb light is baked',async()=>{
 const bytes=await readFile('../generated/models/rooms/safe_attic_v1_compact.glb');
 const gltf=await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'');
 const root=gltf.scene;root.updateMatrixWorld(true);
 expect(gltf.parser.json.extensionsUsed??[]).not.toContain('KHR_lights_punctual');
 const ray=new THREE.Raycaster();ray.far=40;
 const hit=(x:number,y:number,z:number,d:THREE.Vector3)=>{
  ray.set(new THREE.Vector3(x,z,-y),d);return ray.intersectObject(root,true)[0];
 };
 // There must be actual empty space past the frame, not a black wall/pane.
 const sky=hit(-3.5,3.03,2.10,new THREE.Vector3(-1,0,0));
 expect(sky).toBeTruthy();expect(sky.distance).toBeGreaterThan(8);
 for(const y of [2.2,3.8])expect(hit(-3.5,y,2.10,new THREE.Vector3(-1,0,0)).distance).toBeLessThan(1);
 for(const x of [-4.08,0,4.08])for(const z of [.06,1.5,3.08]){
  const wall=hit(x,3.8,z,new THREE.Vector3(0,0,-1));expect(wall).toBeTruthy();expect(wall.distance).toBeLessThan(.6);
 }
 const near:number[]=[],far:number[]=[];
 root.traverse(o=>{
  if(!(o instanceof THREE.Mesh))return;
  const pos=o.geometry.attributes.position,col=o.geometry.attributes.color;
  for(let i=0;i<pos.count;i++){
   const p=new THREE.Vector3().fromBufferAttribute(pos,i).applyMatrix4(o.matrixWorld);
   if(Math.abs(p.y)>.002)continue;
   const y=-p.z;
   if(Math.hypot(p.x,y-2.96)<.65)near.push(col.getX(i));
   if(p.x< -3&&p.x> -4&&y>.4&&y<1.4)far.push(col.getX(i));
  }
 });
 expect(near.length).toBeGreaterThan(5);expect(far.length).toBeGreaterThan(5);
 const mean=(v:number[])=>v.reduce((a,b)=>a+b,0)/v.length;
 expect(mean(near)).toBeGreaterThan(mean(far)*1.15);
});
