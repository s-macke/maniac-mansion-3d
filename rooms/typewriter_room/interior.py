"""027: family portrait, stone fireplace, typewriter, plants and original wallpaper."""
from pathlib import Path
import math
from blender_shared.furnishings import source_patch,panel
from blender_shared.bedroom_furniture import plant,finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 source_patch(g,ROOT/'source/room 027.png',(176,8,313,64),(1.45,4.907,2.14),(5.55,1.87),'Original_den_wallpaper')
 source_patch(g,ROOT/'source/room 027.png',(71,8,110,64),(-3.53,4.907,2.14),(1.40,1.87),'Original_den_wallpaper_left')
 b('Den_wainscot',(0,4.85,.54),(8.5,.10,1.02),'brown')
 for z,col in [(.13,'red'),(1.06,'black'),(1.12,'yellow')]:b('Den_panel_rail',(0,4.77,z),(8.5,.045,.055),col)
 # Complete the inset rectangular outlines of the original timber panels.
 for left,right in [(-4.18,-3.12),(-.59,1.42),(1.50,2.42),(2.50,4.18)]:
  for z in [.22,.94]:b('Den_panel_border',((left+right)/2,4.788,z),(right-left,.018,.025),'red')
  for xx in [left,right]:b('Den_panel_border',(xx,4.788,.58),(.025,.018,.72),'red')
 # Three-dimensional fireplace surrounds an actual recess with a dark back.
 x,y=-1.8,4.39
 b('Fireplace_dark_recess',(x,4.765,.57),(1.43,.03,1.08),'black')
 for dx in [-.81,.81]:b('Stone_fireplace_pier',(x+dx,y,.57),(.43,.74,1.14),'gray')
 b('Fireplace_lintel',(x,y,1.07),(2.10,.74,.27),'gray');b('Fireplace_mantel',(x,y,1.26),(2.26,.88,.12),'brown')
 # Original irregular red/brown stone faces and colored flecks, flush with
 # the solid three-dimensional piers and lintel (the opening remains empty).
 source_patch(g,ROOT/'source/room 027.png',(99,74,183,108),(x,4.012,.57),(2.10,1.14),'Original_fireplace_stones',only={'red','lightred','brown','gray','darkgray'})
 b('Mantel_yellow_edge',(x,3.944,1.26),(2.26,.014,.032),'yellow')
 panel(g,'Family_portrait_frame',-1.8,4.91,2.18,1.80,1.60)
 source_patch(g,ROOT/'source/room 027.png',(115,13,168,61),(-1.8,4.848,2.18),(1.55,1.36),'Original_family_portrait')
 # The source has an open red table, not a closed cupboard.
 b('Typewriter_table_top',(.56,4.14,.77),(1.43,.99,.09),'red')
 for xx in [-.035,1.155]:
  for yy in [3.76,4.52]:
   b('Typewriter_table_leg',(xx,yy,.375),(.10,.10,.75),'red')
   b('Table_leg_highlight',(xx-.021,yy-.053,.375),(.025,.012,.70),'yellow')
 for yy in [3.75,4.53]:
  b('Table_apron',(.56,yy,.64),(1.19,.07,.16),'red')
  b('Table_apron_edge',(.56,yy-.042,.69),(1.16,.013,.022),'yellow')
 b('Typewriter_base',(.56,4.13,.91),(1.03,.62,.21),'black')
 b('Typewriter_keyboard',(.56,3.93,1.005),(.88,.30,.06),'darkgray')
 for row in range(3):
  for col in range(10):g.cyl('Typewriter_key',(.19+col*.079+(row%2)*.024,3.82+row*.087,1.047),.022,.018,'white',8)
 b('Typewriter_body',(.56,4.34,1.10),(.86,.22,.35),'black')
 roller=g.cyl('Typewriter_roller',(0,0,0),.07,1.0,'gray',16);roller.rotation_euler.y=math.pi/2;roller.location=(.56,4.32,1.31)
 # Short pale sheet at the carriage, rather than a tall printed page.
 b('Typewriter_paper',(.56,4.355,1.32),(.64,.018,.09),'white')
 for xx in [-.01,1.13]:
  knob=g.cyl('Carriage_knob',(0,0,0),.055,.09,'black',12);knob.rotation_euler.y=math.pi/2;knob.location=(xx,4.32,1.31)
 b('Typewriter_spacebar',(.56,3.777,1.047),(.46,.035,.023),'gray')
 plant(g,-3.59,4.05,2.05)
 # Empty right pot sits forward of the observatory ladder's clear approach.
 g.cyl('Empty_pot',(2.22,4.54,.27),.27,.49,'cyan',16);g.cyl('Empty_pot_rim',(2.22,4.54,.51),.32,.11,'cyan',16);g.cyl('Empty_pot_inside',(2.22,4.54,.57),.25,.014,'black',16)
 for i,(w,d,col) in enumerate([(3.6,1.36,'pink'),(3.25,1.11,'purple')]):b('Den_rug',(0,1.04,.002+i*.002),(w,d,.001),col)
 finish(c)
