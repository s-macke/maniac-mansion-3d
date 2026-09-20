# Garage and forecourt — furnished room v1

Room 016 shows an outdoor forecourt leading into a covered garage bay. This package keeps that distinction: an open-air approach from the pool, a wide open vehicle entrance, gray walls, blue floor and a simple pitched roof. The covered bay now contains the static red-and-turquoise car from background 016, with real wheels, window panels, rear fins, circular taillight housings, chrome trim and the original EDSEL rear plate. The rear/trunk faces the forecourt, matching the source; the nose points into the bay. A sparse storage rack and raised shutter slats/tracks complete the garage fixtures. The shutter remains open and the car is not drivable.

The provisional unit is 14 × 8 m. The forecourt occupies the first 4 m; the covered bay is 10 × 7 m with a 3.3 m eave height and 4.75 m ridge. The entrance is 4.8 × 2.95 m. Roof shape follows the cutaway; unseen dimensions and gray roof finish are inferred. There is no new interactive door leaf in this pass.

The pool fence has a 2.6 m path opening at pool-local `(20,5.2,0)`. It meets garage `pool_path` local `(0,4,0)` at world `(-26.37,38.9,0)`. Garage placement is `(-26.37,42.9,0)`, yaw `pi`. The exact fence opening and path alignment are provisional, based on the suggested pool/garage relationship.

`build.py` uses shared scene setup but owns the outdoor approach and garage geometry; `interior.py` builds the car and fixtures. Authored `geometry.obstacles` blocks their footprints. `room.json` owns dimensions, ports and bake settings. Current outputs are `generated/blender/garage/garage_source_v1.blend`, `generated/blender/garage/garage_v1.blend`, `generated/previews/rooms/garage/` and `generated/models/rooms/garage_v1.glb` with compact/gzip companions.

```bash
python3 scripts/build.py room garage
python3 scripts/build.py check
./walkthrough.sh build
```

Start at http://127.0.0.1:5174/?room=garage or follow the opening at the far end of the pool deck. The path and bay stay at the same floor elevation. Perimeter curbs and garage walls remain solid boundaries.

Walk along the clear aisle beside the car to reach the hatch landing at garage-local `(12,2.9)`. The parked car changes circulation inside the bay; the pool path, vehicle threshold and ladder portal keep their existing positions.

## Source and generated files

This folder contains the builder, furnishing recipe, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/garage/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/garage/`; derived door metadata and shading reports in `generated/reports/rooms/garage/`. Builders never write derived data back into `room.json`.

A shared ladder now links the meteor chamber to a real floor hatch inside the garage. This user-requested shortcut replaces the old meteor-chamber exit door and the original long passage. Use E/click/tap to climb in either direction. Ordinary walking cannot fall through the garage hatch.

## Furnishing validation and download

The furnished optimized GLB is 262,316 bytes (76,617 bytes with gzip). The existing vertex-color bake supplies soft shading without runtime global illumination.

Static build, typecheck, catalog validation and 15 focused navigation/GLB checks pass, including furniture collision, clear door thresholds, the pool approach and the garage hatch landing.
Three desktop Chrome checks pass: garage circulation to the hatch, pantry interior movement, and the meteor-chamber/garage ladder round trip. Browser screenshots were inspected, including the simplified title without background numbers. No physical-mobile validation was performed.
