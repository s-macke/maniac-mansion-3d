"""051 meteor chamber: riveted wall, parallel pipes, switch cabinet and suspended laboratory rig."""
import math,bpy
from pathlib import Path
from mathutils import Matrix
from blender_shared.lab_furniture import metal_wall,opposite_metal_wall,pipe,panel,gauge,cylinder,disc
from blender_shared.furnishings import curved_line,source_patch
from blender_shared.bedroom_furniture import finish

def furnish(g,c):
 b=g.box;half=c['geometry']['halfWidth'];metal_wall(g,half,5.1)
 for z,col in [(.47,'purple'),(.59,'purple'),(1.51,'red'),(1.65,'purple'),(1.79,'purple'),(2.54,'cyan')]:pipe(g,'Lab_wall_pipe',[(-half+.41,4.76,z),(half-.41,4.76,z)],.026,col,False)
 for x in [-3.63,-.63,1.62,4.71]:pipe(g,'Vertical_lab_pipe',[(x,4.71,.20),(x,4.71,3.10)],.052,'cyan')
 b('Switch_cabinet',(-2.55,4.36,.79),(1.20,.69,1.58),'cyan');b('Cabinet_gray_rim',(-2.55,3.994,.79),(1.06,.04,1.44),'gray');b('Cabinet_inset',(-2.55,3.965,.79),(.95,.02,1.31),'cyan')
 b('Lever_back',(-2.55,3.94,.96),(.36,.05,.42),'black')
 for dx in [-.14,.14]:b('Lever_bracket',(-2.55+dx,3.88,.99),(.045,.12,.36),'gray')
 cylinder(g,'Lever_axle',(-2.76,3.84,.85),(-2.34,3.84,.85),.05,'gray')
 g.beam('Lever_handle',(-2.55,3.84,.86),(-2.55,3.77,1.43),.065,'gray')
 for z in [1.30+i*.035 for i in range(5)]:b('Lever_grip_rib',(-2.55,3.765,z),(.10,.09,.015),'black')
 for xx in [-3.06,-2.04]:
  for zz in [.10,1.47]:b('Switch_case_bolt',(xx,3.94,zz),(.035,.02,.035),'aqua')
 for x in [-2.86+i*.105 for i in range(7)]:b('Cabinet_vent',(x,3.94,.23),(.032,.021,.14),'black')
 cylinder(g,'Inline_tank',(-.58,4.43,.55),(1.18,4.43,.55),.35,'cyan',28)
 for x in [-.48,-.29,.87,1.09]:cylinder(g,'Tank_band',(x-.025,4.43,.55),(x+.025,4.43,.55),.368,'green',28)
 pipe(g,'Tank_feed',[(-2.01,4.55,1.17),(.10,4.55,1.17),(.28,4.43,1.17),(.28,4.12,1.08),(.28,4.12,.67)],.055,'gray')
 b('Tank_feed_socket',(.28,4.075,.61),(.28,.13,.18),'gray')
 for x,side in [(-.58,-1),(1.18,1)]:
  cylinder(g,'Tank_end_cap',(x-side*.025,4.43,.55),(x+side*.08,4.43,.55),.30,'gray',24)
  cylinder(g,'Tank_end_pipe',(x,4.43,.55),(x+side*.25,4.43,.55),.085,'purple',20)
  for angle in range(6):
   a=angle*math.tau/6;g.sphere('Tank_flange_bolt',(x+side*.083,4.43+.25*math.cos(a),.55+.25*math.sin(a)),(.025,.025,.025),'aqua')
 # Source arrows point outward on either side of the central inlet.
 for x,side in [(-.12,-1),(.69,1)]:
  points=[(-.14,-.045),(.015,-.045),(.015,-.11),(.16,0),(.015,.11),(.015,.045),(-.14,.045)]
  g.mesh('Tank_red_direction_arrow',[(x+side*u,4.066,.58+v) for u,v in points],[tuple(range(len(points))) if side==1 else tuple(reversed(range(len(points))))],'red')
 pipe(g,'Tank_left_connection',[(-.83,4.43,.55),(-1.05,4.76,.55),(-half+.41,4.76,.55)],.032,'purple',False)
 pipe(g,'Tank_right_connection',[(1.43,4.43,.55),(1.63,4.76,.55),(half-.41,4.76,.55)],.032,'purple',False)
 b('Tank_wall_termination',(half-.36,4.82,.55),(.20,.18,.32),'gray')
 # Hanging apparatus, supported from ceiling pipework.
 x,y=3.47,4.38
 pipe(g,'Rig_supply',[(x+.10,y,2.70),(x+.53,y,2.70),(x+.73,y,3.10)],.070,'black')
 for z,r,col in [(2.71,.16,'cyan'),(2.49,.095,'gray'),(2.30,.20,'black')]:g.cyl('Rig_neck',(x,y,z),r,.19,col,20)
 gauge(g,x-.32,y-.16,2.58,.13)
 pipe(g,'Rig_red_feed',[(x,y,2.80),(x,y,3.12)],.045,'red',False)
 for i in range(7):g.cyl('Rig_feed_rib',(x,y,2.83+i*.04),.057,.012,'pink',16)
 for side in [-1,1]:
  g.beam('Rig_antenna',(x+side*.10,y,2.75),(x+side*.25,y,2.96),.018,'gray')
  g.sphere('Rig_green_tip',(x+side*.25,y,2.96),(.055,.055,.055),'lime')
 for zz in [2.39,2.44,2.49]:g.cyl('Rig_neck_rib',(x,y,zz),.145,.018,'black',24)
 vs=[(x+r*math.cos(i*math.tau/20),y+r*math.sin(i*math.tau/20),z) for r,z in [(.43,2.09),(.14,2.31)] for i in range(20)]
 g.mesh('Rig_bell',vs,[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],'gray');g.cyl('Rig_probe',(x,y,1.95),.045,.24,'pink')
 g.cyl('Rig_bell_rim',(x,y,2.09),.45,.065,'white',32)
 for i in range(20):
  a=i*math.tau/20;g.sphere('Bell_rim_perforation',(x+.452*math.cos(a),y+.452*math.sin(a),2.09),(.018,.018,.013),'black')
 for s in [-1,1]:
  curved_line(g,'Rig_pincer',[(x+s*.38,y,2.42),(x+s*.64,y,2.05),(x+s*.39,y,1.79)],.04,'gray')
  for xx,zz in [(x+s*.38,2.42),(x+s*.64,2.05)]:disc(g,'Pincer_joint',xx,y-.03,zz,.064,'aqua')
  for dz in [-.035,.035]:g.beam('Pincer_finger',(x+s*.39,y,1.79),(x+s*.29,y,1.79+dz),.023,'gray')
  b('Red_terminal',(x+s*.68,4.7,1.24),(.24,.20,.12),'lightred')
  for i in range(4):b('Terminal_contact',(x+s*(.52-i*.06),4.7,1.24),(.013,.12,.12),'gray')
  pipe(g,'Terminal_supply',[(x+s*.68,4.7,1.24),(x+s*.82,4.7,1.24),(x+s*.82,4.7,3.11)],.045,'cyan',False)
 # The right terminal sits on a ribbed guide between cyan collars.
 for zz in [1.59+i*.05 for i in range(12)]:
  g.cyl('Rig_side_guide_rib',(x+.82,4.7,zz),.071,.018,'gray',16)
 for zz in [1.55,2.18]:b('Rig_guide_collar',(x+.82,4.7,zz),(.35,.19,.055),'aqua')
 # Preserve the irregular purple spill, pink flecks and detached droplets.
 before=set(bpy.data.objects)
 source_patch(g,Path(__file__).resolve().parents[2]/'source/room 051.png',(311,109,361,124),(0,0,0),(1.24,.38),'Original_floor_spill',only={'purple','pink'})
 bpy.context.view_layer.update()
 transform=Matrix.Translation((2.65,1.08,.005))@Matrix.Rotation(-math.pi/2,4,'X')
 for obj in set(bpy.data.objects)-before:obj.matrix_world=transform@obj.matrix_world
 opposite_metal_wall(g,c['geometry']['halfWidth'],c['geometry']['depth'],c['geometry']['height'])
 finish(c)
