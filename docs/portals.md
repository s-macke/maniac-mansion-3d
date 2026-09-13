# Room spaces and seamless portals

Each room is an independent space by default. Geometry in another space may occupy the same coordinates without becoming visible or supplying a floor. Room-local navigation functions and the generated Blender models are unchanged.

## Authoring connections

`house/layout.json` version 2 keeps the room placements and connection endpoints. Connected ports require a threshold centre, unit outward normal, matching width and a height sufficient for the walker. Their `state: open` means a usable connection exists; the independent door animation still starts closed.

Connections between different spaces do not need aligned world coordinates. The runtime derives a translation and yaw rotation that maps the source threshold to the destination threshold, source outward to destination inward, and relative floor height without scaling. Placements remain useful for authoring and overview previews, but do not imply visibility between spaces.

The explicit `spaces` list groups `pool` and `garage` as `pool_garage`, with pool as the authoring anchor (`origin`). Their existing relative placements are retained, and their path must stay physically aligned. Group membership is exclusive. The hall/landing/staircase is already one room and needs no grouping. Unassigned doors and original windows remain unchanged.

## Movement and doors

The runtime tracks `activeRoom` and `activeSpace`. It evaluates the existing floor and wall rules only inside that space. A doorway bridge provides clearance through conservative wall insets only when both sides are loaded. Movement is subdivided to prevent tunnelling; crossing transforms position, floor elevation, facing and remaining displacement. Reset and `?room=...` select an explicit starting space.

`moveWalker()` also returns `yawDelta`, `heightDelta` and `crossed` for camera continuity. `activate()` is for explicit placement/reset/test setup, not automatic bounds-based room detection. Tests that position a walker directly must also select its room.

One persistent door state remains owned by its original room. Opposite-side leaf proxies share the original geometry/materials and copy its animated transform. They are visual instances, not extra doors or independent states. Ray targeting and collision transform into the owning room, so doors work from either side and stop swinging before the walker. Walls still occlude interaction.

## Rendering and residency

Only the current space is drawn directly. Visible doorways render destination spaces into cropped render targets, using transformed cameras and clipping at the destination entrance plane. The texture is projected back into the source aperture; real walls, frames and leaves provide depth occlusion. Cropping preserves projected pixel detail without rendering a full-screen texture for every small doorway. The main near plane shrinks near a threshold to avoid a blank flash before crossing.

`portalDepth: 3` bounds rendering to three consecutive doorways. The reverse entrance is excluded from recursion; offscreen apertures are culled conservatively. At the depth limit further apertures show the dark background, without changing or deleting their door leaves. Closed owner-side doors skip their concealed render pass. Opposite-side closed doors may still need a destination pass to show their inset geometry.

Current-space rooms and immediate neighbors are resident. Visible deeper portal chains request more rooms. Unwanted rooms remain cached for ten seconds; render targets no longer used by the current view are disposed immediately. Shared kit resources remain reusable until the walkthrough is disposed. Crossing into an unloaded or failed destination is blocked; a loading failure preserves the current space and displays the existing reload message.

The renderer uses existing unlit, baked materials, sRGB output and no tone mapping or dynamic lighting. `.viewport`'s diagnostic `data-walker` includes current room/space, loaded rooms, portal passes and target count. These are debugging data, not extra interface controls.

## Validation

- `tests/portals.spec.ts`: translated/rotated/elevated connections, reverse movement, unloaded/closed gates, overlap isolation, continuous outdoors, camera mapping and clipping.
- `tests/portal-rendering.spec.ts`: an isolated Vite fixture loads actual GLBs and compares pixels before/after relocating the kitchen, checks three-deep views and render-target release. Fixture pages are not part of the production build.
- Existing movement, shared-door and room tests select their space explicitly when placing a walker at test coordinates. `tests/relative-hosting.spec.ts` checks the portal-enabled static build at three URL depths.

Browser tests use software-rendered Chrome. Their render counts and touch checks do not establish performance on physical mobile hardware. Blender files do not need rebuilding for this runtime change.
