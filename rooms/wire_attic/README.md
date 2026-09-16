# Wire attic — room 015

Empty shell based on [the original background](../../source/room%20015.png): cyan wall surfaces and gray floor, with soft baked shading. The damaged plaster, boards, wiring and roof detail are deferred until furnishing. Dimensions and the stair arrival opening are inferred for layout review.

Reach it through the paint-blotched panel on the right wall of the [den/typewriter room](../typewriter_room/README.md), then walk up the [hidden stairs](../attic_stairs/README.md). The [original hint book](https://c64sets.com/maniac_mansion/hint_book.pdf), printed page 39, confirms this route. There is no connection from the mummy bathroom.

Rebuild with `./docker-build.sh room wire_attic`; start directly with `?room=wire_attic`. The panel uses ordinary door controls: E or click/tap, no paint-remover puzzle. Both transitions use seamless doorway portals. No character, puzzle or wire-repair gameplay is included.

Validation: Docker/Blender generation, catalog check, static build and typecheck passed. Focused tests cover the closed panel, shared asset lifecycle, stair movement and exported floor/headroom. A software-rendered Chrome test opened the panel, walked to the attic and back, then closed it without page errors.
