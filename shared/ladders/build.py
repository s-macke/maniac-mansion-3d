"""One reusable 28 cm EGA ladder section, instanced by every room."""
import bpy,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from blender_shared.shell import setup
from finalize_baked_glb import finalize
scene,cols,geo=setup({'gray':(168,168,168),'white':(252,252,252),'darkgray':(84,84,84)})
for x in [-.36,.36]:geo.box('Rail',(x,0,.14),(.065,.085,.28),'gray')
geo.box('Rung',(0,-.035,.14),(.72,.10,.055),'gray')
objects=list(cols['Architecture'].objects);bpy.context.view_layer.update();vs=[];fs=[];cs=[]
for o in objects:
 for poly in o.data.polygons:
  n=(o.matrix_world.to_3x3()@poly.normal).normalized();shade=.95 if n.z>.5 else .70 if abs(n.x)>.5 else .84
  color=tuple(v*shade for v in o.data.materials[poly.material_index].diffuse_color[:3])+(1,);start=len(vs)
  for i in poly.vertices:vs.append(o.matrix_world@o.data.vertices[i].co);cs.append(color)
  fs.append(tuple(range(start,len(vs))))
mat=bpy.data.materials.new('Ladder_baked_EGA');mat.use_nodes=True;n=mat.node_tree.nodes;n.clear();a=n.new('ShaderNodeVertexColor');a.layer_name='Col';e=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(a.outputs['Color'],e.inputs['Color']);mat.node_tree.links.new(e.outputs[0],out.inputs[0])
mesh=bpy.data.meshes.new('Ladder_section');mesh.from_pydata(vs,[],fs);mesh.materials.append(mat);mesh.update();col=mesh.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='POINT')
for item,c in zip(col.data,cs):item.color=c
for o in objects:bpy.data.objects.remove(o,do_unlink=True)
o=bpy.data.objects.new('Ladder_section',mesh);cols['Architecture'].objects.link(o)
for p in ['generated/models/ladders','generated/blender/shared/ladders']:(ROOT/p).mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='DESELECT');o.select_set(True)
p=ROOT/'generated/models/ladders/ladder_v1.glb';bpy.ops.export_scene.gltf(filepath=str(p),use_selection=True,export_format='GLB',export_cameras=False,export_lights=False);finalize(p)
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'generated/blender/shared/ladders/ladder_v1.blend'))
print('LADDER_KIT_COMPLETE',flush=True)
