#!/usr/bin/env python3
"""Room catalog, house validation, and independent Blender build commands."""
import argparse, json, math, re, shutil, subprocess
from pathlib import Path
from optimize_baked_glb import optimize
from room_config import load_config
ROOT = Path(__file__).resolve().parents[1]

def read(path):
    return json.loads((ROOT / path).read_text())

def world(instance, port):
    x, y, z = port['position']; c, s = math.cos(instance['yaw']), math.sin(instance['yaw'])
    ox, oy, oz = instance['position']; nx, ny = port['outward'][:2]; nz = port['outward'][2] if len(port['outward'])==3 else 0
    return (ox+c*x-s*y, oy+s*x+c*y, oz+z), (c*nx-s*ny, s*nx+c*ny, nz)

def catalog(require_outputs=True):
    layout = read('house/layout.json'); definitions = {}
    ids = [r['id'] for r in layout['rooms']]
    if len(set(ids)) != len(ids): raise ValueError('Duplicate house instance id')
    if layout['start'] not in ids: raise ValueError('Unknown start instance')
    groups = layout.get('spaces', [])
    grouped = [r for g in groups for r in g['rooms']]
    if len(grouped) != len(set(grouped)) or any(r not in ids for r in grouped): raise ValueError('Invalid space membership')
    if len({g['id'] for g in groups}) != len(groups) or any(g['id'] in ids or g['origin'] not in g['rooms'] for g in groups): raise ValueError('Invalid space id or origin')
    if layout.get('portalDepth', 3) != 3: raise ValueError('Portal depth must be three')
    space_of = lambda room: next((g['id'] for g in groups if room in g['rooms']), room)
    for instance in layout['rooms']:
        if len(instance['position']) != 3 or not all(math.isfinite(v) for v in [*instance['position'],instance['yaw']]):
            raise ValueError('Invalid placement: '+instance['id'])
        d = load_config(ROOT / instance['definition'], generated=require_outputs)
        if d['id'] in definitions and d != definitions[d['id']]: raise ValueError('Conflicting room definitions')
        definitions[d['id']] = d
        for field in (['asset','source','baked','build'] if require_outputs else ['build']):
            if not (ROOT / d[field]).is_file(): raise ValueError('Missing '+d[field])
        if not re.fullmatch(r'[a-z][a-z0-9_]*',d['id']) or not re.fullmatch(r'[a-z][a-z0-9_]*',d['navigation']): raise ValueError('Invalid room or navigation id')
        if not (ROOT/'web/lib/rooms'/f"{d['navigation']}.ts").is_file(): raise ValueError('Missing navigation module')
        if require_outputs and d.get('sharedAssetLibrary') and not (ROOT/d['sharedAssetLibrary']).is_file(): raise ValueError('Missing shared library: '+d['sharedAssetLibrary'])
        for library in d.get('sharedAssetLibraries',{}).values():
            if require_outputs and not (ROOT/library).is_file(): raise ValueError('Missing shared library: '+library)
        shared=d.get('geometry',{}).get('sharedAssets',[])
        shared_ids=[s['id'] for s in shared]
        if len(shared_ids)!=len(set(shared_ids)): raise ValueError('Duplicate shared instance: '+d['id'])
        if any(not s.get('library') for s in shared) and not d.get('sharedAssetLibrary'): raise ValueError('Missing shared library reference')
        nodes={l['node'] for door in d.get('geometry',{}).get('doors',[]) for l in door['leaves']}
        for s in shared:
            allowed=['Ladder_section'] if s.get('library')=='ladders' else ['Standard_leaf','Standard_frame','Pool_leaf','Pool_frame','Security_leaf','Security_frame','Entrance_transom','Concealed_leaf','Grating_leaf']
            if s.get('library') and s['library'] not in d.get('sharedAssetLibraries',{}): raise ValueError('Unknown shared library: '+s['library'])
            if s['asset'] not in allowed or len(s['matrix'])!=16 or not all(math.isfinite(v) for v in s['matrix']): raise ValueError('Invalid shared instance: '+s['id'])
            if s.get('doorNode') and s['doorNode'] not in nodes: raise ValueError('Unknown shared door hinge: '+s['id'])
        ports = [p['id'] for p in d['ports']]
        if len(ports) != len(set(ports)): raise ValueError('Duplicate port: '+d['id'])
        for p in d['ports']:
            if p['width'] <= 0 or abs(math.sqrt(sum(v*v for v in p['outward']))-1)>1e-6: raise ValueError('Invalid port: '+p['id'])
    instances = {i['id']: i for i in layout['rooms']}; occupied = set()
    for link in layout['connections']:
        endpoints = []
        for end in [link['a'],link['b']]:
            key=(end['instance'],end['port'])
            if key in occupied: raise ValueError('Port connected twice: '+str(key))
            occupied.add(key); i=instances[end['instance']]
            if i.get('previewOnly'): raise ValueError('A preview-only room cannot have house connections')
            d=read(i['definition'])
            p=next(p for p in d['ports'] if p['id']==end['port'])
            if p['state']!='open': raise ValueError('Connection uses a closed port: '+str(key))
            if p.get('kind')!='hatch' and p.get('height', 0) < (.6 if p.get('kind')=='crawl' else 1.62): raise ValueError('Connected aperture too low: '+p['id'])
            endpoints.append((world(i,p),p))
        (a,an),(b,bn) = [v[0] for v in endpoints]
        if space_of(link['a']['instance']) == space_of(link['b']['instance']) and (math.dist(a,b)>.02 or math.dist(an,[-v for v in bn])>.01): raise ValueError('Misaligned continuous connection: '+str(link))
        if endpoints[0][1].get('kind')!=endpoints[1][1].get('kind'): raise ValueError('Connection kinds differ')
        if endpoints[0][1].get('kind')=='hatch' and (any(p.get('depth',0)<=0 or p['outward'][:2]!=[0,0] or abs(p['outward'][2])!=1 for _,p in endpoints) or abs(endpoints[0][1]['depth']-endpoints[1][1]['depth'])>.001): raise ValueError('Invalid hatch aperture')
        if abs(endpoints[0][1]['width']-endpoints[1][1]['width'])>.02: raise ValueError('Connection widths differ')
    ladders=layout.get('ladders',[])
    if len({l['id'] for l in ladders}) != len(ladders): raise ValueError('Duplicate ladder connection')
    for ladder in ladders:
        if ladder['lower']['room']==ladder['upper']['room']: raise ValueError('Ladder endpoints must be different rooms')
        pair={(ladder[key]['room'],ladder[key]['port']) for key in ['lower','upper']}
        if not any({(link[key]['instance'],link[key]['port']) for key in ['a','b']}==pair for link in layout['connections']): raise ValueError('Ladder endpoints must share one portal connection')
        for key in ['lower','upper']:
            end=ladder[key]
            if end['room'] not in ids: raise ValueError('Unknown ladder room')
            if (end['room'],end['port']) not in occupied: raise ValueError('Ladder needs a connected hatch')
            d=read(instances[end['room']]['definition'])
            port=next(p for p in d['ports'] if p['id']==end['port'])
            if port.get('kind')!='hatch' or port['outward'][2]!=(1 if key=='lower' else -1): raise ValueError('Invalid ladder hatch orientation')
            if key=='lower' and port['position'][2]<=end['landing']['height']: raise ValueError('Ladder must rise to its hatch')
            if not all(math.isfinite(v) for v in [*end['landing'].values(),*end['shaft'].values(),end['yaw']]): raise ValueError('Invalid ladder endpoint')
    crawls=layout.get('crawls',[])
    for crawl in crawls:
        pair={(crawl[key]['room'],crawl[key]['port']) for key in ['a','b']}
        if not any({(link[key]['instance'],link[key]['port']) for key in ['a','b']}==pair for link in layout['connections']): raise ValueError('Crawl requires connected endpoints')
        for key in ['a','b']:
            end=crawl[key];d=read(instances[end['room']]['definition']);p=next(p for p in d['ports'] if p['id']==end['port'])
            if p.get('kind')!='crawl': raise ValueError('Crawl requires low portal ports')
        if not crawl['waypoints'] or not all(math.isfinite(v) for p in [crawl['a']['landing'],crawl['b']['landing'],*crawl['waypoints']] for v in p.values()): raise ValueError('Invalid crawl path')
    return layout, definitions

