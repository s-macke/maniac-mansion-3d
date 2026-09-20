"""Background 014 is an art studio; retain the established plant_room package ID."""
from pathlib import Path
import math,random,bpy
from blender_shared.furnishings import source_patch
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Freestanding easel, solid canvas and the original still-life painting.
 for x in [-.67,.67]:geo.beam('Easel_leg',(x,3.18,.06),(x,3.73,2.67),.09,'brown')
 geo.beam('Easel_rear_leg',(0,4.35,.06),(0,3.76,2.5),.10,'brown')
 for z,w in [(.16,1.65),(.6,1.55),(2.48,1.65)]:b('Easel_crossbar',(0,3.55,z),(w,.17,.09),'brown')
 b('Canvas_back',(0,3.48,1.6),(1.68,.10,1.43),'gray')
 source_patch(geo,ROOT/'source/room 014.png',(123,41,190,93),(0,3.419,1.6),(1.65,1.39),'Original_still_life')
 # Timber tub to the right of the canvas.
 geo.cyl('Paint_tub',(1.96,4.47,.47),.54,.91,'brown',16)
 for z in [.19,.72]:geo.cyl('Tub_red_band',(1.96,4.47,z),.56,.09,'red',16)
 geo.cyl('Tub_dark_opening',(1.96,4.47,.94),.49,.035,'black',16)
 for i in range(16):
  a=i*math.tau/16;geo.beam('Tub_stave',(1.96+.545*math.cos(a),4.47+.545*math.sin(a),.08),(1.96+.545*math.cos(a),4.47+.545*math.sin(a),.9),.022,'black')
 for z in [.75,.63,.51]:b('Paint_drip',(1.99,3.905,z),(.10,.015,.17),'purple')
 # Fruit bowl on the low red pedestal, paint tin and fallen brush.
 b('Fruit_pedestal',(-2.05,2.7,.28),(.79,.70,.56),'red')
 geo.sphere('Fruit_bowl',(-2.05,2.7,.64),(.34,.24,.10),'yellow')
 for dx,dy,col in [(-.17,0,'red'),(.04,-.10,'purple'),(.17,.04,'green'),(-.02,.12,'yellow')]:geo.sphere('Wax_fruit',(-2.05+dx,2.7+dy,.77),(.12,.11,.12),col)
 geo.cyl('Paint_tin',(-1.19,2.58,.17),.13,.33,'cyan',16);geo.cyl('Paint_lid',(-1.19,2.58,.34),.14,.025,'white',16)
 geo.beam('Dropped_brush',(-1.84,2.22,.045),(-1.48,2.42,.045),.035,'brown');b('Brush_bristles',(-1.46,2.44,.045),(.15,.1,.05),'black')
 # Wall sketches preserve the supplied lines, with no invented paintings.
 for crop,x,z,w,h in [((192,20,226,57),1.08,2.46,.70,.76),((290,12,312,70),2.72,2.05,.42,1.11)]:
  source_patch(geo,ROOT/'source/room 014.png',crop,(x,5.34,z),(w,h),'Studio_sketch',only={'white','gray','black'})
 for x in [-1.25,1.6]:
  geo.cyl('Lamp_wire',(x,4.0,2.98),.018,.27,'black')
  geo.mesh('Studio_lamp_shade',[(x+r*math.cos(i*math.tau/16),4+r*math.sin(i*math.tau/16),z) for r,z in [(.24,2.77),(.055,2.97)] for i in range(16)],[(i,(i+1)%16,(i+1)%16+16,i+16) for i in range(16)],'black')
  geo.sphere('Studio_bulb',(x,4,2.79),(.08,.08,.04),'white')
 rng=random.Random(14)
 for i in range(85):
  x=rng.uniform(-2.7,2.5);y=4.25+.18*math.sin(x*2)+rng.uniform(-.10,.1)
  b('Floor_paint_speck',(x,y,.013),(rng.uniform(.025,.07),.04,.009),'purple')
 bpy.data.objects['Wall_front'].name='Front_inferred_studio'
