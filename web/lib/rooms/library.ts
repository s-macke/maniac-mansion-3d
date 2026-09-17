import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const c=manifest.definitions.library;const g=c.geometry;
export function floorHeight(p:Point,height=0){
 if(p.x< -g.halfWidth||p.x>g.halfWidth||p.y<0||p.y>g.depth)return NaN;
 
 return Math.abs(height)<.34?0:NaN;
}
export function canStand(p:Point,height=0){
 for(const b of g.obstacles){const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;}
 const h=floorHeight(p,height);if(!Number.isFinite(h)||Math.abs(h-height)>.34)return false;
 const margin=RADIUS+g.wallThickness;
 if(p.x< -g.halfWidth+margin||p.x>g.halfWidth-margin||p.y<margin||p.y>g.depth-margin)return false;
 
 return true;
}
export const zone=()=>c.label;
