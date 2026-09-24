# Arcade — furnished room v1

Original background: 018. Six solid cabinets preserve the original game-title signs, with dark screens, joysticks, buttons and coin slots. A low pinball table, source poster and wall target complete the room. All machines are static scenery: no playable games have been added.

Connects through the right ordinary door in the security corridor. The corridor owns the moving leaf.

The inferred footprint is 10.8 × 5.55 m, with a 3.12 m ceiling. The longer left-to-right layout follows the artwork: six cabinets spread along the rear wall, with the pinball table at the left end. The front doorway retains its original position and portal connection. Dimensions and unseen walls remain provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, furniture collision footprints, bake settings and current paths. `interior.py` supplies the furnishing callback. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room arcade
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/arcade/arcade_source_v1.blend` and `generated/blender/arcade/arcade_v1.blend`; browser output is `generated/models/rooms/arcade_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=arcade.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains source builders, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/arcade/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/arcade/`; derived door metadata and shading reports in `generated/reports/rooms/arcade/`. Builders never write derived data back into `room.json`.

Furniture leaves the entry, circulation routes and any stair approaches clear. The original EGA palette and existing soft vertex-baked shading require no runtime GI. Rebuild with the existing room command; all Blender scenes, model files and previews remain generated outputs.

Current furnished export: 420,744 bytes optimized, 102,813 bytes gzip. Download size includes furniture and source-art details; the existing shared door kit is cached separately.

Validation: the floor-wide 16 focused navigation/model/portal checks and five desktop Chrome furnishing checks pass, alongside the catalog check, static build and typecheck. Browser screenshots and Blender previews were inspected; physical-mobile performance was not measured.


### Artwork detail review

Added the gray stepped plinth and narrow upper step beneath each arcade cabinet. Room connections and navigation footprints are unchanged.
