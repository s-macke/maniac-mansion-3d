# Working on the Maniac Mansion walkthrough

## Project rules

- Keep the walkthrough local unless the user explicitly requests hosting or deployment.
- Do not stage or commit changes unless explicitly asked.
- Preserve the original EGA artwork, palette and accepted appearance. Use simple geometry and soft baked shading suitable for the browser; no runtime global illumination is required.
- This is exploration only: no gameplay or character work unless requested. Interactive doors start closed.
- New rooms begin as empty shells with doors so the layout can be reviewed before furnishing.
- Use the original `source/` backgrounds and `source/connection_suggestion.png` as the visual and layout basis. Record uncertain connections rather than inventing destinations.

## Documentation map

Read the documents relevant to the task; this index does not require reading every file for each change.

| Document | Purpose |
|---|---|
| [Project README](README.md) | Current walkthrough overview and local launch command |
| [Project plan](PLAN.md) | Scope, decisions and development history; older version references are historical |
| [Reference documentation](docs/README.md) | Index of the artwork inventory, palette and contact sheets |
| [Docker build](docs/docker.md) | Container toolchain, complete asset rebuild and local output export |
| [GitHub Pages](docs/github-pages.md) | Automated Blender build, static deployment and repository setup |
| [Source-only rebuild](docs/rebuilding.md) | Git inputs, ignored outputs and fresh-checkout build order |
| [Architecture](docs/architecture.md) | Room packaging, coordinates, connections, loading, doors and build workflow |
| [Room portals](docs/portals.md) | Independent spaces, doorway rendering, movement transforms and continuous outdoor groups |
| [Connection map](docs/connection_map.md) | Artwork-based topology and unresolved links |
| [Room inventory](generated/reference/room_inventory.md) | Supplied backgrounds and candidate rooms |
| [Scale and style](docs/scale_and_style.md) | EGA palette, display aspect and inferred dimensions |
| [Web README](web/README.md) | Local build, controls, runtime and validation instructions |
| [Connected hall](rooms/connected_hall/README.md) | Entrance, staircase, landing and hall-owned doors |
| [Living room](rooms/living_room/README.md) | Furnished room and corrected arched radio |
| [Front exterior](rooms/front_exterior/README.md) | Porch, roof, bushes and unresolved metal grating |
| [Kitchen](rooms/kitchen/README.md) | Empty shell, facade clearance and dining-door ownership |
| [Dining room](rooms/dining_room/README.md) | Empty shell, provisional proportions and pantry boundary |
| [Pantry](rooms/pantry/README.md) | Gray shell and shared doors to dining and pool |
| [Pool deck](rooms/pool/README.md) | Outdoor deck, filled pool and pantry connection |
| [Garage and forecourt](rooms/garage/README.md) | Outdoor approach and empty covered garage bay |
| [First-floor layout](docs/first_floor.md) | Library, five upstairs shells, door ownership and deferred stairs |
| [Shared doors](shared/doors/README.md) | Reusable leaf/frame authoring, mirroring and runtime lifecycle |

Keep affected documentation current when changing paths, workflow, room connections or accepted behavior. Prefer updating the current description over appending contradictory version notes.

## Files and ownership

- `source/` contains original artwork and the connection drawing; preserve these inputs.
- `rooms/<room>/` contains only source builders, authored `room.json` and README. `shared/doors/` contains the shared kit builders.
- `house/layout.json` assembles independent room units in the browser. The entrance and landing remain one hall unit.
- `scripts/build.py` is the common local, Docker and Compose entry point. `scripts/rooms.py` handles catalog validation and browser synchronization; `scripts/room_config.py` merges authored configs with generated manifests.
- Never write generated door transforms into authored `room.json`. Builders emit `generated/reports/rooms/<room>/manifest.json` through `save_generated()`.
- All generated Blender scenes, GLBs, reports and previews belong under `generated/`. This includes editable scenes with `_source_` in the filename.
- Browser model copies, generated adapters/registry, dependencies and web build output remain ignored under `web/`. Do not edit generated files to implement lasting changes.
- Navigation lives in `web/lib/rooms/`; assembly, streaming and doors in `web/lib/house/`.
- Preserve current accepted outputs when relocating files. Do not recreate superseded design iterations.

## Build and verification

```bash
./docker-build.sh list
./docker-build.sh room kitchen --site
./docker-build.sh all
```

Local equivalents use `python3 scripts/build.py`; set `BLENDER_BIN` to the Blender executable. See [source-only rebuilding](docs/rebuilding.md) and [Docker](docs/docker.md) for prerequisites, artifact exports and verification.

Local review URL: `http://127.0.0.1:5174/`. Room query values select starting positions in the same assembled house.

Run focused checks appropriate to the change. Do not claim browser interaction or physical-mobile validation from navigation tests or static compilation alone. Do not rebuild unchanged artwork for documentation-only edits.
