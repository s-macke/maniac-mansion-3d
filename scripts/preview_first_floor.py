"""Assembled first-floor and library views; room outputs remain independent."""
import bpy,json
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'generated/previews/assembly';OUT.mkdir(parents=True,exist_ok=True)
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;moving=[]
for room in json.loads((ROOT/'house/layout.json').read_text())['rooms']:
 if room['id'] not in ['hall','living_room','front_exterior','library','plant_room','music_room','security_hall','medical_room','arcade']:continue
 cfg=load_config(ROOT/room['definition'],generated=True)
 with bpy.data.libraries.load(str(ROOT/cfg['baked']),link=False) as (a,b):b.collections=['Baked_cel_room']
 col=b.collections[0];scene.collection.children.link(col);bpy.context.view_layer.update()
 transform=Matrix.Translation(Vector(room['position']))@Matrix.Rotation(room['yaw'],4,'Z')
 for door in cfg.get('geometry',{}).get('doors',[]):
  for leaf in door['leaves']:
   o=col.objects[leaf['node']];rest=o.matrix_world.copy();moving.append((o,transform@rest,leaf['openAngle']))
 for o in col.objects:
  if not o.parent:o.matrix_world=transform@o.matrix_world
  o.hide_render=False
scene.world=bpy.data.worlds.new('Night');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=False;scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
cam=bpy.data.objects.new('Connection',bpy.data.cameras.new('Connection'));scene.collection.objects.link(cam);cam.data.lens=22;scene.camera=cam
scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100
views=[('landing',(-3.8,7,4.98),(.2,9.75,4.95)),('plant_door',(-4.8,8.5,4.98),(-9.6,8.5,4.98)),('music_door',(4.8,8.5,4.98),(10.4,8.5,4.98)),('security_door',(.2,8.2,4.98),(.2,13,4.98)),('security_rooms',(-4.5,11,4.98),(2,15.3,4.98)),('library_door',(17.6,3.15,1.62),(24,3.15,1.62))]
for state,amount in [('closed',0),('open',1)]:
 for o,rest,angle in moving:o.matrix_world=rest@Matrix.Rotation((amount-1)*angle,4,'Z')
 for name,loc,target in views:
  cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'_'+state+'_v1.png'));bpy.ops.render.render(write_still=True)
print('FIRST_FLOOR_PREVIEWS_COMPLETE',flush=True)
