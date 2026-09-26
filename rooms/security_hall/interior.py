"""Background 013: patterned corridor, framed portraits, rug and sculpture."""
from pathlib import Path
import bpy,math
from mathutils import Matrix
from blender_shared.furnishings import source_patch,panel,curved_line
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Wallpaper stays around existing doors and clear of the stairwell.
 ports=[p for p in c['ports'] if p['id'] in ['medical_door','arcade_door']]
 # Painted wallpaper is batched into two flush meshes, not thousands of boxes.
 patterns={'blue':([],[]),'gray':([],[])}
 for ix in range(124):
  x=-6.27+ix*.091
  if x>4.93:continue
  for iz in range(30):
   z=.35+iz*.089
   if any(abs(x-p['position'][0])<p['width']/2+.16 and z<p['height']+.13 for p in ports):continue
   for color,w,h,y in [('blue',.043,.045,5.368),('gray',.012,.013,5.367)]:
    vs,fs=patterns[color];n=len(vs)
    vs.extend([(x-w/2,y,z-h/2),(x+w/2,y,z-h/2),(x+w/2,y,z+h/2),(x-w/2,y,z+h/2)]);fs.append((n,n+1,n+2,n+3))
 for color,(vs,fs) in patterns.items():geo.mesh('Wallpaper_'+color,vs,fs,color)
 for xa,xb in [(-6.35,-3.8),(-2.2,2.4),(4.0,5.1)]:
  for z,col in [(.21,'red'),(.30,'yellow'),(3.03,'red')]:b('Corridor_rail',((xa+xb)/2,5.29,z),(xb-xa,.09,.07),col)
 for crop,x,z,w,h in [((313,29,362,75),0,2.05,1.30,1.23),((62,34,92,55),-4.93,2.13,.66,.46),((206,32,231,57),-1.73,2.25,.48,.48),((402,42,427,70),1.61,2.08,.50,.56)]:
  panel(geo,'Portrait_frame',x,5.25,z,w+.16,h+.16)
  source_patch(geo,ROOT/'source/room 013.png',crop,(x,5.18,z),(w,h),'Original_corridor_portrait')
 # Small wall keypad beside the medical door, as in background 013.
 b('Security_keypad_case',(-3.96,5.285,1.82),(.27,.12,.61),'black')
 b('Security_keypad_face',(-3.96,5.216,1.82),(.21,.019,.53),'gray')
 b('Security_keypad_display',(-3.96,5.2,2.00),(.15,.013,.10),'blue')
 for row in range(5):
  for col in range(3):b('Security_keypad_button',(-4.02+col*.06,5.188,1.68+row*.052),(.029,.014,.025),'aqua')
 # Inset rug has negligible height and never changes the walking surface.
 for layer,(w,d,col) in enumerate([(6.4,1.42,'black'),(6.25,1.3,'red'),(6.04,1.12,'pink')]):b('Corridor_rug',(0,2.1,.001+layer*.001),(w,d,.0005),col)
 for x in [-4.2,2.01]:
  geo.cyl('Candlestick_base',(x,4.95,.04),.16,.08,'brown');geo.cyl('Candlestick_stem',(x,4.95,1.03),.024,1.98,'yellow')
  geo.cyl('Candlestick_wax',(x,4.95,2.16),.045,.27,'white')
  geo.cyl('Candle_drip_tray',(x,4.95,2.025),.10,.028,'lightred',24)
  for zz,rr in [(.08,.18),(.13,.13)]:geo.cyl('Candlestick_foot_ring',(x,4.95,zz),rr,.03,'lightred',24)
  flame=geo.sphere('Candle_flame',(x,4.95,2.335),(.028,.028,.070),'yellow');flame['bake_unlit']=True;flame['bake_no_shadow']=True
  geo.cyl('Candle_wick',(x,4.95,2.305),.008,.04,'black')
 # Reclining sculpture with rounded anatomy, bent legs and a supporting arm.
 statue_before=set(bpy.data.objects)
 sx,sy=-5.45,3.78
 geo.sphere('Statue_plinth',(sx,sy,.18),(.68,.47,.18),'aqua')
 geo.sphere('Statue_plinth_inset',(sx,sy-.02,.18),(.62,.455,.145),'cyan')
 b('Statue_plaque',(sx,sy-.475,.19),(.38,.024,.11),'lightred')
 source_patch(geo,ROOT/'source/room 013.png',(34,114,62,120),(sx,sy-.489,.19),(.35,.078),'Statue_plaque_lettering')
 def limb(name,a,b,r,col='aqua'):
  from mathutils import Vector
  a,b=Vector(a),Vector(b)
  o=geo.sphere(name,(a+b)/2,(r,r,(b-a).length/2+r*.3),col);o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
 geo.sphere('Statue_hip',(sx+.03,sy,.48),(.23,.20,.18),'aqua')
 limb('Statue_torso',(sx+.02,sy,.51),(sx-.28,sy,.94),.16)
 limb('Statue_neck',(sx-.28,sy,.94),(sx-.30,sy,1.11),.065)
 geo.sphere('Statue_head',(sx-.30,sy,1.18),(.13,.12,.17),'aqua')
 geo.sphere('Statue_hair',(sx-.33,sy+.045,1.27),(.15,.125,.10),'cyan')
 geo.sphere('Statue_nose',(sx-.23,sy-.112,1.18),(.023,.035,.034),'aqua')
 for dx in [-.045,.035]:geo.sphere('Statue_eye',(sx-.30+dx,sy-.109,1.22),(.014,.007,.01),'cyan')
 for dy,knee in [(-.09,.37),(.09,.53)]:
  limb('Statue_thigh',(sx+.02,sy+dy,.49),(sx+.32,sy+dy,knee),.09)
  limb('Statue_calf',(sx+.32,sy+dy,knee),(sx+.56,sy+dy,.32),.065)
  geo.sphere('Statue_foot',(sx+.57,sy+dy,.29),(.085,.06,.04),'aqua')
 for start,end in [((sx-.25,sy-.14,.93),(sx-.06,sy-.20,.75)),((sx-.06,sy-.20,.75),(sx-.32,sy-.18,1.04)),((sx-.32,sy+.10,.94),(sx-.43,sy+.13,.67)),((sx-.43,sy+.13,.67),(sx-.51,sy+.08,.35))]:limb('Statue_arm',start,end,.046)
 geo.sphere('Statue_hand',(sx-.32,sy-.18,1.04),(.055,.03,.075),'aqua')
 # The original plinth/figure nearly reaches the candle height; the old figure was undersized.
 bpy.context.view_layer.update()
 transform=Matrix.Translation((-5.30,sy,0))@Matrix.Scale(1.4,4)@Matrix.Translation((-sx,-sy,0))
 for obj in set(bpy.data.objects)-statue_before:obj.matrix_world=transform@obj.matrix_world
 # White tread faces and carved red stringer accents on the existing navigable stairs.
 st=c['geometry']['stairs']
 for i in range(st['segments']):
  y=st['y0']+(st['y1']-st['y0'])*i/st['segments'];z=st['rise']*(i+1)/st['segments']
  b('White_stair_nosing',((st['x0']+st['x1'])/2,y+.018,z+.007),(st['x1']-st['x0'],.036,.013),'white')
 x=st['x0']-.10;y=st['y0']+.02
 b('Stair_newel_foot',(x,y,.08),(.16,.18,.16),'brown')
 b('Stair_newel_post',(x,y,.52),(.07,.075,.82),'red')
 geo.sphere('Stair_newel_aqua_finial',(x,y,.99),(.085,.085,.09),'aqua')
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_security'
