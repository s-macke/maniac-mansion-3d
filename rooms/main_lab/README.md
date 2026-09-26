# Main laboratory

Furnished from [background 030](../../source/room%20030.png). Control bank and circular scanner above three apparatus chairs, a drinks machine with its original pixel logo, radiation-marked equipment cabinet and small console. Furniture footprints preserve the cross-room route: big-screen outer laboratory (031) → this room (030) → meteor chamber (051). Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room main_lab --site`; start locally at `/?room=main_lab`.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.

## Artwork detail review — 2026-09-22

The meter bank has three columns of two green meters, with a separate switch beneath each meter, matching background 030.

## Door orientation

The gray outer-lab entrance is on the left and the teal meteor-room exit on the right, matching background 030.

## Detailed laboratory review — 2026-09-26

Corrected the three colored indicator stacks to one beside a black cooling grille. Added the auxiliary split red/aqua dial and lower scanner gauge. The apparatus helmets have slotted front plates, side electrodes and vertical ribbed feeds rather than generic face gauges. Shortened the projecting seats, added red edge trim, removed invented restraints from the taller central apparatus, and detailed the radiation cabinet frame and vent dividers. The new auxiliary dial has its own collision footprint.

The opposite wall also uses the matching light-blue metal panels, blue seams and black rivets, continued across its full width at the user’s request. This inferred wall has no copied doorway or machinery.
