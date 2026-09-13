import {test,expect} from '@playwright/test';
import {publicAssetUrl} from '../lib/public-asset';
test('room downloads use the same deployment prefix as the static app',()=>{
 expect(publicAssetUrl('/models/hall.glb','/maniac-mansion')).toBe('/maniac-mansion/models/hall.glb');
 expect(publicAssetUrl('models/hall.glb','/games/maniac-mansion')).toBe('/games/maniac-mansion/models/hall.glb');
 expect(publicAssetUrl('/models/hall.glb','')).toBe('/models/hall.glb');
});
