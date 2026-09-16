"""Reproducible EGA porch and exterior; original PNGs are read-only references."""
import bpy,math,json,sys,random
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config,save_generated,manifest_path
from blender_shared.geometry import Geometry,linear
config=load_config(OUT/'room.json',prepare=True)
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene
scene.world=bpy.data.worlds.new('Night');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.image_settings.file_format='PNG';scene.render.resolution_percentage=100
scene.unit_settings.system='METRIC';bpy.context.preferences.filepaths.save_version=0
colors={'black':(0,0,0),'red':(168,0,0),'brown':(168,84,0),'yellow':(252,252,84),'blue':(0,0,168),'lightblue':(84,84,252),'white':(252,252,252),'gray':(168,168,168),'darkgray':(84,84,84),'cyan':(0,168,168),'aqua':(84,252,252),'green':(0,168,0),'lime':(84,252,84)}
mats={}
for name,rgb in colors.items():
 m=bpy.data.materials.new('EGA_'+name);m.diffuse_color=(*[linear(v) for v in rgb],1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=m.diffuse_color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);mats[name]=m
collections={}
for name in config['bake']['collections']+['Cameras','Connection_ports']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
geo=Geometry(collections,mats);box,mesh,beam,cyl,sphere,camera=[getattr(geo,n) for n in ['box','mesh','beam','cyl','sphere','camera']]
# Facade stays on the exterior half of the entrance plane; hall owns the doors.
geo.active='Architecture'
box('Facade',((8+.925)/2,-.11,3.65),(8-.925,.22,7.3),'gray')
# Independent exterior space owns a complete facade, including behind upstairs rooms.
box('Facade',((-8-.925)/2,-.11,3.65),(8-.925,.22,7.3),'gray')
box('Door_header',(0,-.11,5.24),(1.85,.22,4.12),'gray')
for z in [i*.24 for i in range(31)]:
 for a,b in ([(-8,-.925),(.925,8)] if z<3.25 else [(-8,8)]):box('Siding_joint',((a+b)/2,-.235,z),(b-a,.012,.028),'darkgray')
for x,z0,z1 in [(-8,0,7.3),(8,0,7.3)]:box('Corner_board',(x,-.25,(z0+z1)/2),(.15,.13,z1-z0),'brown')
# Narrow black windows with the original red/yellow sash and cyan reflection.
def window(x,z,w=.90,h=1.9):
 box('Window_frame',(x,-.30,z),(w+.14,.16,h+.14),'brown')
 box('Window_ink',(x,-.39,z),(w+.07,.04,h+.07),'black')
 for dx in [-w/2,w/2]:box('Window_red_sash',(x+dx,-.42,z),(.055,.05,h),'red')
 for dz in [-h/2,0,h/2]:box('Window_sash',(x,-.43,z+dz),(w,.05,.045),'brown')
 box('Window_gold_edge',(x-w/2+.065,-.445,z),(.018,.015,h-.08),'yellow')
 for dz in [-.35,.5]:
  beam('Window_cyan_glint',(x-w*.28,-.455,z+dz),(x-w*.13,-.455,z+dz+.09),.025,'cyan')
 box('Window_sill',(x,-.43,z-h/2-.10),(w+.23,.26,.12),'gray')
for x in [-6.7,-4.9,-3.1,3.1,4.9,6.7]:window(x,1.85)
for x in [-6.3,-3.7,0,3.7,6.3]:window(x,5.5,1.05,1.65)
# Two-sided entrance frame; the actual open double leaves belong to the hall.
for x in [-1.04,1.04]:box('Entrance_post',(x,-.27,1.63),(.16,.24,3.26),'brown')
box('Entrance_lintel',(0,-.27,3.25),(2.24,.24,.15),'brown')
# Porch, red foundation brickwork, turned columns and a gap for the stair.
geo.active='Porch'
grate=config['geometry']['grating'];gx,gy,gz=grate['x'],grate['y'],grate['z'];gw,gh=grate['width'],grate['height']
gl,gr=gx-gw/2,gx+gw/2;gb,gt=gz-gh/2,gz+gh/2
# A genuine recess in the brickwork, with its closed metal grille in front.
for lo,hi in [(-8.25,gl),(gr,8.25)]:box('Porch_foundation',((lo+hi)/2,-1.1,-.63),(hi-lo,2.2,1.14),'red')
for lo,hi in [(-1.2,gb),(gt,-.06)]:box('Grating_brick_header_sill',(gx,-1.1,(lo+hi)/2),(gw,2.2,hi-lo),'red')
# The portal supplies the view through the recess.
for x in [gl,gr]:
 box('Grating_reveal',(x,gy+.15,gz),(.05,.3,gh),'darkgray')
 box('Grating_metal_frame',(x,gy-.035,gz),(.07,.07,gh+.07),'gray')
 box('Grating_blue_edge',(x-.02,gy-.075,gz),(.018,.018,gh),'blue')
