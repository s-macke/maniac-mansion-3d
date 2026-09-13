import {createDoors} from './doors';
import data from './generated.json' with {type:'json'};
import { adapters } from './adapters.generated';
import { toLocal, toWorld } from './placement';
import { moveWalker as step, RADIUS } from './navigation';
import type { Walker, Navigation, Placement, Point, RoomDefinition } from './types';
export function createHouseRuntime(previewId?:string|null){
 const allRooms:Placement[]=data.rooms;
 const requested=previewId?allRooms.find(r=>r.id===previewId):undefined;
 const preview=requested?.previewOnly?requested:undefined;
 const rooms:Placement[]=preview?[{...preview,position:[0,0,0],yaw:0}]:allRooms.filter(r=>!r.previewOnly);
 const house={...data,start:requested?requested.id:data.start};
 const definitions:Record<string,RoomDefinition>=data.definitions;
 const doors=createDoors(rooms,definitions);
 const initial=rooms.find(r=>r.id===house.start)!;
 let available:Set<string>|null=null;
 const requireLoadedRooms=()=>{available=new Set();};
 const setRoomLoaded=(id:string,loaded:boolean)=>{if(available){if(loaded)available.add(id);else available.delete(id);}};
 const SPAWN=definitions[initial.definition].spawn;
 const START=toWorld(SPAWN,initial),START_YAW=SPAWN.yaw+initial.yaw,START_PITCH=SPAWN.pitch;
function candidates(p:Point,height:number) {
 return rooms.flatMap(room=>{
  if(available&&!available.has(room.id))return [];
  const local=toLocal({...p,height},room),def=definitions[room.definition];
  if(local.x<def.bounds.min[0]||local.x>def.bounds.max[0]||local.y<def.bounds.min[1]||local.y>def.bounds.max[1])return [];
  const nav=adapters[def.navigation];
  if(!nav)throw new Error('Missing navigation adapter: '+def.navigation);
  return [{room,local,nav}];
 });
}
function support(p:Point,height:number) {
 if(doors.blocks({...p,height}))return;
 // Physical door leaves also block the portal bridge and neighboring room support.
 for(const room of rooms){
  const local=toLocal({...p,height},room);
  for(const box of definitions[room.definition].geometry?.doorObstacles??[]){
   if(local.height>=box.max[2]||local.height+1.62<=box.min[2])continue;
   const x=Math.max(box.min[0],Math.min(box.max[0],local.x)),y=Math.max(box.min[1],Math.min(box.max[1],local.y));
   if(Math.hypot(local.x-x,local.y-y)<RADIUS)return;
  }
 }
 const inside=candidates(p,height).find(({local,nav})=>nav.canStand(local,local.height));
 if(inside)return inside;
 // Only declared, aligned doorways bridge the conservative room-wall collision bounds.
 for(const link of preview?[]:house.connections){
  const a=rooms.find(r=>r.id===link.a.instance),b=rooms.find(r=>r.id===link.b.instance);
  if(!a||!b||(available&&(!available.has(a.id)||!available.has(b.id))))continue;
  const port=definitions[a.definition].ports.find(p=>p.id===link.a.port)!;
  const other=definitions[b.definition].ports.find(p=>p.id===link.b.port)!;
  if(port.state!=='open'||other.state!=='open')continue;
  const local=toLocal({...p,height},a),dx=local.x-port.position[0],dy=local.y-port.position[1];
  const along=dx*port.outward[0]+dy*port.outward[1],across=-dx*port.outward[1]+dy*port.outward[0];
  if(Math.abs(along)>.75||Math.abs(across)>port.width/2-RADIUS-.04||Math.abs(local.height-port.position[2])>.34)continue;
  const room=along<=0?a:b,point=toLocal({...p,height},room),floor=port.position[2]+a.position[2]-room.position[2];
  const nav:Navigation={canStand:()=>true,floorHeight:()=>floor,zone:()=>adapters[definitions[room.definition].navigation].zone(point)};
  return {room,local:point,nav};
 }
}
const navigation:Navigation={
 canStand:(p,height=0)=>Boolean(support(p,height)),
 floorHeight:(p,height=0)=>{
  const hit=support(p,height);
  return hit?hit.nav.floorHeight(hit.local,hit.local.height)+hit.room.position[2]:NaN;
 },
 zone:(p)=>{const hit=support(p,p.height);return hit?hit.nav.zone(hit.local):'House';},
};
const moveWalker=(p:Walker,dx:number,dy:number)=>step(p,dx,dy,navigation);
const zoneAt=(p:Walker)=>navigation.zone(p);
return {doors,house,rooms,definitions,SPAWN,START,START_YAW,START_PITCH,navigation,moveWalker,zoneAt,requireLoadedRooms,setRoomLoaded,preview:Boolean(preview),backgrounds:rooms.flatMap(r=>definitions[r.definition].backgrounds)};
}
export const {house,rooms,definitions,SPAWN,START,START_YAW,START_PITCH,navigation,moveWalker,zoneAt}=createHouseRuntime();
