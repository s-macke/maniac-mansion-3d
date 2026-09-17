# Typewriter room — room 027

Empty shell based on [the original background](../../source/room%20027.png), with shared doors and soft baked shading. Furniture and decorative objects are deferred. See [upper-floor layout](../../docs/upper_floor.md) for provisional connections and unresolved exits.

`build.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room typewriter_room`. Generated scenes, models and previews live under `generated/`; the browser starts here with `?room=typewriter_room`.

The paint blotch on the right wall is now a shared `Concealed_leaf` panel. It starts closed and opens with E or click/tap, revealing the [hidden stairs](../attic_stairs/README.md) up to the [wire attic](../wire_attic/README.md). The patch uses pixels from background 027; it has no conventional door frame or handle. The plant-to-ceiling route remains deferred.

The ceiling hatch above the right-hand blue pot now connects to the [observatory](../observatory/README.md). A shared ladder makes that route usable during the shell stage; it is independent of the painted-panel attic stairs.

The temporary den ladder faces the back wall beneath the visible ceiling opening above the right-hand blue pot, beside the painted wall (local X 3.1, Y 4.52). Its ceiling opening and the observatory ladder align through the portal; the painted-panel door remains on the right wall.
