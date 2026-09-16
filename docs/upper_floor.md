# Upper-floor shell layout

The route continues from the security corridor's existing stairs into **012 windowed stair hall**, then up its left staircase into **038 upper corridor**. The four rear doors now run left to right: purple/radio bedroom with ladder (021), red heart bedroom with ladder (019), green bedroom (026), and exercise/mummy room (025). This order follows the user’s confirmed background identification. The corridor's right door reaches the typewriter room (027).

These are independent room spaces with empty interiors, shared doors and soft baked shading. The stair hall retains three dark framed windows and a usable left stair; bedroom furniture, wallpaper patterns, plants, pictures and decorative fixtures are deferred. All interactive doors start closed. With the two [ladder destination shells](ladders.md), the house has 27 room GLBs plus shared door and ladder kits.

## Interpretation and unresolved exits

The connection drawing supplies the visual basis, with corridor assignments corrected from user feedback. Metric dimensions remain provisional. In particular, the security-stair arrival is represented by an inferred front doorway on the stair hall's right side, where the reference suggests circulation. The rear door beside its stairs now opens into the photo darkroom (023), on the same level at 6.72 m. The top of the left stair leads through a portal to the upper corridor's left entrance.

The windowed hall starts at 6.72 m and the upper corridor/bedroom level at 10.08 m. These are walkthrough elevations derived from two 3.36 m flights, not measurements from the game. Authoring placements deliberately separate the new shells; doorway portals establish their adjacency without requiring exterior cutouts or overlapping geometry.

The exercise/mummy room's far door now opens into the mummy bathroom (024) on the same level at 10.08 m. This is reached through the exercise room, not an extra corridor door. The heart-bedroom and radio-bedroom ladders now lead through hatch portals to the safe attic and Green Tentacle’s room. Other roof rooms and the library spiral stair remain deferred.

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

Each destination has a clear threshold; one shared leaf/frame pair belongs to the owner. Room packages contain only their builder, authored configuration and README. The shell builder supports stairs on either side, optional opaque window panels and per-wall palette colors. Windows do not expose other room spaces.

```bash
./docker-build.sh room windowed_hall
./docker-build.sh room security_hall
./docker-build.sh room upper_corridor
# Repeat for green_bedroom, heart_bedroom, radio_bedroom, mummy_room, typewriter_room.
./docker-build.sh room mummy_bathroom
./docker-build.sh room photo_room
```

Use `?room=windowed_hall` or `?room=upper_corridor` at the local preview URL to review these spaces directly. `web/tests/upper-floor.spec.ts` covers closed doors, crossing/return transforms, both stair flights, actual model floor/headroom, corrected corridor slots and bathroom/photo-room connections.

The [original hint book](https://c64sets.com/maniac_mansion/hint_book.pdf), printed pages 39 and 43, confirms den/typewriter-room access to the wire attic and Edna’s bedroom ladder to the safe attic. There is no bathroom-to-attic connection to implement. The Edna route is now implemented using background 009 as the boarded safe-room reference; its cutaway placement remains tentative. The wire-attic route is implemented: open the painted panel on the den’s right wall, walk through the independent stair passage, then enter the empty wire-attic shell through its upper portal.

## Validation

Docker/Blender generation, catalog validation, static build and typechecking passed. The focused navigation/model/portal checks passed, including both stair flights. A software-rendered Chrome test walked from the windowed hall up into the corridor, opened the green-bedroom door, entered and returned downstairs without page errors. It waits for the swinging doors to finish before advancing. This is desktop browser validation, not a physical-mobile performance test. The rooms use compressed downloads and shared assets; ladder-equipped shells add only their hatch geometry.

The corrected corridor and two side rooms passed 16 focused checks, static build/typechecking, and catalog validation. Chrome walked the stairs to the green bedroom in its third slot and back, then tested separate round trips through the mummy bathroom and photo-room doors. Door approaches leave clearance for the leaf swing.
