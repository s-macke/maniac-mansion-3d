# Security corridor — layout shell v1

Original background: 013. This is an empty layout shell with the original EGA wall/floor colors and soft baked shading. Furniture and decorative details are deferred.

Connects through the reinforced landing door, owned by the hall. Owns the medical and arcade doors. The staircase rises another 3.36 m to the initially closed `higher_floor` door, now owned here and connected to the [windowed stair hall](../windowed_hall/README.md).

The inferred footprint is 13.2 × 5.55 m, with a 3.12 m ceiling. These dimensions and unseen walls are provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, bake settings and current paths. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room security_hall
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/security_hall/security_hall_source_v1.blend` and `generated/blender/security_hall/security_hall_v1.blend`; browser output is `generated/models/rooms/security_hall_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=security_hall.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/security_hall/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/security_hall/`; derived door metadata and shading reports in `generated/reports/rooms/security_hall/`. Builders never write derived data back into `room.json`.
