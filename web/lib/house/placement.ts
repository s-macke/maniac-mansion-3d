import type { Placement, Walker } from './types';
export function toWorld(p:Walker, room:Placement):Walker {
 const c=Math.cos(room.yaw),s=Math.sin(room.yaw),[x,y,z]=room.position;
 return {x:x+c*p.x-s*p.y,y:y+s*p.x+c*p.y,height:z+p.height};
}
export function toLocal(p:Walker, room:Placement):Walker {
 const c=Math.cos(room.yaw),s=Math.sin(room.yaw),[x,y,z]=room.position,dx=p.x-x,dy=p.y-y;
 return {x:c*dx+s*dy,y:-s*dx+c*dy,height:p.height-z};
}