for z in [gb,gt]:box('Grating_metal_frame',(gx,gy-.035,z),(gw+.07,.07,.07),'gray')
from blender_shared.door_assets import register_hinged,KIT
config['geometry']['doors']=[];config['geometry']['sharedAssets']=[];config['sharedAssetLibrary']=KIT
register_hinged(config,'Grating_leaf',Matrix.Translation((gx,gy+.035,gz))@Matrix.Diagonal(Vector((gw-.08,1,gh-.08,1))),(gl+.04,gy+.035,gb),math.pi/2,collections['Porch'],port='under_porch_grating',node='Door_grating',label='Metal grating')
for x in [gl+.025,gr-.025]:
 for z in [gb+.025,gt-.025]:box('Grating_frame_bolt',(x,gy-.08,z),(.035,.02,.035),'white')
box('Porch_deck',(0,-1.1,-.06),(16.6,2.2,.12),'gray')
for row in range(4):
 z=-1.1+row*.26
 for lo,hi in ([(-8.25,gl),(gr,8.25)] if gb-.02<z<gt+.02 else [(-8.25,8.25)]):box('Brick_mortar',((lo+hi)/2,-2.207,z),(hi-lo,.012,.018),'brown')
 for i in range(33):
  x=-8.1+i*.5+(row%2)*.25
  for lo,hi in ([ (z+.015,min(z+.245,gb)),(max(z+.015,gt),z+.245)] if gl-.015<x<gr+.015 else [(z+.015,z+.245)]):
   if hi>lo:box('Brick_joint',(x,-2.21,(lo+hi)/2),(.018,.014,hi-lo),'brown')
for i in range(8):
 front=-4.6+i*.3;top=-1.2+(i+1)*.15
 box('Entrance_step',(0,(front-2.2)/2,(top-1.2)/2),(3,(-2.2-front),top+1.2),'darkgray')
 box('Step_nosing',(0,front-.008,top-.015),(3,.055,.035),'gray')
for side in [-1,1]:
 beam('Stair_side', (side*1.64,-4.65,-1.12),(side*1.64,-2.15,.17),.20,'gray')
 box('Stair_foot',(side*1.68,-4.65,-.92),(.34,.4,.56),'darkgray');sphere('Stair_finial',(side*1.68,-4.65,-.55),(.20,.20,.19),'gray')
for x in [-7.7,-4.6,-1.7,1.7,4.6,7.7]:
 box('Column_square_base',(x,-1.8,.12),(.29,.29,.24),'brown')
 top=3.805
 cyl('Porch_column',(x,-1.8,(.155+top)/2),.085,top-.155,'brown',8)
 for z in [.3,.9,3.2,3.7]:cyl('Column_collar',(x,-1.8,z),.14,.13,'red',8)
for a,b in [(-8.2,-1.8),(1.8,8.2)]:
 for z in [.22,1.02]:box('Porch_rail',((a+b)/2,-2,z),(b-a,.17,.12),'red')
 box('Rail_gold_edge',((a+b)/2,-2.09,1.055),(b-a,.025,.025),'brown')
 for i in range(int((b-a)/.36)+1):
  x=a+i*.36;box('Baluster',(x,-2,.61),(.09,.1,.73),'brown');box('Baluster_neck',(x,-2,.72),(.14,.13,.12),'yellow')
