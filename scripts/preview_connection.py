"""Render the current doorway assembly without changing independent room files."""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'generated/previews/assembly';OUT.mkdir(parents=True,exist_ok=True)
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config
OUT.mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);scene=bpy.context.scene
for room in json.loads((ROOT/'house/layout.json').read_text())['rooms']:
 if room.get('previewOnly'):continue
 cfg=load_config(ROOT/room['definition'],generated=True)
 with bpy.data.libraries.load(str(ROOT/cfg['baked']),link=False) as (a,b):b.collections=['Baked_cel_room']
 collection=b.collections[0];scene.collection.children.link(collection)
 bpy.context.view_layer.update()
 transform=Matrix.Translation(Vector(room['position']))@Matrix.Rotation(room['yaw'],4,'Z')
 for o in collection.objects:
  if not o.parent:o.matrix_world=transform@o.matrix_world
  o.hide_render=False
scene.render.engine='CYCLES';scene.cycles.samples=16;scene.cycles.use_denoising=False
scene.world=bpy.data.worlds.new('Dark');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.resolution_x=1280;scene.render.resolution_y=800;scene.render.resolution_percentage=100;scene.render.image_settings.file_format='PNG'
for name,loc,target in [('hall_to_living',(4.6,3.15,1.62),(10,3.15,1.62)),('living_to_hall',(8.4,3.15,1.62),(1,3.15,1.62)),('exterior_approach',(-21.4,2.35,.42),(-6.4,2.35,5.5)),('exterior_front_door',(-9.8,2.35,1.1),(-3.5,2.35,1.62)),('hall_to_exterior',(-4.5,2.35,1.62),(-14,2.35,.2))]:
 data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-Vector(loc)).to_track_quat('-Z','Y').to_euler();data.lens=24;scene.camera=o
 scene.render.filepath=str(OUT/f'{name}.png');bpy.ops.render.render(write_still=True)
print('CONNECTION_PREVIEWS_COMPLETE',flush=True)
