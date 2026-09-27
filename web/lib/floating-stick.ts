/** Two independent touch gestures: a floating movement stick and swipe-to-look. */
export function createFloatingStick(canvas:HTMLCanvasElement,host:HTMLElement,callbacks:{
  enabled:()=>boolean;begin:()=>void;look:(dx:number,dy:number)=>void;tap:(x:number,y:number)=>void;
}) {
  const radius=48,deadZone=6;
  const movement={forward:0,right:0};
  let stick:{id:number;x:number;y:number}|null=null;
  let swipe:{id:number;x:number;y:number;startX:number;startY:number;distance:number}|null=null;
  const visual=document.createElement('div');visual.className='floating-stick';visual.hidden=true;visual.setAttribute('aria-hidden','true');
  const thumb=document.createElement('div');thumb.className='floating-stick-thumb';visual.appendChild(thumb);host.appendChild(visual);
  const release=(id:number)=>{if(canvas.hasPointerCapture(id))canvas.releasePointerCapture(id);};
  const clear=()=>{
    const ids=[stick?.id,swipe?.id];stick=null;swipe=null;movement.forward=movement.right=0;visual.hidden=true;
    for(const id of ids)if(id!==undefined)release(id);
  };
  const down=(event:PointerEvent)=>{
    if(!callbacks.enabled())return;
    const rect=canvas.getBoundingClientRect();
    if(event.clientX<rect.left+rect.width/2){
      if(stick)return;
      stick={id:event.pointerId,x:event.clientX,y:event.clientY};
      visual.style.left=`${event.clientX-rect.left}px`;visual.style.top=`${event.clientY-rect.top}px`;
      thumb.style.transform='translate(0px, 0px)';visual.hidden=false;
    }else{
      if(swipe)return;
      swipe={id:event.pointerId,x:event.clientX,y:event.clientY,startX:event.clientX,startY:event.clientY,distance:0};
    }
    event.preventDefault();canvas.setPointerCapture(event.pointerId);callbacks.begin();
  };
  const move=(event:PointerEvent)=>{
    if(stick?.id===event.pointerId){
      event.preventDefault();const dx=event.clientX-stick.x,dy=event.clientY-stick.y,length=Math.hypot(dx,dy);
      const scale=length?Math.min(radius,length)/length:0;
      thumb.style.transform=`translate(${dx*scale}px, ${dy*scale}px)`;
      const speed=Math.max(0,Math.min(1,(length-deadZone)/(radius-deadZone)));
      movement.right=length?dx/length*speed:0;movement.forward=length?-dy/length*speed:0;
    }else if(swipe?.id===event.pointerId){
      event.preventDefault();const dx=event.clientX-swipe.x,dy=event.clientY-swipe.y;
      swipe.distance+=Math.hypot(dx,dy);swipe.x=event.clientX;swipe.y=event.clientY;callbacks.look(dx,dy);
    }
  };
  const up=(event:PointerEvent)=>{
    if(stick?.id===event.pointerId){stick=null;movement.forward=movement.right=0;visual.hidden=true;release(event.pointerId);}
    else if(swipe?.id===event.pointerId){
      const ended=swipe;swipe=null;release(event.pointerId);
      if(event.type==='pointerup'&&ended.distance<6)callbacks.tap(ended.startX,ended.startY);
    }
  };
  canvas.addEventListener('pointerdown',down);canvas.addEventListener('pointermove',move);
  canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);canvas.addEventListener('lostpointercapture',up);
  return {movement,clear,dispose(){
    clear();canvas.removeEventListener('pointerdown',down);canvas.removeEventListener('pointermove',move);
    canvas.removeEventListener('pointerup',up);canvas.removeEventListener('pointercancel',up);canvas.removeEventListener('lostpointercapture',up);visual.remove();
  }};
}
