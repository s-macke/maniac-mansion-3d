// Read-only audit of exported room geometry; no Blender rebuild required.
import {readFile, mkdir, writeFile} from 'node:fs/promises';
import {fileURLToPath} from 'node:url';
import path from 'node:path';
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';

const root = fileURLToPath(new URL('../../', import.meta.url));
const tolerance = 0.0005; // 0.5 mm, a diagnostic threshold, not a visibility guarantee.
const cellSize = 0.5;
const read = async p => JSON.parse(await readFile(path.join(root,p),'utf8'));
const cross = (a,b,c) => (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);

// Convex triangle clipping: shared edges/vertices have zero area and are ignored.
export function overlap(a,b) {
  let out=a.map(p=>[...p]);
  const sign=Math.sign(cross(...b));
  for(let i=0;i<3 && out.length;i++) {
    const u=b[i],v=b[(i+1)%3],input=out;out=[];
    for(let j=0;j<input.length;j++) {
      const p=input[j],q=input[(j+1)%input.length];
      const dp=sign*cross(u,v,p),dq=sign*cross(u,v,q);
      if(dp>=0)out.push(p);
      if((dp>=0)!==(dq>=0)) {const t=dp/(dp-dq);out.push([p[0]+t*(q[0]-p[0]),p[1]+t*(q[1]-p[1])]);}
    }
  }
  let area=0;
  for(let i=0;i<out.length;i++)area+=out[i][0]*out[(i+1)%out.length][1]-out[i][1]*out[(i+1)%out.length][0];
  return {area:Math.abs(area)/2, polygon:out};
}

export function intersection(a,b) {
  if(Math.abs(a.n.dot(b.n))<0.999999)return null;
  if(b.p.some(p=>Math.abs(a.n.dot(p)-a.d)>tolerance))return null;
  const axis=[Math.abs(a.n.x),Math.abs(a.n.y),Math.abs(a.n.z)].indexOf(Math.max(Math.abs(a.n.x),Math.abs(a.n.y),Math.abs(a.n.z)));
  const axes=[0,1,2].filter(i=>i!==axis);
  const projected=p=>axes.map(i=>p.getComponent(i));
  const hit=overlap(a.p.map(projected),b.p.map(projected));
  const area=hit.area/Math.abs(a.n.getComponent(axis));
  if(area<1e-7)return null;
  const point=new THREE.Vector3();
  for(let k=0;k<2;k++)point.setComponent(axes[k],hit.polygon.reduce((s,p)=>s+p[k],0)/hit.polygon.length);
  point.setComponent(axis,(a.d-axes.reduce((s,i)=>s+a.n.getComponent(i)*point.getComponent(i),0))/a.n.getComponent(axis));
  return {point,area,gap:Math.max(...b.p.map(p=>Math.abs(a.n.dot(p)-a.d))),opposed:a.n.dot(b.n)<0};
}

function triangles(scene) {
  const result=[];scene.updateMatrixWorld(true);
  scene.traverse(obj=>{
    if(!obj.isMesh)return;
    const pos=obj.geometry.attributes.position,idx=obj.geometry.index;
    for(let i=0;i<(idx?.count??pos.count);i+=3){
      const p=[0,1,2].map(j=>new THREE.Vector3().fromBufferAttribute(pos,idx?idx.getX(i+j):i+j).applyMatrix4(obj.matrixWorld));
      const n=new THREE.Vector3().subVectors(p[1],p[0]).cross(new THREE.Vector3().subVectors(p[2],p[0]));
      if(n.lengthSq()<1e-20)continue;n.normalize();
      result.push({p,n,d:n.dot(p[0]),name:obj.name,face:i/3,min:[0,1,2].map(k=>Math.min(...p.map(v=>v.getComponent(k)))),max:[0,1,2].map(k=>Math.max(...p.map(v=>v.getComponent(k))))});
    }
  });return result;
}

