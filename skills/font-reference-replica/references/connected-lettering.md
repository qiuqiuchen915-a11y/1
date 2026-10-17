# Lightly connected lettering / 轻连笔字形

Use this workflow for partial ligatures, shared terminals, interlocking Chinese
components, sweeping baseline strokes, or near-touching slanted display lettering.
Preserve all original no-substitution and unseen-glyph truthfulness rules.

## 1. Record relationships before splitting characters

Read the full text, but do not use OCR boxes as cutting boundaries. First lock the
line box, tilt, baselines, word silhouette, and negative spaces. At native scale
and nearest-neighbor magnification, classify each apparent junction:

- true connection: a visible foreground bridge;
- overlap/occlusion: one stroke hides another; visible pixels do not prove its hidden path;
- near-touch: a real background gap must remain open;
- shared swash: a long terminal extends through another character's space;
- unresolved: antialiasing/compression makes the relationship ambiguous.

Record a connection map: involved characters/strokes, junction ROI in source pixel
coordinates, endpoints, entry/exit tangents, minimum neck width, gap width, stroke
layer order if visible, and confidence. Do not infer actual writing order from a
flat raster. Require stronger source evidence when a 1-pixel bridge is ambiguous.

## 2. Reconstruct groups, retaining character identity

Treat connected or interlocking characters as a **joint reconstruction group**,
while retaining a Glyph Record for each character. A connected component is not
necessarily a character: one character can have many components and a ligature
can include several characters. Do not split at equal widths or bounding boxes.

For unchanged visible text, prefer original pixel reuse or joint contour tracing.
Trace both sides of the connecting neck, its taper, tangent transitions, and the
adjacent counters. Keep the broad-to-thin stroke contrast, slant, deliberate
asymmetry, acute corners and sweeping terminals. Do not replace a variable-width
connector with a constant-width line or round all joins. Preserve open negative
spaces; do not close them to make lettering look more connected.

Separate base silhouette, surface scratches, shadow and ornament. A scratch must
not be silently repaired as a broken stroke. A shadow must not become a bridge.
Do not use dilation, closing, smoothing or generative cleanup to manufacture
connections or erase intentional gaps. Upscaling is inspection, not new evidence.

For new text, reuse visible glyph fragments and verified stroke families, then
construct new transitions in context. Do not copy a ligature onto an incompatible
stroke. Mark unseen characters and new joins as inferred, never pixel-exact.

## 3. Fix a junction without damaging its neighbors

Replace the rule “freeze every correct glyph” at shared boundaries with: freeze
all pixels outside the failed junction ROI; inside it, permit edits to both
participating strokes. Include enough context on each side for tangent continuity.
Keep the shared endpoint, line placement, tilt and surrounding negative space
fixed. If a group must be moved or scaled, transform the group as one unit first.
Do not normalize spacing independently per character or regenerate the whole line.

## 4. Validate every connection and every intentional gap

Evaluate whole-line silhouette, per-character structure, and every junction ROI.
Use the same registered coordinates in both images and include stroke interiors
on both sides of the bridge. Test the missing-bridge, unwanted-bridge and
wrong-neck-width cases separately. Do not let a high whole-image IoU override a
visibly severed or invented connection. Compare preserved scratches separately
from base contour masks.

The comparison helper accepts repeated half-open ROIs `x0 y0 x1 y1`:

```bash
python scripts/font_compare.py reference.png candidate.png \
  --roi 40 20 65 45 --roi 80 20 105 45
```

Choose actual coordinates from the reference; these are illustrative only.
Each ROI reports mask IoU, contour F1 and 8-connected component counts. A count
mismatch is a warning for changed connectivity, not automatic semantic failure:
scratches, noise, cropping and thresholding also affect it. Equal counts do not
prove the right strokes connect. Inspect bridge placement, minimum width and the
negative-space gap visually even when counts match. The script does not measure
those widths, infer ligatures, reconstruct missing strokes, or certify a replica.
Use independently checked masks on textured/effected backgrounds. Never tune
segmentation just to obtain passing metrics. Compare only corresponding visible
text; different words cannot be certified by a whole-image overlap score.
