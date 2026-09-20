'use client';
import { useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { EYE_HEIGHT } from '@/lib/house/navigation';
import { createHouseRuntime } from '@/lib/house/runtime';
import { createHouseAssets } from '@/lib/house/assets';
import {createPool} from '@/lib/house/pool';
import {createCrawls} from '@/lib/house/crawls';
import {createLadders} from '@/lib/house/ladders';
import * as THREE from 'three';

type Runtime = { interact:()=>void; enter: (capture?:boolean) => void; reset: () => void; pause: () => void; key: (key:string,down:boolean)=>void };
export default function Walkthrough() {
  const host=useRef<HTMLDivElement>(null),runtime=useRef<Runtime|null>(null);
  const [ready,setReady]=useState(false),[progress,setProgress]=useState(0),[active,setActive]=useState(false);
  const [doorAction,setDoorAction]=useState('');
  const [showHint,setShowHint]=useState(true);
  const [zone,setZone]=useState('Entrance hall');
  const [preview,setPreview]=useState(false);
  const [error,setError]=useState(''),[fallback,setFallback]=useState(true),[touch,setTouch]=useState(false);
  useEffect(()=>{
    const view=createHouseRuntime(new URLSearchParams(window.location.search).get('room'));
    const ladders=createLadders(view),crawls=createCrawls(view),pool=createPool(view);
    const {START,START_YAW,START_PITCH,moveWalker,zoneAt}=view;
    setPreview(view.preview);setZone(zoneAt(START));
    const container=host.current!;let disposed=false,frame=0,walking=false,dragging=false,needsRender=true;let lastZone=zoneAt(START);
    let loaded=false,hadLock=false,distanceWalked=0,hintFinished=false;
    const coarse=matchMedia('(pointer:coarse)').matches;setTouch(coarse);
    let renderer:THREE.WebGLRenderer;
    try { renderer=new THREE.WebGLRenderer({antialias:true,powerPreference:'high-performance'}); }
    catch { setError('This browser could not start 3D graphics. Try Chrome or Firefox with hardware acceleration enabled.');return; }
    renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.NoToneMapping;
    renderer.setPixelRatio(Math.min(devicePixelRatio,1.5));container.appendChild(renderer.domElement);
    const scene=new THREE.Scene();scene.background=new THREE.Color(0x000000);
    const camera=new THREE.PerspectiveCamera(68,1,.05,60);camera.rotation.order='YXZ';
    let walker={...START},yaw=START_YAW,pitch=START_PITCH,eye=START.height+EYE_HEIGHT,last=performance.now();
    const keys=new Set<string>();
    const sync=()=>{camera.position.set(walker.x,eye,-walker.y);camera.rotation.set(pitch,yaw,0);};sync();
    const resize=()=>{const {width,height}=container.getBoundingClientRect();renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();needsRender=true;};resize();
    const observer=new ResizeObserver(resize);observer.observe(container);
    const pause=()=>{walking=false;keys.clear();dragging=false;setActive(false);if(document.pointerLockElement===renderer.domElement)document.exitPointerLock();};
    const reset=()=>{ladders.cancel();crawls.cancel();pool.cancel();view.resetSpace();walker={...START};yaw=START_YAW;pitch=START_PITCH;eye=START.height+EYE_HEIGHT;keys.clear();sync();needsRender=true;};
    const enableFallback=()=>{if(!disposed){setFallback(true);walking=true;setActive(true);container.focus();}};
    const enter=(capture=true)=>{
      if(!loaded||disposed)return;
      walking=true;setActive(true);container.focus();
      if(!capture || coarse || !renderer.domElement.requestPointerLock){enableFallback();return;}
      try { const p=renderer.domElement.requestPointerLock();if(p)p.catch(enableFallback); }catch{enableFallback();}
    };
    const interact=(point?:THREE.Vector2)=>{if(!walking||ladders.active||crawls.active||pool.active)return;const poolChoice=pool.target(walker,yaw);if(poolChoice){if(pool.begin(poolChoice,walker,yaw))keys.clear();needsRender=true;return;}const crawl=crawls.target(walker,yaw);if(crawl){const hit=point?assets.doorView.target(camera,point):null;if(hit){view.doors.toggle(hit.key);}else if(crawls.begin(crawl,walker,yaw))keys.clear();needsRender=true;return;}const ladder=ladders.target(walker,yaw);if(ladder){if(ladders.begin(ladder,walker,yaw)){keys.clear();needsRender=true;}return;}const door=assets.doorView.target(camera,point);if(door){view.doors.toggle(door.key);needsRender=true;}};
    runtime.current={interact:()=>interact(),enter,reset,pause,key:(key,down)=>{if(down)keys.add(key);else keys.delete(key);}};
    const onLock=()=>{const locked=document.pointerLockElement===renderer.domElement;
      if(hadLock&&!locked)pause();if(locked)dragging=false;hadLock=locked;setFallback(!locked);
    };
    const onLockError=()=>enableFallback();
    const onKey=(e:KeyboardEvent)=>{
      if(e.code==='Escape'){pause();return;}
      if(!walking)return;
      if(e.code==='KeyE'&&!e.repeat){e.preventDefault();interact();return;}
      if(['KeyW','KeyA','KeyS','KeyD','ArrowUp','ArrowDown','ArrowLeft','ArrowRight','ShiftLeft','ShiftRight','KeyR'].includes(e.code)) {
        e.preventDefault();if(e.code==='KeyR')reset();else keys.add(e.code);
      }
    };
    const onUp=(e:KeyboardEvent)=>keys.delete(e.code);
    const look=(dx:number,dy:number)=>{yaw-=dx*.0022;pitch=Math.max(-1.35,Math.min(1.35,pitch-dy*.0022));};
    const mouse=(e:MouseEvent)=>{if(walking && document.pointerLockElement===renderer.domElement)look(e.movementX,e.movementY);};
    let pointerX=0,pointerY=0,downX=0,downY=0,dragDistance=0;
    const down=(e:PointerEvent)=>{if(!loaded)return;if(document.pointerLockElement===renderer.domElement){interact();return;}dragging=true;dragDistance=0;downX=pointerX=e.clientX;downY=pointerY=e.clientY;renderer.domElement.setPointerCapture(e.pointerId);enter();};
    const drag=(e:PointerEvent)=>{if(!walking||!dragging)return;dragDistance+=Math.hypot(e.clientX-pointerX,e.clientY-pointerY);look(e.clientX-pointerX,e.clientY-pointerY);pointerX=e.clientX;pointerY=e.clientY;};
    const up=(e:PointerEvent)=>{
      if(dragging&&dragDistance<6&&e.type!=='pointercancel'){
        const rect=renderer.domElement.getBoundingClientRect();interact(new THREE.Vector2((downX-rect.left)/rect.width*2-1,1-(downY-rect.top)/rect.height*2));
      }
      dragging=false;
    };
    const hidden=()=>{if(document.hidden)pause();};
    document.addEventListener('pointerlockchange',onLock);document.addEventListener('pointerlockerror',onLockError);
    document.addEventListener('keydown',onKey);document.addEventListener('keyup',onUp);document.addEventListener('mousemove',mouse);
    document.addEventListener('visibilitychange',hidden);window.addEventListener('blur',pause);
    renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointermove',drag);renderer.domElement.addEventListener('pointerup',up);renderer.domElement.addEventListener('pointercancel',up);
    const toolLife=new AbortController();
    type Tool = { name:string;description:string;inputSchema:object;annotations:{readOnlyHint:boolean};execute:(input:unknown)=>unknown };
    const context=(document as Document & {modelContext?:{registerTool:(tool:Tool,options:{signal:AbortSignal})=>unknown}}).modelContext;
    const validateEmpty=(input:unknown)=>{if(!input || typeof input!=='object' || Array.isArray(input) || Object.keys(input).length)throw new Error('Expected an empty object.');};
    if(context?.registerTool) for(const tool of [
      {name:'read_walkthrough_position',description:'Read the current room position and whether walking is active.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:(input:unknown)=>{validateEmpty(input);return {...walker,walking};}},
      {name:'reset_walkthrough_position',description:'Return to the starting position, just like Reset position.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:false},execute:(input:unknown)=>{validateEmpty(input);reset();return {...walker,walking};}},
    ]) {try{void Promise.resolve(context.registerTool(tool,{signal:toolLife.signal})).catch(()=>{});}catch{/* optional browser capability */}}
    const assets=createHouseAssets(scene,{
      changed:()=>{needsRender=true;},ready:()=>{loaded=true;setReady(true);if(!document.hidden)enter(false);},progress:setProgress,error:message=>{pause();setError(message);},
    },view);
    assets.update(walker);
    let lastAction='',lastDoorCheck=-Infinity;
    const tick=(now:number)=>{
      if(disposed)return;const dt=Math.min((now-last)/1000,.15);last=now;
      if(walking&&pool.active){
        const climb=pool.step(dt);if(climb){walker=climb.walker;eye=walker.height+EYE_HEIGHT;needsRender=true;if(climb.done)keys.clear();}
      }else if(walking&&crawls.active){
        const crawl=crawls.step(dt);if(crawl){walker=crawl.walker;yaw+=crawl.yawDelta;eye=walker.height+crawl.eyeHeight;needsRender=true;if(crawl.done)keys.clear();}
      }else if(walking&&ladders.active){
        const climb=ladders.step(dt);if(climb){walker=climb.walker;yaw+=climb.yawDelta;eye=walker.height+EYE_HEIGHT;needsRender=true;if(climb.done)keys.clear();}
      }else if(walking){
        const turn=(Number(keys.has('ArrowLeft'))-Number(keys.has('ArrowRight')))*1.55*dt;yaw+=turn;
        let forward=Number(keys.has('KeyW')||keys.has('ArrowUp'))-Number(keys.has('KeyS')||keys.has('ArrowDown'));
        let right=Number(keys.has('KeyD'))-Number(keys.has('KeyA'));const length=Math.hypot(forward,right);
        if(length){const before=walker;forward/=length;right/=length;const speed=2.5*(keys.has('ShiftLeft')||keys.has('ShiftRight')?2:1)*dt;const moved=moveWalker(walker,(-Math.sin(yaw)*forward+Math.cos(yaw)*right)*speed,(Math.cos(yaw)*forward+Math.sin(yaw)*right)*speed);walker=moved;yaw+=moved.yawDelta;eye+=moved.heightDelta;
          if(!hintFinished){distanceWalked+=moved.crossed?speed:Math.hypot(walker.x-before.x,walker.y-before.y,walker.height-before.height);if(distanceWalked>=3){hintFinished=true;setShowHint(false);}}
        }
      }
      if(view.doors.update(walking?dt:0,walker)){assets.doorView.sync();needsRender=true;}
      assets.update(walker);
      const nextZone=zoneAt(walker);
      if(nextZone!==lastZone){lastZone=nextZone;setZone(nextZone);}
      if(!crawls.active)eye+=(walker.height+EYE_HEIGHT-eye)*(1-Math.exp(-16*dt));sync();
      if(now-lastDoorCheck>120){
        lastDoorCheck=now;
        const crawl=walking?crawls.target(walker,yaw):null;
        const ladder=walking&&!crawls.active&&!crawl?ladders.target(walker,yaw):null;
        const selected=walking&&!crawls.active&&!crawl&&!ladders.active&&!ladder?assets.doorView.target(camera):null;
        const poolChoice=walking?pool.target(walker,yaw):null;
        const action=pool.active?'Climbing…':poolChoice?poolChoice.label:crawls.active?'Crawling…':crawl?crawl.label:ladders.active?'Climbing…':ladder?(ladder.ready?ladder.label:'Loading ladder destination…'):selected?(selected.blocked?'Step back · ': '')+(selected.target===1?'Close':'Open')+' '+selected.def.label.toLowerCase():'';
        if(action!==lastAction){lastAction=action;setDoorAction(action);}
      }
      if(walking||needsRender){assets.render(renderer,camera);needsRender=false;}
      container.dataset.walker=JSON.stringify({...walker,room:view.activeRoom,space:view.activeSpace,portals:assets.portalStats,loadedRooms:assets.loadedRooms,crawling:crawls.active,eyeHeight:eye-walker.height,poolDrained:view.poolState.drained,poolClimbing:pool.active,climbing:ladders.active||pool.active,climbProgress:ladders.progress,movingDoors:view.doors.items.filter(d=>d.amount!==d.target).map(d=>d.key),yaw,pitch,walking,drawCalls:renderer.info.render.calls,triangles:renderer.info.render.triangles});
      frame=requestAnimationFrame(tick);
    };frame=requestAnimationFrame(tick);
    return ()=>{
      disposed=true;toolLife.abort();cancelAnimationFrame(frame);observer.disconnect();keys.clear();if(document.pointerLockElement===renderer.domElement)document.exitPointerLock();
      document.removeEventListener('pointerlockchange',onLock);document.removeEventListener('pointerlockerror',onLockError);document.removeEventListener('keydown',onKey);document.removeEventListener('keyup',onUp);document.removeEventListener('mousemove',mouse);document.removeEventListener('visibilitychange',hidden);window.removeEventListener('blur',pause);
      renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointermove',drag);renderer.domElement.removeEventListener('pointerup',up);renderer.domElement.removeEventListener('pointercancel',up);
      assets.dispose();renderer.dispose();renderer.domElement.remove();runtime.current=null;
    };
  },[]);
  return <main className="walkthrough">
    <div ref={host} className="viewport" tabIndex={-1} aria-label={`First-person view of ${zone}`} />
    <header className="hud"><div className="identity"><p className="eyebrow">MANIAC MANSION</p><h1>{zone}</h1></div><div className="hud-actions">
      {ready && !error && <Button className="hud-button" onClick={()=>active?runtime.current?.pause():runtime.current?.enter()}>{active?'Pause':'Resume'}</Button>}
      <Button className="hud-button" disabled={!ready} onClick={()=>runtime.current?.reset()}>Reset position</Button>
    </div></header>
    {(error || !ready || (active && showHint)) && <section className={`entry${ready&&!error?' hint':''}${touch?' touch-hint':''}`} aria-label="Walkthrough controls">
      <h2>{error?'Unable to enter':ready?'Explore the house':'Opening the house…'}</h2>
      {error?<p className="error" role="alert">{error}</p>:<>
        <p>{touch?'Drag to look around. Use the arrows to walk. Tap a nearby door to open it, or a ladder to climb.':'Walk with WASD. Click or drag to look. Aim at a nearby door or ladder and press E to use it.'}</p>
        <div className="key-row"><kbd>W A S D</kbd><span>walk</span><kbd>Shift</kbd><span>faster</span><kbd>Mouse</kbd><span>look</span><kbd>Esc</kbd><span>pause</span></div>
        {!ready && <><div className="progress-line" role="progressbar" aria-label="Loading room" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}><span style={{width:`${progress}%`}} /></div><p className="small" aria-live="polite">Loading room · {progress}%</p></>}
        <p className="small">{preview?'Independent room preview. Doors stay closed for now.':'The front steps lead into the hall. Walk through to the living room or take the grand staircase upstairs.'}</p>
      </>}
    </section>}
    {active && <div className="reticle" aria-hidden="true" />}
    {active && doorAction && <Button className="door-action" aria-label={doorAction} aria-keyshortcuts={!touch?'E':undefined} onClick={()=>runtime.current?.interact()}>{!touch && <kbd>E</kbd>}{doorAction}</Button>}
    {active && touch && <div className="touch-pad" aria-label="Movement controls">{[['KeyW','↑','Forward'],['KeyA','←','Left'],['KeyS','↓','Backward'],['KeyD','→','Right']].map(([code,label,title])=><Button key={code} aria-label={title} onPointerDown={e=>{e.currentTarget.setPointerCapture(e.pointerId);runtime.current?.key(code,true);}} onPointerUp={()=>runtime.current?.key(code,false)} onPointerCancel={()=>runtime.current?.key(code,false)}>{label}</Button>)}</div>}
    <footer className="footer"><span className="status" aria-live="polite">{error?'ROOM UNAVAILABLE':!ready?'LOADING':active?'EXPLORING':'PAUSED'}</span><span className="desktop-help">{fallback?'Click or drag to look · Shift to walk faster · Arrow keys also work · R to reset':'WASD to walk · Shift to walk faster · Mouse to look · R to reset'}</span></footer>
  </main>;
}
