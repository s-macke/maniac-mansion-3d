# Maniac Mansion — local house walkthrough

A local, static first-person walkthrough of the exterior, connected entrance/landing, living room, kitchen and dining room. No backend, runtime lights, shadows, or global illumination are used. Nothing has been committed or published.

## Run

From the project root:

```bash
./walkthrough.sh
```

Open **http://127.0.0.1:5174/**. The first run builds if needed; subsequent runs serve `web/dist/client/` using Node's built-in HTTP server. Node 22.13+ is needed for building. A finished `dist/client/` can also be served by any ordinary static web server without Node or npm.

`PORT=8080 ./walkthrough.sh` selects another port. Stop with Ctrl+C.

The build uses Vite and vinext directly. No OpenAI Sites plugin, hosting configuration, or hosting account is required.

## Controls

- Walking starts automatically when the room loads.
- The controls hint disappears after 3 metres of actual walking.
- Click the scene to capture the mouse, or drag to look.
- **WASD** walks; the **mouse** looks around.
- **Arrow Up/Down** walk, **Arrow Left/Right** turn.
- **Esc** pauses and releases the mouse; click the scene or **Resume** to continue.
- **R** or **Reset position** returns to the initial viewpoint.
- If mouse capture is unavailable, drag to look instead.
- Touch devices get directional buttons and drag-to-look.

The hall connects to the exterior, living room and kitchen; the kitchen connects to the dining room. Unassigned doors remain boundaries. There is no jumping, gameplay, or character. The curved stairway connects the entrance to the upstairs landing at 3.36 m. Walk around the gallery and look down into the entrance, then return along the same stairs. Collision uses a player radius, room limits, furniture footprints, stair rails, and a continuous stair surface, rather than every decorative mesh triangle.

## Edit and build

```bash
./walkthrough.sh dev       # development server on 127.0.0.1:5173
./walkthrough.sh build     # regenerate static output after edits
```

Application: `web/components/walkthrough.tsx`. Room collision: `web/lib/rooms/connected_hall.ts`. House assembly, transforms, and movement: `web/lib/house/`. The source of truth is `house/layout.json` plus each room's `room.json`; `prebuild` and `predev` validate these and generate the browser manifest and adapter registry.

The hall asset is `/models/connected_hall/connected_hall_v6.glb`, losslessly compacted from `generated/models/rooms/connected_hall_v6.glb`. Nearby room units load independently and release GPU resources when unloaded. See [the architecture guide](../docs/architecture.md) for independent room builds and connection markers.

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

## Hosting under a subdirectory

For **https://simulationcorner.net/maniac-mansion/**, build with:

```bash
BASE_PATH=/maniac-mansion ./walkthrough.sh build
```

Upload the contents of `web/dist/client/` to the server's `maniac-mansion/` directory. The path is a build-time setting: rebuild when changing it. Both framework JavaScript/CSS and room-model downloads use this prefix. No server-side application is required.

For the existing localhost root URL, rebuild without `BASE_PATH`:

```bash
./walkthrough.sh build
./walkthrough.sh
```

## Connected living room

Open http://127.0.0.1:5174/?room=hall for the hall, or http://127.0.0.1:5174/?room=living_room to start in the living room. Room assets load independently. Walk through the hall’s right-side doorway, or return through the living room’s left doorway. The same staircase continues upstairs to the landing. Doorway crossings are blocked until the neighboring asset is ready.

The default start is now the exterior approach. `?room=front_exterior`, `?room=hall`, and `?room=living_room` choose starting positions in the same assembled house. Climb the porch steps and open the front double doors to enter the hall. Exterior and hall/living-room assets retain independent downloads and collision definitions.


## Door controls

Aim at the nearby front double doors or hall/living-room door and press **E**, click while in mouse look, or tap the door / contextual button. Doors start closed, swing smoothly, and pause before hitting the walker. Unconnected doors stay closed. Reset position preserves door state; reloading the page resets it.

The hall and kitchen keep named hinge nodes for the shared moving leaves. Static room shading remains baked, and the browser adds no real-time shadows or GI. See `lib/house/doors.ts` and `lib/house/door-view.ts` for the reusable behavior.


Kitchen shell: `/?room=kitchen` starts in the empty kitchen within the assembled house. From the hall, use the door left of the staircase. Its shared leaf starts closed; open the far door to enter the dining room.


## Shared door assets

The house loads 14 room GLBs plus one shared door library at `/models/shared/standard_doors_v1.glb`. Hall v6, living-room v4, kitchen v4, dining-room v1 and pantry v1 use this kit; the exterior uses v3. The kit contains a standard leaf and frame, reused by size and mirrored for handle side. Special door artwork also comes from the library.

Moving leaves share geometry/materials, while static frames and leaves use per-room instanced batches. Unloading a room keeps the kit cached and retains interactive door state. A room waits for its door assets before allowing entry. See [door authoring and lifecycle](../shared/doors/README.md).


Dining-room shell: `/?room=dining_room` starts inside room 037. From the kitchen, open the far door; the pantry door at the other end opens into room 036. The house now has 14 room GLBs plus the shared door kit. Kitchen v4 retains the facade-clearance fix while owning this new interactive leaf.

Pantry room 036 is connected beyond dining at `(-0.82,41.7,0)`, yaw `pi/2`. Its rear blue mesh door now opens onto the pool deck. See [the pantry package](../rooms/pantry/README.md).

Pool deck: `/?room=pool` starts outdoors beside the filled pool. Open the pantry mesh door to reach it from the house. Water and fences are solid boundaries. The scene uses static baked lighting and an opaque blue water surface.

The [garage and forecourt](../rooms/garage/README.md) connect through the far pool fence opening. Room 016 includes an outdoor approach and a covered empty bay; the exact path placement is provisional.

The [library and complete first-floor shell layout](../docs/first_floor.md) are connected: plant room, music room, security corridor, medical room and arcade. All connecting doors start closed. The higher storey and unresolved library spiral staircase remain deferred.

Focused first-floor verification:

```bash
npm run typecheck
npx playwright test tests/first-floor.spec.ts tests/doors.spec.ts tests/shared-assets.spec.ts
WALKTHROUGH_URL=http://127.0.0.1:5174 npx playwright test tests/downloads.spec.ts
```

These checks exercise navigation, actual GLB geometry, door reuse and HTTP downloads. They do not claim interactive-browser or physical-mobile performance validation. `scripts/preview_first_floor.py` renders the assembled doors and room connections from the current baked Blender scenes.
