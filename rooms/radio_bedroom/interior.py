"""021: Fred's blue bed, radio laboratory and original wall art."""
from blender_shared.placement import rear_anchored
from pathlib import Path
import math
from blender_shared.furnishings import source_patch,panel,curved_line
from blender_shared.bedroom_furniture import bed,cabinet,chandelier,finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.1)
def furnish(g,c):
 b=g.box
 bed(g,-1.15,3.9,2.8,1.35)
 cabinet(g,'Radio_console',1.95,4.23,2.35,.88,.87)
 b('Radio_case',(1.94,4.22,1.25),(1.04,.57,.67),'cyan');b('Radio_face',(1.94,3.922,1.25),(.94,.025,.57),'black')
 for z in [1.37,1.49]:
  b('Tuner_scale',(1.92,3.895,z),(.65,.018,.072),'aqua')
  for i in range(9):b('Tuner_tick',(1.63+i*.07,3.88,z),(.015,.01,.052),'blue')
 for x in [1.7,2.14]:
  o=g.cyl('Tuning_knob',(0,0,0),.10,.05,'gray',16);o.rotation_euler.x=math.pi/2;o.location=(x,3.87,1.07)
 for x in [1.32,2.57]:
  g.cyl('Radio_coil_core',(x,4.24,1.43),.045,.84,'cyan')
  for k in range(8):g.cyl('Radio_coil',(x,4.24,1.38+k*.047),.09,.016,'yellow')
 curved_line(g,'Loop_aerial',[(1.94+.23*math.cos(a*math.tau/32),4.29,1.97+.23*math.sin(a*math.tau/32)) for a in range(33)],.025,'aqua')
 g.cyl('Aerial_mast',(1.94,4.29,1.68),.02,.30,'aqua')
 for x in [.96,2.95]:
  g.cyl('Microphone_base',(x,4.08,.98),.14,.045,'aqua');g.cyl('Microphone_stand',(x,4.08,1.12),.025,.28,'cyan');g.sphere('Microphone',(x,4.08,1.41),(.09,.07,.23),'aqua')
  for k in range(7):b('Mic_grille',(x,4.005,1.26+k*.045),(.14,.018,.012),'cyan')
 panel(g,'Fred_portrait',-1.8,4.83,2.06,1.25,1.23,'yellow')
 source_patch(g,ROOT/'source/room 021.png',(97,28,138,61),(-1.8,4.755,2.06),(.95,.96),'Original_Fred_portrait')
 source_patch(g,ROOT/'source/room 021.png',(160,25,200,73),(-.15,4.79,2.03),(.83,1.0),'Wanted_poster')
 chandelier(g,.3,3.1,'yellow')
 g.sphere('Pendant_center_globe',(.3,3.1,2.88),(.12,.12,.15),'yellow')
 g.sphere('Center_globe_glint',(.275,3.005,2.92),(.038,.024,.08),'white')
 finish(c)
