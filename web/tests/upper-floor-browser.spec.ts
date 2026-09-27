import {test,expect} from '@playwright/test';
test('walk up the windowed hall stairs, enter the corridor and bedroom, then return',async({page})=>{
 test.setTimeout(150000);
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=windowed_hall');await expect(page.locator('.status')).toHaveText('EXPLORING', {timeout:45000});
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
 await page.screenshot({path:'test-results/windowed-hall-browser.png'});
 await go(40,.65);await go(34.55,.65);await go(34.55,4.2);await aim(34.55,6.1);
 await expect(page.locator('.door-action')).toContainText('Open higher floor');await page.keyboard.press('e');await expect(page.locator('.door-action')).toContainText('Close higher floor');await expect.poll(async()=>(await state()).movingDoors).not.toContain('windowed_hall:higher_floor');
 await cross(34.55,7,'upper_corridor');expect((await state()).height).toBeCloseTo(10.08);
 await go(57.3,2.4);await go(65.8,2.4);await aim(65.8,4.8);
 await expect(page.locator('.door-action')).toContainText('Open green bedroom door');await page.keyboard.press('e');await expect(page.locator('.door-action')).toContainText('Close green bedroom door');await expect.poll(async()=>(await state()).movingDoors).not.toContain('upper_corridor:green_bedroom_door');
 await cross(65.8,6,'green_bedroom');await expect(page.getByRole('heading',{name:'Green bedroom',exact:true})).toBeVisible();
 await go(89.5,3.8);await page.screenshot({path:'test-results/upper-bedroom-browser.png'});
 await cross(89.5,6,'upper_corridor');await go(65.8,2.4);await go(57.3,2.4);
 await cross(54,2.4,'windowed_hall');await go(34.55,4.7);await go(34.55,.65);expect((await state()).height).toBeCloseTo(6.72);
 expect(errors).toEqual([]);
});