def sync(layout, definitions):
    # Generated browser manifest deliberately includes no Blender filesystem paths.
    rooms=[]
    for i in layout['rooms']:
        d=definitions[read(i['definition'])['id']];source=ROOT/d['asset'];compact=source.with_name(source.stem+'_compact.glb')
        optimize(source,compact)
        target=ROOT/'web/public/models'/d['id']/source.name
        target.parent.mkdir(parents=True,exist_ok=True)
        if not target.exists() or target.read_bytes()!=compact.read_bytes(): shutil.copyfile(compact,target)
        shutil.copyfile(str(compact)+'.gz',str(target)+'.gz')
        rooms.append({**{k:v for k,v in i.items() if k!='definition'},'definition':d['id']})
    libraries={d['sharedAssetLibrary'] for d in definitions.values() if d.get('sharedAssetLibrary')}
    libraries.update(path for d in definitions.values() for path in d.get('sharedAssetLibraries',{}).values())
    for path in libraries:
        source=ROOT/path;compact=source.with_name(source.stem+'_compact.glb');optimize(source,compact)
        target=ROOT/'web/public/models/shared'/source.name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(compact,target);shutil.copyfile(str(compact)+'.gz',str(target)+'.gz')
    runtime={**layout,'rooms':rooms,'definitions':{k:{**{field:d[field] for field in ['id','label','backgrounds','navigation','bounds','spawn','geometry','ports']},'asset':'/models/'+d['id']+'/'+Path(d['asset']).name,**({'sharedAssetLibrary':'/models/shared/'+Path(d['sharedAssetLibrary']).name} if d.get('sharedAssetLibrary') else {}),**({'sharedAssetLibraries':{id:'/models/shared/'+Path(path).name for id,path in d['sharedAssetLibraries'].items()}} if d.get('sharedAssetLibraries') else {})} for k,d in definitions.items()}}
    target=ROOT/'web/lib/house/generated.json';target.write_text(json.dumps(runtime,indent=2)+'\n')
    names=sorted({d['navigation'] for d in definitions.values()})
    imports=[f"import * as room_{i} from '../rooms/{name}';" for i,name in enumerate(names)]
    registry="// Generated by scripts/build.py sync; edit room packages instead.\nimport type { Navigation } from './types';\n"+'\n'.join(imports)+"\nexport const adapters:Record<string,Navigation>={"+','.join(f'{name}:room_{i}' for i,name in enumerate(names))+"};\n"
    (ROOT/'web/lib/house/adapters.generated.ts').write_text(registry)
    print('Synced',len(rooms),'house unit(s); losslessly optimized exports and gzip downloads prepared.')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['list','check','sync','build','bake'])
    parser.add_argument('room',nargs='?');parser.add_argument('--blender',default=str(ROOT/'blender-4.2.3-linux-x64/blender'))
    args=parser.parse_args();layout,definitions=catalog(require_outputs=args.command in ['check','sync'])
    if args.command=='list':
        for id,d in definitions.items():print(id+' — '+d['label']+' — backgrounds '+', '.join(d['backgrounds']))
    elif args.command=='check':print('House definitions, assets, navigation modules, and connections valid.')
    elif args.command=='sync':sync(layout,definitions)
    else:
        if args.room not in definitions:parser.error('Choose a room from the list command')
        d=definitions[args.room]
        script=d['build'] if args.command=='build' else 'scripts/blender_shared/bake.py'
        subprocess.run([args.blender,'-b','-t','8','--python-exit-code','1','--python',str(ROOT/script),'--','--room-config',str(ROOT/next(i['definition'] for i in layout['rooms'] if read(i['definition'])['id']==args.room))],check=True,cwd=ROOT)

if __name__=='__main__': main()
