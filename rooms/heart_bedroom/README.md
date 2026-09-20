# Heart bedroom — room 019

Furnished from [the original background](../../source/room%20019.png), preserving the EGA palette and soft baked shading. Red heart wallpaper, vanity with cracked aqua mirror and bottles, curtained red bed, potted plant, hanging light and original Edna portrait. The right-side ladder and its landing remain accessible.

The existing shared ladder and ceiling hatch retain their continuous portal connection to the safe attic. Furniture stays outside the approach, shaft and landing.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room heart_bedroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=heart_bedroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 355,608 bytes (96,710 bytes with gzip); door and ladder kits are shared separately.
