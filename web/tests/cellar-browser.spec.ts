import {test,expect} from '@playwright/test';
test('walk down from the entrance hall into the cellar and return',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
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
 async function cross(x:number,y:number,room:string){
  await aim(x,y);await page.keyboard.down('w');try{await expect.poll(async()=>(await state()).room,{timeout:15000,intervals:[50]}).toBe(room);}finally{await page.keyboard.up('w');await page.screenshot({path:'test-results/upper-route-last.png'});}
 }



 await go(-4.65,.55);await go(3.12,.55);await go(3.12,4.6);await aim(3.12,6.5);
 await expect(page.locator('.door-action')).toContainText('Open cellar door');await page.keyboard.press('e');
 await expect(page.locator('.door-action')).toContainText('Close cellar door');await expect.poll(async()=>(await state()).movingDoors).not.toContain('hall:cellar_door');
 await page.screenshot({path:'test-results/cellar-entrance.png'});await cross(3.12,7.5,'cellar');
 await go(346.7,.6);expect((await state()).height).toBeCloseTo(-3.36,1);await go(343,.6);await aim(340,3);await page.screenshot({path:'test-results/cellar-browser.png'});
 await go(346.7,.6);await go(346.7,5.65);await cross(346.7,7,'hall');expect((await state()).height).toBeCloseTo(0);expect(errors).toEqual([]);
});
test('open the bush grating and crawl through its portal in both directions',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/');await expect(page.locator('.status')).toHaveText('EXPLORING', {timeout:45000});
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



 await go(-11.9,2.35);await go(-11.9,6.6);await go(-9.25,6.6);await aim(-8.6,5.2);
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,790,{steps:8});await page.mouse.up();
 await expect.poll(async()=>(await state()).portals.passes).toBeGreaterThan(1);
 await expect(page.locator('.door-action')).toContainText('Open metal grating');await page.keyboard.press('e');
 await expect(page.locator('.door-action')).toContainText('Crawl under house');await page.screenshot({path:'test-results/grating-open.png'});
 await page.keyboard.press('e');await expect.poll(async()=>(await state()).crawling).toBe(true);
 await expect.poll(async()=>(await state()).eyeHeight).toBeLessThan(.6);
 await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,205,{steps:6});await page.mouse.up();
 await page.screenshot({path:'test-results/grating-crawl.png'});
 await expect.poll(async()=>(await state()).room,{timeout:20000}).toBe('under_house');
 await expect.poll(async()=>(await state()).crawling,{timeout:20000}).toBe(false);
 expect((await state()).eyeHeight).toBeCloseTo(1.62);await aim(370,1.75);await page.screenshot({path:'test-results/under-house-browser.png'});
 await aim(360,1.75);await expect(page.locator('.door-action')).toContainText('Crawl outside');await page.locator('.door-action').click();
 await expect.poll(async()=>(await state()).room,{timeout:20000}).toBe('front_exterior');
 await expect.poll(async()=>(await state()).crawling,{timeout:20000}).toBe(false);
 expect((await state()).height).toBeCloseTo(-1.2);expect((await state()).eyeHeight).toBeCloseTo(1.62);expect(errors).toEqual([]);
});

test('mobile touch opens the grating and crawls outside',async({browser})=>{
 test.setTimeout(180000);
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const page=await context.newPage();const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto((process.env.WALKTHROUGH_URL||'http://127.0.0.1:5173')+'/?room=under_house');
 await expect(page.getByRole('button',{name:'Forward',exact:true})).toBeVisible({timeout:45000});
 const cdp=await context.newCDPSession(page);
 const touch=(type:'touchStart'|'touchMove'|'touchEnd',x=0,y=0)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:type==='touchEnd'?[]:[{x,y,id:1}]});
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');
 async function look(x:number,y:number){
  for(let i=0;i<24;i++){
   const p=await state();let delta=-Math.atan2(x-p.x,y-p.y)-p.yaw;
   while(delta>Math.PI)delta-=2*Math.PI;while(delta< -Math.PI)delta+=2*Math.PI;
   if(Math.abs(delta)<.02)return;
   const dx=Math.max(-110,Math.min(110,-delta/.0022));
   await touch('touchStart',195,280);await touch('touchMove',195+dx,280);await touch('touchEnd');
   await expect.poll(async()=>Math.abs((await state()).yaw-p.yaw)).toBeGreaterThan(.001);
  }
  throw new Error('Touch steering failed');
 }
 async function walk(x:number,y:number){
  await look(x,y);const p=await state(),dx=x-p.x,dy=y-p.y,length=Math.hypot(dx,dy);
  const button=(await page.getByRole('button',{name:'Forward',exact:true}).boundingBox())!;
  await touch('touchStart',button.x+button.width/2,button.y+button.height/2);
  try{await expect.poll(async()=>{const q=await state();return((q.x-p.x)*dx+(q.y-p.y)*dy)/length;},{timeout:20000,intervals:[70]}).toBeGreaterThan(length-.14);}finally{await touch('touchEnd');}
 }
 await walk(361.9,1.75);await look(360,1.75);
 await expect(page.locator('.door-action')).toContainText('Open metal grating');await page.locator('.door-action').tap();
 await expect(page.locator('.door-action')).toContainText('Crawl outside');await page.locator('.door-action').tap();
 await expect.poll(async()=>(await state()).crawling).toBe(true);
 await expect.poll(async()=>(await state()).room,{timeout:20000}).toBe('front_exterior');
 await expect.poll(async()=>(await state()).crawling,{timeout:20000}).toBe(false);
 expect((await state()).height).toBeCloseTo(-1.2);expect((await state()).eyeHeight).toBeCloseTo(1.62);
 await page.screenshot({path:'test-results/cellar-crawl-mobile.png'});expect(errors).toEqual([]);await context.close();
});
