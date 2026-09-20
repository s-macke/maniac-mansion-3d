import {test,expect} from '@playwright/test';
import {createHouseRuntime} from '../lib/house/runtime';
import {toWorld} from '../lib/house/placement';

for(const id of ['cellar','under_house','dungeon','outer_lab','main_lab','meteor_chamber','library','kitchen','dining_room','garage','pantry','plant_room','music_room','security_hall','medical_room','arcade','windowed_hall','photo_room','upper_corridor','radio_bedroom','heart_bedroom','green_bedroom','mummy_room','mummy_bathroom','typewriter_room','safe_attic','tentacle_room','wire_attic','observatory'])test(id+' furnished interior renders and its aisle is walkable',async({page})=>{
 test.setTimeout(90000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room='+id);await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 const room=createHouseRuntime(id).rooms.find(r=>r.id===id)!;
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');
 async function aim(x:number,y:number){
  const q=toWorld({x,y,height:0},room),p=await state(),target=-Math.atan2(q.x-p.x,q.y-p.y);
  const wrap=(n:number)=>Math.atan2(Math.sin(n),Math.cos(n));let delta=wrap(target-p.yaw);
  for(let i=0;i<12&&Math.abs(delta)>.02;i++){
   const part=Math.max(-.65,Math.min(.65,delta));await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650-part/.0022,430,{steps:4});await page.mouse.up();
   await expect.poll(async()=>Math.abs(wrap(target-(await state()).yaw)),{intervals:[50]}).toBeLessThan(Math.abs(delta)-.003);delta=wrap(target-(await state()).yaw);
  }
 }
 async function go(x:number,y:number){
  await aim(x,y);const p=await state(),q=toWorld({x,y,height:0},room),dx=q.x-p.x,dy=q.y-p.y,d=Math.hypot(dx,dy);
  await page.keyboard.down('w');try{await expect.poll(async()=>{const s=await state();return ((s.x-p.x)*dx+(s.y-p.y)*dy)/d;},{timeout:15000,intervals:[50]}).toBeGreaterThan(d-.13);}finally{await page.keyboard.up('w');}
 }
 if(id==='cellar'){await go(0,2.6);await aim(-3.2,5.7);await page.screenshot({path:'test-results/cellar-pipe-bank.png'});await aim(1,5.4);}
 if(id==='under_house'){await go(0,1.5);await aim(5,3);}
 if(id==='dungeon'){await go(0,2.7);await aim(-1.9,4.5);}
 if(id==='outer_lab'){await go(0,2.6);await aim(1,4.8);}
 if(id==='main_lab'){await go(0,1.2);await aim(0,5);}
 if(id==='meteor_chamber'){await go(-2.6,2.6);await aim(0,4.5);}
 if(id==='library'){await go(-4.5,1.2);await aim(0,4.7);}
 if(id==='kitchen'){await go(0,2.9);await aim(0,5);}
 if(id==='dining_room'){await go(-8.7,1);await go(-3.5,1);await aim(0,3.5);}
 if(id==='garage'){await go(4.8,4);await aim(8.45,4.6);await page.screenshot({path:'test-results/garage-car.png'});await go(4.8,2.2);await go(12,2.2);await go(12,2.9);await aim(12,4.22);}
 if(id==='pantry'){await go(0,2.9);await aim(1.4,4.9);}
 if(id==='plant_room'){await go(1.8,2.2);await aim(0,3.6);}
 if(id==='music_room'){await go(1.9,1.4);await aim(2.74,.65);await page.mouse.move(650,430);await page.mouse.down();await page.mouse.move(650,620,{steps:5});await page.mouse.up();await page.screenshot({path:'test-results/music-room-record-desk.png'});await page.mouse.move(650,620);await page.mouse.down();await page.mouse.move(650,430,{steps:5});await page.mouse.up();await aim(2.85,3.12);await page.screenshot({path:'test-results/music-room-crt.png'});await aim(-1,2.8);}
 if(id==='security_hall'){await go(0,3.7);await aim(0,5.35);}
 if(id==='medical_room'){await go(1.4,1.4);await go(1.4,3.4);await aim(-3.3,4.8);await page.screenshot({path:'test-results/medical-room-board-lamp.png'});await aim(4.15,3.95);}
 if(id==='arcade'){await go(4.4,2.5);await go(4.4,3.6);await go(-3,3.6);await go(-3,1.4);await aim(1,4.9);}
 if(id==='windowed_hall'){await go(-1.6,2.3);await aim(2,5.9);}
 if(id==='photo_room'){await go(0,2.3);await aim(-1.7,3.55);}
 if(id==='upper_corridor'){await go(-4.5,2.5);await aim(-8.5,2.4);await page.screenshot({path:'test-results/upper-corridor-left-door.png'});await aim(0,4.7);}
 if(id==='radio_bedroom'){await go(0,2.3);await aim(.3,4.6);}
 if(id==='heart_bedroom'){await go(0,2.1);await aim(-2.6,3.6);await page.screenshot({path:'test-results/heart-bedroom-vanity.png'});await aim(1.5,3.6);}
 if(id==='green_bedroom'){await go(1.5,2.3);await aim(-1.8,4.4);}
 if(id==='mummy_room'){await go(1.5,2.5);await aim(-1,4.5);}
 if(id==='mummy_bathroom'){await go(-.7,2.5);await aim(-3.03,2.22);await page.screenshot({path:'test-results/bathroom-toilet.png'});await aim(1.6,4.4);}
 if(id==='typewriter_room'){await go(0,2.3);await aim(-1.2,4.6);}
 if(id==='safe_attic'){await go(1.5,2.6);await aim(3.95,1.85);}
 if(id==='tentacle_room'){await go(0,2.1);await aim(.5,4.2);}
 if(id==='wire_attic'){await go(0,2.7);await aim(1,4.9);}
 if(id==='observatory'){await go(-.8,3.4);await aim(1.55,6.14);}
 expect((await state()).room).toBe(id);expect(errors).toEqual([]);
 await page.screenshot({path:`test-results/${id}-furnished.png`});
});
