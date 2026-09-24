# Dining room — furnished room v1

Room 037 has red and gold wall panelling, lower vertical slats, the original pixel painting, twin three-globe chandeliers, and a long rounded table with turquoise cloth and scalloped trim. Two high-backed end chairs, three candelabra and two roast platters follow the source artwork. These are static furnishings, not gameplay objects.

## Package and placement

- `build.py` / `room.json`: independent room builder and furnishing recipe and dimensions, ports, shared-door placements and bake settings.
- `generated/blender/dining_room/dining_room_source_v1.blend`: editable furnished scene with packed original reference.
- `generated/blender/dining_room/dining_room_v1.blend`: baked-light preview scene, including shared doors.
- `generated/models/rooms/dining_room_v1.glb`: room-only GLB; doors use the common kit.

The blockout is 19.2 × 5.55 m, with a 3.12 m ceiling. Its length is provisionally 1.5 times the kitchen's, reflecting the longer source panorama. This is a layout-review proportion, not a measured historical floor plan.

Placement: `(-0.82,28.9,0)`, yaw `pi/2`. Its left `kitchen_door` at local `(-9.6,2.9,0)` meets kitchen `dining_door` at world `(-3.72,19.3,0)`, width 1.3 m, height 2.83 m. Kitchen v4 owns the shared interactive leaf, initially closed; dining supplies the matching frame. The room extends straight beyond the kitchen with no level change or overlapping room volume. It keeps the same exterior-facing plane at world x=-6.37.

The far `pantry_door` now connects to the pantry. Dining owns its shared interactive leaf, initially closed and opening into dining.

## Local review and rebuild

Open `http://127.0.0.1:5174/?room=dining_room` to start inside this room within the complete house, or open the kitchen's far door with E / click / touch. The default house start stays outside.

```bash
python3 scripts/rooms.py build dining_room --blender /path/to/blender
python3 scripts/rooms.py bake dining_room --blender /path/to/blender
python3 scripts/build.py check
cd web
npm run build
```

Furniture collision leaves clear aisles along both sides of the table and around the end chairs. The direct room start is beside the kitchen doorway. Door ownership, initial closed state, independent space and facade clearance remain unchanged.

The room builder uses `scripts/blender_shared/shell.py` for scene setup, rectangular walls/floor/ceiling, side doorways, reference markers and the existing right-end door hinge convention. Colors, cameras and door ownership remain explicit in `build.py`; `interior.py` builds furniture and panelling. Dimensions, ports and collision footprints remain in `room.json`.

## Source and generated files

This folder contains the builder, furnishing recipe, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/dining_room/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/dining_room/`; derived door metadata and shading reports in `generated/reports/rooms/dining_room/`. Builders never write derived data back into `room.json`.

## Furnishing validation and download

The furnished optimized GLB is 1,104,980 bytes (277,881 bytes with gzip). The existing unlit vertex-color bake keeps soft shading in the browser without runtime lights. Original painting/stain pixels use color-run geometry; no extra texture download is needed.

The static build, typecheck, catalog check and 15 focused collision, connection and actual-GLB checks pass, including the retained kitchen facade clearance.
Desktop Chrome also renders all three furnished rooms without page errors and walks a clear aisle in each; the resulting screenshots were inspected. No physical-mobile validation was run.

## Artwork detail review — 2026-09-22

The platters distinguish the roast bird from the sliced ham: the bird retains its projecting bone, while the ham has a white fat rim, red cut face and fine white marbling, following background 037.

The shared kitchen/dining leaf is handed to match dining background 037: knob
on the left, hinge on the right from the dining side, opening into the kitchen.
Handle and hinge are mirrored together; the two faces remain physically aligned.
