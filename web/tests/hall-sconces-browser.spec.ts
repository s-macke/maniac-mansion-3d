import {test,expect} from '@playwright/test';
test('hall sconces have visible depth from front and side approaches',async({page})=>{
 test.setTimeout(180000);
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=hall');await expect(page.locator('.status')).toHaveText('EXPLORING', {timeout:45000});
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
 await go(-4.65,4.3);await aim(-4.62,6.04);
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,220,{steps:5});await page.mouse.up();
 await page.screenshot({path:'test-results/hall-sconce-front.png'});
 await page.mouse.move(650,220);await page.mouse.down();await page.mouse.move(650,430,{steps:5});await page.mouse.up();
 await go(-5.4,4.3);await aim(-4.62,6.04);
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,240,{steps:5});await page.mouse.up();
 await page.screenshot({path:'test-results/hall-sconce-side.png'});
 expect(errors).toEqual([]);
});
