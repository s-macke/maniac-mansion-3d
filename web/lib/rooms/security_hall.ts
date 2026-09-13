import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const c=manifest.definitions.security_hall;const g=c.geometry;
export function floorHeight(p:Point,height=0){
 if(p.x< -g.halfWidth||p.x>g.halfWidth||p.y<0||p.y>g.depth)return NaN;
 const s=g.stairs;if(p.x>=s.x0&&p.x<=s.x1&&p.y>=s.y0)return Math.min(1,(p.y-s.y0)/(s.y1-s.y0))*s.rise;
 return Math.abs(height)<.34?0:NaN;
}
export function canStand(p:Point,height=0){
 const h=floorHeight(p,height);if(!Number.isFinite(h)||Math.abs(h-height)>.34)return false;
 const margin=RADIUS+g.wallThickness;
 if(p.x< -g.halfWidth+margin||p.x>g.halfWidth-margin||p.y<margin+.22||p.y>g.depth-margin)return false;
 const s=g.stairs;if(p.y>=s.y0&&p.x>=s.x0-RADIUS&&p.x<=s.x1+RADIUS){if(p.x<s.x0+RADIUS||p.x>s.x1-RADIUS)return false;}
 return true;
}
export const zone=()=>c.label;
