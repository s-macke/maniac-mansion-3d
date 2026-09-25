import {test,expect} from '@playwright/test';
test('pool rear facade remains visible and its pantry portal stays usable',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Drag'));});
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



 await aim(-6.37,40.9);
 await expect(page.locator('.door-action')).toContainText('Open');await page.keyboard.press('e');
 await expect(page.locator('.door-action')).toContainText('Close');
 await expect.poll(async()=>(await state()).movingDoors).toHaveLength(0);
 await page.screenshot({path:'test-results/pool-pantry-open-facade.png'});
 await page.keyboard.down('w');try{await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe('pantry');}finally{await page.keyboard.up('w');}
 await page.keyboard.down('s');try{await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe('pool');}finally{await page.keyboard.up('s');}
 await go(-10.17,40.9);await go(-10.17,34.7);await go(-24.87,34.7);await aim(-6.37,38.6);
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,280,{steps:5});await page.mouse.up();
 await page.screenshot({path:'test-results/pool-rear-house.png'});
 await page.mouse.move(650,280);await page.mouse.down();await page.mouse.move(650,430,{steps:5});await page.mouse.up();
 await aim(-16.37,44.1);await page.screenshot({path:'test-results/pool-side-fence.png'});expect(errors).toEqual([]);
});
