"""015: original broken plaster and exposed laths, boarded window and loose wires."""
from blender_shared.placement import rear_anchored
from pathlib import Path
import bpy,math
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.2)
def furnish(g,c):
 b=g.box
 # The original jagged silhouettes form separate depth layers, exposing timber below plaster.
 for colors,y,label in [({'brown','red'},4.97,'Exposed_laths'),({'black','blue'},4.95,'Cracks_and_wire_marks'),({'darkgray'},4.934,'Damaged_gray_plaster'),({'cyan'},4.90,'Ragged_cyan_plaster'),({'lime'},4.889,'Damp_streaks')]:
  before=set(bpy.data.objects)
  source_patch(g,ROOT/'source/room 015.png',(40,0,280,101),(0,y,1.58),(8.16,2.99),label,only=colors)
  for o in set(bpy.data.objects)-before:o['bake_unlit']=False
 # Solid boards cross the black window recess at alternating angles.
 b('Window_recess',(2.22,4.99,2.06),(1.76,.035,1.92),'black')
 for i,(z,angle) in enumerate([(1.25,.15),(1.48,-.18),(1.78,.15),(2.05,-.13),(2.30,.06),(2.56,-.12),(2.78,.13)]):
  o=b('Window_board',(2.22,4.81-i*.005,z),(1.86,.065,.20),'yellow');o.rotation_euler.y=angle
  for x in [1.41,3.02]:b('Board_nail',(x,4.765-i*.005,z-(x-2.22)*math.sin(angle)),(.024,.016,.032),'red')
 # Actual projecting wire ends at the left broken-plaster opening.
 for dx,col in [(0,'red'),(.10,'blue')]:
  curved_line(g,'Exposed_loose_wire',[(-2.86+dx,4.83,1.40),(-2.70+dx,4.75,1.41),(-2.62+dx,4.72,1.20),(-2.76+dx,4.68,1.09)],.027,col)
  g.beam('Bare_wire_end',(-2.76+dx,4.68,1.09),(-2.76+dx,4.68,1.00),.014,'yellow')
 # Hanging fitting and cable, and a few physical rafter edges at the roof line.
 curved_line(g,'Attic_cable',[(-1.53,4.36,3.10),(-1.53,4.36,2.83),(-1.72,4.34,2.65)],.024,'black')
 b('Crooked_light_shade',(-1.71,4.34,2.66),(.39,.20,.055),'blue');g.cyl('Exposed_bulb',(-1.71,4.34,2.50),.048,.19,'white')
 for x in [-3.93,3.93]:g.beam('Roof_edge',(x,5.2-c['geometry']['depth']+.3,3.035),(x,4.92,3.035),.075,'darkgray')
 finish(c)
