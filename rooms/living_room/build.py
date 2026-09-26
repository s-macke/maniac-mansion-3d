"""Independent room 003 reconstruction. Original source pixels remain unchanged."""
import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config,save_generated,manifest_path
from blender_shared.geometry import Geometry,linear
config=load_config(OUT/'room.json',prepare=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.engine='CYCLES';scene.cycles.samples=24
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB'
bpy.context.preferences.filepaths.save_version=0
colors={'black':(0,0,0),'red':(168,0,0),'brown':(168,84,0),'yellow':(252,252,84),'blue':(0,0,168),'lightblue':(84,84,252),'purple':(168,0,168),'pink':(252,84,252),'white':(252,252,252),'gray':(168,168,168),'cyan':(0,168,168),'aqua':(84,252,252)}
mats={}
def material(rgb):
 name='EGA_'+('_'.join(map(str,rgb)))
 m=bpy.data.materials.get(name)
 if m:return m
 m=bpy.data.materials.new(name);m.diffuse_color=(*[linear(v) for v in rgb],1);m.use_nodes=True
 n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=m.diffuse_color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);return m
for name,rgb in colors.items():mats[name]=material(rgb)
collections={}
for name in ['Architecture','Furniture','Windows','Artwork','Chandelier','Cameras','Reference','Connection_ports']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
geo=Geometry(collections,mats);box,mesh,beam,cyl,sphere,put,camera=[getattr(geo,k) for k in ['box','mesh','beam','cyl','sphere','put','camera']]
image=bpy.data.images.load(str(ROOT/'source/room 003.png'));image.pack();pixels=list(image.pixels[:]);W,H=image.size
# Exact source pixels as colored runs, with DOS 1.2 vertical aspect correction.
def clip_outline(points,outline):
 # Clip a face to the clockwise radio casing outline in world X/Z coordinates.
 for a,b in zip(outline,outline[1:]+outline[:1]):
  def side(p):return (b[0]-a[0])*(p[2]-a[1])-(b[1]-a[1])*(p[0]-a[0])
  result=[]
  for p,q in zip(points,points[1:]+points[:1]):
   sp,sq=side(p),side(q)
   if sp<=1e-9:result.append(p)
   if (sp<=0)!=(sq<=0):
    t=sp/(sp-sq);result.append(tuple(v+(w-v)*t for v,w in zip(p,q)))
  points=result
  if len(points)<3:return []
 return points

def art(name,rect,x,y,z,width,height=None,outline=None):
 u0,v0,u1,v1=rect;pitch=width/(u1-u0);vertical=(height/(v1-v0) if height is not None else pitch*1.2);vs=[];fs=[];mi=[];materials=[]
 for v in range(v0,v1):
  u=u0
  def color(k):
   off=((H-1-v)*W+k)*4;return tuple(round(pixels[off+i]*255) for i in range(3))
  if name=='Original_radio_face':
   # Outer ink contour, excluding the wallpaper and cabinet outside the radio.
   edge=[k for k in range(u0,u1) if color(k)==(0,0,0)]
   lo,hi=(min(edge),max(edge)+1) if v<84 else (116,140)
   u=lo
  else:hi=u1
  while u<hi:
   rgb=color(u);end=u+1
   while end<hi and color(end)==rgb:end+=1
   if name=='Original_floor_mark' and rgb in {(84,84,252),(0,0,168),(0,0,0)}:u=end;continue
   m=material(rgb)
   if m not in materials:materials.append(m)
   a=x-width/2+(u-u0)*pitch;b=x-width/2+(end-u0)*pitch;bottom=z+(v1-v-1)*vertical;top=bottom+vertical
   points=[(a,y,bottom),(b,y,bottom),(b,y,top),(a,y,top)]
   if outline:points=clip_outline(points,outline)
   if len(points)>=3:
    i=len(vs);vs.extend(points);fs.append(tuple(range(i,i+len(points))));mi.append(materials.index(m))
   u=end
 o=mesh(name,vs,fs,None)
 for m in materials:o.data.materials.append(m)
 for p,i in zip(o.data.polygons,mi):p.material_index=i
 o['reference']='source/room 003.png';return o
# Long red room with blue carpet and narrow vertical gold/black wallpaper stripes.
geo.active='Architecture'
open_left=next(p for p in config['ports'] if p['id']=='left_door')['state']=='open'
box('Carpet',(0,2.8,-.08),(12.8,5.8,.16),'lightblue')
box('Back_wall',(0,5.72,1.75),(13,.24,3.5),'red')
if open_left:
 for a,b in [(0,2.475),(3.525,5.6)]:box('Left_wall',(-6.52,(a+b)/2,1.75),(.24,b-a,3.5),'red')
 box('Left_door_header',(-6.52,3,3.125),(.24,1.05,.75),'red')
