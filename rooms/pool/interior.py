"""Drained basin details from background 002, below the existing water level."""
import math
from pathlib import Path
from blender_shared.lab_furniture import cylinder,pipe,disc
from blender_shared.furnishings import source_patch
ROOT=Path(__file__).resolve().parents[2]

def furnish(g,p):
 g.active='Details';bottom=p['bottom'];back=p['y1']-.105
 # Small aqua/white tiles beneath the rim, following background 002.
 width=p['x1']-p['x0']-.20;count=round(width/.43)
 for i in range(count):
  xx=p['x0']+.10+(i+.5)*width/count
  g.box('Basin_tile',(xx,back-.004,-.28),(width/count-.016,.018,.18),'aqua' if i%3 else 'white')
  g.box('Basin_opposite_tile',(xx,p['y0']+.109,-.28),(width/count-.016,.018,.18),'aqua' if i%3 else 'white')
 g.mesh('Basin_wall_shadow',[(p['x0']+.10,back-.016,-.39),(6.8,back-.016,-.39),(11.0,back-.016,bottom+.02),(p['x0']+.10,back-.016,bottom+.02)],[(0,1,2,3)],'blue')
 # Keep the centre aisle and the original ladder landing open.
 x,y=14.65,7.25
 # Broad rounded pressure chamber over a narrow stepped pedestal, not a barrel.
 profile=[(.52,.025),(.53,.09),(.40,.15),(.39,.24),(.36,.28),(.36,.38),(.32,.42),(.32,.52),(.39,.60),(.51,.69),(.61,.84),(.65,1.03),(.62,1.22),(.52,1.43),(.33,1.58),(0,1.64)]
 verts=[];faces=[]
 for radius,z in profile:
  verts.extend((x+radius*math.cos(i*math.tau/32),y+radius*math.sin(i*math.tau/32),bottom+z) for i in range(32))
 for j in range(len(profile)-1):
  for i in range(32):faces.append((j*32+i,j*32+(i+1)%32,(j+1)*32+(i+1)%32,(j+1)*32+i))
 body=g.mesh('Reactor_pressure_chamber',verts,faces,'darkgray')
 body.data.materials.append(g.mats['gray'])
 for face in body.data.polygons:
  band=face.index//32
  if band in [1,3,5,12,13,14]:face.material_index=1
 disc(g,'Radiation_mount',x,y-.639,bottom+1.08,.24,'darkgray')
 source_patch(g,ROOT/'source/room 002.png',(238,76,253,90),(x,y-.657,bottom+1.08),(.43,.401),'Reactor_radiation',only={'black','yellow'})
 for xx,height in [(x-.48,1.49),(x,1.70),(x+.48,1.78)]:
  pipe(g,'Reactor_feed',[(xx,7.56,bottom+height),(xx,7.56,p['water']-.07)],.065,'lightgreen',False)
  cylinder(g,'Feed_highlight',(xx-.02,7.50,bottom+height),(xx-.02,7.50,p['water']-.07),.022,'aqua')
  cylinder(g,'Feed_socket',(xx,7.56,bottom+(1.10 if xx>x+.4 else height-.30)),(xx,7.56,bottom+height),.09,'darkgray')
  cylinder(g,'Feed_socket_lip',(xx,7.56,bottom+height-.025),(xx,7.56,bottom+height+.02),.115,'gray')
 points=[(x+.60,y,bottom+1.02),(15.68,y,bottom+1.02),(15.97,y,bottom+1.16),(16.03,y,bottom+1.45),(15.99,y,bottom+1.67),(16.18,y,bottom+1.83),(16.53,y,bottom+1.93),(16.87,y,bottom+1.86),(p['x1']-.10,y,bottom+1.86)]
 pipe(g,'Flexible_hose',points,.12,'darkgray',False)
 for a,b in zip(points,points[1:]):
  n=math.ceil(math.dist(a,b)/.09)
  for i in range(n):
   t=(i+.5)/n;u=min(1,t+.032/math.dist(a,b));aa=tuple(a[k]+(b[k]-a[k])*t for k in range(3));bb=tuple(a[k]+(b[k]-a[k])*u for k in range(3));cylinder(g,'Hose_rib',aa,bb,.134,'gray',12)
 # Hose terminates in the right wall; the green leak follows that wall.
 wall_x=p['x1']-.09
 cylinder(g,'Hose_wall_flange',(wall_x-.095,y,bottom+1.86),(wall_x+.015,y,bottom+1.86),.17,'darkgray')
 cylinder(g,'Hose_wall_flange_rim',(wall_x-.103,y,bottom+1.86),(wall_x-.075,y,bottom+1.86),.18,'gray')
 leak_x=wall_x-.018
 pipe(g,'Green_wall_leak',[(leak_x,y,bottom+1.71),(leak_x,y+.025,bottom+1.31),(leak_x,y-.015,bottom+.99),(leak_x,y+.02,bottom+.50),(leak_x,y,bottom+.08)],.018,'lightgreen',False)
 for dy,z,r in [(-.09,1.55,.025),(.10,1.25,.019),(-.07,.88,.018),(.05,.69,.02),(-.13,.31,.016),(.14,.12,.013)]:
  g.sphere('Green_wall_droplet',(wall_x-.009,y+dy,bottom+z),(.012,r,r*1.9),'green' if z<1 else 'lightgreen')
 g.mesh('Green_liquid_splash',[(wall_x+dx,y+dy,bottom+.008) for dx,dy in [(-.16,-.02),(-.08,-.08),(-.03,-.03),(-.01,-.06),(-.01,.06),(-.07,.09),(-.10,.03),(-.15,.07)]],[tuple(range(8))],'green')
 # Original painted numbers retain the artwork's pixel shapes and colors.
 for crop,z in [((47,24,76,42),-.68),((47,80,76,98),-1.93)]:
  source_patch(g,ROOT/'source/room 002.png',crop,(6.60,back-.037,z),(.80,.50),'Depth_mark',only={'black'})
 # Continue the basin finish opposite the source wall, without copying its
 # equipment, depth numbers, button, leak or directional shadow.
 for z in [-1.05,-2.18]:
  g.box('Basin_depth_seam',((p['x0']+p['x1'])/2,back-.030,z),(width,.012,.022),'blue')
  g.box('Basin_opposite_depth_seam',((p['x0']+p['x1'])/2,p['y0']+.135,z),(width,.012,.022),'blue')
 # Drain grille sits flush with the basin floor.
 g.cyl('Drain_rim',(10,5.85,bottom+.013),.54,.022,'gray',40)
 g.cyl('Drain_recess',(10,5.85,bottom+.027),.43,.007,'black',40)
 for offset in [-.3,-.15,0,.15,.3]:
  length=2*math.sqrt(.43**2-offset**2)
  g.box('Drain_bar',(10+offset,5.85,bottom+.034),(.035,length,.015),'gray')
 from chair import build_chair
 build_chair(g,'Basin_chair',7,6.95,bottom+.015)
 for offset in [-.3,-.15,0,.15,.3]:
  length=2*math.sqrt(.43**2-offset**2)
  g.box('Drain_crossbar',(10,5.85+offset,bottom+.039),(length,.026,.013),'gray')
 # Red wall button with its original downward arrow and lettering.
 source_patch(g,ROOT/'source/room 002.png',(180,63,201,77),(12.65,back-.021,-1.30),(.63,.42),'Button_arrow_and_lettering',only={'black','blue','red','brown','lightred'})
 disc(g,'Red_button_rim',12.65,back-.052,-1.72,.15,'black',.065)
 disc(g,'Red_button',12.65,back-.092,-1.72,.116,'red',.046)
 g.sphere('Button_highlight',(12.61,back-.120,-1.67),(.024,.013,.038),'lightred')
 # Source-like angular floor fractures around the equipment and drain.
 for path in [[(17.08,7.75),(16.72,7.22),(16.90,6.81),(16.22,6.37),(16.40,5.98)],[(16.90,6.81),(15.58,6.65),(15.19,6.22),(14.33,6.10)],[(14.33,6.10),(13.76,5.87),(13.20,6.03)],[(16.22,6.37),(16.01,5.70)],[(10.82,5.88),(11.32,5.74),(11.68,5.96)]]:
  for a,b in zip(path,path[1:]):g.beam('Basin_floor_crack',(*a,bottom+.006),(*b,bottom+.006),.015,'blue')
 # Thin angular cracks on the right wall; no extra opening or connection.
 for path in [[(7.2,-.35),(7.0,-.75),(7.3,-1.04),(6.95,-1.45),(7.13,-1.85)],[(7.3,-1.04),(7.55,-1.28)],[(7.0,-.75),(6.8,-.90)]]:
  for a,b in zip(path,path[1:]):g.beam('Basin_wall_crack',(p['x1']-.098,*a),(p['x1']-.098,*b),.012,'blue')
