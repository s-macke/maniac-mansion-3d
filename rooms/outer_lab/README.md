# Outer laboratory

Current footprint: **10.4 × 5.1 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [background 031](../../source/room%20031.png): the big green screen with its original pixel diagram, console, cooling fins, cyan pipes, keypad and articulated arm. This is the first laboratory after the skeleton dungeon, before the three-apparatus main laboratory (030). Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room outer_lab --site`; start locally at `/?room=outer_lab`.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.
