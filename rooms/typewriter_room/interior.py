"""027: family portrait, stone fireplace, typewriter, plants and original wallpaper."""
from pathlib import Path
import math
from blender_shared.furnishings import source_patch,panel
from blender_shared.bedroom_furniture import cabinet,plant,finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 source_patch(g,ROOT/'source/room 027.png',(176,8,313,64),(1.45,4.907,2.14),(5.55,1.87),'Original_den_wallpaper')
 source_patch(g,ROOT/'source/room 027.png',(71,8,110,64),(-3.53,4.907,2.14),(1.40,1.87),'Original_den_wallpaper_left')
 b('Den_wainscot',(0,4.85,.54),(8.5,.10,1.02),'brown')
 for z,col in [(.13,'red'),(1.06,'black'),(1.12,'yellow')]:b('Den_panel_rail',(0,4.77,z),(8.5,.045,.055),col)
 # Three-dimensional fireplace surrounds an actual recess with a dark back.
 x,y=-1.8,4.39
 b('Fireplace_dark_recess',(x,4.765,.57),(1.43,.03,1.08),'black')
 for dx in [-.81,.81]:b('Stone_fireplace_pier',(x+dx,y,.57),(.43,.74,1.14),'gray')
 b('Fireplace_lintel',(x,y,1.07),(2.10,.74,.27),'gray');b('Fireplace_mantel',(x,y,1.26),(2.26,.88,.12),'brown')
 # Raised irregular stone faces wrap around the opening.
 for dx in [-.81,.81]:
  for k in range(5):
   z=.12+k*.20
   g.mesh('Fireplace_stone',[(x+dx-.17,y-.382,z-.08),(x+dx+.16,y-.382,z-.09),(x+dx+.19,y-.382,z+.065),(x+dx-.12,y-.382,z+.09)],[(0,1,2,3)],'brown' if k%2 else 'red')
 for dx in [-.48,0,.48]:b('Lintel_stone',(x+dx,y-.382,1.09),(.39,.025,.15),'brown')
 panel(g,'Family_portrait_frame',-1.8,4.79,2.18,1.80,1.60)
 source_patch(g,ROOT/'source/room 027.png',(115,13,168,61),(-1.8,4.71,2.18),(1.55,1.36),'Original_family_portrait')
 cabinet(g,'Typewriter_table',.56,4.14,1.33,.89,.75,'red')
 b('Typewriter_base',(.56,4.13,.91),(1.03,.62,.21),'black')
 b('Typewriter_keyboard',(.56,3.93,1.005),(.88,.30,.06),'darkgray')
 for row in range(3):
  for col in range(10):g.cyl('Typewriter_key',(.19+col*.079+(row%2)*.024,3.82+row*.087,1.047),.022,.018,'white',8)
 b('Typewriter_body',(.56,4.34,1.10),(.86,.22,.35),'black')
 roller=g.cyl('Typewriter_roller',(0,0,0),.07,1.0,'gray',16);roller.rotation_euler.y=math.pi/2;roller.location=(.56,4.32,1.31)
 b('Typewriter_paper',(.56,4.36,1.45),(.64,.013,.28),'white')
 for z in [1.39,1.43,1.47]:b('Typed_line',(.56,4.348,z),(.40,.006,.009),'darkgray')
 plant(g,-3.59,4.05,2.05)
 # Empty right pot sits forward of the observatory ladder's clear approach.
 g.cyl('Empty_pot',(2.22,4.54,.27),.27,.49,'cyan',16);g.cyl('Empty_pot_rim',(2.22,4.54,.51),.32,.11,'cyan',16);g.cyl('Empty_pot_inside',(2.22,4.54,.57),.25,.014,'black',16)
 for i,(w,d,col) in enumerate([(3.6,1.36,'pink'),(3.25,1.11,'purple')]):b('Den_rug',(0,1.04,.002+i*.002),(w,d,.001),col)
 finish(c)
