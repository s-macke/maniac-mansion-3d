# Library — layout shell v1

Original background: 005. This is an empty layout shell with the original EGA wall/floor colors and soft baked shading. Furniture and decorative details are deferred.

Connects through the living-room double doors, owned by the living room. The spiral stair visible in the reference is deferred until its destination is resolved; this shell does not invent that connection.

The inferred footprint is 12.8 × 5.55 m, with a 3.12 m ceiling. These dimensions and unseen walls are provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, bake settings and current paths. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room library
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/library/library_source_v1.blend` and `generated/blender/library/library_v1.blend`; browser output is `generated/models/rooms/library_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=library.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/library/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/library/`; derived door metadata and shading reports in `generated/reports/rooms/library/`. Builders never write derived data back into `room.json`.
