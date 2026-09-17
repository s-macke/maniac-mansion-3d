"""Shared static cel-light bake, driven by a room's bake configuration.
Run through scripts/rooms.py bake ROOM. No room geometry or destinations live here.
"""
import bpy, math, json, sys
from pathlib import Path
from mathutils import Vector
from mathutils.bvhtree import BVHTree
ROOT=Path(__file__).resolve().parents[2]
config_path=Path(sys.argv[sys.argv.index('--room-config')+1])
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config,manifest_path
config=load_config(config_path,generated=True);settings=config['bake']
OUT=ROOT/'generated/previews/rooms'/config['id'];OUT.mkdir(parents=True,exist_ok=True)
asset=Path(config['asset']).stem
bpy.ops.wm.open_mainfile(filepath=str(ROOT/config['source']))
bpy.context.preferences.filepaths.save_version=0
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=24
light=Vector(settings['lights'][0]);cell=settings['cell']
names=settings['collections']
objects=[o for name in names for o in bpy.data.collections[name].objects if o.type=='MESH']
# Include all closed-room surfaces in shadow queries. Illumination is a point inside the room.
verts=[];polys=[]
for o in objects:
 if o.get('bake_unlit') or o.get('bake_no_shadow') or o.get('door_node'):continue
 start=len(verts);verts.extend([o.matrix_world@v.co for v in o.data.vertices])
 polys.extend([tuple(start+i for i in p.vertices) for p in o.data.polygons])
bvh=BVHTree.FromPolygons(verts,polys,all_triangles=False)
mat=bpy.data.materials.new('Baked_cel_vertex_colors_UNLIT');mat.use_nodes=True
n=mat.node_tree.nodes;n.clear();attr=n.new('ShaderNodeVertexColor');attr.layer_name='Col'
e=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial')
mat.node_tree.links.new(attr.outputs['Color'],e.inputs['Color']);mat.node_tree.links.new(e.outputs[0],out.inputs[0])
mat.diffuse_color=(1,1,1,1)
# Keep front wall and ceiling separate so reference cutaway and interior views remain available.
groups={}
door_hinges={o['door_node']:Vector(o['door_hinge']) for o in objects if o.get('door_node') and not o.get('shared_asset')}
# A small area source gives a soft penumbra. Lighting varies per vertex rather
# than painting one color over each grid cell; textures and geometry stay sharp.
lights=[Vector(v) for v in settings['lights']]
light_groups=[[l]+[l+Vector((math.cos(i*math.tau/8)*.32,math.sin(i*math.tau/8)*.32,0)) for i in range(8)] for l in lights]
light_samples=light_groups[0]
def smooth(a,b,x):
 t=max(0,min(1,(x-a)/(b-a)));return t*t*(3-2*t)
def shade(p,normal,base):
 factors=[]
 for center, samples in zip(lights,light_groups):
  direction=(center-p).normalized();nd=max(0,normal.dot(direction))
  lit=.56+.20*smooth(.21,.33,nd)+.24*smooth(.62,.74,nd)
  visible=0
  for sample in samples:
   toward=sample-p;distance=toward.length;direction=toward.normalized()
   hit=bvh.ray_cast(p+normal*.008+direction*.002,direction,max(0,distance-.015))[0]
   visible+=hit is None
  factors.append(.43+(lit-.43)*visible/len(samples))
 factor=max(factors)
 return tuple(c*factor for c in base[:3])+(1.,)

def emit(group,points,normal,base,colors=None):
 vs,fs,cs=groups.setdefault(group,([],[],[]));start=len(vs)
 if colors is None:colors=[shade(p,normal,base) for p in points]
 vs.extend(points);fs.append(tuple(range(start,start+len(points))));cs.extend(colors)
