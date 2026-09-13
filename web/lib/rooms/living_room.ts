import type {Point} from '../house/types';
import {RADIUS} from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const config=manifest.definitions.living_room.geometry;
export function floorHeight(p:Point,height=0){return Math.abs(height)<.34&&p.x>=-config.halfWidth&&p.x<=config.halfWidth&&p.y>=0&&p.y<=config.depth?0:NaN;}
export function canStand(p:Point,height=0){
 if(!Number.isFinite(floorHeight(p,height)))return false;
 if(p.x< -config.halfWidth+RADIUS+.24||p.x>config.halfWidth-RADIUS-.15||p.y<RADIUS+.1||p.y>config.depth-RADIUS-.2)return false;
 for(const b of config.obstacles){const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));if(Math.hypot(p.x-x,p.y-y)<RADIUS)return false;}
 return true;
}
export const zone=()=> 'Living room';
