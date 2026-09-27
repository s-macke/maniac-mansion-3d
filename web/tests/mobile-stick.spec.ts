import {test,expect,type Page,type CDPSession} from '@playwright/test';

test.use({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
const state=async(page:Page)=>JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);
const distance=(a:{x:number;y:number},b:{x:number;y:number})=>Math.hypot(a.x-b.x,a.y-b.y);
const point=(id:number,x:number,y:number)=>({id,x,y,radiusX:5,radiusY:5,force:1});
async function touches(cdp:CDPSession,type:'touchStart'|'touchMove'|'touchEnd'|'touchCancel',touchPoints:ReturnType<typeof point>[]){await cdp.send('Input.dispatchTouchEvent',{type,touchPoints});}
async function open(page:Page){await page.goto('/?room=hall');await expect(page.locator('.status')).toHaveText('EXPLORING',{timeout:45000});return page.context().newCDPSession(page);}
async function stationary(page:Page){const before=await state(page);await page.waitForTimeout(220);expect(distance(await state(page),before)).toBeLessThan(.015);}
async function center(page:Page,x:number,y:number){const box=await page.locator('.floating-stick').boundingBox();expect(box).not.toBeNull();expect(box!.x+box!.width/2).toBeCloseTo(x,1);expect(box!.y+box!.height/2).toBeCloseTo(y,1);}

test('left stick floats at the thumb, has a dead zone, moves and stops on release',async({page})=>{
 const cdp=await open(page);const stick=page.locator('.floating-stick');await expect(stick).toBeHidden();await stationary(page);
 const before=await state(page);
 await touches(cdp,'touchStart',[point(1,110,670)]);await expect(stick).toBeVisible();await center(page,110,670);
 await touches(cdp,'touchMove',[point(1,113,668)]);await stationary(page);
 await touches(cdp,'touchMove',[point(1,110,622)]);
 await expect.poll(async()=>distance(await state(page),before)).toBeGreaterThan(.35);
 expect((await state(page)).yaw).toBeCloseTo(before.yaw,4);
 await page.screenshot({path:'test-results/mobile-floating-stick.png'});
 await touches(cdp,'touchEnd',[]);await expect(stick).toBeHidden();await stationary(page);
 await touches(cdp,'touchStart',[point(2,35,410)]);await center(page,35,410);await stationary(page);
 await touches(cdp,'touchEnd',[]);await cdp.detach();
});

test('two thumbs independently move and look, retaining their roles across the screen midpoint',async({page})=>{
 const cdp=await open(page);const before=await state(page);
 await touches(cdp,'touchStart',[point(1,90,670)]);
 await touches(cdp,'touchStart',[point(1,90,670),point(2,320,430)]);
 await touches(cdp,'touchMove',[point(1,90,630),point(2,280,445)]);
 await expect.poll(async()=>distance(await state(page),before)).toBeGreaterThan(.25);
 await expect.poll(async()=>Math.abs((await state(page)).yaw-before.yaw)).toBeGreaterThan(.05);
 const moving=await state(page);
 await touches(cdp,'touchMove',[point(1,90,630),point(2,175,445)]);
 await center(page,90,670);await expect.poll(async()=>Math.abs((await state(page)).yaw-moving.yaw)).toBeGreaterThan(.1);
 await touches(cdp,'touchEnd',[point(1,90,630)]);await expect(page.locator('.floating-stick')).toBeHidden();await stationary(page);
 const stopped=await state(page);await touches(cdp,'touchMove',[point(2,150,450)]);
 await expect.poll(async()=>Math.abs((await state(page)).yaw-stopped.yaw)).toBeGreaterThan(.02);await stationary(page);
 await touches(cdp,'touchEnd',[]);await cdp.detach();
});

test('cancel, pause and resize clear movement; the next touch can start a new stick',async({page})=>{
 const cdp=await open(page);
 for(const end of ['cancel','pause','resize'] as const){
  const before=await state(page);
  await touches(cdp,'touchStart',[point(1,100,580)]);await touches(cdp,'touchMove',[point(1,100,540)]);
  await expect.poll(async()=>distance(await state(page),before)).toBeGreaterThan(.15);
  if(end==='cancel')await touches(cdp,'touchCancel',[]);
  if(end==='pause'){await page.evaluate(()=>window.dispatchEvent(new Event('blur')));await expect(page.locator('.status')).toHaveText('PAUSED');}
  if(end==='resize')await page.setViewportSize({width:844,height:390});
  await expect(page.locator('.floating-stick')).toBeHidden();await stationary(page);
  if(end!=='cancel')await touches(cdp,'touchEnd',[]);
 }
 await cdp.detach();
});
