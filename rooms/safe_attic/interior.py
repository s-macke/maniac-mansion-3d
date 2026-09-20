"""009: boarded attic, cracked walls, small window and portrait-covered safe."""
from blender_shared.placement import rear_anchored
from pathlib import Path
import math,random,bpy
from mathutils import Matrix
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.2)
def furnish(g,c):
 b=g.box
 # Gray boards retain the room's base colors; the reference's telescope overlay is not room lighting.
 for row in range(14):
  z=.20+row*.208
  b('Attic_wall_board',(0,4.977,z),(8.17,.06,.19),'darkgray')
  for x in [-4.06,4.06,(-1.7 if row%2 else 1.50)]:
   b('Board_joint',(x,4.935,z),(.014,.016,.19),'black')
   for dz in [-.047,.047]:b('Board_nail',(x+.065,4.918,z+dz),(.018,.014,.018),'gray')
 # Sparse turquoise weathering below the boards, without reproducing the blue circular overlay.
 rng=random.Random(9);vs=[];fs=[]
 for i in range(440):
  x=rng.uniform(-4.04,4.04);z=rng.uniform(.15,1.08);w=rng.uniform(.012,.035);h=rng.uniform(.008,.03);n=len(vs)
  vs.extend([(x,4.932,z),(x+w,4.932,z),(x+w,4.932,z+h),(x,4.932,z+h)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Board_weathering',vs,fs,'cyan')
 # Opaque star window on the left; it creates no additional room connection.
 for x,w,d,h,col in [(-4.075,1.10,.08,1.65,'black'),(-4.023,1.02,.055,1.55,'gray'),(-3.985,.88,.025,1.40,'black')]:b('Attic_window',(x,3.73,1.81),(d,w,h),col)
 b('Window_crossbar',(-3.96,3.73,1.81),(.035,.90,.035),'gray')
 for y,z in [(3.42,2.13),(3.86,1.58),(3.77,2.32)]:b('Window_star',(-3.963,y,z),(.012,.02,.025),'white')
 for pts in [[(-4.108,1.45,.3),(-4.108,1.83,.7),(-4.108,1.68,1.04),(-4.108,1.98,1.43)], [(-4.108,3.1,2.65),(-4.108,2.9,2.9),(-4.108,2.45,3.08)]]:curved_line(g,'Wall_crack',pts,.014,'black')
 # Closed, static safe case behind the portrait. No puzzle or new moving mechanism.
 b('Safe_case',(3.98,1.85,1.85),(.25,1.03,1.63),'black')
 b('Safe_door',(3.84,1.85,1.85),(.035,.95,1.53),'darkgray')
 for z in [1.38,2.29]:b('Safe_hinge',(3.806,2.26,z),(.04,.09,.12),'gray')
 before=set(bpy.data.objects)
 b('Portrait_safe_cover',(0,0,1.85),(.94,.035,1.49),'black')
 b('Portrait_border',(0,-.027,1.85),(.86,.02,1.41),'white')
 source_patch(g,ROOT/'source/room 009.png',(276,26,293,82),(0,-.077,1.85),(.74,1.29),'Original_attic_portrait')
 bpy.context.view_layer.update();transform=Matrix.Translation((3.77,1.85,0))@Matrix.Rotation(-math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=transform@o.matrix_world
 # Small suspended bulb, kept as geometry with static baked shading.
 g.cyl('Attic_light_cord',(0,3.66,2.92),.012,.39,'black');g.cyl('Bulb_socket',(0,3.66,2.67),.065,.11,'black')
 g.sphere('Attic_bulb',(0,3.66,2.55),(.07,.07,.11),'white')
 finish(c)
