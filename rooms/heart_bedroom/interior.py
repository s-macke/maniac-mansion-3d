"""019: source-led vanity, heart bed, telephone, portrait and ceiling fixture."""
import math
import bpy
from mathutils import Matrix, Vector
from pathlib import Path
from blender_shared.placement import rear_anchored, offset_group
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import plant,finish
ROOT=Path(__file__).resolve().parents[2]

@rear_anchored(5.1)
def furnish(g,c):
 b=g.box
 # Staggered large hearts, matching the original repeat rather than tiny icons.
 verts=[];faces=[]
 for row in range(11):
  z=.41+row*.255
  for col in range(17):
   x=-4.10+col*.51+(row%2)*.255
   if x>4.12:continue
   points=[(-.19,.045),(-.15,.115),(-.065,.115),(0,.055),(.065,.115),(.15,.115),(.19,.045),(0,-.125)]
   n=len(verts);verts.extend([(x+u,4.919,z+v) for u,v in points]);faces.append(tuple(range(n,n+8)))
 g.mesh('Staggered_heart_wallpaper',verts,faces,'red')
 # Dark red ceiling border and layered skirting seen around the patterned wall.
 b('Rear_ceiling_cornice',(0,4.84,3.035),(8.64,.16,.17),'red')
 for side in [-1,1]:
  b('Side_ceiling_cornice',(side*4.27,5.1-c['geometry']['depth']/2,3.06),(.12,c['geometry']['depth'],.12),'red')
 for z,h,col in [(.27,.08,'red'),(.215,.025,'yellow'),(.18,.035,'brown')]:
  b('Rear_wall_base_rail',(0,4.885,z),(8.64,.055,h),col)
 # A local surround on the corridor side; the shared moving leaf is unchanged.
 with offset_group(y=5.1-c['geometry']['depth']):
  for y in [1.28,2.72]:
   b('Bedroom_door_red_jamb',(-4.29,y,1.44),(.055,.10,2.88),'red')
   b('Bedroom_door_highlight',(-4.255,y-.025,1.44),(.018,.022,2.88),'lightred')
  b('Bedroom_door_lintel',(-4.29,2,2.88),(.055,1.54,.08),'red')
 # Vanity: two small side compartments and a long central panel, short dark feet.
 vanity_before=set(bpy.data.objects)
 b('Vanity_body',(-2.15,4.18,.49),(2.75,.83,.70),'red')
 b('Vanity_top',(-2.15,4.18,.89),(2.88,.93,.11),'red')
 b('Vanity_top_front_edge',(-2.15,3.709,.875),(2.88,.035,.025),'black')
 for x in [-3.44,-.86]:b('Vanity_foot',(x,4.16,.105),(.13,.70,.21),'black')
 def inset(name,x,y,z,w,h):
  b(name+'_dark',(x,y,z),(w,.035,h),'black')
  b(name+'_red_border',(x,y-.023,z),(w-.035,.014,h-.035),'lightred')
  b(name+'_recess',(x,y-.033,z),(w-.105,.012,h-.105),'red')
 for x,w in [(-3.12,.48),(-2.15,1.33),(-1.18,.48)]:
  inset('Vanity_panel',x,3.744,.49,w,.52)
 for x in [-3.12,-1.18]:b('Vanity_handle',(x,3.694,.64),(.045,.027,.024),'black')
 # Flat-topped arched mirror with the actual branching crack, not a single zigzag.
 outline=[(-.57,0),(.57,0),(.57,1.23),(.49,1.43),(.30,1.59),(-.30,1.59),(-.49,1.43),(-.57,1.23)]
 g.mesh('Mirror_dark_outline',[(x-2.23,4.52,z+.94) for x,z in outline],[tuple(range(8))],'red')
 g.mesh('Mirror_aqua_glass',[(x*.95-2.23,4.51,z*.98+.955) for x,z in outline],[tuple(range(8))],'aqua')
 source_patch(g,ROOT/'source/room 019.png',(75,30,110,77),(-2.23,4.507,1.735),(1.08,1.45),'Original_mirror_cracks',only={'cyan'})
 # Blue flower vase at left and the pink/white desk telephone at right.
 b('Blue_vase',(-3.13,4.04,1.035),(.26,.23,.23),'blue')
 b('Vase_label',(-3.13,3.918,1.045),(.16,.015,.075),'aqua')
 for dx,dz in [(-.10,.12),(.02,.24),(.11,.16)]:
  g.beam('Vase_stem',(-3.13,4.04,1.14),(-3.13+dx,4.04,1.14+dz),.018,'green')
  g.sphere('Vase_leaf',(-3.13+dx,4.04,1.14+dz),(.07,.035,.035),'lime')
 b('Telephone_base',(-1.17,4.03,.987),(.47,.30,.09),'purple')
 b('Telephone_body',(-1.17,4.02,1.055),(.24,.21,.12),'white')
 g.cyl('Telephone_dial',(-1.17,4.00,1.124),.073,.015,'pink')
 b('Telephone_receiver',(-1.17,4.04,1.175),(.52,.095,.055),'purple')
 for x in [-1.39,-.95]:
  b('Receiver_earpiece',(x,4.04,1.16),(.13,.15,.08),'pink')
 bpy.context.view_layer.update()
 for obj in set(bpy.data.objects)-vanity_before:
  obj.matrix_world=Matrix.Translation((-2.60,0,0)) @ Matrix.Diagonal(Vector((.82,1,1,1))) @ Matrix.Translation((2.15,0,0)) @ obj.matrix_world
 # Bed runs left-to-right. Its head/pillow is at the curtained right end.
 b('Bed_frame',(.825,3.90,.32),(3.25,1.80,.47),'red')
 b('Bed_mattress',(.825,3.90,.62),(3.17,1.74,.20),'red')
 b('Bed_cover_front',(.825,2.985,.43),(3.23,.055,.65),'red')
 b('Bed_cover_piping',(.825,2.950,.765),(3.23,.022,.022),'lightred')
 b('Bed_footboard',(-.80,3.90,.49),(.14,1.80,.84),'brown')
 for y in [3.10,4.70]:
  g.sphere('Footboard_scroll',(-.80,y,.96),(.075,.10,.12),'brown')
  g.sphere('Footboard_scroll_inset',(-.88,y,.98),(.009,.025,.027),'black')
 # Small stuffed cushion: curved heart outline, softly inflated faces and a
 # sideways lean. The lower tip rests on the mattress instead of standing tall.
 count=64;angle=math.radians(-32);outline=[]
 for i in range(count):
  t=i*math.tau/count
  u=.76*(16*math.sin(t)**3)/32
  v=.50*(13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t)+2.5)/29
  outline.append((u*math.cos(angle)-v*math.sin(angle),(u*math.sin(angle)+v*math.cos(angle))*.72))
 center_z=.732-min(v for u,v in outline)
 verts=[(1.99,3.72,center_z)];rings=13
 for ring in range(1,rings):
  theta=math.pi*ring/rings;scale=math.sin(theta)
  for u,v in outline:
   verts.append((1.99+u*scale,3.63+.09*math.cos(theta)+v*scale*.32,center_z+v*scale))
 front=len(verts);verts.append((1.99,3.54,center_z));faces=[]
 for i in range(count):faces.append((0,1+(i+1)%count,1+i))
 for ring in range(rings-2):
  ring_start=1+ring*count;next_ring=ring_start+count
  for i in range(count):j=(i+1)%count;faces.append((ring_start+i,ring_start+j,next_ring+j,next_ring+i))
 last=1+(rings-2)*count
 for i in range(count):faces.append((last+i,last+(i+1)%count,front))
 pillow=g.mesh('Soft_heart_pillow',verts,[tuple(reversed(face)) for face in faces],'red')
 pillow['bake_curved_center']=[1.99,3.63+c['geometry']['depth']-5.1,center_z]
 pillow['bake_curved_radii']=[.42,.12,.22];pillow['bake_curved_sign']=1
 # Pillow faces the foot of the bed, with its rounded shape preserved.
 bpy.context.view_layer.update()
 turn=Matrix.Translation((2.10,3.90,center_z)) @ Matrix.Rotation(-math.pi/2,4,'Z') @ Matrix.Translation((-1.99,-3.63,-center_z))
 pillow.matrix_world=turn @ pillow.matrix_world
 pillow['bake_curved_center']=[2.10,3.90+c['geometry']['depth']-5.1,center_z]
 pillow['bake_curved_radii']=[.12,.42,.22]
 # Headboard and curtains span the whole right end, perpendicular to the
 # mattress length. Do not place this assembly flat against the rear wall.
 head_before=set(bpy.data.objects)
 b('Canopy_red_back',(1.845,4.86,1.67),(1.55,.10,2.05),'red')
 for x,sign in [(1.12,1),(2.57,-1)]:
  b('Canopy_post',(x,4.59,1.43),(.075,.075,2.68),'red')
  verts=[]
  for zz,width in [(2.65,.59),(2.18,.49),(1.57,.28),(1.15,.08),(.95,.22)]:
   for j in range(9):
    t=j/8;verts.append((x+sign*t*width,4.53+(.022 if j%2 else -.022),zz))
  g.mesh('Gathered_curtain',verts,[(i*9+j,i*9+j+1,(i+1)*9+j+1,(i+1)*9+j) for i in range(4) for j in range(8)],'red')
  curved_line(g,'Curtain_edge',[(x+sign*w,4.494,zz) for zz,w in [(2.65,.59),(2.18,.49),(1.57,.28),(1.15,.08),(.95,.22)]],.018,'lightred')
 b('Canopy_valance',(1.845,4.53,2.77),(1.65,.25,.32),'red')
 for x in [1.08+i*.20 for i in range(9)]:b('Valance_pleat',(x,4.396,2.79),(.018,.018,.22),'lightred')
 bpy.context.view_layer.update()
 head_transform=Matrix.Translation((2.50,3.90,0)) @ Matrix.Rotation(-math.pi/2,4,'Z') @ Matrix.Diagonal(Vector((1.09,1,1,1))) @ Matrix.Translation((-1.845,-4.53,0))
 for obj in set(bpy.data.objects)-head_before:obj.matrix_world=head_transform @ obj.matrix_world
 b('Bed_headboard',(2.50,3.90,.56),(.14,1.80,1.0),'red')
 # Heavy yellow frame with purple inner bevel, attached to the rear wall.
 b('Portrait_back',(.13,4.875,2.14),(1.52,.09,1.44),'red')
 for w,h,col,yy in [(1.48,1.40,'yellow',4.818),(1.26,1.18,'purple',4.803),(1.09,1.02,'black',4.792)]:
  b('Portrait_frame_layer',(.13,yy,2.14),(w,.018,h),col)
 source_patch(g,ROOT/'source/room 019.png',(193,22,231,56),(.13,4.781,2.14),(1.02,.94),'Original_doctor_portrait')
 # Bedside cupboard backs onto the right wall, with its front facing inward.
 cupboard_before=set(bpy.data.objects)
 with offset_group(y=5.1-c['geometry']['depth']):
  b('Bedside_cupboard',(2.57,1.67,.32),(.80,.58,.64),'red')
  b('Bedside_cupboard_top',(2.57,1.67,.675),(.88,.64,.07),'red')
  inset('Bedside_panel',2.57,1.368,.34,.67,.52)
  b('Bedside_key_bow',(2.45,1.65,.72),(.09,.09,.018),'yellow')
  b('Bedside_key_shaft',(2.60,1.65,.72),(.23,.023,.018),'yellow')
  b('Bedside_key_tooth',(2.68,1.68,.72),(.025,.07,.018),'yellow')
 bpy.context.view_layer.update()
 front_offset=5.1-c['geometry']['depth']
 cupboard_transform=Matrix.Translation((3.98,1.39+front_offset,0)) @ Matrix.Rotation(-math.pi/2,4,'Z') @ Matrix.Translation((-2.57,-1.67-front_offset,0))
 for obj in set(bpy.data.objects)-cupboard_before:obj.matrix_world=cupboard_transform @ obj.matrix_world
 with offset_group(y=5.1-c['geometry']['depth']):
  plant(g,-3.45,1.18,1.25,'purple')
 # Compact ceiling fixture: black upright, two aqua shades and white glints.
 g.cyl('Pendant_stem',(-1.20,4.00,2.94),.025,.36,'black')
 for side in [-1,1]:
  x=-1.20+side*.32
  curved_line(g,'Pendant_arm',[(-1.20,4,2.77),(x,4,2.85),(x,4,2.98)],.024,'black')
  g.sphere('Pendant_black_cup',(x,4,2.96),(.16,.12,.065),'black')
  glow=g.sphere('Pendant_aqua_shade',(x,4,3.005),(.13,.10,.09),'aqua')
  glow['bake_unlit']=True;glow['bake_no_shadow']=True
  glint=g.sphere('Pendant_glint',(x-.04,3.91,3.025),(.035,.012,.035),'white');glint['bake_unlit']=True;glint['bake_no_shadow']=True
 finish(c)
