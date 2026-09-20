# Medical room — furnished room v1

Current footprint: **9.6 × 5.55 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Original background: 022. The room contains a drawer desk with green lamp, the original chalkboard/certificates and anatomy poster, an examination table, red-cross medicine cupboard against the right wall with its doors facing into the room, and static teaching skeleton. The chalkboard face is 3.0 × 1.25 m, surrounded by a complete four-sided wooden frame; the upper-left plaster crack uses the original broad jagged silhouette, flush with the wall. The skeleton is a display prop, with no animation or character behavior.

Connects through the left ordinary door in the security corridor. The corridor owns the moving leaf.

The inferred footprint is 9.6 × 5.55 m, with a 3.12 m ceiling. These dimensions and unseen walls are provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, furniture collision footprints, bake settings and current paths. `interior.py` supplies the furnishing callback. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room medical_room
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/medical_room/medical_room_source_v1.blend` and `generated/blender/medical_room/medical_room_v1.blend`; browser output is `generated/models/rooms/medical_room_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=medical_room.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains source builders, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/medical_room/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/medical_room/`; derived door metadata and shading reports in `generated/reports/rooms/medical_room/`. Builders never write derived data back into `room.json`.

Furniture leaves the entry, circulation routes and any stair approaches clear. The original EGA palette and existing soft vertex-baked shading require no runtime GI. Rebuild with the existing room command; all Blender scenes, model files and previews remain generated outputs.

Current furnished export: 369,516 bytes optimized, 96,003 bytes gzip. Download size includes furniture and source-art details; the existing shared door kit is cached separately.

Validation: the floor-wide 16 focused navigation/model/portal checks and five desktop Chrome furnishing checks pass, alongside the catalog check, static build and typecheck. Browser screenshots and Blender previews were inspected; physical-mobile performance was not measured.

The green desk lamp is visibly switched on: bright EGA green glass and a yellow underside accompany a soft downward fixture light baked onto the desktop. `bake.practicalLights` supplies its position, range and cone; `fillStrength` gently reduces the otherwise uniform fill. There are no browser lights, bloom or runtime GI.

The cupboard/frame/crack/lamp correction passes the static build, typecheck, catalog check, furnished-room circulation test, exported lamp-color check and local Chrome walking/render check. Blender and browser views were inspected; the lamp test verifies brighter nearby desktop vertices, bounded colors and absence of runtime light extensions.
