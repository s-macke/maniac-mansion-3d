import type {HouseRuntime} from './runtime';
import type {CrawlLink,Walker} from './types';
import {toWorld} from './placement';
import {mapThrough,portalCoordinates,type Portal} from './portals';
import {EYE_HEIGHT} from './navigation';
const LOW_EYE=.42,SETTLE=.6,SPEED=.8;
const mix=(a:Walker,b:Walker,t:number):Walker=>({x:a.x+(b.x-a.x)*t,y:a.y+(b.y-a.y)*t,height:a.height+(b.height-a.height)*t});
const ease=(t:number)=>t*t*(3-2*t);
type Choice={link:CrawlLink;forward:boolean;edge:Portal;label:string;ready:boolean};
export function createCrawls(view:HouseRuntime){
 let flight:{choice:Choice;points:Walker[];lengths:number[];distance:number;time:number}|undefined;
 const room=(id:string)=>view.rooms.find(r=>r.id===id)!;
 const at=(end:CrawlLink['a'])=>toWorld(end.landing,room(end.room));
 function target(p:Walker,yaw:number):Choice|null{
  if(flight)return null;
  for(const link of view.house.crawls??[])for(const forward of [true,false]){
   const end=forward?link.a:link.b;if(view.activeRoom!==end.room)continue;
   const landing=at(end);if(Math.hypot(p.x-landing.x,p.y-landing.y)>.8||Math.abs(p.height-landing.height)>.25)continue;
   const edge=view.graph.outgoing(view.activeSpace).find(e=>e.from.port.id===end.port)!;
   const dx=edge.from.point.x-p.x,dy=edge.from.point.y-p.y;
   if((-Math.sin(yaw)*dx+Math.cos(yaw)*dy)/Math.hypot(dx,dy)<.3)continue;
   const door=view.portalDoor(edge)!,loaded=view.isLoaded(edge.from.room.id)&&view.isLoaded(edge.to.room.id);
   const ready=loaded&&door.amount===door.target;
   return {link,forward,edge,ready,label:!loaded?'Loading passage…':door.blocked?'Step back · Grating blocked':door.amount!==door.target?'Moving metal grating…':door.amount===0?'Open metal grating':forward?'Crawl under house':'Crawl outside'};
  }
  return null;
 }
 function begin(choice:Choice,p:Walker,yaw:number){
  const current=target(p,yaw);if(!current?.ready||current.link.id!==choice.link.id)return false;
  const door=view.portalDoor(choice.edge)!;
  if(door.amount===0){view.doors.toggle(door.key);return false;}
  const edge=view.graph.portals.find(e=>e.from.room.id===choice.link.a.room&&e.from.port.id===choice.link.a.port)!,reverse=view.graph.portals.find(e=>e.key===edge.reverse)!;
  let points=[at(choice.link.a),...choice.link.waypoints.map(p=>toWorld(p,room(choice.link.a.room))),mapThrough(at(choice.link.b),reverse)];
  if(!choice.forward)points=points.reverse().map(p=>mapThrough(p,edge));
  points[0]={...p};const lengths=points.slice(1).map((b,i)=>Math.hypot(b.x-points[i].x,b.y-points[i].y,b.height-points[i].height));
  flight={choice,points,lengths,distance:lengths.reduce((a,b)=>a+b,0),time:0};return true;
 }
 function step(dt:number){
  if(!flight)return null;const f=flight,duration=f.distance/SPEED+2*SETTLE;f.time=Math.min(duration,f.time+Math.max(0,dt));
  let distance=Math.max(0,Math.min(f.distance,(f.time-SETTLE)*SPEED)),p=f.points[0];
  for(let i=0;i<f.lengths.length;i++){const length=f.lengths[i];p=mix(f.points[i],f.points[i+1],length?Math.min(1,distance/length):1);if(distance<=length)break;distance-=length;}
  const progress=f.time<SETTLE?ease(f.time/SETTLE):f.time>duration-SETTLE?ease((duration-f.time)/SETTLE):1;
  const eyeHeight=EYE_HEIGHT+(LOW_EYE-EYE_HEIGHT)*progress;
  const crossed=portalCoordinates(p,f.choice.edge).along>=0,destination=crossed?f.choice.edge.to.room.id:f.choice.edge.from.room.id;
  const changed=view.activeRoom!==destination;if(changed)view.activate(destination);
  const walker=crossed?mapThrough(p,f.choice.edge):p,done=f.time===duration;
  if(done)flight=undefined;
  return {walker,eyeHeight,yawDelta:changed?f.choice.edge.yaw:0,done};
 }
 return {target,begin,step,cancel(){flight=undefined;},get active(){return Boolean(flight);}};
}
