import {createDoors} from './doors';
import data from './generated.json' with {type:'json'};
import {adapters} from './adapters.generated';
import {toLocal,toWorld} from './placement';
import {RADIUS} from './navigation';
import {createPortals,mapThrough,portalCoordinates,mapPlacement,type Portal} from './portals';
import type {Walker,Navigation,Placement,Point,RoomDefinition,HouseData} from './types';

export function createHouseRuntime(previewId?:string|null,source:HouseData=data){
 const requested=source.rooms.find(r=>r.id===previewId),preview=requested?.previewOnly?requested:undefined;
 const rooms=preview?[{...preview,position:[0,0,0],yaw:0}]:source.rooms.filter(r=>!r.previewOnly);
 const house={...source,rooms,connections:preview?[]:source.connections,start:requested?.id??source.start};
 const definitions:Record<string,RoomDefinition>=source.definitions,graph=createPortals(house);
 let activeRoom=house.start,activeSpace=graph.spaceOf(activeRoom),available:Set<string>|null=null;
 const initial=rooms.find(r=>r.id===house.start)!;
 const SPAWN=definitions[initial.definition].spawn,START=toWorld(SPAWN,initial),START_YAW=SPAWN.yaw+initial.yaw,START_PITCH=SPAWN.pitch;
 const isLoaded=(id:string)=>!available||available.has(id);
 const requireLoadedRooms=()=>{available=new Set();};
 const setRoomLoaded=(id:string,loaded:boolean)=>{if(loaded)available?.add(id);else available?.delete(id);};
 function activate(id:string){if(!rooms.some(r=>r.id===id))throw new Error('Unknown room: '+id);activeRoom=id;activeSpace=graph.spaceOf(id);}
 const resetSpace=()=>activate(house.start);
 function doorPortal(room:Placement,port:string,space=activeSpace){return graph.outgoing(space).find(p=>p.to.room.id===room.id&&p.to.port.id===port);}
 function doorPlacement(room:Placement,port:string,space=activeSpace){
  if(graph.spaceOf(room.id)===space)return room;
  const p=doorPortal(room,port,space);return p?mapPlacement(room,graph.portals.find(q=>q.key===p.reverse)!):null;
 }
 const doors=createDoors(rooms,definitions,(room,port,p)=>{
  if(graph.spaceOf(room.id)===activeSpace)return p;
  const edge=doorPortal(room,port);return edge?mapThrough(p,edge):null;
 });
 const portalDoor=(edge:Portal)=>doors.items.find(d=>(d.room.id===edge.from.room.id&&d.def.port===edge.from.port.id)||(d.room.id===edge.to.room.id&&d.def.port===edge.to.port.id));
 function nearOpening(p:Walker,edge:Portal,margin=RADIUS+.04){
  if(edge.from.port.kind==='hatch')return false;
  const q=portalCoordinates(p,edge);
  return Math.abs(q.along)<=.75&&Math.abs(q.across)<=Math.min(edge.from.port.width,edge.to.port.width)/2-margin&&Math.abs(q.height)<=.34;
 }
 function support(p:Point,height:number){
  const walker={...p,height};
  if(doors.blocks(walker))return;
  for(const room of graph.members(activeSpace)){
   const local=toLocal(walker,room);
   for(const box of definitions[room.definition].geometry?.doorObstacles??[]){
    if(local.height>=box.max[2]||local.height+1.62<=box.min[2])continue;
    const x=Math.max(box.min[0],Math.min(box.max[0],local.x)),y=Math.max(box.min[1],Math.min(box.max[1],local.y));
    if(Math.hypot(local.x-x,local.y-y)<RADIUS)return;
   }
  }
  for(const room of graph.members(activeSpace)){
   if(!isLoaded(room.id))continue;
   const local=toLocal(walker,room),def=definitions[room.definition],nav=adapters[def.navigation];
   if(local.x<def.bounds.min[0]||local.x>def.bounds.max[0]||local.y<def.bounds.min[1]||local.y>def.bounds.max[1])continue;
   if(nav.canStand(local,local.height))return {room,height:nav.floorHeight(local,local.height)+room.position[2],zone:nav.zone(local)};
  }
  // The source wall inset is walkable only in a declared, ready aperture.
  for(const edge of graph.outgoing(activeSpace)){
   if(!isLoaded(edge.from.room.id)||!isLoaded(edge.to.room.id)||!nearOpening(walker,edge))continue;
   const q=portalCoordinates(walker,edge);
   if(q.along<=.001||edge.continuous)return {room:edge.from.room,height:edge.from.point.height,zone:adapters[definitions[edge.from.room.definition].navigation].zone(toLocal(walker,edge.from.room))};
  }
 }
 const navigation:Navigation={canStand:(p,h=0)=>Boolean(support(p,h)),floorHeight:(p,h=0)=>support(p,h)?.height??NaN,zone:p=>support(p,p.height)?.zone??definitions[rooms.find(r=>r.id===activeRoom)!.definition].label};
 function moveWalker(start:Walker,dx:number,dy:number){
  let p={...start},yawDelta=0,heightDelta=0,crossed=false;
  const count=Math.max(1,Math.ceil(Math.hypot(dx,dy)/.045));let sx=dx/count,sy=dy/count;
  function attempt(x:number,y:number){
   const q={x:p.x+x,y:p.y+y,height:p.height};
   for(const edge of graph.outgoing(activeSpace)){
    const before=portalCoordinates(p,edge),after=portalCoordinates(q,edge);
    if(before.along>1e-7||after.along<=1e-7||!nearOpening(q,edge))continue;
    if(!isLoaded(edge.from.room.id)||!isLoaded(edge.to.room.id)||doors.blocks(q))return false;
    if(edge.continuous){activeRoom=edge.to.room.id;break;}
    const mapped=mapThrough(q,edge),oldRoom=activeRoom;
    activate(edge.to.room.id);
    const floor=support(mapped,mapped.height);
    if(!floor){activate(oldRoom);return false;}
    p={...mapped,height:floor.height};yawDelta+=edge.yaw;heightDelta+=edge.to.point.height-edge.from.point.height;crossed=true;
    const c=Math.cos(edge.yaw),s=Math.sin(edge.yaw),nx=c*sx-s*sy;sy=s*sx+c*sy;sx=nx;
    return true;
   }
   const floor=support(q,q.height);if(!floor)return false;
   p={...q,height:floor.height};activeRoom=floor.room.id;return true;
  }
  for(let i=0;i<count;i++)if(!attempt(sx,sy)){const previous=activeSpace;if(attempt(sx,0)&&activeSpace!==previous)continue;attempt(0,sy);}
  return {...p,yawDelta,heightDelta,crossed};
 }
 const zoneAt=(p:Walker)=>navigation.zone(p);
 return {doors,house,rooms,definitions,graph,portalDoor,doorPlacement,SPAWN,START,START_YAW,START_PITCH,navigation,moveWalker,zoneAt,isLoaded,requireLoadedRooms,setRoomLoaded,activate,resetSpace,
  get activeRoom(){return activeRoom;},get activeSpace(){return activeSpace;},preview:Boolean(preview),backgrounds:rooms.flatMap(r=>definitions[r.definition].backgrounds)};
}
export const {house,rooms,definitions,SPAWN,START,START_YAW,START_PITCH,navigation,moveWalker,zoneAt}=createHouseRuntime();
export type HouseRuntime=ReturnType<typeof createHouseRuntime>;
