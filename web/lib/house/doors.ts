import {toLocal} from './placement';
import {RADIUS} from './navigation';
import type {Placement, RoomDefinition, Walker, DoorLeaf} from './types';

export function leafAngle(leaf:DoorLeaf,amount:number){return (amount-1)*leaf.openAngle;}
/** The exported rest pose is open. Rotate the walker back into that pose for an exact oriented-box test. */
export function touchesLeaf(p:Walker,leaf:DoorLeaf,amount:number,radius=RADIUS){
 if(p.height>=leaf.max[2]||p.height+1.62<=leaf.min[2])return false;
 const a=-leafAngle(leaf,amount),c=Math.cos(a),s=Math.sin(a),dx=p.x-leaf.hinge[0],dy=p.y-leaf.hinge[1];
 const x=leaf.hinge[0]+c*dx-s*dy,y=leaf.hinge[1]+s*dx+c*dy;
 const qx=Math.max(leaf.min[0],Math.min(leaf.max[0],x)),qy=Math.max(leaf.min[1],Math.min(leaf.max[1],y));
 return Math.hypot(x-qx,y-qy)<radius;
}
export function createDoors(rooms:Placement[],definitions:Record<string,RoomDefinition>){
 const items=rooms.flatMap(room=>(definitions[room.definition].geometry?.doors??[]).map(def=>({
  key:room.id+':'+def.id,room,def,port:definitions[room.definition].ports.find(p=>p.id===def.port)!,amount:def.initialOpen?1:0,target:def.initialOpen?1:0,blocked:false,
 })));
 function toggle(key:string){const door=items.find(d=>d.key===key);if(!door)return false;door.target=door.target===1?0:1;door.blocked=false;return true;}
 function update(dt:number,walker:Walker){
  if(dt<=0)return false;
  let changed=false;
  for(const door of items){
   door.blocked=false;if(door.amount===door.target)continue;
   const local=toLocal(walker,door.room),direction=Math.sign(door.target-door.amount);
   const end=door.amount+direction*Math.min(Math.abs(door.target-door.amount),Math.max(0,dt)/.8);
   const steps=Math.max(1,Math.ceil(Math.abs(end-door.amount)/.01)),start=door.amount;
   for(let i=1;i<=steps;i++){
    const next=i===steps?end:start+(end-start)*(i/steps);
    if(door.def.leaves.some(leaf=>touchesLeaf(local,leaf,next,RADIUS+.025))){door.blocked=true;break;}
    door.amount=next;changed=true;
   }
  }
  return changed;
 }
 function blocks(walker:Walker){return items.some(d=>d.def.leaves.some(l=>touchesLeaf(toLocal(walker,d.room),l,d.amount)));}
 return {items,toggle,update,blocks};
}
export type Doors=ReturnType<typeof createDoors>;
