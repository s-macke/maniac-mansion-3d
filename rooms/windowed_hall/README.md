# Windowed stair hall — room 012

Furnished from [background 012](../../source/room%20012.png): cyan patterned wallpaper, detailed leaded window grids, two red/gold timber columns, a broad-leaf plant beside the stairs, a turned balustrade, the original landscape picture and torn-wallpaper detail. The existing EGA shell palette and soft baked shading are preserved. See [upper-floor layout](../../docs/upper_floor.md) for provisional connections and unresolved exits.

`build.py`, `interior.py` and `room.json` are the authored inputs. Rebuild with `./docker-build.sh room windowed_hall`. Generated scenes, models and previews live under `generated/`; the browser starts here with `?room=windowed_hall`.

The rear `photo_door` beside the stairs now connects to the [photo darkroom](../photo_room/README.md) on this level, one floor below the bedroom corridor. Its shared leaf starts closed.

The columns, plant pot and balustrade have authored collision footprints. Both door approaches and the full left stair remain clear. The upper half of the lower staircase descends 1.68 m through a real floor opening behind the balustrade, from its left end toward the right wall. Its ten treads continue through the right-side `security_door` portal into the lower half in the security corridor. The rail guards the stairwell, rather than bordering a flat aisle. The portal supplies the quarter-turn from the security corridor; no door leaf or frame blocks the stairs. The shell navigation helper supports optional furniture footprints alongside stairs and floor holes.

The furnished optimized model is 1,882,844 bytes, or 589,938 bytes with gzip. It uses the existing unlit vertex-color material and shared doors.

Validation: static build, typecheck and catalog checks pass, with 17 focused navigation/model checks and four desktop Chrome checks across this level, the photo-door round trip and the upper stair route. No physical-mobile test was run.


## Artwork detail review — 2026-09-24

Added the clipped corners of the leaded window panes, completing their octagonal outlines.

Each of the 72 panes now has a shallow convex glass surface inside the leaded
grid, with dark baked shading and small curved green reflections. Recessed black
backing keeps the night-time glass opaque; there is no clear outside view or
transparent rendering. Three soft, low-strength bake sources sit at the windows
and add a restrained light spill into the room. All lighting remains baked into
vertex colors; the browser needs no runtime lights or glass/refraction shader.

The descending security staircase uses the same broad white step faces and
brown wooden nosings as its lower half in the security corridor, including
across the rotated portal.

The inferred opposite wall continues this room’s architectural finish. See the
[complete wall-finish audit](../../docs/opposite_walls.md) for the specific treatment
and the distinction between repeating decoration and unique source details.
