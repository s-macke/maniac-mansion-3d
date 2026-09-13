# Step 1: room inventory and initial map

Step 1 is complete as an initial planning pass. The supplied artwork establishes the layout basis; uncertain door destinations and unmatched connectors remain explicitly recorded. The local walkthrough now contains 14 room units; see [the architecture guide](architecture.md) for the current implementation.

- [Room inventory](../generated/reference/room_inventory.md): all 51 images, descriptive names, visible exits, cutaway matches, and state/reference classification.
- [Connection map](connection_map.md): spatial bands, route diagram, evidence per connection, and unresolved links.
- [Display aspect and scale](scale_and_style.md): provisional 1.2 vertical display correction, exact source colors, and shared Blender dimensions.
- [Machine-readable inventory](../generated/reference/room_inventory.csv): dimensions, metadata, and source hashes.
- [Exact source palette](../generated/reference/palette.json): all 16 sampled colors.
- [Entrance aspect comparison](../generated/reference/images/entrance-aspect-comparison.png): raw and corrected display proportions.

## Labeled contact sheets

Each image is shown at native pixel size, with no squeezed panoramas or palette changes.

| Main references | Additional references |
|---|---|
| [001–010](../generated/reference/images/contact-main-01.png) | [032–046, selected IDs](../generated/reference/images/contact-extra-01.png) |
| [011–020](../generated/reference/images/contact-main-02.png) | [048–050, 052](../generated/reference/images/contact-extra-02.png) |
| [021–030](../generated/reference/images/contact-main-03.png) | |
| [031, 036–038, 044, 047, 051](../generated/reference/images/contact-main-04.png) | |

The filenames have gaps; page labels are descriptive ranges, not counts. See the inventory for the full list.

## Current implementation

See the [project README](../README.md) and [room workflow](architecture.md). The inventory above remains the original planning reference.

See [the library and first-floor layout](first_floor.md) for the current upstairs shells, door ownership and deferred routes.
