"""019: heart wallpaper, vanity, curtained red bed and Edna portrait."""
from pathlib import Path
from blender_shared.furnishings import source_patch,panel,curved_line
from blender_shared.bedroom_furniture import bed,cabinet,plant,chandelier,pattern,finish
ROOT=Path(__file__).resolve().parents[2]
def furnish(g,c):
 b=g.box
 pattern(g,'Heart_wallpaper',-4.27,4.27,4.91,.32,3.08,'heart','red')
 cabinet(g,'Vanity',-2.15,4.18,2.75,.83,.87,'red')
 b('Vanity_mirror_frame',(-2.23,4.54,1.61),(1.11,.11,1.42),'cyan');g.sphere('Mirror_arch',(-2.23,4.54,2.27),(.555,.056,.28),'cyan')
 b('Mirror_glass',(-2.23,4.47,1.65),(.98,.025,1.34),'aqua');g.sphere('Mirror_glass_arch',(-2.23,4.47,2.27),(.49,.018,.23),'aqua')
 curved_line(g,'Mirror_crack',[(-2.0,4.448,2.43),(-2.24,4.448,2.08),(-2.06,4.448,1.95),(-2.45,4.448,1.43)],.012,'cyan')
 for x,col in [(-3.12,'blue'),(-1.14,'pink')]:
  g.sphere('Vanity_bottle',(x,4.09,1.02),(.12,.10,.10),col);g.cyl('Bottle_neck',(x,4.09,1.15),.035,.09,col)
 bed(g,1.15,3.82,2.48,1.53,'red')
 for y in [3.05,4.6]:
  b('Canopy_post',(2.45,y,1.43),(.095,.095,2.68),'brown');b('Curtain_fold',(2.39,y,1.74),(.16,.11,1.65),'red')
 b('Canopy_valance',(2.39,3.82,2.77),(.24,1.77,.32),'red')
 for y in [3.06+i*.13 for i in range(13)]:b('Valance_highlight',(2.247,y,2.77),(.015,.018,.26),'lightred')
 g.sphere('Curtain_tie',(2.37,3.07,1.12),(.22,.12,.19),'red')
 panel(g,'Edna_portrait',.73,4.84,2.14,1.3,1.31,'yellow')
 source_patch(g,ROOT/'source/room 019.png',(193,22,231,56),(.73,4.76,2.14),(.93,.96),'Original_Edna_portrait')
 plant(g,-3.45,1.18,1.25,'purple');chandelier(g,0,3,'aqua');finish(c)
