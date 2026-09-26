import * as THREE from 'three';
import {type Portal} from './portals';
import type {HouseRuntime} from './runtime';

const point=(p:{x:number;y:number;height:number})=>new THREE.Vector3(p.x,p.height,-p.y);
export function portalMatrix(edge:Portal){
 const a=point(edge.from.point),b=point(edge.to.point);
 return new THREE.Matrix4().makeTranslation(b.x,b.y,b.z).multiply(new THREE.Matrix4().makeRotationY(edge.yaw)).multiply(new THREE.Matrix4().makeTranslation(-a.x,-a.y,-a.z));
}
export function portalCamera(camera:THREE.PerspectiveCamera,edge:Portal){
 camera.updateMatrixWorld();const clone=camera.clone();
 clone.matrixAutoUpdate=true;clone.matrixWorld.copy(portalMatrix(edge).multiply(camera.matrixWorld));
 clone.matrixWorld.decompose(clone.position,clone.quaternion,clone.scale);clone.updateMatrixWorld(true);return clone;
}
/** Destination geometry stays on the interior side of its entrance plane. */
export function entrancePlane(edge:Portal){
 const p=point(edge.to.point),n=new THREE.Vector3(-edge.to.normal.x,-edge.to.normal.height,edge.to.normal.y);
 return new THREE.Plane().setFromNormalAndCoplanarPoint(n,p.addScaledVector(n,-.002));
}
export function portalCorners(edge:Portal){
 if(edge.from.port.kind==='hatch'){
  const {port,room}=edge.from,base=point(edge.from.point);
  return [[-1,-1],[1,-1],[1,1],[-1,1]].map(([x,y])=>base.clone().add(new THREE.Vector3(x*port.width/2,0,-y*port.depth!/2).applyAxisAngle(new THREE.Vector3(0,1,0),room.yaw)));
 }
 const {point:p,normal:n,port}=edge.from,t=new THREE.Vector3(-n.y,0,-n.x),base=point(p);
 return [[-1,0],[1,0],[1,1],[-1,1]].map(([x,y])=>base.clone().addScaledVector(t,x*port.width/2).add(new THREE.Vector3(0,y*(port.height??2.7),0)));
}
/** A conservative screen footprint; near-plane intersections retain the portal. */
export function portalRect(camera:THREE.PerspectiveCamera,edge:Portal):THREE.Vector4|null{
 const p=point(edge.from.point),n=new THREE.Vector3(edge.from.normal.x,edge.from.normal.height,-edge.from.normal.y);
 if(camera.position.clone().sub(p).dot(n)>.06)return null;
 camera.updateMatrixWorld(true);
 const corners=portalCorners(edge),frustum=new THREE.Frustum().setFromProjectionMatrix(new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix,camera.matrixWorldInverse));
 if(!frustum.intersectsBox(new THREE.Box3().setFromPoints(corners).expandByScalar(.02)))return null;
 const projected=corners.map(v=>v.applyMatrix4(camera.matrixWorldInverse));
 if(projected.some(v=>v.z>=-camera.near))return new THREE.Vector4(0,0,1,1);
 projected.forEach(v=>v.applyMatrix4(camera.projectionMatrix));
 const x=Math.max(-1,Math.min(...projected.map(v=>v.x))),y=Math.max(-1,Math.min(...projected.map(v=>v.y)));
 const width=Math.max(0,Math.min(1,Math.max(...projected.map(v=>v.x)))-x),height=Math.max(0,Math.min(1,Math.max(...projected.map(v=>v.y)))-y);
 return width*height>0?new THREE.Vector4((x+1)/2,(y+1)/2,width/2,height/2):null;
}
export function portalFootprint(camera:THREE.PerspectiveCamera,edge:Portal){const r=portalRect(camera,edge);return r?r.z*r.w:0;}


