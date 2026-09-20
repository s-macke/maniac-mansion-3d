import {test,expect} from '@playwright/test';
import {toWorld,toLocal} from '../lib/house/placement';
import {neighboringRooms} from '../lib/house/visibility';
import {createHouseRuntime} from '../lib/house/runtime';
const {navigation,START,moveWalker}=createHouseRuntime('hall');
const unit={id:'test',definition:'test',position:[10,-7,4],yaw:Math.PI/2};
test('room placement rotates coordinates and retains floor elevation',()=>{
 const q=toWorld({x:2,y:3,height:1},unit);
 expect(q.x).toBeCloseTo(7);expect(q.y).toBeCloseTo(-5);expect(q.height).toBe(5);
 const p=toLocal(q,unit);expect(p.x).toBeCloseTo(2);expect(p.y).toBeCloseTo(3);expect(p.height).toBe(1);
});
test('loading follows connections and includes continuous outdoor groups',()=>{
 const v=createHouseRuntime('hall'),neighbors=neighboringRooms(v.graph,v.activeSpace);
 expect([...neighbors].sort()).toEqual(['cellar','front_exterior','hall','kitchen','living_room','music_room','plant_room','security_hall']);
 expect(neighbors.has('dining_room')).toBe(false);
 expect([...neighboringRooms(v.graph,'pool_garage')].sort()).toEqual(['garage','meteor_chamber','pantry','pool']);
});
test('house navigation rejects empty space and resolves both hall elevations',()=>{
 expect(navigation.canStand({x:100,y:100},0)).toBe(false);
 expect(navigation.floorHeight({x:100,y:100},0)).toBeNaN();
 expect(navigation.zone(START)).toBe('Entrance hall');
 expect(navigation.floorHeight({x:-3,y:5.8},0)).toBe(0);
 expect(navigation.floorHeight({x:-4.5,y:8},3.36)).toBe(3.36);
 expect(moveWalker(START,-100,0).x).toBeGreaterThan(-5.85);
});
