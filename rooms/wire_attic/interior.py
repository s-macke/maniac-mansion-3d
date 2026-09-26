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
  if label=='Cracks_and_wire_marks':
   # The lamp and pull cord are solid objects now; omit their old flat silhouette.
   for crop in [(40,0,98,101),(124,0,280,101),(98,37,124,101)]:
    xa,ya,xb,yb=crop
    center=((((xa+xb)/2-40)/240-.5)*8.16,y,1.58+(.5-(ya+yb)/202)*2.99)
    source_patch(g,ROOT/'source/room 015.png',crop,center,((xb-xa)/240*8.16,(yb-ya)/101*2.99),label,only=colors)
  else:
   source_patch(g,ROOT/'source/room 015.png',(40,0,280,101),(0,y,1.58),(8.16,2.99),label,only=colors)
  for o in set(bpy.data.objects)-before:o['bake_unlit']=False
 # Restore the gray plaster behind the removed flat ceiling-wire pixels.
 b('Old_wire_plaster_fill',(-1.70,4.956,2.87),(.17,.003,.42),'darkgray')
 # Solid boards cross the black window recess at alternating angles.
 b('Window_recess',(2.22,4.99,2.06),(1.76,.035,1.92),'black')
 # Irregular crossed boards, with varied lengths and chipped ends.
 for i,(x,z,w,angle) in enumerate([(2.18,2.80,1.44,-.24),(2.17,2.55,1.75,.27),(2.29,2.29,1.86,-.05),(2.18,2.03,1.66,.32),(2.13,1.71,1.80,-.19),(2.30,1.43,1.36,-.28)]):
  profile=[(-w/2,-.10),(-w/2+.035,.08),(-w/2+.12,.12),(w/2-.08,.105),(w/2,.07),(w/2-.02,-.08),(w/2-.16,-.105)]
  n=len(profile);vs=[(xx,yy,zz) for yy in [-.0325,.0325] for xx,zz in profile]
  o=g.mesh('Window_board',vs,[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],'yellow');o.location=(x,4.81-i*.014,z);o.rotation_euler.y=angle
  for dx in [-w*.40,w*.40]:
   b('Board_nail',(x+dx*math.cos(angle),4.773-i*.014,z-dx*math.sin(angle)),(.024,.006,.032),'red')
 # The black floor outline is scenery; its destination is deliberately unspecified.
 with_floor_y=5.2-c['geometry']['depth']
 curved_line(g,'Attic_floor_outline',[(-.65,with_floor_y+1.40,.006),(.65,with_floor_y+1.40,.006),(.44,with_floor_y+1.96,.006),(-.44,with_floor_y+1.96,.006),(-.65,with_floor_y+1.40,.006)],.018,'black')
 # Actual projecting wire ends at the left broken-plaster opening.
 for dx,col in [(0,'red'),(.10,'blue')]:
  curved_line(g,'Exposed_loose_wire',[(-2.86+dx,4.83,1.40),(-2.70+dx,4.75,1.41),(-2.62+dx,4.72,1.20),(-2.76+dx,4.68,1.09)],.027,col)
  g.beam('Bare_wire_end',(-2.76+dx,4.68,1.09),(-2.76+dx,4.68,1.00),.014,'yellow')
 curved_line(g,'Lamp_pull_cord',[(-1.48,4.30,2.64),(-1.48,4.30,2.10)],.008,'black')
 b('Lamp_pull_end',(-1.48,4.30,2.08),(.06,.025,.025),'black')
 # Hanging fitting and cable, and a few physical rafter edges at the roof line.
 curved_line(g,'Attic_cable',[(-1.53,4.36,3.10),(-1.53,4.36,2.83),(-1.72,4.34,2.65)],.024,'black')
 o=b('Crooked_light_shade',(-1.71,4.34,2.66),(.48,.20,.035),'blue');o.rotation_euler.y=-.32;
 g.cyl('Bulb_socket',(-1.71,4.34,2.60),.062,.11,'black');g.cyl('Exposed_bulb',(-1.71,4.34,2.50),.048,.19,'white')
 for o in bpy.data.objects:
  if o.name.startswith('Exposed_bulb'):o['bake_unlit']=True;o['bake_no_shadow']=True
 for x in [-3.93,3.93]:g.beam('Roof_edge',(x,5.2-c['geometry']['depth']+.3,3.035),(x,4.92,3.035),.075,'darkgray')
 finish(c)
