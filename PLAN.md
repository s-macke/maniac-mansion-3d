# Maniac Mansion 3D Walkthrough

## Goal and scope

Create a static website for exploring a 3D reconstruction of the Maniac Mansion house, based on the EGA backgrounds in `source/`.

The initial experience is a first-person walkthrough. There is no gameplay: no puzzles, inventory, dialogue, NPCs, or game progression. All areas should be accessible for exploration. An optional later third-person mode may show Dave as the player character.

## Current phase: room shells first

Build new rooms as empty walkable shells with doors to review the house layout. Furniture, appliances, windows and other interior artwork come later. Keep existing completed rooms intact. Kitchen (007) is the first room in this phase. Interactive doors start closed.

## Layout reference

Use the supplied artwork [connection_suggestion.png](source/connection_suggestion.png) as the basis for the house layout and room connections. Its cutaway arrangement guides floor placement, room grouping, stairs, and the relationship between the house, underground areas, pool, and garage.

The individual backgrounds in `source/` remain the reference for each room's EGA appearance and details. Match the rooms in the artwork to those image files before modeling connected areas. Treat the cutaway as a layout guide rather than a measured architectural drawing: infer depth and dimensions during blockout, record unclear connections, and document any necessary departures from the suggested arrangement. Characters depicted in the artwork do not expand the walkthrough scope.

## Visual direction

**Core requirement: it must look like the original artwork brought into 3D.** Preserve the source's shapes, proportions, colors, pixel patterns, and recognizable details. Use a simple, flat, comic-like presentation grounded in the original images.

- Use simple 3D geometry with the original EGA colors and pixel textures. Sample colors from the supplied images instead of choosing an approximate modern palette.
- Model room shells, stairs, furniture, and large props as geometry.
- Extract suitable details such as wallpaper, pictures, and labels from the backgrounds for textures.
- Preserve original pixel artwork wherever it can be mapped cleanly onto geometry. Keep source images unchanged and save derived textures separately.
- Use crisp nearest-neighbor texture sampling as the starting point; avoid smoothing away pixel patterns. Evaluate distant texture aliasing in the browser without compromising the intended appearance.
- Reproduce drawn shading and dithering through source textures or deliberately chosen palette colors.
- Keep silhouettes and geometry simple, following the illustrated shapes rather than adding realistic surface detail.
- Reconstruct unseen walls, ceilings, and object backs consistently with the visible artwork.
- Compare each room against its background using a dedicated reference camera.

### Rendering in Blender and the browser

- Start with unlit materials: use emission-based materials in Blender and their supported unlit equivalent in the GLB/browser pipeline. Verify that the export preserves this behavior.
- Use Blender's Standard view transform with neutral exposure and gamma as the starting point. Configure browser color handling consistently and verify sampled colors in exported renders.
- Avoid photorealistic lighting, glossy reflections, metallic effects, ambient occlusion, bloom, depth of field, and cinematic color grading in the baseline style.
- Let geometry, occlusion, the original drawn shading, and movement communicate depth. Following review of the first unlit model, use restrained cel-style shade bands and baked direct shadows to avoid an overly sterile appearance. Retain the original base colors; darker derived shadow shades are permitted.
- Keep room lighting browser-friendly: the current prototype bakes direct lighting into vertex colors and exports an unlit GLB, with no runtime global illumination. Preserve the flat source scene for comparison and editing.
- Do not introduce a generic toon shader or thick outlines by default. Add edge lines only where they help reproduce the original drawing style.
- Validate both a reference-camera render and freely explored viewpoints. A room must retain its original character when viewed from new angles.

The current `source/` folder contains 37 top-level backgrounds, all 128 pixels high and between 320 and 960 pixels wide. Some are scrolling panoramas; their pixel width does not directly determine physical room dimensions. Additional images are in `source/not_important/` and should be reviewed only as needed for references or alternate states.

## Technical approach

- **Authoring:** Blender 4.2.3, with editable `.blend` sources and repeatable Blender Python automation where useful.
- **Browser assets:** GLB exports with web-compatible materials and textures.
- **Viewer:** Three.js, packaged as a static website without a backend.
- **Movement:** first-person mouse look and keyboard walking, with simple collision and stair traversal.
- **Room connections:** open passages or automatic door opening, without keys, locks, or gameplay requirements.
- **Collision:** simple collision geometry separate from detailed visible meshes.
- **Optional third person:** Dave, a follow camera, basic walking animation, and camera obstruction handling.

Native desktop control of Blender is unavailable in this environment; scene creation and modification can use Blender Python.

## Implementation plan

### 1. Inventory and map

