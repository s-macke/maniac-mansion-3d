"""Replace standard door construction meshes with reusable kit instances.
Room builders keep dimensions and openings; the common kit owns appearance.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2]
KIT='generated/models/doors/standard_doors_v1.glb'

def register(config,specs):
 bpy.context.view_layer.update()
 with bpy.data.libraries.load(str(ROOT/'generated/blender/shared/doors/standard_doors_v1.blend'),link=False) as (a,b):b.meshes=['Standard_leaf','Standard_frame']
 meshes=dict(zip(['Standard_leaf','Standard_frame'],b.meshes));instances=[];remove=set()
 leaves_by_node={l['node']:l for d in config['geometry'].get('doors',[]) for l in d['leaves']}
 def instance(id,asset,matrix,collection,door_node=None):
  entry={'id':id,'asset':asset,'matrix':[float(matrix[r][c]) for c in range(4) for r in range(4)]}
  o=bpy.data.objects.new('Shared_'+id,meshes[asset]);collection.objects.link(o);o['shared_asset']=asset
  if door_node:
   leaf=leaves_by_node[door_node];hinge=Vector(leaf['hinge']);pivot=bpy.data.objects.new(door_node,None);collection.objects.link(pivot);pivot.location=hinge;pivot['shared_asset']='pivot'
   matrix=Matrix.Translation(-hinge)@matrix;entry['matrix']=[float(matrix[r][c]) for c in range(4) for r in range(4)];entry['doorNode']=door_node
   o.parent=pivot;o['door_node']=door_node
  o.matrix_local=matrix;instances.append(entry)
 for prefix,width,height in specs:
  parts=[o for o in bpy.data.objects if o.type=='MESH' and o.name.startswith(tuple(prefix+s for s in ['_leaf','_raised_panel','_knob','_jamb','_lintel']))]
  if not parts:raise ValueError('Missing standard door: '+prefix)
  remove.update(parts);frame=bpy.data.objects.get(prefix+'_jamb')
  if frame:
   matrix=frame.matrix_world@Matrix.Translation(Vector(((width+.21)/2-.019,.1,-height/2)))@Matrix.Diagonal(Vector((width,1,height,1)))
   instance(prefix+'_frame','Standard_frame',matrix,frame.users_collection[0])
  for leaf in [o for o in parts if o.name.startswith(prefix+'_leaf')]:
   node=leaf.get('door_node');knobs=[o for o in parts if o.name.startswith(prefix+'_knob') and (not node or o.get('door_node')==node)]
   # Choose the nearest handle, including mirrored double leaves and existing open poses.
   knob=min(knobs,key=lambda o:(o.matrix_world.translation-leaf.matrix_world.translation).length)
   local=leaf.matrix_world.inverted()@knob.matrix_world.translation;mirror=-1 if local.x>0 else 1
   xs=[v.co.x for v in leaf.data.vertices];zs=[v.co.z for v in leaf.data.vertices]
   matrix=leaf.matrix_world@Matrix.Diagonal(Vector(((max(xs)-min(xs))*mirror,1,max(zs)-min(zs),1)))
   instance(leaf.name,'Standard_leaf',matrix,leaf.users_collection[0],node)
 for o in remove:bpy.data.objects.remove(o,do_unlink=True)
 config['geometry']['sharedAssets']=instances;config['sharedAssetLibrary']=KIT
 bpy.context.view_layer.update()
 return instances


def register_static(config,specs):
 """Attach distinctive library meshes; specs are (asset, placement matrix, collection)."""
 names=list(dict.fromkeys(spec[0] for spec in specs))
 with bpy.data.libraries.load(str(ROOT/'generated/blender/shared/doors/standard_doors_v1.blend'),link=False) as (a,b):b.meshes=list(names)
 meshes=dict(zip(names,b.meshes))
 for spec in specs:
  asset,matrix,collection=spec[:3];instance_id=spec[3] if len(spec)>3 else asset
  obj=bpy.data.objects.new('Shared_'+instance_id,meshes[asset]);collection.objects.link(obj);obj.matrix_world=matrix;obj['shared_asset']=asset
  config['geometry']['sharedAssets'].append({'id':instance_id,'asset':asset,'matrix':[float(matrix[r][c]) for c in range(4) for r in range(4)]})
 bpy.context.view_layer.update()


def register_hinged(config,asset,closed_matrix,hinge,angle,collection,*,port,node,label,instance_id=None,append_leaf=False):
 """Attach a library leaf in its open rest pose; runtime closes it initially."""
 with bpy.data.libraries.load(str(ROOT/'generated/blender/shared/doors/standard_doors_v1.blend'),link=False) as (a,b):b.meshes=[asset]
 mesh=b.meshes[0];hinge=Vector(hinge)
 opened=Matrix.Translation(hinge)@Matrix.Rotation(angle,4,'Z')@Matrix.Translation(-hinge)@closed_matrix
 points=[opened@v.co for v in mesh.vertices]
 leaf={'node':node,'hinge':list(hinge),'openAngle':angle,'min':[min(p[i] for p in points) for i in range(3)],'max':[max(p[i] for p in points) for i in range(3)]}
 previous=next((d['leaves'] for d in config['geometry'].get('doors',[]) if d['id']==port),[]) if append_leaf else []
 config['geometry']['doors']=[d for d in config['geometry'].get('doors',[]) if d['id']!=port]+[{'id':port,'label':label,'port':port,'initialOpen':False,'leaves':previous+[leaf]}]
 pivot=bpy.data.objects.new(node,None);collection.objects.link(pivot);pivot.location=hinge;pivot['shared_asset']='pivot'
 obj=bpy.data.objects.new('Shared_'+asset,mesh);collection.objects.link(obj);obj.parent=pivot;obj['shared_asset']=asset;obj['door_node']=node
 local=Matrix.Translation(-hinge)@opened;obj.matrix_local=local
 config['geometry']['sharedAssets'].append({'id':instance_id or asset,'asset':asset,'doorNode':node,'matrix':[float(local[r][c]) for c in range(4) for r in range(4)]})
 bpy.context.view_layer.update()
