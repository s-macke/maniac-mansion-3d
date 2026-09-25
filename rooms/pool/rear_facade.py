"""Inferred rear elevation, requested by the user; borrows front-exterior EGA motifs.
All masses sit behind the pool boundary. The pantry aperture stays a real portal.
"""
def build(geo,port):
 box,mesh,beam=geo.box,geo.mesh,geo.beam
 geo.active='Architecture'
 cy=port['position'][1];dw=port['width'];dh=port['height']
 lo,hi=-4.,15.;height=7.3
 for a,b in [(lo,cy-dw/2),(cy+dw/2,hi)]:
  box('Rear_house_wall',(-.12,(a+b)/2,height/2),(.24,b-a,height),'gray')
 box('Rear_house_header',(-.12,cy,(dh+height)/2),(.24,dw,height-dh),'gray')
 # Side returns give depth; no interior block may obscure the pantry portal.
 for y in [lo,hi]:box('Rear_house_return',(-2.5,y,3.65),(5.,.20,7.3),'gray')
 for z in [i*.24 for i in range(31)]:
  for a,b in ([(lo,cy-dw/2),(cy+dw/2,hi)] if z<dh else [(lo,hi)]):
   box('Rear_siding_joint',(.009,(a+b)/2,z),(.018,b-a,.026),'darkgray')
 for y in [lo,hi]:box('Rear_corner_board',(.045,y,height/2),(.09,.16,height),'brown')
 # Low brick plinth, broken at the existing doorway: no step across its threshold.
 for a,b in [(lo,cy-dw/2),(cy+dw/2,hi)]:
  box('Rear_brick_plinth',(.028,(a+b)/2,.19),(.056,b-a,.38),'red')
  for z in [.12,.25]:box('Rear_mortar',(.061,(a+b)/2,z),(.01,b-a,.016),'brown')
  for i in range(int((b-a)/.48)):
   y=a+.24+i*.48
   for z in [.065,.19,.315]:box('Rear_brick_joint',(.062,y+(.2 if z==.19 else 0),z),(.012,.014,.105),'brown')
 def window(y,z,w=.94,h=1.8):
  box('Rear_window_frame',(.07,y,z),(.14,w+.14,h+.14),'brown')
  box('Rear_window_dark',(.152,y,z),(.024,w+.07,h+.07),'black')
  for dy in [-w/2,w/2]:box('Rear_window_red_sash',(.18,y+dy,z),(.045,.055,h),'red')
  for dz in [-h/2,0,h/2]:box('Rear_window_crossbar',(.18,y,z+dz),(.045,w,.045),'brown')
  box('Rear_window_gold_edge',(.209,y-w/2+.065,z),(.014,.018,h-.08),'yellow')
  for dz in [-.35,.5]:beam('Rear_window_glint',(.217,y-w*.28,z+dz),(.217,y-w*.13,z+dz+.09),.025,'cyan')
  box('Rear_window_sill',(.16,y,z-h/2-.10),(.32,w+.23,.12),'gray')
 for y in [-2.4,.3,6.2,9.,12.8]:window(y,1.85)
 for y in [-2.2,1.4,5.,8.6,12.2]:window(y,5.5,1.05,1.65)
 for z in [3.48,7.25]:
  box('Rear_floor_cornice',(.085,(lo+hi)/2,z),(.17,hi-lo+.22,.13),'brown')
  box('Rear_cornice_highlight',(.178,(lo+hi)/2,z+.047),(.016,hi-lo+.22,.024),'yellow')
 # Shallow entrance canopy, with no columns obstructing the walking strip.
 box('Rear_pantry_canopy',(.53,cy,3.22),(1.55,3.4,.13),'darkgray')
 box('Rear_canopy_fascia',(1.32,cy,3.19),(.10,3.48,.22),'brown')
 for y in [cy-1.5,cy+1.5]:beam('Rear_canopy_bracket',(.12,y,2.9),(1.23,y,3.2),.10,'brown')
 v=[(1.37,cy-1.8,3.31),(1.37,cy+1.8,3.31),(1.37,cy,4.35),(-.3,cy-1.8,3.31),(-.3,cy+1.8,3.31),(-.3,cy,4.35)]
 mesh('Rear_entrance_gable',v,[(0,1,2),(3,5,4)],'darkgray')
 mesh('Rear_entrance_roof',v,[(0,2,5,3),(2,1,4,5)],'blue')
 for a,b in [(0,2),(2,1),(0,1)]:beam('Rear_gable_edge',v[a],v[b],.09,'lightblue')
 def hip(name,x,y,z,w,d,rise):
  v=[(x-w/2,y-d/2,z),(x+w/2,y-d/2,z),(x+w/2,y+d/2,z),(x-w/2,y+d/2,z),(x,y-d*.33,z+rise),(x,y+d*.33,z+rise)]
  mesh(name,v,[(0,1,4),(1,2,5,4)],'blue');mesh(name+'_far',v,[(2,3,5),(3,0,4,5)],'lightblue')
  for a,b in [(0,1),(1,2),(2,3),(3,0),(4,5)]:beam(name+'_edge',v[a],v[b],.09,'cyan')
 hip('Rear_main_roof',-2.45,5.5,7.36,5.7,19.9,1.6)
 # Modest offset tower and chimney echo the front silhouette, without copying its entrance.
 box('Rear_roof_tower',(-2.,10.4,8.9),(2.5,2.7,3.0),'gray')
 for z in [7.55,10.4]:box('Rear_tower_cornice',(-2.,10.4,z),(2.72,2.92,.15),'cyan')
 for y in [9.78,11.02]:
  box('Rear_tower_window',(-.736,y,9.28),(.028,.5,1.25),'black')
  box('Rear_tower_window_edge',(-.711,y-.30,9.28),(.03,.09,1.35),'lightblue')
 hip('Rear_tower_roof',-2.,10.4,10.5,3.1,3.3,1.15)
 for y in [-1.7,-.75]:
  box('Rear_chimney',(-3.4,y,8.6),(.50,.5,2.),'darkgray')
  box('Rear_chimney_cap',(-3.4,y,9.64),(.65,.66,.14),'gray')