# Shallow canopy, gables and the blue-gray tower silhouette from background 047.
def roof(name,x,y,z,w,d,rise):
 v=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x,y-d/2,z+rise),(x-w/2,y+d/2,z),(x+w/2,y+d/2,z),(x,y+d/2,z+rise)]
 mesh(name,v,[(0,1,2),(3,5,4)],'darkgray');mesh(name+'_slopes',v,[(0,2,5,3),(2,1,4,5)],'blue')
 for a,b in [(0,2),(2,1),(0,1)]:beam(name+'_edge',v[a],v[b],.11,'lightblue')
geo.active='Architecture'
# The exterior canopy is continuous; independent upstairs spaces cannot intersect it.
for a,b,z in [(-8.45,8.45,3.91)]:
 box('Porch_canopy',((a+b)/2,-1.3,z),(b-a,3,.20),'darkgray')
 box('Canopy_red_fascia',((a+b)/2,-2.82,z-.04),(b-a,.12,.22),'brown')
roof('Entrance_gable',0,-1.35,3.98,3.8,3.1,1.55)
# Background 047: low linking roofs, narrow left turret, central cupola,
# and a lower square right tower. All roof volumes stay above the hall ceiling.
def hip_roof(name,x,y,z,w,d,rise,ridge=.5):
 v=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z),
    (x-ridge/2,y,z+rise),(x+ridge/2,y,z+rise)]
 mesh(name,v,[(0,1,5,4)],'lightblue')
 mesh(name+'_sides',v,[(1,2,5),(2,3,4,5),(3,0,4)],'blue')
 for a,b in [(0,1),(1,2),(2,3),(3,0),(4,5)]:beam(name+'_rim',v[a],v[b],.10,'cyan')
 for a,b in [(0,4),(1,5)]:beam(name+'_hip',v[a],v[b],.055,'blue')
hip_roof('Main_hip_roof',0,2,7.36,17,5,1.2,11)
# Horizontal cornices and narrow black openings follow the source's pixel bands.
def tower(name,x,y,z,w,d,h,levels):
 box(name,(x,y,z+h/2),(w,d,h),'gray')
 box(name+'_side_shadow',(x+w/2+.015,y,z+h/2),(.03,d,h),'darkgray')
 for elevation in [z+.1,z+h]+levels:
  box(name+'_cornice',(x,y,elevation),(w+.28,d+.24,.16),'blue')
  box(name+'_front_cornice',(x,y-d/2-.15,elevation+.04),(w+.3,.08,.13),'cyan')
 for elevation in levels:
  for dx in [-w*.24,w*.24]:
   box(name+'_window',(x+dx,y-d/2-.035,elevation+.76),(w*.23,.065,1.05),'black')
   box(name+'_window_reveal',(x+dx-w*.115-.055,y-d/2-.08,elevation+.76),(.095,.06,1.17),'lightblue')
   box(name+'_window_sill',(x+dx,y-d/2-.11,elevation+.2),(w*.26,.13,.10),'darkgray')
tower('Central_tower',-2.9,2,7.4,3.1,3.3,5.4,[8.05,10.35])
# Faceted cupola: real curved roof volume, not a triangular front billboard.
cx,cy=-2.9,2;segments=12
rings=[(12.86,1.85),(13.12,1.8),(13.62,1.6),(14.12,1.23),(14.48,.68),(14.62,.15)]
vs=[(cx+r*math.cos(i*math.tau/segments),cy+r*math.sin(i*math.tau/segments),z) for z,r in rings for i in range(segments)]
for i in range(segments):
 faces=[(j*segments+i,j*segments+(i+1)%segments,(j+1)*segments+(i+1)%segments,(j+1)*segments+i) for j in range(len(rings)-1)]
 mesh('Cupola_roof',vs,faces,'lightblue' if math.sin((i+.5)*math.tau/segments)<-.25 else 'blue')
