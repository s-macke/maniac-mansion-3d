"""Build the reusable EGA door kit: unit-width/unit-height leaf and frame."""
import bpy,sys,json
from pathlib import Path
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'scripts'))
from blender_shared.geometry import Geometry,linear
from finalize_baked_glb import finalize
for path in ['generated/models/doors','generated/blender/shared/doors','generated/previews/shared']:(ROOT/path).mkdir(parents=True,exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True);bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;col=bpy.data.collections.new('Door_kit');scene.collection.children.link(col)
mats={}
for name,rgb in {'black':(0,0,0),'brown':(168,84,0),'yellow':(252,252,84),'red':(168,0,0),'gray':(168,168,168),'blue':(0,0,168),'white':(252,252,252),'darkgray':(84,84,84)}.items():
 m=bpy.data.materials.new(name);m.diffuse_color=(*[linear(v) for v in rgb],1);mats[name]=m
geo=Geometry({'Architecture':col},mats);geo.door('Template',0,1.3,2.83,(0,0))
leaf=[o for o in col.objects if o.name.startswith(('Template_leaf','Template_raised_panel','Template_knob'))]
for o in list(leaf):
 if o.name.startswith('Template_leaf'):continue
 back=o.copy();back.data=o.data.copy();col.objects.link(back);back.location.y=-.36-o.location.y;leaf.append(back)
bpy.context.view_layer.update()
frame=[o for o in col.objects if o not in leaf]
mat=bpy.data.materials.new('Shared_EGA_vertex_color');mat.use_nodes=True
n=mat.node_tree.nodes;n.clear();attr=n.new('ShaderNodeVertexColor');attr.layer_name='Col';e=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(attr.outputs['Color'],e.inputs['Color']);mat.node_tree.links.new(e.outputs[0],out.inputs[0])
sys.path.insert(0,str(Path(__file__).resolve().parent))
from designs import pool_door,security_door,entrance_transom
parts=[('Standard_leaf',leaf),('Standard_frame',frame)]
before=set(col.objects);pool_door(geo);bpy.context.view_layer.update();pool_parts=list(set(col.objects)-before)
parts.extend([('Pool_leaf',[o for o in pool_parts if 'jamb' not in o.name]),('Pool_frame',[o for o in pool_parts if 'jamb' in o.name])])
before=set(col.objects);security_door(geo,ROOT);bpy.context.view_layer.update();security_parts=list(set(col.objects)-before)
parts.extend([('Security_leaf',[o for o in security_parts if not o.name.startswith('Security_door_frame')]),('Security_frame',[o for o in security_parts if o.name.startswith('Security_door_frame')])])
for name,build in [('Entrance_transom',lambda:entrance_transom(geo))]:
 before=set(col.objects);build();bpy.context.view_layer.update();parts.append((name,list(set(col.objects)-before)))
for name,objects in parts:
 vs=[];fs=[];cs=[]
 for o in objects:
  for poly in o.data.polygons:
   normal=(o.matrix_world.to_3x3()@poly.normal).normalized()
   # Neutral soft edge shading, identical on both faces and stable while moving.
   factor=.82 if abs(normal.y)>.9 else .68 if abs(normal.x)>.9 else .92 if normal.z>0 else .62
   color=tuple(v*factor for v in o.data.materials[poly.material_index].diffuse_color[:3])+(1,)
   start=len(vs)
   for i in poly.vertices:
    p=o.matrix_world@o.data.vertices[i].co
    if name=='Standard_leaf':p=Vector((p.x/1.265,p.y+.18,(p.z-1.415)/2.73))
    elif name=='Standard_frame':p=Vector((p.x/1.3,p.y,p.z/2.83))
    vs.append(p);cs.append(color)
   fs.append(tuple(range(start,len(vs))))
 me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.materials.append(mat);me.update()
 colors=me.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='POINT')
 for item,c in zip(colors.data,cs):item.color=c
 ob=bpy.data.objects.new(name,me);col.objects.link(ob)
for _,objects in parts:
 for o in objects:bpy.data.objects.remove(o,do_unlink=True)
bpy.ops.object.select_all(action='DESELECT')
for o in col.objects:o.select_set(True)
bpy.ops.export_scene.gltf(filepath=str(ROOT/'generated/models/doors/standard_doors_v1.glb'),use_selection=True,export_format='GLB',export_cameras=False,export_lights=False)
finalize(ROOT/'generated/models/doors/standard_doors_v1.glb')
# Arrange the editable scene for inspection after exporting local-space meshes.
# Room builders append mesh data only, so these display transforms do not affect placement.
bpy.data.objects['Standard_leaf'].location=(-4.4625,-.18,1.59);bpy.data.objects['Standard_leaf'].scale=(-.89,1,3.08)
other=bpy.data.objects['Standard_leaf'].copy();col.objects.link(other);other.name='Preview_second_leaf';other.location.x=-3.5375;other.scale.x=.89
bpy.data.objects['Standard_frame'].location.x=-4;bpy.data.objects['Standard_frame'].scale=(1.85,1,3.18)
bpy.data.objects['Entrance_transom'].location=(-4,0,3.18)
bpy.data.objects['Security_leaf'].location.x=4;bpy.data.objects['Security_frame'].location.x=4
scene.world=bpy.data.worlds.new('Door_library_preview');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.05,.05,.05,1)
cam=bpy.data.objects.new('Library_preview',bpy.data.cameras.new('Library_preview'));scene.collection.objects.link(cam)
cam.location=(0,-14,4);cam.rotation_euler=(Vector((0,0,1.5))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=11;scene.camera=cam
scene.render.engine='CYCLES';scene.cycles.samples=4;scene.view_settings.view_transform='Standard';scene.view_settings.look='None'
scene.render.resolution_x=1200;scene.render.resolution_y=500;scene.render.resolution_percentage=100
scene.render.filepath=str(ROOT/'generated/previews/shared/doors.png')
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA';area.spaces.active.shading.type='MATERIAL'
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'generated/blender/shared/doors/standard_doors_v1.blend'))
bpy.ops.render.render(write_still=True)
print('DOOR_KIT_COMPLETE',flush=True)
