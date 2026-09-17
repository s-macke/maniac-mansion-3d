# Cellar rooms and entrance routes

Two independent routes are implemented for layout review:

| Entrance | Destination | Movement |
|---|---|---|
| Entrance hall rear-right door | Cellar / machinery room 008 | Open the shared door, then walk down the right-side stairs |
| Grating behind the left porch bush | Under-house passage 029 | Open the grating, then use the guided crouched passage |

Both destinations begin as empty shells using their original backgrounds and EGA palette. The machinery, long pipework, structural details and furnishings remain deferred. The cellar's left door now leads through the dungeon and laboratories to the meteor chamber. The under-house passage remains separate.

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

## Dungeon and laboratories

The additional shell route is **008 cellar → 004 dungeon → 051 outer laboratory → 030 main laboratory → 031 meteor chamber**. Each room is an independent portal space. All four connecting leaves start closed and open from either side without keys or puzzles. Provisional dimensions and a common cellar floor level avoid inventing unseen stairs.

| Owner | Door | Destination |
|---|---|---|
| Cellar | Left door | Dungeon right rear door |
| Dungeon | Left rear laboratory door | Outer laboratory right door |
| Outer laboratory | Left teal door | Main laboratory right teal door |
| Main laboratory | Left gray door | Meteor chamber right gray door |

The supplied cutaway establishes the underground arrangement; matching door colors in the original backgrounds establish this blockout's door slots. The [original Lucasfilm hint book](https://c64sets.com/maniac_mansion/hint_book.pdf), printed pages 5, 21 and 45–46, supports the basement/dungeon connection, the laboratory approach through a ready room and the meteor room beside the laboratory. Matching background 051 to the outer/ready room remains an artwork-based interpretation, not a verified game-script mapping. The older proposed direct 004 → 030 link omitted this intervening room.

The dungeon uses brown surfaces with blue side walls; laboratory shells use blue floors and side walls with light-blue rear walls. Shared `Dungeon_leaf`, `Lab_leaf` and `Metal_leaf` templates reproduce source EGA door pixels on both faces. Dungeon door reinforcement, stone patterns, windows, machines, chairs and other interior details are deferred. The nested locked-door mechanism is simplified to one shared interactive leaf for this shell pass.

At the user's request, the meteor chamber's former exit door is replaced by a direct ladder portal into the garage floor. The original door and long escape passage are omitted in this walkthrough interpretation. The radiation-marked compartment in 030 is equipment, not an extra room connection.

Build the extension with `./docker-build.sh room ROOM --site` for `dungeon`, `outer_lab`, `main_lab` and `meteor_chamber`. Rebuild `cellar` too when starting from the preceding revision. Direct local review links use `/?room=dungeon` (and the other room IDs). `tests/cellar-extension.spec.ts` checks initially closed doors, one shared owner per connection, forward/reverse portal movement and route isolation; `tests/cellar-extension-browser.spec.ts` walks the whole route and returns.

Extension validation: five Blender room rebuilds (including the updated cellar), the shared door kit, production web build, TypeScript and catalog checks passed. Twelve focused navigation/asset tests passed, followed by a desktop Chrome walkthrough from the cellar to the meteor chamber and back through every new door. All four browser room views were inspected. This extension has not been physically tested on mobile.

The garage escape uses matching ceiling/floor hatches and shared ladder sections. Press E or the climb action in either direction. The garage floor is cut around the hatch, and ordinary walking cannot step into it. The garage remains part of the continuous pool/garage outdoor space. Rebuild `meteor_chamber` and `garage`; the route is covered by the shared ladder tests and `tests/garage-ladder-browser.spec.ts`.

Garage ladder validation: both Blender room builds, production web build, TypeScript and catalog checks passed. All ten focused tests passed, including a Chrome ascent into the garage and return, shared ladder geometry, continuous portal transforms and protection against walking into the garage hatch. The garage hatch browser view was inspected.
