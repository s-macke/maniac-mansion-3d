"""Current exterior/kitchen boundary preview."""
import bpy,json
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'generated/previews/assembly'
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config
OUT.mkdir(parents=True,exist_ok=True)
layout=json.loads((ROOT/'house/layout.json').read_text())
for version in ['after']:
 bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene
 for room in layout['rooms']:
  if room['id'] not in ['front_exterior','kitchen']:continue
  cfg=load_config(ROOT/room['definition'],generated=True);file=ROOT/cfg['baked']
  with bpy.data.libraries.load(str(file),link=False) as (a,b):b.collections=['Baked_cel_room']
  col=b.collections[0];scene.collection.children.link(col);bpy.context.view_layer.update()
  matrix=Matrix.Translation(Vector(room['position']))@Matrix.Rotation(room['yaw'],4,'Z')
  for o in col.objects:
   if not o.parent:o.matrix_world=matrix@o.matrix_world
   o.hide_render=False
 scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=False
 scene.world=bpy.data.worlds.new('Night');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
 scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.resolution_x=1000;scene.render.resolution_y=650;scene.render.resolution_percentage=100
 cam=bpy.data.objects.new('Facade_clearance',bpy.data.cameras.new('Facade_clearance'));scene.collection.objects.link(cam);cam.location=(-10.4,8.15,1.62);cam.rotation_euler=(Vector((-6.4,8.15,1.85))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.lens=24;scene.camera=cam
 scene.render.filepath=str(OUT/f'kitchen_facade_{version}_v3.png');bpy.ops.render.render(write_still=True)
print('CLEARANCE_PREVIEWS_COMPLETE',flush=True)
