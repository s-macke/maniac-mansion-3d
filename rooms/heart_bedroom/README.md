# Heart bedroom — room 019

Current footprint: **9 × 4.5 m**, retained from the [room size audit](../../docs/room_size_audit.md). The original [background 019](../../source/room%20019.png) remains the visual basis, with the EGA palette and soft baked shading.

The detailed artwork pass restores the large staggered heart pattern, dark red ceiling cornice, layered base rails and bedroom-side door surround. The vanity is narrower than the bed, with three separate front panels, short feet, a blue flower vase and a pink/white telephone. Its arched aqua mirror carries the original branching crack pixels. The longer red bed has its heart pillow at the right head end, a brown footboard with rounded ends, and a pleated curtain pair facing into the room. The rear-wall portrait has a thick yellow frame and purple inner border. A small foreground bedside cupboard carries the decorative yellow key visible in the source; it has no gameplay function.

The compact black ceiling fixture has two aqua shades and white glints. Local fixture illumination is baked into vertex colors; no runtime lights or global illumination are required. The portrait is backed against the wall; the mirror is supported over the vanity rather than treated as a wall decal.

The existing shared ladder and ceiling hatch retain their continuous portal connection to the safe attic. The bedside cupboard sits forward and left of the approach. Furniture collision bounds follow the revised proportions. Door/hatch positions, room dimensions, destinations and shared ownership are unchanged; interactive doors start closed.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room heart_bedroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=heart_bedroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 416,100 bytes (133,602 bytes with gzip); shared doors and ladders remain separate.
