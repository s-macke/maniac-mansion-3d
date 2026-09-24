# Photo room — room 023

Current footprint: **7.4 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [background 023](../../source/room%20023.png), preserving the nearly black room and red/brown fittings. A solid red workbench holds a yellow developing tray and photographic paper beneath an enlarger with bellows, lens and curled cable. A hanging red safelight and broad nine-drawer cabinet complete the scene. All equipment is static. The entrance connects to `windowed_hall` through a seamless doorway portal, with one shared interactive door owned by that room and closed initially.

The right doorway follows the supplied image. This is the photography darkroom, one floor below the bedroom corridor, reached from the rear door beside the windowed-hall stairs.

Dimensions and independent-space placement are provisional. Rebuild with `./docker-build.sh room photo_room`; generated scenes and models remain under `generated/`. Review locally using `?room=photo_room`. See [upper-floor layout](../../docs/upper_floor.md).

`interior.py` supplies the optional shared-shell furnishing callback; `room.json` owns the bench and cabinet footprints. The entrance and central work aisle remain unobstructed. Shading is baked into vertex colors, with no runtime lights or GI; the dark appearance follows the source.

The optimized room model is 143,336 bytes (41,706 bytes with gzip). It uses the existing unlit vertex-color material and shared doors.

Validation: static build, typecheck and catalog checks pass, with 17 focused navigation/model checks and four desktop Chrome checks across this level, the photo-door round trip and the upper stair route. No physical-mobile test was run.

## Artwork refinement

The red safelight glass is visibly lit and a finite downward fixture light is baked onto the workbench. The room retains its nearly black walls and original red/brown palette, with no runtime lights. See the [five-room artwork review](../../docs/artwork_review.md).


## Artwork detail review — 2026-09-24

Restored the second pale enlarger-head band and the small black ventilation slots.
