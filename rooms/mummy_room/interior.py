"""025: sarcophagus, strength machine, low cabinet, calendar and mummy wall print."""
from pathlib import Path
import math
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import cabinet,finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 b('Exercise_wainscot',(0,4.85,.48),(10.04,.10,.88),'brown')
 for z,col in [(.13,'red'),(.76,'red'),(.88,'yellow'),(.96,'red')]:b('Exercise_wall_rail',(0,4.78,z),(10.04,.06,.04),col)
 cabinet(g,'Organ_cabinet',-3.73,4.32,1.20,.76,.89)
 source_patch(g,ROOT/'source/room 025.png',(72,82,111,103),(-3.73,3.86,.49),(1.03,.56),'Original_cabinet_contents')
 source_patch(g,ROOT/'source/room 025.png',(81,31,111,73),(-3.73,4.915,1.73),(.78,1.09),'Original_calendar')
 # A solid, inanimate blue Egyptian sarcophagus, with crossed arms and banded wrapping.
 x,y=-1.94,4.13
 body=g.sphere('Sarcophagus_body',(x,y,1.12),(.38,.25,.94),'lightblue')
 g.sphere('Sarcophagus_head',(x,y,2.12),(.29,.24,.34),'lightblue')
 g.mesh('Headdress',[(x-.44,y-.22,1.99),(x-.22,y-.22,2.51),(x+.22,y-.22,2.51),(x+.44,y-.22,1.99)],[(0,1,2,3)],'blue')
 g.sphere('Sarcophagus_face',(x,y-.26,2.17),(.17,.08,.22),'lightblue')
 for dx in [-.085,.085]:b('Sarcophagus_eye',(x+dx,y-.319,2.22),(.07,.024,.034),'black')
 # Keep the stripes inside the tapering headdress silhouette.
 for k in range(6):
  zz=2.015+k*.071
  outer=.44-(zz-1.99)/.52*.22
  for side in [-1,1]:
   b('Headdress_stripe',(x+side*(outer-.043),y-.226,zz),(.075,.018,.018),'lightblue')
 b('Pharaoh_beard',(x,y-.33,2.0),(.07,.07,.18),'blue')
 for s in [-1,1]:
  curved_line(g,'Crossed_sarcophagus_arm',[(x+s*.29,y-.17,1.80),(x+s*.25,y-.28,1.52),(x-s*.18,y-.30,1.85)],.14,'blue')
  g.sphere('Sarcophagus_foot',(x+s*.18,y-.05,.12),(.18,.30,.12),'lightblue')
 # Wrap the blue bands against the ellipsoid rather than flat floating rods.
 for k in range(7):
  zz=.40+k*.18
  points=[]
  for i in range(17):
   xx=-.22+i*.44/16;z=zz-xx*.40
   hit,point,_,_=body.ray_cast((xx/.38,-4,(z-1.12)/.94),(0,1,0))
   if hit:points.append((x+xx,y+point.y*.25-.002,z))
  curved_line(g,'Wrapping_band',points,.018,'blue')
 # Thin aerial above the headdress: a mast with three crossbars.
 g.beam('Mummy_aerial_mast',(x,y,2.48),(x,y,2.93),.019,'black')
 for z,w in [(2.68,.38),(2.77,.46),(2.86,.28)]:g.beam('Mummy_aerial_crossbar',(x-w/2,y,z),(x+w/2,y,z),.016,'black')
 # Exercise machine: open steel uprights, pulley, seat and stacked weights.
 x,y=.03,4.14
 b('Machine_base',(x,y,.07),(1.03,.92,.14),'black')
 for dx in [-.43,.43]:
  g.beam('Machine_upright',(x+dx,y+.22,.10),(x+dx,y+.22,2.33),.065,'black')
  g.beam('Upright_glint',(x+dx-.02,y+.175,.14),(x+dx-.02,y+.175,2.25),.018,'gray')
 curved_line(g,'Machine_top',[(x-.43,y+.22,2.33),(x-.19,y+.22,2.46),(x+.19,y+.22,2.46),(x+.43,y+.22,2.33)],.07,'black')
 g.beam('Pulley_cable',(x,y+.22,2.43),(x,y+.22,.70),.014,'gray')
 for k in range(7):b('Weight_stack',(x,y+.19,.21+k*.085),(.40,.33,.055),'darkgray')
 # Actual pulley wheel, axle, pull cable and horizontal upper grip.
 pulley=g.cyl('Machine_pulley',(0,0,0),.105,.065,'gray',16)
 pulley.rotation_euler.x=math.pi/2;pulley.location=(x,y+.22,2.35)
 hub=g.cyl('Pulley_hub',(0,0,0),.032,.025,'black',12)
 hub.rotation_euler.x=math.pi/2;hub.location=(x,y+.175,2.35)
 g.beam('Front_pull_cable',(x,y+.10,2.35),(x,y-.02,1.65),.013,'gray')
 g.beam('Pull_bar',(x-.27,y-.02,1.65),(x+.27,y-.02,1.65),.035,'white')
 for side in [-1,1]:g.beam('Pull_grip',(x+side*.19,y-.02,1.65),(x+side*.32,y-.02,1.65),.048,'black')
 b('Machine_seat',(x,y-.18,.80),(.55,.49,.09),'brown');b('Machine_backrest',(x,y+.19,1.09),(.39,.11,.54),'black')
 for dx in [-.29,.29]:curved_line(g,'Exercise_handle',[(x+dx,y+.2,1.0),(x+dx,y-.30,1.0),(x+dx,y-.32,1.18)],.045,'yellow')
 source_patch(g,ROOT/'source/room 025.png',(265,25,368,73),(2.28,4.915,1.97),(2.74,1.28),'Original_mummy_diagram')
 finish(c)
