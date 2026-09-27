import {test,expect} from '@playwright/test';
import {originalArtwork} from '../lib/original-artwork';
import data from '../lib/house/generated.json' with {type:'json'};

test('references follow room, landing and pool state',()=>{
 expect(originalArtwork(data.definitions.connected_hall,'Entrance hall',false).selected).toBe('010');
 expect(originalArtwork(data.definitions.connected_hall,'Upstairs landing',false).selected).toBe('011');
 expect(originalArtwork(data.definitions.pool,'Pool deck',false).selected).toBe('006');
 expect(originalArtwork(data.definitions.pool,'Pool deck',true).selected).toBe('002');
 for(const room of Object.values(data.definitions))expect(room.backgrounds).toContain(originalArtwork(room,room.label,false).selected);
});

test('desktop comparison loads on demand, allows walking, and enlarges into a paused dialog',async({page,request})=>{
 const images:string[]=[];page.on('request',r=>{if(r.url().includes('/originals/'))images.push(r.url());});
 await page.goto('/?room=hall');await expect(page.locator('.status')).toHaveText('EXPLORING',{timeout:45000});
 expect(images).toHaveLength(0);
 await page.getByRole('button',{name:'Original',exact:true}).click();
 const panel=page.getByRole('complementary',{name:'Original artwork'}),img=panel.locator('img');
 await expect(img).toHaveAttribute('src','./originals/010.png');await expect.poll(()=>img.evaluate((i:HTMLImageElement)=>i.naturalWidth)).toBeGreaterThan(0);
 await expect(page.locator('.status')).toHaveText('EXPLORING');
 const before=JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);
 await page.keyboard.down('w');try{await expect.poll(async()=>{const p=JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);return Math.hypot(p.x-before.x,p.y-before.y);}).toBeGreaterThan(.2);}finally{await page.keyboard.up('w');}
 await panel.getByLabel('Original background').selectOption('011');await expect(img).toHaveAttribute('src','./originals/011.png');
 await page.getByRole('button',{name:'Enlarge original artwork'}).click();
 const dialog=page.getByRole('dialog',{name:'Original artwork'});await expect(dialog).toBeVisible();await expect(page.locator('.status')).toHaveText('PAUSED');
 await page.screenshot({path:'test-results/original-desktop.png'});
 await page.keyboard.press('Escape');await expect(dialog).toBeHidden();await expect(page.locator('.status')).toHaveText('EXPLORING');
 // Every declared reference is included in the static site, not just the current room.
 for(const id of new Set(Object.values(data.definitions).flatMap(d=>d.backgrounds))){const r=await request.get(`/originals/${id}.png`);expect(r.ok()).toBe(true);expect(r.headers()['content-type']).toContain('image/png');}
});

test('mobile original pauses movement, traps input and resumes when closed',async({browser})=>{
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
 const page=await context.newPage();await page.goto((process.env.WALKTHROUGH_URL||'http://127.0.0.1:5173')+'/?room=living_room');
 await expect(page.locator('.status')).toHaveText('EXPLORING',{timeout:45000});
 await page.getByRole('button',{name:'Original',exact:true}).tap();const dialog=page.getByRole('dialog',{name:'Original artwork'});
 await expect(dialog).toBeVisible();await expect(dialog.locator('img')).toHaveAttribute('src','./originals/003.png');await expect.poll(()=>dialog.locator('img').evaluate((i:HTMLImageElement)=>i.naturalWidth)).toBeGreaterThan(0);
 await expect(page.locator('.status')).toHaveText('PAUSED');await expect(page.locator('.floating-stick')).toBeHidden();
 const before=JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);
 await page.keyboard.down('w');await page.waitForTimeout(200);await page.keyboard.up('w');
 const after=JSON.parse((await page.locator('.viewport').getAttribute('data-walker'))!);expect(after.x).toBe(before.x);expect(after.y).toBe(before.y);
 await page.screenshot({path:'test-results/original-mobile.png'});
 await dialog.getByRole('button',{name:'Close original'}).tap();await expect(dialog).toBeHidden();await expect(page.locator('.status')).toHaveText('EXPLORING');
 expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);await context.close();
});
