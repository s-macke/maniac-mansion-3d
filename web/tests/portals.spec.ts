import {test,expect} from '@playwright/test';
import * as THREE from 'three';
import data from '../lib/house/generated.json' with {type:'json'};
import {createHouseRuntime} from '../lib/house/runtime';
import {mapThrough,portalCoordinates} from '../lib/house/portals';
import {portalCamera,portalFootprint,entrancePlane,portalMatrix} from '../lib/house/portal-renderer';
import type {HouseData} from '../lib/house/types';

function fixture(){
 const source:HouseData=structuredClone(data);
 const living=source.rooms.find(r=>r.id==='living_room')!;living.position=[100,90,4];living.yaw=Math.PI/2;
 const v=createHouseRuntime('hall',source),edge=v.graph.outgoing('hall').find(p=>p.to.room.id==='living_room')!;
 return {v,edge};
}
test('translated rotated portal preserves displacement, elevation and facing, in both directions',()=>{
 const {v,edge}=fixture(),door=v.portalDoor(edge)!;door.amount=door.target=1;
 const start={x:4.5,y:3.15,height:0},end={x:8,y:3.15,height:0},expected=mapThrough(end,edge);
 const moved=v.moveWalker(start,3.5,0);
 expect(v.activeRoom).toBe('living_room');expect(moved.x).toBeCloseTo(expected.x,4);expect(moved.y).toBeCloseTo(expected.y,4);expect(moved.height).toBe(4);expect(moved.yawDelta).toBeCloseTo(Math.PI/2);
 const back=v.moveWalker(moved,0,-3.5);expect(v.activeRoom).toBe('hall');expect(back.x).toBeCloseTo(start.x,4);expect(back.y).toBeCloseTo(start.y,4);expect(back.height).toBe(0);
 const camera=new THREE.PerspectiveCamera(68,1.4,.05,60);camera.position.set(start.x,1.62,-start.y);camera.lookAt(8,1.62,-3.15);camera.updateMatrixWorld();
 const other=portalCamera(camera,edge),p=mapThrough({x:camera.position.x,y:-camera.position.z,height:camera.position.y},edge);
 expect(other.position.distanceTo(new THREE.Vector3(p.x,p.height,-p.y))).toBeLessThan(1e-6);
 const reverse=v.graph.portals.find(p=>p.key===edge.reverse)!;
 expect(portalCamera(other,reverse).position.distanceTo(camera.position)).toBeLessThan(1e-6);
 const roundtrip=portalMatrix(reverse).multiply(portalMatrix(edge));expect(roundtrip.elements.every((x,i)=>Math.abs(x-new THREE.Matrix4().elements[i])<1e-6)).toBe(true);
});
test('closed or unloaded destinations cannot be crossed; reset restores the starting space',()=>{
 const {v,edge}=fixture(),start={x:4.5,y:3.15,height:0};
 expect(v.moveWalker(start,4,0).x).toBeLessThan(6.4);expect(v.activeRoom).toBe('hall');
 const d=v.portalDoor(edge)!;d.amount=d.target=1;v.requireLoadedRooms();v.setRoomLoaded('hall',true);
 expect(v.moveWalker(start,4,0).x).toBeLessThan(6.4);expect(v.activeRoom).toBe('hall');
 v.setRoomLoaded('living_room',true);v.moveWalker(start,3.5,0);expect(v.activeRoom).toBe('living_room');v.resetSpace();expect(v.activeRoom).toBe('hall');
});
test('overlapping unrelated rooms never supply floors or collisions to the current space',()=>{
 const source:HouseData=structuredClone(data),hall=source.rooms.find(r=>r.id==='hall')!;
 const kitchen=source.rooms.find(r=>r.id==='kitchen')!;kitchen.position=[...hall.position];kitchen.yaw=0;
 const v=createHouseRuntime('hall',source),baseline=createHouseRuntime('hall');
 for(const p of [{x:0,y:2,height:0},{x:0,y:12,height:0},{x:-4.5,y:8,height:3.36}]){
  expect(v.navigation.canStand(p,p.height)).toBe(baseline.navigation.canStand(p,p.height));
 }
 expect(v.activeSpace).toBe('hall');
});
test('pool and garage share a continuous space and preserve world movement',()=>{
 const v=createHouseRuntime('pool'),edge=v.graph.outgoing(v.activeSpace).find(p=>p.to.room.id==='garage')!;
 expect(edge.continuous).toBe(true);expect(v.graph.members(v.activeSpace).map(r=>r.id)).toEqual(['pool','garage']);
 const start={x:edge.from.point.x-edge.from.normal.x,y:edge.from.point.y-edge.from.normal.y,height:0};
 const end=v.moveWalker(start,edge.from.normal.x*2,edge.from.normal.y*2);
 expect(end.x).toBeCloseTo(start.x+edge.from.normal.x*2,3);expect(end.y).toBeCloseTo(start.y+edge.from.normal.y*2,3);expect(end.yawDelta).toBe(0);expect(v.activeSpace).toBe('pool_garage');
});
test('portal camera clipping keeps the destination interior and culls offscreen apertures',()=>{
 const {edge}=fixture(),camera=new THREE.PerspectiveCamera(68,1.4,.05,60);camera.position.set(4.5,1.62,-3.15);camera.lookAt(7,1.62,-3.15);camera.updateMatrixWorld();
 expect(portalFootprint(camera,edge)).toBeGreaterThan(0);
 camera.lookAt(0,1.62,-3.15);camera.updateMatrixWorld();expect(portalFootprint(camera,edge)).toBe(0);
 const plane=entrancePlane(edge),inside=mapThrough({x:7,y:3.15,height:1},edge),outside=mapThrough({x:5,y:3.15,height:1},edge);
 expect(plane.distanceToPoint(new THREE.Vector3(inside.x,inside.height,-inside.y))).toBeGreaterThan(0);
 expect(plane.distanceToPoint(new THREE.Vector3(outside.x,outside.height,-outside.y))).toBeLessThan(0);
 expect(portalCoordinates({x:6.4,y:3.15,height:0},edge).along).toBeCloseTo(0);
});
