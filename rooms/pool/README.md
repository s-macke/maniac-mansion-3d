# Pool deck and basin — one outdoor unit

Backgrounds 006 (filled deck) and 002 (drained basin) share one independent outdoor builder. It recreates the stone deck, turquoise coping, blue filled pool, metal ladder, pink floating chair silhouette, teal/yellow fence and sparse distant night sky using the original EGA palette and baked lighting. No indoor shell template is used.

The provisional deck is 20 × 11 m; the pool opening is 12.2 × 5.8 m. The deck stays at the pantry floor elevation for continuous exploration. The near curb, matching teal/yellow fence and unseen dimensions are inferred. The far fence opening now connects to the garage forecourt; the around-house connection is deferred. An inferred rear house elevation completes the view behind the pantry doorway.

The pantry owns the shared blue mesh door. Its leaf now separates from the fixed frame, has detail on both faces and starts closed. Open it with E / click / touch to step onto the deck. Pool placement is `(-6.37,44.1,0)`, yaw `pi`; its `pantry_door` meets the pantry rear port at world `(-6.37,40.9,0)`.

The pool starts filled. Face it from a nearby deck edge and press **E**, click or tap **Drain pool**. Water, glints and the floating chair disappear together. At the far-rim ladder, use **Climb into pool**; the same action below becomes **Climb out of pool**. After climbing out, step away from the ladder along the rim and use **Refill pool**. Refill is unavailable in the basin or during a climb. There are no draining puzzles, timers or swimming mechanics.

The basin is 2.8 m below the deck. It is part of this same GLB and room instance, with no separate portal or duplicated pool. Navigation uses the selected floor height and runtime-local drained state; ordinary walking cannot fall over the rim. The original ladder geometry now reaches the bottom. Background 002 supplies the gray reactor with radiation emblem, tall feed pipes, ribbed hose, original pixel depth markings, drain grille, pink plug and wall cracks. These details are authored in `interior.py`; basin-specific collision footprints keep the reactor and plug solid while preserving the ladder landing and central aisle. The equipment stays beneath the filled water surface.

`web/lib/house/pool.ts` owns the toggle and guided same-room ladder motion. `createPoolNavigation` supplies deck/basin collision without shared global state. The bake keeps water and chair meshes in the named `Pool_water` group; the asset loader updates its visibility even after unloading/reloading the room. Wet-only props are excluded from baked shadow queries so they leave no fixed shadow in the empty basin. Leaving the area or resetting position preserves the selected state; reloading the page starts filled.

`build.py` / `room.json` own the geometry, dimensions, ports and lighting. Outputs are `generated/blender/pool/pool_source_v1.blend`, `generated/blender/pool/pool_v1.blend`, `generated/previews/rooms/pool/` and `generated/models/rooms/pool_v1.glb` with compact/gzip companions.

```bash
python3 scripts/build.py room pool
python3 scripts/build.py check
./walkthrough.sh build
```

Start locally at http://127.0.0.1:5174/?room=pool or walk through the pantry. No hosting or commits are part of this change.

`tests/pool-basin.spec.ts` covers state isolation, refill restrictions, continuous climbing, basin support and separate wet geometry. `tests/pool-basin-browser.spec.ts` exercises draining, basin walking, ascent and refilling in Chrome. `scripts/preview_pool.py` reproduces the assembled doorway views.

## Source and generated files

This folder contains only the builder, authored `room.json` and documentation. Original artwork is in `source/`. Generated scenes live in `generated/blender/pool/`; GLBs in `generated/models/rooms/`; previews in `generated/previews/rooms/pool/`; derived door metadata and shading reports in `generated/reports/rooms/pool/`. Builders never write derived data back into `room.json`.

Validated: Blender rebuild, production web build, TypeScript and catalog checks passed. Focused checks cover basin equipment collision, floor support, state isolation and ladder continuity; Chrome completed drain → descend → walk → ascend → refill. Drained, reactor and refilled browser views were inspected. Physical-mobile performance was not tested.

The stars occupy a 40 m hemisphere around the deck, including overhead, instead of a narrow plane just behind the fence. Tiny cyan points and occasional blue crosses retain the source's sparse EGA appearance. The sky geometry is unlit, casts no baked shadows and has no opaque backdrop that could hide the adjoining garage.

## Inferred rear house elevation

At the user's request, `rear_facade.py` fills the previously black house-facing
view with an invented rear elevation. Gray horizontal siding, narrow dark
windows with red/yellow trim, a brick plinth, blue hip roofs, an offset tower
and a shallow gabled pantry canopy borrow the front exterior's visual language.
This is an interpretation of the unseen rear, not an original background or a
claim about the interior layout. It belongs to the pool model so portal room
visibility cannot remove it. The original pantry opening, pool, fence, basin
and garage connection are retained. Decorative windows do not create new
rooms or traversable connections. Geometry stays behind the deck boundary
except shallow trim and the overhead canopy; illumination remains baked.

Validation: pool Blender rebuild, production build, typecheck and catalog pass.
Nine focused asset/navigation checks pass, including the upper facade and a
clear ray through the pantry opening. Chrome completed the pantry round trip,
rear-facade review and drain → basin → refill sequence. The final facade
without an interior blocking volume was rechecked in Chrome. The complete
pool model is 1,373,784 bytes optimized (376,510 bytes gzip). No physical-mobile
validation was performed.

The previously open near edge now has the same pointed teal/yellow fence as
the far edge, following the existing curb and blocked navigation boundary.
It closes the black side view without changing the pantry or garage openings.

The added near fence was rebuilt and inspected in Blender and Chrome. Seven
focused pool/garage checks and the pantry round-trip/browser review pass,
along with the production build and catalog check.
