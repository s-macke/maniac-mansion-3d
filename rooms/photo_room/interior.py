"""Background 023: black darkroom with red photographic bench and drawer cabinet."""
from blender_shared.placement import rear_anchored, offset_group
import math,bpy
from blender_shared.furnishings import curved_line

@rear_anchored(5.1)
def furnish(geo,c):
 b=geo.box
 with offset_group(x=0.5, y=0):
  # Broad red workbench, with a white-edged surface and wooden end panel.
  b('Darkroom_bench',(-2.38,4.10,.49),(2.96,1.12,.98),'red')
  b('Workbench_top',(-2.38,4.10,1.01),(3.05,1.18,.09),'lightred')
  b('Workbench_front_edge',(-2.38,3.492,.98),(3.05,.028,.055),'white')
  b('Workbench_black_inset',(-2.38,3.474,.82),(2.94,.025,.09),'black')
  b('Workbench_wood_end',(-.89,4.10,.49),(.10,1.14,.98),'brown')
  # Shallow yellow developer tray, dark liquid and adjacent sheet of paper.
  b('Developing_tray',(-3.13,4.01,1.075),(.75,.48,.045),'yellow');b('Tray_dark_liquid',(-3.13,4.01,1.102),(.64,.37,.014),'black')
  for x in [-3.52,-2.74]:b('Tray_handle',(x,4.01,1.09),(.07,.18,.03),'yellow')
  b('Photographic_paper',(-1.93,3.93,1.064),(.87,.52,.008),'white')
  # Enlarger: support column, movable head, bellows and lens above the paper.
  ex,ey=-1.27,4.17
  b('Enlarger_base',(ex,ey,1.085),(.54,.54,.065),'brown')
  b('Enlarger_column',(ex+.15,ey+.13,1.70),(.095,.09,1.20),'gray')
  b('Enlarger_column_highlight',(ex+.094,ey+.072,1.70),(.021,.016,1.2),'white')
  b('Enlarger_head',(ex-.13,ey,1.98),(.49,.38,.28),'brown')
  # Original head narrows in three rounded red steps above its brown housing.
  for r,z,h in [(.205,2.125,.055),(.155,2.18,.055),(.095,2.228,.041)]:
   geo.cyl('Enlarger_stepped_cap',(ex-.13,ey,z),r,h,'lightred',24)
  for z,r in [(2.15,.185),(2.202,.125)]:geo.cyl('Cap_dark_band',(ex-.13,ey,z),r,.012,'red',24)
  for z in [1.77+i*.042 for i in range(5)]:b('Bellows_fold',(ex-.13,ey,z),(.37,.34,.019),'red')
  # Red head has two pale bands and a row of black ventilation slots.
  b('Enlarger_upper_band',(ex-.13,ey-.202,2.07),(.51,.018,.025),'gray')
  for dx in [-.13,0,.13]:b('Enlarger_vent',(ex-.13+dx,ey-.205,1.88),(.055,.018,.027),'black')
  b('Enlarger_head_band',(ex-.13,ey-.202,1.96),(.51,.018,.032),'white')
  geo.cyl('Enlarger_lens',(ex-.13,ey,1.715),.092,.13,'gray',16);geo.cyl('Lens_glass',(ex-.13,ey,1.642),.074,.02,'black',16)
  geo.beam('Enlarger_focus_arm',(ex-.32,ey,1.84),(ex-.70,ey,1.84),.035,'brown');geo.sphere('Focus_knob',(ex-.70,ey,1.84),(.075,.075,.045),'red')
  # The orange curled power lead climbs from the head to the ceiling.
  curved_line(geo,'Enlarger_power_lead',[(ex-.13+.038*math.sin(i*.9),ey+.035*math.cos(i*.9),2.25+i*.020) for i in range(43)],.018,'brown')
  # Hanging safelight with a red underside; illumination stays in the static bake.
  lx,ly=-2.93,4.15
  geo.cyl('Safelight_wire',(lx,ly,2.78),.015,.65,'brown')
  verts=[(lx+r*math.cos(i*math.tau/20),ly+r*math.sin(i*math.tau/20),z) for r,z in [(.31,2.38),(.075,2.55)] for i in range(20)]
  geo.mesh('Safelight_shade',verts,[(i,(i+1)%20,(i+1)%20+20,i+20) for i in range(20)],'gray')
  lamp=geo.cyl('Safelight_red_glass',(lx,ly,2.365),.063,.045,'lightred',20);lamp['bake_unlit']=True;lamp['bake_no_shadow']=True
 # Wide, shallow eight-drawer paper/negative cabinet from the source.
 b('Darkroom_drawer_case',(1.42,4.47,1.05),(3.02,.92,2.10),'brown')
 b('Darkroom_cabinet_front',(1.42,3.985,1.05),(2.88,.045,2.02),'red')
 for i in range(8):
  z=.23+i*.244
  b('Drawer_pale_border',(1.42,3.95,z),(2.67,.029,.212),'lightred')
  b('Drawer_red_face',(1.42,3.928,z),(2.56,.025,.160),'red')
  b('Drawer_top_highlight',(1.42,3.909,z+.070),(2.53,.012,.016),'lightred')
  b('Drawer_handle',(1.42,3.885,z),(.23,.055,.026),'gray')
  b('Drawer_handle_glint',(1.42,3.852,z+.016),(.17,.012,.018),'white')
 for x in [-.04,2.88]:b('Cabinet_foot',(x,4.46,.06),(.10,.71,.12),'brown')
 # Sparse seams keep the source's nearly black room legible without adding white lights.
 for x in [-c['geometry']['halfWidth']+.20,c['geometry']['halfWidth']-.20]:b('Darkroom_wall_seam',(x,4.905,1.56),(.008,.012,3.12),'gray')
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_photo_room'
