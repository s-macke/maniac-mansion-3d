"""Small building helpers for rectangular interior shells.
Room scripts keep colors, cameras, door ownership and special features explicit.
Outdoor and furnished rooms do not need to use these helpers.
"""
import bpy,math
from mathutils import Matrix,Vector
from .geometry import Geometry,linear


def setup(colors):
 bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
 scene=bpy.context.scene;scene.unit_settings.system='METRIC';scene.render.engine='CYCLES';scene.cycles.samples=16
 scene.world=bpy.data.worlds.new('Night');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
 scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
 mats={}
 for name,rgb in colors.items():
  m=bpy.data.materials.new('EGA_'+name);m.diffuse_color=(*[linear(v) for v in rgb],1);m.use_nodes=True
  n=m.node_tree.nodes;n.clear();e=n.new('ShaderNodeEmission');e.inputs[0].default_value=m.diffuse_color;o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(e.outputs[0],o.inputs[0]);mats[name]=m
 collections={}
 for name in ['Architecture','Doors','Cameras','Reference','Connection_ports']:
  c=bpy.data.collections.new(name);scene.collection.children.link(c);collections[name]=c
 geo=Geometry(collections,mats)
 return scene,collections,geo


def build_shell(geo,g,name,*,floor,back,wall,trim,closed_right=False):
 W,D,H,T=(g[k] for k in ['halfWidth','depth','height','wallThickness']);box=geo.box
 box(name.capitalize()+'_floor',(0,D/2,-.06),(W*2,D,.12),floor)
 box(name.capitalize()+'_back',(0,D-T/2,H/2),(W*2,T,H),back)
 if closed_right:
  box(name.capitalize()+'_right',(W-T/2,D/2,H/2),(T,D,H),wall)
  box('Right_skirting',(W-T-.018,D/2,.13),(.036,D,.26),trim)
 box('Front_inferred_'+name,(0,T/2,H/2),(W*2,T,H),wall)
 box('Ceiling_'+name,(0,D/2,H+.02),(W*2,D,.04),wall)
 box('Back_skirting',(0,D-T-.018,.13),(W*2,.036,.26),trim)
 box('Front_skirting',(0,T+.018,.13),(W*2,.036,.26),trim)


def side_door(geo,g,port,side,prefix,*,wall,trim,frame_only=False):
 W,D,H,T=(g[k] for k in ['halfWidth','depth','height','wallThickness']);box=geo.box
 y=port['position'][1];width=port['width'];dh=port['height'];x=side*(W-T/2)
 for a,b in [(0,y-width/2),(y+width/2,D)]:
  box('Side_wall',(x,(a+b)/2,H/2),(T,b-a,H),wall)
  box('Side_skirting',(side*(W-T-.018),(a+b)/2,.13),(.036,b-a,.26),trim)
 box('Door_header',(x,y,(dh+H)/2),(T,width,H-dh),wall)
 geo.active='Doors'
 before=set(bpy.data.objects);geo.door(prefix,0,width,dh,(side*W,y),math.pi/2 if side<0 else -math.pi/2)
 if frame_only:
  for o in set(bpy.data.objects)-before:
   if o.name.startswith((prefix+'_leaf',prefix+'_raised_panel',prefix+'_knob')):bpy.data.objects.remove(o,do_unlink=True)
 geo.active='Architecture'


def reference(root,config,collections,background):
 # Packed reference and named ports make the independent Blender package reviewable.
 image=bpy.data.images.load(str(root/f'source/room {background}.png'));image.pack()
 ref=bpy.data.objects.new(f'Reference_room_{background}',None);collections['Reference'].objects.link(ref);ref.empty_display_type='IMAGE';ref.data=image;ref.hide_render=True;ref.hide_viewport=True
 for port in config['ports']:
  o=bpy.data.objects.new('PORT_'+port['id'],None);collections['Connection_ports'].objects.link(o);o.location=port['position'];o.empty_display_type='ARROWS';o['state']=port['state'];o['outward']=port['outward'];o['width']=port['width']


def interactive_side_door(config,collections,port,prefix,node,label):
 """Prepare a right-end door opening into its owning room, using the existing hinge convention."""
 bpy.context.view_layer.update()
 parts=[o for o in collections['Doors'].objects if o.name.startswith(tuple(prefix+s for s in ['_leaf','_raised_panel','_knob']))]
 leaf=bpy.data.objects[prefix+'_leaf']
 for o in list(parts):
  if o==leaf:continue
  back=o.copy();back.data=o.data.copy();collections['Doors'].objects.link(back);back.name=o.name+'_back';back.location.x=2*leaf.location.x-o.location.x;parts.append(back)
 bpy.context.view_layer.update()
 hinge=Vector((leaf.location.x,port['position'][1]-port['width']/2,0));angle=math.pi/2
 swing=Matrix.Translation(hinge)@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-hinge)
 for o in parts:o.matrix_world=swing@o.matrix_world;o['door_node']=node;o['door_hinge']=list(hinge)
 bpy.context.view_layer.update()
 points=[o.matrix_world@v.co for o in parts for v in o.data.vertices]
 config['geometry']['doorObstacles']=[]
 config['geometry']['doors']=[{'id':port['id'],'label':label,'port':port['id'],'initialOpen':False,'leaves':[{'node':node,'hinge':list(hinge),'openAngle':angle,'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}]}]
