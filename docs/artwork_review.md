# Five-room artwork refinement

This pass applies the medical-room review method to five existing interiors: compare proportions, placement, complete silhouettes and borders, distinctive source details, and visible light sources. Original EGA colors and the accepted door/portal layout remain the basis. Room footprints are unchanged.

| Room | Reference | Corrections |
|---|---|---|
| Library | 005 | Broader spiral with a continuous curved outer stringer, complete bookcase crown, green telephone receiver and visibly lit reading lamps with local baked light. The staircase remains decorative because its destination is unresolved. |
| Music room | 017 | Broader grand piano while retaining its height, depth, angle and supported keyboard; piano, stereo and television redistributed to retain doorway clearance; original rounded rectangular CRT glass replaces the oval approximation. Existing cassette and foreground record desk remain. |
| Cellar | 008 | Restored three horizontal ribbed gray return pipes behind the cyan risers; broadened the furnace/cooler assembly without raising chimney tops through the ceiling. Stairs and dungeon access remain clear. |
| Photo room | 023 | Visible red safelight glass and a localized baked pool on the workbench, retaining the nearly black room and original red/brown palette. |
| Mummy bathroom | 024 | Toilet/cistern backs onto the left wall and faces inward; original jagged plaster damage restored above the mirror and beside the curtain. Graffiti lies flush against the rear wall. |

## Implementation

All changes live in the room builders/configs. Collision footprints follow the larger spiral, piano and machinery and the rotated toilet. Existing doors, stairs, ladders and room destinations are preserved. No characters, puzzles or new connections are introduced.

The shared fixture bake accepts an optional light direction, allowing the library's upward-facing lamps to illuminate the nearby wall/books while the photo safelight points downward at the bench. The medical lamp keeps its default downward direction. All fixture light, falloff and shadows remain baked vertex colors; no runtime lights, bloom or global illumination are added.

## Local review

Use `http://127.0.0.1:5174/?room=library`, replacing `library` with `music_room`, `cellar`, `photo_room` or `mummy_bathroom`. Reference and inside views are regenerated under `generated/previews/rooms/<room>/` by the normal room builds.

## Validation

All five Blender packages were rebuilt and their reference renders inspected. The static website build, TypeScript check and catalog validation pass. Fourteen focused navigation/model checks pass, including first-floor door transitions, circulation, actual model floors, both upper stair flights and the cellar stairs. The enlarged piano initially intruded on the entry approach; redistributing the piano, stereo and television restored the clearance without weakening the door tests.

Eight desktop Chrome scenarios pass: walking/rendering each of the five rooms, descending and returning on the cellar stairs, and bathroom/photo doorway round trips. The final music-room arrangement was checked again after adjustment. Browser screenshots were inspected. Export checks confirm bounded vertex colors and no runtime light extension; sampled darkroom desktop vertices beneath the safelight are brighter than those at the distant end of the same surface. No physical-mobile performance test was run.


## Upper corridor — 038

Restored the details missed by the initial furnishing pass: brown side walls,
solid timber corner piers and chamfered red/gold edges, returning wainscot rails,
and the red left-door surround with its original devil-face ornament. The stair
hall retains ownership of that interactive door. The three fixtures each have
two black bell shades and white undersides, replacing the incorrect aqua globes.
Their local light is baked; flush source-pixel wallpaper patches preserve the
cyan/blue pools of light shown in the artwork. Portal positions, walking
clearances, closed initial door states and room dimensions are unchanged.

Validation: rebuilt the corridor with Docker/Blender, built and typechecked the
site, and passed the five furnishing/upper-floor navigation checks. Both desktop
browser checks passed: hallway walking with left-door screenshots, and the full
windowed-hall stairs → corridor → green bedroom → stairs return route. The local
server was restarted before the successful final browser run.


## Red heart bedroom — 019

Replaced the generic furnishing approximations with source-specific details:
large staggered hearts and ceiling/base trim; a narrower three-panel vanity with
short dark feet, blue flower vase and pink/white telephone; original branching
mirror-crack pixels; a wider bed with its heart pillow at the curtained right
head end and rounded brown footboard; a complete yellow/purple portrait frame;
and the foreground bedside cupboard with its decorative yellow key. The curtain
pair faces into the room. The compact two-shade ceiling fixture adds soft baked
local light. The portrait is mounted against the rear wall.

The cupboard sits forward and left of the ladder aisle, with its own collision
footprint. Vanity and bed collisions follow their corrected proportions. The
room footprint, shared door ownership and safe-attic portal remain unchanged.

Validation: rebuilt and inspected the Blender reference render and browser
close-ups of the vanity and bed. Static build, typecheck, catalog validation and
12 navigation/model checks pass. Both desktop browser checks pass: furnished-room
walking and the continuous safe-attic ladder round trip. The optimized bedroom
is 416,100 bytes (133,602 bytes gzipped).

The heart cushion was subsequently replaced with a thin, inflated curved mesh,
rounded lobes and a lower sideways tilt, removing the initial angular slab.
