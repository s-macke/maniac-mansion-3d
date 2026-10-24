import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {createHouseRuntime} from '../lib/house/runtime';
import {mapThrough} from '../lib/house/portals';
import {toWorld} from '../lib/house/placement';
const ids=['windowed_hall','upper_corridor','green_bedroom','heart_bedroom','radio_bedroom','mummy_room','typewriter_room','mummy_bathroom','photo_room'];
test('upper-floor portals have one closed shared door and allow return travel',()=>{
 const reference=createHouseRuntime();
 for(const edge of reference.graph.portals.filter(e=>ids.includes(e.to.room.id)&&e.key.endsWith(':0')&&!(e.from.room.id==='security_hall'&&e.from.port.id==='higher_floor'))){
  const v=createHouseRuntime(edge.from.room.id),door=v.portalDoor(edge)!;
  expect(door,edge.key).toBeTruthy();expect(door.amount).toBe(0);
  const owners=v.doors.items.filter(d=>(d.room.id===edge.from.room.id&&d.def.port===edge.from.port.id)||(d.room.id===edge.to.room.id&&d.def.port===edge.to.port.id));expect(owners).toHaveLength(1);
  const n=edge.from.normal,a={x:edge.from.point.x-n.x*.5,y:edge.from.point.y-n.y*.5,height:edge.from.point.height};
  expect(v.moveWalker(a,n.x,n.y).crossed,edge.to.room.id+' closed').toBe(false);
  door.amount=door.target=1;
  const b=v.moveWalker(a,n.x,n.y),expected=mapThrough({x:a.x+n.x,y:a.y+n.y,height:a.height},edge);
  expect(v.activeRoom).toBe(edge.to.room.id);expect(Math.hypot(b.x-expected.x,b.y-expected.y)).toBeLessThan(.02);expect(b.height).toBeCloseTo(expected.height);
  const reverse=v.graph.portals.find(e=>e.key===edge.reverse)!;
  const back=v.moveWalker(b,reverse.from.normal.x,reverse.from.normal.y);
  expect(v.activeRoom).toBe(edge.from.room.id);expect(Math.hypot(back.x-a.x,back.y-a.y)).toBeLessThan(.02);expect(back.height).toBeCloseTo(a.height,1);
 }
});
test('both stair flights lead up through their portals and back down',()=>{
 for(const id of ['security_hall','windowed_hall']){
  const v=createHouseRuntime(id),room=v.rooms.find(r=>r.id===id)!,g=v.definitions[room.definition].geometry!;
  const s=g.stairs as {x0:number;x1:number;y0:number;y1:number;rise:number};
  const at=(x:number,y:number,height=0)=>toWorld({x,y,height},room),x=(s.x0+s.x1)/2;
  let p=at(x,s.y0-.45);const edge=v.graph.outgoing(v.activeSpace).find(e=>e.from.port.id==='higher_floor')!;const door=v.portalDoor(edge);if(door)door.amount=door.target=1;
  const go=(y:number,h:number)=>{const q=at(x,y,h);p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(Math.hypot(p.x-q.x,p.y-q.y)).toBeLessThan(.02);expect(p.height).toBeCloseTo(q.height,1);};
  for(let i=0;i<=80;i++)go(s.y0+(s.y1-s.y0)*i/80,s.rise*i/80);
  go(Number(g.depth)-.4,s.rise);p=v.moveWalker(p,0,.9);expect(v.activeRoom).toBe(edge.to.room.id);
  const reverse=v.graph.portals.find(e=>e.key===edge.reverse)!;p=v.moveWalker(p,reverse.from.normal.x*.9,reverse.from.normal.y*.9);expect(v.activeRoom).toBe(id);
  for(let i=80;i>=0;i--)go(s.y0+(s.y1-s.y0)*i/80,s.rise*i/80);
  go(s.y0-.45,0);
 }
});
test('new shell GLBs have supporting floors and clear stair headroom',async()=>{
 const v=createHouseRuntime();
 for(const id of [...ids,'security_hall','attic_stairs','wire_attic','cellar','under_house','dungeon','outer_lab','main_lab','meteor_chamber']){
  const room=v.rooms.find(r=>r.id===id)!,def=v.definitions[room.definition],bytes=await readFile('../generated/models/rooms/'+def.asset.split('/').at(-1));
  const root=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;root.updateMatrixWorld(true);
  const g=def.geometry!,s=g.stairs as {x0:number;x1:number;y0:number;y1:number;rise:number;segments:number}|undefined;
  const samples=[{x:def.spawn.x,y:def.spawn.y,h:def.spawn.height},...(s?Array.from({length:20},(_,i)=>({x:(s.x0+s.x1)/2,y:s.y0+(s.y1-s.y0)*(i+.5)/20,h:s.rise*(i+.5)/20})):[])];
  const d=g.descendingStairs as {x0:number;x1:number;y0:number;y1:number;drop:number;segments:number}|undefined;
  if(d)for(let i=0;i<d.segments;i++)samples.push({x:d.x0+(d.x1-d.x0)*(i+.5)/d.segments,y:(d.y0+d.y1)/2,h:-d.drop*(i+.5)/d.segments});
  const ray=new THREE.Raycaster();
  for(const p of samples){
   ray.set(new THREE.Vector3(p.x,p.h+1.62,-p.y),new THREE.Vector3(0,-1,0));ray.far=1.9;
   const hits=ray.intersectObject(root,true);expect(hits.length,id+' floor '+JSON.stringify(p)).toBeGreaterThan(0);expect(Math.abs(hits[0].point.y-p.h),id+' floor height').toBeLessThan(.2);
   ray.ray.direction.set(0,1,0);ray.far=.55;expect(ray.intersectObject(root,true),id+' headroom').toHaveLength(0);
  }
 }
});
test('bedroom slots and missing side rooms follow the corrected route',()=>{
 const v=createHouseRuntime();
 const bedrooms=v.graph.outgoing('upper_corridor').filter(e=>e.from.port.outward[1]===1).sort((a,b)=>a.from.port.position[0]-b.from.port.position[0]);
 expect(bedrooms.map(e=>e.to.room.id)).toEqual(['radio_bedroom','heart_bedroom','green_bedroom','mummy_room']);
 for(const [from,to,level] of [['mummy_room','mummy_bathroom',10.08],['windowed_hall','photo_room',6.72]] as const){
  const edge=v.graph.outgoing(from).find(e=>e.to.room.id===to)!;expect(edge).toBeTruthy();expect(edge.from.point.height).toBeCloseTo(level);expect(edge.to.point.height).toBeCloseTo(level);
 }
 expect(v.graph.outgoing('mummy_bathroom').map(e=>e.to.room.id)).toEqual(['mummy_room']);
 expect(v.graph.outgoing('photo_room').map(e=>e.to.room.id)).toEqual(['windowed_hall']);
});

