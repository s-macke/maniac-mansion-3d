/** Outdoor approach and covered garage bay, sharing one continuous slab elevation. */
import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const g=manifest.definitions.garage.geometry;
export function floorHeight(p:Point,height=0){
 if(Math.abs(height)>.34||p.x<0||p.x>g.width||p.y<0||p.y>g.depth)return NaN;
 if(p.x>=g.bayFront&&(p.y<g.bayY0||p.y>g.bayY1))return NaN;
 return 0;
}
export function canStand(p:Point,height=0){
 if(!Number.isFinite(floorHeight(p,height)))return false;
 if(p.x<RADIUS+.26||p.x>g.width-g.wallThickness-RADIUS||p.y<RADIUS+.26||p.y>g.depth-.26-RADIUS)return false;
 if(p.x>g.bayFront-RADIUS){
  if(p.y<g.bayY0+g.wallThickness+RADIUS||p.y>g.bayY1-g.wallThickness-RADIUS)return false;
  if(p.x<g.bayFront+g.wallThickness+RADIUS&&(p.y<g.openingY0+.06+RADIUS||p.y>g.openingY1-.06-RADIUS))return false;
 }
 for(const h of g.floorHoles)if(p.x>h.x0-RADIUS&&p.x<h.x1+RADIUS&&p.y>h.y0-RADIUS&&p.y<h.y1+RADIUS)return false;
 return true;
}
export const zone=(p:Point)=>p.x<g.bayFront?'Garage forecourt':'Garage';
