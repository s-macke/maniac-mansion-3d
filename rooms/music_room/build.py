"""Artwork-based furnished room, retaining the established shared shell and ports."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from blender_shared.layout_shell import build
from interior import furnish
build(Path(__file__).with_name('room.json'),furnish)

# Reverse inspection from the clear front-right aisle, outside the television.
import bpy
from mathutils import Vector
camera=bpy.data.objects['03_Reverse'];camera.location=(3.73,1.5,1.62)
camera.rotation_euler=(Vector((-1.4,2.7,1.1))-camera.location).to_track_quat('-Z','Y').to_euler()
bpy.ops.wm.save_as_mainfile(filepath=bpy.data.filepath)
