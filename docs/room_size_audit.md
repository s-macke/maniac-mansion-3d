# Room size audit

Reviewed 2026-09-20 against the original backgrounds, authored room geometry and existing generated reference previews. This is a visual proportions audit of all **34 room/area packages**, including the combined entrance/landing and pool/basin. The initial audit was read-only; the size corrections described below have now been implemented.

## Findings and priorities

The following corrections are implemented, retaining the original palette, furniture dimensions and shared door/ladder sizes:

| Room(s) | Before (m) | Now (m) | Change |
|---|---:|---:|---|
| Medical room | 6.4 × 5.55 | 9.6 × 5.55 | Spread desk, anatomy chart and skeleton across the rear; cupboard backs onto the right wall. |
| Mummy bathroom | 8.6 × 5.1 | 7.2 × 4.5 | Move fixtures inward, shorten foreground floor, regenerate tile coverage. |
| Photo room | 8.6 × 5.1 | 7.4 × 4.5 | Move bench inward and reduce empty foreground. |
| Outer laboratory | 12.8 × 5.1 | 10.4 × 5.1 | Narrow the shell so the screen occupies more of the back wall. |
| Radio and heart bedrooms | 9 × 5.1 | 9 × 4.5 | Reduce depth; move rear furniture, ladders and hatch landings together. |
| Green bedroom | 8 × 5.1 | 8 × 4.5 | Reduce depth, retaining the piggy table near the front. |
| Safe attic, Tentacle room, wire attic | 8.6 × 5.2 | 8.6 × 4.5 | Shorten foreground floor; retain hatch clearance and fit long side-wall details. |

Dimensions remain design estimates, **not dimensions recovered from the game**. The arcade retains its recently widened footprint. The subsequent [five-room artwork pass](artwork_review.md) broadens the library spiral, music-room piano and cellar machinery. Pool and garage dimensions remain unchanged.

## How to read the audit

Dimensions below are the authored horizontal X × Y extents in metres, not necessarily “frontage × depth” in the illustrated camera. Most simple rooms have a 3.12 m wall height. The hall, stairs, dome, exterior and pool need separate vertical interpretation: their bounding-box height includes multiple levels, ladders, roofs or underground space and is not a ceiling height.

Source images were compared with the project's 1.2 vertical display correction. Panoramas were kept intact. Perspective, scrolling width and different preview cameras prevent a single pixels-to-metres conversion. Door size, furniture occupancy and the overall long/compact character are better evidence than matching screenshot rectangles. Foreground floor can also look larger solely because of camera position.

- **Keep:** no compelling shell-size mismatch found; not a claim of exact original dimensions.
- **Resize candidate:** a visible mismatch warrants a focused trial.
- **Review:** shell size and furniture scale/camera effects cannot yet be separated confidently.
- **Inferred:** the artwork does not establish the whole traversable volume.

## Complete room review

