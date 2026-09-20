# Mummy bathroom — room 024

Furnished from [the original background](../../source/room%20024.png), preserving the EGA palette and soft baked shading. Tiled walls and floor, high toilet cistern with pull chain, bowl, wall basin with exposed trap and cracked mirror, an open tub with shower and folded curtain, an opaque side window, and original wall graffiti. The rear entry is the only room connection; there is no attic route.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room mummy_bathroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=mummy_bathroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 408,252 bytes (104,763 bytes with gzip); door and ladder kits are shared separately.
