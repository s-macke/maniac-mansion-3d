"""026: patterned bedspread, model aircraft, plans, hamster enclosure and piggy bank."""
from blender_shared.placement import rear_anchored, offset_group
from pathlib import Path
import random,bpy
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import bed,cabinet,finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.1)
def furnish(g,c):
 b=g.box;bed(g,-2.10,3.78,2.75,1.58,'lime','gray')
 # This bed has an open metal frame, unlike the two wooden beds.
 for o in list(bpy.data.objects):
  if o.name.startswith('Bed_end'):bpy.data.objects.remove(o,do_unlink=True)
 for x in [-3.475,-.725]:
  curved_line(g,'Metal_bed_end',[(x,2.98,.90),(x,3.20,1.02),(x,4.36,1.02),(x,4.58,.90)],.045,'gray')
 # Repeat irregular red/green EGA flecks across top and hanging blanket.
 rng=random.Random(26)
 for i in range(300):
  x=rng.uniform(-3.03,-.79);y=rng.uniform(3.04,4.49);col=rng.choice(['green','red','black'])
  b('Camouflage_top',(x,y,.759),(.07,.10,.004),col)
  b('Camouflage_drop',(x,2.931,rng.uniform(.25,.60)),(.06,.009,.05),col)
 for x in [-3.48,-.72]:
  for y in [2.94,4.61]:g.cyl('Bedpost',(x,y,.62),.047,1.22,'gray');g.sphere('Bedpost_finial',(x,y,1.24),(.072,.072,.072),'gray')
 source_patch(g,ROOT/'source/room 026.png',(48,24,152,73),(-2.0,4.79,2.04),(2.50,1.18),'Original_blueprint')
 cabinet(g,'Hamster_cabinet',.15,4.36,.90,.75,.92,'green')
 # Open-front framed enclosure: solid animal visible from multiple angles.
 b('Hamster_tank_base',(.15,4.36,.99),(.79,.62,.05),'gray')
 b('Hamster_tank_back',(.15,4.66,1.23),(.79,.025,.49),'lightblue')
 for xx in [-.23,.53]:
  for yy in [4.06,4.66]:b('Tank_corner',(xx,yy,1.23),(.022,.022,.49),'black')
 for zz in [1.0,1.47]:
  for yy in [4.06,4.66]:b('Tank_long_rim',(.15,yy,zz),(.79,.024,.027),'gray')
  for xx in [-.23,.53]:b('Tank_side_rim',(xx,4.36,zz),(.024,.62,.027),'gray')
 g.sphere('Hamster_body',(.19,4.32,1.13),(.225,.12,.115),'white')
 g.sphere('Hamster_brown_back',(.26,4.34,1.205),(.13,.105,.055),'brown')
 g.sphere('Hamster_head',(-.04,4.30,1.15),(.11,.105,.11),'white')
 g.sphere('Hamster_muzzle',(-.125,4.275,1.12),(.055,.07,.045),'white')
 g.sphere('Hamster_pink_nose',(-.17,4.245,1.125),(.018,.021,.016),'lightred')
 for yy in [4.225,4.375]:
  g.sphere('Hamster_ear',(-.015,yy,1.242),(.038,.025,.050),'white')
  g.sphere('Hamster_inner_ear',(-.026,yy-.012,1.251),(.022,.014,.026),'lightred')
  g.sphere('Hamster_eye',(-.076,4.203 if yy<4.3 else 4.397,1.179),(.014,.008,.015),'black')
 for xx in [-.045,.30]:
  for yy in [4.225,4.415]:
   g.sphere('Hamster_leg',(xx,yy,1.09),(.035,.026,.065),'white')
   g.sphere('Hamster_paw',(xx,yy,1.035),(.04,.028,.022),'lightred')
 g.sphere('Hamster_tail',(.41,4.34,1.10),(.03,.024,.025),'white')
 with offset_group(y=5.1-c['geometry']['depth']):
  cabinet(g,'Piggy_table',1.08,1.0,1.04,.69,.54)
  g.sphere('Piggy_bank',(1.08,1,.85),(.36,.17,.23),'lightred');g.sphere('Pig_snout',(1.43,1,.85),(.08,.12,.095),'lightred')
  for x in [.89,1.29]:
   for y in [.88,1.12]:b('Pig_foot',(x,y,.66),(.075,.06,.13),'lightred')
  for y in [.91,1.09]:g.mesh('Pig_ear',[(1.23,y,1),(1.31,y,1.19),(1.37,y,1)],[(0,1,2)],'lightred')
  b('Coin_slot',(1.08,1,1.075),(.14,.025,.007),'black');g.sphere('Pig_eye',(1.34,.84,.95),(.025,.012,.025),'black')
 for x,y,z,col in [(-2.8,3.7,2.74,'blue'),(-1.25,3.95,2.91,'white')]:
  g.cyl('Model_plane_thread',(x,y,(3.12+z)/2),.005,3.12-z,'gray')
  # Complete the propeller, upright tail and wheels of each hanging model.
  g.beam('Plane_propeller',(x-.13,y-.365,z),(x+.13,y-.365,z),.018,col)
  g.sphere('Plane_spinner',(x,y-.365,z),(.045,.045,.045),col)
  g.mesh('Plane_vertical_tail',[(x,y+.14,z+.03),(x,y+.29,z+.15),(x,y+.32,z+.03)],[(0,1,2)],col)
  for dx in [-.11,.11]:
   g.beam('Plane_undercarriage',(x+dx,y-.10,z),(x+dx,y-.10,z-.12),.015,'gray')
   g.sphere('Plane_wheel',(x+dx,y-.10,z-.13),(.025,.045,.045),'black')
  b('Plane_fuselage',(x,y,z),(.075,.69,.07),col);b('Plane_wings',(x,y-.04,z),( .72,.14,.045),col);b('Plane_tail',(x,y+.27,z+.03),(.30,.10,.035),col)
 source_patch(g,ROOT/'source/room 026.png',(162,17,204,43),(.36,4.79,2.51),(.92,.57),'Red_pennant',only={'red','lightred'})
 # The source window is on the right return wall, perpendicular to the door.
 from blender_shared.windows import cut_wall,outside_window
 author_offset=5.1-c['geometry']['depth']
 window_y=2.9+author_offset
 cut_wall(g,'Wall_right',[(window_y-.5,window_y+.5,1.0,2.6)],axis='y',author_offset_y=author_offset)
 outside_window(g,'Bedroom_window',(c['geometry']['halfWidth']-c['geometry']['wallThickness'],window_y,1.8),(1,0),1.0,1.6,seed=26)
 finish(c)
