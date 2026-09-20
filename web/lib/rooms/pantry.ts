/** Furnished pantry. Door passage is handled by the shared house portal/door system. */
import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const config=manifest.definitions.pantry.geometry;
export function floorHeight(p:Point,height=0){
 return Math.abs(height)<.34&&p.x>=-config.halfWidth&&p.x<=config.halfWidth&&p.y>=0&&p.y<=config.depth?0:NaN;
}
export function canStand(p:Point,height=0){
 for(const b of config.obstacles){const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;}
 const margin=RADIUS+config.wallThickness;
 return Number.isFinite(floorHeight(p,height))&&p.x>=-config.halfWidth+margin&&p.x<=config.halfWidth-margin&&p.y>=margin&&p.y<=config.depth-margin;
}
export const zone=()=> 'Pantry';
