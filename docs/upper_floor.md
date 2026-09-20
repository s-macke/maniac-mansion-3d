# Upper-floor layout and interiors

The radio/heart bedrooms now measure 9 × 4.5 m and the green bedroom 8 × 4.5 m. The photo room is 7.4 × 4.5 m and the mummy bathroom 7.2 × 4.5 m. Rear fixtures, collision bounds, ports and bedroom ladder endpoints follow the reduced depth; front furnishings retain their placement. See the [room size audit](room_size_audit.md).

The route continues from the security corridor's existing stairs into **012 windowed stair hall**, then up its left staircase into **038 upper corridor**. The four rear doors now run left to right: purple/radio bedroom with ladder (021), red heart bedroom with ladder (019), green bedroom (026), and exercise/mummy room (025). This order follows the user’s confirmed background identification. The corridor's right door reaches the typewriter room (027).

These are independent room spaces with shared doors and soft baked shading. The windowed stair hall and photo darkroom at 6.72 m are now furnished from backgrounds 012 and 023. The hall includes patterned walls, leaded windows, timber posts, a plant, balustrade and original wall picture; the darkroom includes the bench, enlarger, trays, safelight and paper cabinet. The bedroom level at 10.08 m is also furnished: upper corridor, radio bedroom, heart bedroom, green bedroom, exercise/mummy room, mummy bathroom and typewriter den. All interactive doors start closed. With the two [ladder destination rooms](ladders.md), the house has 34 room GLBs plus shared door and ladder kits.

## Interpretation and unresolved exits

The connection drawing supplies the visual basis, with corridor assignments corrected from user feedback. Metric dimensions remain provisional. In particular, the security-stair arrival is represented by an inferred front doorway on the stair hall's right side, where the reference suggests circulation. The rear door beside its stairs now opens into the photo darkroom (023), on the same level at 6.72 m. The top of the left stair leads through a portal to the upper corridor's left entrance.

The windowed hall starts at 6.72 m and the upper corridor/bedroom level at 10.08 m. These are walkthrough elevations derived from two 3.36 m flights, not measurements from the game. Authoring placements deliberately separate the new shells; doorway portals establish their adjacency without requiring exterior cutouts or overlapping geometry.

The exercise/mummy room's far door now opens into the mummy bathroom (024) on the same level at 10.08 m. This is reached through the exercise room, not an extra corridor door. The heart-bedroom and radio-bedroom ladders now lead through hatch portals to the safe attic and Green Tentacle’s room. The four [top-floor rooms](top_floor.md) are furnished. The library spiral stair destination remains unresolved.

## Ownership and reproduction

| Connection | Moving door owner |
|---|---|
| Security corridor → windowed hall | Security corridor `higher_floor` |
| Windowed hall → upper corridor | Windowed hall `higher_floor` |
| Upper corridor → four bedrooms | Upper corridor, one door per bedroom |
| Upper corridor → typewriter room | Upper corridor `typewriter_door` |
| Typewriter room → hidden attic stairs | Typewriter room `hidden_panel` |
| Hidden attic stairs → wire attic | Open portal, no door leaf |
| Exercise/mummy room → mummy bathroom | Mummy room `bathroom_door` |
| Windowed stair hall → photo room | Windowed hall `photo_door` |

Furniture footprints preserve both stair routes, every door approach and all three bedroom-level ladder landings. Each destination has a clear threshold; one shared leaf/frame pair belongs to the owner. Room packages contain source builders and furnishing recipes, authored configuration and README. The shell builder supports stairs on either side, optional opaque window panels and per-wall palette colors. Windows do not expose other room spaces.

```bash
./docker-build.sh room windowed_hall
./docker-build.sh room security_hall
./docker-build.sh room upper_corridor
# Repeat for green_bedroom, heart_bedroom, radio_bedroom, mummy_room, typewriter_room.
./docker-build.sh room mummy_bathroom
./docker-build.sh room photo_room
```

Use `?room=windowed_hall` or `?room=upper_corridor` at the local preview URL to review these spaces directly. `web/tests/upper-floor.spec.ts` covers closed doors, crossing/return transforms, both stair flights, actual model floor/headroom, corrected corridor slots and bathroom/photo-room connections.

The [original hint book](https://c64sets.com/maniac_mansion/hint_book.pdf), printed pages 39 and 43, confirms den/typewriter-room access to the wire attic and Edna’s bedroom ladder to the safe attic. There is no bathroom-to-attic connection to implement. The Edna route is now implemented using background 009 as the boarded safe-room reference; its cutaway placement remains tentative. The wire-attic route is implemented: open the painted panel on the den’s right wall, walk through the independent stair passage, then enter the furnished wire attic through its upper portal.

## Validation

Docker/Blender generation, catalog validation, static build and typechecking passed. The focused navigation/model/portal checks passed, including both stair flights. A software-rendered Chrome test walked from the windowed hall up into the corridor, opened the green-bedroom door, entered and returned downstairs without page errors. It waits for the swinging doors to finish before advancing. This is desktop browser validation, not a physical-mobile performance test. The rooms use compressed downloads and shared assets; ladder-equipped shells add only their hatch geometry.

The corrected corridor and two side rooms passed 16 focused checks, static build/typechecking, and catalog validation. Chrome walked the stairs to the green bedroom in its third slot and back, then tested separate round trips through the mummy bathroom and photo-room doors. Door approaches leave clearance for the leaf swing.

### Furnished windowed-hall level

The static build, typecheck, catalog and 17 navigation/model checks pass with the furnished hall and darkroom. Four desktop Chrome checks cover their interiors, the photo-door round trip, and ascending to the bedroom corridor then returning down the windowed stairs. Reference renders and browser screenshots were inspected. The shared palette was also checked against all original backgrounds for an exact 16-color match. Physical-mobile performance was not measured.

## Furnished bedroom level

The seven room-local `interior.py` recipes use the existing shell callback. Shared small furniture forms live in `scripts/blender_shared/bedroom_furniture.py`; each room owns its composition, original-art crops and collision footprints. The corridor retains its four rear doors in the confirmed order. Beds, vanity, radio console, exercise machine, bathroom fixtures and den furnishings leave continuous walking routes. Lamps use the static bake; there are no new runtime lights or gameplay. The den pot is offset beside the ladder to preserve its usable approach.

Validation of the furnished bedroom level: Docker/Blender generation, catalog checks, static build and typecheck pass. Fifteen focused navigation/model tests cover furniture clearance, doors, stairs and hatch geometry. Thirteen desktop Chrome tests cover all seven interiors, both bedroom ladders, the observatory ladder, bathroom door, upper staircase and concealed attic passage. Reference renders and browser views were inspected. No physical-mobile performance test was run. The seven room models total about 737 KB with gzip, excluding shared door and ladder kits.
