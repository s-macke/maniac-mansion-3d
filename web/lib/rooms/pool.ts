/** Outdoor deck; water and perimeter fences remain solid exploration boundaries. */
import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const c=manifest.definitions.pool.geometry;
export function floorHeight(p:Point,height=0){
 if(Math.abs(height)>.34||p.x<0||p.x>c.width||p.y<0||p.y>c.depth)return NaN;
 const b=c.pool;if(p.x>b.x0&&p.x<b.x1&&p.y>b.y0&&p.y<b.y1)return NaN;
 return 0;
}
export function canStand(p:Point,height=0){
 if(!Number.isFinite(floorHeight(p,height)))return false;
 if(p.x<RADIUS+.18||p.x>c.width-.36-RADIUS||p.y<.36+RADIUS||p.y>c.depth-.36-RADIUS)return false;
 for(const b of [c.pool,...c.obstacles]){
  const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;
 }
 return true;
}
export const zone=()=> 'Pool deck';
