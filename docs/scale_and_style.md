# Display aspect, source palette, and provisional scale

## Source findings

All 51 supplied PNGs were read and inspected. They contain exactly **16 distinct RGB colors across the entire set**. Their channel levels include 84, 168 and 252. Preserve these bytes: replacing them with a conventional 85/170/255 palette would alter the supplied artwork. [palette.json](../generated/reference/palette.json) records the exact RGB values, hex values, and pixel counts. PNGs contain no aspect metadata in the inspected entrance image.

The cutaway's room colors and details differ from the backgrounds. Its role is spatial arrangement, not palette or texture authority. Black pixels in the backgrounds are real image content, not automatically transparency.

## Display aspect decision

Use **1.2 times raw pixel height** as the provisional reference-display correction. ScummVM documents the 320×200 to 320×240 correction for rectangular-pixel games: [aspect ratio explanation](https://docs.scummvm.org/en/v2.7.1/advanced_topics/understand_graphics.html#aspect-ratio-correction).

This is a supported DOS-display convention, not proof of the exact provenance of these exports. The supplied backgrounds are cropped scene regions and panoramas; do **not** stretch an entire 320×128 crop to 4:3, or squeeze a 960-pixel panorama to 320 pixels. For a 320×128 scene crop, the corrected display extent is 320×153.6. For any panorama, retain its width and apply the same relative height correction.

[Entrance aspect comparison](../generated/reference/images/entrance-aspect-comparison.png) shows raw aspect at 5×5 and corrected aspect at 5×6 integer nearest-neighbor scaling. These introduce no new image colors. The contact sheets show raw 1:1 pixels for inspection; use the corrected comparison for proportion decisions.

Keep texture files at their original pixel dimensions. Account for aspect in reference-image placement, UV sizing, and reconstruction proportions. Do not apply a second 1.2 stretch to the completed 3D world or browser camera. Compare reference renders in the same display space before refining furniture proportions. Exact asset provenance remains unverified, so retain the raw comparison alongside the corrected one.

## Shared modeling convention

These are initial design choices for comfortable navigation, not dimensions measured from the game's artwork. Adjust consistently after the entrance prototype.

| Parameter | Initial value | Rationale / use |
|---|---|---|
| Blender units | 1 unit = 1 metre | Consistent exports and movement |
| Blender up | +Z | Convert using normal GLB exporter axis conversion; avoid manual double rotation |
| Origin | Entrance floor, center of main front threshold | Anchor future room placement |
| House axes | +X right along facade, +Y inward, +Z up | Reference-image left/right need not align with these axes |
| Player standing height | 1.75 m | Placeholder for collision and optional Dave |
| First-person eye height | 1.62 m | Evaluate against source composition in prototype |
| Collision radius | 0.25 m | Allows comfortable movement through ordinary doors |
| Single doorway clear opening | 1.0 m wide × 2.2 m high | Start point, adjust visible proportions to source |
| Double entrance clear opening | 1.8 m wide × 2.4 m high | Start point for entrance |
| Typical clear room height | 2.8 m | Initial ordinary-room shell |
| Nominal floor-to-floor | 3.2 m | 2.8 m clear plus structural allowance; not a rigid floor grid |
| Grand entrance clear height | 3.6–4.2 m trial range | Fit stair and source silhouette before settling |
| Stair width | 1.2 m minimum provisional | Main entrance stair may be wider to match drawing |
| Stair rise / tread | 0.16 m / 0.28 m | 20 rises span a nominal 3.2 m level; fit geometry in blockout |
| Stair collision | Smooth ramp under visible treads | Avoid camera bouncing; still respect head clearance |
| Wall thickness | 0.15–0.25 m | Enough for door frames; revise where rooms meet |
| Walk speed | 2.5 m/s | Comfortable exploration starting point |

Do not convert panorama pixels to metres with one global scale: source views use illustrated perspective. Fit doors and recognizable objects first, then room width and depth. Keep the tall tower's cutaway bands provisional until stair routes are resolved.

## Style check for the first modeled room

- Sample materials from the recorded palette and preserve drawn patterns.
- Use simple unlit/emission materials and neutral color handling.
- Compare a reference-camera render with the corrected entrance reference for door shape, stair silhouette, trim, and palette.
- Check additional viewpoints for plausible missing surfaces without adding realistic shading or extra decorative detail.
- Verify the exported browser appearance before treating the Blender style as settled.
