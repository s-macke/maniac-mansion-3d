import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
test('living room, hall and landing are traversable in both directions',()=>{
 const view=createHouseRuntime('living_room');view.doors.toggle('hall:living_door');view.doors.update(1,{x:0,y:1,height:0});let p={...view.START};
 const visit=(x:number,y:number)=>{p=view.moveWalker(p,x-p.x,y-p.y);expect(Math.hypot(p.x-x,p.y-y)).toBeLessThan(.03);};
 visit(8,3.15);visit(4.4,3.15);expect(view.zoneAt(p)).toBe('Entrance hall');
 visit(4.4,.65);visit(-.55,.65);visit(-.55,2.15);
 const route=Array.from({length:201},(_,i)=>{const t=i/200;return{x:-.55+1.3*Math.sin(t*Math.PI*.8),y:2.15+4.13*t};});
 for(const q of route)visit(q.x,q.y);visit(.2,7.6);expect(p.height).toBe(3.36);
 for(const q of route.reverse())visit(q.x,q.y);
 visit(-.55,.65);visit(4.4,.65);visit(4.4,3.15);visit(8,3.15);expect(view.zoneAt(p)).toBe('Living room');
});
test('open door remains a solid leaf while the doorway stays passable',()=>{
 const view=createHouseRuntime('hall');view.doors.toggle('hall:living_door');view.doors.update(1,{x:0,y:1,height:0});
 expect(view.navigation.canStand({x:5.5,y:2.625},0)).toBe(false);
 const stopped=view.moveWalker({x:5.5,y:3.15,height:0},0,-1);
 expect(stopped.y).toBeGreaterThan(2.85);
 expect(view.moveWalker({x:5,y:3.15,height:0},3,0).x).toBeCloseTo(8);
});
test('door jambs and unloaded neighboring rooms remain solid',()=>{
 const view=createHouseRuntime('hall');view.doors.toggle('hall:living_door');view.doors.update(1,{x:0,y:1,height:0});const p={x:5,y:3.15,height:0};
 expect(view.moveWalker({...p,y:3.7},4,0).x).toBeLessThan(6);
 expect(view.moveWalker({...p,height:3.36},4,0).x).toBeLessThan(6);
 view.requireLoadedRooms();view.setRoomLoaded('hall',true);
 expect(view.moveWalker(p,4,0).x).toBeLessThan(6);
 view.setRoomLoaded('living_room',true);expect(view.moveWalker(p,4,0).x).toBeCloseTo(9);
 view.activate('hall');view.setRoomLoaded('living_room',false);expect(view.moveWalker(p,4,0).x).toBeLessThan(6);
});
test('mobile touch controls cross the doorway in both directions',async({browser})=>{
 test.setTimeout(180000);
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const page=await context.newPage();const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto((process.env.WALKTHROUGH_URL||'http://127.0.0.1:5173')+'/?room=living_room');
 await expect(page.getByRole('button',{name:'Forward',exact:true})).toBeVisible({timeout:45000});
 const cdp=await context.newCDPSession(page);
 const touch=(type:'touchStart'|'touchMove'|'touchEnd',x=0,y=0)=>cdp.send('Input.dispatchTouchEvent',{type,touchPoints:type==='touchEnd'?[]:[{x,y,id:1}]});
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');
 async function look(x:number,y:number){
  for(let i=0;i<24;i++){
   const p=await state();let delta=-Math.atan2(x-p.x,y-p.y)-p.yaw;
   while(delta>Math.PI)delta-=2*Math.PI;while(delta< -Math.PI)delta+=2*Math.PI;
   if(Math.abs(delta)<.01)return;
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
 await walk(8,3.15);await look(5,3.15);await page.getByRole('button',{name:'Open living room door',exact:true}).tap();await walk(5,3.15);await expect(page.getByRole('heading',{name:'Entrance hall',exact:true})).toBeVisible();
 await page.screenshot({path:'test-results/mobile-doorway-hall.png'});
 await walk(8,3.15);await expect(page.getByRole('heading',{name:'Living room',exact:true})).toBeVisible();
 expect(errors).toEqual([]);await context.close();
});
