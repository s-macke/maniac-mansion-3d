# Upper corridor — room 038

Furnished from [the original background](../../source/room%20038.png), preserving the EGA palette and soft baked shading. Diamond-patterned blue walls, timber wainscot panels, three hanging lamps, a purple floor with bordered rug, corner drapery and three bare decorative branches. The branches have small collision footprints along the front edge; the full rear doorway aisle remains clear.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room upper_corridor`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=upper_corridor`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 435,768 bytes (116,943 bytes with gzip); door and ladder kits are shared separately.
