"""029: supported crawl-space gallery with varied plumbing and damp timber."""
import random,math
from blender_shared.lab_furniture import pipe,cylinder,wheel
from blender_shared.bedroom_furniture import finish

def furnish(g,c):
 b=g.box
 # Full rear boarding, with dark seams and the source's dense damp grain.
 b('Board_backing',(0,3.309,1.1),(23.64,.02,2.2),'black')
 for row in range(10):b('Underhouse_back_board',(0,3.293,.11+row*.22),(23.64,.022,.207),'darkgray')
 rng=random.Random(29);groups={col:([],[]) for col in ['cyan','gray','black']}
 for i in range(6300):
  x=rng.uniform(-11.79,11.79);z=rng.uniform(.12,2.10);w=rng.uniform(.016,.064);h=rng.uniform(.008,.026)
  col='cyan' if i%5<3 else ('gray' if i%5==3 else 'black');vs,fs=groups[col];n=len(vs)
  vs.extend([(x,3.278,z),(x+w,3.278,z),(x+w,3.278,z+h),(x,3.278,z+h)]);fs.append((n,n+1,n+2,n+3))
 for col,(vs,fs) in groups.items():g.mesh('Damp_timber_grain_'+col,vs,fs,col)
 b('Rear_timber_sill',(0,2.94,.045),(23.64,.72,.09),'brown')
 # Joists behind the red front beam give the roof its missing depth.
 for i in range(35):
  x=-11.6+i*.68
  g.beam('Overhead_joist',(x,2.79,2.09),(x+.38,3.30,2.09),.085,'darkgray')
  g.beam('Joist_light_edge',(x-.025,2.79,2.04),(x+.355,3.30,2.04),.019,'gray')
 # Eleven red/yellow supports, matching the spacing in the panorama.
 for i in range(11):
  x=-10.10+i*2
  b('Foundation_post_foot',(x,2.73,.125),(.34,.38,.25),'white')
  b('Yellow_support_post',(x,2.73,1.09),(.18,.15,1.83),'yellow')
  b('Post_red_cap',(x,2.73,1.90),(.20,.18,.54),'red')
  b('Post_front_light',(x-.055,2.635,1.02),(.028,.02,1.66),'yellow')
  for side in [-1,1]:
   g.beam('Red_diagonal_brace',(x,2.73,1.66),(x+side*.69,2.73,2.15),.115,'lightred')
  for z in [1.87,2.02]:
   b('Support_bolt_dark',(x,2.625,z),(.055,.018,.055),'black')
   b('Support_bolt',(x-.005,2.612,z+.005),(.025,.014,.025),'gray')
 b('Red_upper_beam',(0,2.76,2.13),(23.78,.22,.14),'red')
 b('Beam_red_front_edge',(0,2.636,2.16),(23.78,.025,.026),'lightred')
 # Three main runs have different elevations and interrupted branch patterns.
 levels=[.67,1.00,1.40]
 for z in levels:pipe(g,'Long_blue_pipe',[(-9.33,3.09,z),(11.30,3.09,z)],.053,'blue',collars=False)
 branches=[
  [(-9.35,3.09,2.10),(-9.35,3.09,.67),(-8.82,3.09,.67)],
  [(-9.03,3.09,2.10),(-9.03,3.09,1.0),(-8.55,3.09,1.0)],
  [(-7.25,3.09,.18),(-7.25,3.09,1.40),(-6.75,3.09,1.40)],
  [(-1.68,3.09,.18),(-1.68,3.09,1.0),(-.60,3.09,1.0)],
  [(-.60,3.09,1.0),(-.60,3.09,2.10)],
  [(5.94,3.09,.67),(6.34,3.09,.67),(6.34,3.09,2.10)],
  [(8.17,3.09,1.4),(8.57,3.09,1.15),(9.02,3.09,1.15)],
  [(10.10,3.09,1.0),(10.10,3.09,2.10)],
  [(10.43,3.09,.67),(10.90,3.09,.67),(10.90,3.09,1.92)],
 ]
 for pts in branches:pipe(g,'Branch_blue_pipe',pts,.056,'blue')
 for row,z in enumerate(levels):
  for i in range(13):
   x=-8.85+i*1.58+(row%2)*.24
   if x>11.3:continue
   cylinder(g,'Pipe_collar',(x-.055,3.09,z),(x+.055,3.09,z),.084,'blue')
   b('Pipe_collar_glint',(x,3.002,z+.037),(.080,.016,.025),'lightblue')
  b('Pipe_upper_glint',(.985,3.050,z+.047),(20.6,.012,.015),'lightblue')
 # Small valve/spigot assembly at the right, visible between the supports.
 pipe(g,'Valve_branch',[(8.45,3.09,.67),(8.45,3.09,1.06)],.048,'blue')
 wheel(g,8.45,2.98,1.12,.20,'blue')
 cylinder(g,'Valve_outlet',(8.45,3.00,.84),(8.65,2.99,.84),.038,'blue')
 # The small rear grille at the left is scenery, not a new route.
 b('Rear_grille_recess',(-11.14,3.02,.58),(1.32,.045,.57),'black')
 for x in [-11.80,-10.48]:b('Grille_frame',(x,2.983,.58),(.028,.028,.60),'blue')
 for z in [.285,.875]:b('Grille_frame',(-11.14,2.983,z),(1.35,.028,.028),'blue')
 for i in range(13):b('Grille_vertical',(-11.75+i*.10,2.966,.58),(.012,.018,.55),'lightblue')
 for i in range(7):b('Grille_horizontal',(-11.14,2.960,.31+i*.09),(1.28,.015,.012),'lightblue')
 # Small overhead grid and the water pooled below it in the central bay.
 b('Overhead_grille_recess',(1.38,3.055,2.17),(.80,.47,.028),'black')
 for xx in [.98,1.78]:b('Overhead_grille_frame',(xx,3.055,2.15),(.025,.49,.025),'cyan')
 for yy in [2.82,3.29]:b('Overhead_grille_frame',(1.38,yy,2.15),(.82,.025,.025),'cyan')
 for i in range(10):b('Overhead_grille_wire',(1.025+i*.079,3.055,2.139),(.011,.45,.012),'gray')
 for i in range(6):b('Overhead_grille_crosswire',(1.38,2.855+i*.078,2.132),(.76,.010,.012),'cyan')
 # Broken segments make a fine static leak, rather than a solid pipe or waterfall.
 for i in range(14):
  zz=2.08-i*.137;xx=1.38+.025*math.sin(i*1.8)
  g.beam('Water_trickle',(xx,3.18,zz),(xx+.012,3.18,zz-.071),.012,'cyan')
 edge=[(-.63,-.08),(-.47,-.24),(-.14,-.28),(.13,-.22),(.46,-.26),(.63,-.08),(.51,.12),(.29,.19),(-.08,.22),(-.46,.17)]
 g.mesh('Shallow_water_pool',[(1.38+x,2.88+y,.096) for x,y in edge],[tuple(range(len(edge)))],'cyan')
 for radius,col in [(.15,'aqua'),(.29,'lightblue'),(.43,'aqua')]:
  points=[(1.38+radius*math.cos(i*math.tau/32),2.94+radius*.35*math.sin(i*math.tau/32),.099) for i in range(33)]
  for a,bb in zip(points,points[1:]):g.beam('Pool_ripple',a,bb,.008,col)
 finish(c)
