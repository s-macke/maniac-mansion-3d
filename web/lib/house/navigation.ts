import type { Walker, Navigation } from './types';
export const EYE_HEIGHT=1.62;
export const RADIUS=.24;
export function moveWalker(walker: Walker, dx: number, dy: number, navigation: Navigation): Walker {
  let p={...walker};
  // Small fixed spatial substeps avoid tunneling at low frame rates; axis sliding
  // lets the player move along walls instead of getting caught on them.
  const count=Math.max(1,Math.ceil(Math.hypot(dx,dy)/.045));
  for(let i=0;i<count;i++) {
    let q={x:p.x+dx/count,y:p.y+dy/count};
    if(navigation.canStand(q,p.height)) p={...q,height:navigation.floorHeight(q,p.height)};
    else {
      q={x:p.x+dx/count,y:p.y};if(navigation.canStand(q,p.height))p={...q,height:navigation.floorHeight(q,p.height)};
      q={x:p.x,y:p.y+dy/count};if(navigation.canStand(q,p.height))p={...q,height:navigation.floorHeight(q,p.height)};
    }
  }
  return p;
}