else:box('Left_wall',(-6.52,2.8,1.75),(.24,5.6,3.5),'red')
for a,b in [(0,2.1),(3.9,5.6)]:box('Right_wall',(6.52,(a+b)/2,1.75),(.24,b-a,3.5),'red')
box('Right_door_header',(6.52,3,3.225),(.24,1.8,.55),'red')
box('Front_inferred_wall',(0,-.12,1.75),(13,.24,3.5),'red');box('Ceiling_living',(0,2.8,3.6),(13,5.8,.2),'red')
for i in range(83):
 x=-6.35+i*.155
 box('Wallpaper_ink',(x,5.579,1.94),(.05,.02,3.08),'black')
 box('Wallpaper_gold',(x+.039,5.563,1.94),(.016,.018,3.08),'brown')
for z,h,mat in [(.10,.16,'red'),(.23,.045,'black'),(.28,.035,'yellow'),(3.45,.06,'brown')]:
 box('Back_trim',(0,5.52,z),(12.8,.12,h),mat)
 for x in [-6.39,6.39]:
  cuts=[(0,2.475),(3.525,5.6)] if open_left and x<0 and z<2.75 else ([(0,2.1),(3.9,5.6)] if x>0 and z<2.95 else [(0,5.6)])
  for a,b in cuts:box('Side_trim',(x,(a+b)/2,z),(.12,b-a,h),mat)
# Doors are independent closed leaves with named future connection markers.
for name,x,rot,width in [('Left_door',-6.4,math.pi/2,1.05),('Right_double_door',6.4,-math.pi/2,1.8)]:
 geo.door(name,0,width,2.75 if x<0 and open_left else 2.95,(x,3.0),rot,double=width>1.5)
 if x<0 and open_left:
  for o in list(bpy.data.objects):
   if o.name.startswith(('Left_door_leaf','Left_door_raised_panel','Left_door_knob')):bpy.data.objects.remove(o,do_unlink=True)
# The source double door has a straight lintel, unlike the hall entrance.
for o in list(bpy.data.objects):
 if o.name.startswith('Right_double_door_transom'):bpy.data.objects.remove(o,do_unlink=True)
# Tufted sofa: shaped back, rolled arms, cushions, and turned wooden feet.
geo.active='Furniture'
def rounded(name,loc,size,mat,bevel=.10):
 o=box(name,loc,size,mat);b=o.modifiers.new('Soft upholstery edges','BEVEL');b.width=bevel;b.segments=3
 bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.modifier_apply(modifier=b.name);o.select_set(False);return o
for x in [-1.52,1.52]:
 for y in [3.86,4.72]:
  cyl('Sofa_wood_leg',(x,y,.19),.085,.38,'brown',10);cyl('Leg_collar',(x,y,.29),.11,.055,'yellow',10)
rounded('Sofa_base',(0,4.31,.43),(3.5,1.25,.30),'purple',.09)
for x in [-1.03,0,1.03]:rounded('Seat_cushion',(x,4.15,.66),(1.02,1.00,.27),'pink',.09)
# Arched upholstered back with a solid silhouette, rather than a flat billboard.
outline=[(-1.64,.68),(-1.68,1.12),(-1.5,1.40),(-1.0,1.56),(-.5,1.63),(0,1.66),(.5,1.63),(1,1.56),(1.5,1.4),(1.68,1.12),(1.64,.68)]
vs=[(x,y,z) for y in [4.65,4.96] for x,z in outline];n=len(outline)
mesh('Sofa_arched_back',vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'pink')
for x in [-1.64,1.64]:
 rounded('Sofa_rolled_arm',(x,4.24,.89),(.40,1.30,.56),'purple',.18)
 sphere('Arm_scroll',(x,3.60,.99),(.22,.13,.22),'pink')
 beam('Sofa_gold_arm_front',(x,3.62,.25),(x,3.62,.88),.075,'brown')
for x in [-.65,0,.65]:
 for z in [1.03,1.34]:
  sphere('Tuft_button',(x,4.635,z),(.042,.018,.034),'purple')
  for dx,dz in [(-.16,-.10),(.16,-.10),(-.16,.10),(.16,.10)]:beam('Tuft_seam',(x,4.64,z),(x+dx,4.64,z+dz),.014,'purple')
box('Sofa_front_wood_rail',(0,3.65,.36),(3.35,.10,.065),'brown')
box('Sofa_front_gold_edge',(0,3.59,.395),(3.35,.018,.021),'yellow')
# Radio on its small cabinet, at the left of the seating arrangement.
for x in [-5.12,-4.08]:
 for y in [4.51,5.13]:box('Radio_cabinet_leg',(x,y,.24),(.085,.085,.48),'brown')
