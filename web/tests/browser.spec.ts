import { test, expect } from '@playwright/test';
const state=async(page:any)=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker'));
test('room loads, mouse look and walking work, pause and reset recover',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('/?room=hall');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 await expect(page.locator('canvas')).toBeVisible();
 await page.screenshot({path:'test-results/entrance-ready.png'});
 await expect(page.getByRole('button',{name:'Explore room'})).toHaveCount(0);
 await expect(page.getByRole('region',{name:'Walkthrough controls'})).toBeVisible();
 const before=await state(page);await page.keyboard.down('w');await expect.poll(async()=>{const p=await state(page);return Math.hypot(p.x-before.x,p.y-before.y);},{timeout:10000}).toBeGreaterThan(3.15);await page.keyboard.up('w');
 await expect(page.getByRole('region',{name:'Walkthrough controls'})).toHaveCount(0);
 const after=await state(page);expect(Math.hypot(after.x-before.x,after.y-before.y)).toBeGreaterThan(.3);
 await page.mouse.click(700,450);await page.mouse.move(700,450);await page.mouse.move(880,430);await page.waitForTimeout(120);
 await expect.poll(async()=>Math.abs((await state(page)).yaw-before.yaw)).toBeGreaterThan(.1);
 await page.keyboard.press('r');await expect(page.getByRole('region',{name:'Walkthrough controls'})).toHaveCount(0);await expect.poll(async()=>(await state(page)).x).toBeCloseTo(-4.65,2);const reset=await state(page);expect(reset.x).toBeCloseTo(-4.65,2);expect(reset.y).toBeCloseTo(1.1,2);
 await page.screenshot({path:'test-results/entrance-walking.png'});
 await page.keyboard.press('Escape');await expect(page.getByRole('button',{name:'Resume',exact:true})).toBeVisible();
 const paused=await state(page);await page.keyboard.down('w');await page.waitForTimeout(150);await page.keyboard.up('w');expect((await state(page)).x).toBeCloseTo(paused.x,3);
 await page.mouse.click(700,450);await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible();
 expect(errors).toEqual([]);expect(after.triangles).toBeGreaterThan(1000);expect(after.drawCalls).toBeLessThan(20);
});
test('pointer-lock denial falls back to dragging; reset button shares state',async({page})=>{
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Test denial'));});
 await page.goto('/?room=hall');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 await expect(page.getByText('Click or drag to look · Arrow keys also work · R to reset')).toBeVisible();
 const before=await state(page);await page.mouse.move(800,400);await page.mouse.down();await page.mouse.move(950,450,{steps:5});await page.mouse.up();
 await expect.poll(async()=>Math.abs((await state(page)).yaw-before.yaw)).toBeGreaterThan(.1);
 await page.keyboard.down('w');await page.waitForTimeout(180);await page.keyboard.up('w');
 await page.getByRole('button',{name:'Reset position'}).click();expect((await state(page)).x).toBeCloseTo(-4.65,2);
});
test('load failure gives a visible actionable error',async({page})=>{
 await page.route('**/models/connected_hall/*.glb',route=>route.abort());await page.goto('/?room=hall');
 await expect(page.getByRole('alert')).toContainText('Reload the page',{timeout:30000});
 await expect(page.getByRole('button',{name:'Reset position'})).toBeDisabled();
});
test('mobile layout loads and touch movement is available',async({browser})=>{
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const page=await context.newPage();
 await page.goto(process.env.WALKTHROUGH_URL || 'http://127.0.0.1:5173');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 await expect(page.getByRole('button',{name:'Forward',exact:true})).toBeVisible();
 await page.screenshot({path:'test-results/entrance-mobile.png'});expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);await context.close();
});
test('walk upstairs into the landing and look back into the same hall',async({page})=>{
 test.setTimeout(180000);await page.setViewportSize({width:960,height:600});
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag for deterministic route steering'));});
 await page.goto('/?room=hall');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 await page.keyboard.press('r');
 await expect.poll(async()=>(await state(page)).x).toBeCloseTo(-4.65,2);
 async function lookToward(x:number,y:number){
  for(let i=0;i<12;i++){
   const p=await state(page);const desired=-Math.atan2(x-p.x,y-p.y);let difference=desired-p.yaw;
   while(difference>Math.PI)difference-=Math.PI*2;while(difference< -Math.PI)difference+=Math.PI*2;
   if(Math.abs(difference)<.008)return;
   const dx=Math.max(-250,Math.min(250,-difference/.0022));
   await page.mouse.move(480,300);await page.mouse.down();await page.mouse.move(480+dx,300);await page.mouse.up();
   await expect.poll(async()=>Math.abs((await state(page)).yaw-p.yaw)).toBeGreaterThan(.001);
  }
  throw new Error('Could not steer toward route waypoint');
 }
 async function walkTo(x:number,y:number){
  await lookToward(x,y);const p=await state(page);const dx=x-p.x,dy=y-p.y,length=Math.hypot(dx,dy);
  if(length<.18)return;
  await page.keyboard.down('w');
  try{await expect.poll(async()=>{const q=await state(page);return ((q.x-p.x)*dx+(q.y-p.y)*dy)/length;},{timeout:15000,intervals:[70]}).toBeGreaterThan(length-.17);}finally{await page.keyboard.up('w');}
 }
 await walkTo(4.4,.65);await walkTo(4.4,3.15);await lookToward(9,3.15);
 await page.screenshot({path:'test-results/hall-to-living-doorway.png'});
 await walkTo(8,3.15);await expect(page.getByRole('heading',{name:'Living room',exact:true})).toBeVisible();
 await lookToward(3,3.15);await page.screenshot({path:'test-results/living-to-hall-doorway.png'});
 await walkTo(4.4,3.15);await walkTo(4.4,.65);
 await walkTo(-.55,.65);await walkTo(-.55,1.55);await walkTo(-.55,2.15);
 for(let i=1;i<=8;i++){const t=i/8;await walkTo(-.55+1.3*Math.sin(t*Math.PI*.8),2.15+4.13*t);}
 await walkTo(.22,7.6);await expect(page.getByRole('heading',{name:'Upstairs landing',exact:true})).toBeVisible();
 expect((await state(page)).height).toBeCloseTo(3.36,2);
 await page.screenshot({path:'test-results/upstairs-landing.png'});
 await walkTo(-3.8,7.8);await lookToward(0,2.5);
 await page.screenshot({path:'test-results/balcony-looking-down.png'});
});
