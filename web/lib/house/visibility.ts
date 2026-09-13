import type { Walker, Placement } from './types';
import { toLocal } from './placement';
/** Bounding-box distance avoids unloading a large room while still inside it. */
export function roomDistance(p:Walker,room:Placement,bounds:{min:number[];max:number[]}) {
 const q=toLocal(p,room),v=[q.x,q.y,q.height];
 return Math.hypot(...v.map((x,i)=>Math.max(bounds.min[i]-x,0,x-bounds.max[i])));
}
export function nearbyRooms(p:Walker,rooms:Placement[],definitions:Record<string,{bounds:{min:number[];max:number[]}}>,loaded:Set<string>,loadRadius:number,unloadRadius:number) {
 return new Set(rooms.filter(r=>roomDistance(p,r,definitions[r.definition].bounds)<=(loaded.has(r.id)?unloadRadius:loadRadius)).map(r=>r.id));
}