// The lower flight must emerge beside the railing, not through an invented door.
test('security stairs arrive from the right with a quarter-turn and a clear landing',()=>{
 const v=createHouseRuntime('security_hall');
 const edge=v.graph.outgoing(v.activeSpace).find(e=>e.from.port.id==='higher_floor')!;
 expect(edge.to.port.position).toEqual([6.4,5.35,-1.68]);expect(edge.to.port.outward).toEqual([1,0]);
 expect(Math.abs(Math.atan2(Math.sin(edge.yaw),Math.cos(edge.yaw)))).toBeCloseTo(Math.PI/2);
 expect(v.portalDoor(edge)).toBeUndefined();
 let p={x:edge.from.point.x,y:edge.from.point.y-.25,height:edge.from.point.height};
 const start={...p};const crossed=v.moveWalker(p,0,.8);p=crossed;expect(v.activeRoom).toBe('windowed_hall');
 expect(Math.cos(crossed.yawDelta)).toBeCloseTo(0);expect(p.height).toBeCloseTo(5.04+.55/3.5*1.68,1);
 const r=v.rooms.find(r=>r.id==='windowed_hall')!;
 const go=(x:number,y:number)=>{const q=toWorld({x,y,height:0},r);p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(Math.hypot(p.x-q.x,p.y-q.y)).toBeLessThan(.03);};
 go(3,5.35);
 const stopped=v.moveWalker(p,0,-1);expect(stopped.y).toBeGreaterThan(4.84);
 go(2.35,5.35);expect(p.height).toBeCloseTo(6.72);go(2.35,4);go(2.35,5.35);go(5.9,5.35);
 const reverse=v.graph.portals.find(e=>e.key===edge.reverse)!;
 p=v.moveWalker(p,.75,0);expect(v.activeRoom).toBe('security_hall');
 expect(p.height).toBeCloseTo(start.height);expect(p.x).toBeCloseTo(start.x);
 const roundtrip=mapThrough(mapThrough(start,edge),reverse);
 expect(roundtrip.x).toBeCloseTo(start.x);expect(roundtrip.y).toBeCloseTo(start.y);expect(roundtrip.height).toBeCloseTo(start.height);
});

test('descending stairwell edges contain no coincident visible faces',async()=>{
 const bytes=await readFile('../generated/models/rooms/windowed_hall_v1_compact.glb');
 const root=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength) as ArrayBuffer,'')).scene;root.updateMatrixWorld(true);
 for(const x of [3.677,4.433,5.189])for(const z of [-.057,-.23])for(const side of [-1,1]){
  const ray=new THREE.Raycaster(new THREE.Vector3(x,z,-5.35),new THREE.Vector3(0,0,side),0,.55);
  expect(ray.intersectObject(root,true),`stair edge x=${x}, z=${z}, side=${side}`).toHaveLength(1);
 }
});
