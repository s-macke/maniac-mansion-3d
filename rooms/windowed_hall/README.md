# Windowed stair hall — room 012

Empty shell based on [the original background](../../source/room%20012.png), with shared doors and soft baked shading. Furniture and decorative objects are deferred. See [upper-floor layout](../../docs/upper_floor.md) for provisional connections and unresolved exits.

`build.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room windowed_hall`. Generated scenes, models and previews live under `generated/`; the browser starts here with `?room=windowed_hall`.

The rear `photo_door` beside the stairs now connects to the [photo darkroom](../photo_room/README.md) on this level, one floor below the bedroom corridor. Its shared leaf starts closed.
