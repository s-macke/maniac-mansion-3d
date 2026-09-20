import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';

test('furniture blocks walking while each furnished room retains a continuous circulation route',()=>{
 const cases=[
  {id:'garage',blocked:[[8.45,4.6],[7.9,7]],route:[[2,4],[4.8,4],[4.8,2.2],[12,2.2],[12,2.9],[12,2.2],[4.8,2.2],[4.8,4],[2,4]]},
  {id:'pantry',blocked:[[1.4,4.9]],route:[[-1.6,2.9],[1.4,2.9],[1.4,4.1],[-.8,4.1],[-.8,3],[-1.6,2.9]]},
  {id:'library',blocked:[[0,3.3],[4.85,2.1],[0,4.9]],route:[[-4.5,2.8],[-3,1],[2.5,1],[2.5,3.5],[2.5,1],[-3,1],[-4.5,2.8]]},
  {id:'kitchen',blocked:[[-1.8,4.6],[4.48,4.7]],route:[[-5,2.9],[5,2.9],[5,1],[-5,1],[-5,2.9]]},
  {id:'dining_room',blocked:[[0,2.8],[-7.65,2.8],[7.65,2.8]],route:[[-8.7,2.9],[-8.7,1],[8.7,1],[8.7,4.6],[-8.7,4.6],[-8.7,2.9]]},
 ];
 for(const c of cases){
  const v=createHouseRuntime(c.id),room=v.rooms.find(r=>r.id===c.id)!;
  const at=(a:number[])=>toWorld({x:a[0],y:a[1],height:0},room);
  expect(v.navigation.canStand(v.START,0),c.id+' spawn').toBe(true);
  for(const q of c.blocked)expect(v.navigation.canStand(at(q),0),c.id+' furniture '+q).toBe(false);
  let p=at(c.route[0]);
  for(const q of c.route.slice(1).map(at)){
   p=v.moveWalker(p,q.x-p.x,q.y-p.y);
   expect(Math.hypot(p.x-q.x,p.y-q.y),c.id+' aisle').toBeLessThan(.03);
  }
 }
});
