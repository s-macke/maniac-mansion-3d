# Typewriter room — room 027

Empty shell based on [the original background](../../source/room%20027.png), with shared doors and soft baked shading. Furniture and decorative objects are deferred. See [upper-floor layout](../../docs/upper_floor.md) for provisional connections and unresolved exits.

`build.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room typewriter_room`. Generated scenes, models and previews live under `generated/`; the browser starts here with `?room=typewriter_room`.

The paint blotch on the right wall is now a shared `Concealed_leaf` panel. It starts closed and opens with E or click/tap, revealing the [hidden stairs](../attic_stairs/README.md) up to the [wire attic](../wire_attic/README.md). The patch uses pixels from background 027; it has no conventional door frame or handle. The plant-to-ceiling route remains deferred.
