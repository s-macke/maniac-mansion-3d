"""Background 018: six solid arcade cabinets with original marquee art."""
from pathlib import Path
import bpy,math
from blender_shared.furnishings import source_patch
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Distinct cabinets share a construction recipe, while preserving every source title.
 crops=[(171,14,210,37),(229,21,266,36),(293,17,329,38),(349,17,385,38),(403,24,442,38),(469,15,506,39)]
 for i,(col,crop) in enumerate(zip(['green','lightred','lightblue','gray','blue','cyan'],crops)):
  x=-2.15+i*.85;y=4.79;w=.70
  # Side profile: tall marquee, recessed display and projecting control deck.
  profile=[(y+.43,0),(y-.45,0),(y-.45,.88),(y-.57,1.02),(y-.28,1.26),(y-.25,1.84),(y-.49,1.92),(y-.49,2.3),(y+.43,2.3)]
  vs=[(x+side*w/2,yy,z) for side in [-1,1] for yy,z in profile];n=len(profile)
  geo.mesh('Arcade_cabinet_'+str(i),vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],'black')
  b('Cabinet_base_color',(x,y-.465,.43),(w-.07,.025,.76),col)
  b('Coin_slot_plate',(x,y-.485,.51),(.29,.022,.48),'black')
  for dx in [-.08,.08]:
   b('Coin_slot',(x+dx,y-.502,.60),(.07,.014,.04),'gray');b('Coin_return',(x+dx,y-.502,.35),(.07,.014,.06),'lightred')
  b('Screen_trim',(x,y-.30,1.51),(w-.09,.04,.65),col);b('Dark_screen',(x,y-.327,1.51),(w-.15,.03,.55),'black')
  geo.beam('Screen_glint',(x-.23,y-.347,1.71),(x-.18,y-.347,1.76),.022,'lightblue')
  b('Control_panel',(x,y-.45,1.045),(w-.05,.26,.05),col)
  geo.cyl('Joystick_stick',(x-.16,y-.48,1.13),.015,.12,'gray');geo.sphere('Joystick_ball',(x-.16,y-.48,1.21),(.045,.045,.045),'red')
  for dx in [.05,.16]:geo.cyl('Arcade_button',(x+dx,y-.5,1.084),.027,.025,'white')
  source_patch(geo,ROOT/'source/room 018.png',crop,(x,y-.505,2.11),(w-.03,.35),'Original_marquee_'+str(i))
 # Low pinball table at the left, leaving the front doorway and central aisle free.
 b('Pinball_body',(-1.88,2.27,.69),(1.32,.72,.25),'lightred');b('Pinball_glass',(-1.88,2.27,.83),(1.23,.65,.025),'white')
 for x in [-2.38,-1.38]:
  for y in [2.02,2.52]:geo.beam('Pinball_leg',(x,y,.04),(x,y,.65),.06,'gray')
 geo.cyl('Pinball_dark_detail',(-1.88,2.27,.85),.12,.012,'black')
 # Right-wall target and left-wall original poster, rotated as wall art.
 before=set(geo.collections[geo.active].objects)
 source_patch(geo,ROOT/'source/room 018.png',(34,16,59,87),(0,0,1.92),(.5,1.42),'Arcade_poster')
 for o in set(geo.collections[geo.active].objects)-before:o.rotation_euler.z=math.pi/2;o.location=(-2.70,3.15,0)
 for layer,(radius,col) in enumerate([(.40,'black'),(.30,'red'),(.21,'black'),(.11,'red')]):
  geo.mesh('Wall_target',[(2.71-layer*.003,2.7+radius*math.cos(i*math.tau/32),1.9+radius*math.sin(i*math.tau/32)) for i in range(32)],[tuple(reversed(range(32)))],col)
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_arcade'
