# Maniac Mansion in 3D

A local first-person walkthrough preserving the supplied EGA artwork and soft baked lighting. The entrance and upstairs landing currently form one continuous architectural unit.

```bash
./walkthrough.sh
```

Open http://127.0.0.1:5174/. See [controls and local build instructions](web/README.md).

- [House layout](house/layout.json): placement and connections of independent room units.
- [Living-room preview](http://127.0.0.1:5174/?room=living_room): start in room 003 and walk through to the entrance hall.
- [Hall package](rooms/connected_hall/README.md): editable scenes, builder, configuration, and previews.
- [Architecture guide](docs/architecture.md): where changes belong and how to add a room.
- [Project plan](PLAN.md) and [reference connection map](docs/connection_map.md).

Original images, current model files and their build dependencies are retained; superseded design iterations have been removed. No gameplay, character, or hosting is required for this prototype.

The walkthrough now starts on the front approach. Walk up the steps, open the double doors and enter the hall. See [the exterior package](rooms/front_exterior/README.md) for source references and build commands. Use `?room=hall` to start inside as before.


## Layout-first rooms

New rooms begin as empty shells with doors; interior details follow after layout review. The [kitchen shell](rooms/kitchen/README.md) is connected through the hall door left of the staircase. Open that door with E or the touch button, or start directly at [the kitchen](http://127.0.0.1:5174/?room=kitchen). All interactive doors start closed.


Standard door models are now maintained in the [shared door kit](shared/doors/README.md). Rooms reference its leaf and frame by placement and size, including mirrored double doors. All interactive doors still start closed.

The [pantry shell](rooms/pantry/README.md) is connected beyond dining; its rear blue mesh door opens onto the [pool deck](rooms/pool/README.md).

The [garage and forecourt](rooms/garage/README.md) connect through the far pool fence opening. Room 016 includes an outdoor approach and a covered empty bay; the exact path placement is provisional.

The [library and complete first-floor shell layout](docs/first_floor.md) are connected: plant room, music room, security corridor, medical room and arcade. All connecting doors start closed. The [upper-floor shells](docs/upper_floor.md) continue through the windowed stair hall, upper corridor and five adjoining rooms. The library spiral staircase remains unresolved.

For a fresh Git checkout without generated models or dependencies, follow [the source-only rebuild instructions](docs/rebuilding.md).

Rooms now use [seamless doorway portals](docs/portals.md): overlapping spaces stay separate, while pool and garage remain one continuous outdoor area. Open-door views extend up to three doorways deep.

To regenerate the models and compile the website entirely in Docker, see [the Docker build instructions](docs/docker.md).

The [GitHub Pages workflow](docs/github-pages.md) rebuilds the Blender assets and deploys the static website on pushes to `main`, once Pages is enabled in the repository settings.

For incremental Docker builds, use `./docker-build.sh room kitchen --site`; use `./docker-build.sh all` for every room and the website. [Compose commands](docs/docker.md#everyday-builds-with-compose).

[Ladder portals](docs/ladders.md) connect the heart bedroom to the safe attic and the radio bedroom to Green Tentacle’s room. Approach and face the ladder, then press E or tap the climb action. Both destinations are empty shells.

The mummy bathroom (024) now connects beyond the exercise/mummy room. The photo darkroom (023) opens from the windowed stair hall one level below the bedrooms. Both are empty shells with closed shared doors.

The [wire attic](rooms/wire_attic/README.md) is reached through the painted wall panel in the den/typewriter room and a short staircase. Open the panel with E or tap it; no puzzle items are needed.

Two [cellar routes](docs/cellar.md) are open for review: the hall’s rear-right door leads down to room 008, and the grating behind the left porch bush leads to passage 029. Both begin as empty, separate shells.
