"""Independent outdoor pool deck based on room 006; no indoor shell template."""
import bpy,json,math,sys,random
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(OUT))
from room_config import load_config,save_generated,manifest_path
from blender_shared.geometry import Geometry,linear
config=load_config(OUT/'room.json',prepare=True);g=config['geometry'];W=g['width'];D=g['depth'];p=g['pool']
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.engine='CYCLES';scene.cycles.samples=16
scene.world=bpy.data.worlds.new('Night');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
colors={'black':(0,0,0),'gray':(168,168,168),'darkgray':(84,84,84),'blue':(0,0,168),'lightblue':(84,84,252),'cyan':(0,168,168),'aqua':(84,252,252),'yellow':(252,252,84),'lightgreen':(84,252,84),'pink':(252,84,252),'purple':(168,0,168),'white':(252,252,252)}
mats={}
for name,rgb in colors.items():
 m=bpy.data.materials.new('EGA_'+name);m.diffuse_color=(*[linear(v) for v in rgb],1);m.use_nodes=True;n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=m.diffuse_color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);mats[name]=m
collections={}
for name in ['Architecture','Pool','Fence','Details','Cameras','Reference','Connection_ports']:
 c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
geo=Geometry(collections,mats);box=geo.box
# Four deck strips leave a real pool opening.
x0,x1,y0,y1=[p[k] for k in ['x0','x1','y0','y1']]
for a,b,c,d in [(0,x0,0,D),(x1,W,0,D),(x0,x1,0,y0),(x0,x1,y1,D)]:box('Deck',((a+b)/2,(c+d)/2,-.10),(b-a,d-c,.20),'gray')
# Coarse irregular stone polygons follow the source's gray outlines and dark centres.
rng=random.Random(6);verts=[];faces=[]
for ix in range(36):
 for iy in range(20):
  a=ix*W/36;b=(ix+1)*W/36;c=iy*D/20;d=(iy+1)*D/20
  if b>x0-.28 and a<x1+.28 and d>y0-.28 and c<y1+.28:continue
  inset=.035;pts=[(a+inset,c+.08),(a+.16,c+inset),(b-.09,c+.035),(b-inset,c+.2),(b-.09,d-.035),(a+.08,d-.02)]
  start=len(verts);verts.extend((x+rng.uniform(-.025,.025),y+rng.uniform(-.025,.025),.006) for x,y in pts);faces.append(tuple(range(start,start+6)))
geo.mesh('Stone_deck_pattern',verts,faces,'darkgray')
# Only the wall segment around the pantry doorway; remaining house mass stays room-owned.
port=config['ports'][0];cy=port['position'][1];dw=port['width'];dh=port['height']
for a,b in [(0,cy-dw/2),(cy+dw/2,6.4)]:box('House_wall',(.09,(a+b)/2,1.7),(.18,b-a,3.4),'gray')
box('House_header',(.09,cy,(dh+3.4)/2),(.18,dw,3.4-dh),'gray')
# Dark outer door reveal lets the shared pantry leaf be seen from outdoors.
for side in [-1,1]:box('Pool_entry_reveal',(.05,cy+side*(dw/2+.045),dh/2),(.10,.09,dh),'darkgray')
geo.active='Pool'
box('Basin_floor',((x0+x1)/2,(y0+y1)/2,p['bottom']-.1),(x1-x0,y1-y0,.2),'blue')
for x in [x0,x1]:box('Basin_side',(x,(y0+y1)/2,p['bottom']/2),(.18,y1-y0,-p['bottom']),'lightblue')
for y in [y0,y1]:box('Basin_end',((x0+x1)/2,y,p['bottom']/2),(x1-x0,.18,-p['bottom']),'blue')
for x in [x0-.14,x1+.14]:box('Turquoise_coping',(x,(y0+y1)/2,.035),(.28,y1-y0+.56,.07),'aqua')
for y in [y0-.14,y1+.14]:box('Turquoise_coping',((x0+x1)/2,y,.035),(x1-x0,.28,.07),'aqua')
water=box('Water_surface',((x0+x1)/2,(y0+y1)/2,p['water']),(x1-x0-.18,y1-y0-.18,.025),'blue');water['bake_unlit']=True
# Sparse geometric EGA glints, not reflective shaders.
for i in range(26):
 x=rng.uniform(x0+.4,x1-.4);y=rng.uniform(y0+.3,y1-.3)
 o=box('Water_glint',(x,y,p['water']+.02),(rng.uniform(.07,.24),.018,.01),'cyan');o['bake_unlit']=True
# Metal ladder and handrails reach the basin floor in the drained state.
geo.active='Details'
for x in [10.65,11.35]:
 geo.beam('Ladder_rail',(x,y1-.16,p['bottom']+.12),(x,y1-.16,.65),.055,'gray')
 geo.beam('Ladder_grip',(x,y1-.16,.65),(x,y1+.6,.65),.055,'white')
 geo.beam('Ladder_foot',(x,y1+.6,.65),(x,y1+.6,0),.055,'gray')
