"""004: irregular stone wall, barred openings, chained skeletal remains and chandelier."""
from pathlib import Path
import random,math,bpy
from mathutils import Matrix,Vector
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.lab_furniture import disc
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box;rng=random.Random(4)
 # Dense irregular masonry on the original rear wall and inferred opposite wall.
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Skirting'):bpy.data.objects.remove(obj,do_unlink=True)
 for front in [False,True]:
  wall_y=.19 if front else 4.916
  toward=1 if front else -1
  for row in range(12):
   for col in range(28):
    x=-6.18+col*.46+(row%2)*.23+rng.uniform(-.025,.025);z=.14+row*.255+rng.uniform(-.012,.012)
    if x>6.18 or (not front and any(abs(x-p['position'][0])<p['width']/2+.16 and z<p['height']+.04 for p in c['ports'])):continue
    w=rng.uniform(.43,.50);h=rng.uniform(.25,.29);pts=[(-w*.47,-h*.33),(-w*.5,h*.13),(-w*.22,h*.50),(w*.32,h*.46),(w*.52,-h*.06),(w*.27,-h*.48)]
    g.mesh('Opposite_stone_edge' if front else 'Stone_red_edge',[(x+u,wall_y,z+v) for u,v in pts],[tuple(range(6))],'red')
    g.mesh('Opposite_stone_face' if front else 'Stone_brown_face',[(x+u*.81,wall_y+toward*.012,z+v*.81) for u,v in pts],[tuple(range(6))],'brown')
 # Source blue metal surrounds, rather than bare gray door apertures.
 for port in c['ports']:
  x=port['position'][0];w=port['width'];h=port['height']
  for dx in [-w/2-.055,w/2+.055]:
   b('Dungeon_door_jamb',(x+dx,4.86,h/2),(.11,.14,h),'blue')
   b('Dungeon_jamb_edge',(x+dx-.025,4.783,h/2),(.023,.012,h),'lightblue')
  b('Dungeon_door_lintel',(x,4.86,h+.045),(w+.22,.14,.09),'blue')
  b('Dungeon_lintel_edge',(x,4.783,h+.063),(w+.20,.014,.018),'lightblue')
 # Right blue plate: pale corner facet and small visible bolt heads.
 g.mesh('Right_wall_light_facet',[(6.211,.20,3.10),(6.211,4.89,3.10),(6.211,4.89,1.45)],[(0,1,2)],'lightblue')
 g.beam('Right_wall_diagonal_seam',(6.204,.20,3.10),(6.204,4.89,1.45),.018,'blue')
 for yy,zz in [(y,.22) for y in [.35,1.15,1.95,2.75,3.55,4.55]]+[(y,2.97) for y in [.45,1.65,2.85,4.35]]:
  b('Right_wall_rivet',(6.205,yy,zz),(.025,.048,.045),'blue')
  b('Right_rivet_glint',(6.188,yy-.008,zz+.009),(.012,.018,.015),'aqua')
 # Two arched barred windows are opaque decorative recesses, not extra room connections.
 for x in [-1.66,1.77]:
  for y,w,h,col in [(4.86,1.05,1.18,'blue'),(4.825,.95,1.10,'gray'),(4.793,.83,1.02,'black')]:
   bottom=1.55;spring=bottom+h-w/2;pts=[(x-w/2,y,bottom),(x+w/2,y,bottom),(x+w/2,y,spring)]+[(x+w/2*math.cos(i*math.pi/16),y,spring+w/2*math.sin(i*math.pi/16)) for i in range(1,17)]
   g.mesh('Barred_arch',pts,[tuple(range(len(pts)))],col)
  for dx in [-.25,0,.25]:g.beam('Window_bar',(x+dx,4.756,1.57),(x+dx,4.756,2.51),.036,'lightblue')
 def link(name,center,rx,rz,side=False,color='gray'):
  # Open elliptical metal links, alternating their planes through the chain.
  cx,cy,cz=center
  pts=[(cx+(0 if side else rx*math.cos(i*math.tau/16)),cy+(rx*math.cos(i*math.tau/16) if side else 0),cz+rz*math.sin(i*math.tau/16)) for i in range(17)]
  curved_line(g,name,pts,.016,color)
 # Gothic blue chandelier: open linked suspension, shaped arms and crown cups.
 for i in range(5):link('Chandelier_chain',(0,3.78,3.08-i*.09),.034,.057,i%2==1,'blue')
 g.cyl('Chandelier_hub',(0,3.78,2.53),.095,.16,'blue',12)
 for dx,dy in [(-.39,0),(.39,0),(0,.24)]:
  curved_line(g,'Chandelier_curved_arm',[(0,3.78,2.55),(dx*.5,3.78+dy*.5,2.42),(dx,3.78+dy,2.43),(dx,3.78+dy,2.62)],.045,'blue')
  for z,r in [(2.45,.105),(2.63,.085)]:g.cyl('Chandelier_cup',(dx,3.78+dy,z),r,.055,'blue',12)
  for side in [-1,1]:
   curved_line(g,'Crown_prong',[(dx+side*.055,3.78+dy,2.62),(dx+side*.11,3.78+dy,2.80),(dx+side*.085,3.78+dy,2.91)],.024,'lightblue')
  g.cyl('Blue_candle',(dx,3.78+dy,2.76),.028,.20,'lightblue',12)
  flame=g.sphere('Blue_candle_tip',(dx,3.78+dy,2.90),(.024,.027,.057),'aqua');flame['bake_unlit']=True
 # Skeleton slumps across the floor; both wrists share the hanging wall chain.
 sx,sy=-2.63,4.02
 g.sphere('Skull',(sx,sy,.72),(.16,.13,.19),'white')
 for dx in [-.062,.062]:g.sphere('Skull_socket',(sx+dx,sy-.115,.755),(.046,.022,.047),'black')
 b('Skull_jaw',(sx,sy-.02,.55),(.17,.15,.058),'white')
 hip=Vector((sx-.54,sy-.40,.16));neck=Vector((sx,sy,.49));axis=(neck-hip).normalized();across=Vector((0,1,0));out=axis.cross(across).normalized()
 for i in range(10):
  pos=hip.lerp(neck,i/9);g.sphere('Spine_bone',pos,(.035,.035,.029),'white')
 for i in range(5):
  center=hip.lerp(neck,.42+i*.105);width=.12+i*.01
  curved_line(g,'Rib',[center+across*(math.cos(j*math.tau/18)*width)+out*(math.sin(j*math.tau/18)*.085) for j in range(19)],.022,'white')
 for side in [-1,1]:
  curved_line(g,'Leg_bones',[(hip.x,hip.y+side*.08,.17),(sx-1.02,sy-.51+side*.12,.24),(sx-1.52,sy-.72+side*.14,.07)],.038,'white')
  for toe in range(4):g.beam('Foot_toe',(sx-1.52,sy-.72+side*.14,.07),(sx-1.62,sy-.74+side*.14+toe*.018,.055),.018,'white')
  wrist=(sx+side*.045,4.47,1.43)
  curved_line(g,'Raised_arm',[(sx+side*.14,sy,.50),(sx+side*.32,4.18,.97),wrist],.034,'white')
  link('Wrist_cuff',wrist,.052,.046,False,'gray')
  for finger in range(3):g.beam('Hand_finger',(wrist[0],wrist[1],1.43),(wrist[0]+(finger-1)*.022,wrist[1],1.49),.014,'white')
 b('Chain_wall_plate',(sx,4.89,2.40),(.34,.05,.22),'blue')
 b('Chain_plate_face',(sx,4.858,2.40),(.25,.015,.14),'lightblue')
 for xx in [sx-.13,sx+.13]:b('Anchor_bolt',(xx,4.847,2.40),(.027,.012,.034),'gray')
 link('Wall_anchor_ring',(sx,4.82,2.39),.052,.06,False)
 for i in range(12):
  t=i/11;link('Wrist_chain_link',(sx,4.80-.33*t,2.32-.83*t),.035,.054,i%2==1)
 # Original scrawled lettering on the left steel wall.
 before=set(bpy.data.objects)
 source_patch(g,ROOT/'source/room 004.png',(0,22,84,90),(0,0,1.77),(1.57,1.28),'Dungeon_graffiti',only={'black'})
 bpy.context.view_layer.update();m=Matrix.Translation((-6.192,2.55,0))@Matrix.Rotation(math.pi/2,4,'Z')
 for o in set(bpy.data.objects)-before:o.matrix_world=m@o.matrix_world
 g.sphere('Dungeon_floor_patch',(0,2.8,.002),(5.23,1.74,.002),'brown')
 finish(c)
