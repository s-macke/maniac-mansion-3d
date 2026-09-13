"""Compatibility entry point; the hall builder now lives with its room package."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().parents[1]/'rooms/connected_hall/build.py'),run_name='__main__')
