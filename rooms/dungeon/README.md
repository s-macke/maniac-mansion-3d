# Dungeon

Furnished from [background 004](../../source/room%20004.png). Irregular stone wall, blue barred recesses, chandelier, original graffiti and static skeletal remains. Both rear door approaches and the cross-room aisle remain clear; the barred recesses are decorative. Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room dungeon --site`; start locally at `/?room=dungeon`.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.
