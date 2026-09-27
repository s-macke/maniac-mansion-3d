# Maniac Mansion in 3D

Walk through the Maniac Mansion house in your browser. This fan project reimagines the original EGA backgrounds as connected 3D spaces, keeping their distinctive colors, furniture and odd little details while letting you look beyond the original camera angle.

**[Explore the mansion →](https://s-macke.github.io/maniac-mansion-3d/)**

https://github.com/user-attachments/assets/97f56075-cd70-4319-b6c8-3dcc580e6338

## Explore the house

Start outside, walk up the porch steps and open the front doors. From the entrance hall, explore 34 room spaces: the library and kitchen, bedrooms and attics, the observatory, the cellar laboratories, and the pool and garage. Drain the pool to climb down into its basin, or follow a ladder to another floor.

This is a first-person architectural walkthrough. There are no puzzles to solve, inventory items to collect or characters to control. Doors, ladders and hidden passages let you explore without playing through the original game's puzzles.

The rooms are modeled from the original artwork with simple geometry and soft baked lighting. Some dimensions, unseen walls and connections are interpretations: the original painted backgrounds do not describe a single physically consistent building. Doorway portals let rooms retain their own proportions while remaining connected as you walk through them.

## Controls

| Action | Desktop |
|---|---|
| Walk | **WASD**, or **↑ / ↓** |
| Walk faster | Hold **Shift** |
| Look around | Click the scene and move the mouse, or drag; **← / →** turn |
| Open or close doors, use ladders and other interactions | Approach, aim and press **E** |
| Pause / release the mouse | **Esc** |
| Reset position | **R** |

On touch devices, use the directional buttons, drag to look, and tap the contextual action button. Doors start closed; the introductory controls hint disappears after you begin walking.

## Run locally

A fresh checkout contains the source artwork and builders. Generate the models and website first using **Docker with Compose**:

```bash
git clone https://github.com/s-macke/maniac-mansion-3d.git
cd maniac-mansion-3d
./docker-build.sh all
```

The container includes Blender, Python and npm. The first build bakes all rooms and can take tens of minutes. Then serve the finished website with Python 3:

```bash
python3 -m http.server 5174 --bind 127.0.0.1 --directory web/dist/client
```

Open **http://127.0.0.1:5174/**.

If Node.js is installed, `./walkthrough.sh` can serve the built site instead. For building without Docker, see the [local toolchain and rebuild instructions](docs/rebuilding.md).

## How it is built

Blender Python builders generate the room geometry, bake the lighting and export compact GLB models. A Three.js viewer assembles the rooms in the browser, reuses shared door and ladder assets, and loads connected spaces as needed. Lighting is baked into the assets; the browser does not need global illumination.

The result is a static website with no backend. Asset URLs are relative, so the same build can run at a domain root or in a subdirectory. The [GitHub Pages workflow](docs/github-pages.md) generates the Blender assets, compiles and checks the website, and deploys from `main`.

| Location | Contents |
|---|---|
| [`source/`](source/) | Original background references |
| [`rooms/`](rooms/) | Per-room Blender builders, configuration and notes |
| [`shared/`](shared/) | Reusable door and ladder builders |
| [`house/layout.json`](house/layout.json) | Room spaces and connections |
| [`scripts/`](scripts/) | Asset generation, baking and build tools |
| [`web/`](web/) | Browser viewer, navigation and tests |
| `generated/` | Local Blender scenes, models, reports and previews; ignored by Git |

After the initial build, rebuild just one room and the website with:

```bash
./docker-build.sh room kitchen --site
```

For viewer development, use `./walkthrough.sh dev` with Node.js 22.13 or newer. See the [Docker guide](docs/docker.md) for incremental builds and the [architecture guide](docs/architecture.md) for where changes belong.

## Further reading

- [Artwork, palette and reference documentation](docs/README.md)
- [Room connections and uncertain routes](docs/connection_map.md)
- [Doorway portals](docs/portals.md) and [ladder connections](docs/ladders.md)
- [Browser build, controls and validation](web/README.md)
- [Source-only rebuilds](docs/rebuilding.md) and [GitHub Pages deployment](docs/github-pages.md)
- [Project plan and development history](PLAN.md)

## Credits

Maniac Mansion and its original artwork were created by Lucasfilm Games. This is an unofficial fan reconstruction; the original game and artwork belong to their respective rights holders.
