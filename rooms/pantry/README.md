# Pantry — empty shell v1

Room 036 follows the original gray wall/floor palette. The independent 6.4 × 5.55 m shell has a 3.12 m ceiling; dimensions are provisional for layout review. Shelves, supplies, wall cracks and exposed brick detail are deferred.

The left dining doorway uses the shared frame. Dining owns its interactive leaf, which starts closed and swings into dining. The distinctive blue mesh door on the rear wall now opens onto the pool deck. Pantry owns its moving shared leaf; its frame stays fixed. Both faces carry the mesh detail, and the leaf starts closed.

Placement in `house/layout.json` is `(-0.82,41.7,0)`, yaw `pi/2`. The dining threshold is world `(-3.72,38.5,0)`. The shell keeps the kitchen/dining exterior-facing plane at x=-6.37.

`build.py` and `room.json` generate `generated/blender/pantry/pantry_source_v1.blend`, `generated/blender/pantry/pantry_v1.blend`, current previews and `generated/models/rooms/pantry_v1.glb`. Lighting is baked into vertex colors for the browser.

```bash
python3 scripts/build.py room pantry
python3 scripts/build.py check
./walkthrough.sh build
```

Start at http://127.0.0.1:5174/?room=pantry or walk through dining and open its far door. Nothing is published or committed.

Validation: 13 focused navigation, door and shared-asset tests pass, plus the download check for all seven assets. Typecheck and static build pass. Blender room and assembled open/closed previews were inspected; no physical-mobile test was run. The optimized pantry is 165,832 bytes, or 45,818 bytes gzip. Assembled views can be regenerated with `scripts/preview_pantry.py`.

The room builder uses `scripts/blender_shared/shell.py` for scene setup, rectangular walls/floor/ceiling, side doorways, reference markers and the existing right-end door hinge convention. Colors, cameras, door ownership and special assets remain explicit in this room’s `build.py`; dimensions and ports remain in `room.json`.

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/pantry/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/pantry/`; derived door metadata and shading reports in `generated/reports/rooms/pantry/`. Builders never write derived data back into `room.json`.