1. Create a labeled contact sheet and identify room names.
2. Record doors, stairs, exterior connections, and alternate room states.
3. Build a room connection map from `connection_suggestion.png`, matching the depicted rooms to background filenames and distinguishing explicit connections from inferred ones.
4. Check the intended display aspect before deriving proportions from the images.
5. Establish a shared scale, player height, doorway dimensions, and floor heights.

**Deliverable:** room inventory and an initial house connection map based on the supplied artwork, with unresolved connections marked.

**Status (2026-09-10): initial pass complete.** See [step 1 deliverables](docs/README.md), including all 51 images, six labeled contact sheets, a cutaway-based connection map, exact 16-color palette, display-aspect comparison, and provisional modeling scale. The map explicitly separates visible, suggested, and unresolved connections; full-house topology is not yet verified. Original images remain unchanged.

### 2. Model the entrance hall

Use `source/room 010.png` as the first representative room.

1. Block out walls, floor, ceiling, doorways, and stairs.
2. Add recognizable furniture and architectural details.
3. Apply source-sampled EGA colors, original pixel textures, and simple unlit materials.
4. Set up a reference camera and compare renders against the background.
5. Export an initial GLB and verify its appearance in the browser.

**Deliverable:** editable entrance hall scene, GLB export, and comparison preview demonstrating fidelity to the original artwork and colors.

**Prototype:** [room 010 model and previews](rooms/room_010/README.md). v1 preserves the editable flat geometry; v3 tests baked cel shading with softened, interpolated direct shadows; v2 is retained as the earlier coarse-shadow comparison. This is a first visual interpretation for review; final source matching and browser walkthrough validation remain pending.

### 3. Build the first-person website prototype

1. Load the entrance hall into a minimal Three.js viewer.
2. Add mouse look and keyboard movement.
3. Add floor, wall, furniture, and stair collision as needed.
4. Provide clear controls, a start action, and a reset-position action.
5. Verify the exported materials and textures retain the intended appearance.

**Milestone:** a convincing entrance hall that can be explored on a static webpage.

**Prototype implemented:** [local browser walkthrough](web/README.md), with first-person movement, mouse look, pause/reset, closed-room collision, and curved stair traversal. Uses the connected-hall baked-lighting GLB with no runtime lighting. The first walkthrough is kept local; visual refinement and additional rooms remain later work.

### 4. Validate connected rooms

1. Model a second room connected according to the room map.
2. Align its doorway and floor with the entrance hall.
3. Verify travel in both directions without collision snags or visible gaps.
4. Block out the rest of the house using the supplied cutaway's floor arrangement and room groupings to identify spatial conflicts before detailed modeling.
5. Resolve conflicting source perspectives or layouts while preserving recognizable rooms and the artwork's suggested connections wherever possible; document necessary assumptions and departures.

**Deliverable:** two connected, walkable rooms and a rough whole-house layout.

**Connected prototype implemented:** rooms 010 and 011 form one double-height hall, following the user-approved interpretation. The main staircase meets an upstairs gallery at 3.36 m; the player can look down into the entrance and return downstairs without a scene transition. Original landing portraits, lamps, and reinforced door details come from room 011 pixels. Other door destinations and the whole-house blockout remain deferred. Keep this walkthrough local.

### 5. Expand the walkthrough

1. Finish rooms in connected groups, following the approved visual style.
2. Reuse doors, trim, stairs, materials, and recurring props.
3. Keep editable Blender sources, exported assets, and reference previews organized by room.
4. Validate each room's appearance, collision, and connections as it is added.
5. Include exterior areas needed to enter and explore the house.

**Deliverable:** the complete explorable house, with all mapped areas accessible without gameplay.

### 6. Optional Dave third-person mode

Only after first-person exploration works well:

1. Add a Dave model consistent with the visual style.
2. Add idle and walking animations.
3. Implement a follow camera that handles walls and narrow rooms.
4. Allow switching between first-person and third-person views.

This remains a walkthrough, with no additional characters or gameplay systems.

### 7. Verify and publish

1. Walk every connection and staircase; check for inaccessible areas and stuck positions.
2. Check browser rendering, loading time, and movement performance.
3. Optimize assets where measurements show a need.
4. Build and verify the static site on the selected hosting service.

**Completion criteria:** the site loads successfully, the house can be explored continuously, room connections and collision work, and the rooms look like the original EGA artwork translated into 3D. Reference comparisons must verify colors, pixel detail, silhouettes, and major proportions in both Blender renders and the browser.

## Suggested project layout

```text
source/                 Original reference backgrounds
rooms/                  Editable Blender room scenes and previews
generated/models/rooms/           Exported GLB room assets
assets/textures/         Derived pixel textures
scripts/                Blender automation and export helpers
web/                    Static walkthrough application
docs/                   Room inventory, connection map, and assumptions
```

