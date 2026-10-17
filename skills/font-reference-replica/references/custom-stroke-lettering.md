# Inventive strokes / 创意笔画与部件变形

Use for custom hooks, loops, swashes, shared strokes, component fusion,
substitution of a conventional stroke with a shape, and unusual intersections.
Combine with connected-lettering.md and broken-connected-lettering.md when needed.

## Preserve the specimen, not a canonical font outline

Identify the intended character sequence, then record its *visible* design.
Do not normalize creative lettering into standard print glyphs. Existing rules
against added/deleted/merged strokes mean no unrequested deviation from the
reference: they do not require undoing a deliberate omission, fusion or loop
already visible in that reference. If reading is ambiguous, flag the ambiguity;
do not confidently change character identity to fit an ordinary glyph template.

For every distinctive feature, record:

- its character(s), component(s) and role: structural stroke, terminal or ornament;
- its actual centerline direction, curvature, inflection and turning points;
- outer contour, inner counter, variable width, taper and end shape;
- attachment points, incoming/outgoing tangents, crossings and visible occlusion;
- its extension beyond the character box, nearby clearance and text-group rhythm;
- evidence level: observed shape, inferred hidden segment or newly constructed form.

Treat a shared or borrowed stroke as a group-owned shape referenced by both
characters, not two independent copies. Preserve the entire contextual contour
when tracing; do not truncate a swash to a single-character box or duplicate a
shared stroke when reassembling glyphs. Distinguish decorative curls from required
structural strokes. Preserve deliberate asymmetry and nonuniform curvature;
do not replace every loop with a circle or smooth away corners and inflections.

## Reconstruct in three layers of evidence

1. Lock the original whole-word silhouette, positions and baseline rhythm.
2. Reuse or jointly trace visible glyph fragments and custom stroke geometry,
   preserving negative spaces, broken joints, shared joins and variable widths.
3. Apply surface texture/effects separately after the geometry is accepted.

Inspect each special feature at native size and in a context crop. Verify its
attachment location, tangent direction, loop opening/counter, extension, weight
transition, nearby gaps and contribution to readability. Use corresponding tight
ROIs for mask/negative-space QA; same component counts can hide wrong loops,
attachments or curvature. Existing helper metrics do not measure curvature,
identify character semantics or certify creative-stroke fidelity. Manually inspect
these features and repair only the affected group/feature ROI.

## New words: derive rules, do not paste arbitrary flourishes

Build a feature library from visible examples: what stroke roles accept a loop,
where a hook turns, how terminal taper changes, which components share strokes,
and where space permits an extension. Record exceptions, not just a style label.
For unseen characters, first make the intended character structurally legible,
then adapt only compatible features at corresponding stroke roles. Do not attach
an attractive curl everywhere or copy one word's exact ligature onto incompatible
characters. Check the result in the whole target word for crowded counters,
accidental letter fusion, loss of recognition and arbitrary decorative additions.
Mark new characters, substituted features and new joins as inferred designs;
they are not exact recovered source glyphs. Preserve exact visible instances when
they recur unless their contextual connection genuinely requires a stated change.
