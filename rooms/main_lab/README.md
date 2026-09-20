# Main laboratory

Furnished from [background 030](../../source/room%20030.png). Control bank and circular scanner above three apparatus chairs, a drinks machine with its original pixel logo, radiation-marked equipment cabinet and small console. Furniture footprints preserve the cross-room route: big-screen outer laboratory (031) → this room (030) → meteor chamber (051). Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room main_lab --site`; start locally at `/?room=main_lab`.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.
