# Plant room — layout shell v1

Original background: 014. This is an empty layout shell with the original EGA wall/floor colors and soft baked shading. Furniture and decorative details are deferred.

Connects through the left landing door, owned by the hall. The overlapping upper facade section is removed so the doorway and room are unobstructed.

The inferred footprint is 6.4 × 5.55 m, with a 3.12 m ceiling. These dimensions and unseen walls are provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, bake settings and current paths. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room plant_room
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/plant_room/plant_room_source_v1.blend` and `generated/blender/plant_room/plant_room_v1.blend`; browser output is `generated/models/rooms/plant_room_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=plant_room.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/plant_room/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/plant_room/`; derived door metadata and shading reports in `generated/reports/rooms/plant_room/`. Builders never write derived data back into `room.json`.
