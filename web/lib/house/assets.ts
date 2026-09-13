import {instantiateSharedAssets} from './shared-assets';
import {createDoorView} from './door-view';
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { publicAssetUrl } from '../public-asset';
import { createHouseRuntime } from './runtime';
import { nearbyRooms } from './visibility';
import type { Walker } from './types';
function dispose(root:THREE.Object3D) {
 const geometries=new Set<THREE.BufferGeometry>(),materials=new Set<THREE.Material>(),textures=new Set<THREE.Texture>();
 root.traverse(o=>{if(o instanceof THREE.InstancedMesh)o.dispose();if(o instanceof THREE.Mesh&&!o.userData.sharedDoorResource){geometries.add(o.geometry);for(const m of Array.isArray(o.material)?o.material:[o.material]){materials.add(m);for(const value of Object.values(m))if(value instanceof THREE.Texture)textures.add(value);}}});
 textures.forEach(t=>t.dispose());materials.forEach(m=>m.dispose());geometries.forEach(g=>g.dispose());root.removeFromParent();
}
/** Independent GLBs assembled in house coordinates; distant assets are released. */
export function createHouseAssets(scene:THREE.Scene,callbacks:{changed:()=>void;ready:()=>void;progress:(n:number)=>void;error:(message:string)=>void},view=createHouseRuntime()) {
 const {house,rooms,definitions}=view;
 const doorView=createDoorView(scene,view.doors);
 view.requireLoadedRooms();
 const loaded=new Map<string,THREE.Object3D>(),pending=new Set<string>(),failed=new Set<string>();
 const libraries=new Map<string,Promise<THREE.Group>>();
 let wanted=new Set<string>(),disposed=false;const loader=new GLTFLoader();
 function library(url:string){
  let pending=libraries.get(url);
  if(!pending){pending=loader.loadAsync(publicAssetUrl(url)).then(gltf=>gltf.scene);libraries.set(url,pending);}
  return pending;
 }
 return {
  doorView,
  update(p:Walker){
   if(disposed)return;
   wanted=nearbyRooms(p,rooms,definitions,new Set(loaded.keys()),house.loadRadius,house.unloadRadius);
   for(const [id,root] of loaded)if(!wanted.has(id)){doorView.detach(id);dispose(root);loaded.delete(id);view.setRoomLoaded(id,false);callbacks.changed();}
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
     group.add(gltf.scene);scene.add(group);doorView.attach(id,group);loaded.set(id,group);view.setRoomLoaded(id,true);callbacks.changed();
     if(id===house.start){callbacks.progress(100);callbacks.ready();}
    },e=>{if(!disposed&&id===house.start&&e.total)callbacks.progress(Math.round(100*e.loaded/e.total));},()=>{
     pending.delete(id);failed.add(id);if(!disposed)callbacks.error(`${def.label} could not load. Reload the page to try again.`);
    });
   }
  },
  dispose(){disposed=true;loaded.forEach(dispose);loaded.clear();libraries.forEach(p=>{void p.then(root=>dispose(root)).catch(()=>{});});libraries.clear();},
 };
}
