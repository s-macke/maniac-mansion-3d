# Observatory — room 028

Circular empty shell based on [the original observatory](../../source/room%20028.png). The floor is light blue; the curved walls and dome use cyan with aqua opening edges. The dome has an actual open telescope slit, not a black panel or an opaque window. Telescope, controls, poster and other equipment are deferred.

## Shape and openings

`build.py` constructs a 64-sided circular floor and wall with a 16-ring elliptical dome. The provisional interior radius is 4.2 m, the wall spring line 2.05 m and the dome crown 4.8 m. A 45-degree radial slit faces the rear-right quadrant and extends from its 1.25 m sill to the crown. Neither dome nor outer shell covers this sector. These dimensions and orientation interpret the 2D artwork for first-person review.

The floor's rectangular den hatch is physically cut out. The floor is clipped to the circular boundary around that hole; no rectangular slab, hidden floor or ceiling spans it. Navigation follows the circular footprint and blocks ordinary walking into the hatch or through the slit sill.

Curved surfaces opt into analytic normals in the shared bake helper. Illumination is still stored as vertex colors with unlit materials, so the browser needs no real-time lighting or GI. Other room surfaces keep their existing baking behavior.

## Access

The [original Lucasfilm hint book](https://c64sets.com/maniac_mansion/hint_book.pdf), printed pages 39–41, places the observatory opening above the den's plant. It is separate from the painted-panel route to the wire attic. The former plant-room-to-observatory guess is superseded.

For this empty-shell stage, a shared ladder stands in for climbing the grown plant. Approach the rear-right ladder in the den/typewriter room and use **Climb up** (E, click or tap). The hatch uses the existing continuous ladder portal, with a return **Climb down** action. No growing-plant puzzle, character or teleport cut is introduced. The hatch position is inferred, since its upper side is not clearly shown in background 028.

```bash
./docker-build.sh room typewriter_room
./docker-build.sh room observatory --site
```

Local starts: `/?room=observatory` or `/?room=typewriter_room`. Sources stay in `rooms/observatory/`; Blender scenes, GLBs and previews are generated under `generated/`.

## Checks

`tests/observatory.spec.ts` checks circular collision, floor support, headroom and actual ray clearance through the slit and hatch. `tests/ladders.spec.ts` covers the den/observatory continuous climb and return, as well as the shared ladder geometry and real openings. `tests/observatory-browser.spec.ts` exercises the route in Chrome and captures views of the dome and hatch.

Validated: both Blender builds, production web build, TypeScript and house checks; nine focused checks, including a Chrome climb up and back down with visible portals and verification that the mistaken left-hand ceiling opening is closed. Dome and hatch browser screenshots were inspected. Physical-mobile performance was not tested.

The temporary den ladder faces the back wall beneath the visible ceiling opening above the right-hand blue pot, beside the painted wall (local X 3.1, Y 4.52). Its ceiling opening and the observatory ladder align through the portal; the painted-panel door remains on the right wall.
