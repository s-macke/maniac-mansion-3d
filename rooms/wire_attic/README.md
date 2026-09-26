# Wire attic — room 015

Current footprint: **8.6 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20015.png). Original jagged plaster, cracks, damp streaks and exposed laths separated into shallow depth layers; solid angled yellow boards over the dark window recess; projecting loose wire ends and a hanging fitting. The floor and left wall use the source’s dark gray.

The front portal leads to the hidden attic stairs, then the den’s painted panel. There is no new floor hatch or additional route. The damaged window remains opaque; the room does not reveal unrelated spaces.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room wire_attic`; generated Blender scenes, models and previews stay under `generated/`. Local review: `http://127.0.0.1:5174/?room=wire_attic`. See [top-floor guide](../../docs/top_floor.md) and [ladder connections](../../docs/ladders.md).

Simple geometry and baked vertex colors preserve the EGA style without runtime lighting. Static furniture uses authored collision footprints; room placements and portal destinations are unchanged.

The optimized room model is 509,012 bytes (175,464 bytes with gzip).


### Artwork detail review

Made the exposed bulb visibly bright and added soft local baked light beneath its actual position. Room connections and navigation footprints are unchanged.

## Detailed source review — 2026-09-25

Replaced the regular window-board ladder with irregular overlapping planks of varied lengths, angles and chipped outlines, with attached nail heads. Tilted the blue lamp fitting and added its socket and pull cord. Restored the black floor outline as static scenery without assigning it a destination or interaction. Removed the unsupported brown skirting color.
