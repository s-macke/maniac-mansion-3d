import {test,expect} from '@playwright/test';
import {toWorld} from '../lib/house/placement';
import {createHouseRuntime} from '../lib/house/runtime';
test('living room entry uses world coordinates and furniture blocks movement',()=>{
 const hall=createHouseRuntime(),living=createHouseRuntime('living_room');
 expect(hall.rooms.map(r=>r.id)).toEqual(['hall','living_room','front_exterior','kitchen','dining_room','pantry','pool','garage','library','plant_room','music_room','security_hall','medical_room','arcade']);expect(living.rooms.map(r=>r.id)).toEqual(['hall','living_room','front_exterior','kitchen','dining_room','pantry','pool','garage','library','plant_room','music_room','security_hall','medical_room','arcade']);
 expect(living.zoneAt(living.START)).toBe('Living room');expect(living.navigation.canStand(living.START,0)).toBe(true);
 const placement=living.rooms.find(r=>r.id==='living_room')!;
 const sofa=living.moveWalker(toWorld({x:0,y:2,height:0},placement),0,4);expect(sofa.y).toBeLessThan(3.45);
 const radio=living.moveWalker(toWorld({x:-4.6,y:2,height:0},placement),0,4);expect(radio.y).toBeLessThan(4.35);
 const wall=living.moveWalker(living.START,-100,0);expect(wall.x).toBeGreaterThan(6.7);
 expect(createHouseRuntime('unknown').rooms.map(r=>r.id)).toEqual(['hall','living_room','front_exterior','kitchen','dining_room','pantry','pool','garage','library','plant_room','music_room','security_hall','medical_room','arcade']);
});
test('living room entry loads the connected assets and starts walking',async({page})=>{
 const errors:string[]=[],models:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('request',r=>{if(r.url().includes('.glb'))models.push(r.url());});
 await page.goto('/?room=living_room');await expect(page.getByRole('heading',{name:'Living room',exact:true})).toBeVisible();
 await expect(page.locator('.status')).toHaveText('EXPLORING', {timeout:45000});
 const state=async()=>JSON.parse(await page.locator('.viewport').getAttribute('data-walker')||'{}');const start=await state();
 await page.keyboard.down('w');await expect.poll(async()=>{const p=await state();return Math.hypot(p.x-start.x,p.y-start.y);},{timeout:10000}).toBeGreaterThan(.5);await page.keyboard.up('w');
 expect(new Set(models).size).toBe(models.length);expect(models.some(m=>m.includes('living_room_v4.glb'))).toBe(true);expect(errors).toEqual([]);
 expect((await state()).drawCalls).toBeLessThan(70);await page.screenshot({path:'test-results/living-room.png'});
});
