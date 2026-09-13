# Docker and Compose builds

For automatic builds and deployment on GitHub, see [GitHub Pages](github-pages.md). Its `pages` Docker target exports only the static website; the `artifacts` target below also exports Blender scenes and reports.

The toolchain contains Blender 4.2.3, Node.js 22.22.0, Python/Pillow, DejaVu fonts and Blender's Linux libraries. Blender is downloaded from the official release server and checked against its pinned SHA-256 digest. Host Blender and npm installations are not required.

## Everyday commands

```bash
./docker-build.sh list
./docker-build.sh room kitchen
./docker-build.sh room kitchen --site
./docker-build.sh all
./docker-build.sh site
```

- `room kitchen`: rebuild/bake just the kitchen and optimize its GLB. Build the shared door kit if missing or older than its inputs.
- `room kitchen --site`: additionally compile the whole website using existing outputs for the other rooms.
- `all`: regenerate all rooms, inventories and previews, then compile/typecheck the site.
- `site`: compile/typecheck the website using existing generated models.

On a fresh checkout, run `all` before an incremental website build. After changing shared door geometry, use `all` to keep baked scenes and door metadata consistent. A single-room build does not update other rooms or assembly previews.

`compose.yaml` provides one reusable toolchain service. The shell wrapper prepares writable `.docker/` dependency/cache directories, passes your user/group IDs and invokes `docker compose run --rm`. Generated files belong to your user. Container npm dependencies stay in `.docker/node_modules/`, separate from host `web/node_modules/`.

All paths and build ordering are implemented in **`scripts/build.py`**, shared by local Python, Compose and the Dockerfile. Compose only supplies the environment. Outputs go directly into this checkout's `generated/` and `web/dist/client/`. See [source/output ownership](rebuilding.md).

The wrapper runs the cached `docker compose build builder` before each command. The same static build works at root or in any server subdirectory. No server starts and nothing is published automatically.

## Clean source-only export

With Docker Engine/Desktop and Buildx:

```bash
docker buildx build --platform linux/amd64 --target artifacts \
  --output type=local,dest=exports/docker .
```

`.dockerignore` excludes local outputs and dependencies. The build generates assets from `source/`, `rooms/`, `shared/`, `house/` and `scripts/`, runs npm compilation/typechecking and focused navigation/GLB/shared-door tests, then exports:

| Output | Contents |
|---|---|
| `exports/docker/site/` | Complete static website, including browser models and gzip copies |
| `exports/docker/generated/` | Blender scenes, model exports, manifests, reports, previews and inventory |
| `exports/docker/maniac-mansion-static.zip` | Static website ZIP |

Toolchains, node_modules and transient caches are not exported. Existing working-tree models remain untouched by this clean-export command. The final stage is a file export, not a running web server image. All website URLs are relative; no deployment prefix is configured at build time.

For an unprefixed local preview:

```bash
python3 -m http.server 5175 --bind 127.0.0.1 --directory exports/docker/site
```

This simple server serves ordinary GLBs; the project's existing static server supports gzip negotiation. The pinned Blender archive is Linux x86-64: ARM hosts need Docker's amd64 emulation and will be slower. Full CPU builds include every room and preview and can take tens of minutes; unchanged clean-export builds use Docker's cache.

`--python-exit-code 1`, checked Python subprocesses and shell `set -e` propagate errors. Tests in the Dockerfile inspect navigation and actual GLBs without launching a browser; they are not physical-mobile performance tests.

References: Docker's [one-off Compose commands](https://docs.docker.com/reference/cli/docker/compose/run/), [local output exporter](https://docs.docker.com/build/building/export/), and Blender's [official checksum manifest](https://download.blender.org/release/Blender4.2/blender-4.2.3.sha256).
