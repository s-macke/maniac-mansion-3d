"""Reusable ladder sections, referenced rather than duplicated in room GLBs."""
import bpy,math
from pathlib import Path
from mathutils import Matrix,Vector
ROOT=Path(__file__).resolve().parents[2]
KIT='generated/models/ladders/ladder_v1.glb'
def register(config,collection):
 ladders=config['geometry'].get('ladders',[])
 if not ladders:return
 config.setdefault('sharedAssetLibraries',{})['ladders']=KIT
 with bpy.data.libraries.load(str(ROOT/'generated/blender/shared/ladders/ladder_v1.blend'),link=False) as (_,data):data.meshes=['Ladder_section']
 mesh=data.meshes[0]
 for ladder in ladders:
  x,y,z=ladder['position'];count=round(ladder['height']/.28);base=Matrix.Translation(Vector((x,y,z)))@Matrix.Rotation(ladder['yaw'],4,'Z')
  for i in range(count):
   matrix=base@Matrix.Translation(Vector((0,0,i*.28)));id=f"{ladder['id']}_{i}"
   o=bpy.data.objects.new('Shared_'+id,mesh);collection.objects.link(o);o.matrix_world=matrix;o['shared_asset']='Ladder_section'
   config['geometry']['sharedAssets'].append({'id':id,'asset':'Ladder_section','library':'ladders','matrix':[float(matrix[r][c]) for c in range(4) for r in range(4)]})
 bpy.context.view_layer.update()
