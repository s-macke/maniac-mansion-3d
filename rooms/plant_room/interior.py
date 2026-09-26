"""Background 014 is an art studio; retain the established plant_room package ID."""
from pathlib import Path
import math,random,bpy
from mathutils import Matrix
from blender_shared.furnishings import source_patch,curved_line
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Freestanding easel, solid canvas and the original still-life painting.
 for x in [-.67,.67]:geo.beam('Easel_leg',(x,3.18,.06),(x,3.73,2.67),.09,'brown')
 geo.beam('Easel_rear_leg',(0,4.35,.06),(0,3.76,2.5),.10,'brown')
 for z,w in [(.16,1.65),(.6,1.55),(2.48,1.65)]:b('Easel_crossbar',(0,3.55,z),(w,.17,.09),'brown')
 b('Canvas_back',(0,3.48,1.6),(1.68,.10,1.43),'gray')
 source_patch(geo,ROOT/'source/room 014.png',(123,41,190,93),(0,3.419,1.6),(1.65,1.39),'Original_still_life')
 # Two screw clamps project above the canvas in background 014.
 for x in [-.45,.45]:
  b('Canvas_clamp_stem',(x,3.48,2.61),(.085,.10,.35),'brown')
  b('Canvas_clamp_ink',(x,3.405,2.48),(.25,.08,.23),'black')
  b('Canvas_clamp_red',(x,3.356,2.48),(.19,.025,.17),'red')
  b('Canvas_clamp_screw',(x,3.333,2.48),(.10,.023,.034),'gray')
 # Timber tub to the right of the canvas.
 geo.cyl('Paint_tub',(1.96,4.47,.47),.54,.91,'brown',16)
 for z in [.19,.72]:geo.cyl('Tub_red_band',(1.96,4.47,z),.56,.09,'red',16)
 geo.cyl('Tub_dark_opening',(1.96,4.47,.94),.49,.035,'black',16)
 for i in range(16):
  a=i*math.tau/16;geo.beam('Tub_stave',(1.96+.545*math.cos(a),4.47+.545*math.sin(a),.08),(1.96+.545*math.cos(a),4.47+.545*math.sin(a),.9),.022,'black')
 for z in [.75,.63,.51]:b('Paint_drip',(1.99,3.905,z),(.10,.015,.17),'purple')
 # Fruit bowl on the low red pedestal, paint tin and fallen brush.
 b('Fruit_pedestal',(-2.05,2.7,.28),(.79,.70,.56),'red')
 geo.sphere('Fruit_basket',(-2.05,2.7,.64),(.34,.24,.10),'brown')
 for j in range(3):
  z=.60+j*.035
  curved_line(geo,'Basket_woven_rim',[(-2.05+.34*math.cos(i*math.tau/32),2.7+.24*math.sin(i*math.tau/32),z) for i in range(33)],.018,'yellow' if j%2 else 'lightred')
 for i in range(16):
  a=i*math.tau/16
  geo.beam('Basket_weave',(-2.05+.30*math.cos(a),2.7+.21*math.sin(a),.58),(-2.05+.34*math.cos(a),2.7+.24*math.sin(a),.70),.014,'yellow')
 for dx,dy,col in [(-.17,0,'red'),(.04,-.10,'purple'),(.17,.04,'green'),(-.02,.12,'yellow')]:geo.sphere('Wax_fruit',(-2.05+dx,2.7+dy,.77),(.12,.11,.12),col)
 geo.cyl('Paint_tin',(-1.19,2.58,.17),.13,.33,'cyan',16);geo.cyl('Paint_tin_rim',(-1.19,2.58,.34),.14,.025,'white',24);geo.cyl('Open_tin_paint',(-1.19,2.58,.355),.115,.008,'aqua',24)
 geo.beam('Dropped_brush',(-1.84,2.22,.045),(-1.48,2.42,.045),.035,'brown');b('Brush_bristles',(-1.46,2.44,.045),(.15,.1,.05),'aqua')
 # Original loose paper above the tub and large drawing on the right wall.
 source_patch(geo,ROOT/'source/room 014.png',(192,20,226,57),(1.08,5.369,2.46),(.70,.76),'Studio_loose_sketch',only={'white','gray','black'})
 before=set(bpy.data.objects)
 source_patch(geo,ROOT/'source/room 014.png',(290,12,312,70),(0,0,2.05),(.48,1.25),'Studio_side_drawing',only={'white','gray','black'})
 bpy.context.view_layer.update()
 transform=Matrix.Translation((3.019,3.7,0))@Matrix.Rotation(-math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=transform@o.matrix_world
 for x in [-1.25,1.6]:
  geo.cyl('Lamp_wire',(x,4.0,2.98),.018,.27,'black')
  geo.mesh('Studio_lamp_shade',[(x+r*math.cos(i*math.tau/24),4+r*math.sin(i*math.tau/24),z) for r,z in [(.24,2.77),(.055,2.97)] for i in range(24)],[(i,(i+1)%24,(i+1)%24+24,i+24) for i in range(24)],'gray')
  geo.cyl('Studio_lamp_rim',(x,4,2.77),.255,.025,'darkgray',24)
  o=geo.sphere('Studio_bulb',(x,4,2.745),(.08,.08,.04),'white');o['bake_unlit']=True;o['bake_no_shadow']=True
 # Broad magenta paint run below the leaking tub, in addition to small splashes.
 geo.mesh('Tub_paint_pool',[(1.55,4.23,.008),(1.64,3.99,.008),(2.05,3.73,.008),(2.56,3.82,.008),(2.75,4.13,.008),(2.31,4.34,.008)],[(0,1,2,3,4,5)],'purple')
 rng=random.Random(14)
 for i in range(85):
  x=rng.uniform(-2.7,2.5);y=4.25+.18*math.sin(x*2)+rng.uniform(-.10,.1)
  b('Floor_paint_speck',(x,y,.013),(rng.uniform(.025,.07),.04,.009),'purple')
 bpy.data.objects['Wall_front'].name='Front_inferred_studio'
