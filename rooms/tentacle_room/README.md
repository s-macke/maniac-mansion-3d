# Green Tentacle’s music room — room 020

Furnished from [the original background](../../source/room%20020.png). Two large solid speaker cabinets with concentric driver cones, blue striped walls and timber panelling, low green bed, hi-fi shelf, and the original tour poster, Disco Sucks sign and Mom portrait. No character or music gameplay is added.

The shared floor hatch returns to the radio bedroom. The left speaker is placed behind and beside the landing, keeping the entire climb path clear.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room tentacle_room`; generated Blender scenes, models and previews stay under `generated/`. Local review: `http://127.0.0.1:5174/?room=tentacle_room`. See [top-floor guide](../../docs/top_floor.md) and [ladder connections](../../docs/ladders.md).

Simple geometry and baked vertex colors preserve the EGA style without runtime lighting. Static furniture uses authored collision footprints; existing room placements and portals are unchanged.

The optimized model is 464,340 bytes (118,759 bytes with gzip); ladder geometry is shared separately.
