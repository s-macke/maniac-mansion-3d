import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const c=manifest.definitions.front_exterior.geometry;
export function floorHeight(p:Point){
 if(Math.abs(p.x)>c.halfWidth||p.y<c.front||p.y>0)return NaN;
 if(p.y>=c.porchFront)return Math.abs(p.x)<=8.3?0:NaN;
 if(p.y>=c.stairFront&&Math.abs(p.x)<=c.stairHalfWidth){
  const step=Math.min(c.steps,Math.floor((p.y-c.stairFront)/(c.porchFront-c.stairFront)*c.steps)+1);
  return c.ground*(1-step/c.steps);
 }
 return c.ground;
}
export function canStand(p:Point,height=c.ground){
 const h=floorHeight(p);
 if(!Number.isFinite(h)||Math.abs(h-height)>.34)return false;
 if(Math.abs(p.x)>12.5-RADIUS||p.y<c.front+RADIUS||p.y>-.18-RADIUS)return false;
 // Porch balustrade and stair cheeks keep the walker on the modeled route.
 if(p.y>c.porchFront-RADIUS&&p.y< -1.85+RADIUS&&Math.abs(p.x)>1.5-RADIUS)return false;
 if(p.y>=c.stairFront-.1&&p.y<c.porchFront&&Math.abs(Math.abs(p.x)-1.64)<RADIUS+.13)return false;
 if(h===0&&Math.abs(p.x)>8.15-RADIUS)return false;
 for(const b of c.bushes){const x=Math.max(b.x-b.width/2,Math.min(b.x+b.width/2,p.x)),y=Math.max(b.y-b.depth/2,Math.min(b.y+b.depth/2,p.y));if(h<c.ground+b.height&&Math.hypot(p.x-x,p.y-y)<RADIUS)return false;}
 for(const b of c.obstacles){const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;}
 return true;
}
export const zone=()=> 'Front exterior';
