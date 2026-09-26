# Radio bedroom — room 021

Current footprint: **9 × 4.5 m**, revised after the [room size audit](../../docs/room_size_audit.md). Furniture retains its physical size; door apertures and ladder dimensions are unchanged. Wall-mounted details, collision footprints and any hatch landings follow the revised shell.

Furnished from [the original background](../../source/room%20021.png), preserving the EGA palette and soft baked shading. Blue bed with a red headboard and brown footboard, a low radio console with one green tuning scale, speaker grille, tapered capped coils, loop aerial and two distinct microphones, a two-globe hanging light, original Fred portrait and wanted poster. The light-blue floor follows the source. The left ladder approach stays clear.

The existing shared ladder and ceiling hatch retain their continuous portal connection to Green Tentacle’s room. Furniture stays outside the approach, shaft and landing.

`build.py`, `interior.py` and `room.json` are the authored inputs. Solid furnishings use `geometry.obstacles` for walking collision. Shared doors start closed; existing room placements and portal destinations are unchanged.

Rebuild with `./docker-build.sh room radio_bedroom`. Generated Blender scenes, GLBs and previews live under `generated/`. Review at `http://127.0.0.1:5174/?room=radio_bedroom`. See [upper-floor layout](../../docs/upper_floor.md) for door ownership and provisional dimensions.

The optimized room model is 675,488 bytes (219,477 bytes with gzip).


### Artwork detail review

The earlier third-globe interpretation was incorrect: background 021 shows two globes flanking a black central stem. The detailed review below corrects it. Room connections and navigation footprints are unchanged.


## Detailed source review — 2026-09-25

Lowered the console to match its height relative to the bed. Rebuilt the radio face with one green scale, needle, dark tuning knobs, top switches and a separate perforated speaker panel. Coils taper toward blue caps. The left microphone is pale and mounted on a rectangular switch box; the right has an aqua cradle and black grille holes. The blue bedding reaches the red headboard, with joined rounded bed-end silhouettes and a lower brown footboard. The portrait uses its original clipped-corner frame artwork on a thin solid backing; it and the poster sit against the wall. Removed the unsupported brown skirting color. The two white/yellow globes hang over the radio with local baked light. Room dimensions, furniture footprints and ladder clearance are retained.