## First milestone boundary

Complete the entrance hall and browser walking prototype before detailed work on the rest of the house. Review room proportions, texture treatment, camera height, and movement feel at that point, then use those decisions for subsequent rooms.

## Maintainable room assembly

Implemented after the connected-hall prototype: independent room packages, a central house layout, explicit doorway ports, shared Blender geometry and baking helpers, room-local navigation adapters, and nearby GLB loading. The hall and landing remain one unit. See [architecture guide](docs/architecture.md). The living room is the next independent unit; its specific doorway connection remains to be resolved.

## Living room review

Room 003 is modeled as an independent unit, with an isolated local browser preview at `?room=living_room`. Source details, editable geometry, soft baked lighting, closed-door ports, and furniture collision are included. Integration with the hall follows visual review; no doorway destination has been invented.

## First inter-room connection

Implemented: living-room left door ↔ hall right-side door, following the cutaway’s adjacency. Rooms remain independent assets, with matching doorway markers, continuous floor heights, shared-wall ownership, and load-aware doorway collision. The walkthrough now supports living room → entrance hall → upstairs landing in both directions.

## Front exterior first pass

- Separate room 001 exterior package, retaining original EGA palette and porch details.
- Front path, lawn, eight entrance steps, railing and props; roof silhouette interpreted from room 047.
- Continuous bidirectional porch-to-hall route with visible open double doors, baked lighting and collision.
- Local default start outside; hall and living-room query starts retained. No gameplay or hosting added.
- Upper building envelope and routes around the grounds remain future work.

Exterior v3 restores both stair-side bushes and the recessed metal grating behind the left one. The grille is modeled and named, with its route left for later; shrub collision preserves the central stair approach.


### Interactive doors (hall v4)

Separate the front double leaves and living-room leaf within the hall GLB; retain the fixed frames and accepted v3. Use shared browser door state, hinged animation, moving collision, E/click/touch interaction and session state across room streaming. Keep unfinished destinations closed. Preserve baked EGA shading, exclude moving leaves from static cast shadows, and avoid adding GI or gameplay systems. See `rooms/connected_hall/README.md`.


### Kitchen shell v1

Kitchen is its own Blender/GLB package, attached to hall `rear_left` (left of the main staircase) at ground level. Its long axis extends behind the hall; the entrance end sits below the gallery with a 3.12 m ceiling. This resolves the cutaway's compressed above/behind placement as depth, not an additional storey. It is an explicit blockout interpretation, not a verified game-script mapping.

Preserve the EGA blue wall/floor palette from room 007. Include an openable entrance and a closed far doorway reserved for dining room 037. Do not build the dining room or assign other hall exits yet. No kitchen furnishings in this phase.


### Shared doors implemented

Use a common standard leaf and frame kit for new room shells, with size/placement transforms and mirroring. Double doors reuse two leaves. Existing indoor rooms have been migrated (hall v6, living v4, kitchen v2); special door artwork remains distinct. Browser loading, shared resource lifetime, closed starting states and door collisions are covered by focused tests. See `shared/doors/README.md` for the reusable authoring workflow.


### Dining-room shell v1

Continue the layout-first phase with room 037 after kitchen. Empty red walls and pink floor retain the source palette; furnishings and decorative interior detail are deferred. Connect through the kitchen's far shared door, initially closed. Leave the far pantry doorway closed. Dining is an independent 19.2 × 5.55 m unit at ground level, placed straight beyond the kitchen. Its proportions and placement remain reviewable blockout choices.

## Design iteration cleanup — 2026-09-13

Removed superseded Blender scenes, GLBs, previews, build recipes and experiment reports. Earlier version references in this plan describe project history, not files still available. Keep the current five room packages, shared door kit and original reference artwork. The combined hall now generates its entrance geometry directly through `rooms/connected_hall/entrance.py`; the intermediate base scene and its standalone generator have been removed. Current room assets were preserved byte for byte. Nothing was committed.

## Pantry shell

Room 036 continues the empty-room layout pass beyond dining. Keep the original gray palette and blue rear mesh door, reuse the shared dining doorway, and leave the suggested pool exit unconnected. Dimensions are provisional.

## All door designs in the shared library

The pantry mesh door, reinforced landing door and entrance transom now join the wooden leaf/frame in `shared/doors`. Room builders own placement and behavior; the library owns design. Distinctive shapes and source pixel art are preserved, with reusable neutral edge shading. Unconnected doors remain closed. The Blender library includes a display arrangement for inspection.

## Focused shell cleanup

Extracted repeated interior-shell construction for kitchen, dining and pantry into optional shared helpers. Room-specific colors, cameras, connections and special assets stay local. The next outdoor area does not need to follow the rectangular-shell recipe.

