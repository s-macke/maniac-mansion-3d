"""024: tiled bathroom, elevated cistern, cracked mirror and curtained tub."""
from blender_shared.placement import rear_anchored, offset_group
from pathlib import Path
import math,bpy
from mathutils import Matrix
from blender_shared.furnishings import source_patch,curved_line
from blender_shared.bedroom_furniture import finish
ROOT=Path(__file__).resolve().parents[2]
@rear_anchored(5.1)
def furnish(g,c):
 b=g.box
 # Tile coverage follows the current shell; Y uses the rear-anchored artwork frame.
 W=c['geometry']['halfWidth'];D=c['geometry']['depth'];front=5.1-D
 for i in range(int((2*W-.4)/.60)+1):
  x=-W+.2+i*.60;b('Floor_grout',(x,(front+5.1)/2,.003),(.014,D-.36,.004),'black')
 for i in range(int((D-.4)/.60)+1):
  y=front+.2+i*.60;b('Floor_grout',(0,y,.003),(2*W-.4,.014,.004),'black')
 for i in range(int((2*W-.5)/.36)+1):
  x=-W+.25+i*.36
  if -1.55<x<.15:continue
  for k in range(5):
   z=.18+k*.22;b('Wall_tile',(x,4.905,z),(.34,.024,.20),'aqua')
   for dx,dz in [(-.08,.04),(.05,-.045),(.09,.055)]:b('Tile_speck',(x+dx,4.889,z+dz),(.026,.009,.031),'cyan')
 with offset_group(x=0.7, y=0):
  with offset_group(x=-.25):
   # Wall hung basin and exposed waste trap.
   g.sphere('Basin_bowl',(-2.58,4.38,.91),(.68,.40,.24),'white')
   g.sphere('Basin_inner',(-2.58,4.34,1.08),(.52,.29,.045),'aqua')
   b('Basin_back',(-2.58,4.63,1.03),(1.38,.18,.18),'white')
   curved_line(g,'Sink_trap',[(-2.58,4.43,.81),(-2.58,4.43,.52),(-2.36,4.43,.41),(-2.22,4.43,.56),(-2.22,4.82,.60)],.10,'gray')
   curved_line(g,'Tap',[(-2.58,4.60,1.1),(-2.58,4.60,1.38),(-2.58,4.38,1.38),(-2.58,4.38,1.28)],.045,'gray')
   for x in [-2.93,-2.23]:g.cyl('Tap_handle',(x,4.6,1.17),.06,.04,'gray')
   b('Mirror_frame',(-2.58,4.84,2.05),(1.16,.07,1.27),'gray')
   source_patch(g,ROOT/'source/room 024.png',(56,11,85,39),(-2.58,4.79,2.05),(1.07,1.15),'Original_cracked_mirror')
  toilet_before=set(bpy.data.objects)
  # High cistern, pull chain, ceramic bowl and dark seat aperture.
  x,y=-3.48,2.82
  b('High_cistern',(x,y+.14,2.32),(.64,.39,.62),'white');b('Cistern_lid',(x,y+.14,2.65),(.72,.46,.07),'white')
  g.cyl('Flush_pipe',(x,y+.26,1.34),.045,1.32,'gray')
  curved_line(g,'Pull_chain',[(x+.29,y,2.38),(x+.29,y,1.61)],.013,'gray')
  g.sphere('Chain_handle',(x+.29,y,1.57),(.035,.028,.075),'white')
  g.sphere('Toilet_pedestal',(x,y-.18,.28),(.26,.29,.30),'white');g.sphere('Toilet_bowl',(x,y-.22,.56),(.43,.53,.24),'white')
  g.sphere('Seat_rim',(x,y-.26,.76),(.44,.52,.05),'white');g.sphere('Seat_opening',(x,y-.28,.806),(.31,.37,.008),'black')
  bpy.context.view_layer.update()
  toilet_transform=Matrix.Translation((-3.73,2.82,0))@Matrix.Rotation(math.pi/2,4,'Z')@Matrix.Translation((3.48,-2.82,0))
  for o in set(bpy.data.objects)-toilet_before:o.matrix_world=toilet_transform@o.matrix_world
 with offset_group(x=-0.7, y=0):
  # Open tub made from sides and a lowered inner basin, never a filled block.
  x,y=2.29,3.99;w,d=2.87,1.39
  b('Tub_bottom',(x,y,.32),(w-.22,d-.22,.13),'aqua')
  for yy in [y-d/2,y+d/2]:b('Tub_side',(x,yy,.57),(w,.12,.58),'aqua')
  for xx in [x-w/2,x+w/2]:b('Tub_end',(xx,y,.57),(.12,d,.58),'aqua')
  for yy in [y-d/2,y+d/2]:b('Tub_white_rim',(x,yy,.90),(w+.12,.18,.09),'white')
  for xx in [x-w/2,x+w/2]:b('Tub_white_rim',(xx,y,.90),(.18,d,.09),'white')
  for xx in [x-1.1,x+1.1]:
   for yy in [y-.44,y+.44]:g.sphere('Tub_claw_foot',(xx,yy,.18),(.12,.12,.16),'white')
  curved_line(g,'Shower_pipe',[(3.50,4.65,.94),(3.50,4.65,2.94),(2.96,4.65,2.94),(2.96,4.65,2.72)],.046,'gray')
  g.sphere('Shower_head',(2.96,4.65,2.67),(.24,.18,.07),'gray')
  g.beam('Curtain_rod',(.78,3.24,2.95),(3.88,3.24,2.95),.04,'gray')
  for i in range(7):
   xx=.92+i*.115;b('Shower_curtain',(xx,3.25+.028*math.sin(i*2),1.92),(.12,.05,1.91),'lime' if i%2 else 'white')
   g.sphere('Curtain_ring',(xx,3.24,2.94),(.032,.045,.06),'gray')
  source_patch(g,ROOT/'source/room 024.png',(202,16,271,39),(2.83,4.919,2.22),(1.80,.60),'Original_bathroom_graffiti',only={'black'})
  # Opaque right-wall window preserves the reference without exposing another room space.
  b('Bathroom_window_frame',(4.075,4.08,2.01),(.10,1.02,1.41),'brown')
  b('Bathroom_window_glass',(4.011,4.08,2.01),(.025,.85,1.24),'blue')
  for yy in [3.66,4.50]:b('Bathroom_window_jamb',(3.99,yy,2.01),(.06,.045,1.26),'red')
  for z in [1.40,2.62]:b('Bathroom_window_rail',(3.99,4.08,z),(.06,.85,.04),'yellow')
  for yy,z in [(3.91,2.39),(4.30,1.79)]:b('Bathroom_window_star',(3.989,yy,z),(.009,.022,.033),'white')
 # Original missing plaster around the mirror and beside the curtain, flush to the wall.
 for crop,x,z,w,h in [((40,0,55,40),-3.10,2.595,.40,1.04),((147,0,165,48),.31,2.485,.50,1.26)]:
  source_patch(g,ROOT/'source/room 024.png',crop,(x,4.919,z),(w,h),'Bathroom_plaster_damage',only={'aqua','gray','darkgray','lime'})
 finish(c)
