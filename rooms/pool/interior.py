"""Drained basin details from background 002, below the existing water level."""
import math
from pathlib import Path
from blender_shared.lab_furniture import cylinder,pipe,disc
from blender_shared.furnishings import source_patch
ROOT=Path(__file__).resolve().parents[2]

def furnish(g,p):
 g.active='Details';bottom=p['bottom'];back=p['y1']-.105
 # Keep the centre aisle and the original ladder landing open.
 x,y=14.65,7.25
 g.cyl('Reactor_foot',(x,y,bottom+.08),.52,.16,'darkgray',32)
 g.cyl('Reactor_body',(x,y,bottom+.77),.46,1.34,'gray',32)
 for z in [bottom+.27,bottom+.55,bottom+1.22]:g.cyl('Reactor_band',(x,y,z),.49,.075,'darkgray',32)
 g.sphere('Reactor_dome',(x,y,bottom+1.42),(.46,.46,.32),'gray')
 disc(g,'Radiation_plate',x,y-.47,bottom+1.17,.29,'yellow')
 source_patch(g,ROOT/'source/room 002.png',(230,74,260,91),(x,y-.493,bottom+1.17),(.54,.306),'Reactor_radiation',only={'black','yellow'})
 for i,xx in enumerate([x-.48,x,x+.48]):
  pipe(g,'Reactor_feed',[(xx,7.56,bottom+1.36),(xx,7.56,-.40)],.065,'lightgreen',False)
  cylinder(g,'Feed_highlight',(xx-.02,7.50,bottom+1.49),(xx-.02,7.50,-.40),.025,'aqua')
  g.box('Feed_socket',(xx,7.56,bottom+1.39),(.20,.22,.14),'darkgray')
 points=[(x+.45,y,bottom+1.16),(15.75,y,bottom+1.16),(16.17,y,bottom+1.65),(16.56,y,bottom+1.65),(16.64,y,bottom+.24)]
 pipe(g,'Flexible_hose',points,.13,'darkgray',False)
 for a,b in zip(points,points[1:]):
  n=math.ceil(math.dist(a,b)/.105)
  for i in range(n):
   t=(i+.5)/n;u=min(1,t+.034/math.dist(a,b));aa=tuple(a[k]+(b[k]-a[k])*t for k in range(3));bb=tuple(a[k]+(b[k]-a[k])*u for k in range(3));cylinder(g,'Hose_rib',aa,bb,.145,'gray',12)
 # Original painted numbers retain the artwork's pixel shapes and colors.
 for crop,z in [((47,24,76,42),-.68),((47,80,76,98),-1.93)]:
  source_patch(g,ROOT/'source/room 002.png',crop,(6.60,back-.008,z),(.80,.50),'Depth_mark',only={'black'})
 for z in [-1.05,-2.18]:g.box('Basin_depth_seam',((p['x0']+p['x1'])/2,back,z),(p['x1']-p['x0']-.20,.012,.022),'darkgray')
 # Drain grille sits flush with the basin floor.
 g.cyl('Drain_rim',(10,5.85,bottom+.013),.54,.022,'gray',40)
 g.cyl('Drain_recess',(10,5.85,bottom+.027),.43,.007,'black',40)
 for offset in [-.3,-.15,0,.15,.3]:
  length=2*math.sqrt(.43**2-offset**2)
  g.box('Drain_bar',(10+offset,5.85,bottom+.034),(.035,length,.015),'gray')
 g.box('Basin_plug_base',(7,6.95,bottom+.04),(.58,.40,.08),'purple')
 g.box('Basin_plug',(7.10,7.02,bottom+.25),(.25,.25,.43),'pink')
 pipe(g,'Plug_cord',[(6.74,6.9,bottom+.05),(6.37,6.55,bottom+.045),(6.43,6.26,bottom+.045),(6.72,6.20,bottom+.045)],.018,'black',False)
 # Thin angular cracks on the right wall; no extra opening or connection.
 for path in [[(7.2,-.35),(7.0,-.75),(7.3,-1.04),(6.95,-1.45),(7.13,-1.85)],[(7.3,-1.04),(7.55,-1.28)],[(7.0,-.75),(6.8,-.90)]]:
  for a,b in zip(path,path[1:]):g.beam('Basin_wall_crack',(p['x1']-.098,*a),(p['x1']-.098,*b),.012,'blue')
