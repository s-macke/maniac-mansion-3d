# Maniac Mansion — local house walkthrough

A local, static first-person walkthrough of the exterior, connected entrance/landing, living room, kitchen and dining room. No backend, runtime lights, shadows, or global illumination are used. Nothing has been committed or published.

## Run

From the project root:

```bash
./walkthrough.sh
```

Open **http://127.0.0.1:5174/**. The first run builds if needed; subsequent runs serve `web/dist/client/` using Node's built-in HTTP server. Node 22.13+ is needed for building. A finished `dist/client/` can also be served by any ordinary static web server without Node or npm.

`PORT=8080 ./walkthrough.sh` selects another port. Stop with Ctrl+C.

The build uses Vite and React directly. No OpenAI Sites plugin, hosting configuration, or hosting account is required.

## Controls

- Walking starts automatically when the room loads.
- The controls hint appears only on desktop and disappears after 3 metres of actual walking.
- Click the scene to capture the mouse, or drag to look.
- **WASD** walks; the **mouse** looks around. Hold either **Shift** key to move twice as fast (5 m/s instead of 2.5 m/s). Release it to return to normal speed. Ladder and crawl animations keep their normal speed.
- **Arrow Up/Down** walk, **Arrow Left/Right** turn.
- **Esc** pauses and releases the mouse; click or tap the scene to continue.
- **R** returns to the initial viewpoint.
- If mouse capture is unavailable, drag to look instead.
- On touch devices, touching anywhere on the left half creates a floating joystick at that point. Deflection controls direction and speed; releasing stops movement and hides the stick. Swipe on the right half to look, independently of the movement thumb. Right-side taps and the contextual action button still interact with doors and ladders. Cancelling a touch, pausing, resizing or resetting clears the stick.
- The GitHub icon and link at the top right open the repository in a new tab and pause the walkthrough.

The hall connects to the exterior, living room and kitchen; the kitchen connects to the dining room. Unassigned doors remain boundaries. There is no jumping, gameplay, or character. The curved stairway connects the entrance to the upstairs landing at 3.36 m. Walk around the gallery and look down into the entrance, then return along the same stairs. Collision uses a player radius, room limits, furniture footprints, stair rails, and a continuous stair surface, rather than every decorative mesh triangle.

## Edit and build

```bash
./walkthrough.sh dev       # development server on 127.0.0.1:5173
./walkthrough.sh build     # regenerate static output after edits
```

Application: `web/components/walkthrough.tsx`. Room collision: `web/lib/rooms/connected_hall.ts`. House assembly, transforms, and movement: `web/lib/house/`. The source of truth is `house/layout.json` plus each room's `room.json`; `prebuild` and `predev` validate these and generate the browser manifest and adapter registry.

The hall asset is `./models/connected_hall/connected_hall_v6.glb`, losslessly compacted from `generated/models/rooms/connected_hall_v6.glb`. The current room space and connected neighbors load independently. Doorway portals isolate overlapping rooms, with views up to three doors deep; pool and garage share a continuous space. See [portal architecture](../docs/portals.md) and [the architecture guide](../docs/architecture.md).

The viewer uses sRGB output and no tone mapping, preserving the baked appearance. The static room is not continuously redrawn while paused. At higher screen densities, rendering is capped at 1.5× device pixel ratio.

## Validation

With a local server running:

```bash
cd web
npm run typecheck
WALKTHROUGH_URL=http://127.0.0.1:5174 npm test
```

The tests use an isolated headless Chrome at `/usr/bin/google-chrome`. Set the executable in `playwright.config.ts` if Chrome is elsewhere. They cover automatic room entry, the distance-based controls hint, movement, mouse look, pause/reset/resume, mouse-capture fallback, failed downloads, mobile layout, wall/furniture collision, the curved stairs in both directions, gallery rails, overlapping floors, and walking upstairs in the browser. Software rendering is used for repeatability; this is not a measurement of normal GPU performance. Screenshots are in `web/test-results/`.

The optional feature-detected WebMCP position-read/reset tools share the interface's state. Native WebMCP support was unavailable in this environment; the walkthrough does not depend on it.

Validated on 2026-09-10: static production build and TypeScript checks passed; all 15 browser/collision/assembly tests passed against the static server. The optimized GLB preserves every triangle position and baked color exactly.

## Hosting under any server folder

Build once with `./walkthrough.sh build`, then upload the contents of `web/dist/client/` to any server directory. The same output works at `/`, `/maniac-mansion-3d/`, or `/games/mansion/` without rebuilding or configuring a URL prefix. JavaScript, CSS, the favicon and room-model downloads all use relative URLs.

