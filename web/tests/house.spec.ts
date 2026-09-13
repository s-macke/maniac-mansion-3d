import {test,expect} from '@playwright/test';
import {toWorld,toLocal} from '../lib/house/placement';
import {roomDistance,nearbyRooms} from '../lib/house/visibility';
import {createHouseRuntime} from '../lib/house/runtime';
const {navigation,START,moveWalker}=createHouseRuntime('hall');
const unit={id:'test',definition:'test',position:[10,-7,4],yaw:Math.PI/2};
const bounds={min:[-2,-3,0],max:[2,3,4]};
test('room placement rotates coordinates and retains floor elevation',()=>{
 const q=toWorld({x:2,y:3,height:1},unit);
 expect(q.x).toBeCloseTo(7);expect(q.y).toBeCloseTo(-5);expect(q.height).toBe(5);
 const p=toLocal(q,unit);expect(p.x).toBeCloseTo(2);expect(p.y).toBeCloseTo(3);expect(p.height).toBe(1);
 expect(roomDistance(q,unit,bounds)).toBeCloseTo(0);
});
test('nearby loading accounts for room size, rotation and unload hysteresis',()=>{
 const rooms=[unit],defs={test:{bounds}},loaded=new Set(['test']);
 const point=toWorld({x:29,y:0,height:0},unit); // 27m beyond room boundary
 expect(nearbyRooms(point,rooms,defs,new Set(),24,32).size).toBe(0);
 expect(nearbyRooms(point,rooms,defs,loaded,24,32).has('test')).toBe(true);
 expect(nearbyRooms(toWorld({x:40,y:0,height:0},unit),rooms,defs,loaded,24,32).size).toBe(0);
});
test('house navigation rejects empty space and resolves both hall elevations',()=>{
 expect(navigation.canStand({x:100,y:100},0)).toBe(false);
 expect(navigation.floorHeight({x:100,y:100},0)).toBeNaN();
 expect(navigation.zone(START)).toBe('Entrance hall');
 expect(navigation.floorHeight({x:-3,y:5.8},0)).toBe(0);
 expect(navigation.floorHeight({x:-4.5,y:8},3.36)).toBe(3.36);
 expect(moveWalker(START,-100,0).x).toBeGreaterThan(-5.85);
});
