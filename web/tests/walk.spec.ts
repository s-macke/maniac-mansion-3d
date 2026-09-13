import { test } from '@playwright/test';
import assert from 'node:assert/strict';
import { START, moveWalker, floorHeight, stairEdges, canStand } from '../lib/walk';
test('starting position is clear and reset coordinates stay on the floor',()=>{assert(canStand(START));assert.equal(floorHeight(START),0);});
test('large movement cannot tunnel through walls or the clock',()=>{
 let p=moveWalker(START,-100,0);assert(p.x>=-5.841);
 p=moveWalker({...START,x:-5.12},0,100);assert(p.y<5.37);
});
test('plant collision keeps the player outside pot radius',()=>{const p=moveWalker({x:-2.25,y:3,height:0},0,2);assert(p.y<=4.34);});
test('walk the actual curved stair centerline up and down',()=>{
 let p={x:-.55,y:1.5,height:0};
 const route=Array.from({length:201},(_,i)=>{const t=i/200;return {x:-.55+1.3*Math.sin(t*Math.PI*.8),y:2.15+4.10*t};});
 for(const q of route)p=moveWalker(p,q.x-p.x,q.y-p.y);
 assert(p.height>3.2,JSON.stringify(p));
 const top=p.height;
 for(const q of route.reverse())p=moveWalker(p,q.x-p.x,q.y-p.y);
 p=moveWalker(p,0,-.8);assert.equal(p.height,0);assert(top>3.2);
});
test('stairs cannot be entered through a side rail',()=>{
 const i=10,a=stairEdges[i].left,b=stairEdges[i].right;
 const p={x:(a.x+b.x)/2,y:(a.y+b.y)/2};let w={...p,height:floorHeight(p)};
 w=moveWalker(w,-4,0);assert(w.x>a.x);assert(w.height>0);
});
test('staircase and gallery form one connected walking surface in both directions',()=>{
 let p={x:-.55,y:1.5,height:0};
 const up=Array.from({length:201},(_,i)=>{const t=i/200;return{x:-.55+1.3*Math.sin(t*Math.PI*.8),y:2.15+4.13*t};});
 for(const q of up)p=moveWalker(p,q.x-p.x,q.y-p.y);
 p=moveWalker(p,0,1.2);assert(p.y>7.3,JSON.stringify(p));assert.equal(p.height,3.36);
 for(const q of [{x:-4.5,y:8.0},{x:4.5,y:8.0},{x:.2,y:8.7},{x:.2,y:7.5}]){
  p=moveWalker(p,q.x-p.x,q.y-p.y);assert(Math.hypot(p.x-q.x,p.y-q.y)<.1,JSON.stringify(p));assert.equal(p.height,3.36);
 }
 for(const q of up.reverse())p=moveWalker(p,q.x-p.x,q.y-p.y);
 p=moveWalker(p,0,-.8);assert.equal(p.height,0);assert(p.y<2);
});
test('gallery rail prevents falling, while ground floor stays accessible beneath it',()=>{
 const p=moveWalker({x:-4.5,y:8,height:3.36},0,-4);assert(p.y>5.95);assert.equal(p.height,3.36);
 assert.equal(floorHeight({x:-4.5,y:5.8},0),0);
 assert.equal(floorHeight({x:-4.5,y:5.8},3.36),3.36);
});
