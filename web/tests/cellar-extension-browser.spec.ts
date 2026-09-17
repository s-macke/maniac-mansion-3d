import {test,expect} from '@playwright/test';
test('walk the complete cellar laboratory route and return through the same doors',async({page})=>{
 test.setTimeout(240000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=cellar');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
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




 async function open(){
  await expect(page.locator('.door-action')).toContainText('Open');await page.keyboard.press('e');
  await expect(page.locator('.door-action')).toContainText('Close');
  await expect.poll(async()=>(await state()).movingDoors).toHaveLength(0);
 }
 await go(333.6,2.6);await aim(331.8,2.6);await open();await cross(330.8,2.6,'dungeon');
 await go(407.9,2.7);await aim(400.1,5.1);await page.screenshot({path:'test-results/dungeon-browser.png'});
 await go(400.1,2.7);await aim(400.1,5.1);await open();await cross(400.1,6.1,'outer_lab');
 await go(440,2.6);await aim(430,2.6);await page.screenshot({path:'test-results/outer-lab-browser.png'});
 await go(431.4,2.6);await aim(429.6,2.6);await open();await cross(428.6,2.6,'main_lab');
 await go(474,2.6);await aim(461,2.6);await page.screenshot({path:'test-results/main-lab-browser.png'});
 await go(461.6,2.6);await aim(459.8,2.6);await open();await cross(458.8,2.6,'meteor_chamber');
 await go(502,2.6);await aim(496.4,5.1);await page.screenshot({path:'test-results/meteor-browser.png'});
 await go(503.6,2.6);await cross(506.6,2.6,'main_lab');
 await go(474.4,2.6);await cross(477.2,2.6,'outer_lab');
 await go(440.6,2.6);await cross(443.4,2.6,'dungeon');
 await go(400.1,2.7);await go(407.9,2.7);await cross(407.9,6.1,'cellar');
 expect((await state()).height).toBeCloseTo(-3.36,1);expect(errors).toEqual([]);
});
