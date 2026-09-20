# Under-house passage — room 029

Furnished from [background 029](../../source/room%20029.png). Long dark passage with blue pipes, yellow supports, red braces, brown sill and cyan damp flecks. Fixtures occupy the rear strip, leaving a continuous aisle to the low grating. Original EGA colors and soft baked shading use the existing browser pipeline.

The exterior owns the shared hinged grating. Approach from the left side of the bush, open it with E or the action button, then use **Crawl under house**. The guided movement lowers the viewpoint, follows a path behind the bush and crosses a seamless portal. Inside, standing height returns; face the entrance and use **Crawl outside** to return. Looking around and pausing still work; Reset cancels the crawl.

This is an independent underground space. It is not connected to room 008 or further cellar rooms yet. Rebuild with `./docker-build.sh room under_house`; use `?room=under_house` for direct review. See [cellar routes](../../docs/cellar.md).

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.
