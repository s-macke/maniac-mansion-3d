# Under-house passage — room 029

Furnished from [background 029](../../source/room%20029.png). Long dark passage with eleven yellow supports, red caps and braces, overhead joists, white footings, a brown sill and dense cyan/gray damp grain. The blue plumbing has three horizontal runs with varied risers, elbows, collars and a small right-hand valve. A narrow grid grille sits at the left rear. The central overhead grille has a fine static leak and shallow cyan puddle with ripple lines beneath it. Both grilles are scenery, not additional routes. Fixtures occupy the rear strip, leaving a continuous aisle to the low grating. Original EGA colors and soft baked shading use the existing browser pipeline.

The exterior owns the shared hinged grating. Approach from the left side of the bush, open it with E or the action button, then use **Crawl under house**. The guided movement lowers the viewpoint, follows a path behind the bush and crosses a seamless portal. Inside, standing height returns; face the entrance and use **Crawl outside** to return. Looking around and pausing still work; Reset cancels the crawl.

This is an independent underground space. It is not connected to room 008 or further cellar rooms yet. Rebuild with `./docker-build.sh room under_house`; use `?room=under_house` for direct review. See [cellar routes](../../docs/cellar.md).

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.

Six broad bake positions distribute the fill along the full passage, with a
modest overall brightness increase. No lamps are invented and no runtime lights
are added. The black floor/ceiling and EGA base colors remain; the extra light
makes the timber, pipe fittings and supports easier to read. All new details stay
in the existing rear scenery strip, preserving the aisle and crawl connection.

The inferred opposite wall continues this room’s architectural finish. See the
[complete wall-finish audit](../../docs/opposite_walls.md) for the specific treatment
and the distinction between repeating decoration and unique source details.
