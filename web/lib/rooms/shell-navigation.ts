import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
type Shell={label:string;geometry:{halfWidth:number;depth:number;height:number;wallThickness:number;floorHoles?:{x0:number;x1:number;y0:number;y1:number}[];stairs?:{x0:number;x1:number;y0:number;y1:number;rise:number}}};
/** Rectangular shells with an optional straight stair on either side. */
export function shellNavigation(c:Shell){
 const g=c.geometry,s=g.stairs;
 function floorHeight(p:Point,height=0){
  if(p.x< -g.halfWidth||p.x>g.halfWidth||p.y<0||p.y>g.depth)return NaN;
  if(s&&p.x>=s.x0&&p.x<=s.x1&&p.y>=s.y0)return Math.min(1,(p.y-s.y0)/(s.y1-s.y0))*s.rise;
  return Math.abs(height)<.34?0:NaN;
 }
 function canStand(p:Point,height=0){
  const h=floorHeight(p,height),margin=RADIUS+g.wallThickness;
  if(!Number.isFinite(h)||Math.abs(h-height)>.34)return false;
  if(p.x< -g.halfWidth+margin||p.x>g.halfWidth-margin||p.y<margin||p.y>g.depth-margin)return false;
  for(const hole of g.floorHoles??[])if(p.x>hole.x0-RADIUS&&p.x<hole.x1+RADIUS&&p.y>hole.y0-RADIUS&&p.y<hole.y1+RADIUS)return false;
  if(s&&p.y>=s.y0&&p.x>=s.x0-RADIUS&&p.x<=s.x1+RADIUS&&(p.x<s.x0+RADIUS||p.x>s.x1-RADIUS))return false;
  return true;
 }
 return {floorHeight,canStand,zone:()=>c.label};
}
