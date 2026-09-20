# Windowed stair hall — room 012

Furnished from [background 012](../../source/room%20012.png): cyan patterned wallpaper, detailed leaded window grids, two red/gold timber columns, a broad-leaf plant beside the stairs, a turned balustrade, the original landscape picture and torn-wallpaper detail. The existing EGA shell palette and soft baked shading are preserved. See [upper-floor layout](../../docs/upper_floor.md) for provisional connections and unresolved exits.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room windowed_hall`. Generated scenes, models and previews live under `generated/`; the browser starts here with `?room=windowed_hall`.

The rear `photo_door` beside the stairs now connects to the [photo darkroom](../photo_room/README.md) on this level, one floor below the bedroom corridor. Its shared leaf starts closed.

The columns, plant pot and balustrade have authored collision footprints. Both door approaches and the full left stair remain clear. The balustrade is a decorative barrier on the existing solid landing; no new floor opening or circulation route is invented. The shell navigation helper supports optional furniture footprints alongside stairs and floor holes.

The furnished optimized model is 831,624 bytes, or 229,284 bytes with gzip. It uses the existing unlit vertex-color material and shared doors.

Validation: static build, typecheck and catalog checks pass, with 17 focused navigation/model checks and four desktop Chrome checks across this level, the photo-door round trip and the upper stair route. No physical-mobile test was run.