box('Radio_cabinet',(-4.6,4.82,.52),(1.22,.76,.47),'brown');box('Cabinet_top',(-4.6,4.80,.80),(1.35,.86,.10),'brown')
box('Cabinet_drawer_ink',(-4.6,4.419,.57),(.99,.02,.25),'black');box('Cabinet_drawer',(-4.6,4.398,.57),(.91,.025,.19),'brown');box('Drawer_handle',(-4.6,4.37,.60),(.20,.035,.045),'yellow')
# Curved radio cabinet carries the original grille and dial pixels.
profile=[(-.41,0),(-.41,.30),(-.32,.52),(-.16,.64),(0,.69),(.16,.64),(.32,.52),(.41,.30),(.41,0)]
vs=[(-4.6+x,y,.85+z) for y in [4.65,5.02] for x,z in profile];n=len(profile)
mesh('Radio_arched_case',vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'brown')
geo.active='Artwork';art('Original_radio_face',(116,62,140,87),-4.6,4.638,.85,.79,height=.66,outline=[(-4.6+x,.85+z) for x,z in profile])
# Cut real openings behind the original curtains and broken-pane linework.
from blender_shared.windows import cut_wall
geo.active='Architecture'
holes=[(x-.84,x+.84,.65,3.30) for x in [-2.92,2.92]]
for prefix in ['Back_wall','Wallpaper_ink','Wallpaper_gold']:
 cut_wall(geo,prefix,holes)
geo.active='Windows'
for x,rect in [(-2.92,(175,16,242,100)),(2.92,(390,16,458,100))]:
 # Black inside the pane becomes open space. Retain black curtain contours by
 # flood-filling only the blue/black pane components, bounded by colored cloth.
 u0,v0,u1,v1=rect
 def rgb(u,v):
  off=((H-1-v)*W+u)*4;return tuple(round(pixels[off+i]*255) for i in range(3))
 pane=set();todo=[(u,v) for v in range(v0+9,v1-7) for u in range(u0+5,u1-5) if rgb(u,v)==(0,0,168)]
 while todo:
  u,v=todo.pop()
  if (u,v) in pane or not(u0+5<=u<u1-5 and v0+9<=v<v1-7) or rgb(u,v) not in [(0,0,0),(0,0,168)]:continue
  pane.add((u,v));todo.extend([(u-1,v),(u+1,v),(u,v-1),(u,v+1)])
 # Exact colored runs are retained, with only the pane's black faces removed.
 o=art('Original_window_and_drapes',rect,x,5.525,.57,1.85)
 pitch=1.85/(u1-u0);vertical=pitch*1.2
 import bmesh
 bm=bmesh.new();bm.from_mesh(o.data)
 for f in list(bm.faces):
  c=f.calc_center_median();u=int((c.x-(x-.925))/pitch)+u0;v=v1-1-int((c.z-.57)/vertical)
  if (u,v) in pane and rgb(u,v)==(0,0,0):bm.faces.remove(f)
 bm.to_mesh(o.data);bm.free()
 for dx in [-.84,.84]:box('Window_jamb',(x+dx,5.81,1.975),(.07,.38,2.65),'brown')
 for z in [.65,3.30]:box('Window_reveal',(x,5.81,z),(1.75,.38,.065),'brown')
 # Enclosed black night beyond the wall, not an opaque pane at the frame.
 for label,loc,size in [
  ('Night',(x,24,1.8),(3.6,.04,8)),
  ('Night_side',(x-1.8,15,1.8),(.04,18,8)),
  ('Night_side',(x+1.8,15,1.8),(.04,18,8)),
  ('Night_top',(x,15,5.8),(3.6,18,.04)),
  ('Night_bottom',(x,15,-2.2),(3.6,18,.04))]:
  o=box(label,loc,size,'black');o['bake_unlit']=True;o['bake_no_shadow']=True;o['bake_group']='Living_window_sky'
 for dx in [-.90,.90]:
  for j in range(3):beam('Velvet_curtain_fold',(x+dx+(j-1)*.033,5.49-j*.015,.60),(x+dx+(j-1)*.026,5.49-j*.015,2.72),.05,'purple' if j%2 else 'pink')
 box('Window_sill',(x,5.48,.53),(2.0,.38,.09),'brown')
