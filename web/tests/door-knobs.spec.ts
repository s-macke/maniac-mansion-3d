import {test,expect} from '@playwright/test';
import * as THREE from 'three';
import {createHouseRuntime} from '../lib/house/runtime';
import {loadDoorKit} from './shared-fixture';

test('every standard and screen-door handle is opposite its hinge, including both dining-room doors',async()=>{
 const runtime=createHouseRuntime(),kit=await loadDoorKit();let checked=0,total=0;
 for(const room of runtime.rooms){
  const def=runtime.definitions[room.definition];
  for(const asset of def.geometry?.sharedAssets??[]){
   if(!asset.doorNode)continue;
   // Instance matrices are in Blender coordinates and relative to the hinge.
   const hinge=new THREE.Vector3().applyMatrix4(new THREE.Matrix4().fromArray(asset.matrix).invert());
   const mesh=kit.getObjectByName(asset.asset) as THREE.Mesh;
   mesh.geometry.computeBoundingBox();const bounds=mesh.geometry.boundingBox!;
   expect(Math.min(Math.abs(hinge.x-bounds.min.x),Math.abs(hinge.x-bounds.max.x)),room.id+':'+asset.doorNode+' edge pivot').toBeLessThan(.04);total++;
   if(!['Standard_leaf','Pool_leaf','Dungeon_leaf','Metal_leaf'].includes(asset.asset))continue;
   let handleX=-.34;
   if(asset.asset==='Standard_leaf'){
    const p=mesh.geometry.getAttribute('position');const xs:number[]=[];
    // The physical knobs project beyond the panels on both faces (glTF Z).
    for(let i=0;i<p.count;i++)if(Math.abs(p.getZ(i))>.19)xs.push(p.getX(i));
    expect(xs.length).toBeGreaterThan(0);handleX=xs.reduce((a,b)=>a+b,0)/xs.length;
   }else if(asset.asset==='Pool_leaf')handleX=.52;
   else if(asset.asset==='Metal_leaf')handleX=-.14;
   expect(hinge.x*handleX,room.id+':'+asset.doorNode).toBeLessThan(0);
   expect(Math.abs(hinge.x)).toBeGreaterThan(.48);checked++;
  }
 }
 expect(checked).toBeGreaterThan(20);expect(total).toBe(runtime.doors.items.reduce((n,d)=>n+d.def.leaves.length,0));
 const cellar=runtime.definitions.connected_hall.geometry!.sharedAssets!.find(a=>a.doorNode==='Door_cellar')!;
 expect(cellar.asset).toBe('Standard_plain_leaf');
 const plain=kit.getObjectByName('Standard_plain_leaf') as THREE.Mesh;
 plain.geometry.computeBoundingBox();expect(Math.max(Math.abs(plain.geometry.boundingBox!.min.z),Math.abs(plain.geometry.boundingBox!.max.z))).toBeLessThan(.14);
});
