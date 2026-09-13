/** Collision in Blender floor coordinates (x, y); Three.js uses (x, height, -y).
 * Matches scripts/model_entrance.py and scripts/model_connected_hall.py. Closed doors are room boundaries for this slice.
 */
import type { Point } from '../house/types';
import { segmentProjection, inPolygon } from '../house/geometry';
import { RADIUS } from '../house/navigation';
import manifest from '../house/generated.json' with {type:'json'};
const config=manifest.definitions.connected_hall;
const {stair,gallery}=config.geometry;
const N = stair.segments;
const centers = Array.from({ length: N + 1 }, (_, i) => {
  const t = i / N;
  return { x: stair.x + stair.sweep * Math.sin(t * Math.PI * stair.angle), y: stair.y + stair.length * t };
});
export const stairEdges = centers.map((p, i) => {
  const a = centers[Math.max(0, i - 1)], b = centers[Math.min(N, i + 1)];
  const length = Math.hypot(b.x - a.x, b.y - a.y);
  const nx = (b.y - a.y) / length, ny = -(b.x - a.x) / length;
  const half = (stair.width - stair.taper * i / N) / 2;
  return { left: { x: p.x - nx * half, y: p.y - ny * half }, right: { x: p.x + nx * half, y: p.y + ny * half } };
});
export const galleryBoundary: Point[] = [
  {x:-gallery.halfWidth,y:gallery.front},{x:gallery.openingLeft,y:gallery.front},stairEdges[N].left,stairEdges[N].right,
  {x:gallery.openingRight,y:gallery.front},{x:gallery.halfWidth,y:gallery.front},{x:gallery.halfWidth,y:gallery.back},{x:-gallery.halfWidth,y:gallery.back},
];
export function floorHeight(p: Point, currentHeight = 0) {
  for(let i=0;i<N;i++) {
    if(inPolygon(p,[stairEdges[i].left,stairEdges[i].right,stairEdges[i+1].right,stairEdges[i+1].left])) {
      return (i+segmentProjection(p,centers[i],centers[i+1]).t)*stair.rise/N;
    }
  }
  // Two floors overlap in plan. The current elevation determines which one
  // supports the player; walking beneath the balcony must not teleport upstairs.
  if(currentHeight>2.95 && inPolygon(p,galleryBoundary)) return stair.rise;
  return p.y<=6.5 ? 0 : Number.NaN;
}
const galleryRails = [
  [galleryBoundary[0],galleryBoundary[1]], [galleryBoundary[1],galleryBoundary[2]],
  [galleryBoundary[3],galleryBoundary[4]], [galleryBoundary[4],galleryBoundary[5]],
];

const barriers = stairEdges.slice(0,-1).flatMap((p,i) => [[p.left,stairEdges[i+1].left],[p.right,stairEdges[i+1].right]]);
const pots = [{x:-2.25,y:4.99,r:.42},{x:2.10,y:5.05,r:.42}];
const boxes = [
  {x0:-5.53,x1:-4.71,y0:5.60,y1:6.24}, // clock case and plinth
  ...[stairEdges[0].left,stairEdges[0].right].map(p=>({x0:p.x-.24,x1:p.x+.24,y0:p.y-.23,y1:p.y+.23})),
];
export function canStand(p: Point, previousHeight = 0) {
  const h = floorHeight(p,previousHeight);
  if(!Number.isFinite(h))return false;
  if(p.x < -6.08+RADIUS || p.x > 6.08-RADIUS || p.y < .14+RADIUS) return false;
  if(p.y > (h>2.95 ? 9.42 : 6.26)-RADIUS) return false;
  if(Math.abs(h-previousHeight)>.34) return false;
  for(const c of pots) if(h<1.4 && Math.hypot(p.x-c.x,p.y-c.y)<c.r+RADIUS) return false;
  for(const b of h<1.4 ? boxes : []) {
    const qx=Math.max(b.x0,Math.min(b.x1,p.x)),qy=Math.max(b.y0,Math.min(b.y1,p.y));
    if(Math.hypot(p.x-qx,p.y-qy)<RADIUS) return false;
  }
  for(const [a,b] of barriers) {
    const railHeight=floorHeight(segmentProjection(p,a,b));
    if((h<1.4 || !Number.isFinite(railHeight) || h<railHeight+.95) && segmentProjection(p,a,b).distance<RADIUS+.045)return false;
  }
  if(h>2.95)for(const [a,b] of galleryRails)if(segmentProjection(p,a,b).distance<RADIUS+.07)return false;
  return true;
}

export function zone(p: {height:number;y:number}) {
 return p.height>3.30 && p.y>6.5?"Upstairs landing":p.height>.2?"Grand staircase":"Entrance hall";
}
