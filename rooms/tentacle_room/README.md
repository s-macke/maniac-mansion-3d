# Green Tentacle’s music room — room 020

Current footprint: **8.6 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20020.png). Two large solid speaker cabinets with concentric driver cones, blue striped walls and timber panelling, low green bed, hi-fi shelf, and the original tour poster, Disco Sucks sign and Mom portrait. No character or music gameplay is added.

The shared floor hatch returns to the radio bedroom. The left speaker is placed behind and beside the landing, keeping the entire climb path clear.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room tentacle_room`; generated Blender scenes, models and previews stay under `generated/`. Local review: `http://127.0.0.1:5174/?room=tentacle_room`. See [top-floor guide](../../docs/top_floor.md) and [ladder connections](../../docs/ladders.md).

Simple geometry and baked vertex colors preserve the EGA style without runtime lighting. Static furniture uses authored collision footprints; room placements and portal destinations are unchanged.

The optimized room model is 468,368 bytes (119,394 bytes with gzip).


### Artwork detail review

Added the small green/yellow key on the right wall as static scenery. Room connections and navigation footprints are unchanged.
