# Upper corridor — room 038

Furnished from [the original background](../../source/room%20038.png), preserving the EGA palette and soft baked shading. Diamond-patterned blue walls, timber wainscot panels, three twin black bell-shade lamps with white undersides, a purple floor with bordered rug, solid timber corner piers with red-and-gold chamfered edges, and three bare decorative branches. Brown side walls carry returning wainscot rails. The left entrance has a red surround and the original devil-face ornament, reproduced directly from background 038 pixels; its moving door remains owned by the windowed stair hall. Local soft light from the three visible fixtures is baked into the room. Flush original pixel color runs also preserve the cyan/blue illuminated wallpaper beneath the lamps; multiplying a pure-blue material by white light alone cannot reproduce that source color change. There are no runtime lights. The branches have small collision footprints along the front edge; the full rear doorway aisle remains clear.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room upper_corridor`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=upper_corridor`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 840,672 bytes (202,786 bytes with gzip); door and ladder kits are shared separately.
