import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';
test('approach, steps and open double entrance connect to the hall in both directions',()=>{
 const v=createHouseRuntime(),ex=v.rooms.find(r=>r.id==='front_exterior')!;
 expect(v.zoneAt(v.START)).toBe('Front exterior');v.doors.toggle('hall:front_doors');v.doors.update(1,{x:0,y:1,height:0});let p={...v.START};
 const visit=(x:number,y:number)=>{const q=toWorld({x,y,height:0},ex);p=v.moveWalker(p,q.x-p.x,q.y-p.y);expect(Math.hypot(p.x-q.x,p.y-q.y)).toBeLessThan(.03);};
 visit(0,-5);expect(p.height).toBe(-1.2);visit(0,-1);expect(p.height).toBeCloseTo(0);
 visit(0,1.6);expect(v.zoneAt(p)).toBe('Entrance hall');
 visit(0,-1);visit(0,-5);visit(0,-12);expect(p.height).toBe(-1.2);
 const onPorch=toWorld({x:3,y:-1,height:0},ex),outside=v.moveWalker(onPorch,-3,0);
 expect(outside.x).toBeGreaterThan(-8.3); // front balustrade is solid
 const stone=toWorld({x:7,y:-5.6,height:-1.2},ex);expect(v.navigation.canStand(stone,stone.height)).toBe(false);
 v.requireLoadedRooms();v.setRoomLoaded('front_exterior',true);
 p=toWorld({x:0,y:-1,height:0},ex);expect(v.moveWalker(p,3,0).x).toBeLessThan(-6.4);
});
test('bushes are solid and the left grating can be inspected from the side',()=>{
 const v=createHouseRuntime(),ex=v.rooms.find(r=>r.id==='front_exterior')!;
 const at=(x:number,y:number)=>toWorld({x,y,height:-1.2},ex);
 for(const x of [-2.8,2.8])expect(v.navigation.canStand(at(x,-3.02),-1.2)).toBe(false);
 expect(v.navigation.canStand(at(-4.4,-2.9),-1.2)).toBe(true);
 expect(v.navigation.canStand(at(0,-5),-1.2)).toBe(true);
 const p=at(-2.8,-5),q=at(-2.8,-2.9),stopped=v.moveWalker(p,q.x-p.x,q.y-p.y);
 expect(stopped.x).toBeLessThan(-10.1);
 expect(v.definitions.front_exterior.ports.find(p=>p.id==='under_porch_grating')?.state).toBe('open');
 expect(v.doors.items.find(d=>d.def.port==='under_porch_grating')?.amount).toBe(0);
});
test('exterior browser entry walks up the steps through visible front doors and back',async({page})=>{
 test.setTimeout(150000);
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.setViewportSize({width:1000,height:700});await page.goto('/');
 await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');
 await expect(page.getByRole('heading',{name:'Front exterior',exact:true})).toBeVisible();
 await page.screenshot({path:'test-results/exterior-approach.png'});
 await page.keyboard.down('w');
 await expect(page.getByRole('button',{name:'Open front doors',exact:true})).toBeVisible({timeout:45000});await page.keyboard.press('e');
 try{await expect.poll(async()=>(await state()).x,{timeout:45000}).toBeGreaterThan(-4.9);}finally{await page.keyboard.up('w');}
 await expect(page.getByRole('heading',{name:'Entrance hall',exact:true})).toBeVisible();expect((await state()).height).toBeCloseTo(0);
 await page.screenshot({path:'test-results/exterior-entered-hall.png'});
 await page.keyboard.down('s');
 try{await expect.poll(async()=>(await state()).x,{timeout:45000}).toBeLessThan(-12);}finally{await page.keyboard.up('s');}
 expect((await state()).height).toBeCloseTo(-1.2);await expect(page.getByRole('heading',{name:'Front exterior',exact:true})).toBeVisible();
 await page.keyboard.press('r');await expect.poll(async()=>(await state()).x).toBeCloseTo(-21.4,2);
 expect(errors).toEqual([]);
});
test('mobile touch can climb the exterior steps and enter the hall',async({browser})=>{
 test.setTimeout(120000);
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});const page=await context.newPage();
 await page.goto(process.env.WALKTHROUGH_URL||'http://127.0.0.1:5173');
 await expect(page.getByRole('button',{name:'Forward',exact:true})).toBeVisible({timeout:45000});
 const cdp=await context.newCDPSession(page),button=(await page.getByRole('button',{name:'Forward',exact:true}).boundingBox())!;
 await page.screenshot({path:'test-results/exterior-mobile.png'});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:button.x+button.width/2,y:button.y+button.height/2,id:1}]});
 await expect(page.getByRole('button',{name:'Open front doors',exact:true})).toBeVisible({timeout:45000});
 await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
 await page.getByRole('button',{name:'Open front doors',exact:true}).tap();
 await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:button.x+button.width/2,y:button.y+button.height/2,id:1}]});
 try{await expect.poll(async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}').x,{timeout:45000}).toBeGreaterThan(-4.9);}finally{await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});}
 await expect(page.getByRole('heading',{name:'Entrance hall',exact:true})).toBeVisible();
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);await context.close();
});
