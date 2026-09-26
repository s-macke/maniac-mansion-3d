"""Room 007: independent colors, cameras and door ownership for the shared shell helpers."""
import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(OUT))
from room_config import load_config,save_generated,manifest_path
from blender_shared import shell
from blender_shared.layout_shell import PALETTE
from interior import furnish
from blender_shared.door_assets import register
config=load_config(OUT/'room.json',prepare=True);g=config['geometry']
ports={p['id']:p for p in config['ports']}
colors={'blue':(0,0,168),'lightblue':(84,84,252),'black':(0,0,0),'brown':(168,84,0),'yellow':(252,252,84),'red':(168,0,0),'gray':(168,168,168)}
scene,collections,geo=shell.setup(PALETTE)
shell.build_shell(geo,g,'kitchen',floor='blue',back='lightblue',wall='blue',trim='brown',closed_right=False)
shell.side_door(geo,g,ports['hall_door'],-1,'Hall_frame',wall='blue',trim='brown',frame_only=True)
shell.side_door(geo,g,ports['dining_door'],1,'Dining_door',wall='blue',trim='brown',frame_only=False)
furnish(geo,ROOT)
from blender_shared.opposite_walls import apply as opposite_walls
opposite_walls(geo,config)
shell.reference(ROOT,config,collections,'007')
geo.active='Cameras'
geo.camera('01_Reference',(0,-9,3.4),(0,3,1.4),lens=27)
geo.camera('02_Inside',(-4.5,1.25,1.62),(5,3.15,1.5),lens=22)
geo.camera('03_Reverse',(4.5,3.8,1.62),(-6.4,2.9,1.5),lens=22)
scene.camera=bpy.data.objects['02_Inside'];scene['room_id']='007';scene['version']=Path(config['source']).stem;scene['scope']='Furnished interior based on original artwork, with shared interactive doors.'
scene.render.resolution_x=1000;scene.render.resolution_y=650
shell.interactive_side_door(config,collections,ports['dining_door'],'Dining_door','Door_dining','Dining room door',reverse_hinge=True)
register(config,[('Hall_frame',ports['hall_door']['width'],ports['hall_door']['height']),('Dining_door',ports['dining_door']['width'],ports['dining_door']['height'])])
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('KITCHEN_SOURCE_COMPLETE',flush=True)

save_generated(config)
