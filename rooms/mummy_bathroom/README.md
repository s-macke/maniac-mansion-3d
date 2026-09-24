# Mummy bathroom — room 024

Current footprint: **7.2 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20024.png), preserving the EGA palette and soft baked shading. Tiled walls and floor, high toilet cistern with pull chain, bowl, wall basin with exposed trap and cracked mirror, an open tub with shower and folded curtain, a recessed side window onto the blue night sky, and original wall graffiti. The rear entry is the only room connection; there is no attic route.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room mummy_bathroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=mummy_bathroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 414,100 bytes (110,394 bytes with gzip).

## Artwork refinement

The toilet and high cistern back onto the left wall and face inward. The original jagged plaster silhouettes are restored above the mirror and beside the curtain. The graffiti sits 1 mm in front of the rear wall instead of floating ahead of it. See the [five-room artwork review](../../docs/artwork_review.md).


The outside windows use `scripts/blender_shared/windows.py`: real openings in
the existing wall slabs, recessed frames and sills, and distant stars against
the original blue night color. Near frames occlude the sky naturally as you
move. The sky is static unlit geometry in this room, not another room connection;
wall collision still prevents walking outside. Doors and furnishings are unchanged.


## Artwork detail review — 2026-09-24

Restored the thin green enamel drip and detached spot beneath the bathtub rim.
