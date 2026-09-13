import {test,expect} from '@playwright/test';
import {readFile} from 'node:fs/promises';
test('room downloads negotiate gzip and retain the exact optimized GLB',async({request})=>{
 for(const [room,file] of [['connected_hall','connected_hall_v6'],['living_room','living_room_v4'],['front_exterior','front_exterior_v3'],['kitchen','kitchen_v4'],['dining_room','dining_room_v1'],['pantry','pantry_v1'],['pool','pool_v1'],['garage','garage_v1'],['library','library_v1'],['plant_room','plant_room_v1'],['music_room','music_room_v1'],['security_hall','security_hall_v1'],['medical_room','medical_room_v1'],['arcade','arcade_v1'],['shared','standard_doors_v1']]){
  const path=`/models/${room}/${file}.glb`,plain=await request.get(path,{headers:{'Accept-Encoding':'identity'}});
  expect(plain.status()).toBe(200);expect(plain.headers()['content-encoding']).toBeUndefined();
  const packed=await request.get(path,{headers:{'Accept-Encoding':'gzip'}});
  expect(packed.status()).toBe(200);expect(packed.headers()['content-encoding']).toBe('gzip');
  expect(packed.headers()['vary']).toBe('Accept-Encoding');
  expect(Number(packed.headers()['content-length'])).toBeLessThan(room==='kitchen'?150000:room==='living_room'?550000:1800000);
  // Playwright decodes HTTP compression; these bytes must match the raw GLB.
  expect(Buffer.compare(await packed.body(),await plain.body())).toBe(0);
  expect(Buffer.compare(await plain.body(),await readFile(`../generated/models/${room==='shared'?'doors':'rooms'}/${file}_compact.glb`))).toBe(0);
  const disabled=await request.head(path,{headers:{'Accept-Encoding':'gzip;q=0'}});expect(disabled.headers()['content-encoding']).toBeUndefined();
 }
});
