"""Assembled pantry/pool connection views without modifying independent room assets."""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'generated/previews/assembly';OUT.mkdir(parents=True,exist_ok=True)
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene;moving=[]
for room in json.loads((ROOT/'house/layout.json').read_text())['rooms']:
 if room['id'] not in ['pantry','pool']:continue
 cfg=load_config(ROOT/room['definition'],generated=True)
 with bpy.data.libraries.load(str(ROOT/cfg['baked']),link=False) as (a,b):b.collections=['Baked_cel_room']
 col=b.collections[0];scene.collection.children.link(col);bpy.context.view_layer.update()
 transform=Matrix.Translation(Vector(room['position']))@Matrix.Rotation(room['yaw'],4,'Z')
 for door in cfg.get('geometry',{}).get('doors',[]):
  for leaf in door['leaves']:
   o=col.objects[leaf['node']];rest=o.matrix_world.copy()
   if door['id']=='pool_door':moving.append((o,transform,rest,leaf['openAngle']))
   else:o.matrix_world=rest@Matrix.Rotation(-leaf['openAngle'],4,'Z')
 bpy.context.view_layer.update()
 for o in col.objects:
  if not o.parent:o.matrix_world=transform@o.matrix_world
  o.hide_render=False
scene.render.engine='CYCLES';scene.cycles.samples=12;scene.cycles.use_denoising=False
scene.world=bpy.data.worlds.new('Dark');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100
camera=bpy.data.objects.new('Pool_connection',bpy.data.cameras.new('Pool_connection'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.lens=22
for state,amount in [('open',1),('closed',0)]:
 for o,placement,rest,angle in moving:o.matrix_world=placement@rest@Matrix.Rotation((amount-1)*angle,4,'Z')
 for name,loc,target in [('pantry_to_pool',(-4.5,40.9,1.62),(-10,40.9,1.62)),('pool_to_pantry',(-8.4,40.9,1.62),(-4,40.9,1.62))]:
  camera.location=loc;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/f'{name}_{state}_shared_v1.png');bpy.ops.render.render(write_still=True)
print('POOL_CONNECTION_PREVIEWS_COMPLETE',flush=True)
