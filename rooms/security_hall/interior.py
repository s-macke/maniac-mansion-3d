"""Background 013: patterned corridor, framed portraits, rug and sculpture."""
from pathlib import Path
import bpy,math
from blender_shared.furnishings import source_patch,panel,curved_line
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Wallpaper stays around existing doors and clear of the stairwell.
 ports=[p for p in c['ports'] if p['id'] in ['medical_door','arcade_door']]
 for ix in range(65):
  x=-6.27+ix*.174
  if x>4.93:continue
  for iz in range(15):
   z=.35+iz*.178
   if any(abs(x-p['position'][0])<p['width']/2+.16 and z<p['height']+.13 for p in ports):continue
   b('Wallpaper_square',(x,5.351,z),(.063,.009,.065),'blue')
   b('Wallpaper_dot',(x,5.339,z),(.023,.008,.025),'gray')
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
  geo.cyl('Candlestick_wax',(x,4.95,2.16),.045,.27,'aqua')
 # Static reclining aqua statue on an oval pedestal, using solid simple forms.
 sx,sy=-5.45,3.78
 geo.sphere('Statue_plinth',(sx,sy,.18),(.68,.47,.18),'cyan')
 b('Statue_plaque',(sx,sy-.45,.19),(.38,.024,.11),'red')
 geo.sphere('Statue_hip',(sx+.03,sy,.47),(.20,.19,.20),'aqua')
 geo.beam('Statue_torso',(sx-.02,sy,.47),(sx-.26,sy,1.10),.22,'aqua')
 geo.sphere('Statue_head',(sx-.28,sy,1.33),(.16,.14,.20),'aqua')
 geo.sphere('Statue_hair',(sx-.3,sy+.02,1.43),(.17,.15,.13),'cyan')
 for dy in [-.08,.10]:
  curved_line(geo,'Statue_leg',[(sx+.02,sy+dy,.51),(sx+.36,sy+dy,.40),(sx+.59,sy+dy,.30)],.115,'aqua')
 curved_line(geo,'Statue_arm',[(sx-.23,sy-.12,1.06),(sx+.03,sy-.17,.90),(sx-.26,sy-.16,1.20)],.075,'aqua')
 curved_line(geo,'Statue_supporting_arm',[(sx-.34,sy+.12,1.03),(sx-.47,sy+.11,.65),(sx-.56,sy+.08,.40)],.075,'aqua')
 # White tread faces and carved red stringer accents on the existing navigable stairs.
 st=c['geometry']['stairs']
 for i in range(st['segments']):
  y=st['y0']+(st['y1']-st['y0'])*i/st['segments'];z=st['rise']*(i+1)/st['segments']
  b('White_stair_nosing',((st['x0']+st['x1'])/2,y+.018,z+.007),(st['x1']-st['x0'],.036,.013),'white')
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_security'
