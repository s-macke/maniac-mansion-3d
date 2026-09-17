# Ladder connections

Four climb routes use shared ladders and continuous hatch portals:

| Lower room | Upper room | Reference |
|---|---|---|
| Heart bedroom / Edna (019) | Safe attic (009) | Original hint book, printed page 43 |
| Radio bedroom / Fred (021) | Green Tentacle’s speaker room (020) | Original hint book, printed pages 37–38 |
| Den / typewriter room (027) | Observatory (028) | Printed pages 39–41; temporary ladder replaces plant climbing in this shell stage |

The [original Lucasfilm hint book](https://c64sets.com/maniac_mansion/hint_book.pdf) confirms these routes. Background 009 is used as the safe-attic reference: boarded wall, left window and portrait on the right. Its position in the supplied cutaway remains tentative; the blue circular telescope overlay is not reproduced as room lighting. Room 020 supplies the speaker-room palette. Furnishings, including the safe, painting and speakers, remain deferred. Hatch placement and dimensions are inferred to suit the walkthrough.

The mummy bathroom has no attic connection. The separate wire attic (015) is accessed from the den/typewriter room (027), according to printed page 39; that route now uses an interactive painted wall panel and [walkable stairs](../rooms/attic_stairs/README.md), followed by a seamless portal into the empty attic shell.

The fourth route is a user-requested direct **meteor chamber (031) ↔ garage (016)** ladder. It replaces the original exit door and long passage; the garage floor has an actual open hatch.

## Controls and movement

Approach and face a ladder, then press **E**, click the action button or tap it on touch devices. The same action at the upper landing descends. A guided climb aligns with the ladder, moves vertically, and steps onto the landing. Looking around remains available; pausing suspends the climb and Reset returns to the starting position. Normal walking cannot step into an open hatch.

This is a continuous portal crossing: the room above/below is visible through the opening during approach and movement. There is no fade or camera cut. The active independent space changes when the **camera** crosses the hatch plane; position and facing transform through the same portal mapping used by doors. Destinations must finish loading before climbing.

## Authoring and reproduction

- `house/layout.json` contains ordinary portal `connections` plus `ladders` movement metadata: lower/upper room and port, safe landing, climb shaft and facing.
- Each room declares a `kind: hatch` port with matching `width`/`depth`, local position and outward normal `[0,0,1]` below or `[0,0,-1]` above.
- `geometry.ceilingHoles` / `floorHoles` cut the actual shell slabs. The lower ceiling has a short shaft up to the portal plane. `geometry.ladders` places the reusable rail/rung sections in both Blender and the browser.
- `web/lib/house/ladders.ts` owns guided motion; `portal-renderer.ts` supports horizontal apertures, clipping and near-plane handling. Hatches use the existing graph for streaming and visibility.
- [Shared ladder kit](../shared/ladders/README.md): one small GLB, loaded once and batched per room. No baked ladder copies remain in room GLBs.

```bash
./docker-build.sh room heart_bedroom
./docker-build.sh room radio_bedroom
./docker-build.sh room safe_attic
./docker-build.sh room tentacle_room --site
```

The shared kit rebuilds automatically when missing or changed. `all` also generates it. Start locally with `./walkthrough.sh`; use `?room=heart_bedroom` or `?room=radio_bedroom` for direct review.

## Verification

`tests/ladders.spec.ts` checks continuous up/down transforms, the camera-plane switch, safe landings, unloaded destinations, hatch collision, real GLB openings and shared geometry batching. `tests/ladders-browser.spec.ts` walks both routes in software-rendered Chrome, checks portal visibility, and exercises a round trip with emulated phone touch controls. This does not establish physical-mobile performance.

The [observatory](../rooms/observatory/README.md) has circular collision, a curved dome with a real open telescope slit, and a floor hatch to the den. The painted wall panel still leads separately to the wire attic.
