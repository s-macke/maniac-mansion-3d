# Safe attic — room 009

Current footprint: **8.6 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20009.png). Gray boarded wall with nails and turquoise weathering, cracked side walls, a small opaque star window, hanging bulb and the original portrait on a closed safe case. The portrait and safe are static furnishings. The blue circular telescope-view overlay in background 009 is excluded, following the established reference interpretation.

The shared floor hatch returns to the heart bedroom. The safe sits forward of the hatch, leaving its shaft and landing clear.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room safe_attic`; generated Blender scenes, models and previews stay under `generated/`. Local review: `http://127.0.0.1:5174/?room=safe_attic`. See [top-floor guide](../../docs/top_floor.md) and [ladder connections](../../docs/ladders.md).

Simple geometry and baked vertex colors preserve the EGA style without runtime lighting. Static furniture uses authored collision footprints; room placements and portal destinations are unchanged.

The optimized room model is 286,780 bytes (76,903 bytes with gzip).
