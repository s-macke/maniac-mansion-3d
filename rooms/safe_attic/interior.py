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
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Skirting') and (obj.location.y>c['geometry']['depth']-.3 or obj.location.y<.3):
   bpy.data.objects.remove(obj,do_unlink=True)
 wall_before=set(bpy.data.objects)
 # Trace the staggered plank ends from 009 instead of repeating equal boards.
 b('Board_dark_backing',(0,5.013,1.56),(8.24,.014,3.12),'black')
 joints=[[119,190,239],[214],[143],[94,134,207],[],[111,135,190],[],[87,119],[],[135,206],[],[94,119,207],[167]]
 def wall_x(u):return -4.12+(u-63)/195*8.24
 def wall_z(v):return 3.12-v/104*3.12
 for row,ends in enumerate(joints):
  top=wall_z(row*8);bottom=wall_z((row+1)*8)
  cuts=[63,*ends,258]
  for j,(left,right) in enumerate(zip(cuts,cuts[1:])):
   x0=wall_x(left)+.012;x1=wall_x(right)-.012
   # Slightly uneven depth and chipped end cuts retain the old timber surface.
   y=5.001-.004*((row+j)%3)
   vertices=[(x0,y,bottom+.018),(x1-.018,y,bottom+.018),
             (x1,y,bottom+.07),(x1,y,top-.025),
             (x0+.012,y,top-.014),(x0,y,top-.065)]
   g.mesh('Attic_staggered_plank',vertices,[tuple(range(6))],'darkgray')
   # Blue seam edges and paired dark nail holes visible in the original.
   b('Plank_lower_edge',((x0+x1)/2,y-.002,bottom+.012),(x1-x0,.006,.015),'blue')
   if right<258:
    for dz in [.075,.145]:b('Board_nail',(x1-.095,y-.006,bottom+dz),(.032,.008,.026),'black')
 for x in [-4.105,4.105]:b('Wall_corner_edge',(x,5.00,1.56),(.018,.022,3.12),'black')
 # Preserve the actual winding/dense weathering silhouette, not uniform noise.
 # Only turquoise pixels are used; the established circular-overlay exclusion stays.
 image=bpy.data.images.load(str(ROOT/'source/room 009.png'),check_existing=False)
 image.colorspace_settings.name='Non-Color';pixels=list(image.pixels);iw,ih=image.size
 groups={'cyan':([],[]),'aqua':([],[])}
 for v in range(104):
  for u in range(63,258):
   if 157<=u<=176 and 25<=v<=43:continue # hanging bulb belongs to its solid model
   off=((ih-1-v)*iw+u)*4;rgb=tuple(round(k*255) for k in pixels[off:off+3])
   if rgb not in [(0,168,168),(84,252,252)]:continue
   color='cyan' if rgb==(0,168,168) else 'aqua';vs,fs=groups[color];n=len(vs)
   vs.extend([(wall_x(u),4.979,wall_z(v+1)),(wall_x(u+1),4.979,wall_z(v+1)),
              (wall_x(u+1),4.979,wall_z(v)),(wall_x(u),4.979,wall_z(v))]);fs.append((n,n+1,n+2,n+3))
 for color,(vs,fs) in groups.items():g.mesh('Original_board_weathering_'+color,vs,fs,color)
 bpy.data.images.remove(image)
 # User-requested continuation on the unseen opposite wall. Rotate the complete
 # board treatment, preserving inward-facing surfaces. Weathering is distinct below.
 bpy.context.view_layer.update()
 opposite=Matrix.Translation((0,10.4-c['geometry']['depth'],0))@Matrix.Rotation(math.pi,4,'Z')
 for obj in set(bpy.data.objects)-wall_before:
  if obj.name.startswith('Original_board_weathering'):continue
  copy=obj.copy();copy.data=obj.data.copy();obj.users_collection[0].objects.link(copy)
  copy.name='Front_inferred_safe_attic_'+obj.name
  copy.matrix_world=opposite@obj.matrix_world
 # Independent damp patches on the inferred wall: a tall left-hand stain,
 # separated low islands and a small upper-right patch, not the source's winding trail.
 rng=random.Random(19009);groups={'cyan':([],[]),'aqua':([],[])}
 patches=[(-2.9,.33,.82,.30),(-2.65,.87,.50,.48),(-2.88,1.55,.31,.43),
          (-.35,.22,.88,.22),(1.75,.35,.70,.32),(2.75,.72,.46,.48),(2.25,2.04,.52,.24)]
 y=10.4-c['geometry']['depth']-4.979
 for row in range(104):
  z=(row+.5)*3.12/104
  for col in range(195):
   x=-4.12+(col+.5)*8.24/195
   # Coherent ragged edges with sparse holes inside each damp patch.
   xx=x+.12*math.sin(z*17+x*3);zz=z+.075*math.sin(x*13-z*5)
   density=max(math.exp(-2*((xx-cx)/rx)**2-2*((zz-cz)/rz)**2) for cx,cz,rx,rz in patches)
   if density<.12 or rng.random()>density*.77:continue
   color='aqua' if rng.random()<.21 else 'cyan';vs,fs=groups[color];n=len(vs)
   dx=8.24/195/2;dz=3.12/104/2
   vs.extend([(x-dx,y,z-dz),(x-dx,y,z+dz),(x+dx,y,z+dz),(x+dx,y,z-dz)]);fs.append((n,n+1,n+2,n+3))
 for color,(vs,fs) in groups.items():g.mesh('Front_inferred_safe_attic_weathering_'+color,vs,fs,color)
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
