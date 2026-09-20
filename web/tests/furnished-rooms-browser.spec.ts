import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';

for(const id of ['library','kitchen','dining_room','garage','pantry'])test(id+' furnished interior renders and its aisle is walkable',async({page})=>{
 test.setTimeout(90000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room='+id);await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 const room=createHouseRuntime(id).rooms.find(r=>r.id===id)!;
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');
 async function aim(x:number,y:number){
  const q=toWorld({x,y,height:0},room),p=await state(),target=-Math.atan2(q.x-p.x,q.y-p.y);
  const wrap=(n:number)=>Math.atan2(Math.sin(n),Math.cos(n));let delta=wrap(target-p.yaw);
  for(let i=0;i<12&&Math.abs(delta)>.02;i++){
   const part=Math.max(-.65,Math.min(.65,delta));await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650-part/.0022,430,{steps:4});await page.mouse.up();
   await expect.poll(async()=>Math.abs(wrap(target-(await state()).yaw)),{intervals:[50]}).toBeLessThan(Math.abs(delta)-.003);delta=wrap(target-(await state()).yaw);
  }
 }
 async function go(x:number,y:number){
  await aim(x,y);const p=await state(),q=toWorld({x,y,height:0},room),dx=q.x-p.x,dy=q.y-p.y,d=Math.hypot(dx,dy);
  await page.keyboard.down('w');try{await expect.poll(async()=>{const s=await state();return ((s.x-p.x)*dx+(s.y-p.y)*dy)/d;},{timeout:15000,intervals:[50]}).toBeGreaterThan(d-.13);}finally{await page.keyboard.up('w');}
 }
 if(id==='library'){await go(-4.5,1.2);await aim(0,4.7);}
 if(id==='kitchen'){await go(0,2.9);await aim(0,5);}
 if(id==='dining_room'){await go(-8.7,1);await go(-3.5,1);await aim(0,3.5);}
 if(id==='garage'){await go(4.8,4);await aim(8.45,4.6);await page.screenshot({path:'test-results/garage-car.png'});await go(4.8,2.2);await go(12,2.2);await go(12,2.9);await aim(12,4.22);}
 if(id==='pantry'){await go(0,2.9);await aim(1.4,4.9);}
 expect((await state()).room).toBe(id);expect(errors).toEqual([]);
 await page.screenshot({path:`test-results/${id}-furnished.png`});
});
