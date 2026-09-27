import {test,expect,type Page} from '@playwright/test';

async function instrument(page:Page){
 await page.addInitScript(()=>{
  (window as any).gpuDraws=0;
  HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));
  for(const prototype of [WebGLRenderingContext.prototype,WebGL2RenderingContext.prototype]){
   for(const name of ['drawArrays','drawElements','drawArraysInstanced','drawElementsInstanced']){
    const original=(prototype as any)[name];if(!original)continue;
    (prototype as any)[name]=function(...args:any[]){(window as any).gpuDraws++;return original.apply(this,args);};
   }
  }
 });
}
const draws=(page:Page)=>page.evaluate(()=>(window as any).gpuDraws as number);
const state=async(page:Page)=>JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);
async function idle(page:Page){await page.waitForTimeout(250);const before=await draws(page);expect(before).toBeGreaterThan(0);await page.waitForTimeout(400);expect(await draws(page)).toBe(before);}

test('active idle view stops GPU draws; movement, look, doors and resize redraw',async({page})=>{
 await instrument(page);await page.goto('/?room=hall');await expect(page.locator('.status')).toHaveText('EXPLORING',{timeout:45000});await page.waitForLoadState('networkidle');await idle(page);
 let before=await draws(page);await page.keyboard.down('w');try{await expect.poll(()=>draws(page)).toBeGreaterThan(before);}finally{await page.keyboard.up('w');}await idle(page);
 before=await draws(page);await page.mouse.move(900,450);await page.mouse.down();await page.mouse.move(1000,460,{steps:4});await page.mouse.up();await expect.poll(()=>draws(page)).toBeGreaterThan(before);await idle(page);
 await page.keyboard.press('r');await expect.poll(async()=>(await state(page)).x).toBeCloseTo(-4.65,2);
 const reset=await state(page),yaw=-Math.atan2(-6.4-reset.x,2.35-reset.y),drag=-(yaw-reset.yaw)/.0022;
 await page.mouse.move(1100,450);await page.mouse.down();await page.mouse.move(1100+drag,450,{steps:5});await page.mouse.up();
 await expect(page.locator('.door-action')).toContainText('Open');await idle(page);
 before=await draws(page);await page.keyboard.press('e');await expect.poll(()=>draws(page)).toBeGreaterThan(before);
 await page.waitForTimeout(100);before=await draws(page);await expect.poll(()=>draws(page)).toBeGreaterThan(before);
 await expect.poll(async()=>(await state(page)).movingDoors.length).toBe(0);await page.waitForLoadState('networkidle');await idle(page);
 before=await draws(page);await page.setViewportSize({width:1280,height:800});await expect.poll(()=>draws(page)).toBeGreaterThan(before);await idle(page);
});

test('stationary view redraws when a delayed neighboring room arrives',async({page})=>{
 await instrument(page);let release!:()=>void;const gate=new Promise<void>(resolve=>{release=resolve;});
 await page.route('**/models/living_room/*.glb',async route=>{await gate;await route.continue();});
 try{
  await page.goto('/?room=hall');await expect(page.locator('.status')).toHaveText('EXPLORING',{timeout:45000});
  await expect.poll(async()=>(await state(page)).loadedRooms.includes('hall')).toBe(true);
  await page.waitForTimeout(500);await idle(page);const before=await draws(page);release();
  await expect.poll(async()=>(await state(page)).loadedRooms.includes('living_room')).toBe(true);await expect.poll(()=>draws(page)).toBeGreaterThan(before);await idle(page);
 }finally{release();}
});

test('mobile joystick and swipe redraw; releasing both returns to idle',async({browser})=>{
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const page=await context.newPage();
 await instrument(page);await page.goto((process.env.WALKTHROUGH_URL||'http://127.0.0.1:5173')+'/?room=hall');await expect(page.locator('.status')).toHaveText('EXPLORING',{timeout:45000});await page.waitForLoadState('networkidle');await idle(page);
 const cdp=await context.newCDPSession(page);let before=await draws(page);
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{id:1,x:100,y:650}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{id:1,x:100,y:610}]});await expect.poll(()=>draws(page)).toBeGreaterThan(before);
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await idle(page);
 before=await draws(page);await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{id:2,x:310,y:430}]});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{id:2,x:270,y:440}]});await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 await expect.poll(()=>draws(page)).toBeGreaterThan(before);await idle(page);await context.close();
});