async function audit(config) {
  const bytes=await readFile(path.join(root,config.asset));
  const scene=(await new GLTFLoader().parseAsync(bytes.buffer.slice(bytes.byteOffset,bytes.byteOffset+bytes.byteLength),'')).scene;
  const tris=triangles(scene),grid=new Map(),groups=new Map();let pairs=0;
  for(let i=0;i<tris.length;i++){
    const a=tris[i],lo=a.min.map(v=>Math.floor((v-tolerance)/cellSize)),hi=a.max.map(v=>Math.floor((v+tolerance)/cellSize));
    const seen=new Set();
    for(let x=lo[0];x<=hi[0];x++)for(let y=lo[1];y<=hi[1];y++)for(let z=lo[2];z<=hi[2];z++){
      const key=`${x},${y},${z}`,bucket=grid.get(key)??[];
      for(const j of bucket){
        if(seen.has(j))continue;seen.add(j);const b=tris[j];
        if(a.min.some((v,k)=>v>b.max[k]+tolerance||a.max[k]<b.min[k]-tolerance))continue;
        const hit=intersection(a,b);if(!hit)continue;pairs++;
        // Report Blender room-local coordinates: X/Y floor, Z height.
        const p=[hit.point.x,-hit.point.z,hit.point.y];
        const groupKey=p.map(v=>Math.floor(v/.25)).join(',')+':'+hit.opposed;
        let g=groups.get(groupKey);
        if(!g){g={position:p,area:0,pairs:0,maxGap:0,opposed:hit.opposed,examples:[]};groups.set(groupKey,g);}
        if(hit.area>g.area)g.position=p;
        g.area=Math.max(g.area,hit.area);g.pairs++;g.maxGap=Math.max(g.maxGap,hit.gap);
        if(g.examples.length<3)g.examples.push({a:a.name,faceA:a.face,b:b.name,faceB:b.face});
      }
      bucket.push(i);grid.set(key,bucket);
    }
  }
  const findings=[...groups.values()].sort((a,b)=>Number(a.opposed)-Number(b.opposed)||b.area-a.area);
  const origin=new THREE.Vector3(config.spawn.x,config.spawn.height+1.6,-config.spawn.y);
  // A bounded triage pass, not an exhaustive visibility audit or camera walkthrough.
  for(const g of findings.filter(g=>!g.opposed).slice(0,100)){
    const point=new THREE.Vector3(g.position[0],g.position[2],-g.position[1]);
    const direction=point.clone().sub(origin),distance=direction.length();
    const hits=new THREE.Raycaster(origin,direction.normalize(),.001,distance+.001).intersectObject(scene,true);
    g.lineOfSightFromSpawn=!!hits.length&&Math.abs(hits[0].distance-distance)<.001;
  }
  return {id:config.id,label:config.label,asset:config.asset,triangles:tris.length,pairs,findings};
}

async function main(){
  const layout=await read('house/layout.json'),results=[];
  const requested=process.argv.slice(2);
  for(const definition of [...new Set(layout.rooms.map(r=>r.definition))]){
    const config=await read(definition);
    if(requested.length&&!requested.includes(config.id))continue;
    const result=await audit(config);results.push(result);
    console.log(`${result.id}: ${result.triangles} triangles, ${result.pairs} pairs, ${result.findings.length} locations`);
  }
  const out=path.join(root,'generated/reports/surface-audit',requested.length?results.map(r=>r.id).join('+'):'');await mkdir(out,{recursive:true});
  await writeFile(path.join(out,'findings.json'),JSON.stringify({tolerance,scope:'Room GLBs only; excludes separately instanced shared kits, inter-room seams and runtime portal rendering.',rooms:results},null,2)+'\n');
  const lines=['# Surface overlap candidates','',`Plane tolerance: ${tolerance*1000} mm. Positions are room-local Blender (X, Y, Z), in metres. Locations grouped into 25 cm cells; positions are sample points inside actual overlaps.`,
    '', 'These are geometric candidates, not confirmed visible flicker. Hidden/internal faces, touching solids and intentional layers may be reported. Opposed normals often indicate internal contact. Largest individual triangle overlap is shown, not total surface area. Shared door/ladder kits and inter-room/portal seams are not included.',''];
  for(const r of results){
    lines.push(`## ${r.label} (${r.id})`,'',`${r.pairs} overlapping triangle pairs; ${r.findings.length} candidate locations.`,``, '| # | Local X / Y / Z (m) | Overlap (cm²) | Max gap (mm) | Normals |','|---|---|---:|---:|---|');
    r.findings.forEach((g,i)=>lines.push(`| ${i+1} | ${g.position.map(v=>v.toFixed(3)).join(' / ')} | ${(g.area*10000).toFixed(2)} | ${(g.maxGap*1000).toFixed(3)} | ${g.opposed?'opposed':'same direction'} |`));lines.push('');
  }
  await writeFile(path.join(out,'positions.md'),lines.join('\n'));
  const shortlist=['# Surface audit: initial review positions','',
    'Parallel, same-direction overlaps with a clear geometric ray from the configured room spawn at eye height 1.6 m. Only the 100 largest same-direction candidates per room were sampled. This is not proof of visible flicker, and shared kits are absent from the ray test. Coordinates are local Blender X/Y/Z in metres. All candidates remain in positions.md and findings.json.','',
    '| Room | Local X / Y / Z (m) | Largest overlap (cm²) | Gap (mm) |','|---|---|---:|---:|'];
  for(const r of results)for(const g of r.findings.filter(g=>g.lineOfSightFromSpawn))shortlist.push(`| ${r.id} | ${g.position.map(v=>v.toFixed(3)).join(' / ')} | ${(g.area*10000).toFixed(2)} | ${(g.maxGap*1000).toFixed(3)} |`);
  await writeFile(path.join(out,'review-first.md'),shortlist.join('\n')+'\n');
}
if(process.argv[1]===fileURLToPath(import.meta.url))await main();
