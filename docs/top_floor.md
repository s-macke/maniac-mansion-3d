# Furnished top floor

Four independent rooms at 13.44 m complete the existing top level. All are reconstructed from the original EGA backgrounds with simple geometry and baked vertex colors. They retain their original ports, ladder landings and placements.

| Room | Background | Furnishings | Access |
|---|---|---|---|
| [Safe attic](../rooms/safe_attic/README.md) | 009 | Gray boards, weathering, window, bulb, portrait-covered safe | Heart bedroom ladder |
| [Green Tentacle’s music room](../rooms/tentacle_room/README.md) | 020 | Speakers, green bed, stereo, posters and timber panels | Radio bedroom ladder |
| [Wire attic](../rooms/wire_attic/README.md) | 015 | Damaged plaster, laths, boarded window, loose wiring | Den panel and hidden attic stairs |
| [Observatory](../rooms/observatory/README.md) | 028 | Telescope, pedestal controls, control box, star chart and lamp | Den ladder |

The hidden attic stairs remain the existing inferred passage because there is no separate stair background. No new destinations, characters or gameplay are introduced. The safe portrait is a static cover; the instruments, stereo and wires are decorative. Interactive doors retain their closed initial state.

## Artwork and geometry

Each room keeps its composition in a local `interior.py`, attached to its existing source builder. Original posters and small wall details use exact source-color geometry. The wire attic separates original pixel silhouettes into shallow plaster/lath layers and places solid boards and wire ends in front. The safe attic omits the blue telescope-view overlay already excluded by the reference documentation.

The circular observatory keeps its curved shell, open slit and real floor hatch. Its telescope points through the rear-right opening. Authored obstacle rectangles cover the instrument and control cabinet; circular boundary and hatch collision remain in force. An offset model ray verifies that the telescope does not cause the aperture itself to become sealed.

## Rebuild and review

```bash
./docker-build.sh room safe_attic
./docker-build.sh room tentacle_room
./docker-build.sh room wire_attic
./docker-build.sh room observatory --site
```

Review locally at `http://127.0.0.1:5174/?room=observatory` (substitute any room ID above). Generated Blender scenes, models and previews stay under `generated/`. Door and ladder kits remain shared.

The four optimized room models total 452,473 bytes with gzip (about 452 KB), excluding the shared ladder kit. Their individual sizes are recorded in the room READMEs.

## Validation

Docker/Blender generation, the static build, typecheck and catalog validation pass. Twelve focused navigation/model checks cover furniture collision, continuous ladders, the real hatch and dome slit, and physical body clearance around all three upper ladder landings. The landing geometry check catches the original speaker-cone overlap and passes after the fronts are recessed.

Eight desktop Chrome checks load and walk all four furnished rooms and complete the two bedroom-ladder, observatory-ladder and concealed-stair round trips. Blender reference renders and browser screenshots were inspected. Physical-mobile performance was not tested.
