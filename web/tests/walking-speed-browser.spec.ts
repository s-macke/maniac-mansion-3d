import {test,expect} from '@playwright/test';

test('either Shift key doubles walking speed and release restores normal speed',async({page})=>{
 await page.addInitScript(()=>{HTMLCanvasElement.prototype.requestPointerLock=()=>Promise.reject(new Error('Use drag controls'));});
 await page.goto('/?room=under_house');await expect(page.getByRole('button',{name:'Pause',exact:true})).toBeVisible({timeout:45000});
 // Measure actual displacement per animation time along the long, clear aisle.
 const speed=()=>page.evaluate(()=>new Promise<number>(resolve=>{
  const read=()=>JSON.parse(document.querySelector('.viewport')!.getAttribute('data-walker')!);
  let prior:ReturnType<typeof read>,last=0,distance=0,elapsed=0,count=0;
  function sample(now:number){
   const p=read();
   if(last){distance+=Math.hypot(p.x-prior.x,p.y-prior.y);elapsed+=Math.min((now-last)/1000,.15);count++;}
   prior=p;last=now;
   if(count===4)resolve(distance/elapsed);else requestAnimationFrame(sample);
  }
  requestAnimationFrame(sample);
 }));
 for(const shift of ['ShiftLeft','ShiftRight']){
  await page.keyboard.press('r');await page.keyboard.down('d');
  expect(await speed()).toBeCloseTo(2.5,1);
  await page.keyboard.down(shift);expect(await speed()).toBeCloseTo(5,1);
  await page.keyboard.up(shift);expect(await speed()).toBeCloseTo(2.5,1);
  await page.keyboard.up('d');
 }
});
