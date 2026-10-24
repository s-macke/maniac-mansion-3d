import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {stairEdges} from '../lib/rooms/connected_hall';
async function model(name:string){const b=await readFile('../generated/models/rooms/'+name);const root=(await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength) as ArrayBuffer,'')).scene;root.updateMatrixWorld(true);return root;}
test('curved hall stair has one side surface at each upper tread/panel join',async()=>{
 const root=await model('connected_hall_v6_compact.glb');
 for(const i of [10,13,16,19])for(const side of ['left','right'] as const){
  const edge=stairEdges[i][side],next=stairEdges[i+1][side],other=stairEdges[i][side==='left'?'right':'left'],otherNext=stairEdges[i+1][side==='left'?'right':'left'];
  const x=edge.x+(next.x-edge.x)*.37,y=edge.y+(next.y-edge.y)*.37;
  const cx=(x+other.x+(otherNext.x-other.x)*.37)/2,cy=(y+other.y+(otherNext.y-other.y)*.37)/2;
  const direction=new THREE.Vector3(x-cx,0,-y+cy),length=direction.length();
  const ray=new THREE.Raycaster(new THREE.Vector3(cx,(i+.7)*3.36/21,-cy),direction.normalize(),length-.003,length+.003);
  // Restrict to the side joint; hidden facade geometry can sit inside the stair body.
  expect(ray.intersectObject(root,true).length,`curve segment ${i} ${side}`).toBe(1);
 }
});
test('porch brickwork meets the deck without coincident front faces',async()=>{
 const root=await model('front_exterior_v3_compact.glb');
 for(const x of [-6.137,5.137,7.137])for(const z of [-.09,-.16]){
  const ray=new THREE.Raycaster(new THREE.Vector3(x,z,2.6),new THREE.Vector3(0,0,-1),0,.45);
  expect(ray.intersectObject(root,true).length,`porch seam ${x} ${z}`).toBe(1);
 }
});
test('brick courses continue onto both porch end walls',async()=>{
 const root=await model('front_exterior_v3_compact.glb');
 for(const side of [-1,1]){
  const ray=new THREE.Raycaster(new THREE.Vector3(side*8.7,-.58,1.13),new THREE.Vector3(-side,0,0),0,.6);
  const hits=ray.intersectObject(root,true);expect(hits.length).toBeGreaterThan(0);
  expect(Math.abs(hits[0].point.x)).toBeGreaterThan(8.26);
 }
});

test('ceiling rails continue across landing and security door headers',async()=>{
 const hall=await model('connected_hall_v6_compact.glb');
 for(const [x,y,dx,dy] of [[.2,9.4,0,1],[-5.8,8.5,-1,0],[5.8,8.5,1,0]]){
  const hits=new THREE.Raycaster(new THREE.Vector3(x,6.97,-y),new THREE.Vector3(dx,0,-dy),0,.5).intersectObject(hall,true);
  expect(hits.length).toBeGreaterThan(0);expect(hits[0].distance).toBeLessThan(.27);
 }
 const corridor=await model('security_hall_v1_compact.glb');
 for(const x of [-3,3.2]){
  const hits=new THREE.Raycaster(new THREE.Vector3(x,3.03,-5),new THREE.Vector3(0,0,-1),0,.5).intersectObject(corridor,true);
  expect(hits.length).toBeGreaterThan(0);expect(hits[0].distance).toBeLessThan(.27);
 }
});
