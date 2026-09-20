/** One pool unit with deck and basin floors; only the drained state permits basin walking. */
import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const c=manifest.definitions.pool.geometry;
export function createPoolNavigation(isDrained:()=>boolean=()=>false){
function floorHeight(p:Point,height=0){
 if(p.x<0||p.x>c.width||p.y<0||p.y>c.depth)return NaN;
 const basin=c.pool;
 if(isDrained()&&Math.abs(height-basin.bottom)<.34&&p.x>basin.x0&&p.x<basin.x1&&p.y>basin.y0&&p.y<basin.y1)return basin.bottom;
 if(Math.abs(height)>.34)return NaN;
 const b=c.pool;if(p.x>b.x0&&p.x<b.x1&&p.y>b.y0&&p.y<b.y1)return NaN;
 return 0;
}
function canStand(p:Point,height=0){
 if(!Number.isFinite(floorHeight(p,height)))return false;
 if(Math.abs(height-c.pool.bottom)<.34){
  const b=c.pool,m=RADIUS+.1;
  if(!(p.x>b.x0+m&&p.x<b.x1-m&&p.y>b.y0+m&&p.y<b.y1-m))return false;
  for(const o of b.obstacles){
   const x=Math.max(o.x0,Math.min(o.x1,p.x)),y=Math.max(o.y0,Math.min(o.y1,p.y));
   if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;
  }
  return true;
 }
 if(p.x<RADIUS+.18||p.x>c.width-.36-RADIUS||p.y<.36+RADIUS||p.y>c.depth-.36-RADIUS)return false;
 for(const b of [c.pool,...c.obstacles]){
  const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;
 }
 return true;
}
return {floorHeight,canStand,zone:(p:Point & {height?:number})=>(p.height??0)<-1?'Pool basin':'Pool deck'};
}
export const {floorHeight,canStand,zone}=createPoolNavigation();
