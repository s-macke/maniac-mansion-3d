"""Extend the editable entrance into a continuous double-height hall and landing.
Generates entrance and landing directly from their room geometry recipes. Run with Blender in background mode.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector, Matrix
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config,save_generated,manifest_path
from blender_shared.geometry import Geometry, linear
CONFIG=load_config(OUT/'room.json',prepare=True)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from entrance import build_entrance
build_entrance()
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene
collections={n:bpy.data.collections[n] for n in ['Architecture','Doors','Staircase','Clock','Plants','Pixel_ornaments','Cameras','Collision','Reference']}
for name in ['Landing','Landing_art']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
mats={m.name.removeprefix('EGA_'):m for m in bpy.data.materials if m.name.startswith('EGA_')}
geo=Geometry(collections,mats)
put,box,mesh,beam,cyl,sphere,localbox,wall,door,camera=[getattr(geo,n) for n in ['put','box','mesh','beam','cyl','sphere','localbox','wall','door','camera']]
geo.active='Architecture'
if next(p for p in CONFIG['ports'] if p['id']=='right_side')['state']=='open':
 # Meet the neighboring carpet exactly, without coplanar floor overlap.
 floor=bpy.data.objects['Red_floor'];floor.scale.x=12.9/13;floor.location.x=-.05
for o in list(bpy.data.objects):
 if o.name.startswith(('Ceiling_','Stairwell_','Upper_landing_placeholder')):bpy.data.objects.remove(o,do_unlink=True)
# The gallery floor replaces the old upper strip of the rear downstairs wall.
for o in list(collections['Architecture'].objects):
 if not o.name.startswith('Back_'):continue
 inv=o.matrix_world.inverted();zs=[(o.matrix_world@v.co).z for v in o.data.vertices]
 if min(zs)>=3.18:bpy.data.objects.remove(o,do_unlink=True);continue
 for v in o.data.vertices:
  p=o.matrix_world@v.co;p.z=min(p.z,3.18);v.co=inv@p
for o in collections['Pixel_ornaments'].objects:o.location.z-=.25
# Double-height outer shell, following the same wall finish.
for name,width,origin,rot in [('Atrium_left',5.95,(-6.4,2.975),math.pi/2),('Atrium_right',5.95,(6.4,2.975),-math.pi/2),('Front_inferred_upper',12.8,(0,0),math.pi)]:
 before=set(bpy.data.objects);wall(name,width,origin,rot,[])
 for o in set(bpy.data.objects)-before:o.location.z+=3.36
# Match lower/upper shell joins cleanly: upper cladding overlaps only the hidden solid shell.
geo.active='Landing'
stair=CONFIG['geometry']['stair'];gallery=CONFIG['geometry']['gallery']
Z=stair['rise'];BACK=gallery['back'];EDGE=gallery['front'];TOP=stair['y']+stair['length']
# Preserve the staircase's angled final tread. The gallery floor meets that
# exact diagonal edge, so no gap or invisible threshold is needed.
N=stair['segments'];centers=[Vector((stair['x']+stair['sweep']*math.sin(i/N*math.pi*stair['angle']),stair['y']+stair['length']*i/N,0)) for i in range(N+1)]
p=centers[-1];tangent=(centers[-1]-centers[-2]).normalized();normal=Vector((tangent.y,-tangent.x,0))
left=p-normal*.825;right=p+normal*.825
boundary=[(-6.4,EDGE),(-1.15,EDGE),(left.x,left.y),(right.x,right.y),(1.55,EDGE),(6.4,EDGE)]
for i,(a,b) in enumerate(zip(boundary,boundary[1:])):
 quad=[a,b,(b[0],BACK),(a[0],BACK)]
 verts=[(x,y,z) for z in [Z-.20,Z] for x,y in quad]
 mesh('Gallery_floor_'+str(i),verts,[(4,5,6,7),(3,2,1,0),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7)],'red')
# Upper rear and side walls with real doorway apertures behind closed leaves.
for name,width,origin,rot,doors in [('Gallery_back',12.8,(0,BACK),0,[(.20,1.90,2.95)]),('Gallery_left',3.8,(-6.4,7.85),math.pi/2,[(.65,1.05,2.72)]),('Gallery_right',3.8,(6.4,7.85),-math.pi/2,[(-.65,1.05,2.72)])]:
 before=set(bpy.data.objects);wall(name,width,origin,rot,doors)
 for o in set(bpy.data.objects)-before:o.location.z+=Z
for name,u,origin,rot in [('Landing_left_door',.65,(-6.4,7.85),math.pi/2),('Landing_right_door',-.65,(6.4,7.85),-math.pi/2)]:
 before=set(bpy.data.objects);door(name,u,1.05,2.72,origin,rot)
 for o in set(bpy.data.objects)-before:o.location.z+=Z
# Visible wood fascia and a balustrade with an open stair arrival in its center.
def railing(a,b):
 beam('Gallery_rail_ink',(*a,Z+.99),(*b,Z+.99),.13,'black')
 beam('Gallery_rail_wood',(*a,Z+1.025),(*b,Z+1.025),.105,'brown')
 beam('Gallery_rail_highlight',(*a,Z+1.081),(*b,Z+1.081),.025,'yellow')
 length=math.dist(a,b);count=max(2,round(length/.29))
 for i in range(count+1):
  t=i/count;x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t
  cyl('Gallery_baluster',(x,y,Z+.49),.043,.86,'brown',8)
  for z in [.13,.74,.89]:cyl('Baluster_collar',(x,y,Z+z),.067,.065,'yellow',8)
 beam('Gallery_bottom_rail',(*a,Z+.08),(*b,Z+.08),.09,'brown')
railing((-6.35,EDGE),(-1.15,EDGE));railing((1.55,EDGE),(6.35,EDGE))
# Rails terminate at the same angled edge as the visible staircase.
railing((-1.15,EDGE),(left.x,left.y));railing((1.55,EDGE),(right.x,right.y))
# Source art is losslessly represented by flat colored runs, avoiding texture blur
# and allowing the same baked-vertex-color pipeline as the rest of the house.
geo.active='Landing_art'
image=bpy.data.images.load(str(ROOT/'source/room 011.png'));image.pack();pixels=list(image.pixels[:]);W,H=image.size
rgbmat={}
for m in mats.values():
 c=m.diffuse_color[:3]
 rgb=tuple(round((12.92*v if v<=.0031308 else 1.055*v**(1/2.4)-.055)*255) for v in c);rgbmat[rgb]=m

def artwork(name,rect,x,y,z,width,exclude=None):
 u0,v0,u1,v1=rect;pitch=width/(u1-u0);verts=[];faces=[];indices=[];materials=[]
 for v in range(v0,v1):
  u=u0
  while u<u1:
   def color(k):
    off=((H-1-v)*W+k)*4;return tuple(round(pixels[off+i]*255) for i in range(3))
   c=color(u);end=u+1
   while end<u1 and color(end)==c:end+=1
   if exclude is None or c not in exclude:
    if c not in rgbmat:
     m=bpy.data.materials.new('EGA_pixel_'+'_'.join(map(str,c)));m.diffuse_color=(*[linear(k) for k in c],1);m.use_nodes=True
     n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=m.diffuse_color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);rgbmat[c]=m
    m=rgbmat[c]
    if m not in materials:materials.append(m)
    a=x-width/2+(u-u0)*pitch;b=x-width/2+(end-u0)*pitch;lo=z+(v1-v-1)*pitch*1.2;hi=lo+pitch*1.2
    start=len(verts);verts.extend([(a,y,lo),(b,y,lo),(b,y,hi),(a,y,hi)]);faces.append((start,start+1,start+2,start+3));indices.append(materials.index(m))
   u=end
 obj=mesh(name,verts,faces,None)
 for m in materials:obj.data.materials.append(m)
 for face,i in zip(obj.data.polygons,indices):face.material_index=i
 obj['reference']='source/room 011.png';return obj
for x,rect in [(-2.25,(184,16,240,64)),(2.65,(376,17,434,65))]:
 geo.active='Landing';box('Portrait_frame_depth',(x,BACK-.10,Z+1.84),(1.45,.19,1.48),'brown')
 geo.active='Landing_art';artwork('Original_family_portrait',rect,x,BACK-.21,Z+1.12,1.40)
# Two illustrated lamps, with source silhouettes rather than a generic modern fixture.
for x,rect in [(-4.55,(103,0,145,46)),(4.85,(494,0,539,46))]:
 artwork('Original_wall_lamp',rect,x,BACK-.24,Z+2.02,.86,exclude={(0,168,168),(84,252,252),(0,0,0)})
# Finials at each gallery opening echo the source's stair-head ornaments.
geo.active='Landing'
for x in [-1.15,1.55]:
 box('Gallery_newel',(x,EDGE,Z+.56),(.24,.26,1.12),'brown')
 box('Gallery_newel_cap',(x,EDGE,Z+1.08),(.38,.38,.10),'yellow')
 sphere('Gallery_finial',(x,EDGE,Z+1.22),(.14,.11,.13),'brown')
 for dx in [-.10,0,.10]:
  bpy.ops.mesh.primitive_cone_add(vertices=4,radius1=.045,radius2=0,depth=.17,location=(x+dx,EDGE,Z+1.37));put(bpy.context.object,'Gallery_finial_crown','yellow')
geo.active='Architecture'
box('Ceiling_combined',(0,BACK/2,7.11),(13,BACK+.1,.20),'cyan')
# Existing cutaway behavior remains available, while all surfaces export normally.
for o in bpy.data.objects:
 if o.type=='MESH' and any(c.name in ['Architecture','Doors','Staircase','Clock','Plants','Pixel_ornaments','Landing','Landing_art'] for c in o.users_collection):o.hide_render=False
# The shared wall occupies the hall side of the port plane. Its neighboring
# room owns the other half; neither room's back faces intrude into the other.
if next(p for p in CONFIG['ports'] if p['id']=='right_side')['state']=='open':
 for o in bpy.data.objects:
  if o.type=='MESH' and o.name.startswith(('Right_','Atrium_right','Gallery_right')):o.location.x-=.22
CONFIG['geometry']['doors']=[]
def movable(parts,hinge,angle,node):
 bpy.context.view_layer.update()
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 for o in parts:o['door_node']=node;o['door_hinge']=list(hinge)
 return {'node':node,'hinge':list(hinge),'openAngle':angle,'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}
# One shared physical leaf, owned by the hall, swings inward around its south hinge.
if next(p for p in CONFIG['ports'] if p['id']=='right_side')['state']=='open':
 leaf=bpy.data.objects['Right_side_leaf']
 parts=[o for o in bpy.data.objects if o.name.startswith(('Right_side_leaf','Right_side_raised_panel','Right_side_knob'))]
 for o in list(parts):
  if o==leaf:continue
  back=o.copy();back.data=o.data.copy();collections['Doors'].objects.link(back)
  back.name=o.name+'_back';back.location.x=2*leaf.location.x-o.location.x;parts.append(back)
 bpy.context.view_layer.update()
 hinge=Vector((leaf.location.x,3.15-1.05/2,0))
 swing=Matrix.Translation(hinge)@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation(-hinge)
 for o in parts:o.matrix_world=swing@o.matrix_world
 bpy.context.view_layer.update()
 CONFIG['geometry']['doors'].append({'id':'living_door','label':'Living room door','port':'right_side','initialOpen':False,'leaves':[movable(parts,hinge,math.pi/2,'Door_living')]})
# Preserve both entrance leaves and swing them inward, one from each jamb.
if next(p for p in CONFIG['ports'] if p['id']=='entrance')['state']=='open':
 for o in bpy.data.objects:
  if o.type=='MESH' and o.name.startswith(('Left_','Atrium_left','Gallery_left','Front_double')):o.location.x+=.22
 floor=bpy.data.objects['Red_floor'];floor.scale.x=12.8/13;floor.location.x=0
 bpy.context.view_layer.update()
 leaves=sorted([o for o in bpy.data.objects if o.name.startswith('Front_double_leaf')],key=lambda o:o.location.y)
 entrance={'id':'front_doors','label':'Front doors','port':'entrance','initialOpen':False,'leaves':[]};CONFIG['geometry']['doors'].append(entrance)
 decorations=[o for o in bpy.data.objects if o.name.startswith(('Front_double_raised_panel','Front_double_knob'))]
 for i,leaf in enumerate(leaves):
  parts=[leaf]+[o for o in decorations if min(leaves,key=lambda l:abs(l.location.y-o.location.y))==leaf]
  for o in list(parts):
   if o==leaf:continue
   back=o.copy();back.data=o.data.copy();collections['Doors'].objects.link(back);back.name=o.name+'_back';back.location.x=2*leaf.location.x-o.location.x;parts.append(back)
  bpy.context.view_layer.update()
  hinge=Vector((leaf.location.x,2.35+(-1 if i==0 else 1)*1.85/2,0))
  swing=Matrix.Translation(hinge)@Matrix.Rotation((-1 if i==0 else 1)*math.pi/2,4,'Z')@Matrix.Translation(-hinge)
  for o in parts:o.matrix_world=swing@o.matrix_world
  bpy.context.view_layer.update()
  entrance['leaves'].append(movable(parts,hinge,(-1 if i==0 else 1)*math.pi/2,'Door_front_'+str(i)))
# The kitchen occupies the space behind the lower rear wall, below the gallery.
if next(p for p in CONFIG['ports'] if p['id']=='rear_left')['state']=='open':
 for o in collections['Architecture'].objects:
  if o.name.startswith('Back_'):o.location.y-=.22
 leaf=bpy.data.objects['Rear_left_leaf']
 parts=[o for o in bpy.data.objects if o.name.startswith(('Rear_left_leaf','Rear_left_raised_panel','Rear_left_knob'))]
 for o in list(parts):
  if o==leaf:continue
  back=o.copy();back.data=o.data.copy();collections['Doors'].objects.link(back)
  back.name=o.name+'_back';back.location.y=2*leaf.location.y-o.location.y;parts.append(back)
 bpy.context.view_layer.update()
 hinge=Vector((-3.72-1.30/2,leaf.location.y,0));angle=-math.pi/2
 swing=Matrix.Translation(hinge)@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-hinge)
 for o in parts:o.matrix_world=swing@o.matrix_world
 CONFIG['geometry']['doors'].append({'id':'kitchen_door','label':'Kitchen door','port':'rear_left','initialOpen':False,'leaves':[movable(parts,hinge,angle,'Door_kitchen')]})
# Cellar entrance, matching the kitchen's existing shared hinge setup.
leaf=bpy.data.objects['Rear_right_leaf']
parts=[o for o in bpy.data.objects if o.name.startswith(('Rear_right_leaf','Rear_right_raised_panel','Rear_right_knob'))]
for o in list(parts):
 if o==leaf:continue
 back=o.copy();back.data=o.data.copy();collections['Doors'].objects.link(back);back.name=o.name+'_back';back.location.y=2*leaf.location.y-o.location.y;parts.append(back)
bpy.context.view_layer.update()
hinge=Vector((3.12-1.3/2,leaf.location.y,0));angle=-math.pi/2
swing=Matrix.Translation(hinge)@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-hinge)
for o in parts:o.matrix_world=swing@o.matrix_world
CONFIG['geometry']['doors'].append({'id':'cellar_door','label':'Cellar door','port':'rear_right','initialOpen':False,'leaves':[movable(parts,hinge,angle,'Door_cellar')]})
CONFIG['geometry']['doorObstacles']=[]

geo.active='Cameras'
camera('05_Landing',(.18,6.75,Z+1.62),(.20,BACK,Z+1.55),lens=20)
camera('06_Balcony',(-4.2,7.65,Z+1.62),(-.1,2.4,1.7),lens=22)
camera('07_Combined',(-.2,-12,7.0),(0,5.6,3.0),lens=35)
scene['room_id']='010+011';scene['version']='connected_v5';scene['limitations']='Exterior, living room and kitchen connected through interactive doors. Other destinations deferred.'
scene.camera=bpy.data.objects['05_Landing'];scene.render.resolution_x=1280;scene.render.resolution_y=800
# Named connection markers are reviewable in Blender and excluded from the GLB.
ports=bpy.data.collections.new('Connection_ports');scene.collection.children.link(ports)
for port in CONFIG['ports']:
 marker=bpy.data.objects.new('PORT_'+port['id'],None);ports.objects.link(marker)
 marker.location=port['position'];marker.empty_display_type='ARROWS';marker.empty_display_size=.4
 marker['outward']=port['outward'];marker['width']=port['width'];marker['state']=port['state']
# Keep the landing's two standard leaves in the library, owned by this hall.
bpy.context.view_layer.update();upper_leaves=[]
for prefix,pid in [('Landing_left_door','landing_left'),('Landing_right_door','landing_right')]:
 leaf=bpy.data.objects[prefix+'_leaf'];pose=leaf.matrix_world@Matrix.Diagonal(Vector((-1.015,1,2.62,1)))
 hinge=leaf.matrix_world@Vector((-.525,0,-1.36));upper_leaves.append((pid,pose,hinge))
 for o in list(bpy.data.objects):
  if o.name.startswith(tuple(prefix+s for s in ['_leaf','_raised_panel','_knob'])):bpy.data.objects.remove(o,do_unlink=True)
from blender_shared.door_assets import register
register(CONFIG,[('Rear_left', 1.3, 2.83), ('Rear_right', 1.3, 2.83), ('Front_double', 1.85, 3.18), ('Right_side', 1.05, 2.75), ('Landing_left_door', 1.05, 2.72), ('Landing_right_door', 1.05, 2.72)])
from blender_shared.door_assets import register_static
register_static(CONFIG,[('Security_frame',Matrix.Translation((.20,BACK,Z)),collections['Landing']),('Entrance_transom',Matrix.Translation((-6.4+(.22 if next(p for p in CONFIG['ports'] if p['id']=='entrance')['state']=='open' else 0),2.35,3.18))@Matrix.Rotation(math.pi/2,4,'Z'),collections['Doors'])])
from blender_shared.door_assets import register_hinged
for pid,pose,hinge in upper_leaves:register_hinged(CONFIG,'Standard_leaf',pose,hinge,-math.pi/2,collections['Doors'],port=pid,node='Door_'+pid,label=pid.replace('_',' ').capitalize(),instance_id=pid+'_leaf')
register_hinged(CONFIG,'Security_leaf',Matrix.Translation((.2,BACK,Z)),(-.75,BACK-.2,Z),-math.pi/2,collections['Landing'],port='landing_center',node='Door_security',label='Security corridor door')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/CONFIG['source']))
# Write navigation dimensions for review; the browser uses the same values.
(manifest_path(CONFIG).parent/'layout.json').write_text(json.dumps({'rooms':['010','011'],'landing_height':Z,'gallery_front':EDGE,'gallery_back':BACK,'stair_end':TOP,'opening_left':-1.15,'opening_right':1.55,'stair_end_left':[left.x,left.y],'stair_end_right':[right.x,right.y],'gallery_front_boundary':boundary},indent=2)+'\n')
print('CONNECTED_HALL_SOURCE_COMPLETE',flush=True)

save_generated(CONFIG)
