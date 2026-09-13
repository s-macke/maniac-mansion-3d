"""Assembled pool/garage layout views; independent room outputs remain untouched."""
import bpy,json
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'generated/previews/assembly'
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene
for room in json.loads((ROOT/'house/layout.json').read_text())['rooms']:
 if room['id'] not in ['pool','garage']:continue
 config=load_config(ROOT/room['definition'],generated=True)
 with bpy.data.libraries.load(str(ROOT/config['baked']),link=False) as (a,b):b.collections=['Baked_cel_room']
 col=b.collections[0];scene.collection.children.link(col);bpy.context.view_layer.update()
 transform=Matrix.Translation(Vector(room['position']))@Matrix.Rotation(room['yaw'],4,'Z')
 for o in col.objects:
  if not o.parent:o.matrix_world=transform@o.matrix_world
  o.hide_render=False
scene.world=bpy.data.worlds.new('Night');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
cam=bpy.data.objects.new('Connection',bpy.data.cameras.new('Connection'));scene.collection.objects.link(cam);cam.data.lens=22;scene.camera=cam
scene.render.resolution_x=1100;scene.render.resolution_y=650;scene.render.resolution_percentage=100
for name,loc,target in [('pool_to_garage',(-24.17,38.9,1.62),(-34,38.9,1.62)),('garage_to_pool',(-32,38.9,1.62),(-21,38.9,1.5))]:
 cam.location=loc;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();scene.render.filepath=str(OUT/(name+'_v1.png'));bpy.ops.render.render(write_still=True)
print('GARAGE_CONNECTION_PREVIEWS_COMPLETE')
