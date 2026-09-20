# Wire attic — room 015

Furnished from [the original background](../../source/room%20015.png). Original jagged plaster, cracks, damp streaks and exposed laths separated into shallow depth layers; solid angled yellow boards over the dark window recess; projecting loose wire ends and a hanging fitting. The floor and left wall use the source’s dark gray.

The front portal leads to the hidden attic stairs, then the den’s painted panel. There is no new floor hatch or additional route. The damaged window remains opaque; the room does not reveal unrelated spaces.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room wire_attic`; generated Blender scenes, models and previews stay under `generated/`. Local review: `http://127.0.0.1:5174/?room=wire_attic`. See [top-floor guide](../../docs/top_floor.md) and [ladder connections](../../docs/ladders.md).

Simple geometry and baked vertex colors preserve the EGA style without runtime lighting. Static furniture uses authored collision footprints; existing room placements and portals are unchanged.

The optimized model is 427,620 bytes (122,445 bytes with gzip); ladder geometry is shared separately.
