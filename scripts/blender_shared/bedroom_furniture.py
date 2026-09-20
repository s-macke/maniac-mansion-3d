"""Small shared solid forms for the furnished bedroom level; original EGA materials."""
import math,bpy
from .furnishings import curved_line

def finish(c):
 for o in list(bpy.data.objects):
  if o.name.startswith('Wall_front'):o.name='Front_inferred_'+c['id']

def cabinet(g,name,x,y,w,d,h,color='brown'):
 g.box(name,(x,y,h/2),(w,d,h),color)
 g.box(name+'_top',(x,y,h+.035),(w+.10,d+.10,.07),'red')
 for dx in [-w*.44,w*.44]:g.box(name+'_foot',(x+dx,y,.09),(.12,d,.18),'brown')
 for inset,yy,col in [(0,0,'black'),(.045,-.015,'yellow'),(.09,-.03,'red'),(.14,-.045,color)]:
  g.box(name+'_panel',(x,y-d/2-.02+yy,h*.53),(w-.20-inset,.024,h*.67-inset),col)

def bed(g,x,y,w=2.6,d=1.35,color='blue',frame='brown'):
 g.box('Bed_frame',(x,y,.31),(w,d,.42),frame)
 g.box('Bed_mattress',(x,y,.59),(w-.10,d-.06,.24),'white')
 g.box('Bed_cover',(x+.19,y,.63),(w-.48,d+.02,.25),color)
 g.box('Cover_front_drop',(x+.19,y-d/2-.025,.42),(w-.48,.055,.40),color)
 g.sphere('Pillow',(x-w*.34,y,.79),(.37,d*.34,.12),color)
 for dx in [-w/2,w/2]:
  g.box('Bed_end',(x+dx,y,.57),(.13,d+.1,.85),frame)
  g.sphere('Bed_end_round',(x+dx,y,.98),(.068,(d+.1)/2,.16),frame)

def plant(g,x,y,height=1.45,color='cyan'):
 g.cyl('Plant_pot',(x,y,.22),.24,.40,color,16);g.cyl('Pot_rim',(x,y,.40),.28,.10,color,16);g.cyl('Soil',(x,y,.457),.22,.012,'brown',16)
 for i in range(8):
  a=i*math.tau/8;start=(x,y,.46);tip=(x+.58*math.cos(a),y+.58*math.sin(a),height-.25*(i%3))
  mid=(x+.2*math.cos(a),y+.2*math.sin(a),height*.84)
  curved_line(g,'Plant_stem',[start,mid,tip],.025,'green')
  side=(-math.sin(a)*.09,math.cos(a)*.09)
  g.mesh('Plant_leaf',[mid,(mid[0]+side[0],mid[1]+side[1],mid[2]+.15),tip,(mid[0]-side[0],mid[1]-side[1],mid[2]-.06)],[(0,1,2,3)],'lime' if i%2 else 'green')

def chandelier(g,x,y,color='aqua'):
 g.cyl('Pendant_stem',(x,y,2.81),.03,.62,'black')
 for s in [-1,1]:
  curved_line(g,'Pendant_arm',[(x,y,2.5),(x+s*.35,y,2.47),(x+s*.43,y,2.68)],.035,'black')
  g.sphere('Pendant_globe',(x+s*.43,y,2.73),(.12,.12,.15),color)
  g.sphere('Globe_glint',(x+s*.43-.025,y-.095,2.77),(.038,.024,.08),'white')

def pattern(g,name,x0,x1,y,z0,z1,kind,color,ports=()):
 """Batch repeating wallpaper polygons, omitting existing door apertures."""
 vs=[];fs=[]
 for row in range(int((z1-z0)/.24)):
  z=z0+.12+row*.24
  for col in range(int((x1-x0)/.25)):
   x=x0+.12+col*.25+(row%2)*.125
   if x>x1-.09 or any(abs(x-p['position'][0])<p['width']/2+.18 and z<p['height']+.15 for p in ports):continue
   pts=([(-.10,.04),(-.08,.095),(-.03,.095),(0,.055),(.03,.095),(.08,.095),(.10,.04),(0,-.10)] if kind=='heart' else [(-.075,0),(0,.105),(.075,0),(0,-.105)])
   n=len(vs);vs.extend([(x+u,y,z+v) for u,v in pts]);fs.append(tuple(range(n,n+len(pts))))
 g.mesh(name,vs,fs,color)
