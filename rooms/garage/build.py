"""Room 016: outdoor forecourt and furnished garage bay."""
import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(OUT))
from interior import furnish
from blender_shared.layout_shell import PALETTE
from room_config import load_config,save_generated,manifest_path
from blender_shared.shell import setup,reference
config=load_config(OUT/'room.json',prepare=True);g=config['geometry']
scene,collections,geo=setup({**PALETTE,'darkgray':(84,84,84)})
box=geo.box;W=g['width'];D=g['depth'];F=g['bayFront'];T=g['wallThickness'];H=g['height'];A=g['bayY0'];B=g['bayY1'];O0=g['openingY0'];O1=g['openingY1'];OH=g['openingHeight']
# Original gray covered floor contrasts with the blue outdoor forecourt. The outside slab meets the pool path at x=0.
box('Forecourt_floor',(F/2,D/2,-.06),(F,D,.12),'lightblue')
holes=g.get('floorHoles',[])
xs=sorted(set([F,W]+[h[k] for h in holes for k in ['x0','x1']]))
ys=sorted(set([A,B]+[h[k] for h in holes for k in ['y0','y1']]))
for x0,x1 in zip(xs,xs[1:]):
 for y0,y1 in zip(ys,ys[1:]):
  if any(h['x0']<(x0+x1)/2<h['x1'] and h['y0']<(y0+y1)/2<h['y1'] for h in holes):continue
  box('Garage_floor',((x0+x1)/2,(y0+y1)/2,-.06),(x1-x0,y1-y0,.12),'darkgray')
box('Garage_threshold',(F+.07,(O0+O1)/2,.003),(.14,O1-O0,.006),'gray')
for h in holes:
 for x in [h['x0'],h['x1']]:box('Hatch_rim',(x,(h['y0']+h['y1'])/2,.025),(.065,h['y1']-h['y0']+.065,.05),'gray')
 for y in [h['y0'],h['y1']]:box('Hatch_rim',((h['x0']+h['x1'])/2,y,.025),(h['x1']-h['x0'],.065,.05),'gray')
for y in [A+T/2,B-T/2]:box('Garage_side',((F+W)/2,y,H/2),(W-F,T,H),'darkgray')
box('Garage_back',(W-T/2,(A+B)/2,H/2),(T,B-A,H),'darkgray')
for a,b in [(A,O0),(O1,B)]:box('Garage_front',(F+T/2,(a+b)/2,H/2),(T,b-a,H),'gray')
box('Garage_header',(F+T/2,(O0+O1)/2,(OH+H)/2),(T,O1-O0,H-OH),'gray')
for y in [O0,O1]:box('Bay_reveal',(F+.07,y,OH/2),(.22,.12,OH),'black')
box('Bay_lintel',(F+.07,(O0+O1)/2,OH),(.22,O1-O0,.12),'black')
# Roof and gable silhouette are inferred from the cutaway artwork.
box('Ceiling_garage',((F+W)/2,(A+B)/2,H+.035),(W-F,B-A,.07),'gray')
ridge=4.75;mid=(A+B)/2
for y in [A-.15,B+.15]:
 geo.mesh('Garage_roof',[(F-.18,y,H+.06),(W+.18,y,H+.06),(W+.18,mid,ridge),(F-.18,mid,ridge)],[(0,1,2,3)] if y<mid else [(3,2,1,0)],'darkgray')
for x in [F,W]:geo.mesh('Garage_gable',[(x,A,H),(x,B,H),(x,mid,ridge)],[(2,1,0)] if x==F else [(0,1,2)],'gray')
# Low curbs make the inferred forecourt limits visible, leaving only the pool path open.
for y in [.13,D-.13]:box('Forecourt_curb',(F/2,y,.12),(F,.26,.24),'darkgray')
port=config['ports'][0];cy=port['position'][1];half=port['width']/2
for a,b in [(0,cy-half),(cy+half,D)]:box('Forecourt_edge',(.13,(a+b)/2,.12),(.26,b-a,.24),'darkgray')
# Close the narrow non-walkable strips beside the garage with matching low boundaries.
for y in [.25,D-.25]:box('Side_plinth',((F+W)/2,y,.06),(W-F,.5,.12),'darkgray')
from blender_shared.ladder_assets import register
register(config,collections['Architecture'])
furnish(geo,ROOT)
reference(ROOT,config,collections,'016')
geo.active='Cameras'
geo.camera('01_Reference',(-6,-3,5.5),(7,4,1.5),lens=28)
geo.camera('02_Inside',(1.2,4,1.62),(10,4,1.6),lens=22)
geo.camera('03_Reverse',(12,4,1.62),(0,4,1.5),lens=22)
scene.camera=bpy.data.objects['02_Inside'];scene['room_id']='016';scene['scope']='Outdoor forecourt, static EGA car, shelving and raised shutter; cellar ladder remains accessible.'
scene.render.resolution_x=1100;scene.render.resolution_y=650
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('GARAGE_SOURCE_COMPLETE',flush=True)

save_generated(config)
