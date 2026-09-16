# Cellar entrance routes

Two independent routes are implemented for layout review:

| Entrance | Destination | Movement |
|---|---|---|
| Entrance hall rear-right door | Cellar / machinery room 008 | Open the shared door, then walk down the right-side stairs |
| Grating behind the left porch bush | Under-house passage 029 | Open the grating, then use the guided crouched passage |

Both destinations begin as empty shells using their original backgrounds and EGA palette. The machinery, long pipework, structural details and furnishings remain deferred. The cellar's left door is a closed placeholder. The two underground routes are not joined; further connections will be established separately.

## Hall and cellar

The hall owns `cellar_door`, attached to `rear_right`, closed initially. The cellar's `higher_floor` portal is on its stair landing. Room placement puts the cellar floor at -3.36 m and the landing at hall elevation. Walking is continuous down and back up; no guided action or camera cut is used on the stairs.

## Low bush grating

The existing bushes and the 1.25 × 0.72 m grating aperture are retained. The fixed exterior frame remains in the exterior model; its movable bars use `Grating_leaf` in the shared door kit. The leaf swings inward into the recess. The solid black backing is removed so the destination can render through it. Its `seeThrough` port keeps the destination view visible between the bars even while the grille is closed.

A `kind: crawl` portal uses the normal doorway renderer but excludes standing movement. `house/layout.json` declares `crawls` with safe landing positions and a path around the bush's edge. `web/lib/house/crawls.ts` lowers the camera to 0.42 m, follows this path, maps position/facing at the portal plane, then restores the 1.62 m standing eye height. Destination assets and the fully open grating are required before crossing. There is no fade, teleport cut, puzzle or character animation.

From the side of the bush, face the grating and press E or use the action button to open it. Use the resulting **Crawl under house** action. From inside, face the opening and use **Crawl outside**. Clicking the visible grille uses normal door interaction, including closing it. Pause suspends guided motion; Reset cancels it.

The under-house floor is provisionally at -1.2 m, with a small raised sill matching the existing exterior opening. Independent room spaces keep the standing-height interior clear of unrelated porch geometry.

## Build and verification

```bash
./docker-build.sh room cellar
./docker-build.sh room under_house
./docker-build.sh room connected_hall
./docker-build.sh room front_exterior --site
```

The common build creates the new shared grille template automatically. Generated files remain ignored. `tests/cellar.spec.ts` covers closed entrances, staircase descent/ascent, crouched camera continuity, safe return landings, loading gates and route isolation. `tests/cellar-browser.spec.ts` exercises both routes in the local browser. The existing exterior tests retain bush collision checks. Browser automation does not establish physical-mobile performance.

Validated locally: Blender builds for both new shells, the hall, exterior and shared door kit; production web build; TypeScript checking; house catalog checks; and all six cellar navigation/browser tests. Browser checks cover descending and returning through the hall, crawling both ways through the grating, and opening/crawling with emulated mobile touch controls. Existing door, ladder, shared-asset, upper-floor, attic, exterior and first-floor checks also passed during this change.
