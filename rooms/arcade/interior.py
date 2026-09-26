"""Background 018: six solid arcade cabinets with original marquee art."""
from pathlib import Path
import bpy,math
from mathutils import Matrix
from blender_shared.furnishings import source_patch
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box
 # Distinct cabinets share a construction recipe, while preserving every source title.
 crops=[(171,14,210,37),(229,21,266,36),(293,17,329,38),(349,17,385,38),(403,24,442,38),(469,15,506,39)]
 for i,(col,crop) in enumerate(zip(['green','lightred','lightblue','gray','blue','cyan'],crops)):
  x=-2.30+i*1.40;y=4.79;w=.92
  # Side profile: tall marquee, recessed display and projecting control deck.
  profile=[(y+.43,0),(y-.45,0),(y-.45,.88),(y-.57,1.02),(y-.28,1.26),(y-.25,1.84),(y-.49,1.92),(y-.49,2.3),(y+.43,2.3)]
  vs=[(x+side*w/2,yy,z) for side in [-1,1] for yy,z in profile];n=len(profile)
  geo.mesh('Arcade_cabinet_'+str(i),vs,[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)],'black')
  # Only Disco Crazy has the projecting gray staircase in background 018.
  if i==1:
   for level in range(3):
    b('Disco_plinth_step',(x,y-.12-level*.055,.025+level*.035),(w+.12-level*.025,1.12-level*.12,.035),'gray')
  b('Cabinet_base_color',(x,y-.465,.43),(w-.07,.025,.76),col)
  b('Coin_door_outline',(x,y-.481,.43),(w-.17,.008,.65),'black')
  b('Coin_door_face',(x,y-.487,.43),(w-.22,.006,.60),col)
  for dx in [-.21,.21]:
   b('Coin_slot_plate',(x+dx,y-.497,.51),(.13,.014,.39),'black')
   b('Coin_entry',(x+dx,y-.507,.65),(.068,.008,.052),'lightred')
   b('Coin_return',(x+dx,y-.507,.43),(.072,.008,.080),'gray')
   b('Coin_return_recess',(x+dx,y-.513,.447),(.047,.004,.035),'black')
  b('Coin_door_lock',(x-.24,y-.494,.20),(.025,.006,.028),'black')
  b('Screen_trim',(x,y-.30,1.51),(w-.09,.04,.65),['green','gray','gray','gray','cyan','cyan'][i]);b('Dark_screen',(x,y-.327,1.51),(w-.15,.03,.55),'black')
  geo.beam('Screen_glint',(x-.23,y-.347,1.71),(x-.18,y-.347,1.76),.022,'lightblue')
  b('Control_panel',(x,y-.45,1.045),(w-.05,.26,.05),col)
  geo.cyl('Joystick_stick',(x-.16,y-.48,1.13),.015,.12,'gray');geo.sphere('Joystick_ball',(x-.16,y-.48,1.21),(.045,.045,.045),'cyan' if i==1 else 'red')
  for dx in [.05,.16]:geo.cyl('Arcade_button',(x+dx,y-.5,1.084),.027,.025,'white')
  # Copy only the visible painted side motifs, excluding the purple wall pixels.
  side_crops=[(210,39,223,88),(267,31,281,80),(331,35,345,91),None,(442,37,458,87),(508,36,519,83)]
  if side_crops[i]:
   before=set(bpy.data.objects)
   source_patch(geo,ROOT/'source/room 018.png',side_crops[i],(0,0,1.22),(.63,1.42),'Cabinet_side_art_'+str(i),only=['yellow','red','lightred','white','gray','blue','lightblue','green','lime','cyan','aqua'])
   bpy.context.view_layer.update()
   transform=Matrix.Translation((x+w/2+.001,y,0))@Matrix.Rotation(math.pi/2,4,'Z')
   for obj in set(bpy.data.objects)-before:obj.matrix_world=transform@obj.matrix_world
  source_patch(geo,ROOT/'source/room 018.png',crop,(x,y-.505,2.11),(w-.03,.35),'Original_marquee_'+str(i))
 # Low pinball table at the left, leaving the front doorway and central aisle free.
 b('Pinball_body',(-4.15,2.27,.69),(1.32,.72,.25),'lightred');b('Pinball_glass',(-4.15,2.27,.83),(1.23,.65,.025),'white')
 # The source table has tapered blue trestles, rather than four straight metal posts.
 for x in [-4.65,-3.65]:
  for ya,yb in [(1.99,2.17),(2.55,2.37)]:
   geo.beam('Pinball_splayed_leg',(x,ya,.05),(x,yb,.57),.085,'lightblue')
  geo.beam('Pinball_trestle_brace',(x,2.06,.14),(x,2.48,.14),.035,'blue')
 b('Pinball_front_white_stripe',(-4.15,1.903,.72),(1.31,.016,.025),'white')
 geo.cyl('Pinball_dark_detail',(-4.15,2.27,.85),.12,.012,'black')
 # Right-wall target and left-wall original poster, rotated as wall art.
 before=set(geo.collections[geo.active].objects)
 source_patch(geo,ROOT/'source/room 018.png',(34,16,59,87),(0,0,1.92),(.5,1.42),'Arcade_poster')
 for o in set(geo.collections[geo.active].objects)-before:o.rotation_euler.z=math.pi/2;o.location=(-c['geometry']['halfWidth']+.20,3.15,0)
 for layer,(radius,col) in enumerate([(.40,'black'),(.30,'red'),(.21,'black'),(.11,'red')]):
  geo.mesh('Wall_target',[(c['geometry']['halfWidth']-.19-layer*.003,2.7+radius*math.cos(i*math.tau/32),1.9+radius*math.sin(i*math.tau/32)) for i in range(32)],[tuple(reversed(range(32)))],col)
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_arcade'
