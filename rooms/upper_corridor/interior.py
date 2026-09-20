"""038: diamond wallpaper, wood panels, hanging lamps and bare decorative branches."""
import math
from blender_shared.furnishings import curved_line
from blender_shared.bedroom_furniture import finish

def furnish(g,c):
 b=g.box
 for side in [-1,1]:
  x=side*8.25
  g.mesh('Corner_drapery',[(x,4.42,3.11),(x-side*.76,4.42,3.11),(x-side*.13,4.42,2.10)],[(0,1,2)],'red')
  g.beam('Drapery_gold_edge',(x-side*.76,4.40,3.11),(x-side*.13,4.40,2.10),.035,'yellow')
 ports=[p for p in c['ports'] if p['outward']==[0,1]]
 # Thin diamond lattice is one mesh; each strip is clipped away from door frames.
 vs=[];fs=[]
 for i in range(98):
  x=-8.1+i*.166
  for j in range(13):
   z=1.05+j*.162
   if any(abs(x-p['position'][0])<p['width']/2+.21 and z<p['height']+.15 for p in ports):continue
   for s in [-1,1]:
    n=len(vs);vs.extend([(x-.075,4.608,z-s*.08),(x-.067,4.608,z-s*.08),(x+.075,4.608,z+s*.08),(x+.067,4.608,z+s*.08)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Corridor_diamond_lattice',vs,fs,'lightblue')
 cuts=[(-8.25,-6.18),(-4.62,-2.58),(-1.02,1.02),(2.58,4.62),(6.18,8.25)]
 for a,bx in cuts:
  b('Corridor_wood_panel',((a+bx)/2,4.57,.48),(bx-a,.10,.88),'brown')
  for z,col in [(.08,'red'),(.83,'red'),(.94,'yellow')]:b('Wainscot_rail',((a+bx)/2,4.50,z),(bx-a,.06,.04),col)
  for x in [a+.07,bx-.07]:b('Panel_stile',(x,4.49,.47),(.038,.045,.77),'yellow')
 for x in [-3.6,0,3.6]:
  # Bare sculptural branches occupy the front border, leaving the whole doorway aisle free.
  g.cyl('Branch_pot',(x,1.10,.18),.17,.34,'lightred');g.cyl('Branch_pot_lip',(x,1.10,.36),.19,.07,'yellow')
  trunk=[(x,1.10,.39),(x+.12,1.10,.82),(x-.05,1.10,1.24),(x+.18,1.10,1.70),(x+.04,1.10,2.14)]
  curved_line(g,'Bare_branch',trunk,.037,'black')
  for s,z in [(-1,.94),(1,1.33),(-1,1.60)]:curved_line(g,'Bare_twig',[(x,1.10,z),(x+s*.28,1.10,z+.32),(x+s*.32,1.10,z+.60)],.027,'black')
  g.cyl('Lamp_chain',(x,3.8,2.97),.018,.30,'black')
  for dx in [-.20,0,.20]:
   g.beam('Lamp_bracket',(x,3.8,2.82),(x+dx,3.8,2.71),.028,'gray')
   g.sphere('Lamp_globe',(x+dx,3.8,2.64),(.075,.075,.11),'aqua')
 for i,(w,d,col) in enumerate([(10.9,1.87,'black'),(10.68,1.69,'lightblue'),(10.35,1.43,'blue')]):b('Upper_corridor_rug',(0,1.21,.002+i*.002),(w,d,.001),col)
 finish(c)
