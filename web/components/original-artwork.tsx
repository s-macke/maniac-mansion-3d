import {useEffect,useRef,useState} from 'react';
import type {OriginalArtwork} from '@/lib/original-artwork';
import {publicAssetUrl} from '@/lib/public-asset';

export function OriginalArtworkView({artwork,mobile,onModalChange}:{artwork:OriginalArtwork|null;mobile:boolean;onModalChange:(open:boolean)=>void}){
 const [open,setOpen]=useState(false),[large,setLarge]=useState(false);
 const [choice,setChoice]=useState<{key:string;id:string}|null>(null);
 const dialog=useRef<HTMLDialogElement>(null);
 const modal=open&&(mobile||large),key=artwork?`${artwork.room}:${artwork.selected}`:'';
 const selected=choice?.key===key?choice.id:artwork?.selected;
 const close=()=>{setOpen(false);setLarge(false);};
 useEffect(()=>{
  if(modal){onModalChange(true);dialog.current?.showModal();}
  else {dialog.current?.close();onModalChange(false);}
 },[modal,onModalChange]);
 const picture=()=>artwork&&selected?<img key={selected} src={publicAssetUrl(`/originals/${selected}.png`)} alt={`Original EGA artwork — ${artwork.label} (${selected})`} />:null;
 const selector=()=>artwork&&artwork.backgrounds.length>1?<label className="original-selector">Background <select aria-label="Original background" value={selected} onChange={e=>setChoice({key,id:e.target.value})}>{artwork.backgrounds.map(id=><option key={id} value={id}>{id}</option>)}</select></label>:null;
 return <>
  <button type="button" className="original-toggle" disabled={!artwork} aria-expanded={open} onClick={()=>open?close():setOpen(true)}>Original</button>
  {open&&!modal&&<aside className="original-preview" aria-label="Original artwork">
   <div className="original-heading"><span>{artwork?.label}</span><button type="button" aria-label="Close original" onClick={close}>×</button></div>
   <button type="button" className="original-enlarge" aria-label="Enlarge original artwork" onClick={()=>setLarge(true)}>{picture()}</button>
   {selector()}
  </aside>}
  <dialog ref={dialog} className="original-dialog" aria-label="Original artwork" onCancel={event=>{event.preventDefault();close();}} onClick={event=>{if(event.target===event.currentTarget)close();}}>
   {modal&&<div className="original-content"><div className="original-heading"><h2>{artwork?.label} · Original</h2><button type="button" aria-label="Close original" onClick={close}>×</button></div>{picture()}{selector()}</div>}
  </dialog>
 </>;
}
