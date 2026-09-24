"""Reusable EGA pipework and metal details for the underground rooms."""
import math
from mathutils import Vector
from .furnishings import curved_line

def cylinder(g,name,a,b,r,color,segments=20):
 a,b=Vector(a),Vector(b);o=g.cyl(name,(0,0,0),r,(b-a).length,color,segments);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();o.location=(a+b)/2;return o

def pipe(g,name,points,r=.055,color='cyan',collars=True):
 for a,b in zip(points,points[1:]):
  cylinder(g,name,a,b,r,color)
  if collars:
   va,vb=Vector(a),Vector(b);axis=(vb-va).normalized()
   for t in [.08,.92]:
    p=va+(vb-va)*t;cylinder(g,name+'_joint',p-axis*.025,p+axis*.025,r*1.24,'blue' if color=='blue' else 'gray')
 for p in points[1:-1]:g.sphere(name+'_elbow',p,(r,r,r),color)

def disc(g,name,x,y,z,r,color,depth=.025):return cylinder(g,name,(x,y-depth/2,z),(x,y+depth/2,z),r,color,28)

def gauge(g,x,y,z,r=.13):
 disc(g,'Gauge_rim',x,y,z,r,'black');disc(g,'Gauge_face',x,y-.022,z,r*.78,'aqua');g.beam('Gauge_needle',(x,y-.040,z),(x+r*.36,y-.040,z+r*.43),.014,'black')

def wheel(g,x,y,z,r=.25,color='red'):
 curved_line(g,'Valve_wheel',[(x+r*math.cos(i*math.tau/24),y,z+r*math.sin(i*math.tau/24)) for i in range(25)],.045,color)
 for a in [0,math.pi/2]:g.beam('Valve_spoke',(x-r*math.cos(a),y,z-r*math.sin(a)),(x+r*math.cos(a),y,z+r*math.sin(a)),.028,color)
 disc(g,'Valve_hub',x,y,z,.06,'gray',.08)

def metal_wall(g,halfwidth,depth,height=3.12,openings=()):
 y=depth-.194;w=2*(halfwidth-.20);nx=math.ceil(w/.94);vs=[];fs=[]
 def segments(x0,x1,z):
  spans=[(x0,x1)]
  for left,right,top in openings:
   if z>=top:continue
   spans=[part for a,b in spans for part in [(a,min(b,left)),(max(a,right),b)] if part[1]>part[0]]
  return spans
 for i in range(nx):
  x=-w/2+(i+.5)*w/nx
  for j in range(6):
   z=(j+.5)*height/6;z0=j*height/6+.0105;z1=(j+1)*height/6-.0105
   cuts=sorted({z0,z1,*[top for _,_,top in openings if z0<top<z1]})
   for bottom,top in zip(cuts,cuts[1:]):
    for left,right in segments(x-w/nx/2+.0105,x+w/nx/2-.0105,(bottom+top)/2):
     g.box('Lab_wall_plate',((left+right)/2,y,(bottom+top)/2),(right-left,.020,top-bottom),'lightblue')
   for dx in [-w/nx*.39,w/nx*.39]:
    for dz in [-height/6*.37,height/6*.37]:
     xx=x+dx;zz=z+dz
     if any(xx<right and xx+.018>left and zz<top for left,right,top in openings):continue
     n=len(vs);vs.extend([(xx,y-.013,zz),(xx+.018,y-.013,zz),(xx+.018,y-.013,zz+.026),(xx,y-.013,zz+.026)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Metal_wall_rivets',vs,fs,'black')
 cuts=sorted({0,height,*[top for _,_,top in openings]})
 for bottom,top in zip(cuts,cuts[1:]):
  for left,right in segments(-w/2,w/2,(bottom+top)/2):
   g.box('Lab_wall_joint_backing',((left+right)/2,y+.023,(bottom+top)/2),(right-left,.024,top-bottom),'blue')

def panel(g,x,y,z,w=.85,h=.70):
 g.box('Control_panel',(x,y,z),(w,.19,h),'cyan');g.box('Panel_border',(x,y-.107,z),(w-.09,.025,h-.08),'black');g.box('Panel_face',(x,y-.125,z),(w-.15,.02,h-.15),'cyan')
 for i in range(2):
  for j in range(2):
   xx=x+(i-.5)*w*.48;zz=z+(j-.5)*h*.44;g.box('Switch_recess',(xx,y-.142,zz),(w*.15,.02,h*.11),'black');g.box('Switch_light',(xx-.015,y-.156,zz),(w*.065,.015,h*.055),'lightred')
