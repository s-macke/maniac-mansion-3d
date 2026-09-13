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

The [library and complete first-floor shell layout](docs/first_floor.md) are connected: plant room, music room, security corridor, medical room and arcade. All connecting doors start closed. The higher storey and unresolved library spiral staircase remain deferred.

For a fresh Git checkout without generated models or dependencies, follow [the source-only rebuild instructions](docs/rebuilding.md).

Rooms now use [seamless doorway portals](docs/portals.md): overlapping spaces stay separate, while pool and garage remain one continuous outdoor area. Open-door views extend up to three doorways deep.

To regenerate the models and compile the website entirely in Docker, see [the Docker build instructions](docs/docker.md).

The [GitHub Pages workflow](docs/github-pages.md) rebuilds the Blender assets and deploys the static website on pushes to `main`, once Pages is enabled in the repository settings.

For incremental Docker builds, use `./docker-build.sh room kitchen --site`; use `./docker-build.sh all` for every room and the website. [Compose commands](docs/docker.md#everyday-builds-with-compose).
