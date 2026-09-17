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

The furnished optimized GLB is 747,548 bytes (196,329 bytes with gzip). The existing unlit vertex-color bake keeps soft shading in the browser without runtime lights. Books, shelving and the spiral staircase use solid EGA geometry with no texture download.

The static build, typecheck, catalog check and 15 focused collision, connection and actual-GLB checks pass, including the retained kitchen facade clearance.
Desktop Chrome also renders all three furnished rooms without page errors and walks a clear aisle in each; the resulting screenshots were inspected. No physical-mobile validation was run.
