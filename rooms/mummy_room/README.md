# Exercise / mummy room — room 025

Furnished from [the original background](../../source/room%20025.png), preserving the EGA palette and soft baked shading. Static blue Egyptian sarcophagus, strength machine with weights and pulleys, low cabinet with original contents, calendar and mummy wall diagram. The central aisle connects both side doors.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room mummy_room`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=mummy_room`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 297,092 bytes (76,798 bytes with gzip); door and ladder kits are shared separately.
