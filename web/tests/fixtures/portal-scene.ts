import * as THREE from 'three';
import data from '../../lib/house/generated.json' with {type:'json'};
import {createHouseRuntime} from '../../lib/house/runtime';
import {createHouseAssets} from '../../lib/house/assets';
import {createPortalRenderer,portalCamera} from '../../lib/house/portal-renderer';
import type {HouseData} from '../../lib/house/types';

const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setSize(640,360);renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.NoToneMapping;document.body.append(renderer.domElement);
let assets:ReturnType<typeof createHouseAssets>|undefined,frame=0,ready=false;
let camera:THREE.PerspectiveCamera,view:ReturnType<typeof createHouseRuntime>;
async function build(shifted:boolean){
 cancelAnimationFrame(frame);assets?.dispose();ready=false;
 const source:HouseData=structuredClone(data);
 if(shifted){const room=source.rooms.find(r=>r.id==='kitchen')!;room.position=[200,-100,7];room.yaw+=Math.PI/2;}
 view=createHouseRuntime('hall',source);for(const door of view.doors.items)door.amount=door.target=1;
 const scene=new THREE.Scene();scene.background=new THREE.Color(0);
 camera=new THREE.PerspectiveCamera(68,640/360,.05,60);camera.position.set(-3.72,1.62,-4.7);camera.lookAt(-3.72,1.62,-8);
 const errors:string[]=[];
 assets=createHouseAssets(scene,{changed:()=>{},progress:()=>{},ready:()=>{},error:e=>errors.push(e)},view);
 function tick(){assets!.update(view.START);assets!.render(renderer,camera);frame=requestAnimationFrame(tick);}
 tick();
 const start=performance.now();
 while(!['hall','kitchen','dining_room','pantry'].every(id=>assets!.loadedRooms.includes(id))){
  if(errors.length)throw new Error(errors.join('\n'));
  if(performance.now()-start>30000)throw new Error('Portal chain did not load: '+assets!.loadedRooms.join(','));
  await new Promise(resolve=>setTimeout(resolve,50));
 }
 await new Promise(resolve=>setTimeout(resolve,300));ready=true;
}
function pixels(){const gl=renderer.getContext(),buffer=new Uint8Array(640*360*4);assets!.render(renderer,camera);gl.readPixels(0,0,640,360,gl.RGBA,gl.UNSIGNED_BYTE,buffer);return buffer;}
// Subpixel diagonal geometry exposes missing coverage inside the portal image,
// independently of the canvas's own antialiasing and the room artwork.
function antialiasProbe(){
 const probeView=createHouseRuntime('hall');for(const door of probeView.doors.items)door.amount=door.target=1;
 const edge=probeView.graph.outgoing(probeView.activeSpace).find(e=>e.to.room.id==='kitchen')!;
 const probeCamera=new THREE.PerspectiveCamera(68,640/360,.05,60);
 probeCamera.position.set(-3.72,1.62,-4.7);probeCamera.lookAt(-3.72,1.62,-8);
 const child=portalCamera(probeCamera,edge),scene=new THREE.Scene();scene.background=new THREE.Color(0);
 const bars=new THREE.Group();bars.position.copy(child.position).add(child.getWorldDirection(new THREE.Vector3()).multiplyScalar(4));bars.quaternion.copy(child.quaternion);scene.add(bars);
 const geometry=new THREE.PlaneGeometry(.012,2.2),material=new THREE.MeshBasicMaterial({color:0xffffff});
 for(let i=-12;i<=12;i++){const bar=new THREE.Mesh(geometry,material);bar.position.x=i*.065;bar.rotation.z=.37;bars.add(bar);}
 const max=renderer.capabilities.maxSamples;
 function measure(limit:number){
  renderer.capabilities.maxSamples=limit;
  const portals=createPortalRenderer(renderer,scene,probeView,space=>{bars.visible=space===edge.to.space;});
  portals.render(probeCamera);const gl=renderer.getContext(),pixels=new Uint8Array(640*360*4);gl.readPixels(0,0,640,360,gl.RGBA,gl.UNSIGNED_BYTE,pixels);
  let covered=0,partial=0;
  for(let y=130;y<230;y++)for(let x=275;x<365;x++){const value=pixels[(y*640+x)*4];if(value>0)covered++;if(value>5&&value<250)partial++;}
  const targets=portals.stats.targets;portals.dispose();return {covered,partial,targets};
 }
 try{return {maxSamples:max,without:measure(0),with:measure(max)};}
 finally{renderer.capabilities.maxSamples=max;geometry.dispose();material.dispose();}
}
const api={build,pixels,antialiasProbe,get ready(){return ready;},get stats(){return assets?.portalStats;},get memory(){return renderer.info.memory;},
 near(){camera.position.set(-3.72,1.62,-6.49);camera.lookAt(-3.72,1.62,-8);const data=pixels();let lit=0;for(let i=0;i<data.length;i+=4)if(data[i]+data[i+1]+data[i+2]>10)lit++;return lit/(640*360);},
 close(){for(const door of view.doors.items)door.amount=door.target=0;assets!.doorView.sync();assets!.render(renderer,camera);return assets!.portalStats;},
 dispose(){cancelAnimationFrame(frame);assets?.dispose();renderer.dispose();}};
(window as unknown as {portalFixture:typeof api}).portalFixture=api;
