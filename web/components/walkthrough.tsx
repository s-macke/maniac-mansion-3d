'use client';
import { useCallback, useEffect, useRef, useState } from 'react';
import { Button } from '@/components/ui/button';
import { EYE_HEIGHT } from '@/lib/house/navigation';
import { createHouseRuntime } from '@/lib/house/runtime';
import { createHouseAssets } from '@/lib/house/assets';
import {createPool} from '@/lib/house/pool';
import {createCrawls} from '@/lib/house/crawls';
import {createLadders} from '@/lib/house/ladders';
import * as THREE from 'three';
import {OriginalArtworkView} from '@/components/original-artwork';
import {originalArtwork,type OriginalArtwork} from '@/lib/original-artwork';
import {createFloatingStick} from '@/lib/floating-stick';

type Runtime = { referenceModal:(open:boolean)=>void; interact:()=>void; pause:()=>void };
export default function Walkthrough() {
  const host=useRef<HTMLDivElement>(null),runtime=useRef<Runtime|null>(null);
  const [ready,setReady]=useState(false),[progress,setProgress]=useState(0),[active,setActive]=useState(false);
  const [doorAction,setDoorAction]=useState('');
  const [showHint,setShowHint]=useState(true);
  const [artwork,setArtwork]=useState<OriginalArtwork|null>(null);
  const referenceModal=useCallback((open:boolean)=>runtime.current?.referenceModal(open),[]);
  const [zone,setZone]=useState('Entrance hall');
  const [preview,setPreview]=useState(false);
  const [error,setError]=useState(''),[fallback,setFallback]=useState(true),[touch,setTouch]=useState(false);
  useEffect(()=>{
    const view=createHouseRuntime(new URLSearchParams(window.location.search).get('room'));
    const ladders=createLadders(view),crawls=createCrawls(view),pool=createPool(view);
    const {START,START_YAW,START_PITCH,moveWalker,zoneAt}=view;
    setPreview(view.preview);setZone(zoneAt(START));
    const container=host.current!;let disposed=false,frame=0,walking=false,dragging=false,needsRender=true;let lastZone=zoneAt(START);
    let referenceOpen=false,resumeAfterReference=false;
    let lastArtwork='';
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
    let touchControls:ReturnType<typeof createFloatingStick>|undefined;
    const clearInput=()=>{keys.clear();touchControls?.clear();};
    const sync=()=>{camera.position.set(walker.x,eye,-walker.y);camera.rotation.set(pitch,yaw,0);};sync();
    const resize=()=>{touchControls?.clear();const {width,height}=container.getBoundingClientRect();renderer.setSize(width,height);camera.aspect=width/height;camera.updateProjectionMatrix();needsRender=true;};resize();
    const observer=new ResizeObserver(resize);observer.observe(container);
    const pause=()=>{walking=false;clearInput();dragging=false;setActive(false);if(document.pointerLockElement===renderer.domElement)document.exitPointerLock();};
    const reset=()=>{ladders.cancel();crawls.cancel();pool.cancel();view.resetSpace();walker={...START};yaw=START_YAW;pitch=START_PITCH;eye=START.height+EYE_HEIGHT;clearInput();sync();needsRender=true;};
    const enableFallback=()=>{if(!disposed){setFallback(true);walking=true;setActive(true);container.focus();}};
    const enter=(capture=true)=>{
      if(!loaded||disposed||referenceOpen)return;
      walking=true;setActive(true);container.focus();
      if(!capture || coarse || !renderer.domElement.requestPointerLock){enableFallback();return;}
      try { const p=renderer.domElement.requestPointerLock();if(p)p.catch(enableFallback); }catch{enableFallback();}
    };
    const interact=(point?:THREE.Vector2)=>{if(!walking||ladders.active||crawls.active||pool.active)return;const poolChoice=pool.target(walker,yaw);if(poolChoice){if(pool.begin(poolChoice,walker,yaw))clearInput();needsRender=true;return;}const crawl=crawls.target(walker,yaw);if(crawl){const hit=point?assets.doorView.target(camera,point):null;if(hit){view.doors.toggle(hit.key);}else if(crawls.begin(crawl,walker,yaw))clearInput();needsRender=true;return;}const ladder=ladders.target(walker,yaw);if(ladder){if(ladders.begin(ladder,walker,yaw)){clearInput();needsRender=true;}return;}const door=assets.doorView.target(camera,point);if(door){view.doors.toggle(door.key);needsRender=true;}};
    runtime.current={interact:()=>interact(),pause,referenceModal:open=>{
      if(open===referenceOpen)return;
      if(open){resumeAfterReference=walking;pause();referenceOpen=true;}
      else {referenceOpen=false;if(resumeAfterReference&&!document.hidden)enter(false);}
    }};
    const onLock=()=>{const locked=document.pointerLockElement===renderer.domElement;
      if(hadLock&&!locked)pause();if(locked)dragging=false;hadLock=locked;setFallback(!locked);
    };
    const onLockError=()=>enableFallback();
    const onKey=(e:KeyboardEvent)=>{
      if(referenceOpen||(e.target instanceof HTMLElement&&e.target.closest('select')))return;
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
    if(coarse){
      touchControls=createFloatingStick(renderer.domElement,container,{
        enabled:()=>loaded&&!disposed&&!referenceOpen,begin:()=>enter(false),look,
        tap:(x,y)=>{const rect=renderer.domElement.getBoundingClientRect();interact(new THREE.Vector2((x-rect.left)/rect.width*2-1,1-(y-rect.top)/rect.height*2));},
      });
    }else{
      renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointermove',drag);renderer.domElement.addEventListener('pointerup',up);renderer.domElement.addEventListener('pointercancel',up);
    }
    const toolLife=new AbortController();
    type Tool = { name:string;description:string;inputSchema:object;annotations:{readOnlyHint:boolean};execute:(input:unknown)=>unknown };
    const context=(document as Document & {modelContext?:{registerTool:(tool:Tool,options:{signal:AbortSignal})=>unknown}}).modelContext;
    const validateEmpty=(input:unknown)=>{if(!input || typeof input!=='object' || Array.isArray(input) || Object.keys(input).length)throw new Error('Expected an empty object.');};
    if(context?.registerTool) for(const tool of [
      {name:'read_walkthrough_position',description:'Read the current room position and whether walking is active.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true},execute:(input:unknown)=>{validateEmpty(input);return {...walker,walking};}},
      {name:'reset_walkthrough_position',description:'Return to the starting position, just like pressing R.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:false},execute:(input:unknown)=>{validateEmpty(input);reset();return {...walker,walking};}},
    ]) {try{void Promise.resolve(context.registerTool(tool,{signal:toolLife.signal})).catch(()=>{});}catch{/* optional browser capability */}}
    const assets=createHouseAssets(scene,{
      changed:()=>{needsRender=true;},ready:()=>{loaded=true;setReady(true);if(!document.hidden)enter(false);},progress:setProgress,error:message=>{pause();setError(message);},
    },view);
    assets.update(walker);
    let lastAction='',lastDoorCheck=-Infinity;
    const tick=(now:number)=>{
      if(disposed)return;const dt=Math.min((now-last)/1000,.15);last=now;
      if(walking&&pool.active){
        const climb=pool.step(dt);if(climb){walker=climb.walker;eye=walker.height+EYE_HEIGHT;needsRender=true;if(climb.done)clearInput();}
      }else if(walking&&crawls.active){
        const crawl=crawls.step(dt);if(crawl){walker=crawl.walker;yaw+=crawl.yawDelta;eye=walker.height+crawl.eyeHeight;needsRender=true;if(crawl.done)clearInput();}
      }else if(walking&&ladders.active){
        const climb=ladders.step(dt);if(climb){walker=climb.walker;yaw+=climb.yawDelta;eye=walker.height+EYE_HEIGHT;needsRender=true;if(climb.done)clearInput();}
      }else if(walking){
        const turn=(Number(keys.has('ArrowLeft'))-Number(keys.has('ArrowRight')))*1.55*dt;yaw+=turn;
        let forward=Number(keys.has('KeyW')||keys.has('ArrowUp'))-Number(keys.has('KeyS')||keys.has('ArrowDown'));
        let right=Number(keys.has('KeyD'))-Number(keys.has('KeyA'));
        forward+=touchControls?.movement.forward??0;right+=touchControls?.movement.right??0;
        const length=Math.hypot(forward,right);
        if(length){const before=walker;const scale=Math.max(1,length);forward/=scale;right/=scale;const speed=2.5*(keys.has('ShiftLeft')||keys.has('ShiftRight')?2:1)*dt;const moved=moveWalker(walker,(-Math.sin(yaw)*forward+Math.cos(yaw)*right)*speed,(Math.cos(yaw)*forward+Math.sin(yaw)*right)*speed);walker=moved;yaw+=moved.yawDelta;eye+=moved.heightDelta;
          if(!hintFinished){distanceWalked+=moved.crossed?speed:Math.hypot(walker.x-before.x,walker.y-before.y,walker.height-before.height);if(distanceWalked>=3){hintFinished=true;setShowHint(false);}}
        }
      }
      if(view.doors.update(walking?dt:0,walker)){assets.doorView.sync();needsRender=true;}
      assets.update(walker);
      const nextZone=zoneAt(walker);
      const currentRoom=view.rooms.find(room=>room.id===view.activeRoom)!;
      const nextArtwork=originalArtwork(view.definitions[currentRoom.definition],nextZone,view.poolState.drained);
      const artworkKey=`${nextArtwork.room}:${nextArtwork.selected}:${nextArtwork.label}`;
      if(artworkKey!==lastArtwork){lastArtwork=artworkKey;setArtwork(nextArtwork);}
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
      disposed=true;toolLife.abort();cancelAnimationFrame(frame);observer.disconnect();clearInput();if(document.pointerLockElement===renderer.domElement)document.exitPointerLock();
      document.removeEventListener('pointerlockchange',onLock);document.removeEventListener('pointerlockerror',onLockError);document.removeEventListener('keydown',onKey);document.removeEventListener('keyup',onUp);document.removeEventListener('mousemove',mouse);document.removeEventListener('visibilitychange',hidden);window.removeEventListener('blur',pause);
      renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointermove',drag);renderer.domElement.removeEventListener('pointerup',up);renderer.domElement.removeEventListener('pointercancel',up);
      touchControls?.dispose();assets.dispose();renderer.dispose();renderer.domElement.remove();runtime.current=null;
    };
  },[]);
  return <main className="walkthrough">
    <div ref={host} className="viewport" tabIndex={-1} aria-label={`First-person view of ${zone}`} />
    <header className="hud"><div className="identity"><p className="eyebrow">MANIAC MANSION</p><h1>{zone}</h1></div><div className="view-links"><OriginalArtworkView artwork={artwork} mobile={touch} onModalChange={referenceModal} /><a className="github-link" href="https://github.com/s-macke/maniac-mansion-3d" target="_blank" rel="noopener noreferrer" aria-label="View source on GitHub (opens in a new tab)" onClick={()=>runtime.current?.pause()}>
      <svg viewBox="0 0 16 16" width="20" height="20" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82A7.65 7.65 0 0 1 8 3.86c.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z" /></svg>
      <span>GitHub</span>
    </a></div></header>
    {(error || !ready || (active && showHint && !touch)) && <section className={`entry${ready&&!error?' hint':''}`} aria-label="Walkthrough controls">
      <h2>{error?'Unable to enter':ready?'Explore the house':'Opening the house…'}</h2>
      {error?<p className="error" role="alert">{error}</p>:<>
        {!touch && <p>Walk with WASD. Click or drag to look. Aim at a nearby door or ladder and press E to use it.</p>}
        {!touch && <div className="key-row"><kbd>W A S D</kbd><span>walk</span><kbd>Shift</kbd><span>faster</span><kbd>Mouse</kbd><span>look</span><kbd>Esc</kbd><span>pause</span></div>}
        {!ready && <><div className="progress-line" role="progressbar" aria-label="Loading room" aria-valuenow={progress} aria-valuemin={0} aria-valuemax={100}><span style={{width:`${progress}%`}} /></div><p className="small" aria-live="polite">Loading room · {progress}%</p></>}
        {!touch && <p className="small">{preview?'Independent room preview. Doors stay closed for now.':'The front steps lead into the hall. Walk through to the living room or take the grand staircase upstairs.'}</p>}
      </>}
    </section>}
    {active && <div className="reticle" aria-hidden="true" />}
    {active && doorAction && <Button className="door-action" aria-label={doorAction} aria-keyshortcuts={!touch?'E':undefined} onClick={()=>runtime.current?.interact()}>{!touch && <kbd>E</kbd>}{doorAction}</Button>}
    <footer className="footer"><span className="status" aria-live="polite">{error?'ROOM UNAVAILABLE':!ready?'LOADING':active?'EXPLORING':'PAUSED'}</span><span className="desktop-help">{fallback?'Click or drag to look · Shift to walk faster · Arrow keys also work · R to reset':'WASD to walk · Shift to walk faster · Mouse to look · R to reset'}</span></footer>
  </main>;
}
