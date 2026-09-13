import {toWorld} from './placement';
import type {HouseData, Placement, Port, Walker} from './types';

export type PortalEnd={room:Placement;port:Port;space:string;point:Walker;normal:{x:number;y:number}};
export type Portal={key:string;reverse:string;from:PortalEnd;to:PortalEnd;yaw:number;continuous:boolean};
export function createPortals(house:HouseData){
 const spaceOf=(id:string)=>house.spaces?.find(g=>g.rooms.includes(id))?.id??id;
 const end=(ref:{instance:string;port:string}):PortalEnd=>{
  const room=house.rooms.find(r=>r.id===ref.instance)!;
  const port=house.definitions[room.definition].ports.find(p=>p.id===ref.port)!;
  const c=Math.cos(room.yaw),s=Math.sin(room.yaw),[x,y,height]=port.position;
  return {room,port,space:spaceOf(room.id),point:toWorld({x,y,height},room),normal:{x:c*port.outward[0]-s*port.outward[1],y:s*port.outward[0]+c*port.outward[1]}};
 };
 const portals=house.connections.flatMap((link,i)=>{
  const a=end(link.a),b=end(link.b);
  return [[a,b],[b,a]].map(([from,to],side)=>({key:`${i}:${side}`,reverse:`${i}:${1-side}`,from,to,
   yaw:Math.atan2(-to.normal.y,-to.normal.x)-Math.atan2(from.normal.y,from.normal.x),continuous:from.space===to.space}));
 });
 return {portals,spaceOf,members:(space:string)=>house.rooms.filter(r=>spaceOf(r.id)===space),outgoing:(space:string)=>portals.filter(p=>p.from.space===space)};
}
export function mapThrough(p:Walker,portal:Portal):Walker{
 const c=Math.cos(portal.yaw),s=Math.sin(portal.yaw),x=p.x-portal.from.point.x,y=p.y-portal.from.point.y;
 return {x:portal.to.point.x+c*x-s*y,y:portal.to.point.y+s*x+c*y,height:portal.to.point.height+p.height-portal.from.point.height};
}
export function portalCoordinates(p:Walker,portal:Portal){
 const {point,normal}=portal.from,dx=p.x-point.x,dy=p.y-point.y;
 return {along:dx*normal.x+dy*normal.y,across:-dx*normal.y+dy*normal.x,height:p.height-point.height};
}
export function mapPlacement(room:Placement,portal:Portal):Placement{
 const p=mapThrough({x:room.position[0],y:room.position[1],height:room.position[2]},portal);
 return {...room,position:[p.x,p.y,p.height],yaw:room.yaw+portal.yaw};
}