for z in [-2.55,-2.23,-1.83,-1.51,-1.19,-.87,-.55,-.23,.09,.41]:geo.beam('Ladder_rung',(10.65,y1-.16,z),(11.35,y1-.16,z),.048,'white')
from interior import furnish
furnish(geo,p)
# Pink floating chair silhouette visible in the original pool background.
box('Chair_seat',(12,5.5,p['water']+.16),(.72,.72,.13),'pink')
box('Chair_back',(12,5.82,p['water']+.54),(.65,.12,.78),'pink')
box('Chair_side',(11.65,5.5,p['water']+.25),(.10,.70,.20),'purple')
for x in [11.72,12.28]:geo.beam('Chair_foot',(x,5.15,p['water']+.02),(x,5.85,p['water']+.02),.07,'black')
# Keep wet-only surfaces in one independently switchable baked mesh.
for o in bpy.data.objects:
 if o.type=='MESH' and o.name.startswith(('Water_','Chair_')):o['bake_group']='Pool_water';o['bake_no_shadow']=True
geo.active='Fence'
def fence(a,b):
 length=math.dist(a,b);n=math.ceil(length/.36)
 for i in range(n+1):
  t=i/n;x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t;mat='cyan' if x<9 else 'yellow'
  along_x=abs(b[0]-a[0])>abs(b[1]-a[1])
  box('Fence_picket',(x,y,1.04),(.27,.12,2.08) if along_x else (.12,.27,2.08),mat)
  tip=[(x-.135,y-.06,2.08),(x+.135,y-.06,2.08),(x,y-.06,2.25)] if along_x else [(x-.06,y-.135,2.08),(x-.06,y+.135,2.08),(x-.06,y,2.25)]
  geo.mesh('Fence_point',tip,[(0,1,2)],mat)
 for z in [.3,1.25,1.82]:
  # Split rails at the source's teal/yellow color change.
  for i in range(n):
   t=i/n;u=(i+1)/n;x=a[0]+(b[0]-a[0])*t;y=a[1]+(b[1]-a[1])*t
   geo.beam('Fence_rail',(x,y-.10,z),(a[0]+(b[0]-a[0])*u,a[1]+(b[1]-a[1])*u-.10,z),.12,'cyan' if x<9 else 'yellow')
fence((.22,D-.22),(W-.22,D-.22))
exit_port=next(p for p in config['ports'] if p['id']=='garage_path');centre=exit_port['position'][1];half=exit_port['width']/2
fence((W-.22,.22),(W-.22,centre-half-.14))
fence((W-.22,centre+half+.14),(W-.22,D-.22))
# Inferred near boundary completes the safe deck perimeter.
box('Near_deck_curb',(W/2,.18,.12),(W,.36,.24),'darkgray')
geo.active='Details'
for a,b,w in [((19.4,10.3,0),(19.1,10.1,4.7),.22),((19.1,10.1,3.4),(17.1,10.1,4.8),.12),((19.1,10.1,4.0),(19.8,9.1,4.9),.10),((17.1,10.1,4.8),(15.5,10.4,4.6),.06)]:geo.beam('Bare_tree',a,b,w,'darkgray')
for i in range(32):
 x=rng.uniform(.5,19.5);z=rng.uniform(2.8,5)
 o=box('Star',(x,D-.02,z),(.04,.01,.12),'aqua');o['bake_unlit']=True
 o=box('Star',(x,D-.03,z),(.12,.01,.025),'aqua');o['bake_unlit']=True
image=bpy.data.images.load(str(ROOT/'source/room 006.png'));image.pack();ref=bpy.data.objects.new('Reference_room_006',None);collections['Reference'].objects.link(ref);ref.empty_display_type='IMAGE';ref.data=image;ref.hide_render=True;ref.hide_viewport=True
for port in config['ports']:
 o=bpy.data.objects.new('PORT_'+port['id'],None);collections['Connection_ports'].objects.link(o);o.location=port['position'];o.empty_display_type='ARROWS';o['state']=port['state'];o['outward']=port['outward'];o['width']=port['width']
geo.active='Cameras'
geo.camera('01_Reference',(10,-9,8),(10,5,0),lens=30)
geo.camera('02_Inside',(2,3.2,1.62),(12,6,1),lens=20)
geo.camera('03_Reverse',(18.4,7,1.62),(0,3.2,1.3),lens=22)
scene.camera=bpy.data.objects['02_Inside'];scene['room_id']='006';scene['scope']='One pool unit: filled deck and explorable drained basin, with a same-room ladder.';scene.render.resolution_x=1100;scene.render.resolution_y=650
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('POOL_SOURCE_COMPLETE',flush=True)

save_generated(config)
