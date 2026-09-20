# Cellar — room 008

Furnished from [background 008](../../source/room%20008.png). Gray machinery room with cyan ductwork, a red-topped blue furnace, radiator, electrical switch box, gauges and floor stain. The right-hand stairs and left dungeon doorway remain clear. Original EGA colors and soft baked shading use the existing browser pipeline.

The entrance hall owns the interactive `rear_right` cellar door. Its portal connects to the upper stair landing at hall elevation. Walk down the 3.36 m flight to the cellar floor; ascent returns through the same seamless portal. Dimensions are inferred for layout review. The cellar owns the initially closed `dungeon_door`, now connected to room 004. No link to the under-house passage is invented.

Rebuild with `./docker-build.sh room cellar`; use `?room=cellar` for direct review. Generated Blender scenes, GLBs and previews live under `generated/`. See [cellar routes](../../docs/cellar.md).

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.
