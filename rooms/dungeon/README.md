# Dungeon

Furnished from [background 004](../../source/room%20004.png). Irregular stone wall, blue barred recesses, chandelier, original graffiti and static skeletal remains. Both rear door approaches and the cross-room aisle remain clear; the barred recesses are decorative. Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room dungeon --site`; start locally at `/?room=dungeon`.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.

## Artwork detail review — 2026-09-22

The rear wall uses densely packed, staggered irregular stones with red edges and brown faces, following the closely filled masonry in background 004. Door apertures remain clear.

## Detailed overhaul — 2026-09-26

The left laboratory door uses the shared `Dungeon_reinforced_leaf`: the original nested blue panels with two solid crossbars, keepers and padlocks. Both door openings have blue metal surrounds. Locks remain scenery; doors still start closed and open normally.

The hanging fixture now has open linked suspension, shaped blue arms, crown-like prongs, cups and small pale-blue candle tips, with subtle local baked light. The skeleton slumps toward the floor, with posed arms, wrist cuffs and an alternating-link chain attached to a bolted wall anchor. The raised torso has collision; the low leg bones lie across the floor as step-over scenery, leaving the cross-room aisle and left doorway approach clear.

Added the right blue wall's pale corner facet, seam and small bolt heads. The opposite wall now carries the same irregular red-edged brown stonework as the rear wall; that unseen wall remains an inferred continuation. Removed the unsupported blue skirting strip. Original graffiti and barred openings remain.

The shared dungeon/outer-lab doorway is 1.95 m wide, matching the broader reinforced left door in background 004. Both room apertures agree; its destination and closed-first interaction are unchanged.