Use a directory URL ending in `/` (ordinary static servers redirect to this form), or open `index.html` explicitly. Query links such as `?room=kitchen` work in either form. The local server preserves query parameters when redirecting a directory URL. HTTP/HTTPS hosting is required; opening the files directly with `file://` is not supported.

The build uses Vite's React plugin and exports directly to `dist/client/`. There is no server-rendering or export-rewrite step. Blender generation and the prebuild/predev room synchronization remain unchanged.

After building, run `cd web && npx playwright test tests/relative-hosting.spec.ts` from the project root to check one output at all three URL depths. The test starts an isolated temporary static server and checks model loading, movement, doors, refreshes, direct index links and directory redirects.

## Connected living room

Open http://127.0.0.1:5174/?room=hall for the hall, or http://127.0.0.1:5174/?room=living_room to start in the living room. Room assets load independently. Walk through the hall’s right-side doorway, or return through the living room’s left doorway. The same staircase continues upstairs to the landing. Doorway crossings are blocked until the neighboring asset is ready.

The default start is now the exterior approach. `?room=front_exterior`, `?room=hall`, and `?room=living_room` choose starting positions in the same assembled house. Climb the porch steps and open the front double doors to enter the hall. Exterior and hall/living-room assets retain independent downloads and collision definitions.


## Door controls

Aim at the nearby front double doors or hall/living-room door and press **E**, click while in mouse look, or tap the door / contextual button. Doors start closed, swing smoothly, and pause before hitting the walker. Unconnected doors stay closed. Reset position preserves door state; reloading the page resets it.

The hall and kitchen keep named hinge nodes for the shared moving leaves. Static room shading remains baked, and the browser adds no real-time shadows or GI. See `lib/house/doors.ts` and `lib/house/door-view.ts` for the reusable behavior.


Kitchen shell: `/?room=kitchen` starts in the empty kitchen within the assembled house. From the hall, use the door left of the staircase. Its shared leaf starts closed; open the far door to enter the dining room.


## Shared door assets

The house loads 34 room GLBs plus shared door and ladder libraries at `/models/shared/standard_doors_v1.glb`. Hall v6, living-room v4, kitchen v4, dining-room v1 and pantry v1 use this kit; the exterior uses v3. The kit contains a standard leaf and frame, reused by size and mirrored for handle side. Special door artwork also comes from the library.

Moving leaves share geometry/materials, while static frames and leaves use per-room instanced batches. Unloading a room keeps the kit cached and retains interactive door state. A room waits for its door assets before allowing entry. See [door authoring and lifecycle](../shared/doors/README.md).


Dining-room shell: `/?room=dining_room` starts inside room 037. From the kitchen, open the far door; the pantry door at the other end opens into room 036. The house now has 34 room GLBs plus the shared door and ladder kits. Kitchen v4 retains the facade-clearance fix while owning this new interactive leaf.

Pantry room 036 is connected beyond dining at `(-0.82,41.7,0)`, yaw `pi/2`. Its rear blue mesh door now opens onto the pool deck. See [the pantry package](../rooms/pantry/README.md).

Pool deck: `/?room=pool` starts outdoors beside the filled pool. Open the pantry mesh door to reach it from the house. Use E/tap near the edge to drain or refill. Draining exposes the walkable basin and enables the far-rim ladder; refill is available only from the deck away from the ladder. The deck and basin remain one room with static baked lighting.

The [garage and forecourt](../rooms/garage/README.md) connect through the far pool fence opening. Room 016 includes an outdoor approach and a covered empty bay; the exact path placement is provisional.

The [library and complete first-floor shell layout](../docs/first_floor.md) are connected: plant room, music room, security corridor, medical room and arcade. All connecting doors start closed. The upper storey now connects through the windowed hall and upper corridor; the library spiral staircase remains deferred.

Focused first-floor verification:

```bash
npm run typecheck
npx playwright test tests/first-floor.spec.ts tests/doors.spec.ts tests/shared-assets.spec.ts
WALKTHROUGH_URL=http://127.0.0.1:5174 npx playwright test tests/downloads.spec.ts
```

These checks exercise navigation, actual GLB geometry, door reuse and HTTP downloads. They do not claim interactive-browser or physical-mobile performance validation. `scripts/preview_first_floor.py` renders the assembled doors and room connections from the current baked Blender scenes.

[Ladder portals](../docs/ladders.md) connect the heart bedroom to the safe attic and the radio bedroom to Green Tentacle’s room. Approach and face the ladder, then press E or tap the climb action. Both destinations are empty shells.
