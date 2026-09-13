"""Layout-only rectangular rooms with named wall ports and shared door assets."""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
from .shell import setup,reference
from room_config import load_config,save_generated
from .door_assets import register_static,register_hinged,KIT
PALETTE={'black':(0,0,0),'red':(168,0,0),'brown':(168,84,0),'yellow':(252,252,84),'blue':(0,0,168),'lightblue':(84,84,252),'green':(0,168,0),'cyan':(0,168,168),'aqua':(84,252,252),'purple':(168,0,168),'pink':(252,84,252),'gray':(168,168,168),'white':(252,252,252)}

def build(path):
 root=Path(__file__).resolve().parents[2];c=load_config(path,prepare=True);g=c['geometry'];style=c['shell'];W=g['halfWidth'];D=g['depth'];H=g['height'];T=g['wallThickness']
 scene,cols,geo=setup(PALETTE);box=geo.box;ports={p['id']:p for p in c['ports']};stair=g.get('stairs')
 box('Room_floor',(0,D/2,-.06),(2*W,D,.12),style['floor'])
 end=5.1 if stair else W
 box('Ceiling_room',((-W+end)/2,D/2,H+.02),(end+W,D,.04),style['wall'])
 def wall(direction,lo,hi,z0,z1,openings,offset=0):
  cuts=sorted(set([lo,hi]+[max(lo,min(hi,p['position'][1 if direction in ['left','right'] else 0]+s*p['width']/2)) for p in openings for s in [-1,1]]))
  for a,b in zip(cuts,cuts[1:]):
   if b-a<1e-5:continue
   mid=(a+b)/2;holes=[(p['position'][2],p['position'][2]+p['height']) for p in openings if abs(mid-p['position'][1 if direction in ['left','right'] else 0])<p['width']/2]
   zs=sorted(set([z0,z1]+[max(z0,min(z1,z)) for h in holes for z in h]))
   for low,high in zip(zs,zs[1:]):
    if high-low<1e-5 or any(l<=(low+high)/2<=h for l,h in holes):continue
    if direction in ['left','right']:loc=((1 if direction=='right' else -1)*(W-T/2),mid,(low+high)/2);size=(T,b-a,high-low)
    else:loc=(mid,D-T/2 if direction=='back' else T/2+offset,(low+high)/2);size=(b-a,T,high-low)
    box('Wall_'+direction,loc,size,style['wall'])
   if not any(l<=.13<=h for l,h in holes) and z0==0:
    if direction in ['left','right']:loc=((1 if direction=='right' else -1)*(W-T-.018),mid,.13);size=(.036,b-a,.26)
    else:loc=(mid,D-T-.018 if direction=='back' else T+.018+offset,.13);size=(b-a,.036,.26)
    box('Skirting',loc,size,style['trim'])
 for direction in ['left','right','front','back']:
  wall(direction,0 if direction in ['left','right'] else -W,D if direction in ['left','right'] else W,0,H,[ports[e['port']] for e in style['entries'] if e['wall']==direction],style.get('frontOffset',0) if direction=='front' else 0)
 if stair:
  x0,x1,y0,y1,rise,n=[stair[k] for k in ['x0','x1','y0','y1','rise','segments']]
  for i in range(n):
   h=rise*(i+1)/n;a=y0+(y1-y0)*i/n;b=y0+(y1-y0)*(i+1)/n
   box('Stair_tread',((x0+x1)/2,(a+b)/2,h/2),(x1-x0,b-a,h),'brown')
   box('Stair_edge',((x0+x1)/2,a+.02,h+.005),(x1-x0,.04,.02),'white')
  box('Upper_landing',((x0+x1)/2,(y1+D)/2,rise-.08),(x1-x0,D-y1,.16),style['floor'])
  for x in [x0,x1]:geo.beam('Stair_rail',(x,y0,.9),(x,y1,rise+.9),.07,'brown')
  wall('back',5.1,W,H,rise+H,[ports['higher_floor']]);wall('right',0,D,H,rise+H,[])
  box('Stairwell_side',(5.1,D/2,(H+rise+H)/2),(.15,D,rise),style['wall'])
  box('Stairwell_front',((5.1+W)/2,.09,(H+rise+H)/2),(W-5.1,.18,rise),style['wall'])
  box('Ceiling_stairwell',((5.1+W)/2,D/2,rise+H+.02),(W-5.1,D,.04),style['wall'])
 c['geometry']['doors']=[];c['geometry']['sharedAssets']=[];c['sharedAssetLibrary']=KIT
 for e in style['entries']:
  p=ports[e['port']];rot={'back':0,'front':math.pi,'left':math.pi/2,'right':-math.pi/2}[e['wall']];base=Matrix.Translation(Vector(p['position']))@Matrix.Rotation(rot,4,'Z');w=p['width'];h=p['height'];key=p['id']
  if e.get('frame'):register_static(c,[('Standard_frame',base@Matrix.Diagonal(Vector((w,1,h,1))),cols['Doors'],key+'_frame')])
  closed=base@Matrix.Translation(Vector((0,-.18,h/2)))@Matrix.Diagonal(Vector((-(w-.035),1,h-.10,1)))
  if e.get('owner'):register_hinged(c,'Standard_leaf',closed,base@Vector((-w/2,-.18,0)),-math.pi/2,cols['Doors'],port=key,node='Door_'+key,label=key.replace('_',' ').capitalize(),instance_id=key+'_leaf')
  elif e.get('leaf'):register_static(c,[('Standard_leaf',closed,cols['Doors'],key+'_leaf')])
 reference(root,c,cols,c['backgrounds'][0]);geo.active='Cameras'
 geo.camera('01_Reference',(0,-max(8,W*1.6),4.5),(0,D/2,1.3),lens=27)
 geo.camera('02_Inside',(-W+.9,.9,1.62),(0,D-.5,1.5),lens=22)
 geo.camera('03_Reverse',(W-1,D-.8,1.62),(0,.3,1.5),lens=22)
 scene.camera=bpy.data.objects['02_Inside'];scene['room_id']=c['backgrounds'][0];scene['scope']='Room shell, shared doors and circulation only; interior details deferred.'
 scene.render.resolution_x=1000;scene.render.resolution_y=650
 save_generated(c);bpy.ops.wm.save_as_mainfile(filepath=str(root/c['source']));print('LAYOUT_ROOM_COMPLETE',c['id'],flush=True)
