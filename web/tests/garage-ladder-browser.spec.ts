import {test,expect} from '@playwright/test';
test('meteor chamber ladder emerges through garage floor and returns seamlessly',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=meteor_chamber');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
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



 await go(496.4,2);await go(496.4,3.5);await aim(496.4,4.52);
 await page.mouse.move(650,600);await page.mouse.down();await page.mouse.move(650,220,{steps:8});await page.mouse.up();
 await expect(page.locator('.door-action')).toContainText('Climb up');
 await expect.poll(async()=>(await state()).portals.visibleRooms).toContain('garage');
 await page.screenshot({path:'test-results/garage-ladder-below.png'});
 await page.keyboard.press('e');await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe('garage');
 await expect.poll(async()=>(await state()).climbing,{timeout:15000}).toBe(false);
 expect((await state()).height).toBeCloseTo(0);
 await page.mouse.move(650,220);await page.mouse.down();await page.mouse.move(650,870,{steps:8});await page.mouse.up();
 await aim(-38.37,38.9);await expect(page.locator('.door-action')).toContainText('Climb down');
 await expect.poll(async()=>(await state()).portals.visibleRooms).toContain('meteor_chamber');
 await page.screenshot({path:'test-results/garage-floor-hatch.png'});
 await page.locator('.door-action').click();await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe('meteor_chamber');
 await expect.poll(async()=>(await state()).climbing,{timeout:15000}).toBe(false);
 expect((await state()).height).toBeCloseTo(-3.36);expect(errors).toEqual([]);
});
