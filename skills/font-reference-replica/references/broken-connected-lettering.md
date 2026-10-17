# Intentional breaks mixed with connections / 断连共存字形

Read together with connected-lettering.md. Apply within characters as well as
between them. A display glyph may deliberately break a conventional junction
while preserving another. Never restore textbook Chinese stroke connectivity.

## Record positive strokes and negative cuts separately

Before reconstruction, build a source-coordinate junction ledger:

| Field | Required evidence |
|---|---|
| Type | keep-open cut / keep-connected bridge / overlap / near-touch / unresolved |
| Location | character, participating strokes, tight ROI with context |
| Cut geometry | both facing endpoints, width, length, orientation, taper, terminal shape |
| Bridge geometry | entry/exit tangent, neck width, taper and adjacent counters |
| Confidence | visible at native scale / compression-sensitive / occluded |

Record the source's actual geometry, including deliberate misalignment of the
facing terminals. Do not force cuts to a uniform width or position. Distinguish
structural cuts from surface scratches: geometry uses a base mask plus separate
negative cut masks; texture uses a separate layer. Do not label all white gaps
as defects or all dark pixels as scratches. For fine horizontal strokes, narrow
counters and tiny cuts, review original pixels as well as enlarged previews.

## Reconstruct before applying material

Lock the whole text's proportions, line rhythm and spacing. Record thin/thick
stroke contrast, vertical elongation, serif/wedge tips, curved terminals, and
component asymmetry from the reference. Trace visible fragments in context;
do not substitute a standard serif font, reconnect its conventional skeleton,
or equalize horizontal and vertical stroke weight.

For editable tracing, build variable-width positive stroke shapes and retain
intentional cuts as separately editable subtractive shapes. Preserve the final
union-minus-cuts silhouette. A keep-open cut must not erase an adjacent intended
bridge. Inspect the resulting counters and both cut endpoints after rasterizing
at delivery size. Do not use global closing, opening, dilation, smoothing or
skeleton cleanup on the final glyph: these operations can seal cuts or delete
fine connections. Pixel reuse remains preferred for unchanged visible text.

When a junction fails, edit only its documented ROI and shared stroke context;
freeze correct cuts and bridges elsewhere. Make no automated repair to an
unresolved junction. Seek higher-resolution evidence when a gap or hairline is
only one ambiguous antialiased pixel. Enlargement cannot recover missing detail.

## Check both the ink and its absence

Create separate tight ROIs for every intentional cut and every intended bridge,
then use repeated --roi arguments with matched, aligned images. Require:

- intentional cuts stay open, with the correct gap width and terminal shape;
- intended bridges stay connected, with the correct neck width and tangents;
- no fine stroke is lost during thresholding or final-size rasterization;
- local foreground overlap AND local negative-space overlap remain faithful.

The helper reports ROI foreground IoU, background IoU, missing/added foreground
pixel counts, edge F1 and component counts. Filled cut pixels appear as added
foreground; removed bridge pixels appear as missing foreground. These counts
also respond to misalignment and threshold errors: inspect registered masks
before interpreting them. Small tight ROIs reduce dilution by unrelated pixels.
Equal component counts do not prove the right junctions survived: filling one
cut while breaking another bridge can leave the total unchanged. A background
IoU of N/A means neither mask contains background in that ROI, not a pass.
The helper does not infer intended cuts or automatically measure cut/neck widths;
the ledger and visual checks remain required. Never repair candidates by changing
segmentation thresholds until metrics pass.

For different target words, derive a documented design rule from visible examples
(e.g. cut placement relative to a junction, terminal treatment and width contrast),
then construct missing characters and joins in context. Mark new cuts, bridges
and unseen glyphs as inferred. Do not claim exact recovery or compare different
words with whole-image IoU. Keep the original no-similar-font substitution rules.
