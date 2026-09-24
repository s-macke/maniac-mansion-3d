"""004: irregular stone wall, barred openings, chained skeletal remains and chandelier."""
from pathlib import Path
import random,math,bpy
from mathutils import Matrix
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.lab_furniture import disc
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box;rng=random.Random(4)
 # Irregular stone polygons, with mortar gaps and the existing door apertures left clear.
 for row in range(12):
  for col in range(27):
   x=-6.08+col*.46+(row%2)*.23+rng.uniform(-.025,.025);z=.14+row*.255+rng.uniform(-.012,.012)
   if x>6.1 or any(abs(x-p['position'][0])<p['width']/2+.36 and z<p['height']+.13 for p in c['ports']):continue
   w=rng.uniform(.43,.50);h=rng.uniform(.25,.29);pts=[(-w*.47,-h*.33),(-w*.5,h*.13),(-w*.22,h*.50),(w*.32,h*.46),(w*.52,-h*.06),(w*.27,-h*.48)]
   g.mesh('Stone_red_edge',[(x+u,4.896,z+v) for u,v in pts],[tuple(range(6))],'red')
   g.mesh('Stone_brown_face',[(x+u*.81,4.882,z+v*.81) for u,v in pts],[tuple(range(6))],'brown')
 # Two arched barred windows are opaque decorative recesses, not extra room connections.
 for x in [-1.66,1.77]:
  for y,w,h,col in [(4.86,1.05,1.18,'blue'),(4.825,.95,1.10,'gray'),(4.793,.83,1.02,'black')]:
   bottom=1.55;spring=bottom+h-w/2;pts=[(x-w/2,y,bottom),(x+w/2,y,bottom),(x+w/2,y,spring)]+[(x+w/2*math.cos(i*math.pi/16),y,spring+w/2*math.sin(i*math.pi/16)) for i in range(1,17)]
   g.mesh('Barred_arch',pts,[tuple(range(len(pts)))],col)
  for dx in [-.25,0,.25]:g.beam('Window_bar',(x+dx,4.756,1.57),(x+dx,4.756,2.51),.036,'lightblue')
 # Three-prong hanging blue candle fixture.
 g.beam('Dungeon_chandelier_chain',(0,3.78,3.10),(0,3.78,2.35),.025,'blue')
 for x in [-.36,0,.36]:
  curved_line(g,'Chandelier_arm',[(0,3.78,2.35),(x,3.78,2.25),(x,3.78,2.64)],.035,'blue');b('Unlit_candle',(x,3.78,2.76),(.045,.045,.23),'lightblue')
 # Static skeletal remains, resting behind the clear cross-room aisle.
 sx,sy=-1.90,3.83
 g.sphere('Skull',(sx+.30,sy+.13,.96),(.17,.13,.21),'white')
 for dx in [-.07,.07]:g.sphere('Skull_socket',(sx+.30+dx,sy-.003,1.0),(.048,.024,.05),'black')
 b('Skull_jaw',(sx+.30,sy+.105,.78),(.18,.16,.063),'white')
 for i in range(9):g.sphere('Spine_bone',(sx+.05+i*.025,sy-.11+i*.023,.32+i*.046),(.037,.038,.03),'white')
 for i in range(5):
  z=.43+i*.056;w=.17+i*.008;curved_line(g,'Rib',[(sx+.18+math.cos(a)*w,sy+.04-math.sin(a)*.11,z) for a in [j*math.tau/18 for j in range(19)]],.024,'white')
 for s in [-1,1]:
  curved_line(g,'Leg_bones',[(sx+.04,sy+s*.09,.32),(sx-.49,sy-.12+s*.13,.37),(sx-.93,sy-.31+s*.13,.10)],.042,'white')
  curved_line(g,'Raised_arm',[(sx+.23+s*.16,sy+.02,.66),(sx+.25+s*.34,sy+.06,1.08),(sx+.28+s*.11,sy+.14,1.43)],.035,'white')
  curved_line(g,'Wrist_chain',[(sx+.28+s*.11,sy+.14,1.43),(sx+.30,4.73,2.04)],.021,'gray')
 b('Chain_wall_plate',(sx+.30,4.81,2.08),(.29,.06,.24),'blue')
 # Original scrawled lettering on the left steel wall.
 before=set(bpy.data.objects)
 source_patch(g,ROOT/'source/room 004.png',(0,22,84,90),(0,0,1.77),(1.57,1.28),'Dungeon_graffiti',only={'black'})
 bpy.context.view_layer.update();m=Matrix.Translation((-6.192,2.55,0))@Matrix.Rotation(math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=m@o.matrix_world
 g.sphere('Dungeon_floor_patch',(0,2.8,.002),(5.23,1.74,.002),'brown')
 finish(c)