## Pool deck v1

Built room 006 as an independent outdoor unit with a filled pool, walkable stone deck, coping, ladder, floating chair silhouette and EGA fence. The shared pantry mesh door opens onto it and starts closed. This pass uses the original filled-pool state; drained basin/ladder traversal and the garage route remain future work.

## Garage layout shell

Added room 016 as an outdoor forecourt and covered garage bay, with a wide open vehicle entrance. A provisional gap in the far pool fence connects the two areas. Keep the car, shelving, shutter mechanism and decorative details for later.

## Library and first-floor shells — 2026-09-13

Added the ground-floor library and all five rooms around the existing first-floor landing: plant room, music room, security corridor, medical room and arcade. They remain empty shells with shared interactive doors, original EGA colors and baked shading. See [the layout and deferred connections](docs/first_floor.md). The reinforced door is now an operable shared leaf/frame pair. The corridor stair ends at the next closed storey boundary; the unresolved library spiral route remains deferred. No hosting or commits.

## Furnished library, kitchen and dining room

The complete layout is retained while these three shells receive their artwork-based interiors (005, 007 and 037). Source builders create bookcases and a decorative library spiral stair, kitchen cabinets/appliances, and the long turquoise dining table with panelling and the original painting. Furniture footprints prevent walking through the new solids and leave routes to every existing door. Shared doors still start closed. The library staircase has no new destination; appliances and table details are static. Original colors and soft vertex-baked shading require no runtime GI.

## Furnished garage and pantry

Backgrounds 016 and 036 now supply the garage car and storage rack, open shutter fixtures, and pantry shelves/supplies with cracked plaster and exposed brick. Car, appliances and supplies remain static exploration scenery. Furniture footprints route walking around the car to the existing cellar hatch and leave the pantry dining/pool doors clear. Shared doors, floor heights, independent spaces and the continuous pool/garage group are unchanged. All geometry and shading rebuild through the existing room commands; generated files remain ignored.

## Furnished floor above the entrance

The complete five-room landing group is furnished from its original backgrounds: art studio 014 (formerly mislabelled Plant room; stable `plant_room` ID), music room 017, security corridor 013, medical room 022 and arcade 018. Original canvas, posters, portraits, chalkboard and cabinet signs use source pixel geometry; major furniture and display props are solid 3D forms. Machines, instruments, skeleton and statue remain static scenery. Furniture collision preserves door approaches and the corridor stair route. This group is at 3.36 m, called the first floor in the existing floor-height documentation.

## Furnished windowed-hall level

The next physical level above the landing rooms, at 6.72 m, now has a furnished windowed stair hall (012) and photo darkroom (023). Original wallpaper, window lattice, columns, plant, balustrade and picture guide the hall; the darkroom keeps its black palette with a red bench, enlarger, safelight, trays and drawer cabinet. Furniture remains static and its collision footprints leave both stair flights and the shared photo-room doorway usable. The bedroom level at 10.08 m remains the next furnishing group.

### Furnished bedroom level

Completed the upper corridor, radio/heart/green bedrooms, exercise/mummy room, mummy bathroom and typewriter den from backgrounds 038, 021, 019, 026, 025, 024 and 027. Preserve original artwork, browser baked shading and shared doors. Existing ladders, hidden passage and room transforms remain in place; furniture footprints leave their routes clear.

### Furnished top floor

Furnished the safe attic (009), Green Tentacle’s music room (020), wire attic (015) and observatory (028), preserving existing ladder/door routes and the real dome slit. The inferred hidden stairs remain unchanged. See `docs/top_floor.md` for scope, original-art decisions and rebuild commands.

## Furnished cellar and drained basin

Backgrounds 008, 029, 004, 051, 030 and 031 now supply the cellar machinery, under-house supports/pipes, dungeon stonework and remains, and laboratory consoles/chairs/equipment. Background 002 adds reactor equipment, hose, depth markings, drain and plug to the existing pool basin. Shared helpers keep pipe and panel authoring consistent. All props remain exploration scenery; the existing stairs, doors, crawl, garage ladder and pool drain/refill route remain in place. Authored footprints preserve circulation, with separate deck and basin obstacles. Source builders generate the Blender scenes and compact browser models with the established EGA/baked-shading pipeline.

The user corrected the cellar artwork sequence to **004 dungeon → 031 big screen → 030 three apparatus seats/tubes → 051 meteor room**. The outer-laboratory and meteor-chamber interiors/reference assignments were swapped to match, including their collision footprints and connecting gray/teal door assets. Semantic room IDs, portal topology and the final-room garage ladder are retained.
