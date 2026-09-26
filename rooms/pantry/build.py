"""Room 036: independent colors, cameras and door ownership for the shared shell helpers."""
import bpy,json,sys,math
from pathlib import Path
from mathutils import Matrix
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(OUT))
from interior import furnish
from blender_shared.layout_shell import PALETTE
from room_config import load_config,save_generated,manifest_path
from blender_shared import shell
from blender_shared.door_assets import register,register_static,register_hinged
config=load_config(OUT/'room.json',prepare=True);g=config['geometry']
ports={p['id']:p for p in config['ports']}
colors={'blue':(0,0,168),'pink':(252,84,252),'black':(0,0,0),'brown':(168,84,0),'yellow':(252,252,84),'red':(168,0,0),'gray':(168,168,168),'darkgray':(84,84,84),'white':(252,252,252)}
scene,collections,geo=shell.setup({**PALETTE,'darkgray':(84,84,84)})
shell.build_shell(geo,g,'pantry',floor='darkgray',back='gray',wall='gray',trim='darkgray',closed_right=True)
shell.side_door(geo,g,ports['dining_door'],-1,'Dining_frame',wall='gray',trim='darkgray',frame_only=True)
# Cut the rear wall and skirting at the pool doorway, keeping wall thickness inside pantry.
for name in ['Pantry_back','Back_skirting']:bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
geo.active='Architecture';port=ports['pool_door'];cx=port['position'][0];width=port['width'];dh=port['height'];W=g['halfWidth'];D=g['depth'];H=g['height'];T=g['wallThickness']
for a,b in [(-W,cx-width/2),(cx+width/2,W)]:
 geo.box('Pool_wall',((a+b)/2,D-T/2,H/2),(b-a,T,H),'gray')
 geo.box('Pool_skirting',((a+b)/2,D-T-.018,.13),(b-a,.036,.26),'darkgray')
geo.box('Pool_header',(cx,D-T/2,(H+dh)/2),(width,T,H-dh),'gray')
furnish(geo,ROOT)
from blender_shared.opposite_walls import apply as opposite_walls
opposite_walls(geo,config)
shell.reference(ROOT,config,collections,'036')
geo.active='Cameras'
geo.camera('01_Reference',(0,-8,3.4),(0,3,1.4),lens=27)
geo.camera('02_Inside',(-1.9,1.1,1.62),(-.1,5.4,1.5),lens=22)
geo.camera('03_Reverse',(1.8,4.4,1.62),(-3.2,2.9,1.5),lens=22)
scene.camera=bpy.data.objects['02_Inside'];scene['room_id']='036';scene['version']=Path(config['source']).stem;scene['scope']='Stocked pantry shelf, exposed brick and plaster cracks; shared doors remain operable.'
scene.render.resolution_x=1000;scene.render.resolution_y=650
config['geometry']['doorObstacles']=[]
register(config,[('Dining_frame',ports['dining_door']['width'],ports['dining_door']['height'])])
register_static(config,[('Pool_frame',Matrix.Translation((ports['pool_door']['position'][0],g['depth']-g['wallThickness']-.06,0)),collections['Doors'])])
register_hinged(config,'Pool_leaf',Matrix.Translation((cx,D-T-.06,0)),(cx-width/2,D-T-.06,0),-math.pi/2,collections['Doors'],port='pool_door',node='Door_pool',label='Pool door')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('PANTRY_SOURCE_COMPLETE',flush=True)

save_generated(config)
