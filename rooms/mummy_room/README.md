# Mummy room — room 025

Empty shell based on [the original background](../../source/room%20025.png), with shared doors and soft baked shading. Furniture and decorative objects are deferred. See [upper-floor layout](../../docs/upper_floor.md) for provisional connections and unresolved exits.

`build.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room mummy_room`. Generated scenes, models and previews live under `generated/`; the browser starts here with `?room=mummy_room`.

The right-hand `bathroom_door` is now an interactive shared door to the [mummy bathroom](../mummy_bathroom/README.md), closed initially. The corridor places this room fourth from the left.
