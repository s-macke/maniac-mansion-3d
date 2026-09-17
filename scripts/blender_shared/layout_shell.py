"""Layout-only rectangular rooms with named wall ports and shared door assets."""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
from .shell import setup,reference
from room_config import load_config,save_generated
from .door_assets import register_static,register_hinged,KIT
PALETTE={'black':(0,0,0),'red':(168,0,0),'brown':(168,84,0),'yellow':(252,252,84),'blue':(0,0,168),'lightblue':(84,84,252),'green':(0,168,0),'cyan':(0,168,168),'aqua':(84,252,252),'purple':(168,0,168),'pink':(252,84,252),'lightred':(252,84,84),'lime':(84,252,84),'gray':(168,168,168),'white':(252,252,252)}

def build(path, furnish=None):
 root=Path(__file__).resolve().parents[2];c=load_config(path,prepare=True);g=c['geometry'];style=c['shell'];W=g['halfWidth'];D=g['depth'];H=g['height'];T=g['wallThickness']
 scene,cols,geo=setup(PALETTE);box=geo.box;ports={p['id']:p for p in c['ports']};stair=g.get('stairs')
 def slab(name,x0,x1,y0,y1,z,thickness,color,holes):
  xs=sorted(set([x0,x1]+[max(x0,min(x1,h[k])) for h in holes for k in ['x0','x1']]))
  ys=sorted(set([y0,y1]+[max(y0,min(y1,h[k])) for h in holes for k in ['y0','y1']]))
  for a,b in zip(xs,xs[1:]):
   for low,high in zip(ys,ys[1:]):
    if any(h['x0']<(a+b)/2<h['x1'] and h['y0']<(low+high)/2<h['y1'] for h in holes):continue
    if b>a and high>low:box(name,((a+b)/2,(low+high)/2,z),(b-a,high-low,thickness),color)
 slab('Room_floor',-W,W,0,D,-.06,.12,style['floor'],g.get('floorHoles',[]))
 stair_side='left' if stair and stair['x0']<0 else 'right'
 inner=(stair['x1']+.15 if stair_side=='left' else stair['x0']-.15) if stair else W
 ceiling_lo=inner if stair and stair_side=='left' else -W
 ceiling_hi=inner if stair and stair_side=='right' else W
 slab('Ceiling_room',ceiling_lo,ceiling_hi,0,D,H+.02,.04,style['wall'],g.get('ceilingHoles',[]))
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
    box('Wall_'+direction,loc,size,style.get('wallColors',{}).get(direction,style['wall']))
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
  lo,hi=(-W,inner) if stair_side=='left' else (inner,W)
  wall('back',lo,hi,H,rise+H,[ports['higher_floor']]);wall(stair_side,0,D,H,rise+H,[])
  box('Stairwell_side',(inner,D/2,(H+rise+H)/2),(.15,D,rise),style['wall'])
  box('Stairwell_front',((lo+hi)/2,T/2,(H+rise+H)/2),(hi-lo,T,rise),style['wall'])
  box('Ceiling_stairwell',((lo+hi)/2,D/2,rise+H+.02),(hi-lo,D,.04),style['wall'])
 # Opaque window panels preserve the artwork without exposing unrelated room spaces.
 for window in style.get('windows',[]):
  x,z,w,h=[window[k] for k in ['x','z','width','height']];y=D-T-.05
  box('Window_frame',(x,y,z),(w+.14,.10,h+.14),'brown')
  box('Window_dark_glass',(x,y-.07,z),(w,.06,h),'black')
  for dx in [-w/2,0,w/2]:box('Window_mullion',(x+dx,y-.12,z),(.04,.05,h),'gray')
  for dz in [-h/2,-h/6,h/6,h/2]:box('Window_crossbar',(x,y-.12,z+dz),(w,.05,.035),'gray')
  box('Window_sill',(x,y-.08,z-h/2-.10),(w+.22,.24,.12),'brown')
 c['geometry']['doors']=[];c['geometry']['sharedAssets']=[];c['sharedAssetLibrary']=KIT
 for e in style['entries']:
  p=ports[e['port']];rot={'back':0,'front':math.pi,'left':math.pi/2,'right':-math.pi/2}[e['wall']];base=Matrix.Translation(Vector(p['position']))@Matrix.Rotation(rot,4,'Z');w=p['width'];h=p['height'];key=p['id']
  if e.get('frame'):register_static(c,[('Standard_frame',base@Matrix.Diagonal(Vector((w,1,h,1))),cols['Doors'],key+'_frame')])
  closed=base@Matrix.Translation(Vector((0,-.18,h/2)))@Matrix.Diagonal(Vector((-(w-.035),1,h-.10,1)))
  if e.get('owner'):register_hinged(c,e.get('asset','Standard_leaf'),closed,base@Vector((-w/2,-.18,0)),-math.pi/2,cols['Doors'],port=key,node='Door_'+key,label=e.get('label',key.replace('_',' ').capitalize()),instance_id=key+'_leaf')
  elif e.get('leaf'):register_static(c,[(e.get('asset','Standard_leaf'),closed,cols['Doors'],key+'_leaf')])
 from .ladder_assets import register as register_ladders
 register_ladders(c,cols['Architecture'])
 for level,holes in [(0,g.get('floorHoles',[])),(H,g.get('ceilingHoles',[]))]:
  for hole in holes:
   x0,x1,y0,y1=[hole[k] for k in ['x0','x1','y0','y1']]
   for x in [x0,x1]:box('Hatch_frame',(x,(y0+y1)/2,level+.025),(.07,y1-y0+.07,.06),'brown')
   for y in [y0,y1]:box('Hatch_frame',((x0+x1)/2,y,level+.025),(x1-x0,.07,.06),'brown')
   if hole.get('top',level)>level:
    top=hole['top'];z=(level+top)/2
    for x in [x0,x1]:box('Hatch_shaft',(x,(y0+y1)/2,z),(.07,y1-y0+.07,top-level),style['wall'])
    for y in [y0,y1]:box('Hatch_shaft',((x0+x1)/2,y,z),(x1-x0,.07,top-level),style['wall'])
 if furnish:furnish(geo,c)
 reference(root,c,cols,c['backgrounds'][0]);geo.active='Cameras'
 geo.camera('01_Reference',(0,-max(8,W*1.6),4.5),(0,D/2,1.3),lens=27)
 geo.camera('02_Inside',(-W+.9,.9,1.62),(0,D-.5,1.5),lens=22)
 geo.camera('03_Reverse',(W-1,D-.8,1.62),(0,.3,1.5),lens=22)
 scene.camera=bpy.data.objects['02_Inside'];scene['room_id']=c['backgrounds'][0];scene['scope']='Furnished room with shared doors.' if furnish else 'Room shell, shared doors and circulation only; interior details deferred.'
 scene.render.resolution_x=1000;scene.render.resolution_y=650
 save_generated(c);bpy.ops.wm.save_as_mainfile(filepath=str(root/c['source']));print('LAYOUT_ROOM_COMPLETE',c['id'],flush=True)