cyl('Cupola_eave',(cx,cy,12.88),1.9,.14,'cyan',segments)
beam('Cupola_finial',(cx,cy,14.6),(cx,cy,15.45),.09,'cyan')
sphere('Cupola_finial_cap',(cx,cy,15.45),(.11,.11,.11),'aqua')
# Slender left turret echoes the small pointed shape alongside the cupola.
tower('Left_turret',-6.4,1.15,7.4,1.8,2.2,3.1,[7.75])
roof('Left_turret_gable',-6.4,1.15,10.6,2.25,2.55,1.55)
# Small dark opening in the gable, with a gray surround.
box('Turret_attic_reveal',(-6.4,-.14,11.1),(.65,.08,.77),'gray')
box('Turret_attic_window',(-6.4,-.19,11.1),(.35,.05,.64),'black')
beam('Left_turret_spire',(-6.4,1.15,12.15),(-6.4,1.15,12.9),.075,'cyan')
tower('Right_tower',3.1,1.6,7.4,3.1,3.2,3.2,[7.9])
hip_roof('Right_tower_hip',3.1,1.6,10.7,3.8,3.9,1.55,.35)
beam('Right_tower_spire',(3.1,1.6,12.25),(3.1,1.6,13.05),.075,'cyan')
# Short ridge chimney silhouettes at the rear, visible in the distant original.
for x in [5.2,6.25]:
 box('Rear_chimney',(x,3.9,9.0),(.48,.55,1.6),'darkgray')
 box('Chimney_cap',(x,3.9,9.83),(.64,.68,.14),'gray')
# Night grounds and short gravel approach, clear of porch/stair collision.
geo.active='Ground'
box('Lawn',(0,-8,-1.26),(26,16,.12),'green')
mesh('Gravel_path',[(-1.48,-4.7,-1.194),(1.48,-4.7,-1.194),(2.1,-16,-1.194),(-2.1,-16,-1.194)],[(0,1,2,3)],'gray')
rng=random.Random(1)
for i in range(260):
 y=rng.uniform(-15.8,-4.75);x=rng.uniform(-1.4,1.4);size=rng.uniform(.02,.06)
 box('Gravel_pixel',(x,y,-1.184),(size,size,.01),'white' if i%3==0 else 'darkgray')
geo.active='Details'
# Irregular leaf-covered shrubs on both sides of the steps. A separate seed
# preserves the existing gravel and star arrangement when foliage is rebuilt.
foliage=random.Random(31)
for index,bush in enumerate(config['geometry']['bushes']):
 x,y=bush['x'],bush['y'];prefix='Left_bush' if x<0 else 'Right_bush'
 for dx,dy,sx,sy,sz in [(-.48,.06,.50,.46,.42),(0,0,.62,.51,.53),(.48,.04,.49,.45,.46)]:
  sphere(prefix+'_foliage',(x+dx,y+dy,-.73),(sx,sy,sz),'green')
 vs=[];fs=[];indices=[]
 for i in range(240):
  angle=foliage.uniform(0,math.tau);elev=foliage.uniform(-.55,1.45)
  nx,ny,nz=math.cos(angle)*math.cos(elev),math.sin(angle)*math.cos(elev),math.sin(elev)
  center=Vector((x+nx*.94,y+ny*.54,-.73+nz*.52))
  normal=Vector((nx/.94,ny/.54,nz/.52)).normalized();tangent=normal.cross(Vector((0,0,1)))
  if tangent.length<.01:tangent=Vector((1,0,0))
  tangent.normalize();up=normal.cross(tangent).normalized();size=foliage.uniform(.045,.095)
  start=len(vs);vs.extend([center+tangent*size,center+up*size*.7,center-tangent*size,center-up*size*.7]);fs.append(tuple(range(start,start+4)));indices.append(1 if i%4==0 else 0)
 o=mesh(prefix+'_leaves',vs,fs,None)
 for name in ['green','lime']:o.data.materials.append(mats[name])
 for face,index in zip(o.data.polygons,indices):face.material_index=index
