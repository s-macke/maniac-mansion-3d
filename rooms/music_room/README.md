# Music room — furnished room v1

Original background: 017. A slightly angled grand piano with a solid black keybed supporting its keyboard, bench and vase sits among pink wall panels and white pilasters. The gramophone horn, stereo cabinet with a visible cassette and twin reel windows, and blue-screen television preserve the source silhouettes and EGA palette. The foreground wooden desk carries a black vinyl record with grooves and a gray label. Its inferred legs and depth leave a clear aisle behind it. The original wall-paint and blood pixels conform to the layered wall surfaces with a 1 mm offset to avoid flicker. Instruments and equipment are static scenery.

Connects through the right landing door, owned by the hall. Its front wall sits beyond the living-room ceiling footprint to avoid overlap.

The inferred footprint is 8 × 3.95 m, with a 3.12 m ceiling. These dimensions and unseen walls are provisional. Placement and connections live in `house/layout.json`; [the first-floor guide](../../docs/first_floor.md) explains the complete addition.

`room.json` owns dimensions, ports, palette, furniture collision footprints, bake settings and current paths. `interior.py` supplies the furnishing callback. `build.py` calls `scripts/blender_shared/layout_shell.py`, which builds walls around the declared openings and places shared door frames/leaves. The browser assembles the independent room units. Interactive doors start closed; Blender's exported hinge rest pose is open.

```bash
python3 scripts/build.py room music_room
python3 scripts/build.py check
./walkthrough.sh build
```

Current scenes are `generated/blender/music_room/music_room_source_v1.blend` and `generated/blender/music_room/music_room_v1.blend`; browser output is `generated/models/rooms/music_room_v1.glb` with optimized/gzip companions. Start locally at http://127.0.0.1:5174/?room=music_room.

Validation and current download sizes are recorded in [the first-floor guide](../../docs/first_floor.md#validation-and-downloads).

## Source and generated files

This folder contains source builders, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/music_room/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/music_room/`; derived door metadata and shading reports in `generated/reports/rooms/music_room/`. Builders never write derived data back into `room.json`.

Furniture leaves the entry, circulation routes and any stair approaches clear. The original EGA palette and existing soft vertex-baked shading require no runtime GI. Rebuild with the existing room command; all Blender scenes, model files and previews remain generated outputs.

Current furnished export: 361,896 bytes optimized, 105,230 bytes gzip. Download size includes furniture and source-art details; the existing shared door kit is cached separately.

Validation: the floor-wide 16 focused navigation/model/portal checks and five desktop Chrome furnishing checks pass, alongside the catalog check, static build and typecheck. Browser screenshots and Blender previews were inspected; physical-mobile performance was not measured.

## Artwork refinement

The piano composition is wider while retaining its height, depth, slight rotation and solid keybed. The piano, stereo and television are redistributed to preserve the entry clearance and front aisle. The CRT uses the original rounded rectangular glass pixels, including the corner highlights, instead of an oval approximation. See the [five-room artwork review](../../docs/artwork_review.md).


## Artwork detail review — 2026-09-24

Added the pedal lyre, crossbar and three pedals beneath the keyboard, following the existing piano rotation.


## Deeper artwork review

The piano has a smoother curved tail with the accepted width, angle, supported keys and pedals. The lower wall now has black-outlined white panels. The gramophone has a flared outer horn, recessed red lining and dark throat; its purple record has a yellow label, spindle and supported tonearm. The vase has a blue foot and open neck. The reverse review camera now stands clear of the television. Existing baked illumination remains unchanged.

Remaining: pilaster capitals and turned piano legs are simplified, and the keyboard uses a reduced key count. Equipment depth and the unseen walls remain inferred from the single background.

The inferred opposite wall continues this room’s architectural finish. See the
[complete wall-finish audit](../../docs/opposite_walls.md) for the specific treatment
and the distinction between repeating decoration and unique source details.
