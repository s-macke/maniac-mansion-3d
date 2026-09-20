"""Furnished circular EGA observatory with an open dome slit and floor hatch."""
from pathlib import Path
import sys,math,bpy
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config,save_generated
from blender_shared.shell import setup,reference
from blender_shared.layout_shell import PALETTE
from blender_shared.ladder_assets import register
c=load_config(Path(__file__).with_name('room.json'),prepare=True);g=c['geometry']
scene,cols,geo=setup(PALETTE)
R,C,H,Z,T,N,K=[g[k] for k in ['radius','centerY','wallHeight','domeRise','wallThickness','segments','roofRings']]
def mesh(name,points,color):
 return geo.mesh(name,points,[tuple(range(len(points)))],color)
def point(a,r,z):return (r*math.cos(a),C+r*math.sin(a),z)
def patch(name,points,color):
 # Both shell faces are explicit geometry, so the dome remains visible from either side.
 o=mesh(name,points,color)
 if name in ['Dome_inner','Dome_outer','Curved_wall','Outer_wall']:
  o['bake_curved_center']=[0,C,H if name.startswith('Dome') else 0]
  o['bake_curved_radii']=[R,R,Z] if name.startswith('Dome') else [R,R,0]
  o['bake_curved_sign']=-1 if name in ['Dome_inner','Curved_wall'] else 1
def clip(poly,axis,value,greater):
 result=[]
 for p,q in zip(poly,poly[1:]+poly[:1]):
  a=(p[axis]-value)*(1 if greater else -1);b=(q[axis]-value)*(1 if greater else -1)
  if a>=-1e-9:result.append(p)
  if (a<0)!=(b<0):
   t=a/(a-b);result.append(tuple(p[i]+t*(q[i]-p[i]) for i in range(3)))
 return result
# Tile and clip the floor disk around the rectangular access hole; no hidden slab spans it.
hole=g['floorHoles'][0];circle=[point(i*math.tau/N,R,0) for i in range(N)]
xs=sorted(set([-R+i*2*R/16 for i in range(17)]+[hole['x0'],hole['x1']]));ys=sorted(set([i*2*C/16 for i in range(17)]+[hole['y0'],hole['y1']]))
for x0,x1 in zip(xs,xs[1:]):
 for y0,y1 in zip(ys,ys[1:]):
  if hole['x0']<(x0+x1)/2<hole['x1'] and hole['y0']<(y0+y1)/2<hole['y1']:continue
  poly=circle
  for axis,v,positive in [(0,x0,True),(0,x1,False),(1,y0,True),(1,y1,False)]:poly=clip(poly,axis,v,positive)
  if len(poly)>2:
   patch('Circular_floor',poly,'lightblue');patch('Floor_underside',[(x,y,-.12) for x,y,_ in reversed(poly)],'blue')
for i in range(N):
 a=i*math.tau/N;b=(i+1)*math.tau/N
 slit=abs(math.atan2(math.sin((a+b)/2-g['slitAngle']),math.cos((a+b)/2-g['slitAngle'])))<g['slitHalfAngle']
 top=g['slitSill'] if slit else H
 patch('Curved_wall',[point(a,R,0),point(a,R,top),point(b,R,top),point(b,R,0)],'cyan')
 patch('Outer_wall',[point(a,R+T,0),point(b,R+T,0),point(b,R+T,top),point(a,R+T,top)],'cyan')
 patch('Wall_rim',[point(a,R,top),point(a,R+T,top),point(b,R+T,top),point(b,R,top)],'aqua')
 if slit:continue
 for j in range(K):
  lo=j*math.pi/2/K;hi=(j+1)*math.pi/2/K
  inner=[point(a,R*math.cos(lo),H+Z*math.sin(lo)),point(a,R*math.cos(hi),H+Z*math.sin(hi)),point(b,R*math.cos(hi),H+Z*math.sin(hi)),point(b,R*math.cos(lo),H+Z*math.sin(lo))]
  if j==K-1:inner.pop(2)
  patch('Dome_inner',inner,'cyan')
  outer=[point(angle,(R+T)*math.cos(t),H+(Z+T)*math.sin(t)) for angle,t in [(a,lo),(b,lo),(b,hi),(a,hi)]]
  if j==K-1:outer.pop(3)
  patch('Dome_outer',outer,'cyan')
# Slit edge surfaces and thin aqua lips expose real wall thickness instead of a painted window.
for angle in [g['slitAngle']-g['slitHalfAngle'],g['slitAngle']+g['slitHalfAngle']]:
 geo.beam('Slit_upright',point(angle,R,g['slitSill']),point(angle,R,H),.065,'aqua')
 for j in range(K):
  a=j*math.pi/2/K;b=(j+1)*math.pi/2/K
  p=point(angle,R*math.cos(a),H+Z*math.sin(a));q=point(angle,R*math.cos(b),H+Z*math.sin(b))
  geo.beam('Slit_roof_lip',p,q,.065,'aqua')
# Access opening has a shallow visible rim, but no cover or crossbars.
for x in [hole['x0'],hole['x1']]:geo.box('Hatch_rim',(x,(hole['y0']+hole['y1'])/2,.025),(.065,hole['y1']-hole['y0']+.065,.05),'cyan')
for y in [hole['y0'],hole['y1']]:geo.box('Hatch_rim',((hole['x0']+hole['x1'])/2,y,.025),(hole['x1']-hole['x0'],.065,.05),'cyan')
c['geometry']['sharedAssets']=[];c['geometry']['doors']=[];register(c,cols['Architecture'])
sys.path.insert(0,str(Path(__file__).resolve().parent))
from interior import furnish
furnish(geo,c)
reference(ROOT,c,cols,'028');geo.active='Cameras'
geo.camera('01_Reference',(-.2,1.10,2.25),(0,5.9,2.0),lens=15)
geo.camera('02_Inside',(-.6,1.8,1.62),(2,6.5,2.6),lens=20)
geo.camera('03_Reverse',(2.9,3.3,1.62),(-2.5,3.7,.3),lens=22)
scene.camera=bpy.data.objects['02_Inside'];scene['scope']='Furnished circular observatory; real dome slit and den hatch remain open.'
save_generated(c);bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/c['source']));print('OBSERVATORY_COMPLETE',flush=True)
