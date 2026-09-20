# Landing-floor interiors and layout

The medical room is now 9.6 × 5.55 m, with its desk and wall art spread across the longer back wall and its cupboard facing inward from the right wall. See the [room size audit](room_size_audit.md).

The first floor means the storey immediately above the ground floor, at 3.36 m. Its existing landing remains part of the connected hall. Six independent room packages are added: the ground-floor library plus five rooms upstairs. This first-floor milestone introduced 14 room GLBs and one shared door kit; see [upper-floor layout](upper_floor.md) for the current extension. The browser combines them using `house/layout.json`; Blender files remain independently editable and reproducible.

| Room | Background | Access | Moving door owner |
|---|---|---|---|
| Library | 005 | Living-room double doors | Living room |
| Art studio (`plant_room`) | 014 | Left landing door | Hall |
| Music room | 017 | Right landing door | Hall |
| Security corridor | 013 | Reinforced landing door | Hall |
| Medical room | 022 | Left ordinary corridor door | Security corridor |
| Arcade | 018 | Right ordinary corridor door | Security corridor |

The five rooms immediately above the entrance are now furnished from backgrounds 014, 017, 013, 022 and 018: art studio, music room, security corridor, medical room and arcade. Their original EGA colors, shared doors and baked soft shading are preserved. The former “Plant room” label is corrected to “Art studio”; its package ID and query URL remain `plant_room`. The ground-floor library now has bookcases, a reading corner and a decorative spiral staircase. No gameplay, characters or runtime global illumination are added. Every interactive door starts closed and opens/closes from either side. The reinforced door retains its pixel artwork on both faces and now has a separate reusable leaf and frame.

Walk up the main staircase to reach the new floor. The corridor staircase rises a further 3.36 m and now connects through an initially closed shared door to the [windowed stair hall and upper-floor shells](upper_floor.md). The library spiral stair's destination remains unresolved in the supplied connection drawing, so it is modelled as a non-traversable visual feature without an assigned destination.

Connections follow the supplied cutaway and backgrounds. Footprints, unseen walls and metric dimensions are inferred. The 8 × 3.95 m music room clears the living-room ceiling and the corridor stairwell; the art-studio doorway connects through its own independent room space. The 13.2 m-wide security corridor clears the art-studio wing. The exterior keeps its complete facade and continuous canopy in a separate space; neither needs a cutout for the art-studio wing. The medical room and arcade have independent portal spaces; the widened arcade overlaps the medical room’s map footprint without sharing its rendered or navigable interior. These decisions can be adjusted as the rest of the house is mapped.

`rooms/<id>/room.json` stores dimensions and wall-port declarations in `shell.entries`. `scripts/blender_shared/layout_shell.py` creates the simple shell, openings, trim, shared doors and optional corridor staircase. Individual navigation adapters enforce floor elevation, walls, furniture footprints and stair support. Each of these five builders adds its own `interior.py` callback to the common shell. The existing furnished rooms retain their own builders.

Local starting links: `?room=library`, `plant_room`, `music_room`, `security_hall`, `medical_room` and `arcade`. The normal exterior start is unchanged.

## Validation and downloads

Docker/Blender builds, catalog validation, static compilation and typecheck pass. Sixteen focused navigation, model, portal and shared-asset checks pass. Five desktop Chrome checks walk a clear aisle in each furnished room without page errors; their screenshots and Blender reference renders were inspected. This does not constitute physical-mobile validation.

The current furnished-room checks cover furniture collision and circulation, both sides of each shared doorway, the main stairs, the corridor stair headroom, actual model floor elevations and the retained independent room spaces. Rebuild the complete five-room group with the standard room commands; no authored door transforms or room placements changed.

| Furnished package | Optimized GLB | Gzip download |
|---|---:|---:|
| Art studio (`plant_room`) | 240,736 B | 62,830 B |
| Music room | 325,712 B | 92,805 B |
| Security corridor | 1,092,024 B | 236,355 B |
| Medical room | 369,516 B | 96,003 B |
| Arcade | 403,404 B | 98,227 B |

Current standalone previews are generated with each room build under `generated/previews/rooms/<id>/`. The assembly images from `scripts/preview_first_floor.py` document the earlier shell milestone and are not the furnished-room reference views.

The arcade now uses a 10.8 × 5.55 m footprint to reflect background 018’s long horizontal layout. Its six cabinets spread across the rear wall and the pinball table occupies the left end; its existing front-door portal remains fixed.
