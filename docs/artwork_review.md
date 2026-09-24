# Room artwork reviews

## Initial five-room refinement

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
and the foreground bedside cupboard with its decorative yellow key. The headboard and curtain pair span the right end of the bed, opposite the
footboard; the earlier rear-wall placement was incorrect. The mattress uses the
full bed width and the cushion faces the footboard. The compact two-shade ceiling fixture adds soft baked
local light. The portrait is mounted against the rear wall.

The cupboard backs onto the right wall, forward of the ladder, and faces into
the room, with its own collision footprint. Vanity and bed collisions follow their corrected proportions. The
room footprint, shared door ownership and safe-attic portal remain unchanged.

Validation: rebuilt and inspected the Blender reference render and browser
close-ups of the vanity and bed. Static build, typecheck, catalog validation and
12 navigation/model checks pass. Both desktop browser checks pass: furnished-room
walking and the continuous safe-attic ladder round trip. The optimized bedroom
is 413,976 bytes (133,522 bytes gzipped).

The heart cushion was subsequently replaced with a thin, inflated curved mesh,
rounded lobes and a lower sideways tilt, removing the initial angular slab.


## Safe attic — 009

Completed the boarded wall to the floor, ceiling and side corners, with a solid
dark backing and narrow board seams. The visible bulb now contributes soft local
baked light. Replaced the flat star panel with an actual wall aperture, recessed
jambs, sill and crossbar; stars sit at a distance in an enclosed black sky volume.
Movement changes their alignment with the near frame. This is static room
geometry, with no new portal or accessible exterior. The ladder route and safe
placement are unchanged. The original blue telescope overlay remains excluded.

Validation: Blender rebuild, static build, typecheck and catalog checks pass.
Nine model/navigation checks pass, including rays through the open window versus
its surrounding wall, rear-wall edge coverage and brighter baked floor colors
beneath the bulb. Desktop Chrome views from two positions confirm the recessed
window and distant stars; the attic ladder round trip also passes. No physical
mobile performance measurement was made.

## Shared outside windows — 026, 024 and 007

The green bedroom, mummy bathroom and both kitchen windows now use the shared
`blender_shared/windows.py` helper. Existing walls are split only at the window
apertures; frame recesses, mullions and sills remain solid geometry. Distant stars
sit against the original blue night color. The kitchen's pane divisions and the
bathroom's red/yellow trim are retained. These windows are non-traversable and
create no new room connections or runtime lighting. The living room is covered by the detail pass below; the windowed stair hall
and boarded wire attic remain a later, artwork-specific pass.

Validation: all three Blender packages rebuild; static build, typecheck and
catalog checks pass. Four focused model/circulation checks pass, including rays
through every new opening and solid wall coverage above them. Chrome walking
checks pass for all three rooms; inspected views cover the bedroom window, both
kitchen windows and the bathroom's recessed red/yellow surround. No runtime lights
or new room connections were introduced.

## Under-house passage — 029

Restored eleven yellow supports with tall red caps, diagonal braces, bolts and
white feet; added overhead joists and denser damp grain to the rear boards.
The three blue plumbing runs now have varied risers, elbows and collars, plus
the right-hand valve wheel. The left rear grille and central overhead grille
are modeled separately. A fine static leak and shallow cyan puddle with ripple
lines sit below the overhead grille. These are scenery, with no new connections.
Six broad bake positions and a modest fill increase make the details readable
along the full passage while preserving its black floor and ceiling. Fixtures
remain within the existing rear collision strip.

Validation: target Blender rebuild, static build, typecheck and catalog checks
pass. The circulation check and two desktop Chrome checks pass, covering the
full passage aisle and the bush-grating crawl in both directions. Inspected
browser views show the left grille, overhead grid, puddle and right valve wheel.


## Living room — 003

Opened both window apertures through the rear wall and wallpaper, with recessed
wooden reveals and enclosed black night spaces. The original curtain borders,
ties, sash and blue pane linework are retained; only black pane interiors are
removed. The source has no stars, so none are added. The landscape frame now
backs onto the wall. Sofa tufting follows three columns, with a brown/gold front
rail, and the radio cabinet top is brown instead of a broad yellow slab. The
accepted arched radio face, landscape and floor-mark pixels are retained.
The chandelier supplies a soft local baked light with bright candle flames and
slightly reduced general fill. Room dimensions, furniture footprints and shared
door connections remain unchanged.

