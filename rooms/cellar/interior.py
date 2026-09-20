"""008: furnace, pressure vessels, ducts, pipework and electrical box."""
from pathlib import Path
import math,bpy
from mathutils import Matrix
from blender_shared.lab_furniture import pipe,cylinder,gauge,wheel
from blender_shared.furnishings import source_patch
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 # Source gray walls and dark structural seams behind the pipework.
 for x in [-7.4,-5.3,-2.4,.2,2.8,4.95]:b('Cellar_wall_seam',(x,5.905,1.56),(.017,.018,3.12),'black')
 for z in [.35,1.05]:b('Cellar_wall_course',(-1.0,5.897,z),(12.0,.015,.025),'black')
 pipe(g,'Large_duct',[(-5.65,5.62,.14),(-5.65,5.62,3.12)],.23,'cyan',False)
 pipe(g,'Cross_duct',[(-5.65,5.62,2.48),(-.65,5.62,2.48),(-.65,5.62,1.77),(1.45,5.62,1.77)],.22,'cyan',False)
 for z in [.25+i*.24 for i in range(12)]:cylinder(g,'Duct_band',(-5.65,5.62,z-.018),(-5.65,5.62,z+.018),.242,'black')
 for x in [-5.35+i*.27 for i in range(18)]:cylinder(g,'Duct_band',(x-.018,5.62,2.48),(x+.018,5.62,2.48),.234,'black')
 for x in [-4.75,-3.58,-2.94]:pipe(g,'Slender_copper_pipe',[(x,5.73,3.1),(x,5.73,1.00),(x+.42,5.73,.83)],.064,'cyan')
 pipe(g,'Red_hot_pipe',[(-3.55,5.62,.47),(.24,5.62,.47),(.24,5.62,1.61)],.068,'red')
 for i in range(34):b('Hot_pipe_rib',(-3.4+i*.1,5.54,.47),(.022,.14,.17),'yellow')
 # Three ribbed gray return pipes visible behind the cyan risers in 008.
 for z in [.87,1.13,1.39]:
  cylinder(g,'Return_pipe',(-4.98,5.79,z),(.74,5.79,z),.073,'gray')
  for i in range(48):
   x=-4.94+i*.12;cylinder(g,'Return_pipe_rib',(x-.016,5.79,z),(x+.016,5.79,z),.095,'darkgray')
 machine_before=set(bpy.data.objects)
 # Blue furnace housing, vented cooler and red pressure dome.
 b('Furnace_body',(2.54,4.86,.80),(1.75,1.20,1.60),'blue');b('Furnace_firebox',(2.54,4.234,.47),(1.40,.065,.70),'lightblue')
 b('Firebox_dark_border',(2.54,4.192,.47),(1.27,.025,.57),'blue');b('Firebox_face',(2.54,4.17,.47),(1.15,.023,.48),'lightblue')
 wheel(g,2.79,4.115,.47,.12,'blue')
 g.cyl('Red_boiler',(2.55,4.90,1.71),.56,.61,'red',32);g.sphere('Boiler_dome',(2.55,4.90,2.02),(.56,.56,.41),'red')
 for z in [1.53,1.78,2.04]:g.cyl('Boiler_rim',(2.55,4.90,z),.565,.043,'lightred',32)
 b('Boiler_blue_band',(2.55,4.27,1.60),(1.33,.16,.35),'blue')
 source_patch(g,ROOT/'source/room 008.png',(472,60,486,77),(2.55,4.173,1.60),(.25,.30),'Original_boiler_warning')
 pipe(g,'Boiler_chimney',[(2.55,4.90,2.35),(2.55,4.90,3.12)],.13,'black')
 b('Furnace_tower',(1.46,4.91,1.4),(.47,.77,2.4),'blue')
 for x in [1.34,1.59]:gauge(g,x,4.494,2.00,.083)
 pipe(g,'Exhaust_stack',[(1.46,4.91,2.48),(1.46,4.91,3.12)],.19,'gray')
 b('Cooler_case',(.30,4.85,.51),(1.21,1.14,1.02),'blue');b('Cooler_grille',(.30,4.25,.51),(1.0,.045,.78),'black')
 for x in [-.12+i*.14 for i in range(7)]:b('Cooler_vertical_bar',(x,4.217,.51),(.025,.02,.78),'aqua')
 for z in [.17+i*.12 for i in range(6)]:b('Cooler_horizontal_bar',(.30,4.20,z),(1.0,.018,.025),'lightblue')
 g.cyl('Extinguisher',(1.25,4.22,1.14),.13,.69,'red',20);g.sphere('Extinguisher_top',(1.25,4.22,1.49),(.13,.13,.13),'red')
 pipe(g,'Extinguisher_hose',[(1.25,4.23,1.57),(1.05,4.14,1.70),(.93,4.16,1.40)],.025,'cyan',False)
 pipe(g,'Boiler_outlet',[(3.2,5.08,1.62),(4.42,5.08,1.62),(4.42,5.65,2.11)],.055,'cyan')
 bpy.context.view_layer.update()
 machine_transform=Matrix.Translation((1.5,0,0))@Matrix.Diagonal((1.25,1,1,1))@Matrix.Translation((-1.5,0,0))
 for o in set(bpy.data.objects)-machine_before:o.matrix_world=machine_transform@o.matrix_world
 # Small electrical cabinet on the left wall, clear of the dungeon door.
 before=set(bpy.data.objects)
 b('Electrical_box',(0,0,1.44),(.80,.13,1.05),'blue');b('Electrical_box_trim',(0,-.079,1.44),(.73,.025,.98),'gray');b('Electrical_panel',(0,-.1,1.44),(.63,.025,.86),'lightblue')
 b('Panel_handle',(.20,-.14,1.40),(.04,.05,.22),'aqua')
 bpy.context.view_layer.update();m=Matrix.Translation((-7.94,4.40,0))@Matrix.Rotation(math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=m@o.matrix_world
 # Flat green stain, with no movement or gameplay effect.
 g.mesh('Cellar_floor_stain',[(-3.1,1.10,.004),(-2.45,.94,.004),(-2.02,1.11,.004),(-2.2,1.30,.004),(-2.90,1.34,.004)],[(0,1,2,3,4)],'lime')
 finish(c)
