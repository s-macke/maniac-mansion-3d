"""Background 022 medical study: desk, examination table and teaching skeleton."""
from pathlib import Path
import bpy,math
from blender_shared.furnishings import panel,source_patch,curved_line
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Rear-left desk and authentic chalkboard/certificates.
 b('Medical_desktop',(-1.50,4.81,.96),(2.55,.93,.11),'brown')
 for x in [-2.65,-.4]:
  b('Desk_drawer_pedestal',(x,4.84,.47),(.62,.76,.88),'brown')
  for z in [.25,.50,.75]:
   panel(geo,'Desk_drawer',x,4.44,z,.57,.21);b('Drawer_handle',(x,4.366,z),(.17,.04,.035),'yellow')
 source_patch(geo,ROOT/'source/room 022.png',(104,23,198,62),(-1.35,5.335,2.13),(2.26,.94),'Original_chalkboard')
 for x,crop in [(-2.68,(46,33,63,46)),(-2.18,(72,33,94,48))]:source_patch(geo,ROOT/'source/room 022.png',crop,(x,5.331,2.24 if x<-2.5 else 2.78),(.38,.30),'Medical_certificate')
 geo.cyl('Desk_lamp_base',(-2.35,4.8,1.04),.16,.035,'yellow');geo.cyl('Desk_lamp_stem',(-2.35,4.8,1.23),.025,.33,'brown');b('Desk_green_lamp',(-2.35,4.8,1.42),(.43,.23,.14),'green')
 source_patch(geo,ROOT/'source/room 022.png',(281,16,329,87),(.68,5.333,2.07),(1.05,1.55),'Anatomy_chart')
 # Examination table is low and walkable around, not through.
 b('Exam_table_top',(-.10,2.89,.89),(1.95,.84,.11),'white');b('Exam_table_pad',(-.10,2.89,.965),(1.65,.64,.035),'cyan')
 for x in [-.92,.72]:
  for y in [2.57,3.21]:b('Exam_table_leg',(x,y,.44),(.1,.1,.88),'black')
 b('Exam_lower_shelf',(-.1,2.89,.38),(1.65,.65,.08),'cyan')
 # Closed medicine cupboard with unmistakable red crosses.
 b('Medical_cupboard',(2.4,4.86,1.13),(1.07,.87,2.26),'brown')
 for x in [2.15,2.65]:
  b('Cupboard_door',(x,4.412,1.37),(.47,.06,1.65),'gray')
  b('Medicine_cross_vertical',(x,4.37,1.76),(.075,.018,.33),'red');b('Medicine_cross_horizontal',(x,4.37,1.76),(.27,.018,.075),'red')
  geo.sphere('Cupboard_knob',(x+(.14 if x<2.4 else -.14),4.35,.95),(.04,.03,.04),'black')
 # Static teaching skeleton, suspended from a stand. No character or animation.
 sx,sy=1.43,4.59
 b('Skeleton_stand_base',(sx,sy,.035),(.70,.52,.07),'black');geo.cyl('Skeleton_stand',(sx+.30,sy+.18,1.18),.025,2.3,'black')
 geo.beam('Skeleton_hanger',(sx+.30,sy+.18,2.32),(sx,sy,2.32),.025,'black')
 geo.sphere('Skeleton_skull',(sx,sy,2.11),(.14,.11,.18),'white')
 for dx in [-.057,.057]:geo.sphere('Skeleton_eye',(sx+dx,sy-.10,2.14),(.04,.025,.042),'black')
 b('Skeleton_jaw',(sx,sy-.012,1.95),(.16,.12,.055),'white')
 for z in [1.18+i*.066 for i in range(11)]:geo.sphere('Vertebra',(sx,sy,z),(.036,.035,.035),'white')
 for z,w in [(1.78,.22),(1.68,.24),(1.58,.22),(1.48,.18)]:
  curved_line(geo,'Skeleton_rib',[(sx+math.cos(a)*w,sy-.05-math.sin(a)*.085,z+.04*math.sin(a)) for a in [i*math.pi/12 for i in range(25)]],.025,'white')
 for side in [-1,1]:
  joints=[(sx,sy,1.81),(sx+side*.24,sy,1.80),(sx+side*.34,sy,1.4),(sx+side*.32,sy-.05,1.06)]
  curved_line(geo,'Arm_bones',joints,.038,'white')
  for j in range(4):geo.beam('Hand_bone',joints[-1],(sx+side*.32+j*.017,sy-.05,.96),.012,'white')
  geo.beam('Pelvis',(sx,sy,1.17),(sx+side*.13,sy,1.07),.075,'white')
  curved_line(geo,'Leg_bones',[(sx+side*.13,sy,1.07),(sx+side*.16,sy,.62),(sx+side*.14,sy,.15),(sx+side*.14,sy-.15,.10)],.045,'white')
 curved_line(geo,'Ceiling_plaster_crack',[(-2.7,5.33,3.09),(-2.5,5.33,2.95),(-2.68,5.33,2.83),(-2.29,5.33,2.71)],.03,'brown')
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_medical'
