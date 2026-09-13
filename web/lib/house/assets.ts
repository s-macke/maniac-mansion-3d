import {instantiateSharedAssets} from './shared-assets';
import {createDoorView} from './door-view';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { publicAssetUrl } from '../public-asset';
import { createHouseRuntime } from './runtime';
import {createPortalRenderer,portalMatrix} from './portal-renderer';
import type { Walker } from './types';
import {neighboringRooms} from './visibility';
function dispose(root:THREE.Object3D) {
 const geometries=new Set<THREE.BufferGeometry>(),materials=new Set<THREE.Material>(),textures=new Set<THREE.Texture>();
 root.traverse(o=>{if(o instanceof THREE.InstancedMesh)o.dispose();if(o instanceof THREE.Mesh&&!o.userData.sharedDoorResource){geometries.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:[o.material]){materials.add(m);for(const value of Object.values(m))if(value instanceof THREE.Texture)textures.add(value);}}});
 textures.forEach(t=>t.dispose());materials.forEach(m=>m.dispose());geometries.forEach(g=>g.dispose());root.removeFromParent();
}
/** Independent room spaces; only graph neighbors and portal sightlines request GLBs. */
export function createHouseAssets(scene:THREE.Scene,callbacks:{changed:()=>void;ready:()=>void;progress:(n:number)=>void;error:(message:string)=>void},view=createHouseRuntime()) {
 const {house,rooms,definitions}=view;
 const doorView=createDoorView(scene,view.doors,d=>view.doorPlacement(d.room,d.def.port));
 view.requireLoadedRooms();
 const loaded=new Map<string,THREE.Object3D>(),pending=new Set<string>(),failed=new Set<string>();
 const libraries=new Map<string,Promise<THREE.Group>>();
 const lastWanted=new Map<string,number>(),proxies=new Map<string,{root:THREE.Group;leaves:{source:THREE.Object3D;copy:THREE.Object3D}[]}>();
 let visible=new Set<string>();
 let wanted=new Set<string>(),disposed=false;const loader=new GLTFLoader();
 function library(url:string){
  let pending=libraries.get(url);
  if(!pending){pending=loader.loadAsync(publicAssetUrl(url)).then(gltf=>gltf.scene);libraries.set(url,pending);}
  return pending;
 }
 function selectSpace(space:string){
  for(const [id,root] of loaded)root.visible=view.graph.spaceOf(id)===space;
  for(const edge of view.graph.portals.filter(p=>!p.continuous)){
   const door=view.portalDoor(edge),owner=door&&loaded.get(door.room.id);
   if(!door||!owner||view.graph.spaceOf(door.room.id)!==edge.to.space)continue;
   let proxy=proxies.get(edge.key);
   if(!proxy){
    const root=new THREE.Group(),leaves=door.def.leaves.map(leaf=>{
     const source=owner.getObjectByName(leaf.node)!,copy=source.clone(true);copy.matrixAutoUpdate=false;root.add(copy);return {source,copy};
    });scene.add(root);proxy={root,leaves};proxies.set(edge.key,proxy);
   }
   proxy.root.visible=edge.from.space===space;owner.updateMatrixWorld(true);
   const reverse=view.graph.portals.find(p=>p.key===edge.reverse)!,matrix=portalMatrix(reverse);
   for(const leaf of proxy.leaves){leaf.source.updateMatrix();leaf.source.updateWorldMatrix(true,false);leaf.copy.matrix.copy(matrix).multiply(leaf.source.matrixWorld);}
   proxy.root.updateMatrixWorld(true);
  }
 }
 let portalRenderer:ReturnType<typeof createPortalRenderer>|undefined;
 return {
  doorView,
  render(renderer:THREE.WebGLRenderer,camera:THREE.PerspectiveCamera){
   portalRenderer??=createPortalRenderer(renderer,scene,view,selectSpace);
   visible=portalRenderer.render(camera);
  },
  get portalStats(){return portalRenderer?.stats??{passes:0,targets:0,visibleRooms:[]};},
  selectSpace,
  get loadedRooms(){return [...loaded.keys()];},
  update(p:Walker,now=performance.now()){
   if(disposed)return;
   wanted=neighboringRooms(view.graph,view.activeSpace);
   for(const id of visible)wanted.add(id);
   for(const id of wanted)lastWanted.set(id,now);
   for(const [id,time] of lastWanted)if(now-time<10000)wanted.add(id);else lastWanted.delete(id);
   for(const [id,root] of loaded)if(!wanted.has(id)){doorView.detach(id);
    for(const [key,proxy] of proxies)if(proxy.leaves.some(l=>root.getObjectById(l.source.id))){proxy.root.removeFromParent();proxies.delete(key);}
    dispose(root);loaded.delete(id);view.setRoomLoaded(id,false);callbacks.changed();}
   for(const id of wanted){
    if(loaded.has(id)||pending.has(id)||failed.has(id))continue;
    const room=rooms.find(r=>r.id===id)!,def=definitions[room.definition];pending.add(id);
    const kit=def.sharedAssetLibrary?library(def.sharedAssetLibrary):undefined;
    // Attach a rejection handler immediately, including when the room itself fails first.
    kit?.catch(()=>{});
    loader.load(publicAssetUrl(def.asset),async gltf=>{
     try{
      const shared=kit?await kit:undefined;
      if(!disposed&&wanted.has(id)&&shared)instantiateSharedAssets(gltf.scene,def,shared);
     }catch{
      pending.delete(id);failed.add(id);dispose(gltf.scene);
      if(!disposed)callbacks.error('Door assets could not load. Reload the page to try again.');return;
     }
     pending.delete(id);
     if(disposed||!wanted.has(id)){dispose(gltf.scene);return;}
     // glTF already maps Blender Z-up to Three Y-up. House yaw uses the same handedness.
     const group=new THREE.Group();group.position.set(room.position[0],room.position[2],-room.position[1]);group.rotation.y=room.yaw;
     group.add(gltf.scene);scene.add(group);doorView.attach(id,group);loaded.set(id,group);view.setRoomLoaded(id,true);selectSpace(view.activeSpace);callbacks.changed();
     if(id===house.start){callbacks.progress(100);callbacks.ready();}
    },e=>{if(!disposed&&id===house.start&&e.total)callbacks.progress(Math.round(100*e.loaded/e.total));},()=>{
     pending.delete(id);failed.add(id);if(!disposed)callbacks.error(`${def.label} could not load. Reload the page to try again.`);
    });
   }
   selectSpace(view.activeSpace);
  },
  dispose(){disposed=true;portalRenderer?.dispose();proxies.forEach(p=>p.root.removeFromParent());proxies.clear();loaded.forEach(dispose);loaded.clear();libraries.forEach(p=>{void p.then(root=>dispose(root)).catch(()=>{});});libraries.clear();},
 };
}
