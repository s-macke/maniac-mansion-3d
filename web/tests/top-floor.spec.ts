import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createHouseRuntime} from '../lib/house/runtime';
import {RADIUS,EYE_HEIGHT} from '../lib/house/navigation';

test('furnished attic ladder landings have physical body clearance in the exported models',async()=>{
 const v=createHouseRuntime();
 for(const link of v.house.ladders!.filter(l=>['safe_attic','tentacle_room','observatory'].includes(l.upper.room))){
  const end=link.upper,def=v.definitions[end.room],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const root=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;root.updateMatrixWorld(true);
  for(let i=0;i<9;i++){
   const x=end.landing.x+(i?RADIUS*Math.cos(i*Math.PI/4):0),y=end.landing.y+(i?RADIUS*Math.sin(i*Math.PI/4):0);
   const ray=new THREE.Raycaster(new THREE.Vector3(x,EYE_HEIGHT,-y),new THREE.Vector3(0,-1,0),0,EYE_HEIGHT+.1);
   const hits=ray.intersectObject(root,true);
   expect(hits.length,end.room+' landing floor').toBeGreaterThan(0);
   expect(hits[0].point.y,end.room+' furniture enters landing body at '+[x,y]).toBeCloseTo(0,2);
   ray.ray.direction.set(0,1,0);ray.far=.35;
   expect(ray.intersectObject(root,true),end.room+' landing headroom').toHaveLength(0);
  }
 }
});
