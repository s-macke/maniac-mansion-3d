import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
test('boarded attic window exposes distant star geometry through the wall',async()=>{
 const bytes=await readFile('../generated/models/rooms/wire_attic_v1_compact.glb');
 const root=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;
 root.updateMatrixWorld(true);
 const origin=new THREE.Vector3(2.22,1.7,-2),factor=14.2/2.2;
 const x=(202.5-160)*8.16/240,z=1.58+(.5-45.5/101)*2.99;
 const star=new THREE.Vector3(2.22+factor*(x-2.22),1.7+factor*(z-1.7),-16.2);
 const hit=new THREE.Raycaster(origin,star.sub(origin).normalize(),0,40).intersectObject(root,true)[0];
 expect(hit.object.name).toBe('Attic_window_sky');expect(hit.distance).toBeGreaterThan(12);
 const mesh=hit.object as THREE.Mesh,col=mesh.geometry.attributes.color;
 expect(col.getX(hit.face!.a)).toBeGreaterThan(.9);
 for(const [x,z] of [[1,1.8],[3.4,2],[2.2,.8]]){
  const wall=new THREE.Raycaster(new THREE.Vector3(x,z,-3.9),new THREE.Vector3(0,0,-1),0,1).intersectObject(root,true);
  expect(wall.length).toBeGreaterThan(0);
 }
 // Upper plank crosses the top frame in projection, but sits wholly in front.
 const plankRay=new THREE.Raycaster(new THREE.Vector3(2.75,3.02,-3.8),new THREE.Vector3(0,0,-1),0,1);
 expect(plankRay.intersectObject(root,true)[0].distance).toBeLessThan(.27);
 plankRay.near=.3173;plankRay.far=.3177;
 expect(plankRay.intersectObject(root,true)).toHaveLength(1);
});
test('painted panel starts shut and opens onto a ladder shaft',()=>{
 const v=createHouseRuntime('typewriter_room'),panel=v.graph.outgoing(v.activeSpace).find(e=>e.from.port.id==='hidden_panel')!,door=v.portalDoor(panel)!;
 expect(door.amount).toBe(0);expect(door.def.label).toBe('Painted wall panel');
 expect(v.definitions.typewriter_room.geometry!.sharedAssets!.some(s=>s.asset==='Concealed_leaf'&&s.doorNode==='Door_hidden_panel')).toBe(true);
 let p={x:188,y:2.6,height:10.08};expect(v.moveWalker(p,1,0).crossed).toBe(false);
 door.amount=door.target=1;p=v.moveWalker(p,1,0);expect(v.activeRoom).toBe('attic_stairs');
 expect(v.definitions.attic_stairs.geometry!.stairs).toBeUndefined();
 expect(v.definitions.attic_stairs.geometry!.ladders).toHaveLength(1);
 const hatch=v.graph.outgoing('attic_stairs').find(e=>e.to.room.id==='wire_attic')!;
 expect(hatch.from.port.kind).toBe('hatch');expect(hatch.to.port.kind).toBe('hatch');
 const r=v.rooms.find(r=>r.id==='attic_stairs')!;
 const q=toWorld({x:0,y:.6,height:0},r);p=v.moveWalker(p,q.x-p.x,q.y-p.y);
 p=v.moveWalker(p,0,-1);expect(v.activeRoom).toBe('typewriter_room');expect(p.height).toBeCloseTo(10.08);
 expect(v.graph.outgoing('wire_attic').map(e=>e.to.room.id)).toEqual(['attic_stairs']);
});