export function createPortalRenderer(renderer:THREE.WebGLRenderer,scene:THREE.Scene,view:HouseRuntime,selectSpace:(space:string)=>void){
 const black=new THREE.DataTexture(new Uint8Array([0,0,0,255]),1,1);black.needsUpdate=true;
 const surfaces=new Map<string,THREE.Mesh<THREE.BufferGeometry,THREE.MeshBasicMaterial>>();
 const targets=new Map<string,THREE.WebGLRenderTarget>();
 // Canvas antialiasing does not apply to offscreen portal images. Keep each
 // cropped pass multisampled too, including recursively visible doorways.
 const samples=Math.min(4,renderer.capabilities.maxSamples);
 let used=new Set<string>(),visibleRooms=new Set<string>(),passes=0;
 for(const edge of view.graph.portals.filter(p=>!p.continuous)){
  const corners=portalCorners(edge),geometry=new THREE.BufferGeometry();
  geometry.setAttribute('position',new THREE.Float32BufferAttribute(corners.flatMap(v=>v.toArray()),3));geometry.setIndex([0,1,2,0,2,3]);
  geometry.setAttribute('uv',new THREE.Float32BufferAttribute([0,0,1,0,1,1,0,1],2));
  const material=new THREE.MeshBasicMaterial({map:black,side:THREE.DoubleSide,toneMapped:false});
  const rect={value:new THREE.Vector4(0,0,1,1)};material.userData.portalRect=rect;
  material.onBeforeCompile=shader=>{
   shader.uniforms.portalRect=rect;
   shader.vertexShader='varying vec4 portalClip;\n'+shader.vertexShader.replace('#include <project_vertex>','#include <project_vertex>\nportalClip = gl_Position;');
   shader.fragmentShader='varying vec4 portalClip; uniform vec4 portalRect;\n'+shader.fragmentShader.replace('#include <map_fragment>','diffuseColor *= texture2D(map, (portalClip.xy / portalClip.w * 0.5 + 0.5 - portalRect.xy) / portalRect.zw);');
  };
  material.customProgramCacheKey=()=> 'portal-projective-v1';
  const mesh=new THREE.Mesh(geometry,material);mesh.userData.portalSurface=true;mesh.visible=false;mesh.frustumCulled=false;scene.add(mesh);surfaces.set(edge.key,mesh);
 }
 function renderSpace(space:string,camera:THREE.PerspectiveCamera,depth:number,path:string,arrival?:Portal,target:THREE.WebGLRenderTarget|null=null){
  const maps=new Map<string,{texture:THREE.Texture;rect:THREE.Vector4}>(),buffer=target?new THREE.Vector2(target.width,target.height):renderer.getDrawingBufferSize(new THREE.Vector2());
  const blank={texture:black,rect:new THREE.Vector4(0,0,1,1)};
  for(const edge of view.graph.outgoing(space)){
   if(edge.continuous||edge.key===arrival?.reverse)continue;
   const rect=portalRect(camera,edge);if(!rect)continue;
   const door=view.portalDoor(edge);
   // An owner-side closed leaf completely masks the view. Opposite-side leaves
   // still need the destination pass, because their physical offset is inside it.
   const ownerClosed=door&&door.amount===0&&!edge.from.port.seeThrough&&!edge.to.port.seeThrough&&view.graph.spaceOf(door.room.id)===space;
   if(depth>=3||ownerClosed){maps.set(edge.key,blank);continue;}
   for(const room of view.graph.members(edge.to.space))visibleRooms.add(room.id);
   if(!view.isLoaded(edge.to.room.id)){maps.set(edge.key,blank);continue;}
   const key=path+'/'+edge.key;
   const width=Math.max(16,Math.min(buffer.x,Math.ceil(buffer.x*rect.z/16)*16)),height=Math.max(16,Math.min(buffer.y,Math.ceil(buffer.y*rect.w/16)*16));
   let next=targets.get(key);if(!next){next=new THREE.WebGLRenderTarget(width,height,{depthBuffer:true,samples});targets.set(key,next);}
   if(next.width!==width||next.height!==height)next.setSize(width,height);
   const child=portalCamera(camera,edge);
   const crop=new THREE.Matrix4().set(1/rect.z,0,0,(1-2*rect.x-rect.z)/rect.z, 0,1/rect.w,0,(1-2*rect.y-rect.w)/rect.w, 0,0,1,0, 0,0,0,1);
   child.projectionMatrix.premultiply(crop);child.projectionMatrixInverse.copy(child.projectionMatrix).invert();
   used.add(key);renderSpace(edge.to.space,child,depth+1,key,edge,next);maps.set(edge.key,{texture:next.texture,rect});
  }
  selectSpace(space);
  for(const [key,mesh] of surfaces){mesh.visible=maps.has(key);const result=maps.get(key)??blank;mesh.material.map=result.texture;mesh.material.userData.portalRect.value.copy(result.rect);}
  // The reverse aperture at the entrance is clipped, not rendered recursively.
  renderer.clippingPlanes=arrival?[entrancePlane(arrival)]:[];
  renderer.setRenderTarget(target);renderer.render(scene,camera);passes++;
 }
 const oldAutoReset=renderer.info.autoReset;renderer.info.autoReset=false;
 return {
  render(camera:THREE.PerspectiveCamera){
   used=new Set();visibleRooms=new Set();passes=0;renderer.info.reset();
   const oldTarget=renderer.getRenderTarget(),oldPlanes=renderer.clippingPlanes;
   try{
    // Keep the aperture in front of the near plane until the actual crossing.
    const main=camera.clone();
    for(const edge of view.graph.outgoing(view.activeSpace)){
     const d=camera.position.clone().sub(point(edge.from.point)),normal=new THREE.Vector3(edge.from.normal.x,edge.from.normal.height,-edge.from.normal.y);
     const along=Math.abs(d.dot(normal)),across=Math.abs(d.x*normal.z-d.z*normal.x);
     const local=d.clone().applyAxisAngle(new THREE.Vector3(0,1,0),-edge.from.room.yaw);
     const inside=edge.from.port.kind==='hatch'?Math.abs(local.x)<edge.from.port.width/2+.1&&Math.abs(local.z)<edge.from.port.depth!/2+.1:across<edge.from.port.width/2+.1&&d.y>0&&d.y<(edge.from.port.height??2.7);
     if(along<.1&&inside)main.near=Math.min(main.near,Math.max(.0001,along*.4));
    }
    main.updateProjectionMatrix();renderSpace(view.activeSpace,main,0,view.activeSpace);
   }
   finally{renderer.setRenderTarget(oldTarget);renderer.clippingPlanes=oldPlanes;selectSpace(view.activeSpace);}
   for(const [key,target] of targets)if(!used.has(key)){target.dispose();targets.delete(key);}
   return visibleRooms;
  },
  get stats(){return {passes,targets:targets.size,visibleRooms:[...visibleRooms]};},
  dispose(){surfaces.forEach(m=>{m.removeFromParent();m.geometry.dispose();m.material.dispose();});targets.forEach(t=>t.dispose());targets.clear();black.dispose();renderer.info.autoReset=oldAutoReset;},
 };
}
