# Radio bedroom — room 021

Current footprint: **9 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20021.png), preserving the EGA palette and soft baked shading. Blue bed with rounded wooden ends, radio console with tuning scales, coils, loop aerial and microphones, hanging light, original Fred portrait and wanted poster. The light-blue floor follows the source. The left ladder approach stays clear.

The existing shared ladder and ceiling hatch retain their continuous portal connection to Green Tentacle’s room. Furniture stays outside the approach, shaft and landing.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room radio_bedroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=radio_bedroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 310,408 bytes (84,364 bytes with gzip).