| Room / source | Current X × Y (m) | Assessment | Reason / next action |
|---|---:|---|---|
| Front exterior / 001, 044, 047 | 26 × 16 | Inferred | Whole facade and approach, not one enclosed room. Keep accepted porch/stair scale; upper facade references do not determine ground depth. |
| Entrance and landing / 010, 011 | 13 × 9.85 outer bounds | Keep | Combined two-level unit, with a 12.8 m interior width and 3.36 m stair rise. Do not judge it as one unusually deep room. Gallery runs from Y 5.7 to 9.75. |
| Living room / 003 | 12.8 × 5.6 | Keep | Broad horizontal composition is appropriate. Furniture bulk is a separate detail issue. |
| Library / 005 | 12.8 × 5.55 | Revised objects | The artwork pass broadens the spiral and restores its solid curved outer stringer; the shell stays unchanged. |
| Kitchen / 007 | 12.8 × 5.55 | Keep | Long counter/appliance arrangement suits the width. Depth remains inferred. |
| Dining room / 037 | 19.2 × 5.55 | Keep | Exceptionally long panorama supports the long room and table arrangement. |
| Pantry / 036 | 6.4 × 5.55 | Review depth | Width reads compact, but foreground circulation feels generous. Check a shallower floor while retaining both exits. |
| Pool deck and basin / 006, 002 | Deck 20 × 11; basin 12.2 × 5.8 | Inferred / review basin depth | Deck proportions are plausible. Basin bottom is 2.8 m below deck; the drained source emphasizes a deep shaft. Current pool previews show the filled state, so a drained first-person comparison is still needed before accepting or changing its vertical scale. |
| Garage and forecourt / 016 | 14 × 8; bay 10 × 7 | Review bay | Total includes the 4 m approach. Car occupies less of the bay than in the artwork; compare car-to-bay scale before shrinking. Preserve cellar ladder clearance. |
| Plant/art room / 014 | 6.4 × 5.55 | Review depth | Compact source arrangement, with generous empty foreground in the model. Width is not the main concern. |
| Music room / 017 | 8 × 3.95 | Revised objects | The artwork pass broadens the piano while preserving its corrected keybed, angle and foreground desk; the shell stays unchanged. |
| Security hall / 013 | 13.2 × 5.55 | Keep | Long corridor/stair arrangement fits. Stair headroom is additional to the ordinary wall height. |
| Medical room / 022 | 9.6 × 5.55 | Revised | Widened shell and redistributed furniture; cupboard faces inward from the right wall. Entry and examination table keep their size. |
| Arcade / 018 | 10.8 × 5.55 | Keep | Recently widened; six cabinets and separate pinball zone now have a long horizontal arrangement. |
| Windowed hall / 012 | 12.8 × 6.1 | Keep | Long hall and staircase need this circulation space. Depth cannot be fixed precisely from the image. |
| Photo room / 023 | 7.4 × 4.5 | Revised | Reduced width/depth and moved the complete bench group inward; equipment remains full size. |
| Upper corridor / 038 | 17 × 4.8 | Keep | Four-door sequence supports length. Do not shorten merely because it is a corridor. |
| Radio bedroom / 021 | 9 × 4.5 | Revised | Shortened depth; rear furnishings, hatch and ladder approach moved together. |
| Heart bedroom / 019 | 9 × 4.5 | Revised | Shortened depth; rear furnishings and ladder moved together, front plant remains in place. |
| Green bedroom / 026 | 8 × 4.5 | Revised | Shortened depth; bed, rear cabinet and window details follow the wall, front piggy table remains in place. |
| Exercise/mummy room / 025 | 10.4 × 5.1 | Keep | Long source supports the equipment and sarcophagus sequence. |
| Mummy bathroom / 024 | 7.2 × 4.5 | Revised | Reduced footprint, repositioned fixtures, fitted tiles and preserved the rear entry. |
| Typewriter/den / 027 | 9 × 5.1 | Review | Fireplace and desk feel small relative to free floor. Separate furniture scale from room size; preserve both concealed passage and hatch access. |
| Hidden attic stairs / inferred from 015 route | 2.4 × 6.1 | Inferred | Purpose-built connecting passage, not a reconstruction of the rectangular room in 015. Judge tread geometry, headroom and portal clearance instead of source-image aspect. |
| Safe attic / 009 | 8.6 × 4.5 | Revised | Reduced depth with hatch and landing shifted together; safe remains forward of the hatch. |
| Tentacle room / 020 | 8.6 × 4.5 | Revised | Reduced depth without shrinking speakers or bed; side panels fit the shorter walls. |
| Wire attic / 015 | 8.6 × 4.5 | Revised | Reduced depth; rear artwork follows wall and roof-edge beams fit the new span. |
| Observatory / 028 | 8.4 m interior diameter | Inferred / keep provisionally | Circular interior, not an 8.76 m square room. Wall height 2.05 m plus dome rise 2.75 m. Telescope and slit are recognizable; single interior view cannot recover diameter exactly. |
| Cellar / 008 | 16.4 × 6.1 | Revised objects | The artwork pass broadens the furnace/cooler group and restores the horizontal return pipes; stairs and shell remain unchanged. |
| Under-house passage / 029 | 24 × 3.5 | Keep | Long low passage matches the source's character; authored height is 2.2 m. Length is an interpretation tied to multiple access points. |
| Dungeon / 004 | 12.8 × 5.1 | Keep provisionally | Broad room matches panorama; skeleton and door treatment affect perceived scale more than an obvious footprint error. |
| Outer laboratory / 031 | 10.4 × 5.1 | Revised | Narrower shell gives the console more prominence without scaling its original screen artwork. |
| Main laboratory / 030 | 16.4 × 5.5 | Keep | Wide apparatus line, vending machine and cabinet suit a long shell. |
| Meteor chamber / 051 | 11.2 × 5.1 | Review objects/depth | Low devices read small and foreground spacious. Do not resize just to compensate for the intentionally absent character; preserve the garage ladder landing. |

## Applying a correction

For subsequent corrections, work one room at a time. Use a matched reference-facing view and a first-person view to distinguish camera effects from actual proportions. Change geometry and furniture placement together where necessary; do not uniformly scale doors, stairs or ladders.

Update authored bounds, obstacle rectangles, ports, hatch/ladder landings, lights and preview cameras with the builder. Keep generated manifests out of authored configs. Independent portal spaces allow a room to grow without fitting a conventional floor-plan box, but shared outdoor areas and connected hall geometry still require physical alignment.

Rebuild only the changed room, synchronize the browser assets, then check both door transitions and walking clearance. The initial audit used existing generated previews and original artwork; the correction pass rebuilds the ten changed rooms and checks their circulation, portal transitions and ladder clearances.

## Correction-pass validation

All ten revised packages were regenerated with Docker/Blender. The static website build, TypeScript check and catalog validation pass. Eighteen focused navigation/model checks pass, covering furniture circulation, door round trips, stairs, real model floors, hatch apertures and physical clearance at upper ladder landings. The wire-attic circulation test keeps its front waypoint inside the entry instead of translating it through the portal.

Fourteen local desktop Chrome checks pass: one walking/render check per changed room, both bedroom ladders up and down, and bathroom/photo doorway round trips. Updated Blender reference renders and all ten browser interior screenshots were inspected. No physical-mobile performance test was run. Changes remain local and uncommitted.