Validation: rebuilt in Blender and inspected reference/interior and desktop
Chrome close-ups. Static build, typecheck, catalog and window-aperture model
checks pass, including the gap immediately beneath the valance and solid wall
above. Browser walking past the furniture passes; gzip delivery and exact
optimized-file checks pass. Final export: 2,006,560 bytes, 632,000 bytes gzipped.


## Ten-room detail review — 2026-09-22

Stopped after these ten rooms. Each correction follows a visible feature in the
original background, checked against the previous Blender interior preview.

| Room | Background | Fixed mismatch |
|---|---|---|
| plant_room | 014 | Added the two red/brown screw clamps above the canvas, including their gray screw heads. |
| security_hall | 013 | Added the missing wall-mounted keypad beside the medical doorway, with a dark display and three columns of buttons. |
| arcade | 018 | Added the gray stepped plinth and narrow upper step beneath each arcade cabinet. |
| radio_bedroom | 021 | Restored the central third globe to the ceiling fixture; the shared helper previously supplied only two. |
| green_bedroom | 026 | Completed both hanging model aircraft with propellers, spinners, upright tail fins and landing wheels. |
| mummy_room | 025 | Restored the thin black aerial above the sarcophagus, with its three crossbars. |
| typewriter_room | 027 | Replaced generic rectangular fireplace decoration with the original irregular stone faces and colored flecks, mounted on the solid piers and lintel. |
| wire_attic | 015 | Made the exposed bulb visibly bright and added soft local baked light beneath its actual position. |
| tentacle_room | 020 | Added the small green/yellow key on the right wall as static scenery. |
| observatory | 028 | Made the hanging bulb visibly bright and baked its local light onto the nearby dome and floor. |

The wire-attic and observatory lamps use static vertex-color baking. No runtime
lighting, new interactions or connections were added. Original source images
remain untouched.

Lighting verification compared floor-color samples in the previous and rebuilt
GLBs. In linear luminance, the wire-attic sample below the fitting rose from
0.0887 to 0.1295, and the observatory sample from 0.1525 to 0.1892. Neither export
uses `KHR_lights_punctual`. These are local bake checks, not a global brightness
change or a runtime-light implementation.

Validation: all ten Blender packages rebuilt and their source comparisons and
interior previews were inspected. Static build, typecheck, catalog validation
and 13 focused navigation/model checks pass. All ten desktop Chrome room checks
pass, with inspected close-ups of the corrections. The initial browser run lost
its separately launched preview server; the remaining seven checks then passed
with Playwright managing the server lifetime. No physical-mobile test was run.

## Next five-room detail review — 2026-09-22

Stopped after these five additional rooms. Each was compared with its original
background and previous interior preview.

| Room | Background | Fixed mismatch |
|---|---|---|
| dining_room | 037 | The platters distinguish the roast bird from the sliced ham: the bird retains its projecting bone, while the ham has a white fat rim, red cut face and fine white marbling, following background 037. |
| pantry | 036 | The shelving has red backing behind the stocked upper bays and a brown lower compartment, matching background 036 rather than exposing the gray room wall through every shelf. |
| dungeon | 004 | The rear wall uses densely packed, staggered irregular stones with red edges and brown faces, following the closely filled masonry in background 004. Door apertures remain clear. |
| outer_lab | 031 | The two console instruments match background 031: a split pink/aqua dial beside a black-faced dial with a pink rim, each with separate ticks, needle and hub. |
| main_lab | 030 | The meter bank has three columns of two green meters, with a separate switch beneath each meter, matching background 030. |

The corrections retain the EGA palette, existing baked shading, room layout,
collision footprints and door connections. Source images are unchanged.

Validation: all five Blender packages rebuilt successfully. Source comparisons,
interior previews and desktop Chrome screenshots were inspected. The static
site build, typecheck, catalog validation, 11 focused navigation/model checks
and all five browser room checks pass. No physical-mobile test was run.

## Ten additional rooms — 2026-09-24

