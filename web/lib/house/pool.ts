import type {HouseRuntime} from './runtime';
import type {Walker} from './types';
import {toLocal,toWorld} from './placement';
import manifest from './generated.json' with {type:'json'};
type Choice={kind:'drain'|'fill'|'up'|'down';label:string};
/** Pool state and same-room ladder motion; no duplicated basin space or portal. */
export function createPool(view:HouseRuntime){
 const room=view.rooms.find(r=>r.id==='pool'),b=manifest.definitions.pool.geometry.pool,l=b.ladder;
 let flight:{start:Walker;finish:Walker;up:boolean;elapsed:number}|undefined;
 const facing=(p:Walker,x:number,y:number,yaw:number)=>{const dx=x-p.x,dy=y-p.y;return (-Math.sin(yaw)*dx+Math.cos(yaw)*dy)>Math.hypot(dx,dy)*.35;};
 function target(walker:Walker,yaw:number):Choice|null{
  if(!room||flight||view.activeRoom!=='pool'||!view.isLoaded('pool'))return null;
  const p=toLocal(walker,room),angle=yaw-room.yaw;
  if(view.poolState.drained){
   for(const [kind,end] of [['up',l.lower],['down',l.upper]] as const){
    if(Math.abs(p.height-end.height)<.3&&Math.hypot(p.x-end.x,p.y-end.y)<.8&&facing(p,l.shaft.x,l.shaft.y,angle))return {kind,label:kind==='up'?'Climb out of pool':'Climb into pool'};
   }
  }
  if(Math.abs(p.height)>.3)return null;
  const x=Math.max(b.x0,Math.min(b.x1,p.x)),y=Math.max(b.y0,Math.min(b.y1,p.y));
  if(Math.hypot(p.x-x,p.y-y)>1.8||!facing(p,(b.x0+b.x1)/2,(b.y0+b.y1)/2,angle))return null;
  return view.poolState.drained?{kind:'fill',label:'Refill pool'}:{kind:'drain',label:'Drain pool'};
 }
 function begin(choice:Choice,walker:Walker,yaw:number){
  if(!room||target(walker,yaw)?.kind!==choice.kind)return false;
  if(choice.kind==='drain'||choice.kind==='fill'){view.poolState.drained=choice.kind==='drain';return true;}
  flight={start:toLocal(walker,room),finish:choice.kind==='up'?l.upper:l.lower,up:choice.kind==='up',elapsed:0};return true;
 }
 function step(dt:number){
  if(!flight||!room)return null;
  const f=flight,duration=-b.bottom/1.25,total=duration+1;f.elapsed=Math.min(total,f.elapsed+Math.max(0,dt));
  const a={...l.shaft,height:f.up?b.bottom:0},z={...l.shaft,height:f.up?0:b.bottom};
  const mix=(a:Walker,b:Walker,t:number)=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,height:a.height+(b.height-a.height)*t});
  const ease=(t:number)=>t*t*(3-2*t);
  const p=f.elapsed<.5?mix(f.start,a,ease(f.elapsed/.5)):f.elapsed<.5+duration?mix(a,z,(f.elapsed-.5)/duration):mix(z,f.finish,ease((f.elapsed-.5-duration)/.5));
  const done=f.elapsed===total;if(done)flight=undefined;
  return {walker:toWorld(p,room),done};
 }
 return {target,begin,step,cancel(){flight=undefined;},get active(){return Boolean(flight);}};
}
