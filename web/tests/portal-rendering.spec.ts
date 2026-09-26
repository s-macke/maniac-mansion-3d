import {test,expect} from '@playwright/test';
import {spawn,type ChildProcess} from 'node:child_process';
import {once} from 'node:events';
let server:ChildProcess,origin:string;
test.beforeAll(async()=>{
 server=spawn(process.execPath,['node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','0'],{stdio:['ignore','pipe','pipe']});
 origin=await new Promise<string>((resolve,reject)=>{
  let output='';const timer=setTimeout(()=>reject(new Error('Vite did not start')),15000);
  server.on('error',reject);server.stdout!.on('data',chunk=>{output+=chunk.toString();const match=output.match(/http:\/\/127\.0\.0\.1:\d+/);if(match){clearTimeout(timer);resolve(match[0]);}});
 });
});
test.afterAll(async()=>{if(server&&server.exitCode===null){const end=once(server,'exit');server.kill();await end;}});
test('portal image is unchanged when the destination moves and rotates; three-level targets are released',async({page})=>{
 test.setTimeout(120000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await page.goto(origin+'/tests/fixtures/portal-scene.html');
 await page.waitForFunction(()=>Boolean((window as any).portalFixture));
 const first=await page.evaluate(async()=>{const f=(window as any).portalFixture;await f.build(false);(window as any).baseline=f.pixels();return f.stats;});
 expect(first.targets).toBeGreaterThanOrEqual(3);expect(first.visibleRooms).toContain('pantry');expect(first.visibleRooms).not.toContain('pool');
 await page.screenshot({path:'test-results/portal-aligned.png'});
 const comparison=await page.evaluate(async()=>{
  const f=(window as any).portalFixture;await f.build(true);const next=f.pixels(),before=(window as any).baseline;let changed=0,lit=0;
  for(let i=0;i<next.length;i+=4){if(next[i]+next[i+1]+next[i+2]>10)lit++;if(Math.max(Math.abs(next[i]-before[i]),Math.abs(next[i+1]-before[i+1]),Math.abs(next[i+2]-before[i+2]))>8)changed++;}
  return {fraction:changed/(640*360),lit:lit/(640*360),stats:f.stats};
 });
 await page.screenshot({path:'test-results/portal-independent.png'});
 expect(comparison.lit).toBeGreaterThan(.3);expect(comparison.fraction).toBeLessThan(.01);
 expect(await page.evaluate(()=>(window as any).portalFixture.near())).toBeGreaterThan(.8);
 const closed=await page.evaluate(()=>(window as any).portalFixture.close());expect(closed.targets).toBe(0);expect(closed.passes).toBe(1);
 await page.evaluate(()=>(window as any).portalFixture.dispose());expect(errors).toEqual([]);
});

test('fine diagonal lines receive multisample coverage inside portal targets',async({page})=>{
 const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));page.on('console',m=>{if(m.type()==='error')errors.push(m.text());});
 await page.goto(origin+'/tests/fixtures/portal-scene.html');await page.waitForFunction(()=>Boolean((window as any).portalFixture));
 const result=await page.evaluate(()=>(window as any).portalFixture.antialiasProbe());
 expect(result.maxSamples).toBeGreaterThanOrEqual(4);
 expect(result.with.targets).toBeGreaterThan(0);
 expect(result.with.covered).toBeGreaterThan(100);
 expect(result.with.partial).toBeGreaterThan(result.without.partial+100);
 expect(errors).toEqual([]);
 await page.evaluate(()=>(window as any).portalFixture.dispose());
});
