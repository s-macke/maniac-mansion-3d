# Library — furnished room v1

Original background: 005. Rear bookcases contain three rows of EGA-colored books above panelled cupboards. A brown spiral staircase, black reading chair, green telephone on its side table and two floor lamps reproduce the main reference features with solid geometry and soft baked shading.

Connects through the living-room double doors, owned by the living room. The spiral staircase is a non-traversable visual feature: its destination remains unresolved, and no new connection is invented. Furniture collision leaves circulation across the front and around the reading corner.

The inferred footprint is 12.8 × 5.55 m, with a 3.12 m ceiling. These dimensions and unseen walls are provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, bake settings and current paths. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves; the library supplies an optional furnishing callback. Authored `geometry.obstacles` describes furniture footprints. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room library
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/library/library_source_v1.blend` and `generated/blender/library/library_v1.blend`; browser output is `generated/models/rooms/library_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=library.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/library/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/library/`; derived door metadata and shading reports in `generated/reports/rooms/library/`. Builders never write derived data back into `room.json`.

## Furnishing validation and download

The furnished optimized GLB is 865,160 bytes (243,368 bytes with gzip). The existing unlit vertex-color bake keeps soft shading in the browser without runtime lights. Books, shelving and the spiral staircase use solid EGA geometry with no texture download.

The static build, typecheck, catalog check and 15 focused collision, connection and actual-GLB checks pass, including the retained kitchen facade clearance.
Desktop Chrome also renders all three furnished rooms without page errors and walks a clear aisle in each; the resulting screenshots were inspected. No physical-mobile validation was run.

## Artwork refinement

The spiral now has a 1.45 m tread radius and a broad curved outer stringer. A complete top rail caps the bookcases; the telephone receiver is green. The two reading lamps have bright bulb geometry and local upward/backward illumination baked onto nearby surfaces. See the [five-room artwork review](../../docs/artwork_review.md).


## Artwork detail review — 2026-09-24

Restored the spreading green plant in its low red/yellow pot on the middle bookshelf, clearing only its book bay.


## Deeper artwork review

The reading chair has rounded upholstered edges and thin gray seam piping. The green telephone now has a curved receiver, earpieces, rotary dial and coiled lead. Both fit the existing furniture footprints. The lamp stems now match the original black; their two light bakes and the accepted bookcase/stair proportions remain in use. The reverse Blender review camera now stands in the clear right aisle rather than inside the bookcase.

Remaining: book spacing and spine patterns are an approximation rather than a pixel-for-pixel arrangement. The spiral stair destination and unseen room depth remain unresolved; no new route has been invented.

## Hanging stair sign

The lower spiral rail carries the small white sign shown in background 005.
Its face reproduces source pixels (308,86)–(322,93), preserving the unreadable
lettering and gray edge. A thin board and two hanging wires attach it to the
rail; it introduces no interaction or new stair destination.

Validation: library rebuild, production site and catalog checks pass. The
updated desktop Chrome library walkthrough passes; the sign close-up and
Blender reference view were inspected.