# Mailbox and parcel at the left of the approach, as in room 001.
box('Mailbox_post',(-6,-5.6,-.4),(.13,.13,1.6),'brown');box('Mailbox',(-6,-5.6,.42),(.65,.4,.4),'cyan');box('Mailbox_slot',(-6,-5.82,.47),(.3,.02,.05),'black')
box('Parcel',(-5.1,-5.6,-1.02),(.65,.46,.34),'brown')
for x in [-5.3,-4.9]:box('Parcel_band',(x,-5.84,-1.02),(.035,.02,.34),'yellow')
for x in [7,8.4,9.8]:
 box('Gravestone',(x,-5.6,-.77),(.65,.18,.8),'cyan');sphere('Gravestone_round_top',(x,-5.6,-.37),(.325,.09,.23),'cyan')
 for z in [-.64,-.76,-.88]:box('Gravestone_engraving',(x,-5.7,z),(.40,.014,.025),'darkgray')
 # Readable R.I.P. built into the mesh, no browser font or texture download.
 curve=bpy.data.curves.new('RIP','FONT');curve.body='R.I.P.';curve.size=.19;curve.align_x='CENTER';o=bpy.data.objects.new('RIP',curve);collections['Details'].objects.link(o);o.location=(x,-5.71,-.55);o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(mats['black']);bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.convert(target='MESH');o.select_set(False)
for x,y,sgn in [(-10,-6,-1),(11,-7,1)]:
 trunk=[(x,y,-1.2),(x-.35*sgn,y,0),(x-.6*sgn,y,1.2),(x-.45*sgn,y,2.5)]
 for a,b in zip(trunk,trunk[1:]):beam('Bare_tree',a,b,.14,'darkgray')
 for z,side in [(0,-1),(.8,1),(1.5,-1)]:
  a=(x-.3*sgn,y,z);b=(x+side*.8,y-.15,z+.6);c=(x+side*1.1,y-.1,z+1.2)
  beam('Bare_branch',a,b,.09,'gray');beam('Bare_twig',b,c,.045,'gray');beam('Bare_fork',b,(b[0]+side*.4,y-.1,b[2]+.12),.045,'gray')
# Small fence limits the initial approach without inventing a route around the house.
for side in [-1,1]:
 for y in range(-15,-2):
  beam('Fence_picket',(side*12.5,y,-1.2),(side*12.5,y,.1),.055,'darkgray')
 for z in [-.7,-.1]:beam('Fence_rail',(side*12.5,-16,z),(side*12.5,-2,z),.055,'gray')
# Unlit sky accents retain their exact EGA colors and cast no exterior shadows.
geo.active='Sky'
for i in range(100):
 x=rng.uniform(-25,25);z=rng.uniform(5,24)
 box('Star',(x,11,z),(.035,.02,.035),'cyan')
center=Vector((8,10,17));r=2.0;verts=[tuple(center)]+[(center.x+math.cos(i*math.tau/64)*r,center.y,center.z+math.sin(i*math.tau/64)*r) for i in range(64)]
mesh('Moon',verts,[(0,i+1,(i+1)%64+1) for i in range(64)],'aqua')
for i in range(20):
 a=math.pi*.6+i*math.pi*.8/20;b=a+math.pi*.8/20
 mesh('Moon_bright_rim',[(8+math.cos(t)*rr,9.99,17+math.sin(t)*rr) for t,rr in [(a,2),(b,2),(b,1.82),(a,1.82)]],[(0,1,2,3)],'white')
for o in collections['Sky'].objects:o['bake_unlit']=True
geo.active='Cameras'
camera('01_Approach',(0,-15,.42),(0,0,5.5),lens=19)
camera('02_Porch',(-3,-5,1.4),(0,0,1.5),lens=22)
camera('04_Bushes',(0,-7,.7),(0,-2.7,-.35),lens=27)
camera('05_Grating',(-4.4,-2.9,.15),(-2.85,-2.18,-.7),lens=26)
camera('03_Overview',(15,-24,12),(0,-1,5),lens=35)
for port in config['ports']:
 o=bpy.data.objects.new('PORT_'+port['id'],None);collections['Connection_ports'].objects.link(o);o.location=port['position'];o.empty_display_type='ARROWS';o['state']=port['state']
scene.camera=bpy.data.objects['01_Approach'];scene['reference']='001 porch detail; 047 upper silhouette. Upper volume is an exterior study, not a finalized room envelope.'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('FRONT_EXTERIOR_SOURCE_COMPLETE',flush=True)

save_generated(config)
