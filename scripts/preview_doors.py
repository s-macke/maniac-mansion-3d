"""Render open/closed interactive leaves in the assembled house without modifying rooms."""
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
 if room.get('previewOnly'):continue
 cfg=load_config(ROOT/room['definition'],generated=True)
 with bpy.data.libraries.load(str(ROOT/cfg['baked']),link=False) as (a,b):b.collections=['Baked_cel_room']
 col=b.collections[0];scene.collection.children.link(col)
 bpy.context.view_layer.update()
 transform=Matrix.Translation(Vector(room['position']))@Matrix.Rotation(room['yaw'],4,'Z')
 for door in cfg.get('geometry',{}).get('doors',[]):
  for leaf in door['leaves']:
   # Appending rooms can rename duplicate objects (e.g. Door_higher_floor.001).
   # Shared leaf metadata retains the authored node ID across Blender renames.
   hinges={o.parent for o in col.all_objects if o.get('door_node')==leaf['node'] and o.parent}
   if len(hinges)!=1:
    raise ValueError(f"{cfg['id']}: expected one hinge for {leaf['node']}, found {len(hinges)}")
   hinge=hinges.pop()
   moving.append((hinge,transform,hinge.matrix_world.copy(),leaf['openAngle']))
 for o in col.objects:
  if not o.parent:o.matrix_world=transform@o.matrix_world
  o.hide_render=False
scene.render.engine='CYCLES';scene.cycles.samples=8;scene.cycles.use_denoising=False
scene.world=bpy.data.worlds.new('Dark');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0,0,0,1)
scene.view_settings.view_transform='Standard';scene.view_settings.look='None';scene.render.resolution_x=800;scene.render.resolution_y=600;scene.render.resolution_percentage=100
camera=bpy.data.objects.new('Door_preview',bpy.data.cameras.new('Door_preview'));scene.collection.objects.link(camera);scene.camera=camera;camera.data.lens=22
for state,amount in [('open',1),('closed',0)]:
 for o,placement,rest,angle in moving:o.matrix_world=placement@rest@Matrix.Rotation((amount-1)*angle,4,'Z')
 for name,loc,target in [('living',(8.2,3.15,1.62),(5.9,3.15,1.62)),('front',(-8.5,2.35,1.62),(-5.9,2.35,1.62))]:
  camera.location=loc;camera.rotation_euler=(Vector(target)-camera.location).to_track_quat('-Z','Y').to_euler()
  scene.render.filepath=str(OUT/f'door_{name}_{state}_shared_v1.png');bpy.ops.render.render(write_still=True)
print('DOOR_PREVIEWS_COMPLETE',flush=True)
