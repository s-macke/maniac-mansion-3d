import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
test('painted panel starts shut and stairs lead continuously to the wire attic and back',()=>{
 const v=createHouseRuntime('typewriter_room'),panel=v.graph.outgoing(v.activeSpace).find(e=>e.from.port.id==='hidden_panel')!,door=v.portalDoor(panel)!;
 expect(door.amount).toBe(0);expect(door.def.label).toBe('Painted wall panel');
 expect(v.definitions.typewriter_room.geometry!.sharedAssets!.some(s=>s.asset==='Concealed_leaf'&&s.doorNode==='Door_hidden_panel')).toBe(true);
 let p={x:188,y:2.6,height:10.08};expect(v.moveWalker(p,1,0).crossed).toBe(false);
 door.amount=door.target=1;p=v.moveWalker(p,1,0);expect(v.activeRoom).toBe('attic_stairs');
 const r=v.rooms.find(r=>r.id==='attic_stairs')!,g=v.definitions.attic_stairs.geometry!,s=g.stairs as {y0:number;y1:number;rise:number};
 const go=(y:number,h:number)=>{const q=toWorld({x:0,y,height:h},r);p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(p.x).toBeCloseTo(q.x);expect(p.y).toBeCloseTo(q.y);expect(p.height).toBeCloseTo(q.height,1);};
 go(.6,0);for(let i=0;i<=80;i++)go(s.y0+(s.y1-s.y0)*i/80,s.rise*i/80);
 go(5.7,3.36);p=v.moveWalker(p,0,.9);expect(v.activeRoom).toBe('wire_attic');expect(p.height).toBeCloseTo(13.44);
 p=v.moveWalker(p,0,-.9);expect(v.activeRoom).toBe('attic_stairs');
 for(let i=80;i>=0;i--)go(s.y0+(s.y1-s.y0)*i/80,s.rise*i/80);
 go(.6,0);p=v.moveWalker(p,0,-1);expect(v.activeRoom).toBe('typewriter_room');expect(p.height).toBeCloseTo(10.08);
 expect(v.graph.outgoing('wire_attic').map(e=>e.to.room.id)).toEqual(['attic_stairs']);
});
