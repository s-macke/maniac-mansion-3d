"""031 outer laboratory: green monitor console, cooling stack and articulated handling arm."""
from pathlib import Path
import math
from blender_shared.lab_furniture import metal_wall,opposite_metal_wall,pipe,disc,gauge,cylinder
from blender_shared.furnishings import source_patch
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 entry=next(p for p in c['ports'] if p['id']=='dungeon_door')
 ex=entry['position'][0];half=entry['width']/2
 metal_wall(g,c['geometry']['halfWidth'],5.1,openings=[(ex-half,ex+half,entry['height'])])
 # Back-wall equipment leaves the back-left entrance and right exit clear.
 for z in [.48,1.15,2.80]:pipe(g,'Chamber_pipe',[(-2.25,4.76,z),(4.86,4.76,z)],.042,'cyan')
 for x in [-2.19,1.77,4.53]:pipe(g,'Chamber_riser',[(x,4.76,.08),(x,4.76,3.11)],.070,'cyan')
 b('Console_foot',(-.19,4.14,.18),(3.08,1.18,.36),'black');b('Foot_grille',(-.19,3.527,.19),(2.75,.029,.24),'gray')
 for i in range(36):g.beam('Console_diagonal_vent',(-1.48+i*.074,3.506,.11),(-1.40+i*.074,3.506,.27),.022,'black')
 b('Console_pedestal',(-.19,4.32,.79),(2.51,.79,.94),'cyan');b('Console_lower_face',(-.19,3.898,.79),(2.35,.044,.77),'black')
 for index,x in enumerate([-.92,-.29]):
  disc(g,'Gauge_ink_rim',x,3.851,.87,.185,'black')
  disc(g,'Gauge_pink_rim',x,3.831,.87,.160,'pink')
  disc(g,'Gauge_face',x,3.810,.87,.135,'aqua' if index==0 else 'black')
  if index==0:
   pts=[(x,3.787,.87)]+[(x+.134*math.cos(i*math.pi/20),3.787,.87+.134*math.sin(i*math.pi/20)) for i in range(21)]
   g.mesh('Gauge_pink_upper_half',pts,[tuple(range(len(pts)))],'pink')
  for i in range(8):
   a=i*math.tau/8
   g.beam('Gauge_tick',(x+.113*math.cos(a),3.778,.87+.113*math.sin(a)),(x+.137*math.cos(a),3.778,.87+.137*math.sin(a)),.010,'white')
  g.beam('Gauge_needle',(x,3.764,.87),(x,3.764,.982),.014,'black' if index==0 else 'white')
  disc(g,'Gauge_hub',x,3.752,.87,.030,'white',.014)
 for x in [-1.27,.08]:
  for z in [.56,1.10]:b('Gauge_panel_screw',(x,3.86,z),(.037,.02,.037),'cyan')
 pipe(g,'Console_left_cable',[(-1.43,4.08,.60),(-1.80,4.13,.60),(-2.05,4.39,.42),(-2.23,4.76,.42)],.045,'gray',False)
 b('Console_button_panel',(.54,3.846,.84),(.64,.035,.65),'cyan')
 for z,col in [(.61,'black'),(.82,'purple'),(1.04,'red')]:disc(g,'Console_button',.38,3.814,z,.065,col);b('Button_label',(.63,3.807,z),(.23,.018,.022),'black')
 # Original green screen is inset into a substantial three-dimensional housing.
 b('Monitor_housing',(-.19,4.28,1.90),(3.02,.72,1.47),'cyan');b('Monitor_black_border',(-.19,3.899,1.90),(2.79,.03,1.28),'black')
 source_patch(g,ROOT/'source/room 031.png',(156,25,235,62),(-.19,3.875,1.90),(2.57,1.09),'Original_lab_monitor')
 for x in [-1.74,1.36]:
  b('Monitor_side_grille',(x,3.99,1.89),(.21,.22,.67),'cyan')
  for z in [1.63+i*.08 for i in range(7)]:b('Monitor_side_vent',(x,3.868,z),(.10,.02,.035),'black')
 for i in range(8):b('Cooling_fin',(-.19,4.36,2.67+i*.05),(1.18-i*.075,.73,.022),'aqua' if i%2 else 'blue')
 pipe(g,'Console_black_duct',[(.82,4.60,2.56),(1.31,4.60,2.94),(1.31,4.60,3.11)],.14,'black')
 # Tall guide housing and upper elbow linkage, as in the source machinery.
 b('Arm_guide_back',(3.74,4.65,1.93),(.43,.18,2.28),'black')
 b('Arm_guide_housing',(3.74,4.49,1.93),(.32,.24,2.15),'gray')
 b('Arm_guide_slot',(3.68,4.356,1.91),(.08,.025,1.78),'darkgray')
 b('Arm_guide_highlight',(3.84,4.354,1.95),(.035,.025,1.94),'white')
 pts=[(3.71,4.23,2.93),(2.99,4.23,2.40),(3.47,4.23,1.98)]
 for a,z in zip(pts,pts[1:]):g.beam('Manipulator_link',a,z,.16,'gray')
 for x,y,z in pts:
  disc(g,'Arm_joint',x,y-.08,z,.17,'darkgray',.10);disc(g,'Joint_face',x,y-.14,z,.105,'gray')
  disc(g,'Joint_axle',x,y-.163,z,.038,'black')
 b('Arm_lower_reader',(3.31,4.22,1.06),(.70,.30,.22),'darkgray')
 b('Arm_reader_face',(3.31,4.055,1.06),(.56,.025,.13),'black')
 b('Arm_reader_glow',(3.27,4.037,1.065),(.41,.013,.064),'aqua')
 for dx in [-.13,.04]:b('Reader_dark_tick',(3.27+dx,4.026,1.07),(.035,.012,.024),'black')
 pipe(g,'Arm_side_handle',[(3.89,4.44,1.99),(4.02,4.44,1.99),(4.02,4.44,1.67)],.045,'darkgray',False)
 pipe(g,'Arm_lower_cable',[(3.71,4.44,.90),(3.88,4.48,.80),(3.94,4.67,.97)],.053,'black',False)
 # Small wall keypad from the original laboratory artwork.
 b('Wall_keypad',(-4.81,4.76,1.53),(.40,.23,.78),'blue');b('Keypad_display',(-4.81,4.626,1.76),(.31,.022,.17),'green')
 for i in range(3):
  for j in range(3):b('Keypad_button',(-4.93+i*.12,4.624,1.31+j*.11),(.07,.025,.056),'lightred' if i==0 else 'aqua')
 opposite_metal_wall(g,c['geometry']['halfWidth'],c['geometry']['depth'],c['geometry']['height'])
 finish(c)
