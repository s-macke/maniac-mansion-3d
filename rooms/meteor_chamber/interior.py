"""031: green monitor console, cooling stack and articulated handling arm."""
from pathlib import Path
from blender_shared.lab_furniture import metal_wall,pipe,disc,gauge
from blender_shared.furnishings import source_patch
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box;metal_wall(g,5.6,5.1)
 # Keep the existing garage ladder and its approach where the original exit was omitted.
 for z in [.48,1.15,2.80]:pipe(g,'Chamber_pipe',[(-2.25,4.76,z),(4.86,4.76,z)],.042,'cyan')
 for x in [-2.19,1.77,4.53]:pipe(g,'Chamber_riser',[(x,4.76,.08),(x,4.76,3.11)],.070,'cyan')
 b('Console_foot',(-.19,4.14,.18),(3.08,1.18,.36),'black');b('Foot_grille',(-.19,3.527,.19),(2.75,.029,.24),'gray')
 for i in range(36):b('Console_vent',(-1.48+i*.074,3.506,.19),(.028,.014,.18),'black')
 b('Console_pedestal',(-.19,4.32,.79),(2.51,.79,.94),'cyan');b('Console_lower_face',(-.19,3.898,.79),(2.35,.044,.77),'black')
 for x in [-.92,-.29]:
  disc(g,'Pink_gauge',x,3.851,.87,.18,'pink');disc(g,'Gauge_inset',x,3.830,.87,.12,'aqua');b('Gauge_needle',(x,3.811,.89),(.022,.016,.16),'black')
 b('Console_button_panel',(.54,3.846,.84),(.64,.035,.65),'cyan')
 for z,col in [(.61,'black'),(.82,'purple'),(1.04,'red')]:disc(g,'Console_button',.38,3.814,z,.065,col);b('Button_label',(.63,3.807,z),(.23,.018,.022),'black')
 # Original green screen is inset into a substantial three-dimensional housing.
 b('Monitor_housing',(-.19,4.28,1.90),(3.02,.72,1.47),'cyan');b('Monitor_black_border',(-.19,3.899,1.90),(2.79,.03,1.28),'black')
 source_patch(g,ROOT/'source/room 031.png',(156,25,235,62),(-.19,3.875,1.90),(2.57,1.09),'Original_meteor_monitor')
 for x in [-1.74,1.36]:
  b('Monitor_side_grille',(x,3.99,1.89),(.21,.22,.67),'cyan')
  for z in [1.63+i*.08 for i in range(7)]:b('Monitor_side_vent',(x,3.868,z),(.10,.02,.035),'black')
 for i in range(8):b('Cooling_fin',(-.19,4.36,2.67+i*.05),(1.18-i*.075,.73,.022),'aqua' if i%2 else 'blue')
 pipe(g,'Console_black_duct',[(.82,4.60,2.56),(1.31,4.60,2.94),(1.31,4.60,3.11)],.14,'black')
 # Metal handling arm, fixed in the reference pose.
 pts=[(3.71,4.35,2.93),(2.99,4.35,2.29),(3.36,4.35,1.76),(3.24,4.35,1.13)]
 for a,z in zip(pts,pts[1:]):g.beam('Manipulator_link',a,z,.16,'gray')
 for x,y,z in pts:
  disc(g,'Arm_joint',x,y-.105,z,.17,'darkgray',.10);disc(g,'Joint_face',x,y-.165,z,.105,'gray')
 b('Arm_wall_rail',(3.74,4.72,2.02),(.14,.10,2.05),'black')
 for s in [-1,1]:
  g.beam('Manipulator_claw',(3.24,4.35,1.13),(3.24+s*.29,4.35,.94),.062,'gray');g.beam('Claw_tip',(3.24+s*.29,4.35,.94),(3.24+s*.22,4.35,.80),.044,'gray')
 # Small isolated keypad at the left does not reconstruct the omitted exit door.
 b('Wall_keypad',(-4.73,4.76,1.53),(.56,.23,.78),'blue');b('Keypad_display',(-4.73,4.626,1.76),(.43,.022,.17),'green')
 for i in range(3):
  for j in range(3):b('Keypad_button',(-4.9+i*.16,4.624,1.31+j*.11),(.09,.025,.056),'lightred' if i==0 else 'aqua')
 finish(c)
