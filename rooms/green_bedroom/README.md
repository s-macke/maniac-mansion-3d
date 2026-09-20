# Green bedroom — room 026

Furnished from [the original background](../../source/room%20026.png), preserving the EGA palette and soft baked shading. Green/red patterned bedspread and an open metal bed frame, hanging model aircraft, original blueprint and pennant, hamster enclosure and a solid pink piggy bank on its low table. The rear corridor door has an open approach.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room green_bedroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=green_bedroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 475,164 bytes (119,946 bytes with gzip); door and ladder kits are shared separately.
