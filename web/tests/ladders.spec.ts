import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {createLadders} from '../lib/house/ladders';
import {toWorld} from '../lib/house/placement';
import {mapThrough} from '../lib/house/portals';
import {EYE_HEIGHT} from '../lib/house/navigation';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {instantiateSharedAssets} from '../lib/house/shared-assets';
for(const id of ['heart_bedroom','radio_bedroom','typewriter_room','meteor_chamber'])test(`${id} climbs through a continuous hatch in both directions`,()=>{
 const v=createHouseRuntime(id),ladders=createLadders(v),link=v.house.ladders!.find(l=>l.lower.room===id)!;
 const edge=v.graph.portals.find(e=>e.from.room.id===id&&e.from.port.kind==='hatch')!,reverse=v.graph.portals.find(e=>e.key===edge.reverse)!;
 for(const up of [true,false]){
  const end=up?link.lower:link.upper,room=v.rooms.find(r=>r.id===end.room)!;
  let p=toWorld(end.landing,room),yaw=end.yaw+room.yaw;
  const choice=ladders.target(p,yaw)!;expect(choice.up).toBe(up);expect(choice.ready).toBe(true);expect(ladders.begin(choice,p,yaw)).toBe(true);
  let prior=up?p:mapThrough(p,reverse),switches=0;
  for(let i=0;i<1000&&ladders.active;i++){
   const before=v.activeRoom,result=ladders.step(.01)!;p=result.walker;yaw+=result.yawDelta;
   if(before!==v.activeRoom)switches++;
   const canonical=v.activeRoom===id?p:mapThrough(p,reverse);
   expect(Math.hypot(canonical.x-prior.x,canonical.y-prior.y,canonical.height-prior.height)).toBeLessThan(.06);
   expect(v.activeRoom===link.upper.room).toBe(canonical.height+EYE_HEIGHT>=edge.from.point.height);
   prior=canonical;
  }
  expect(ladders.active).toBe(false);expect(switches).toBe(1);
  const finish=up?link.upper:link.lower,expected=toWorld(finish.landing,v.rooms.find(r=>r.id===finish.room)!);
  expect(p.x).toBeCloseTo(expected.x);expect(p.y).toBeCloseTo(expected.y);expect(p.height).toBeCloseTo(expected.height);
  expect(v.navigation.canStand(p,p.height)).toBe(true);
 }
});
test('hatches block ordinary walking and wait for destination assets',()=>{
 const v=createHouseRuntime('safe_attic'),l=createLadders(v),link=v.house.ladders![0],room=v.rooms.find(r=>r.id==='safe_attic')!;
 const landing=toWorld(link.upper.landing,room),shaft=toWorld({...link.upper.shaft,height:0},room);
 expect(v.navigation.canStand(shaft,shaft.height)).toBe(false);
 const walked=v.moveWalker(landing,shaft.x-landing.x,shaft.y-landing.y);expect(Math.hypot(walked.x-shaft.x,walked.y-shaft.y)).toBeGreaterThan(.5);
 v.requireLoadedRooms();v.setRoomLoaded('safe_attic',true);
 const choice=l.target(landing,link.upper.yaw)!;expect(choice.ready).toBe(false);expect(l.begin(choice,landing,link.upper.yaw)).toBe(false);
 expect(l.target(landing,link.upper.yaw+Math.PI)).toBe(null);
});
test('shared ladder sections batch once and room GLBs leave the hatch clear',async()=>{
 const load=async(path:string)=>{const b=await readFile(path);return (await new GLTFLoader().parseAsync(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength) as ArrayBuffer,'')).scene;};
 const kit=await load('../generated/models/ladders/ladder_v1.glb'),v=createHouseRuntime();
 const geometries=new Set();
 for(const id of ['heart_bedroom','radio_bedroom','safe_attic','tentacle_room','typewriter_room','observatory','meteor_chamber','garage']){
  const def=v.definitions[id],root=new THREE.Group();instantiateSharedAssets(root,def,kit,'ladders');
  expect(root.children).toHaveLength(1);const batch=root.children[0] as THREE.InstancedMesh;expect(batch.isInstancedMesh).toBe(true);expect(batch.count).toBeGreaterThanOrEqual(12);geometries.add(batch.geometry);
  const shell=await load('../generated/models/rooms/'+def.asset.split('/').at(-1));shell.updateMatrixWorld(true);
  const hatch=def.ports.find(p=>p.kind==='hatch')!,[x,y,z]=hatch.position;
  const ray=new THREE.Raycaster(new THREE.Vector3(x,z-.35,-y),new THREE.Vector3(0,1,0),0,.7);
  expect(ray.intersectObject(shell,true),id+' hatch opening').toHaveLength(0);
 }
 expect(geometries.size).toBe(1);
});

test('garage hatch blocks ordinary walking while preserving the outdoor space',()=>{
 const v=createHouseRuntime('garage'),link=v.house.ladders!.find(l=>l.id==='garage_escape')!,r=v.rooms.find(r=>r.id==='garage')!;
 const landing=toWorld(link.upper.landing,r),shaft=toWorld({...link.upper.shaft,height:0},r);
 expect(v.activeSpace).toBe('pool_garage');expect(v.navigation.canStand(landing,0)).toBe(true);expect(v.navigation.canStand(shaft,0)).toBe(false);
 const walked=v.moveWalker(landing,shaft.x-landing.x,shaft.y-landing.y);
 expect(walked.crossed).toBe(false);expect(Math.hypot(walked.x-shaft.x,walked.y-shaft.y)).toBeGreaterThan(.4);
});
