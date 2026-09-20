import {test,expect} from '@playwright/test';
for(const [id,x,upper] of [['heart_bedroom',112,'safe_attic'],['radio_bedroom',136,'tentacle_room']] as const)test(`${id} visible hatch portal climbs up and down`,async({page})=>{
 test.setTimeout(120000);
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room='+id);await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
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

 const sign=id==='heart_bedroom'?1:-1;
 await go(x+sign*3.15,2);await go(x+sign*3.15,3.65);await aim(x+sign*4.12,3.65);
 await page.mouse.move(650,600);await page.mouse.down();await page.mouse.move(650,220,{steps:8});await page.mouse.up();
 await expect(page.locator('.door-action')).toContainText('Climb up');
 await expect.poll(async()=>(await state()).portals.visibleRooms).toContain(upper);
 await expect.poll(async()=>(await state()).portals.passes).toBeGreaterThan(1);
 await page.screenshot({path:`test-results/${id}-hatch-up.png`});
 await page.keyboard.press('e');await expect.poll(async()=>(await state()).climbing).toBe(true);
 await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe(upper);
 await page.screenshot({path:`test-results/${id}-crossing.png`});
 await expect.poll(async()=>(await state()).climbing,{timeout:15000}).toBe(false);
 expect((await state()).height).toBeCloseTo(13.44);
 const upperX=id==='heart_bedroom'?220:244;
 await aim(upperX+sign*3.1,3.2);
 await page.mouse.move(650,160);await page.mouse.down();await page.mouse.move(650,870,{steps:8});await page.mouse.up();
 await expect(page.locator('.door-action')).toContainText('Climb down');
 await expect.poll(async()=>(await state()).portals.visibleRooms).toContain(id);
 await page.screenshot({path:`test-results/${id}-hatch-down.png`});
 await page.locator('.door-action').click();
 await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe(id);
 await expect.poll(async()=>(await state()).climbing,{timeout:15000}).toBe(false);
 expect((await state()).height).toBeCloseTo(10.08);expect(errors).toEqual([]);
});

test('mobile touch controls climb a hatch in both directions',async({browser})=>{
 test.setTimeout(180000);
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const page=await context.newPage();const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto((process.env.WALKTHROUGH_URL||'http://127.0.0.1:5173')+'/?room=heart_bedroom');
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
 await walk(115.15,2);await walk(115.15,3.65);await look(116.12,3.65);
 await expect(page.locator('.door-action')).toContainText('Climb up');await page.locator('.door-action').tap();
 await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe('safe_attic');
 await expect.poll(async()=>(await state()).climbing,{timeout:15000}).toBe(false);
 await expect(page.locator('.door-action')).toContainText('Climb down');
 await page.screenshot({path:'test-results/ladder-mobile.png'});
 await page.locator('.door-action').tap();
 await expect.poll(async()=>(await state()).room,{timeout:15000}).toBe('heart_bedroom');
 await expect.poll(async()=>(await state()).climbing,{timeout:15000}).toBe(false);
 expect((await state()).height).toBeCloseTo(10.08);expect(errors).toEqual([]);await context.close();
});