This batch covers ten rooms outside the preceding ten-room and five-room batches.
Each correction follows a visible feature in the original source background.

| Room | Background | Fixed mismatch |
|---|---|---|
| library | 005 | Restored the spreading green plant in its low red/yellow pot on the middle bookshelf, clearing only its book bay. |
| kitchen | 007 | Corrected the knife-rack arrangement: broad cleaver at the left and a toothed white chainsaw guide bar under the red motor at the right. |
| garage | 016 | Restored the small white/red bumper sticker beside the rear plate using the original artwork pixels. |
| music_room | 017 | Added the pedal lyre, crossbar and three pedals beneath the keyboard, following the existing piano rotation. |
| medical_room | 022 | Added the white sheet hanging over both short ends of the examination table, with folded lower edges. |
| windowed_hall | 012 | Added the clipped corners of the leaded window panes, completing their octagonal outlines. |
| photo_room | 023 | Restored the second pale enlarger-head band and the small black ventilation slots. |
| upper_corridor | 038 | Replaced round branch pots with the original square red planters and rectangular pale rims. |
| mummy_bathroom | 024 | Restored the thin green enamel drip and detached spot beneath the bathtub rim. |
| meteor_chamber | 051 | Replaced the generic polygon puddle with the original irregular purple spill, pink highlights and scattered droplets. |

Original source files, room dimensions, collision footprints and connections
remain unchanged. All additions use the existing EGA geometry and baked shading.

The kitchen clearance regression formerly measured the entire model bounding
box, including distant window scenery. It now ray-checks three solid rear-wall
locations against the facade plane; the required 3 cm clearance is unchanged.
The separate aperture check still verifies distant sky through both windows.

Validation: all ten Blender packages rebuilt, including follow-up corrections
for the pot, window joints and flush attachment of the sticker and sheet. The
production site build, typecheck, catalog validation and 19 distinct focused
model/navigation checks pass. All ten desktop Chrome room checks pass; their
source comparisons, Blender previews and browser detail screenshots were
inspected, with the three final mounting refinements rechecked in Chrome.
No physical-mobile test was performed. Changes remain uncommitted.

## Three-room review by priority — 2026-09-24

This pass reviews library (005), music room (017) and garage (016) from large
shapes to small details, with multiple inspection angles. The aim is to resolve
visible mismatches without changing inferred dimensions merely to imitate the
original forced perspective.

| Priority | Library | Music room | Garage |
|---|---|---|---|
| Proportions and main shapes | Kept established bookcase and spiral proportions; rounded the blocky chair upholstery. | Smoothed the piano tail, keeping its accepted width and angle; reshaped the horn flare. | Corrected the major blue/gray floor mismatch; retained the car orientation and bay footprint. |
| Placement and attachment | Receiver, dial and piping follow the chair/phone surfaces; fixed obstructed reverse preview camera. | Recessed horn lining and throat, supported tonearm and vase foot; fixed camera inside the TV. | Window pixels follow sloping glass; rear plate now has a solid body-mounted bracket. |
| Colour and lighting | Black/gray upholstery, green telephone, corrected black lamp stems and existing two lamp bakes. | Red horn interior, purple/yellow record, blue vase foot and white dado panels; existing fill retained. | Dark-gray covered floor, lighter threshold, blue forecourt, cyan trim and original rear-window colours; existing soft bake retained. |
| Small details | Receiver earpieces, rotary holes and coiled cord. | Lower wall panel outlines, spindle, pickup and open vase neck. | Trunk wing, curved shoulder strips and bumper guards. |

Remaining discrepancies are recorded in each room README: approximate library
book patterns; simplified music-room capitals, leg turnings and key count;
simplified compound car curves. Unseen dimensions and the library stair exit
remain uncertain. None of these three rooms is claimed to be an exact 3D
reconstruction from a single 2D view.

Validation: all three Blender packages rebuilt; original backgrounds, Blender
previews and desktop Chrome screenshots from multiple angles were inspected.
All three browser aisle/walkaround checks and eight focused model/navigation
checks pass. The final lamp-stem colour correction was rebuilt and inspected
in the Blender preview. Production build, typecheck and catalog validation pass.
No physical-mobile validation was performed.
