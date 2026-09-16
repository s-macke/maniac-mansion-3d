import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {createCrawls} from '../lib/house/crawls';
import {toWorld} from '../lib/house/placement';
import {mapThrough,portalCoordinates} from '../lib/house/portals';
test('hall cellar door starts closed; descend and return along the cellar stairs',()=>{
 const v=createHouseRuntime('hall');let p={x:3.12,y:6,height:0};
 expect(v.moveWalker(p,0,1).crossed).toBe(false);
 const d=v.doors.items.find(d=>d.key==='hall:cellar_door')!;d.amount=d.target=1;
 p=v.moveWalker(p,0,1);expect(v.activeRoom).toBe('cellar');
 const room=v.rooms.find(r=>r.id==='cellar')!,s=v.definitions.cellar.geometry!.stairs as {x0:number;x1:number;y0:number;y1:number;rise:number},x=(s.x0+s.x1)/2;
 const go=(y:number,h:number)=>{const q=toWorld({x,y,height:h},room);p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(p.x).toBeCloseTo(q.x);expect(p.y).toBeCloseTo(q.y);expect(p.height).toBeCloseTo(q.height,1);};
 for(let i=80;i>=0;i--)go(s.y0+(s.y1-s.y0)*i/80,s.rise*i/80);
 go(.6,0);expect(p.height).toBeCloseTo(-3.36);
 for(let i=0;i<=80;i++)go(s.y0+(s.y1-s.y0)*i/80,s.rise*i/80);
 go(5.7,3.36);p=v.moveWalker(p,0,.9);expect(v.activeRoom).toBe('hall');expect(p.height).toBeCloseTo(0);
 expect(v.graph.outgoing('cellar').map(e=>e.to.room.id)).toEqual(['hall']);
});
test('grating opens, crouched crossing is continuous and returns outside safely',()=>{
 const v=createHouseRuntime('front_exterior'),c=createCrawls(v),link=v.house.crawls![0];
 for(const forward of [true,false]){
  const end=forward?link.a:link.b,room=v.rooms.find(r=>r.id===end.room)!,edge=v.graph.outgoing(v.activeSpace).find(e=>e.from.port.id===end.port)!;
  const reverse=v.graph.portals.find(e=>e.key===edge.reverse)!;
  let p=toWorld(end.landing,room),yaw=-Math.atan2(edge.from.point.x-p.x,edge.from.point.y-p.y);
  expect(v.navigation.canStand(p,p.height)).toBe(true);
  let choice=c.target(p,yaw)!;expect(choice.ready).toBe(true);
  if(forward){expect(c.begin(choice,p,yaw)).toBe(false);v.doors.update(2,p);choice=c.target(p,yaw)!;}
  expect(c.begin(choice,p,yaw)).toBe(true);let before=p,eye=1.62,switches=0;
  for(let i=0;i<2000&&c.active;i++){
   const oldRoom=v.activeRoom,r=c.step(.01)!;p=r.walker;yaw+=r.yawDelta;const canonical=v.activeRoom===end.room?p:mapThrough(p,reverse);
   expect(Math.hypot(canonical.x-before.x,canonical.y-before.y,canonical.height+r.eyeHeight-before.height-eye)).toBeLessThan(.04);
   if(v.activeRoom!==oldRoom)switches++;
   if(Math.abs(portalCoordinates(canonical,edge).along)<.1){expect(canonical.height+r.eyeHeight).toBeGreaterThan(edge.from.point.height);expect(canonical.height+r.eyeHeight).toBeLessThan(edge.from.point.height+.72);}
   before=canonical;eye=r.eyeHeight;
  }
  expect(c.active).toBe(false);expect(switches).toBe(1);expect(eye).toBeCloseTo(1.62);expect(v.navigation.canStand(p,p.height)).toBe(true);
 }
 expect(v.activeRoom).toBe('front_exterior');expect(v.graph.outgoing('under_house').map(e=>e.to.room.id)).toEqual(['front_exterior']);
});
test('crawl waits for loaded assets and excludes normal standing traversal',()=>{
 const v=createHouseRuntime('under_house'),c=createCrawls(v),end=v.house.crawls![0].b,room=v.rooms.find(r=>r.id===end.room)!,p=toWorld(end.landing,room);
 const d=v.doors.items.find(d=>d.def.port==='under_porch_grating')!;d.amount=d.target=1;
 expect(v.moveWalker(p,-3,0).crossed).toBe(false);
 v.requireLoadedRooms();v.setRoomLoaded('under_house',true);const choice=c.target(p,Math.PI/2)!;expect(choice.ready).toBe(false);expect(c.begin(choice,p,Math.PI/2)).toBe(false);
});
