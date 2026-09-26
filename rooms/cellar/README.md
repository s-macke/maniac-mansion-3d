# Cellar — room 008

Furnished from [background 008](../../source/room%20008.png). Gray machinery room with cyan ductwork, a red-topped blue furnace, radiator, electrical switch box, gauges and floor stain. The right-hand stairs and left dungeon doorway remain clear. Original EGA colors and soft baked shading use the existing browser pipeline.

The entrance hall owns the interactive `rear_right` cellar door. Its portal connects to the upper stair landing at hall elevation. Walk down the 3.36 m flight to the cellar floor; ascent returns through the same seamless portal. Dimensions are inferred for layout review. The cellar owns the initially closed `dungeon_door`, now connected to room 004. No link to the under-house passage is invented.

Rebuild with `./docker-build.sh room cellar`; use `?room=cellar` for direct review. Generated Blender scenes, GLBs and previews live under `generated/`. See [cellar routes](../../docs/cellar.md).

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.

## Artwork refinement

The rear wall is light gray, with one ribbed return pipe behind the cyan risers; the earlier three-pipe interpretation was incorrect. The large duct has its blue flange and a separate ceiling intake with red elbow wraps. Narrow black furnace risers, a small pipe gauge and the green drip are restored. The floor spill uses the original pixel silhouette beneath the leaking pipe.

The two small cyan risers join the red ribbed pipe at a shared lower junction, and its other end connects into the furnace manifold. The yellow flared cap sits between the red boiler dome and black chimney.

The furnace has a blue intake manifold, chimney ribs and exhaust flanges, cooler fasteners, a firebox latch and corner bolts, and bands and a label on the extinguisher. Its curved ribbed outlet terminates in a blue flange embedded in the rear wall. The electrical cabinet has an aqua border, yellow warning mark, screws and a solid hanging key. Stair treads and rails are gray rather than brown. All details remain static EGA geometry with baked shading; the staircase and dungeon route retain their navigation dimensions. See the [artwork review](../../docs/artwork_review.md).
