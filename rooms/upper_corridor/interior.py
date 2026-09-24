"""038: diamond wallpaper, wood panels, hanging lamps and bare decorative branches."""
import math
import bpy
from pathlib import Path
from mathutils import Matrix
from blender_shared.furnishings import source_patch
from blender_shared.furnishings import curved_line
from blender_shared.bedroom_furniture import finish

def furnish(g,c):
 b=g.box
 # Solid timber corner piers and chamfered upper corners, not curtains.
 for side in [-1,1]:
  x=side*8.13
  b('Corner_timber_pier',(x,4.49,1.56),(.30,.24,3.12),'brown')
  b('Corner_red_rebate',(x-side*.17,4.35,1.56),(.055,.035,3.12),'red')
  b('Corner_gold_edge',(x-side*.21,4.34,1.56),(.025,.035,3.12),'yellow')
  g.mesh('Corner_chamfer',[(x-side*.18,4.36,2.58),(x-side*.18,4.36,3.12),(x-side*.74,4.36,3.12)],[(0,1,2)],'brown')
  g.beam('Chamfer_red_edge',(x-side*.18,4.345,2.58),(x-side*.74,4.345,3.12),.07,'red')
  g.beam('Chamfer_gold_edge',(x-side*.23,4.325,2.58),(x-side*.79,4.325,3.12),.022,'yellow')
  # Wainscot rail returns around both side walls, stopping at the door.
  for ya,yb in [(.18,1.68),(3.12,4.62)]:
   for zz,col,hh in [(.89,'red',.07),(.95,'yellow',.025)]:
    b('Side_rail_return',(side*8.30,(ya+yb)/2,zz),(.04,yb-ya,hh),col)
 # The left entrance has its own red surround; its moving leaf remains owned
 # by the stair hall, so no duplicate door or portal is introduced here.
 for yy in [1.68,3.12]:
  b('Left_door_black_rebate',(-8.305,yy,1.43),(.035,.16,2.86),'black')
  b('Left_door_red_jamb',(-8.27,yy,1.43),(.055,.10,2.86),'lightred')
  b('Left_door_dark_edge',(-8.235,yy+.045,1.43),(.025,.024,2.86),'red')
 b('Left_door_red_lintel',(-8.27,2.4,2.86),(.065,1.54,.10),'lightred')
 before=set(bpy.data.objects)
 source_patch(g,Path(__file__).resolve().parents[2]/'source/room 038.png',
              (32,3,65,34),(0,0,0),(.72,.60),'Door_devil_ornament',
              only={'black','red','lightred','yellow'})
 for obj in set(bpy.data.objects)-before:
  # The screenshot includes the dark doorway and its red lintel beneath the
  # face. Trim those background pixels rather than attaching a rectangle.
  vertices=[];faces=[]
  for face in obj.data.polygons:
   pts=[obj.data.vertices[i].co.copy() for i in face.vertices]
   row=3+(.30-sum(v.z for v in pts)/4)/.60*31
   lo,hi=(32,65) if row<20 else ((41,58) if row<27 else ((44,56) if row<31 else (47,54)))
   xmin=(lo-32)/33*.72-.36;xmax=(hi-32)/33*.72-.36
   if max(v.x for v in pts)<=xmin or min(v.x for v in pts)>=xmax:continue
   for v in pts:v.x=max(xmin,min(xmax,v.x))
   n=len(vertices);vertices.extend(pts);faces.append(tuple(range(n,n+4)))
  material=obj.data.materials[0]
  mesh=bpy.data.meshes.new(obj.name+'_silhouette');mesh.from_pydata(vertices,[],faces);mesh.materials.append(material);obj.data=mesh
  obj.matrix_world=Matrix.Translation((-8.225,2.4,2.81)) @ Matrix.Rotation(math.pi/2,4,'Z') @ obj.matrix_world
 ports=[p for p in c['ports'] if p['outward']==[0,1]]
 # Thin diamond lattice is one mesh; each strip is clipped away from door frames.
 vs=[];fs=[]
 for i in range(98):
  x=-8.1+i*.166
  for j in range(13):
   z=1.05+j*.162
   if any(abs(x-p['position'][0])<p['width']/2+.21 and z<p['height']+.15 for p in ports):continue
   for s in [-1,1]:
    n=len(vs);vs.extend([(x-.075,4.618,z-s*.08),(x-.067,4.618,z-s*.08),(x+.075,4.618,z+s*.08),(x+.067,4.618,z+s*.08)]);fs.append((n,n+1,n+2,n+3))
 g.mesh('Corridor_diamond_lattice',vs,fs,'lightblue')
 # Preserve the original cyan/blue dithered pools of light, which cannot be
 # recovered by multiplying a pure-blue wall material by a white light.
 # These are flush wall color runs, not floating light cones or runtime effects.
 for x,u in [(-3.6,168),(0,288),(3.6,408)]:
  # Only sample above the branches. Continue the wallpaper's eight-pixel
  # repeat below that, so no photographed branch silhouettes stick to the wall.
  for dest_y,src_y,rows in [(18,18,22),(40,24,16),(56,24,13)]:
   source_patch(g,Path(__file__).resolve().parents[2]/'source/room 038.png',
                (u,src_y,u+64,src_y+rows),
                (x,4.617,3.12-(dest_y+rows/2)*.03075),(1.92,rows*.03075),
                'Original_illuminated_wallpaper',only={'blue','lightblue','aqua','cyan'})
 cuts=[(-8.25,-6.18),(-4.62,-2.58),(-1.02,1.02),(2.58,4.62),(6.18,8.25)]
 for a,bx in cuts:
  b('Corridor_wood_panel',((a+bx)/2,4.57,.48),(bx-a,.10,.88),'brown')
  for z,col in [(.08,'red'),(.83,'red'),(.94,'yellow')]:b('Wainscot_rail',((a+bx)/2,4.50,z),(bx-a,.06,.04),col)
  for x in [a+.07,bx-.07]:b('Panel_stile',(x,4.49,.47),(.038,.045,.77),'yellow')
 for x in [-3.6,0,3.6]:
  # Bare sculptural branches occupy the front border, leaving the whole doorway aisle free.
  # The source has square red planters with pale rectangular rims.
  b('Branch_pot',(x,1.10,.18),(.34,.34,.34),'lightred')
  b('Branch_pot_dark_side',(x+.165,1.10,.18),(.016,.34,.34),'red')
  b('Branch_pot_lip',(x,1.10,.36),(.39,.39,.06),'yellow')
  b('Branch_pot_soil',(x,1.10,.397),(.30,.30,.012),'brown')
  trunk=[(x,1.10,.39),(x+.12,1.10,.82),(x-.05,1.10,1.24),(x+.18,1.10,1.70),(x+.04,1.10,2.14)]
  curved_line(g,'Bare_branch',trunk,.037,'black')
  for s,z in [(-1,.94),(1,1.33),(-1,1.60)]:curved_line(g,'Bare_twig',[(x,1.10,z),(x+s*.28,1.10,z+.32),(x+s*.32,1.10,z+.60)],.027,'black')
  g.cyl('Lamp_chain',(x,4.15,3.015),.019,.21,'black')
  for dx in [-.23,.23]:
   curved_line(g,'Lamp_curved_arm',[(x,4.15,2.94),(x+dx*.6,4.15,2.96),(x+dx,4.15,2.88)],.023,'black')
   # Two black bell shades with bright undersides, as in 038.
   verts=[]
   for zz,rr in [(2.91,.045),(2.76,.15)]:
    verts.extend([(x+dx+rr*math.cos(i*math.tau/12),4.15+rr*math.sin(i*math.tau/12),zz) for i in range(12)])
   g.mesh('Black_bell_shade',verts,[(i,(i+1)%12,(i+1)%12+12,i+12) for i in range(12)],'black')
   glow=g.cyl('Lamp_white_underside',(x+dx,4.15,2.755),.132,.012,'white')
   glow['bake_unlit']=True;glow['bake_no_shadow']=True
 for i,(w,d,col) in enumerate([(10.9,1.87,'black'),(10.68,1.69,'lightblue'),(10.35,1.43,'blue')]):b('Upper_corridor_rug',(0,1.21,.002+i*.002),(w,d,.001),col)
 finish(c)
