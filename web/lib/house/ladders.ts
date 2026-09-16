import type {HouseRuntime} from './runtime';
import type {LadderLink,LadderEnd,Walker} from './types';
import {toWorld} from './placement';
import {mapThrough,type Portal} from './portals';
import {EYE_HEIGHT} from './navigation';
type Choice={link:LadderLink;up:boolean;label:string;ready:boolean;yaw:number};
type Flight={choice:Choice;edge:Portal;reverse:Portal;start:Walker;shaft:Walker;finish:Walker;rise:number;elapsed:number;duration:number};
const mix=(a:Walker,b:Walker,t:number):Walker=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,height:a.height+(b.height-a.height)*t});
const ease=(t:number)=>t*t*(3-2*t);
/** Guided motion; camera crossing the horizontal portal changes the active room. No fade. */
export function createLadders(view:HouseRuntime){
 let flight:Flight|undefined;
 const room=(id:string)=>view.rooms.find(r=>r.id===id)!;
 const landing=(e:LadderEnd)=>toWorld(e.landing,room(e.room));
 function target(p:Walker,yaw:number):Choice|null{
  if(flight)return null;
  for(const link of view.house.ladders??[])for(const up of [true,false]){
   const end=up?link.lower:link.upper,destination=up?link.upper:link.lower;
   if(view.activeRoom!==end.room)continue;
   const at=landing(end),shaft=toWorld({...end.shaft,height:end.landing.height},room(end.room));
   if(Math.hypot(p.x-at.x,p.y-at.y)>1.15||Math.abs(p.height-at.height)>.3)continue;
   const dx=shaft.x-p.x,dy=shaft.y-p.y,length=Math.hypot(dx,dy);
   if(length>.1&&(-Math.sin(yaw)*dx+Math.cos(yaw)*dy)/length<.35)continue;
   return {link,up,label:`Climb ${up?'up':'down'} to ${view.definitions[room(destination.room).definition].label}`,ready:view.isLoaded(end.room)&&view.isLoaded(destination.room),yaw:end.yaw+room(end.room).yaw};
  }
  return null;
 }
 function begin(choice:Choice,p:Walker,yaw:number){
  if(flight||target(p,yaw)?.link.id!==choice.link.id||!view.isLoaded(choice.link.lower.room)||!view.isLoaded(choice.link.upper.room))return false;
  const {lower,upper}=choice.link,edge=view.graph.portals.find(e=>e.from.room.id===lower.room&&e.from.port.id===lower.port)!;
  const reverse=view.graph.portals.find(e=>e.key===edge.reverse)!;
  const base=landing(lower),rise=edge.from.point.height-base.height;
  flight={choice,edge,reverse,start:choice.up?p:mapThrough(p,reverse),shaft:toWorld({...lower.shaft,height:lower.landing.height},room(lower.room)),finish:choice.up?mapThrough(landing(upper),reverse):base,rise,elapsed:0,duration:rise/1.25};
  return true;
 }
 function step(dt:number){
  if(!flight)return null;
  const f=flight;f.elapsed=Math.min(1+f.duration,f.elapsed+Math.max(0,dt));
  const low=f.shaft,high={...low,height:low.height+f.rise},a=f.choice.up?low:high,b=f.choice.up?high:low;
  const p=f.elapsed<.5?mix(f.start,a,ease(f.elapsed/.5)):f.elapsed<.5+f.duration?mix(a,b,(f.elapsed-.5)/f.duration):mix(b,f.finish,ease((f.elapsed-.5-f.duration)/.5));
  const upper=p.height+EYE_HEIGHT>=f.edge.from.point.height,destination=upper?f.choice.link.upper.room:f.choice.link.lower.room;
  const crossed=view.activeRoom!==destination,yawDelta=crossed?(upper?f.edge.yaw:f.reverse.yaw):0;
  if(crossed)view.activate(destination);
  const walker=upper?mapThrough(p,f.edge):p,done=f.elapsed>=1+f.duration;
  if(done)flight=undefined;
  return {walker,yawDelta,done};
 }
 return {target,begin,step,cancel(){flight=undefined;},get active(){return Boolean(flight);},get progress(){return flight?flight.elapsed/(1+flight.duration):null;}};
}
