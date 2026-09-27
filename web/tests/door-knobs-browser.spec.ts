import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
for(const id of ['dining_room','kitchen','hall'])test(id+' kitchen-dining door knob and swing review',async({page})=>{
 test.setTimeout(150000);
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Drag'));});
 await page.goto('/?room='+id);await expect(page.locator('.status')).toHaveText('EXPLORING', {timeout:45000});
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

 if(id==='hall'){
  await go(-4.65,1);await go(3.12,1);await go(3.12,4.6);await aim(3.12,6.5);
  await page.screenshot({path:'test-results/hall-cellar-handleless.png'});
  await go(3.12,1);await go(-3.72,1);await go(-3.72,4.6);await aim(-3.72,6.5);
  await page.screenshot({path:'test-results/hall-kitchen-door-closed.png'});
  await page.keyboard.press('e');await expect(page.locator('.door-action')).toContainText('Close');
  await expect.poll(async()=>(await state()).movingDoors).toHaveLength(0);
  await page.screenshot({path:'test-results/hall-kitchen-door-open.png'});return;
 }
 const x=id==='dining_room'?-9.6:6.4,stand=id==='dining_room'?-8.55:4.5;
 await go(stand,1.5);await go(stand,2.9);await aim(x,2.9);
 await page.screenshot({path:'test-results/'+id+'-door-closed.png'});
 await expect(page.locator('.door-action')).toContainText('Open');await page.keyboard.press('e');
 await expect(page.locator('.door-action')).toContainText('Close');
 await expect.poll(async()=>(await state()).movingDoors).toHaveLength(0);
 await page.screenshot({path:'test-results/'+id+'-door-open.png'});
 await expect(page.locator('.door-action')).toContainText('Close');
});
