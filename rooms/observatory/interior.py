"""028: solid telescope aligned with the open dome slit, controls and star chart."""
from pathlib import Path
import math,bpy
from mathutils import Vector,Matrix
from blender_shared.furnishings import source_patch,curved_line
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 a=Vector((.58,5.30,1.98));end=Vector((3.08,7.39,3.50));axis=(end-a).normalized()
 def tube(name,center,r,length,color):
  o=g.cyl(name,(0,0,0),r,length,color,40);o.rotation_euler=axis.to_track_quat('Z','Y').to_euler();o.location=center;return o
 # Stepped cylindrical optical tube with a dark open lens and rim.
 tube('Telescope_main_tube',(a+end)/2,.36,(end-a).length,'gray')
 tube('Telescope_white_barrel',a+(end-a)*.68,.367,(end-a).length*.60,'white')
 tube('Telescope_rear_housing',a+axis*.35,.27,.75,'white')
 tube('Telescope_mid_collar',a+(end-a)*.43,.387,.17,'darkgray')
 tube('Telescope_front_rim',end,.388,.13,'gray')
 tube('Telescope_lens',end+axis*.072,.327,.012,'black')
 tube('Lens_blue_glass',end+axis*.079,.28,.008,'blue')
 tube('Eyepiece_tube',a-axis*.24,.07,.55,'gray');tube('Eyepiece_black_rim',a-axis*.53,.08,.08,'black')
 # Two off-axis focus controls are visible below the eyepiece in background 028.
 side=Vector((axis.y,-axis.x,0)).normalized()
 p=a+side*.23-Vector((0,0,.13))
 g.beam('Red_focus_stem',p,p-axis*.43,.035,'gray')
 g.sphere('Red_focus_grip',p-axis*.46,(.062,.062,.062),'red')
 p=a+side*.20-Vector((0,0,.26))
 curved_line(g,'Bent_focus_crank',[p,p-Vector((0,0,.20)),p+side*.12-Vector((0,0,.27))],.034,'gray')
 # Fork, round pivot and broad stable pedestal.
 x,y=1.55,6.14
 g.cyl('Telescope_foot',(x,y,.10),.58,.20,'black',32);g.cyl('Telescope_column',(x,y,.84),.24,1.42,'black',24)
 g.cyl('Mount_plate',(x,y,1.60),.48,.12,'darkgray',32)
 for dx in [-.34,.34]:g.beam('Mount_fork',(x+dx,y,1.65),(x+dx,y,2.47),.13,'black')
 pivot=g.cyl('Altitude_pivot',(0,0,0),.25,.82,'black',32);pivot.rotation_euler.y=math.pi/2;pivot.location=(x,y,2.20)
 for r,xx,col in [(.17,x-.43,'gray'),(.11,x-.448,'aqua'),(.065,x-.461,'black')]:
  o=g.cyl('Pivot_dial',(0,0,0),r,.015,col,24);o.rotation_euler.y=math.pi/2;o.location=(xx,y,2.20)
 for z,col in [(1.04,'lime'),(.79,'red')]:
  g.beam('Pedestal_control',(x-.20,y-.12,z),(x-.48,y-.12,z),.035,'gray');g.sphere('Control_knob',(x-.50,y-.12,z),(.065,.065,.065),col)
 # Red and blue finder fittings, plus the curved purple drive cable seen in the original.
 for t,col in [(.22,'lightblue'),(.64,'black'),(.86,'black')]:
  p=a+(end-a)*t;g.sphere('Barrel_fitting',(p.x-.12,p.y-.21,p.z+.27),(.055,.055,.055),col)
 curved_line(g,'Telescope_drive_cable',[(1.46,6.40,2.56),(.89,6.47,2.91),(.62,6.47,3.43),(.62,6.47,4.32)],.070,'purple')
 # Standalone control box and pipes remain away from the den hatch and landing.
 x,y=-3.10,5.62
 b('Observatory_control_box',(x,y,1.14),(.78,.36,1.06),'black')
 for xx in [x-.26,x+.26]:g.beam('Control_box_leg',(xx,y,.035),(xx,y,.65),.046,'gray')
 for xx in [x-.22,x+.05,x+.22]:
  for z in [1.28,1.48]:b('Red_control_light',(xx,y-.193,z),(.045,.023,.045),'lightred')
 b('Control_meter',(x-.15,y-.197,.94),(.22,.025,.17),'gray');b('Meter_glass',(x-.15,y-.216,.94),(.15,.012,.09),'white')
 for xx in [x+.12,x+.27]:b('Control_switch',(xx,y-.219,.84),(.035,.028,.10),'gray')
 curved_line(g,'Control_pipe',[(x+.27,y,.1),(x+.27,y,2.27),(x+.14,y,2.50),(x-.27,y,2.50)],.067,'gray')
 # The original pipe ends in a broad vertical dish with a pale rim and hub.
 for r,yy,col in [(.26,y,'gray'),(.219,y-.025,'black')]:
  dish=g.cyl('Control_pipe_dish',(0,0,0),r,.025,col,32)
  dish.rotation_euler.x=math.pi/2;dish.location=(x-.29,yy,2.50)
 g.beam('Dish_feed_arm',(x-.29,y-.06,2.50),(x-.29,y-.22,2.50),.048,'gray')
 g.sphere('Dish_feed_hub',(x-.29,y-.23,2.50),(.052,.042,.052),'white')
 # Original chart lies tangent to the round wall, below its dome spring line.
 before=set(bpy.data.objects)
 b('Chart_backing',(0,0,1.28),(1.34,.025,1.02),'lightblue')
 source_patch(g,ROOT/'source/room 028.png',(47,56,108,97),(0,-.025,1.28),(1.28,.93),'Original_star_chart')
 bpy.context.view_layer.update();angle=2.0;transform=Matrix.Translation((4.02*math.cos(angle),4.2+4.02*math.sin(angle),0))@Matrix.Rotation(angle-math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=transform@o.matrix_world
 # Hanging metal lamp near the chart; lighting remains baked.
 g.cyl('Dome_lamp_cord',(-.8,5.95,4.13),.013,.80,'black')
 verts=[(-.8+r*math.cos(i*math.tau/20),5.95+r*math.sin(i*math.tau/20),z) for r,z in [(.27,3.59),(.06,3.74)] for i in range(20)]
 g.mesh('Dome_lamp_shade',verts,[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],'gray')
 o=g.cyl('Dome_lamp_bulb',(-.8,5.95,3.60),.09,.035,'white',16);o['bake_unlit']=True;o['bake_no_shadow']=True
