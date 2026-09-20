"""Place authored furniture groups without scaling their geometry or shared assets."""
from contextlib import contextmanager
from functools import wraps
import bpy
from mathutils import Matrix


@contextmanager
def offset_group(x=0, y=0, z=0):
    """Translate only objects created in this block, including world-space meshes."""
    before = set(bpy.data.objects)
    yield
    bpy.context.view_layer.update()
    transform = Matrix.Translation((x, y, z))
    for obj in set(bpy.data.objects) - before:
        obj.matrix_world = transform @ obj.matrix_world


def rear_anchored(authored_depth):
    """Keep a furnishing composition at a fixed distance from the rear wall.

    Shell, doors, windows and ladders are built separately from current config.
    Furnishings retain their physical dimensions; only their location changes.
    """
    def decorate(furnish):
        @wraps(furnish)
        def placed(geo, config):
            with offset_group(y=config['geometry']['depth'] - authored_depth):
                furnish(geo, config)
        return placed
    return decorate
