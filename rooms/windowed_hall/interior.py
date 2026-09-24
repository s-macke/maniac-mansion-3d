"""Background 012: patterned landing, leaded windows, columns and stair plant."""
from pathlib import Path
import math,bpy
from mathutils import Matrix
from blender_shared.furnishings import source_patch,panel,curved_line
ROOT=Path(__file__).resolve().parents[2]

def furnish(geo,c):
 b=geo.box;g=c['geometry'];windows=c['shell']['windows'];ports=[p for p in c['ports'] if p['id']=='photo_door']
 # Small repeated cyan motifs on the existing rear wall, leaving all openings clear.
 vs=[];fs=[]
 def quad(x,z,dx,dz):
  n=len(vs);vs.extend([(x-dx,5.907,z-dz),(x+dx,5.907,z-dz),(x+dx,5.907,z+dz),(x-dx,5.907,z+dz)]);fs.append((n,n+1,n+2,n+3))
 for ix in range(46):
  x=-4.35+ix*.225
  for iz in range(12):
   z=.37+iz*.225
   if any(abs(x-p['position'][0])<p['width']/2+.15 and z<p['height']+.14 for p in ports):continue
   if any(abs(x-w['x'])<w['width']/2+.16 and abs(z-w['z'])<w['height']/2+.16 for w in windows):continue
   quad(x,z,.016,.09);quad(x,z,.09,.016)
   for dx,dz in [(-.052,-.052),(-.052,.052),(.052,-.052),(.052,.052)]:quad(x+dx,z+dz,.018,.018)
 geo.mesh('Cyan_wallpaper_motifs',vs,fs,'aqua')
 # Replace the shell's coarse bars with the reference's dense leaded grid.
 for o in list(bpy.data.objects):
  if o.name.startswith(('Window_mullion','Window_crossbar')):bpy.data.objects.remove(o,do_unlink=True)
 for win in windows:
  x,z,w,h=[win[k] for k in ['x','z','width','height']];y=5.737
  for j in range(5):b('Window_lead_vertical',(x-w/2+j*w/4,y,z),(.028,.038,h),'gray')
  for j in range(7):b('Window_lead_horizontal',(x,y,z-h/2+j*h/6),(w,.038,.025),'gray')
  for i in range(4):
   for j in range(6):
    xx=x-w/2+(i+.2)*w/4;zz=z-h/2+(j+.77)*h/6
    # Clipped leaded corners give each pane its octagonal source outline.
    left=x-w/2+i*w/4;bottom=z-h/2+j*h/6
    for sx in [-1,1]:
     for sz in [-1,1]:
      cx=left+(w/4 if sx==1 else 0);cz=bottom+(h/6 if sz==1 else 0)
      geo.beam('Pane_corner_lead',(cx-sx*.043,y-.008,cz),(cx,y-.008,cz-sz*.043),.018,'gray')
    b('Pane_green_glint',(xx,y+.015,zz),(.04,.008,.018),'green')
  for xx in [x-w/2-.055,x+w/2+.055]:b('Window_red_frame',(xx,5.76,z),(.032,.035,h+.12),'red')
 # Two tall timber columns, based on the foreground posts in the original.
 for x in [-3.75,.85]:
  b('Timber_column',(x,3.05,1.56),(.25,.28,3.12),'brown')
  b('Column_red_inset',(x,2.898,1.59),(.14,.025,2.97),'red')
  for dx in [-.092,.092]:b('Column_gold_edge',(x+dx,2.876,1.59),(.025,.025,2.98),'yellow')
  for z in [.08,3.02]:b('Column_foot_cap',(x,3.05,z),(.43,.43,.14),'brown')
 # Potted broad-leaf plant beside the left stair, clear of its walking width.
 px,py=-4.04,4.63
 geo.cyl('Plant_pot',(px,py,.28),.30,.52,'red',16);geo.cyl('Pot_rim',(px,py,.54),.35,.09,'lightred',16);geo.cyl('Pot_soil',(px,py,.59),.29,.025,'brown',16)
 geo.beam('Plant_trunk',(px,py,.59),(px+.05,py,1.98),.055,'brown')
 for i in range(12):
  a=i*2.4;z=.88+i*.096;end=(px+.46*math.cos(a),py+.35*math.sin(a),z+.15)
  geo.beam('Plant_branch',(px,py,z-.10),end,.025,'green')
  tip=(end[0]+.14*math.cos(a),end[1]+.12*math.sin(a),end[2]+.13)
  perp=(-.12*math.sin(a),.12*math.cos(a),.035)
  root=(px+.13*math.cos(a),py+.1*math.sin(a),z-.08)
  verts=[root,(end[0]+perp[0],end[1]+perp[1],end[2]+perp[2]),tip,(end[0]-perp[0],end[1]-perp[1],end[2]-perp[2]),(end[0],end[1],end[2]+.045)]
  geo.mesh('Broad_plant_leaf',verts,[(0,1,4),(1,2,4),(2,3,4),(3,0,4),(4,1,0),(4,2,1),(4,3,2),(4,0,3)],'green')
  geo.beam('Leaf_rib',root,tip,.016,'lime')
 # Original balustrade as a solid railing; no new floor hole or invented stair route.
 for z in [.10,1.04]:b('Landing_balustrade_rail',(4.38,4.75,z),(3.02,.14,.10),'brown')
 b('Balustrade_gold_top',(4.38,4.745,1.11),(3.05,.16,.025),'yellow')
 for i in range(12):
  x=2.95+i*.258
  geo.cyl('Balustrade_spindle',(x,4.75,.57),.039,.89,'red',8)
  for z in [.28,.79]:geo.sphere('Spindle_turning',(x,4.75,z),(.057,.057,.055),'brown')
 # Add the red/gold stair trim and upright balusters without changing tread heights.
 st=g['stairs']
 for i in range(st['segments']):
  y=st['y0']+(st['y1']-st['y0'])*i/st['segments'];z=st['rise']*(i+1)/st['segments']
  b('Stair_red_riser',((st['x0']+st['x1'])/2,y+.007,z-.04),(st['x1']-st['x0'],.018,.04),'red')
  if i%2==0:geo.beam('Stair_baluster',(st['x1'],y,z),(st['x1'],y,z+.72),.035,'brown')
 # Preserve the original mountain picture on the right wall.
 before=set(geo.collections[geo.active].objects)
 panel(geo,'Landscape_frame',0,0,2.20,1.08,1.15)
 source_patch(geo,ROOT/'source/room 012.png',(570,35,609,76),(0,-.08,2.20),(.89,.94),'Original_landscape')
 bpy.context.view_layer.update()
 transform=Matrix.Translation((6.17,3.5,0))@Matrix.Rotation(-math.pi/2,4,'Z')
 for obj in set(geo.collections[geo.active].objects)-before:obj.matrix_world=transform@obj.matrix_world
 source_patch(geo,ROOT/'source/room 012.png',(439,9,474,47),(3.12,5.906,2.63),(.53,.58),'Torn_wallpaper',only={'gray','darkgray','black','aqua','cyan'})
 for obj in list(bpy.data.objects):
  if obj.name.startswith('Wall_front'):obj.name='Front_inferred_windowed_hall'
