"""Room 037: independent colors, cameras and door ownership for the shared shell helpers."""
import bpy,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'scripts'))
from room_config import load_config,save_generated,manifest_path
from blender_shared import shell
from blender_shared.door_assets import register
config=load_config(OUT/'room.json',prepare=True);g=config['geometry']
ports={p['id']:p for p in config['ports']}
colors={'blue':(0,0,168),'pink':(252,84,252),'black':(0,0,0),'brown':(168,84,0),'yellow':(252,252,84),'red':(168,0,0),'gray':(168,168,168)}
scene,collections,geo=shell.setup(colors)
shell.build_shell(geo,g,'dining_room',floor='pink',back='red',wall='red',trim='brown',closed_right=False)
shell.side_door(geo,g,ports['kitchen_door'],-1,'Kitchen_frame',wall='red',trim='brown',frame_only=True)
shell.side_door(geo,g,ports['pantry_door'],1,'Pantry_door',wall='red',trim='brown',frame_only=False)
shell.reference(ROOT,config,collections,'037')
geo.active='Cameras'
geo.camera('01_Reference',(0,-14,4.2),(0,3,1.4),lens=27)
geo.camera('02_Inside',(-7.5,1.25,1.62),(8.5,3.15,1.5),lens=22)
geo.camera('03_Reverse',(7.5,3.8,1.62),(-9.6,2.9,1.5),lens=22)
scene.camera=bpy.data.objects['02_Inside'];scene['room_id']='037';scene['version']=Path(config['source']).stem;scene['scope']='Empty shell and doors; furnishings and windows deferred for layout review.'
scene.render.resolution_x=1000;scene.render.resolution_y=650
shell.interactive_side_door(config,collections,ports['pantry_door'],'Pantry_door','Door_pantry','Pantry door')
register(config,[('Kitchen_frame',ports['kitchen_door']['width'],ports['kitchen_door']['height']),('Pantry_door',ports['pantry_door']['width'],ports['pantry_door']['height'])])
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/config['source']))
print('DINING_ROOM_SOURCE_COMPLETE',flush=True)

save_generated(config)
