# Room packages and house assembly

The house is assembled from independently editable architectural units. Room backgrounds 010 and 011 are one unit because they share the open stair hall. Future enclosed rooms have their own packages. Nothing is published; the local walkthrough remains the review surface.

## Where changes belong

| Change | Edit |
|---|---|
| Room shape, furnishings, source-pixel details | `rooms/<unit>/build.py`; generated `.blend` edits are not source changes |
| Asset version, bounds, spawn, ports, lighting settings | `rooms/<unit>/room.json` |
| Position, rotation, elevation, or connection between units | `house/layout.json` |
| Room floor and furniture collision | `web/lib/rooms/<unit>.ts` |
| Rectangular shell setup, floors, ceilings, side door openings and reference markers | `scripts/blender_shared/shell.py` |
| Reusable boxes, beams, walls, doors, material assignment | `scripts/blender_shared/geometry.py` |
| Shared soft cel-light bake and export | `scripts/blender_shared/bake.py`, `scripts/finalize_baked_glb.py` |
| House coordinate transforms, movement, nearby asset loading | `web/lib/house/` |
| Mouse, keyboard, touch controls and interface | `web/components/walkthrough.tsx` |

`rooms/connected_hall/entrance.py` generates the entrance geometry in memory as the first stage of the hall builder. The complete hall is generated directly, without an intermediate Blender base scene. New rooms use the shared helpers directly. `scripts/model_connected_hall.py` is a compatibility wrapper for the current hall builder.

## Coordinates and connections

All package coordinates use metres, Blender X/Y for the floor and Z for height. A package origin is stable and independent of house placement. House instances supply `[x,y,z]` and a yaw in radians about positive Z. The browser applies the same transform to meshes and navigation; Three.js receives `(x,z,-y)`.

Each port has a unique name within its package, local position at the centre of its threshold, outward horizontal unit vector, width, and state. Hall ports are named after their physical locations. The right-side port connects to the living room and the entrance connects to the exterior; unused ports remain closed. Matching `PORT_*` markers are saved in each room source. The internal hall staircase needs no inter-unit port.

A house connection has the form:

```json
{"a":{"instance":"hall","port":"right_side"},"b":{"instance":"living","port":"entrance"}}
```

The current connection uses the hall’s right-side port and the living room’s left door. Connections must use open ports whose transformed positions, heights, widths, and opposing normals agree. The check command catches duplicates and misalignment. Opening a connection also requires swinging the physical door leaf clear and updating its collision in the room geometry and navigation; changing the JSON alone does not cut walls or animate doors.

## Commands

From the project root:

```bash
python3 scripts/build.py list
python3 scripts/build.py check
python3 scripts/build.py room connected_hall
./walkthrough.sh build
./walkthrough.sh
```

Build changes only the selected room's editable output. Bake reads its configuration and writes its baked Blender file, previews, and GLB. Keep the current source, bake, export and previews named by `room.json`. Superseded iterations have been removed; temporary comparisons should not accumulate in the project.

Set `BLENDER_BIN` to select Blender locally, or use `./docker-build.sh` for the included toolchain. All output paths point into `generated/`; builders do not write into source folders.

Website build/dev commands validate and copy active assets automatically. `web/lib/house/generated.json`, `adapters.generated.ts`, and `web/public/models/<unit>/` are generated; edit room packages and the house layout instead. Superseded asset copies have been removed.

## Adding another room

1. Create `rooms/<new_room>/` with its authored `room.json`, builder and README. Reference original PNGs in `source/` and declare output paths beneath `generated/`. Call `load_config(..., prepare=True)` at construction start and `save_generated(config)` when construction completes. Use the shared geometry helpers and bake configuration.
2. Add `web/lib/rooms/<new_room>.ts` implementing `floorHeight`, `canStand`, and `zone`, plus focused collision tests. Keep room-local coordinates; do not embed house placement here.
3. Add its instance to `house/layout.json`. The generated adapter registry picks up its navigation module automatically.
4. Build and bake this unit independently. For isolated browser review, mark its instance `previewOnly: true` and use `?room=<instance-id>`. It is excluded from the normal house until ready.
5. Agree which entrance doorway connects to it. Align the two port markers, open the matching mesh and collision apertures, then record the connection.
6. Run the check/build commands and test walking both ways before accepting the new version.

