import manifest from '../house/generated.json' with {type:'json'};
import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
const c=manifest.definitions.observatory,g=c.geometry;
export function floorHeight(p:Point,height=0){
 return Math.hypot(p.x,p.y-g.centerY)<=g.radius&&Math.abs(height)<.34?0:NaN;
}
export function canStand(p:Point,height=0){
 if(!Number.isFinite(floorHeight(p,height)))return false;
 // Inscribed polygon margin matches the actual circular wall, including its open slit sill.
 if(Math.hypot(p.x,p.y-g.centerY)>g.radius*Math.cos(Math.PI/g.segments)-RADIUS-g.wallThickness)return false;
 return !g.floorHoles.some(h=>p.x>h.x0-RADIUS&&p.x<h.x1+RADIUS&&p.y>h.y0-RADIUS&&p.y<h.y1+RADIUS);
}
export const zone=()=>c.label;
