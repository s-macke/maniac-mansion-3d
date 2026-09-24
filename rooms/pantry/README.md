# Pantry — furnished room v1

Room 036 follows the original gray wall/floor palette. The independent 6.4 × 5.55 m shell has a 3.12 m ceiling; dimensions are provisional for layout review. A wooden rack holds colored preserves, tins, packets and a top-shelf bottle. Cracked plaster, original exposed-brick pixels and a small patterned mat reproduce the main details of background 036. Supplies remain static.

The left dining doorway uses the shared frame. Dining owns its interactive leaf, which starts closed and swings into dining. The distinctive blue mesh door on the rear wall now opens onto the pool deck. Pantry owns its moving shared leaf; its frame stays fixed. Both faces carry the mesh detail, and the leaf starts closed.

Placement in `house/layout.json` is `(-0.82,41.7,0)`, yaw `pi/2`. The dining threshold is world `(-3.72,38.5,0)`. The shell keeps the kitchen/dining exterior-facing plane at x=-6.37.

`build.py`, `interior.py` and `room.json` generate `generated/blender/pantry/pantry_source_v1.blend`, `generated/blender/pantry/pantry_v1.blend`, current previews and `generated/models/rooms/pantry_v1.glb`. Lighting is baked into vertex colors for the browser.

```bash
python3 scripts/build.py room pantry
python3 scripts/build.py check
./walkthrough.sh build
```

Start at http://127.0.0.1:5174/?room=pantry or walk through dining and open its far door. The central aisle and both door swings remain clear.

The room builder uses `scripts/blender_shared/shell.py` for scene setup, rectangular walls/floor/ceiling, side doorways, reference markers and the existing right-end door hinge convention. Colors, cameras and door ownership remain explicit in `build.py`; `interior.py` builds the fittings. Dimensions, ports and furniture collision footprints remain in `room.json`.

## Source and generated files

This folder contains the builder, furnishing recipe, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/pantry/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/pantry/`; derived door metadata and shading reports in `generated/reports/rooms/pantry/`. Builders never write derived data back into `room.json`.

## Furnishing validation and download

The furnished optimized GLB is 214,804 bytes (56,500 bytes with gzip). The existing vertex-color bake supplies soft shading without runtime global illumination.

Static build, typecheck, catalog validation and 15 focused navigation/GLB checks pass, including furniture collision, clear door thresholds, the pool approach and the garage hatch landing.
Three desktop Chrome checks pass: garage circulation to the hatch, pantry interior movement, and the meteor-chamber/garage ladder round trip. Browser screenshots were inspected, including the simplified title without background numbers. No physical-mobile validation was performed.

## Artwork detail review — 2026-09-22

The shelving has red backing behind the stocked upper bays and a brown lower compartment, matching background 036 rather than exposing the gray room wall through every shelf.
