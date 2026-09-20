"""Background 017: grand piano, sound cabinet, gramophone and television."""
from pathlib import Path
import math,bpy
from blender_shared.furnishings import panel,source_patch,curved_line
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # White fluted pilasters and pink inset panels.
 for x in [-3.25,-1.65,-.05,1.55,3.15]:
  b('Pilaster',(x,3.63,1.56),(.18,.18,3.12),'white')
  for dx in [-.06,0,.06]:b('Column_flute',(x+dx,3.527,1.56),(.022,.018,2.9),'gray')
  for z in [.10,3.0]:b('Column_capital',(x,3.59,z),(.3,.26,.14),'white')
 for x in [-2.45,-.85,.75,2.35]:
  for inset,col in [(0,'purple'),(.035,'pink'),(.1,'purple'),(.125,'pink')]:b('Pink_wall_panel',(x,3.69-inset*.10,2.0),(1.35-2*inset,.028,1.91-2*inset),col)
 b('White_dado',(0,3.60,.43),(7.45,.12,.65),'white')
 b('Dado_rail',(0,3.52,.82),(7.5,.1,.075),'gray')
 # Small grand piano, rounded tail, solid lid, keyboard and turned legs.
 outline=[(-2.6,2.12),(-.4,2.12),(-.4,2.65),(-.65,3.05),(-1.0,3.23),(-1.65,3.26),(-2.6,2.9)]
 vs=[(x,y,z) for z in [.73,1.02] for x,y in outline];n=len(outline)
 geo.mesh('Grand_piano_body',vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)],'black')
 for x,y in [(-2.42,2.28),(-.61,2.35),(-1.6,3.08)]:
  geo.cyl('Piano_leg',(x,y,.41),.085,.72,'black',12)
  for z in [.18,.55]:geo.sphere('Piano_turned_leg',(x,y,z),(.13,.13,.075),'black')
 b('Piano_keyboard',(-1.7,1.985,.85),(1.62,.30,.07),'white')
 for i in range(23):
  x=-2.46+i*.066;b('Piano_key_gap',(x,1.98,.89),(.006,.29,.012),'black')
  if i%7 not in [2,6]:b('Piano_black_key',(x+.03,2.05,.92),(.038,.17,.058),'black')
 b('Music_rest',(-1.7,2.17,1.19),(1.2,.06,.3),'black')
 b('Piano_bench',(-1.72,1.18,.48),(.94,.46,.13),'blue')
 for x in [-2.09,-1.35]:
  for y in [1.02,1.34]:b('Bench_leg',(x,y,.24),(.07,.07,.48),'black')
 geo.sphere('Piano_vase',(-1.03,2.62,1.16),(.11,.11,.18),'lime');geo.cyl('Vase_neck',(-1.03,2.62,1.35),.055,.1,'green',12)
 for obj in list(geo.collections[geo.active].objects):
  if obj.name.startswith(('Grand_piano','Piano_','Music_rest','Bench_','Vase_')):obj.location.x+=.60
 # Stereo cabinet and gramophone horn.
 b('Stereo_cabinet',(.65,3.12,.65),(1,.69,1.30),'brown');panel(geo,'Stereo_front',.65,2.758,.57,.91,.94)
 for z in [.38,.77]:
  b('Stereo_aqua_face',(.65,2.69,z),(.77,.045,.29),'cyan')
  for i in range(5):b('Stereo_key',(.36+i*.14,2.655,z),(.06,.02,.08),'black')
 b('Turntable',(.65,3.12,1.34),(.97,.68,.1),'red');geo.cyl('Record',(.65,3.12,1.41),.24,.025,'black',24)
 # Trumpet axis along X, opening to the left.
 verts=[(x,3.12+r*math.cos(i*math.tau/20),1.94+r*math.sin(i*math.tau/20)) for x,r in [(.9,.07),(.05,.29)] for i in range(20)]
 geo.mesh('Gramophone_horn',verts,[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],'yellow')
 curved_line(geo,'Horn_rim',[(.05,3.12+.29*math.cos(i*math.tau/20),1.94+.29*math.sin(i*math.tau/20)) for i in range(21)],.035,'red')
 curved_line(geo,'Gramophone_pipe',[(.9,3.12,1.94),(1.02,3.12,1.73),(.73,3.12,1.52)],.06,'brown')
 # CRT with blue glass, side controls and a low stand.
 b('TV_stand',(2.54,3.14,.29),(1.33,.77,.58),'brown');panel(geo,'TV_stand_panel',2.54,2.737,.3,1.26,.5)
 b('CRT_body',(2.54,3.12,1.17),(1.38,.72,1.08),'black')
 b('CRT_aqua_frame',(2.54,2.74,1.17),(1.30,.06,1.0),'cyan');b('CRT_screen',(2.4,2.69,1.17),(.93,.06,.8),'blue')
 geo.sphere('CRT_screen_glow',(2.4,2.65,1.17),(.44,.025,.36),'lightblue')
 for i in range(7):b('CRT_vent',(3.06,2.69,.85+i*.08),(.17,.04,.03),'black')
 for x in [3.01,3.10]:b('TV_button',(x,2.675,1.48),(.035,.02,.09),'red')
 source_patch(geo,ROOT/'source/room 017.png',(151,3,172,32),(-1.16,3.48,2.68),(.35,.48),'Wall_paint',only={'cyan','lightred','gray'})
 source_patch(geo,ROOT/'source/room 017.png',(219,8,251,51),(-.62,3.48,2.29),(.54,.73),'Wall_splatter',only={'red'})
 bpy.data.objects['Wall_front'].name='Front_inferred_music'
