# Meteor chamber

Furnished from [background 051](../../source/room%20051.png): riveted panels, colored pipes, lever cabinet, horizontal tank and suspended meteor apparatus with pincers. This is the final cellar room, after the three-apparatus main laboratory (030). Its garage ladder and landing remain clear. Original EGA colors and soft baked shading use the existing browser pipeline.

See [cellar layout](../../docs/cellar.md) for door ownership, route evidence and unresolved exits. Dimensions are provisional for walkthrough review.

Build with `./docker-build.sh room meteor_chamber --site`; start locally at `/?room=meteor_chamber`.

A shared ladder now links the meteor chamber to a real floor hatch inside the garage. This user-requested shortcut replaces the old meteor-chamber exit door and the original long passage. Use E/click/tap to climb in either direction. Ordinary walking cannot fall through the garage hatch.

`interior.py` adds scenery to the shared shell builder; authored `room.json` keeps its collision footprints. All generated Blender scenes, previews and models remain under `generated/`.
