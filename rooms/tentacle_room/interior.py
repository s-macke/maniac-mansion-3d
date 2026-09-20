"""020: two giant speaker cabinets, green bed, hi-fi shelf and original posters."""
from blender_shared.placement import rear_anchored
from pathlib import Path
import math,bpy
from blender_shared.furnishings import source_patch
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.2)
def furnish(g,c):
 b=g.box
 # Batch thin blue wall stripes above the timber panelling.
 vs=[];fs=[]
 for i in range(91):
  x=-4.07+i*.09;n=len(vs);vs.extend([(x,5.009,1.04),(x+.012,5.009,1.04),(x+.012,5.009,3.1),(x,5.009,3.1)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Music_wall_stripes',vs,fs,'lightblue')
 b('Music_wainscot',(0,4.977,.54),(8.16,.08,1.00),'brown')
 for x in [-4+i*.30 for i in range(28)]:b('Wainscot_stile',(x,4.925,.55),(.026,.02,.88),'lightred')
 for z,col in [(.08,'red'),(1.02,'yellow'),(1.09,'red')]:b('Wainscot_rail',(0,4.91,z),(8.16,.045,.035),col)
 for x in [-4.085,4.085]:
  b('Side_wainscot',(x,(5.2-c['geometry']['depth'])/2+2.60,.54),(.055,c['geometry']['depth']-.42,1.0),'brown')
  for z,col in [(1.02,'yellow'),(1.09,'red')]:b('Side_panel_rail',(x,(5.2-c['geometry']['depth'])/2+2.60,z),(.075,c['geometry']['depth']-.42,.035),col)
 def disc(name,x,y,z,r,depth,col):
  o=g.cyl(name,(0,0,0),r,depth,col,40);o.rotation_euler.x=math.pi/2;o.location=(x,y,z);return o
 for x in [-1.90,2.95]:
  b('Speaker_cabinet',(x,4.61,1.43),(1.19,.76,2.82),'black')
  b('Speaker_gold_edge',(x,4.212,1.43),(1.15,.025,2.76),'brown')
  b('Speaker_red_edge',(x,4.193,1.43),(1.10,.02,2.71),'red')
  b('Speaker_baffle',(x,4.175,1.43),(1.045,.019,2.65),'black')
  for z,r in [(.99,.47),(2.28,.235)]:
   for yy,rr,col in [(4.157,r,'darkgray'),(4.137,r*.91,'black'),(4.121,r*.80,'gray'),(4.102,r*.765,'darkgray'),(4.084,r*.68,'black'),(4.06,r*.25,'gray'),(4.044,r*.17,'white')]:disc('Speaker_cone',x,yy,z,rr,.018,col)
  for dx in [-.47,.47]:
   for z in [.42,1.55,2.66]:b('Speaker_screw',(x+dx,4.151,z),(.025,.015,.025),'gray')
  b('Speaker_badge',(x-.34,4.142,.16),(.19,.02,.06),'cyan')
 # Recess the cabinet fronts to leave full body clearance at the ladder landing.
 for o in list(bpy.data.objects):
  if o.name.startswith('Speaker'):
   o.location.y+=.18
   if o.name.startswith('Speaker_cabinet'):
    o.location.y-=.09;o.scale.y=.58/.76
 # The room's low green sleeping platform, with no character or gameplay.
 b('Green_bed_base',(.46,3.95,.28),(2.72,1.17,.39),'green');b('Green_bed_cover',(.46,3.95,.51),(2.77,1.20,.13),'lime')
 b('Bed_front',(.46,3.331,.36),(2.77,.075,.39),'green');g.sphere('Green_pillow',(-.45,4.08,.66),(.38,.35,.14),'green')
 # Shelf and separate hi-fi components under the Disco Sucks sign.
 b('Stereo_shelf',(.48,4.71,1.41),(2.0,.45,.085),'red')
 for x in [-.20,1.16]:b('Shelf_bracket',(x,4.83,1.25),(.06,.23,.33),'brown')
 for k,z in enumerate([1.56,1.77,1.98]):
  b('Hifi_component',(.46,4.61,z),(.84,.35,.19),'gray');b('Hifi_face',(.46,4.426,z),(.78,.021,.145),'black')
  if k==2:
   b('Receiver_display',(.38,4.41,z),(.48,.013,.065),'green')
   for i in range(9):b('Receiver_tick',(.16+i*.05,4.396,z),(.012,.012,.055),'lime')
  else:
   for dx in [-.22,.20]:b('Tape_deck',(.46+dx,4.407,z),(.29,.014,.08),'aqua')
  for dx in [.29,.34]:b('Hifi_button',(.46+dx,4.392,z-.04),(.023,.017,.024),'white')
 g.sphere('Small_shelf_speaker',(1.06,4.60,1.72),(.09,.085,.27),'black');g.sphere('Shelf_speaker_glint',(1.06,4.508,1.76),(.034,.013,.06),'white')
 source_patch(g,ROOT/'source/room 020.png',(222,16,286,79),(-.56,4.90,2.28),(1.03,1.17),'Original_tour_poster')
 source_patch(g,ROOT/'source/room 020.png',(305,17,351,33),(.56,4.90,2.67),(.92,.36),'Disco_sign')
 source_patch(g,ROOT/'source/room 020.png',(360,17,400,62),(1.60,4.90,2.37),(.67,.93),'Mom_portrait')
 b('Bedside_outlet',(.4,4.899,.84),(.15,.015,.12),'white')
 for x in [.365,.435]:b('Outlet_slot',(x,4.885,.85),(.012,.008,.045),'black')
 finish(c)
