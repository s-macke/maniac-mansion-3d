import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {mapThrough} from '../lib/house/portals';
test('cellar extension portals have one closed shared door and allow return travel',()=>{
 const reference=createHouseRuntime();
 for(const edge of reference.graph.portals.filter(e=>['dungeon','outer_lab','main_lab','meteor_chamber'].includes(e.to.room.id)&&e.key.endsWith(':0'))){
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
test('cellar route follows door order and uses the requested garage escape ladder',()=>{
 const v=createHouseRuntime();
 // Anchor the route to the artwork, not just semantic room IDs.
 expect(v.definitions.outer_lab.backgrounds).toEqual(['031']); // big green screen
 expect(v.definitions.main_lab.backgrounds).toEqual(['030']); // three apparatus seats/tubes
 expect(v.definitions.meteor_chamber.backgrounds).toEqual(['051']); // suspended meteor apparatus
 const neighbors=(id:string)=>v.graph.outgoing(id).map(e=>e.to.room.id).sort();
 expect(neighbors('cellar')).toEqual(['dungeon','hall']);
 expect(neighbors('dungeon')).toEqual(['cellar','outer_lab']);
 expect(neighbors('outer_lab')).toEqual(['dungeon','main_lab']);
 expect(neighbors('main_lab')).toEqual(['meteor_chamber','outer_lab']);
 expect(neighbors('meteor_chamber')).toEqual(['garage','main_lab']);
 expect(neighbors('under_house')).toEqual(['front_exterior']);
 expect(v.definitions.meteor_chamber.ports.some(p=>p.id==='exit_door')).toBe(false);
});
