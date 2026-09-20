"""051: riveted wall, parallel pipes, switch cabinet and suspended laboratory rig."""
import math
from blender_shared.lab_furniture import metal_wall,pipe,panel,gauge,cylinder
from blender_shared.furnishings import curved_line
from blender_shared.bedroom_furniture import finish

def furnish(g,c):
 b=g.box;metal_wall(g,6.4,5.1)
 for z,col in [(.47,'purple'),(.59,'purple'),(1.51,'red'),(1.65,'purple'),(1.79,'purple'),(2.54,'cyan')]:pipe(g,'Lab_wall_pipe',[(-5.99,4.76,z),(5.99,4.76,z)],.026,col,False)
 for x in [-3.63,-.63,1.62,4.71]:pipe(g,'Vertical_lab_pipe',[(x,4.71,.20),(x,4.71,3.10)],.052,'cyan')
 b('Switch_cabinet',(-2.55,4.36,.79),(1.20,.69,1.58),'cyan');b('Cabinet_gray_rim',(-2.55,3.994,.79),(1.06,.04,1.44),'gray');b('Cabinet_inset',(-2.55,3.965,.79),(.95,.02,1.31),'cyan')
 b('Lever_back',(-2.55,3.94,1.00),(.25,.05,.56),'black');b('Lever_handle',(-2.55,3.89,1.13),(.10,.12,.44),'white')
 for x in [-2.86+i*.105 for i in range(7)]:b('Cabinet_vent',(x,3.94,.23),(.032,.021,.14),'black')
 cylinder(g,'Inline_tank',(-.58,4.43,.55),(1.18,4.43,.55),.35,'cyan',28)
 for x in [-.48,-.29,.87,1.09]:cylinder(g,'Tank_band',(x-.025,4.43,.55),(x+.025,4.43,.55),.368,'green',28)
 pipe(g,'Tank_feed',[(.28,4.42,.79),(.28,4.42,1.17),(-1.41,4.75,1.17)],.055,'gray')
 b('Tank_valve',(.28,4.045,.56),(.19,.15,.24),'red')
 # Hanging apparatus, supported from ceiling pipework.
 x,y=3.47,4.38
 pipe(g,'Rig_supply',[(x,y,3.11),(x,y,2.70),(x+.53,y,2.70),(x+.73,y,3.10)],.070,'black')
 for z,r,col in [(2.71,.16,'cyan'),(2.49,.095,'gray'),(2.30,.20,'black')]:g.cyl('Rig_neck',(x,y,z),r,.19,col,20)
 gauge(g,x-.32,y-.16,2.58,.13)
 vs=[(x+r*math.cos(i*math.tau/20),y+r*math.sin(i*math.tau/20),z) for r,z in [(.43,2.09),(.14,2.31)] for i in range(20)]
 g.mesh('Rig_bell',vs,[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],'gray');g.cyl('Rig_probe',(x,y,1.95),.045,.24,'pink')
 for s in [-1,1]:
  curved_line(g,'Rig_pincer',[(x+s*.48,y,2.2),(x+s*.68,y,1.94),(x+s*.47,y,1.79)],.035,'gray')
  b('Red_terminal',(x+s*.68,4.7,1.24),(.30,.20,.12),'lightred')
 g.mesh('Purple_floor_stain',[(2.1,1.0,.003),(2.7,.89,.003),(3.2,1.1,.003),(2.9,1.24,.003),(2.35,1.19,.003)],[(0,1,2,3,4)],'purple')
 finish(c)
