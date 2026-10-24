"""015: original broken plaster and exposed laths, boarded window and loose wires."""
from blender_shared.placement import rear_anchored
from pathlib import Path
import bpy,math
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import finish
from blender_shared.windows import cut_wall,outside_window
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.2)
def furnish(g,c):
 b=g.box
 # Pixel-aligned opening through both the shell and all flat damage layers.
 hole=(199,2,251,67)
 def artwork(crop,y,label,colors):
  xa,ya,xb,yb=crop;hx0,hy0,hx1,hy1=hole
  xs=sorted(set([xa,xb,max(xa,min(xb,hx0)),max(xa,min(xb,hx1))]))
  ys=sorted(set([ya,yb,max(ya,min(yb,hy0)),max(ya,min(yb,hy1))]))
  for a,bb in zip(xs,xs[1:]):
   for low,high in zip(ys,ys[1:]):
    if hx0<(a+bb)/2<hx1 and hy0<(low+high)/2<hy1:continue
    center=((((a+bb)/2-40)/240-.5)*8.16,y,1.58+(.5-(low+high)/202)*2.99)
    source_patch(g,ROOT/'source/room 015.png',(a,low,bb,high),center,((bb-a)/240*8.16,(high-low)/101*2.99),label,only=colors)
 # The original jagged silhouettes form separate depth layers, exposing timber below plaster.
 for colors,y,label in [({'brown','red'},4.97,'Exposed_laths'),({'black','blue'},4.95,'Cracks_and_wire_marks'),({'darkgray'},4.934,'Damaged_gray_plaster'),({'cyan'},4.90,'Ragged_cyan_plaster'),({'lime'},4.889,'Damp_streaks')]:
  before=set(bpy.data.objects)
  if label=='Cracks_and_wire_marks':
   # The lamp and pull cord are solid objects now; omit their old flat silhouette.
   for crop in [(40,0,98,101),(124,0,280,101),(98,37,124,101)]:
    artwork(crop,y,label,colors)
  else:
   artwork((40,0,280,101),y,label,colors)
  for o in set(bpy.data.objects)-before:o['bake_unlit']=False
 # Restore the gray plaster behind the removed flat ceiling-wire pixels.
 b('Old_wire_plaster_fill',(-1.70,4.956,2.87),(.17,.003,.42),'darkgray')
 x0=(hole[0]-160)*8.16/240;x1=(hole[2]-160)*8.16/240
 top=1.58+(.5-hole[1]/101)*2.99;bottom=1.58+(.5-hole[3]/101)*2.99
 cut_wall(g,'Wall_back',[(x0,x1,bottom,top)],author_offset_y=5.2-c['geometry']['depth'])
 outside_window(g,'Attic_window',((x0+x1)/2,4.90,(bottom+top)/2),(0,1),x1-x0,top-bottom,sky='black',frame='darkgray',columns=1,rows=1,seed=15)
 # Preserve the three white source stars as solid distant pixel squares.
 # Project from a central review viewpoint through their original image positions;
 # unlike a wall decal they have depth and move behind the boards with parallax.
 eye=(2.22,2.70,1.70);distance=12.0;factor=(4.90+distance-eye[1])/(4.90-eye[1])
 for px,py in [(202,45),(239,49),(216,57)]:
  x=(px+.5-160)*8.16/240;z=1.58+(.5-(py+.5)/101)*2.99
  o=b('Attic_window_source_star',(eye[0]+factor*(x-eye[0]),4.90+distance,eye[2]+factor*(z-eye[2])),(.034*factor,.008,.0296*factor),'white')
  o['bake_unlit']=True;o['bake_no_shadow']=True;o['bake_group']='Attic_window_sky'
 # Board backs sit 1 mm in front of the frame's front (y=4.8175).
 # Keeping the old recess-relative depth would put the top board's front
 # exactly on that frame face, causing flicker at their intersection.
 # Irregular crossed boards, with varied lengths and chipped ends.
 for i,(x,z,w,angle) in enumerate([(2.18,2.80,1.44,-.24),(2.17,2.55,1.75,.27),(2.29,2.29,1.86,-.05),(2.18,2.03,1.66,.32),(2.13,1.71,1.80,-.19),(2.30,1.43,1.36,-.28)]):
  profile=[(-w/2,-.10),(-w/2+.035,.08),(-w/2+.12,.12),(w/2-.08,.105),(w/2,.07),(w/2-.02,-.08),(w/2-.16,-.105)]
  n=len(profile);vs=[(xx,yy,zz) for yy in [-.0325,.0325] for xx,zz in profile]
  o=g.mesh('Window_board',vs,[tuple(range(n)),tuple(reversed(range(n,2*n)))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],'yellow');o.location=(x,4.784-i*.003,z);o.rotation_euler.y=angle
  for dx in [-w*.40,w*.40]:
   b('Board_nail',(x+dx*math.cos(angle),4.747-i*.003,z-dx*math.sin(angle)),(.024,.006,.032),'red')
 # The floor opening is now cut by the shell and connects to the den ladder shaft.
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
