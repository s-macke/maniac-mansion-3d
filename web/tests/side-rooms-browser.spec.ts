import {test,expect} from '@playwright/test';
for(const [from,to,approach,door,out,back,label] of [
 ['mummy_room','mummy_bathroom',[163.3,2.6],[165.2,2.6],[166.2,2.6],[207.3,5.6],'bathroom door'],
 ['windowed_hall','photo_room',[37.3,4.2],[37.3,6.1],[37.3,7.1],[272.8,2],'photo door'],
] as const)test(`open portal from ${from} to ${to} and return`,async({page})=>{
 test.setTimeout(90000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room='+from);await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
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

 await go(approach[0],approach[1]);await aim(door[0],door[1]);
 await expect(page.locator('.door-action')).toContainText('Open '+label);await page.keyboard.press('e');
 await expect(page.locator('.door-action')).toContainText('Close '+label);
 await expect.poll(async()=>(await state()).movingDoors).not.toContain(from+':'+label.replaceAll(' ','_'));
 await cross(out[0],out[1],to);await page.screenshot({path:`test-results/${to}-browser.png`});
 await cross(back[0],back[1],from);expect(errors).toEqual([]);
});
