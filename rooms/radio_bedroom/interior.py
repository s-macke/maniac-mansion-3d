"""021: Fred's blue bed, radio laboratory and original wall art."""
from blender_shared.placement import rear_anchored,offset_group
from pathlib import Path
import math,bpy
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import cabinet,chandelier,finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.1)
def furnish(g,c):
 b=g.box
 # Blue bedding reaches the red headboard; no exposed white mattress in 021.
 x,y,w,d=-1.15,3.9,2.8,1.35
 b('Bed_frame',(x,y,.31),(w,d,.42),'brown')
 b('Bed_mattress',(x,y,.59),(w-.1,d-.06,.24),'blue')
 b('Bed_cover',(x,y,.63),(w-.1,d+.02,.25),'blue')
 b('Cover_front_drop',(x,y-d/2-.025,.42),(w-.1,.055,.40),'blue')
 g.sphere('Pillow',(x-w*.34,y,.79),(.37,d*.34,.10),'blue')
 for dx,height,col in [(-w/2,1.14,'red'),(w/2,1.0,'brown')]:
  # Joined rounded shoulders, rather than an ellipsoid sitting on a square board.
  half=(d+.1)/2;r=.18
  profile=[(-half,.12),(half,.12)]
  for i in range(6):
   a=i*math.pi/10;profile.append((half-r+r*math.cos(a),height-r+r*math.sin(a)))
  for i in range(6):
   a=math.pi/2+i*math.pi/10;profile.append((-half+r+r*math.cos(a),height-r+r*math.sin(a)))
  n=len(profile);vs=[(x+dx+side*.065,y+yy,z) for side in [-1,1] for yy,z in profile]
  g.mesh('Bed_rounded_end',vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],col)
 # Low radio console, with equipment kept on its red top.
 cabinet(g,'Radio_console',1.95,4.23,2.35,.88,.60)
 with offset_group(z=-.27):
  b('Radio_case',(1.94,4.22,1.25),(1.04,.57,.67),'cyan')
  b('Radio_face',(1.80,3.922,1.25),(.65,.025,.57),'black')
  b('Tuner_outer_frame',(1.80,3.902,1.44),(.60,.014,.19),'aqua')
  b('Tuner_dark_recess',(1.80,3.891,1.44),(.53,.008,.135),'blue')
  b('Tuner_green_scale',(1.80,3.884,1.44),(.47,.006,.077),'lime')
  for i in range(9):b('Tuner_tick',(1.60+i*.049,3.878,1.455),(.012,.006,.043),'white')
  b('Tuner_needle',(1.80,3.873,1.435),(.014,.004,.10),'lightred')
  b('Speaker_panel',(2.285,3.921,1.25),(.255,.024,.57),'aqua')
  for row in range(8):
   for col in range(4):b('Speaker_perforation',(2.205+col*.052,3.905,1.015+row*.064),(.022,.006,.028),'black')
  for xx in [1.60,1.97]:
   o=g.cyl('Tuning_knob',(0,0,0),.105,.045,'gray',24);o.rotation_euler.x=math.pi/2;o.location=(xx,3.872,1.105)
   o=g.cyl('Knob_black_face',(0,0,0),.082,.012,'black',24);o.rotation_euler.x=math.pi/2;o.location=(xx,3.845,1.105)
   b('Knob_marker',(xx-.045,3.836,1.143),(.017,.006,.028),'white')
  for xx in [1.60,1.84,2.08]:
   b('Radio_top_switch',(xx,3.94,1.592),(.14,.11,.035),'red')
   b('Switch_highlight',(xx-.025,3.877,1.591),(.025,.006,.019),'lightred')
  for xx in [1.32,2.57]:
   g.cyl('Radio_coil_core',(xx,4.24,1.55),.042,.55,'cyan')
   for k in range(8):g.cyl('Tapered_radio_coil',(xx,4.24,1.38+k*.047),.13-k*.008,.018,'yellow',24)
   g.cyl('Coil_cap_socket',(xx,4.24,1.79),.060,.052,'black',20)
   g.sphere('Coil_blue_cap',(xx,4.24,1.831),(.056,.056,.045),'lightblue')
   g.sphere('Coil_cap_glint',(xx-.015,4.207,1.851),(.018,.016,.013),'white')
  curved_line(g,'Loop_aerial',[(1.94+.23*math.cos(a*math.tau/32),4.29,1.97+.23*math.sin(a*math.tau/32)) for a in range(33)],.025,'aqua')
  g.cyl('Aerial_mast',(1.94,4.29,1.72),.02,.50,'aqua')
  def mic_grille(name,cx,cz,rx,ry,rz,dx,z,w,h):
   # Small curved patches sit on the ellipsoid rather than hovering on a front plane.
   vs=[];faces=[]
   for i in range(4):
    lo=dx-w/2+w*i/4;hi=lo+w/4
    n=len(vs)
    for xx,zz in [(lo,z-h/2),(hi,z-h/2),(hi,z+h/2),(lo,z+h/2)]:
     yy=4.08-ry*math.sqrt(max(0,1-(xx/rx)**2-((zz-cz)/rz)**2))-.0015
     vs.append((cx+xx,yy,zz))
    faces.append((n,n+1,n+2,n+3))
   g.mesh(name,vs,faces,'black')
  # Left microphone is short, pale and mounted on a rectangular control box.
  b('Left_mic_control_box',(.96,4.08,1.035),(.38,.29,.18),'cyan')
  b('Left_mic_control_face',(.96,3.929,1.035),(.31,.014,.11),'black')
  for xx in [.86,.96,1.06]:b('Mic_control_switch',(xx,3.916,1.04),(.043,.012,.036),'aqua')
  g.cyl('Left_mic_stand',(.96,4.08,1.22),.022,.22,'gray')
  bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=1,location=(.96,4.08,1.43))
  o=g.put(bpy.context.object,'Left_microphone','white');o.scale=(.085,.07,.16)
  for k in range(5):mic_grille('Left_mic_grille',.96,1.43,.085,.07,.16,0,1.32+k*.048,.085,.019)
  # Right microphone retains its aqua oval grille and wide U-shaped cradle.
  g.cyl('Microphone_base',(2.95,4.08,.98),.14,.045,'aqua')
  g.cyl('Microphone_stand',(2.95,4.08,1.12),.025,.28,'cyan')
  bpy.ops.mesh.primitive_uv_sphere_add(segments=64,ring_count=32,radius=1,location=(2.95,4.08,1.43))
  o=g.put(bpy.context.object,'Right_microphone','aqua');o.scale=(.11,.075,.22)
  for row in range(7):
   for col in range(3):mic_grille('Right_mic_grille',2.95,1.43,.11,.075,.22,-.06+col*.06,1.285+row*.047,.025,.025)
  curved_line(g,'Mic_cradle',[(2.80,4.08,1.46),(2.80,4.08,1.23),(3.10,4.08,1.23),(3.10,4.08,1.46)],.025,'aqua')
 # Solid clipped-corner portrait backing, with original frame pixels on its face.
 corners=[(-.545,-.615),(.545,-.615),(.625,-.535),(.625,.535),(.545,.615),(-.545,.615),(-.625,.535),(-.625,-.535)]
 vs=[(-1.8+xx,yy,2.06+zz) for yy in [4.90,4.92] for xx,zz in corners]
 g.mesh('Fred_portrait_backing',vs,[tuple(range(8)),tuple(reversed(range(8,16)))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)],'brown')
 source_patch(g,ROOT/'source/room 021.png',(86,24,146,73),(-1.8,4.899,2.06),(1.25,1.23),'Original_Fred_portrait',only=['black','brown','yellow','lightred','red','blue','lightblue','white','gray','darkgray','cyan','aqua'])
 source_patch(g,ROOT/'source/room 021.png',(160,25,200,73),(-.15,4.919,2.03),(.83,1.0),'Wanted_poster')
 # Two pale globes flank the black center stem; the earlier third globe was erroneous.
 chandelier(g,1.65,4.0,'white')
 for obj in bpy.data.objects:
  if obj.name.startswith(('Pendant_globe','Globe_glint')):
   obj['bake_unlit']=True;obj['bake_no_shadow']=True
 for xx in [1.22,2.08]:
  glow=g.sphere('Globe_yellow_center',(xx,3.897,2.73),(.036,.021,.07),'yellow');glow['bake_unlit']=True
  g.beam('Pendant_lower_finial',(xx,4.0,2.62),(xx,4.0,2.38),.022,'black')
 finish(c)
