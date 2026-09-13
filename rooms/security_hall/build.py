"""Room 013 layout shell; artwork details deferred."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from blender_shared.layout_shell import build
build(Path(__file__).with_name('room.json'))