for oi,o in enumerate(objects):
 if o.get('shared_asset'):continue
 if o.get('bake_group'):group=o['bake_group']
 elif o.get('door_node'):group=o['door_node']
 elif o.name.startswith('Front_inferred'):group='Cutaway_front'
 elif o.name.startswith('Ceiling_') or o.name.startswith('Stairwell_'):group='Cutaway_ceiling'
 else:group=next((name for name in names if o.name in bpy.data.collections[name].objects),'Room')
 for poly in o.data.polygons:
  pts=[o.matrix_world@o.data.vertices[i].co for i in poly.vertices]
  normal=(o.matrix_world.to_3x3().inverted().transposed()@poly.normal).normalized()
  # Opt-in analytic normals keep curved shells smooth after vertex-color baking.
  def shading_normal(p):
   if 'bake_curved_center' not in o:return normal
   center=o['bake_curved_center'];radii=o['bake_curved_radii'];sign=o['bake_curved_sign']
   return Vector([(p[i]-center[i])/(radii[i]*radii[i])*sign if radii[i] else 0 for i in range(3)]).normalized()
  original=o.data.materials[poly.material_index];base=original.diffuse_color
  if o.get('bake_unlit'):
   emit(group,pts,normal,base,[tuple(base)]*len(pts));continue
  # Dense cells on large flat surfaces give baked shadows enough detail; tiny props stay light.
  if len(pts)==4:
   a,b,c,d=pts;nx=max(1,math.ceil(max((b-a).length,(c-d).length)/cell));ny=max(1,math.ceil(max((d-a).length,(c-b).length)/cell))
   def point(u,v):return a.lerp(b,u).lerp(d.lerp(c,u),v)
   grid=[[shade(point(ix/nx,iy/ny),shading_normal(point(ix/nx,iy/ny)),base) for ix in range(nx+1)] for iy in range(ny+1)]
   def corners(ix,iy):return [grid[iy][ix],grid[iy][ix+1],grid[iy+1][ix+1],grid[iy+1][ix]]
   def uniform(ix,iy,color):return all(max(abs(a-b) for a,b in zip(c,color))<1e-7 for c in corners(ix,iy))
   used=set()
   for iy in range(ny):
    for ix in range(nx):
     if (ix,iy) in used:continue
     color=grid[iy][ix];ex=ix+1;ey=iy+1
     if uniform(ix,iy,color):
      while ex<nx and (ex,iy) not in used and uniform(ex,iy,color):ex+=1
      while ey<ny and all((xx,ey) not in used and uniform(xx,ey,color) for xx in range(ix,ex)):ey+=1
      baked_colors=[color]*4
     else:baked_colors=corners(ix,iy)
     used.update((xx,yy) for yy in range(iy,ey) for xx in range(ix,ex))
     emit(group,[point(ix/nx,iy/ny),point(ex/nx,iy/ny),point(ex/nx,ey/ny),point(ix/nx,ey/ny)],normal,base,baked_colors)
  else:emit(group,pts,normal,base,[shade(p,shading_normal(p),base) for p in pts])
 if oi%300==0:print('Baking direct shadows',oi,'/',len(objects),flush=True)
# Replace render geometry with a handful of meshes for low browser draw-call overhead.
shared=[o for o in bpy.data.objects if o.get('shared_asset')]
for o in objects:
 if not o.get('shared_asset'):bpy.data.objects.remove(o,do_unlink=True)
baked=bpy.data.collections.new('Baked_cel_room');scene.collection.children.link(baked)
for o in shared:
 for c in list(o.users_collection):c.objects.unlink(o)
 baked.objects.link(o)
for name,(vs,fs,cs) in groups.items():
 me=bpy.data.meshes.new(name);me.from_pydata([v-door_hinges[name] for v in vs] if name in door_hinges else vs,[],fs);me.materials.append(mat);me.update()
 col=me.color_attributes.new(name='Col',type='FLOAT_COLOR',domain='POINT')
 for item,value in zip(col.data,cs):item.color=value
 ob=bpy.data.objects.new(name,me);baked.objects.link(ob)
 if name in door_hinges:ob.location=door_hinges[name]
 ob['lighting']='Baked direct light, three lit bands plus shadow; no global illumination'
# All final surfaces use vertex-color emission: Cycles only rasterizes this fixed result.
front=[o for o in baked.objects if o.name=='Cutaway_front']
ceilings=[o for o in baked.objects if o.name=='Cutaway_ceiling']
scene['version']=asset;scene['style']='EGA base colors, baked cel bands and direct cast shadows'
scene['lighting']='Static vertex colors; no real-time lights, GI, or custom browser shader required'
views=settings['views'];suffix=settings.get('previewSuffix','v1')
for cam,name,w,h in views:
 scene.camera=bpy.data.objects[cam]
 for o in front+ceilings:o.hide_render=cam in ('01_Reference','07_Combined')
 scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.filepath=str(OUT/f'{name}_{suffix}.png')
 bpy.ops.render.render(write_still=True)
for o in front+ceilings:o.hide_render=False
bpy.ops.object.select_all(action='DESELECT')
for o in baked.objects:o.select_set(o.type=='MESH' and not o.get('shared_asset'))
bpy.ops.export_scene.gltf(filepath=str(ROOT/config['asset']),use_selection=True,export_format='GLB',export_cameras=False,export_lights=False)
import sys
sys.path.insert(0,str(ROOT/'scripts'))
from finalize_baked_glb import finalize
finalize(ROOT/config['asset'])
for o in front+ceilings:o.hide_render=settings.get('startupCutaway',False)
cam,name,w,h=views[0];scene.camera=bpy.data.objects[cam]
scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.filepath=str(OUT/f'{name}_{suffix}.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['baked']))
report={'method':'Interpolated vertex lighting with soft direct shadows and softened cel bands; no GI','light_position':list(light),'light_positions':[list(v) for v in lights],'cell_size_m':cell,'shadow_samples':len(light_samples),'render_meshes':sum(o.type=='MESH' and not o.get('shared_asset') for o in baked.objects),'shared_instances':sum(o.type=='MESH' for o in shared),'vertices':sum(len(o.data.vertices) for o in baked.objects if o.type=='MESH' and not o.get('shared_asset')),'faces':sum(len(o.data.polygons) for o in baked.objects if o.type=='MESH' and not o.get('shared_asset')),'browser_requirements':'Standard glTF COLOR_0 and KHR_materials_unlit; no lights or custom shaders'}
(manifest_path(config).parent/f'shading_report_{suffix}.json').write_text(json.dumps(report,indent=2)+'\n')
print('ROOM_BAKE_COMPLETE',json.dumps(report),flush=True)