## Loading and current limits

The browser loads separate GLBs near the player, using distance to transformed room bounds. The current load radius is 24 m and unload radius 32 m, avoiding repeated loading at a boundary. Unloaded meshes, materials, and textures are disposed. The hall loads as one unit so its open sightlines stay intact. The approved rendering settings and baked colors are unchanged.

The hall and living room are connected. `?room=living_room` starts in the living room within the assembled house. Future `previewOnly` entries remain isolated until connected. Coordinate transforms and loading thresholds have automated checks; doorway traversal and touch controls are checked in browser emulation; physical mobile performance is not measured. Long sightlines may require larger bounds/loading radii. The connected doors open and close through the shared door system described below. The v4 door checks exercise collision, actual GLB hinges, targeting and state retention without browser automation; physical mobile performance remains unmeasured.

## Download optimization

`scripts/build.py sync` runs `optimize_baked_glb.py`: removes normals from these unlit meshes, removes unused buffers, welds identical position/color pairs, and uses 16-bit indices where possible. It verifies the exact positions and floating-point colors at every indexed triangle corner, including winding. No geometry simplification or color quantization is used. Original exports and Blender files are retained.

The local server negotiates the generated `.glb.gz` sidecars through `Accept-Encoding`, with a plain optimized GLB fallback. Another static host must enable gzip or equivalent compression to achieve the same download sizes.

### Doorway collision and loading

The runtime bridges room-local wall bounds only within a declared open portal, with clearance for the player radius. Unlinked walls remain solid. Both room assets must be loaded before the connecting passage becomes traversable. There is no teleport or loading transition. Shared-wall surfaces must stay on their owning side of the port plane; floor edges meet at that plane rather than overlapping.

The shared living-room doorway has one physical door leaf, owned by the hall. It is hinged at the south jamb and swings 90 degrees into the hall, with panels and handles on both faces. Its generated bounds block walking through the leaf, including the portal bridge. The living-room asset supplies the matching frame without a duplicate leaf.

## Front exterior

`front_exterior` is an independent package placed at `(-6.4, 2.35, 0)`, yaw `-pi/2`. Its origin matches the hall's entrance port. Lawn elevation is -1.2 m; eight steps lead to the porch at hall level. Porch rails, stair cheeks, posts and ground props have collision. The full-house start is now on the approach; `?room=hall` and `?room=living_room` provide the existing room starts. The hall owns both interactive front leaves; they start closed and swing inward.

The roof/tower exterior is provisional geometry above the current hall ceiling, based on the distant exterior art. It does not assign new room destinations. Star and moon meshes opt out of lighting and shadow casting through `bake_unlit`; all ordinary room geometry keeps the existing bake behavior.


## Reusable interactive doors

The hall owns the front double doors, living-room door and kitchen door. The kitchen owns the dining-room door. Room GLBs retain named hinge nodes; leaves and standard frames come from the shared kit below.

`geometry.doors` in each generated room manifest describes the derived hinge poses and collision bounds. The builder tags moving meshes with `door_node` and `door_hinge`; the bake groups each leaf separately at its hinge and excludes moving geometry from the static shadow BVH. `web/lib/house/doors.ts` owns session state and oriented collision, and `door-view.ts` binds that state to loaded GLB nodes and nearby line-of-sight targeting. The room loader rebinds the existing state after unloading. Room-local navigation and portal placements do not own animation state.

To reuse this for another connected standard door, tag its leaf and decorations, leave its frame static, and declare its port in authored configuration and derive its hinge, bounds and swing angle in the owning builder. A shared doorway has one owner. An `open` port means the route exists; the moving leaf determines whether it is physically blocked at that moment. Unassigned destinations stay closed.

Door collision checks precede both room support and the portal bridge. Swings use small angular steps and pause before reaching the walker, including for double doors. The browser adds no lights or real-time shadows; baked shading on moving leaves is a deliberate approximation.


## Empty kitchen / layout-first phase

New rooms are built as empty shells with doors before interior detail. Existing completed rooms remain intact. `rooms/kitchen` is the first package in this phase. It uses the room 007 EGA palette, a 3.12 m ceiling and a ground-level connection behind the hall via `rear_left`. The hall exports the `Door_kitchen` hinge for the shared interaction/collision system.

