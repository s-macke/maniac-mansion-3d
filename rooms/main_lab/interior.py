"""030: three apparatus chairs, control banks, vending machine and radiation cabinet."""
from pathlib import Path
import math
from blender_shared.lab_furniture import metal_wall,pipe,panel,gauge,disc
from blender_shared.furnishings import source_patch
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box;metal_wall(g,8.2,5.5)
 for z,col in [(.39,'red'),(.72,'red'),(1.09,'purple'),(1.23,'purple'),(1.36,'purple'),(2.36,'cyan'),(2.55,'cyan')]:pipe(g,'Lab_service_pipe',[(-7.9,5.17,z),(7.9,5.17,z)],.028,col,False)
 for x in [-4.57,3.24,4.94]:pipe(g,'Tall_service_pipe',[(x,5.11,.09),(x,5.11,3.10)],.059,'cyan')
 # Large wall bank with meters, cooling grilles and indicator columns.
 b('Control_bank',(-.73,5.00,2.02),(5.48,.30,2.06),'cyan')
 for x in [-2.78,-1.94,-1.10]:
  b('Meter_column',(x,4.828,2.15),(.57,.035,1.67),'black')
  # Two meters per column, with their separate colored switches (source 030).
  for z in [1.82,2.49]:
   b('Meter_case',(x,4.800,z),(.39,.04,.28),'gray');b('Meter_glass',(x,4.772,z),(.29,.024,.18),'green');b('Meter_glint',(x-.065,4.753,z+.035),(.046,.015,.075),'white')
   b('Meter_switch_frame',(x,4.79,z-.23),(.16,.035,.11),'white')
   b('Meter_switch',(x,4.766,z-.23),(.11,.016,.065),'pink' if x<-1.5 else 'lightred')
 for x in [.24,.91,1.58]:
  b('Indicator_black_column',(x,4.82,2.22),(.38,.039,1.48),'black')
  for i in range(11):b('Indicator_lamp',(x,4.788,1.58+i*.127),(.26,.021,.069),['aqua','yellow','lightred','lime'][i%4])
 # Circular green scanner at the upper right of the bank.
 for r,y,col in [(.57,4.86,'cyan'),(.48,4.80,'blue'),(.42,4.76,'green'),(.34,4.72,'lime')]:disc(g,'Scanner',2.42,y,2.53,r,col)
 for dx in [-.24,-.12,0,.12,.24]:b('Scanner_grid',(2.42+dx,4.699,2.53),(.016,.015,.55),'green')
 for dz in [-.22,-.11,0,.11,.22]:b('Scanner_grid',(2.42,4.691,2.53+dz),(.54,.014,.015),'green')
 # Three solid apparatus chairs. The central seat is taller, as in the reference.
 for x,h in [(-2.16,1.62),(-.18,2.11),(1.80,1.62)]:
  b('Chair_base',(x,4.09,.13),(1.51,1.27,.26),'red');b('Chair_body',(x,4.30,h/2+.15),(1.18,.73,h),'brown')
  b('Red_chair_back',(x,3.914,h*.80),(1.16,.048,h*.59),'red')
  b('Chair_seat',(x,3.73,.60),(1.21,.76,.14),'brown')
  for dx in [-.68,.68]:
   pipe(g,'Chair_arm_frame',[(x+dx,3.48,.13),(x+dx,3.48,.95),(x+dx,4.45,.95)],.061,'gray')
   b('Chair_armrest',(x+dx,3.83,1.01),(.17,.63,.10),'gray')
  for z in [.29,.74]:
   b('Chair_restraint',(x,3.876,z),(.97,.055,.065),'black');b('Restraint_buckle',(x+.22,3.838,z),(.16,.025,.10),'gray')
  g.sphere('Blue_chair_helmet',(x,4.20,h+.32),(.45,.34,.30),'blue');g.cyl('Helmet_collar',(x,4.20,h+.17),.45,.06,'lightblue',28)
  pipe(g,'Helmet_feed',[(x,4.20,h+.60),(x,4.66,3.08)],.043,'red')
  gauge(g,x,3.865,h+.33,.12)
 # Original vending-machine artwork on a solid case.
 x,y=-5.83,4.59
 b('Vending_case',(x,y,1.26),(1.42,1.04,2.52),'cyan');b('Vending_front',(x,4.045,1.26),(1.22,.04,2.36),'lightblue')
 source_patch(g,ROOT/'source/room 030.png',(102,27,158,71),(x,4.012,1.82),(1.16,.97),'Original_Pepsi_logo')
 b('Vending_delivery',(x,4.007,.27),(.57,.045,.24),'gray');b('Vending_slot',(x,3.979,.27),(.44,.02,.13),'black')
 for dx in [.31,.46]:b('Vending_coin_button',(x+dx,4.008,.92),(.09,.025,.065),'white')
 # Radiation-marked compartment is equipment, not a door portal.
 x,y=5.85,4.59
 b('Radiation_cabinet',(x,y,1.28),(1.24,.94,2.56),'gray');b('Cabinet_black_border',(x,4.099,1.28),(1.09,.027,2.42),'black');b('Cabinet_closed_face',(x,4.076,1.28),(.97,.026,2.29),'gray')
 source_patch(g,ROOT/'source/room 030.png',(520,43,536,61),(x,4.054,2.09),(.31,.34),'Original_radiation_sign')
 b('Radiation_handle',(x+.29,4.028,1.22),(.27,.04,.045),'black')
 for i in range(9):b('Cabinet_vent',(x,4.048,.33+i*.045),(.68,.018,.018),'black')
 panel(g,3.74,4.03,1.14,1.05,.78)
 for x in [3.34,4.14]:pipe(g,'Control_pedestal_leg',[(x,4.05,.04),(x,4.05,.80)],.044,'cyan')
 finish(c)
