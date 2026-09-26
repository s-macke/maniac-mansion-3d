# Opposite-wall finish audit

All 51 supplied PNG backgrounds were reviewed for this pass, including alternate
views, close-ups and ending screens. The unseen front walls are inferred: they
continue the room's architectural finish, not its furniture, windows, doors,
portraits, signs or baked pools of light. Worn plaster and timber use different
damage/grain layouts rather than mirroring recognizable stains.

## Added finish continuation

| Room | Reference | Finish continued onto the opposite wall |
|---|---|---|
| Empty pool basin | 002 | Aqua/white tile band and blue depth seams on the opposite basin wall |
| Living room | 003 | Narrow black/gold stripes and colored trim |
| Kitchen | 007 | Red and gold patterned tile skirting |
| Cellar | 008 | Gray plaster and construction seams |
| Windowed hall | 012 | Aqua cross-and-dot wallpaper, clipped at the entrance |
| Security hall | 013 | Fine blue/gray wallpaper and colored rails, clipped at the entrance |
| Wire attic | 015 | Cyan plaster, irregular exposed timber laths and different damp streaks; entrance remains open |
| Music room | 017 | Pink inset panels, white pilasters and paneled dado |
| Heart bedroom | 019 | Staggered heart wallpaper, cornice and base rails |
| Tentacle room | 020 | Blue pinstripes and timber wainscot |
| Mummy bathroom | 024 | Aqua lower wall tiles and cyan specks, supplementing its existing opposite-wall plaster patches |
| Mummy/exercise room | 025 | Brown wainscot with red/yellow rails |
| Typewriter den | 027 | Repeated original wallpaper and complete lower timber panels |
| Under-house passage | 029 | Horizontal timber boards with independently distributed damp grain |
| Pantry | 036 | Gray plaster with differently positioned ragged brick exposures |
| Dining room | 037 | Upper inset panels, narrow lower slats and rails |
| Upper corridor | 038 | Blue diamond lattice and timber panels; the original lamp-light patches stay beside their lamps |

## Already covered or no transferable finish

These account for the other 17 room units in the current house.

| Room | Reference | Audit result |
|---|---|---|
| Connected hall | 010, 011 | Existing front-wall stripes and wainscot on both levels |
| Dungeon | 004 | Existing opposite-wall irregular stonework |
| Safe attic | 009 | Existing boards and deliberately different damp clusters |
| Outer lab | 030 | Existing opposite-wall metal panels and cyan/light-blue marks |
| Main lab | 031 | Existing opposite-wall metal panels and cyan/light-blue marks |
| Meteor chamber | 051 | Existing opposite-wall metal panels and cyan/light-blue marks |
| Library | 005 | Shelves and cupboard fronts belong to the bookcase, not a repeating wall finish |
| Plant room | 014 | Plain painted wall; props and fixture light stay in place |
| Garage | 016 | Plain walls and open forecourt; no new front enclosure |
| Arcade | 018 | Plain painted wall; posters and machines are individual objects |
| Radio bedroom | 021 | Plain painted wall; no duplicated radio, poster or ladder |
| Medical room | 022 | Plain plaster with localized damage; no repeated board, crack or lamp |
| Photo room | 023 | Plain dark walls; photographic equipment stays in place |
| Green bedroom | 026 | Plain green walls; window and decorations stay in place |
| Observatory | 028 | Continuous curved dome already surrounds the room; preserve its open slit |
| Attic stairs | Inferred connection | No independent supplied wall pattern to extend |
| Front exterior | 001 and exterior views | Outdoor facade and porch; no enclosing opposite wall |

The remaining images (032–035, 040–050 and 052) provide telescope views, exterior
views, close-ups, UI or ending scenes rather than additional modeled interiors.
There is no supplied 039 background.

## Implementation and verification

`scripts/blender_shared/opposite_walls.py` owns this finish continuation. The common
layout shell calls it after furnishing and room-depth placement; the four custom
builders (living room, kitchen, dining room and pantry) call it explicitly.
The pool’s basin finish stays in its own interior builder because its walls lie
below deck level and share the existing drain/refill visibility handling.

Only whitelisted seamless architectural meshes are copied. Other finishes are
batched by material, use the existing EGA palette, and are clipped to front door
apertures. Added surfaces have the `Front_inferred_` prefix so the reference
cutaway still hides them. Lighting remains baked, with no browser lights or new
navigation geometry. Generated scenes, previews and browser assets remain under
the existing ignored output paths.

Validation for this pass: all 17 affected areas were rebuilt and their opposite
walls inspected in Blender renders. Scene checks passed for front-surface
alignment and doorway clearance in the 16 enclosed rooms, plus matching tile
sizes/colors and two depth seams in the basin. The house catalog, TypeScript
check, production website build and five portal regression tests passed.
Chrome walkthrough checks passed for the security hall, windowed hall and wire
attic; the pool test drained the pool, walked the basin, climbed out and refilled
it. This is desktop browser validation, not physical-mobile testing.

The generated visual overview is
`generated/previews/opposite-wall-audit.png`; individual views are in
`generated/previews/rooms/<room>/opposite-wall-review.png`.
