# Shared ladder kit

`build.py` generates one 28 cm rail/rung section, `Ladder_section`, in EGA gray with simple baked face shading. Rooms repeat it vertically; a mirrored placement supports the opposite wall. The browser batches these static sections into one draw per room and keeps the shared geometry/material cached across unloading.

Generated editable scene: `generated/blender/shared/ladders/ladder_v1.blend`. This file intentionally contains a single section, not a complete room-height ladder. Generated model: `generated/models/ladders/ladder_v1.glb`. Open the generated room source scene to see its full assembled ladder.

`scripts/blender_shared/ladder_assets.py` records placements and the named `ladders` library in each generated manifest. Authored transforms remain in `geometry.ladders`; generated section matrices never go into `room.json`. Baking includes the ladder in previews while excluding shared meshes from the room GLB.

Build any room that uses ladders via `scripts/build.py room <room>` or Docker; the kit is generated automatically. See [ladder connections](../../docs/ladders.md) for routes and hatch portals.
