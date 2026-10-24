import {test} from 'node:test';
import assert from 'node:assert/strict';
import * as THREE from 'three';
import {intersection} from './audit-surfaces.mjs';
function tri(points){const p=points.map(v=>new THREE.Vector3(...v)),n=p[1].clone().sub(p[0]).cross(p[2].clone().sub(p[0])).normalize();return {p,n,d:n.dot(p[0])};}
const a=tri([[0,0,0],[1,0,0],[0,1,0]]);
test('overlap includes identical and partially overlapping triangles',()=>{
 assert.equal(intersection(a,a).area,.5);
 assert.ok(intersection(a,tri([[.25,0,0],[1.25,0,0],[.25,1,0]])).area>0);
});
test('shared edges and disjoint triangles are not overlaps',()=>{
 assert.equal(intersection(a,tri([[1,0,0],[1,1,0],[0,1,0]])),null);
 assert.equal(intersection(a,tri([[2,0,0],[3,0,0],[2,1,0]])),null);
});
test('near surfaces respect plane tolerance and report reversed winding',()=>{
 assert.ok(intersection(a,tri([[0,0,.0002],[1,0,.0002],[0,1,.0002]])));
 assert.equal(intersection(a,tri([[0,0,.002],[1,0,.002],[0,1,.002]])),null);
 assert.equal(intersection(a,tri([[0,1,0],[1,0,0],[0,0,0]])).opposed,true);
});
test('vertical planes work and crossing nonparallel faces are excluded',()=>{
 const b=tri([[2,0,0],[2,1,0],[2,0,1]]);
 assert.equal(intersection(b,b).area,.5);
 assert.equal(intersection(a,b),null);
});
