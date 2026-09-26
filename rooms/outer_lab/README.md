# Outer laboratory

Current footprint: **10.4 × 5.1 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [background 031](../../source/room%20031.png): the big green screen with its original pixel diagram, console, cooling fins, cyan pipes, keypad and articulated arm. This is the first laboratory after the skeleton dungeon, before the three-apparatus main laboratory (030). Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room outer_lab --site`; start locally at `/?room=outer_lab`.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.

## Artwork detail review — 2026-09-22

The two console instruments match background 031: a split pink/aqua dial beside a black-faced dial with a pink rim, each with separate ticks, needle and hub.

## Door orientation

The dungeon entrance is on the back-left wall; the gray main-lab exit is on the right. Metal panels leave the entrance aperture open.

The shared dungeon/outer-lab doorway is 1.95 m wide, matching the broader reinforced left door in background 004. Both room apertures agree; its destination and closed-first interaction are unchanged.

## Detailed laboratory review — 2026-09-26

Added the tall gray manipulator guide, upper articulated linkage, joint axles, side handle and lower aqua reader. The console now has diagonal base vents, panel screws and its left cable. The wall-panel cutout derives from the authored dungeon port width, keeping the full 1.95 m opening clear. The keypad and its collision footprint fit entirely beside that opening.

The opposite wall also uses the matching light-blue metal panels, blue seams and black rivets, continued across its full width at the user’s request. This inferred wall has no copied doorway or machinery.
