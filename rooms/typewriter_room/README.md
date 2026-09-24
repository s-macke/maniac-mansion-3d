# Typewriter den — room 027

Furnished from [the original background](../../source/room%20027.png), preserving the EGA palette and soft baked shading. Patterned wallpaper, wood panels, solid stone fireplace with a dark recess, original family portrait, typewriter and table, left plant, empty blue pot and bordered rug. The right pot stands beside the existing ladder approach so it does not block the observatory route.

The right painted wall panel remains a shared `Concealed_leaf`, initially closed. It opens into the hidden attic stairs leading to the wire attic. The separate ceiling hatch and shared ladder still lead to the observatory; their existing transforms are unchanged.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room typewriter_room`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=typewriter_room`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 659,332 bytes (147,046 bytes with gzip); door and ladder kits are shared separately.


### Artwork detail review

Replaced generic rectangular fireplace decoration with the original irregular stone faces and colored flecks, mounted on the solid piers and lintel. Room connections and navigation footprints are unchanged.
