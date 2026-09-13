"""Declare baked COLOR_0 as standard unlit base color in Blender's GLB export.
Blender 4.2 exports vertex-color emission as white emission/black base; that
cannot carry the bake in glTF. Keep the geometry/color buffers, fix semantics.
"""
import json,struct
from pathlib import Path

def finalize(path):
 path=Path(path);raw=path.read_bytes();magic,version,total=struct.unpack_from('<4sII',raw)
 assert magic==b'glTF' and version==2 and total==len(raw)
 chunks=[];off=12
 while off<len(raw):
  size,kind=struct.unpack_from('<II',raw,off);chunks.append((kind,raw[off+8:off+8+size]));off+=8+size
 doc=json.loads(chunks[0][1])
 for material in doc['materials']:
  material.pop('emissiveFactor',None);material.pop('emissiveTexture',None)
  material['pbrMetallicRoughness']={'baseColorFactor':[1,1,1,1],'metallicFactor':0,'roughnessFactor':1}
  material['extensions']={'KHR_materials_unlit':{}}
 for mesh in doc['meshes']:
  for primitive in mesh['primitives']:
   assert 'COLOR_0' in primitive['attributes']
   attrs=primitive['attributes'];baked=attrs.pop('COLOR_1',None)
   if baked is None and doc['accessors'][attrs['COLOR_0']]['componentType']==5121:
    # Repair an earlier finalized file: Blender placed the actual emission
    # colors immediately after its all-white base-color attribute.
    candidate=attrs['COLOR_0']+1
    assert doc['accessors'][candidate]['componentType']==5126
    assert doc['accessors'][candidate]['type']=='VEC3'
    assert doc['accessors'][candidate]['count']==doc['accessors'][attrs['COLOR_0']]['count']
    baked=candidate
   if baked is not None:attrs['COLOR_0']=baked
 doc['extensionsUsed']=sorted(set(doc.get('extensionsUsed',[]))|{'KHR_materials_unlit'})
 doc['extensionsRequired']=sorted(set(doc.get('extensionsRequired',[]))|{'KHR_materials_unlit'})
 data=json.dumps(doc,separators=(',',':')).encode();data+=b' '*((-len(data))%4)
 chunks[0]=(chunks[0][0],data)
 body=b''.join(struct.pack('<II',len(data),kind)+data for kind,data in chunks)
 path.write_bytes(struct.pack('<4sII',b'glTF',2,len(body)+12)+body)
 return doc
if __name__=='__main__':
 import sys
 for arg in sys.argv[1:]:
  doc=finalize(arg);print(arg,len(doc['meshes']),'meshes: unlit vertex-color semantics verified')
