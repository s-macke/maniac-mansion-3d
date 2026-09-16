import * as THREE from 'three';
import type {RoomDefinition} from './types';
const basis=new THREE.Matrix4().makeRotationX(-Math.PI/2),inverse=basis.clone().invert();
/** Placement matrices are in Blender coordinates; GLB geometry is already Y-up. */
export function assetMatrix(matrix:number[]){return basis.clone().multiply(new THREE.Matrix4().fromArray(matrix)).multiply(inverse);}
export function instantiateSharedAssets(root:THREE.Object3D,definition:RoomDefinition,library:THREE.Object3D,libraryId="doors"){
 const batches=new Map<string,{template:THREE.Mesh;matrices:THREE.Matrix4[];mirrored:boolean}>();
 for(const instance of definition.geometry?.sharedAssets??[]){
  if((instance.library??'doors')!==libraryId)continue;
  const template=library.getObjectByName(instance.asset);
  if(!template)throw new Error('Missing shared asset: '+instance.asset);
  if(!instance.doorNode){
   if(!(template instanceof THREE.Mesh))throw new Error('Shared template must be a mesh: '+instance.asset);
   const matrix=assetMatrix(instance.matrix),mirrored=matrix.determinant()<0,key=instance.asset+':'+mirrored;
   const batch=batches.get(key)??{template,matrices:[] as THREE.Matrix4[],mirrored};batch.matrices.push(matrix);batches.set(key,batch);continue;
  }
  const object=template.clone(true);object.name='Shared_'+instance.id;
  object.traverse(o=>{o.userData.sharedDoorResource=true;});
  object.matrixAutoUpdate=false;object.matrix.copy(assetMatrix(instance.matrix));
  if(instance.doorNode){
   const leaf=definition.geometry?.doors?.flatMap(d=>d.leaves).find(l=>l.node===instance.doorNode);
   if(!leaf)throw new Error('Missing door hinge: '+instance.doorNode);
   const pivot=new THREE.Group();pivot.name=instance.doorNode;pivot.position.set(leaf.hinge[0],leaf.hinge[2],-leaf.hinge[1]);pivot.add(object);root.add(pivot);
  }else root.add(object);
 }
 // Static frames/leaves batch per room. Mirroring lives on the batch object, so
 // instance matrices retain positive determinants (required by InstancedMesh).
 for(const [key,batch] of batches){
  const mesh=new THREE.InstancedMesh(batch.template.geometry,batch.template.material,batch.matrices.length);
  mesh.name='Shared_'+key;mesh.userData.sharedDoorResource=true;
  const reflect=new THREE.Matrix4().makeScale(-1,1,1);
  if(batch.mirrored)mesh.scale.x=-1;
  batch.matrices.forEach((m,i)=>mesh.setMatrixAt(i,batch.mirrored?reflect.clone().multiply(m):m));
  mesh.instanceMatrix.needsUpdate=true;mesh.computeBoundingBox();mesh.computeBoundingSphere();root.add(mesh);
 }
}
