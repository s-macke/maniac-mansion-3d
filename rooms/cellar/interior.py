"""008: furnace, pressure vessels, ducts, pipework and electrical box."""
from pathlib import Path
import math,bpy
from mathutils import Matrix,Vector
from blender_shared.lab_furniture import pipe,cylinder,gauge,disc
from blender_shared.furnishings import curved_line
from blender_shared.furnishings import source_patch
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 # The original stairs are gray with dark risers, not wooden steps.
 for o in bpy.data.objects:
  if o.type=='MESH' and o.name.startswith(('Stair_tread','Stair_edge','Stair_rail')):
   o.data.materials.clear();o.data.materials.append(g.mats['gray' if o.name.startswith('Stair_edge') else 'darkgray'])
 # Source gray walls and dark structural seams behind the pipework.
 for x in [-7.4,-5.3,-2.4,.2,2.8,4.95]:b('Cellar_wall_seam',(x,5.905,1.56),(.017,.018,3.12),'black')
 for z in [.35,1.05]:b('Cellar_wall_course',(-1.0,5.897,z),(12.0,.015,.025),'black')
 pipe(g,'Large_duct',[(-5.65,5.62,.14),(-5.65,5.62,3.12)],.23,'cyan',False)
 pipe(g,'Cross_duct',[(-5.65,5.62,2.48),(-.90,5.62,2.48)],.22,'cyan',False)
 cylinder(g,'Duct_flange',(-5.42,5.62,2.48),(-5.29,5.62,2.48),.32,'blue')
 # Separate ceiling riser curves through the red wrapped elbow into the furnace.
 elbow=[(-.63,5.26,3.12),(-.63,5.26,2.51),(-.54,5.26,2.23),(-.32,5.26,2.00),(.03,5.26,1.89),(.55,5.26,1.89)]
 pipe(g,'Furnace_intake',elbow,.23,'cyan',False)
 for z in [2.58,2.80,3.02]:cylinder(g,'Intake_rib',(-.63,5.26,z-.018),(-.63,5.26,z+.018),.24,'black')
 for a,bp in [(elbow[2],elbow[3]),(elbow[3],elbow[4])]:
  cylinder(g,'Red_elbow_wrap',a,bp,.255,'lightred')
  cylinder(g,'Red_elbow_seam',a,tuple(a[i]+(bp[i]-a[i])*.12 for i in range(3)),.264,'red')
 for z in [.25+i*.24 for i in range(12)]:cylinder(g,'Duct_band',(-5.65,5.62,z-.018),(-5.65,5.62,z+.018),.242,'black')
 for x in [-5.35+i*.27 for i in range(18)]:cylinder(g,'Duct_band',(x-.018,5.62,2.48),(x+.018,5.62,2.48),.234,'black')
 for x in [-3.58,-2.94]:pipe(g,'Slender_copper_pipe',[(x,5.73,3.1),(x,5.73,.70),(x+.20,5.62,.47),(-2.52,5.62,.47)],.085,'cyan')
 pipe(g,'Leaking_riser',[(-4.75,5.73,3.12),(-4.75,5.73,.85)],.10,'cyan',False)
 for dx,z in [(-.035,.89),(.025,.82),(0,.72)]:g.sphere('Riser_green_drip',(-4.75+dx,5.64,z),(.024,.021,.057),'lime')
 pipe(g,'Rear_valve_pipe',[(-1.9,5.73,3.12),(-1.9,5.73,1.15),(-.95,5.73,1.15)],.068,'cyan')
 pipe(g,'Small_valve_branch',[(-1.9,5.73,1.66),(-1.53,5.73,1.66)],.045,'cyan',False)
 gauge(g,-1.49,5.66,1.67,.09)
 pipe(g,'Red_hot_pipe',[(-2.52,5.62,.47),(.24,5.62,.47),(.24,5.62,1.78),(.24,5.10,1.78)],.068,'red')
 for i in range(27):b('Hot_pipe_rib',(-2.46+i*.1,5.54,.47),(.022,.14,.17),'lightred')
 # One ribbed return behind the risers; the older version invented three.
 for z in [1.19]:
  cylinder(g,'Return_pipe',(-4.98,5.79,z),(.74,5.79,z),.073,'gray')
  for i in range(48):
   x=-4.94+i*.12;cylinder(g,'Return_pipe_rib',(x-.016,5.79,z),(x+.016,5.79,z),.095,'darkgray')
 machine_before=set(bpy.data.objects)
 # Blue furnace housing, vented cooler and red pressure dome.
 b('Furnace_body',(2.54,4.86,.80),(1.75,1.20,1.60),'blue');b('Furnace_firebox',(2.54,4.234,.47),(1.40,.065,.70),'lightblue')
 b('Firebox_dark_border',(2.54,4.192,.47),(1.27,.025,.57),'blue');b('Firebox_face',(2.54,4.17,.47),(1.15,.023,.48),'lightblue')
 disc(g,'Firebox_latch',2.73,4.12,.47,.085,'blue',.05)
 b('Firebox_latch_handle',(2.93,4.095,.47),(.34,.055,.055),'blue')
 for x in [2.05,3.03]:
  for z in [.29,.65]:b('Firebox_bolt',(x,4.143,z),(.033,.015,.033),'aqua')
 g.cyl('Red_boiler',(2.55,4.90,1.71),.56,.61,'red',32);g.sphere('Boiler_dome',(2.55,4.90,2.02),(.56,.56,.41),'red')
 for z in [1.53,1.78,2.04]:g.cyl('Boiler_rim',(2.55,4.90,z),.565,.043,'lightred',32)
 b('Boiler_blue_band',(2.55,4.27,1.60),(1.33,.16,.35),'blue')
 source_patch(g,ROOT/'source/room 008.png',(472,60,486,77),(2.55,4.173,1.60),(.25,.30),'Original_boiler_warning')
 # Yellow flared cap between the red dome and black ribbed chimney (008).
 g.cyl('Boiler_cap_neck',(2.55,4.90,2.435),.18,.09,'black',24)
 cap_vertices=[(2.55+r*math.cos(i*math.tau/24),4.90+r*math.sin(i*math.tau/24),z) for r,z in [(.30,2.47),(.18,2.62)] for i in range(24)]
 cap_faces=[(i,(i+1)%24,(i+1)%24+24,i+24) for i in range(24)]+[tuple(range(23,-1,-1)),tuple(range(24,48))]
 g.mesh('Boiler_yellow_cap',cap_vertices,cap_faces,'yellow')
 pipe(g,'Boiler_chimney',[(2.55,4.90,2.35),(2.55,4.90,3.12)],.13,'black')
 for z in [2.67+i*.065 for i in range(7)]:g.cyl('Chimney_rib',(2.55,4.90,z),.16,.022,'gray',24)
 b('Furnace_tower',(1.46,4.91,1.4),(.47,.77,2.4),'blue')
 for x in [1.34,1.59]:gauge(g,x,4.494,2.00,.083)
 pipe(g,'Exhaust_stack',[(1.46,4.91,2.48),(1.46,4.91,3.12)],.19,'black')
 for z in [2.56,2.61,2.66]:g.cyl('Exhaust_flange',(1.46,4.91,z),.265,.032,'darkgray',24)
 for x in [.70,1.02]:
  pipe(g,'Narrow_furnace_riser',[(x,5.05,2.05),(x,5.05,3.12)],.065,'black',False)
  pipe(g,'Riser_edge',[(x-.04,4.993,2.05),(x-.04,4.993,3.12)],.013,'aqua',False)
 b('Intake_blue_manifold',(.94,4.98,1.88),(1.08,.60,.38),'blue')
 b('Manifold_highlight',(.94,4.663,2.04),(.98,.025,.035),'lightblue')
 b('Cooler_case',(.30,4.85,.51),(1.21,1.14,1.02),'blue');b('Cooler_grille',(.30,4.25,.51),(1.0,.045,.78),'black')
 for x in [-.12+i*.14 for i in range(7)]:b('Cooler_vertical_bar',(x,4.217,.51),(.025,.02,.78),'aqua')
 for z in [.17+i*.12 for i in range(6)]:b('Cooler_horizontal_bar',(.30,4.20,z),(1.0,.018,.025),'lightblue')
 for x in [-.23,.30,.83]:
  for z in [.10,.92]:b('Cooler_corner_bolt',(x,4.19,z),(.05,.025,.04),'aqua')
 g.cyl('Extinguisher',(1.25,4.22,1.14),.13,.69,'red',20);g.sphere('Extinguisher_top',(1.25,4.22,1.49),(.13,.13,.13),'red')
 pipe(g,'Extinguisher_hose',[(1.25,4.23,1.57),(1.05,4.14,1.70),(.93,4.16,1.40)],.025,'cyan',False)
 for z in [.84,1.42]:g.cyl('Extinguisher_band',(1.25,4.22,z),.137,.035,'lightred',20)
 b('Extinguisher_label',(1.25,4.078,1.23),(.075,.014,.12),'yellow')
 # Flexible outlet ends at a bolted blue wall flange.
 hose=[(3.20,5.08,1.62),(3.65,5.10,1.64),(3.92,5.16,1.78),(4.03,5.26,2.02),(4.20,5.48,2.13),(4.43,5.90,2.13)]
 pipe(g,'Boiler_outlet',hose,.065,'cyan',False)
 for a,bp in zip(hose,hose[1:]):
  va,vb=Vector(a),Vector(bp);axis=(vb-va).normalized()
  for i in range(5):
   q=va+(vb-va)*(i+.5)/5;cylinder(g,'Outlet_rib',q-axis*.012,q+axis*.012,.079,'aqua',12)
 disc(g,'Outlet_wall_flange',4.43,5.88,2.13,.19,'blue',.10)
 for dx,dz in [(-.12,0),(.12,0),(0,.12),(0,-.12)]:b('Outlet_flange_bolt',(4.43+dx,5.823,2.13+dz),(.035,.025,.035),'aqua')
 bpy.context.view_layer.update()
 machine_transform=Matrix.Translation((1.5,0,0))@Matrix.Diagonal((1.25,1,1,1))@Matrix.Translation((-1.5,0,0))
 for o in set(bpy.data.objects)-machine_before:o.matrix_world=machine_transform@o.matrix_world
 # Small electrical cabinet on the left wall, clear of the dungeon door.
 before=set(bpy.data.objects)
 b('Electrical_box',(0,0,1.44),(.80,.13,1.05),'blue');b('Electrical_box_trim',(0,-.079,1.44),(.73,.025,.98),'aqua');b('Electrical_panel',(0,-.1,1.44),(.63,.025,.86),'blue')
 g.mesh('Panel_warning', [(-.13,-.119,1.80),(.13,-.119,1.80),(0,-.119,1.65)],[(0,1,2)],'yellow')
 for x in [-.33,.33]:
  for z in [1.0,1.88]:b('Panel_screw',(x,-.119,z),(.035,.015,.035),'aqua')
 curved_line(g,'Hanging_key_ring',[(.55+.055*math.cos(i*math.tau/16),-.02,1.68+.045*math.sin(i*math.tau/16)) for i in range(17)],.015,'aqua')
 b('Hanging_key_shaft',(.55,-.02,1.53),(.028,.025,.24),'aqua')
 for z in [1.43,1.49]:b('Hanging_key_tooth',(.58,-.02,z),(.06,.025,.025),'aqua')
 b('Panel_handle',(.20,-.14,1.40),(.04,.05,.22),'aqua')
 bpy.context.view_layer.update();m=Matrix.Translation((-7.94,4.40,0))@Matrix.Rotation(math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=m@o.matrix_world
 # Flat green stain, with no movement or gameplay effect.
 before=set(bpy.data.objects)
 source_patch(g,ROOT/'source/room 008.png',(140,117,190,128),(0,0,0),(1.33,.29),'Original_green_spill',only={'lime'})
 for o in set(bpy.data.objects)-before:o.matrix_world=Matrix.Translation((-4.72,4.73,.008))@Matrix.Rotation(-math.pi/2,4,'X')
 finish(c)
