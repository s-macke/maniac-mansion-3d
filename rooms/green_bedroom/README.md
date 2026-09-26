# Green bedroom — room 026

Current footprint: **8 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20026.png), preserving the EGA palette and soft baked shading. Green/red patterned bedspread and an open metal bed frame, hanging model aircraft, original blueprint and pennant, hamster enclosure and a solid pink piggy bank on its low table. The rear corridor door has an open approach.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room green_bedroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=green_bedroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 590,560 bytes (154,344 bytes with gzip).


The outside windows use `scripts/blender_shared/windows.py`: real openings in
the existing wall slabs, recessed frames and sills, and distant stars against
the original blue night color. Near frames occlude the sky naturally as you
move. The sky is static unlit geometry in this room, not another room connection;
wall collision still prevents walking outside. Doors and furnishings are unchanged.


### Artwork detail review

Completed both hanging model aircraft with propellers, spinners, upright tail fins and landing wheels. Room connections and navigation footprints are unchanged.

## Detailed source review — 2026-09-25

Replaced the flat hamster-front image and solid blue tank block with a three-dimensional white hamster with a brown back patch, ears, eyes, pink nose, paws and short tail. The enclosure has a floor, blue back and solid frame, leaving the animal visible from the front and sides; it does not use an opaque image or a transparent-material effect. The cabinet and walking footprint are retained. This is static scenery, without animation or gameplay.

Moved the green bedroom’s four-pane outside window from the rear door wall to the perpendicular right-hand wall, as shown in background 026. The rear wall is solid again; the recessed frame, distant blue sky and stars remain.
