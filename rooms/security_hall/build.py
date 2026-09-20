"""Artwork-based furnished room, retaining the established shared shell and ports."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
sys.path.insert(0,str(Path(__file__).resolve().parent))
from blender_shared.layout_shell import build
from interior import furnish
build(Path(__file__).with_name('room.json'),furnish)
