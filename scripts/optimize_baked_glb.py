"""Losslessly compact static unlit room GLBs; preserve positions and baked colors.
Never run on animated, skinned, textured, or lit models. No quantization/decimation.
"""
import copy,gzip,json,struct
from pathlib import Path

def read(path):
 raw=Path(path).read_bytes();magic,version,total=struct.unpack_from('<4sII',raw)
 assert magic==b'glTF' and version==2 and total==len(raw)
 offset=12;chunks={}
 while offset<len(raw):
  size,kind=struct.unpack_from('<II',raw,offset);chunks[kind]=raw[offset+8:offset+8+size];offset+=8+size
 return json.loads(chunks[0x4e4f534a]),chunks[0x004e4942]

def elements(doc,data,index):
 a=doc['accessors'][index];assert 'sparse' not in a
 sizes={5121:1,5123:2,5125:4,5126:4};widths={'SCALAR':1,'VEC3':3,'VEC4':4}
 size=sizes[a['componentType']]*widths[a['type']];v=doc['bufferViews'][a['bufferView']]
 start=v.get('byteOffset',0)+a.get('byteOffset',0);stride=v.get('byteStride',size)
 return [data[start+i*stride:start+i*stride+size] for i in range(a['count'])]

def expanded(doc,data,p):
 keys=['POSITION','COLOR_0'];streams=[elements(doc,data,p['attributes'][k]) for k in keys]
 a=doc['accessors'][p['indices']];fmt={5121:'B',5123:'H',5125:'I'}[a['componentType']]
 return [b''.join(s[struct.unpack('<'+fmt,i)[0]] for s in streams) for i in elements(doc,data,p['indices'])]

def optimize(source,target):
 source,target=Path(source),Path(target)
 assert source.resolve()!=target.resolve(),'Keep the accepted source export intact'
 original,data=read(source);doc=copy.deepcopy(original)
 assert not any(k in doc for k in ['animations','skins','images','textures'])
 assert all('KHR_materials_unlit' in m.get('extensions',{}) for m in doc['materials'])
 doc['accessors']=[];doc['bufferViews']=[];binary=bytearray();before=after=0
 def accessor(raw,template,target_kind):
  binary.extend(b'\0'*((-len(binary))%4));start=len(binary);binary.extend(raw)
  view=len(doc['bufferViews']);doc['bufferViews'].append({'buffer':0,'byteOffset':start,'byteLength':len(raw),'target':target_kind})
  a={k:v for k,v in template.items() if k not in ['bufferView','byteOffset']};a['bufferView']=view
  result=len(doc['accessors']);doc['accessors'].append(a);return result
 for oldmesh,mesh in zip(original['meshes'],doc['meshes']):
  for old,p in zip(oldmesh['primitives'],mesh['primitives']):
   assert p.get('mode',4)==4 and 'targets' not in p
   assert set(p['attributes'])<= {'POSITION','NORMAL','COLOR_0'}
   position=elements(original,data,p['attributes']['POSITION']);color=elements(original,data,p['attributes']['COLOR_0'])
   assert len(position)==len(color)
   lookup={};remap=[];positions=[];colors=[]
   for v,c in zip(position,color):
    key=v+c
    if key not in lookup:lookup[key]=len(positions);positions.append(v);colors.append(c)
    remap.append(lookup[key])
   before+=len(position);after+=len(positions)
   attrs={}
   for key,values in [('POSITION',positions),('COLOR_0',colors)]:
    a=copy.deepcopy(original['accessors'][p['attributes'][key]]);a['count']=len(values)
    attrs[key]=accessor(b''.join(values),a,34962)
   olda=original['accessors'][p['indices']];fmt={5121:'B',5123:'H',5125:'I'}[olda['componentType']]
   indices=[remap[struct.unpack('<'+fmt,i)[0]] for i in elements(original,data,p['indices'])]
   code,component=('H',5123) if len(positions)<=65536 else ('I',5125)
   p['attributes']=attrs;p['indices']=accessor(struct.pack('<'+code*len(indices),*indices),{'count':len(indices),'componentType':component,'type':'SCALAR','min':[min(indices)],'max':[max(indices)]},34963)
 doc['buffers']=[{'byteLength':len(binary)}];binary.extend(b'\0'*((-len(binary))%4))
 header=json.dumps(doc,separators=(',',':')).encode();header+=b' '*((-len(header))%4)
 body=struct.pack('<II',len(header),0x4e4f534a)+header+struct.pack('<II',len(binary),0x004e4942)+binary
 target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(struct.pack('<4sII',b'glTF',2,len(body)+12)+body)
 # Verify every indexed triangle corner, including exact float color bits and winding.
 output,outdata=read(target)
 for a,b in zip(original['meshes'],output['meshes']):
  for p,q in zip(a['primitives'],b['primitives']):assert expanded(original,data,p)==expanded(output,outdata,q)
 compressed=gzip.compress(target.read_bytes(),compresslevel=9,mtime=0);Path(str(target)+'.gz').write_bytes(compressed)
 report={'source':str(source),'output':str(target),'original_bytes':source.stat().st_size,'optimized_bytes':target.stat().st_size,'gzip_bytes':len(compressed),'original_vertices':before,'optimized_vertices':after,'exact_triangle_positions_colors_and_winding':True}
 Path(str(target)+'.json').write_text(json.dumps(report,indent=2)+'\n');return report

if __name__=='__main__':
 import sys
 print(json.dumps(optimize(*sys.argv[1:]),indent=2))
