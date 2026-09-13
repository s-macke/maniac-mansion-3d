import * as THREE from 'three';
import {leafAngle,type Doors} from './doors';
import {toWorld} from './placement';

/** Door state belongs to the house, so unloading a GLB never resets it. */
export function createDoorView(scene:THREE.Scene,doors:Doors){
 const nodes=new Map<string,THREE.Object3D[]>(),ray=new THREE.Raycaster();ray.near=.01;
 function attach(roomId:string,root:THREE.Object3D){
  for(const door of doors.items.filter(d=>d.room.id===roomId)){
   const leaves=door.def.leaves.map(leaf=>{
    const node=root.getObjectByName(leaf.node);
    if(!node)throw new Error('Missing door mesh: '+leaf.node);
    node.traverse(o=>{o.userData.doorKey=door.key;});return node;
   });nodes.set(door.key,leaves);
  }
  sync();
 }
 function detach(roomId:string){for(const door of doors.items.filter(d=>d.room.id===roomId))nodes.delete(door.key);}
 function sync(){for(const door of doors.items)nodes.get(door.key)?.forEach((node,i)=>{node.rotation.y=leafAngle(door.def.leaves[i],door.amount);});}
 function target(camera:THREE.Camera,point=new THREE.Vector2()){
  camera.updateMatrixWorld(true);
  if(!doors.items.some(d=>{
   if(!nodes.has(d.key))return false;
   const p=toWorld({x:d.port.position[0],y:d.port.position[1],height:d.port.position[2]+1.45},d.room);
   return camera.position.distanceTo(new THREE.Vector3(p.x,p.height,-p.y))<4;
  }))return null;
  scene.updateMatrixWorld(true);ray.far=2.8;ray.setFromCamera(point,camera);
  const hit=ray.intersectObjects(scene.children,true)[0];
  if(hit?.object.userData.doorKey&&nodes.has(hit.object.userData.doorKey))return doors.items.find(d=>d.key===hit.object.userData.doorKey)??null;
  // Also aim through the opening: a fully open leaf is edge-on from the doorway.
  const origin=ray.ray.origin.clone(),direction=ray.ray.direction.clone();
  const candidates=doors.items.filter(d=>nodes.has(d.key)).map(door=>{
   const mid=door.port.position;
   const p=toWorld({x:mid[0],y:mid[1],height:mid[2]+1.45},door.room);
   const center=new THREE.Vector3(p.x,p.height,-p.y),delta=center.clone().sub(origin),distance=delta.length();
   return {door,center,distance,dot:delta.normalize().dot(direction)};
  }).filter(c=>c.distance<2.8&&c.dot>.82).sort((a,b)=>b.dot-a.dot);
  for(const c of candidates){
   ray.set(origin,c.center.clone().sub(origin).normalize());ray.far=c.distance;
   const obstruction=ray.intersectObjects(scene.children,true)[0];
   if(!obstruction||obstruction.object.userData.doorKey===c.door.key||obstruction.distance>c.distance-.15)return c.door;
  }
  return null;
 }
 return {attach,detach,sync,target};
}
