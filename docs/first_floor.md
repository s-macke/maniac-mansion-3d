# Library and first-floor layout

The first floor means the storey immediately above the ground floor, at 3.36 m. Its existing landing remains part of the connected hall. Six independent room packages are added: the ground-floor library plus five rooms upstairs. Together the house now has 14 room GLBs and one shared door kit. The browser combines them using `house/layout.json`; Blender files remain independently editable and reproducible.

| Room | Background | Access | Moving door owner |
|---|---|---|---|
| Library | 005 | Living-room double doors | Living room |
| Plant room | 014 | Left landing door | Hall |
| Music room | 017 | Right landing door | Hall |
| Security corridor | 013 | Reinforced landing door | Hall |
| Medical room | 022 | Left ordinary corridor door | Security corridor |
| Arcade | 018 | Right ordinary corridor door | Security corridor |

All new rooms are shells, with artwork-derived EGA floor and wall colors, shared doors and baked soft shading. No furnishings, gameplay, characters or runtime global illumination are added. Every interactive door starts closed and opens/closes from either side. The reinforced door retains its pixel artwork on both faces and now has a separate reusable leaf and frame.

Walk up the main staircase to reach the new floor. The corridor staircase rises a further 3.36 m and ends at a closed doorway for the next storey. Background 012 and the higher floors are outside this pass. The library spiral stair's destination remains unresolved in the supplied connection drawing, so that stair is deferred rather than assigned a destination.

Connections follow the supplied cutaway and backgrounds. Footprints, unseen walls and metric dimensions are inferred. The 8 × 3.95 m music room clears the living-room ceiling and the corridor stairwell; the plant-room doorway replaces the facade section now inside that wing. The 13.2 m-wide security corridor clears the plant wing. The canopy and two porch columns beneath that wing end below its floor. The medical room and arcade have separate, non-overlapping footprints. These decisions can be adjusted as the rest of the house is mapped.

`rooms/<id>/room.json` stores dimensions and wall-port declarations in `shell.entries`. `scripts/blender_shared/layout_shell.py` creates the simple shell, openings, trim, shared doors and optional corridor staircase. Individual navigation adapters enforce floor elevation, walls and stair support. The existing furnished rooms retain their own builders.

Local starting links: `?room=library`, `plant_room`, `music_room`, `security_hall`, `medical_room` and `arcade`. The normal exterior start is unchanged.

## Validation and downloads

The final static build, typecheck and 15 focused door, navigation, GLB-geometry and exterior checks pass. Additional ground-floor regression checks passed during integration. HTTP checks verify all 15 model downloads with and without gzip, including exact byte comparison against the optimized exports. Blender previews of the assembled closed/open connections were inspected; no new interactive-browser or physical-mobile performance test was run.

Checks cover the entire main-stair route into every upstairs room and back, stair headroom, visible floor elevations, non-overlapping footprints, closed/open door targeting from both sides, and shared-kit load/unload behavior.

| New package | Optimized GLB | Gzip download |
|---|---:|---:|
| Library | 107,560 B | 34,180 B |
| Plant room | 57,148 B | 17,681 B |
| Music room | 61,848 B | 19,503 B |
| Security corridor | 190,116 B | 57,196 B |
| Medical room | 55,492 B | 17,076 B |
| Arcade | 54,872 B | 16,766 B |

The six new room downloads total 162,402 bytes compressed. The shared seven-mesh door library is 400,872 bytes optimized / 75,075 bytes gzip, downloaded once for the house.

Reproduce assembled views with:

```bash
./blender-4.2.3-linux-x64/blender -b -t 8 --python scripts/preview_first_floor.py
```

Current previews include [the landing](../generated/previews/assembly/landing_closed_v1.png), [plant-room entry](../generated/previews/assembly/plant_door_open_v1.png), [the security corridor](../generated/previews/assembly/security_rooms_closed_v1.png), and [library entry](../generated/previews/assembly/library_door_open_v1.png).
