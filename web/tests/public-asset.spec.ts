import {test,expect} from '@playwright/test';
import {publicAssetUrl} from '../lib/public-asset';
test('room downloads resolve beside the document at any deployment depth',()=>{
 for(const folder of ['/', '/maniac-mansion-3d/', '/games/mansion/']){
  for(const document of [folder, `${folder}index.html?room=kitchen`]){
   for(const path of ['/models/hall.glb','models/hall.glb']){
    expect(new URL(publicAssetUrl(path),`https://example.test${document}`).pathname).toBe(`${folder}models/hall.glb`);
   }
  }
 }
});
