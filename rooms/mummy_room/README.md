# Exercise / mummy room — room 025

Furnished from [the original background](../../source/room%20025.png), preserving the EGA palette and soft baked shading. Static blue Egyptian sarcophagus, strength machine with weights and pulleys, low cabinet with original contents, calendar and mummy wall diagram. The central aisle connects both side doors.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room mummy_room`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=mummy_room`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 344,172 bytes (92,566 bytes with gzip); door and ladder kits are shared separately.


### Artwork detail review

Restored the thin black aerial above the sarcophagus, with its three crossbars. Room connections and navigation footprints are unchanged.

## Detailed artwork review — 2026-09-25

Fitted the blue wrapping bands to the curved sarcophagus body and kept the headdress stripes inside its tapered silhouette. Added the exercise machine’s solid pulley, axle hub, pull cable and upper grip. Mounted the calendar and mummy diagram against the rear wall, and brought the cabinet artwork onto its front surface. Furniture bounds, doors and circulation remain unchanged.
