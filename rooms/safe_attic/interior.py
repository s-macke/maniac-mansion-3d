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
 # Boards fill the rear wall all the way to the floor, corners and ceiling.
 b('Board_dark_backing',(0,5.013,1.56),(8.24,.014,3.12),'black')
 for row in range(13):
  z=.12+row*.24
  b('Attic_wall_board',(0,5.009,z),(8.24,.018,.224),'darkgray')
  for x in [-4.06,4.06,(-1.7 if row%2 else 1.50)]:
   b('Board_joint',(x,4.997,z),(.014,.005,.224),'black')
   for dz in [-.054,.054]:b('Board_nail',(x+.035,4.993,z+dz),(.018,.005,.018),'gray')
 for x in [-4.105,4.105]:b('Wall_corner_edge',(x,5.00,1.56),(.018,.022,3.12),'black')
 # Sparse turquoise weathering below the boards, without reproducing the blue circular overlay.
 rng=random.Random(9);vs=[];fs=[]
 for i in range(440):
  x=rng.uniform(-4.04,4.04);z=rng.uniform(.15,1.08);w=rng.uniform(.012,.035);h=rng.uniform(.008,.03);n=len(vs)
  vs.extend([(x,4.996,z),(x+w,4.996,z),(x+w,4.996,z+h),(x,4.996,z+h)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Board_weathering',vs,fs,'cyan')
 # Replace the solid left shell wall with four slabs around a real window.
 # This is visual access only; navigation retains the solid outer boundary.
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_left'):bpy.data.objects.remove(obj,do_unlink=True)
 offset=5.2-c['geometry']['depth'];yc=3.73;half=.48;bottom=1.11;top=2.51
 for y0,y1,z0,z1 in [(offset,yc-half,0,3.12),(yc+half,5.2,0,3.12),(yc-half,yc+half,0,bottom),(yc-half,yc+half,top,3.12)]:
  b('Left_wall_window_surround',(-4.21,(y0+y1)/2,(z0+z1)/2),(.18,y1-y0,z1-z0),'darkgray')
 # Open frame, jambs and sill. There is no opaque pane in the opening.
 for yy in [yc-half,yc+half]:
  b('Window_black_frame',(-4.105,yy,1.81),(.045,.10,1.60),'black')
  b('Window_frame_highlight',(-4.078,yy,1.81),(.014,.025,1.51),'gray')
  b('Window_deep_jamb',(-4.29,yy,1.81),(.36,.035,1.40),'darkgray')
 for zz in [bottom,top]:
  b('Window_black_frame',(-4.105,yc,zz),(.045,1.06,.10),'black')
  b('Window_frame_highlight',(-4.078,yc,zz),(.014,1.02,.025),'gray')
  b('Window_reveal',(-4.29,yc,zz),(.36,.96,.035),'darkgray')
 b('Window_crossbar',(-4.078,yc,1.81),(.06,.96,.045),'gray')
 b('Window_sill',(-4.08,yc,1.06),(.31,1.11,.055),'gray')
 # A closed black volume well outside the wall, with distant star geometry.
 # Its depth gives natural frame occlusion/parallax without shaders or a portal.
 def sky_box(name,loc,size,color):
  obj=b(name,loc,size,color);obj['bake_unlit']=True;obj['bake_no_shadow']=True;obj['bake_group']='Attic_window_sky';return obj
 sky_box('Night_sky_back',(-31,yc,5),( .05,40,30),'black')
 for yy in [yc-20,yc+20]:sky_box('Night_sky_side',(-17.6,yy,5),(26.8,.05,30),'black')
 for zz in [-10,20]:sky_box('Night_sky_top_bottom',(-17.6,yc,zz),(26.8,40,.05),'black')
 stars=random.Random(9009)
 for i in range(100):
  xx=stars.uniform(-29,-14);yy=yc+stars.uniform(-15,15);zz=stars.uniform(-6,16)
  size=stars.uniform(.035,.075)
  sky_box('Distant_star',(xx,yy,zz),(.008,size,size),['white','gray','lightblue','yellow'][i%4])
 # Place a few recognizable sparse stars in the normal straight-through view.
 for yy,zz,col in [(yc-2.3,3.8,'lightblue'),(yc+1.4,1.6,'white'),(yc+.4,5.0,'gray')]:
  sky_box('Window_reference_star',(-19,yy,zz),(.008,.065,.065),col)
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
 # Visible suspended bulb supplies the local baked illumination.
 g.cyl('Attic_light_cord',(0,3.66,2.92),.012,.39,'black');g.cyl('Bulb_socket',(0,3.66,2.67),.065,.11,'black')
 bulb=g.sphere('Attic_bulb',(0,3.66,2.55),(.07,.07,.11),'white')
 bulb['bake_unlit']=True;bulb['bake_no_shadow']=True
 finish(c)
