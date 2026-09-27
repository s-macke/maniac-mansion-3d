import {test,expect} from '@playwright/test';
test('reveal the den panel, walk upstairs into the attic, and return',async({page})=>{
 test.setTimeout(120000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=typewriter_room');await expect(page.locator('.status')).toHaveText('EXPLORING', {timeout:45000});
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
 async function cross(x:number,y:number,room:string){
  await aim(x,y);await page.keyboard.down('w');try{await expect.poll(async()=>(await state()).room,{timeout:15000,intervals:[50]}).toBe(room);}finally{await page.keyboard.up('w');await page.screenshot({path:'test-results/upper-route-last.png'});}
 }


 await go(186.6,2.6);await aim(188.5,2.6);
 await expect(page.locator('.door-action')).toContainText('Open painted wall panel');await page.screenshot({path:'test-results/painted-panel-closed.png'});
 await page.keyboard.press('e');await expect(page.locator('.door-action')).toContainText('Close painted wall panel');
 await expect.poll(async()=>(await state()).movingDoors).not.toContain('typewriter_room:hidden_panel');
 await page.screenshot({path:'test-results/painted-panel-open.png'});await cross(189.5,2.6,'attic_stairs');
 await go(292,5.65);expect((await state()).height).toBeCloseTo(13.44,1);
 await cross(292,7,'wire_attic');await go(316,2);await page.screenshot({path:'test-results/wire-attic-browser.png'});
 await cross(316,-1,'attic_stairs');await go(292,.6);expect((await state()).height).toBeCloseTo(10.08,1);
 await cross(292,-1,'typewriter_room');
 await go(186.6,2.6);await aim(188.5,2.6);await page.keyboard.press('e');
 await expect(page.locator('.door-action')).toContainText('Open painted wall panel');
 await expect.poll(async()=>(await state()).movingDoors).not.toContain('typewriter_room:hidden_panel');expect(errors).toEqual([]);
});
