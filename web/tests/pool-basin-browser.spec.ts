import {test,expect} from '@playwright/test';
test('drain the pool, walk its basin, climb out and refill without changing room',async({page})=>{
 test.setTimeout(180000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=pool');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');
 async function aim(x:number,y:number){
  const p=await state(),target=-Math.atan2(x-p.x,y-p.y);let delta=target-p.yaw;
  const wrap=(n:number)=>Math.atan2(Math.sin(n),Math.cos(n));delta=wrap(delta);
  for(let i=0;i<10&&Math.abs(delta)>.02;i++){
   const part=Math.max(-.65,Math.min(.65,delta));await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650-part/.0022,430,{steps:4});await page.mouse.up();
   await expect.poll(async()=>Math.abs(wrap(target-(await state()).yaw)),{intervals:[50]}).toBeLessThan(Math.abs(delta)-.003);delta=wrap(target-(await state()).yaw);
  }
 }
 async function go(x:number,y:number){
  await aim(x,y);const p=await state(),dx=x-p.x,dy=y-p.y,d=Math.hypot(dx,dy);if(d<.16)return;
  await page.keyboard.down('w');try{await expect.poll(async()=>{const q=await state();return ((q.x-p.x)*dx+(q.y-p.y)*dy)/d;},{timeout:18000,intervals:[50]}).toBeGreaterThan(d-.13);}finally{await page.keyboard.up('w');}
 }



 await aim(-16.37,28);
 await page.screenshot({path:'test-results/pool-sky-entry.png'});
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,160,{steps:5});await page.mouse.up();
 await page.screenshot({path:'test-results/pool-sky-overhead.png'});
 await page.mouse.move(650,160);await page.mouse.down();await page.mouse.move(650,430,{steps:5});await page.mouse.up();
 await go(-10.17,40.9);await aim(-14.37,39.1);
 await expect(page.locator('.door-action')).toContainText('Drain pool');await page.keyboard.press('e');
 await expect.poll(async()=>(await state()).poolDrained).toBe(true);
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,600,{steps:5});await page.mouse.up();
 await page.screenshot({path:'test-results/pool-drained.png'});
 await page.mouse.move(650,600);await page.mouse.down();await page.mouse.move(650,430,{steps:5});await page.mouse.up();
 await go(-10.17,34.7);await go(-17.37,34.85);await aim(-17.37,25);
 await page.screenshot({path:'test-results/pool-sky-far-rim.png'});
 await aim(-17.37,36.46);
 await expect(page.locator('.door-action')).toContainText('Climb into pool');await page.locator('.door-action').click();
 await expect.poll(async()=>(await state()).poolClimbing).toBe(true);
 await expect.poll(async()=>(await state()).poolClimbing,{timeout:12000}).toBe(false);
 expect((await state()).room).toBe('pool');expect((await state()).height).toBeCloseTo(-2.8);
 await go(-15.37,39.1);await aim(-17.37,36.16);await page.screenshot({path:'test-results/pool-basin-inside.png'});
 await expect(page.locator('.door-action')).toHaveCount(0);
 await aim(-21.02,36.85);await page.screenshot({path:'test-results/pool-reactor.png'});
 await go(-17.37,36.95);await aim(-17.37,36.16);
 await expect(page.locator('.door-action')).toContainText('Climb out of pool');await page.keyboard.press('e');
 await expect.poll(async()=>(await state()).poolClimbing).toBe(true);
 await expect.poll(async()=>(await state()).poolClimbing,{timeout:12000}).toBe(false);
 expect((await state()).height).toBeCloseTo(0);
 await go(-14.37,34.7);await aim(-14.37,39.1);
 await expect(page.locator('.door-action')).toContainText('Refill pool');await page.locator('.door-action').click();
 await expect.poll(async()=>(await state()).poolDrained).toBe(false);
 await page.screenshot({path:'test-results/pool-refilled.png'});expect(errors).toEqual([]);
});
