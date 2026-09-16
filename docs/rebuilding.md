# Source files and reproducible outputs

```text
source/                    Original game backgrounds and connection_suggestion.png
rooms/<room>/              build.py, authored room.json, README.md
shared/doors/, ladders/    Shared asset builders and documentation
house/layout.json          Placement and connections
scripts/build.py           Common local/Docker build command
scripts/blender_shared/    Blender construction and baking helpers
web/                       Website source, tests and npm lockfile
generated/
  blender/                 Generated source and baked .blend scenes
  models/                  GLBs, optimized copies and gzip files
  previews/                Room, shared-asset and assembly renders
  reports/rooms/<room>/     manifest.json, shading and layout reports
  reference/               Inventory, exact palette and contact sheets
```

Git tracks the authored inputs and ignores `generated/`, web build products, dependencies and caches. Files named `_source_*.blend` are generated editable scenes, not the authoritative recipe. Durable geometry changes belong in the builders. Hand-authored assets that cannot be regenerated must be kept outside `generated/` and included in both Git and the Docker context.

`room.json` stores authored dimensions, palette choices, navigation, ports, bake settings and output paths. The builder writes derived door pivots, mesh placements and collision bounds to `generated/reports/rooms/<room>/manifest.json`. The catalog merges this metadata with authored inputs for baking and browser synchronization. The generated manifest is required: missing room output is an error, not an invitation to reuse stale values from source config.

## Docker / Compose

No host Blender or npm is required. See [Docker instructions](docker.md).

```bash
./docker-build.sh all
./docker-build.sh room kitchen --site
```

## Local equivalent

Install Blender 4.2.3, Python 3 with Pillow and DejaVu Sans, and Node.js >=22.13.0 with npm. The inventory renderer expects `/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf`.

```bash
export BLENDER_BIN="$PWD/blender-4.2.3-linux-x64/blender"
python3 scripts/build.py list
python3 scripts/build.py all
./walkthrough.sh
```

`all` creates the shared door and ladder kits, all room scenes/GLBs, inventories and assembly previews, then runs `npm ci`, compilation and typechecking. It stops immediately on failure. Use `all --assets-only` to omit npm, `room kitchen` for one room, `room kitchen --site` to also update the browser build, or `site` to compile existing models. `check`, `sync`, `doors` and `export exports/local` are also available through the same command. `scripts/rooms.py` is the lower-level catalog/sync helper; it contains no second full-build recipe.

`npm run build` calls `scripts/build.py sync` before compilation. Browser models and TypeScript adapters are generated copies under `web/`; they remain ignored. A clean checkout must generate Blender outputs before npm compilation. Baking can take several minutes per detailed room.

Existing output filenames retain their version suffixes to avoid changing model URLs during this refactor. The directory boundary establishes ownership; renaming rooms or changing geometry is unnecessary.
