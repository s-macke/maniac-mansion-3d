import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
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