The kitchen's entry end is below the existing gallery. Room-local navigation rejects the other storey's elevation, and the ceiling ends at z=3.16, flush with the gallery slab underside. Its far door now connects to the dining room through an interactive leaf owned by the kitchen. Shell bounds and physical door positions are stored in the room configuration rather than embedded in the house placement.


## Shared standard door kit (current)

`shared/doors/build.py` produces `standard_doors_v1.blend` and one GLB with seven meshes and one unlit vertex-color material. Standard leaves and frames across the indoor rooms reference this library through `geometry.sharedAssets`; double doors compose two mirrored/scaled leaf instances. The security door, pantry mesh door and entrance transom also come from the library.

Current room assets are hall v6, living room v4, exterior v3, kitchen v4 and dining room v1. Superseded exports, builders and configurations have been removed. Shared appearances use neutral edge shading rather than baking a different lighting pattern into each copy; rooms still use their existing static-light bake. Frame and panel proportions scale with the doorway.

The source helper `blender_shared/door_assets.py` replaces construction meshes with shared Blender mesh data and writes placement matrices. The bake keeps those objects for editable previews and shadow queries but omits them from room GLBs. Runtime `shared-assets.ts` maps Blender coordinates to Three.js, shares geometry/material references, and batches static instances. Dynamic leaves retain named hinge groups and the existing collision state. Negative mirror transforms are placed on static batch objects, leaving instance matrices positive.

The loader caches one promise per shared library URL, waits for attachment before marking a room navigable, and retains shared resources on room unload. Per-room instance buffers are released then; kit geometry/materials are released at walkthrough teardown. No geometry is duplicated for different hinge sides, no runtime GI is introduced, and starting states remain closed.


### Interior/exterior clearance

The current kitchen uses a shell depth of 5.55 m while retaining its placement and door ports. Its exterior-facing surface is at world x=-6.37, 3 cm behind the facade's inner face at x=-6.4. Room shells must clear the complete exterior wall thickness, not merely offset a coplanar outer face. Validate the exported bounds when placing additional shells near the facade.


### Dining-room shell

`rooms/dining_room` is an independent empty room 037 package. It continues straight beyond the kitchen at `(-0.82,28.9,0)`, yaw `pi/2`, with a 19.2 × 5.55 m footprint and 3.12 m ceiling. Kitchen v4 owns the shared connecting leaf; dining owns its frame and the interactive pantry door. The door library now contains seven meshes, including the distinctive door designs. The house has 14 room GLBs plus one shared kit.

Pantry room 036 is connected beyond dining at `(-0.82,41.7,0)`, yaw `pi/2`. Its gray shell retains the rear blue mesh door as a closed, unassigned pool-route placeholder. See [the pantry package](../rooms/pantry/README.md).

## Shared shell helpers

Kitchen, dining and pantry use `blender_shared.shell` for their repeated scene setup and rectangular shell construction. Each room retains its palette, cameras, doorway ownership and special asset placements in its own builder. Dimensions and named ports come from its `room.json`; builders select ports by ID rather than list position. The interactive-side-door helper currently handles the established right-end door swinging into its owner.

These are optional functions, not a required template for every room. The pool, exterior and furnished rooms can keep independent geometry builders and use only the helpers they need. Refactor validation compared all three rebuilt source scenes, materials, cameras, transforms and door configurations with their previous versions; the accepted baked scenes and browser GLBs did not need regeneration.

## Pool deck

`rooms/pool` is an independent outdoor unit based on room 006, connected to the pantry rear door. Its filled pool and perimeter are collision boundaries; walking is on the deck. The pantry uses `register_hinged` for the shared mesh-door leaf and keeps its matching frame static. Placement and dimensions are provisional; see [pool package](../rooms/pool/README.md).

The [garage and forecourt](../rooms/garage/README.md) connect through the far pool fence opening. Room 016 includes an outdoor approach and a covered empty bay; the exact path placement is provisional.

The [library and complete first-floor shell layout](first_floor.md) are connected: plant room, music room, security corridor, medical room and arcade. All connecting doors start closed. The higher storey and unresolved library spiral staircase remain deferred.

See [source/output ownership and the common build CLI](rebuilding.md) for the authoritative folder structure. Generated room manifests are merged through `scripts/room_config.py`; authored configs are never rewritten by builds.
