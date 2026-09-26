# Safe attic — room 009

Current footprint: **8.6 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20009.png). A complete floor-to-ceiling gray boarded wall with nails and turquoise weathering, cracked side walls, a recessed open star window, hanging bulb and the original portrait on a closed safe case. The boards and black backing meet both corners and the ceiling without exposed gaps. The portrait and safe are static furnishings. The blue circular telescope-view overlay in background 009 is excluded, following the established reference interpretation.

The shared floor hatch returns to the heart bedroom. The safe sits forward of the hatch, leaving its shaft and landing clear.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room safe_attic`; generated Blender scenes, models and previews stay under `generated/`. Local review: `http://127.0.0.1:5174/?room=safe_attic`. See [top-floor guide](../../docs/top_floor.md) and [ladder connections](../../docs/ladders.md).

The visible bulb supplies local, soft baked illumination; the floor beneath it is brighter than the distant corners. Simple geometry and baked vertex colors preserve the EGA style without runtime lighting. Static furniture uses authored collision footprints; room placements and portal destinations are unchanged.

The rear wall follows the original staggered plank ends, with varied lengths, small chipped edges, blue seam edges and paired nail holes. Turquoise weathering is traced from the original pixels, including its winding upper trail and dense lower patches, rather than randomly scattered. The circular overlay remains excluded.


The left wall has a real window aperture, deep jambs, crossbar and sill. A small
static star field sits well beyond the wall inside an enclosed black sky volume.
The frame naturally occludes the distant stars as the viewer moves. The sky is
part of this room package, uses unlit EGA colors, and adds no room connection,
walkable exterior, transparent sorting or runtime lighting. Navigation still
blocks walking through the outside wall. The original window placement and
ladder route are preserved.

At the user’s request, the opposite wall carries the same boarded treatment, rotated into the room with mirrored plank joints and a separate turquoise weathering pattern: a tall stain, isolated low patches and a small upper patch. This unseen wall is an inferred continuation of background 009; the window, safe and hatch are unchanged.