# Landscape artwork in its gold frame; original pixels, not a new painting.
geo.active='Artwork';box('Painting_frame',(4.67,5.535,2.61),(1.49,.12,.99),'brown')
art('Original_landscape',(480,21,537,56),4.67,5.47,2.15,1.43)
# Crystal chandelier with chains, curved arms, candles and hanging facets.
geo.active='Chandelier'
cyl('Ceiling_rose',(0,3.45,3.46),.16,.06,'yellow')
beam('Chandelier_chain',(0,3.45,3.46),(0,3.45,2.95),.033,'brown')
cyl('Chandelier_stem',(0,3.45,2.82),.055,.38,'yellow')
for i in range(8):
 a=i*math.tau/8;end=Vector((math.cos(a)*.57,3.45+math.sin(a)*.57,2.70));mid=Vector((math.cos(a)*.34,3.45+math.sin(a)*.34,2.51))
 beam('Chandelier_arm',(0,3.45,2.75),mid,.028,'yellow');beam('Chandelier_arm_up',mid,end,.028,'yellow')
 cyl('Candle_cup',end,.075,.035,'brown');cyl('Candle',(end.x,end.y,2.80),.023,.19,'white',8)
 sphere('Candle_flame',(end.x,end.y,2.93),(.028,.028,.057),'yellow')
 for j in range(1,5):
  t=j/5;p=Vector((0,3.45,3.10)).lerp(end,t);p.z-=math.sin(t*math.pi)*.17;sphere('Crystal_bead',p,(.025,.025,.043),'white')
 beam('Crystal_drop_wire',mid,mid-Vector((0,0,.17)),.012,'gray');sphere('Crystal_drop',mid-Vector((0,0,.20)),(.036,.036,.075),'aqua')
for o in collections['Chandelier'].objects:
 if o.name.startswith('Candle_flame'):o['bake_unlit']=True;o['bake_no_shadow']=True
# The irregular pale floor mark in the source, represented as a shallow pixel patch.
geo.active='Artwork'
o=art('Original_floor_mark',(271,108,370,128),0,0,0,2.5)
# Rotate the art plane onto the carpet; blue source pixels match the carpet palette.
o.rotation_euler.x=-math.pi/2;o.location=(0,2.98,.012)
# Put the left shared wall on this room's side of the threshold plane.
if open_left:
 for o in bpy.data.objects:
  if o.type=='MESH' and (o.name.startswith(('Left_wall','Left_door')) or (o.name.startswith('Side_trim') and o.location.x<0)):o.location.x+=.24
geo.active='Cameras'
camera('01_Reference',(0,-13,4.4),(0,4.2,1.6),lens=43)
camera('02_Inside',(-4.9,.65,1.62),(.0,4.7,1.57),lens=20)
camera('04_Radio',(-5.35,3.15,1.62),(-4.6,4.75,1.12),lens=52)
camera('03_Reverse',(4.8,4.1,1.62),(-2.4,2.2,1.3),lens=20)
scene.camera=bpy.data.objects['02_Inside'];scene.render.resolution_x=1280;scene.render.resolution_y=800
for p in config['ports']:
 o=bpy.data.objects.new('PORT_'+p['id'],None);collections['Connection_ports'].objects.link(o);o.location=p['position'];o.empty_display_type='ARROWS';o.empty_display_size=.4;o['outward']=p['outward'];o['state']=p['state']
scene['room_id']='003';scene['style']='Original EGA colors, static soft cel lighting';scene['limitations']='Independent review; closed doors; inferred room depth and unseen front wall.'
# The living room owns the library double door, opening into the furnished room.
for o in bpy.data.objects:
 if o.type=='MESH' and (o.name.startswith(('Right_wall','Right_door_header','Right_double_door')) or (o.name.startswith('Side_trim') and o.location.x>0)):o.location.x-=.24
bpy.context.view_layer.update()
library_leaves=[]
for i,leaf in enumerate(sorted([o for o in bpy.data.objects if o.name.startswith('Right_double_door_leaf')],key=lambda o:o.name)):
 pose=leaf.matrix_world@Matrix.Diagonal(Vector((.89*(-1 if i==0 else 1),1,2.85,1)))
 hinge=Vector((leaf.location.x,3.9 if i==0 else 2.1,0));library_leaves.append((pose,hinge,-math.pi/2 if i==0 else math.pi/2))
for o in list(bpy.data.objects):
 if o.name.startswith(('Right_double_door_leaf','Right_double_door_raised_panel','Right_double_door_knob')):bpy.data.objects.remove(o,do_unlink=True)
from blender_shared.door_assets import register
register(config,[('Left_door', 1.05, 2.75), ('Right_double_door', 1.8, 2.95)])
from blender_shared.door_assets import register_hinged
for i,(pose,hinge,angle) in enumerate(library_leaves):
 register_hinged(config,'Standard_leaf',pose,hinge,angle,collections['Architecture'],port='right_double_door',node='Door_library_'+str(i),label='Library doors',instance_id='Library_leaf_'+str(i),append_leaf=i>0)
from blender_shared.opposite_walls import apply as opposite_walls
opposite_walls(geo,config)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('LIVING_ROOM_SOURCE_COMPLETE',flush=True)

save_generated(config)
