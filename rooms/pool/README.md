# Pool deck — outdoor unit v1

Room 006 is an independent outdoor builder. It recreates the stone deck, turquoise coping, blue filled pool, metal ladder, pink floating chair silhouette, teal/yellow fence and sparse night backdrop using the original EGA palette and baked lighting. No indoor shell template is used.

The provisional deck is 20 × 11 m; the pool opening is 12.2 × 5.8 m. The deck stays at the pantry floor elevation for continuous exploration. The near curb and unseen dimensions are inferred. The far fence opening now connects to the garage forecourt; the around-house connection is deferred.

The pantry owns the shared blue mesh door. Its leaf now separates from the fixed frame, has detail on both faces and starts closed. Open it with E / click / touch to step onto the deck. Pool placement is `(-6.37,44.1,0)`, yaw `pi`; its `pantry_door` meets the pantry rear port at world `(-6.37,40.9,0)`.

You can walk around the deck. Water, ladder and the fenced perimeter remain solid boundaries except at the garage path opening. This pass follows the filled-pool state in room 006; the drained basin shown in room 002 and ladder descent are deferred. There is no draining or swimming gameplay.

`build.py` / `room.json` own the geometry, dimensions, ports and lighting. Outputs are `generated/blender/pool/pool_source_v1.blend`, `generated/blender/pool/pool_v1.blend`, `generated/previews/rooms/pool/` and `generated/models/rooms/pool_v1.glb` with compact/gzip companions.

```bash
python3 scripts/build.py room pool
python3 scripts/build.py check
./walkthrough.sh build
```

Start locally at http://127.0.0.1:5174/?room=pool or walk through the pantry. No hosting or commits are part of this change.

The optimized pool GLB is 598,004 bytes / 169,186 bytes gzip. Sixteen focused navigation, door and shared-library checks pass, including a complete deck circuit, blocked water/fences and both sides of the pantry threshold. Room and assembled doorway previews were inspected in Blender; no physical-mobile performance test was run. `scripts/preview_pool.py` reproduces the assembled open/closed views.

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/pool/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/pool/`; derived door metadata and shading reports in `generated/reports/rooms/pool/`. Builders never write derived data back into `room.json`.
