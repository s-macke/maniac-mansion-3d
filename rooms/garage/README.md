# Garage and forecourt — layout shell v1

Room 016 shows an outdoor forecourt leading into a covered garage bay. This package keeps that distinction: an open-air approach from the pool, a wide open vehicle entrance, gray walls, blue floor and a simple pitched roof. The car, shelving, shutter mechanism and decorative detail are deferred.

The provisional unit is 14 × 8 m. The forecourt occupies the first 4 m; the covered bay is 10 × 7 m with a 3.3 m eave height and 4.75 m ridge. The entrance is 4.8 × 2.95 m. Roof shape follows the cutaway; unseen dimensions and gray roof finish are inferred. There is no new interactive door leaf in this pass.

The pool fence has a 2.6 m path opening at pool-local `(20,5.2,0)`. It meets garage `pool_path` local `(0,4,0)` at world `(-26.37,38.9,0)`. Garage placement is `(-26.37,42.9,0)`, yaw `pi`. The exact fence opening and path alignment are provisional, based on the suggested pool/garage relationship.

`build.py` uses shared scene setup but owns the outdoor approach and garage geometry. `room.json` owns dimensions, ports and bake settings. Current outputs are `generated/blender/garage/garage_source_v1.blend`, `generated/blender/garage/garage_v1.blend`, `generated/previews/rooms/garage/` and `generated/models/rooms/garage_v1.glb` with compact/gzip companions.

```bash
python3 scripts/build.py room garage
python3 scripts/build.py check
./walkthrough.sh build
```

Start at http://127.0.0.1:5174/?room=garage or follow the opening at the far end of the pool deck. The path and bay stay at the same floor elevation. Perimeter curbs and garage walls remain solid boundaries.

Validation: 15 focused navigation, shared-door and actual-GLB checks pass, plus gzip download verification for all nine assets. Static build and typecheck pass. Blender shell and assembled connection previews were inspected; no physical-mobile performance measurement was run. The optimized garage is 118,624 bytes / 36,411 bytes gzip. `scripts/preview_garage.py` regenerates the assembled views.

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/garage/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/garage/`; derived door metadata and shading reports in `generated/reports/rooms/garage/`. Builders never write derived data back into `room.json`.
