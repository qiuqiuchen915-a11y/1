# Font Reference Replica — Execution Workflow v3.0

This document is the mandatory operating procedure for `$font-reference-replica v3.0`. The parent `SKILL.md` defines the forensic glyph model and strict reconstruction constraints; this file defines how to scope, choose, execute, verify, and deliver a real job.

## 0. Mission and truthfulness boundary

The objective is the highest technically supportable fidelity to the supplied lettering—not a vaguely similar font, not a redesign, and not free-form styling.

Treat the reference as evidence. Preserve its actual geometry, irregularities, spacing, layout, and effects unless the user explicitly asks to change them.

Never promise literal 100% identity when the source does not support it. Use these provenance labels consistently:

- **Traced/reused**: geometry or pixels directly taken from a visible source glyph.
- **Reconstructed**: geometry rebuilt from a sufficiently clear visible source glyph.
- **Constructed/style-matched**: an unseen glyph inferred from transferable rules.
- **Unverified**: a candidate font or generated result not yet geometrically checked.

A constructed or unverified glyph must never be described as an exact copy. A numerical score is not proof of correct character identity.

## 1. Intake: lock the actual job before drawing

Extract the following from the request and attachments:

### Required when applicable
- Exact target wording, including punctuation, spaces, capitalization, full-width/half-width characters, numerals, and symbols.
- The reference image or source file.
- Which image/text is the primary reference if multiple references are supplied.

### Optional constraints
- Secondary reference images and what each one contributes.
- Whether the target wording is unchanged or contains new/missing characters.
- Whether the original reading direction, line breaks, and composition must be inherited.
- Output color, background, dimensions, format, and intended use.
- Whether editable vector paths/layers are required.
- Hard prohibitions, such as no added ornaments, no background, or no change to surrounding artwork.

### Defaults
If the user does not specify otherwise:
- Foreground: solid black.
- Background: genuinely transparent.
- Format: PNG.
- Composition: inherit the reference reading direction and block arrangement.
- Effects: reproduce only those visibly present in the reference; do not invent new effects.
- Scope: change only the lettering region.
- Deliver the cleanest high-resolution asset supported by the source; do not invent a pixel dimension when none is requested.

Do not ask the user to repeat information already visible in the current conversation. If one essential input is missing, ask one direct question. Do not block execution over optional preferences; apply the defaults above.

## 2. Reframe the task and select a method

First decide what the user is actually asking to preserve:

| Job type | Preferred strategy |
|---|---|
| Same wording, same visible lettering | Pixel isolation/reuse; repair only damaged edges |
| Same glyphs, new size or clean output | Contour tracing or high-resolution reconstruction from the source |
| New wording, all target glyphs visible somewhere | Build a glyph master library, reuse/trace each source glyph, then recompose |
| New wording with unseen glyphs | Search for original vector/font/source if available; otherwise construct from measured style rules and label those glyphs constructed/style-matched |
| Connected, interlocking, or shared-stroke lettering | Analyze the whole word and junction groups before separating glyphs; read the relevant connected-lettering references |
| Material/effects-heavy lettering | Lock glyph geometry first; reconstruct color, texture, bevel, outline, and shadow as separate layers |
| Editable vector requested | Deliver actual editable paths/layers (for example SVG paths); never call a flat PNG an editable vector or claim that PNG alone is an AI source file |

Do not default to text-to-image generation for strict reproduction. It may be used for ideation on unseen glyphs, but its output is not verified geometry and must not replace tracing/reuse of visible glyphs.

## 3. Inspect source evidence and create a Reference Style Sheet

Before reconstruction, inspect the actual pixels and record:

1. Source dimensions, crop, perspective, compression, blur, and approximate glyph height.
2. Foreground/background separation and whether transparency is genuine.
3. Text block orientation, line arrangement, overall silhouette, margins, and reading order.
4. Per-glyph bounding box, aspect ratio, optical center, baseline, lean, and local deformation.
5. Stroke-family width ranges, taper, pressure impression, terminals, corners, joins, bridges, overlaps, and intentional gaps.
6. Counters, apertures, negative spaces, and asymmetry.
7. Color, outlines, gradients, texture, highlights, shadows, extrusion, glow, and raster-edge behavior as separate visual layers.

Classify every note as:
- **Observed invariant** — directly visible and must be preserved.
- **Transferable rule** — repeated behavior that can guide a different glyph.
- **Character-specific exception** — unique to one source glyph; do not copy it indiscriminately.

Resolution guide (approximate glyph height):
- 160 px or more: excellent for detailed tracing.
- 100–159 px: strong.
- 60–99 px: usable with caution.
- 40–59 px: risky for micro-structure.
- Below 40 px: insufficient for confident fine-detail reconstruction.

If the source is too small or blurred for the requested fidelity, state the limitation and request a larger crop when it materially affects the result. Never invent uncertain micro-details.

## 4. Build the character inventory and glyph records

Compare the exact target string against all visible source characters. Classify each target character as:

- **Visible** — fully present and usable.
- **Partially visible** — occluded, clipped, or contaminated.
- **Unseen** — absent from the source.

For every target glyph, record at minimum:
- character identity and occurrence;
- source crop or provenance;
- bounding box, aspect ratio, baseline, optical center, and rotation;
- component/skeleton structure and stroke count/topology;
- stroke-width profile and taper;
- terminal, corner, join, bridge, and gap behavior;
- counter and negative-space geometry;
- local deformation and distinctive irregularities;
- confidence/provenance label.

For Chinese characters, preserve character identity and component order before applying style. Analyze actual visible component proportions and stroke behavior; do not assume a textbook radical form overrides the specimen.

For repeated characters, reuse one master only when the source shows the same shape. Preserve distinct hand-drawn or instance-specific variants when they are visibly different.

## 5. Reconstruct in the correct order

### Pass A — Lock character identity
Verify exact character count, order, spelling, punctuation, and component structure. No style transfer may change the text.

### Pass B — Recover geometry
Use the best-supported mode:
- Pixel reuse for unchanged visible lettering.
- Vector contour tracing for clean, scalable shapes.
- Skeleton plus variable-width stroke reconstruction for brush, handwritten, or pressure-sensitive forms.
- Hybrid font-plus-deformation only when font identification is verified and the rendered glyphs are geometrically corrected against the specimen.

### Pass C — Transfer style to unseen glyphs
Use only measured, repeatable stroke and contour rules. Do not paste one-off loops, swashes, cuts, bridges, or terminals onto unrelated strokes. Preserve required character structure. Mark the result constructed/style-matched.

### Pass D — Rebuild layout
Inherit the reference's reading direction, line breaks, hierarchy, overall silhouette, and optical rhythm unless the user explicitly requests a new composition. Tune pair spacing in context; do not apply uniform tracking blindly.

### Pass E — Rebuild effects
Only after the base glyph geometry is approved, reconstruct effects as separate layers. Effects must not distort the base silhouette unless the reference visibly includes that distortion.

## 6. Quality assurance: inspect evidence, not impressions

Run these checks before delivery:

### Content
- Exact text and character order.
- No missing, duplicated, substituted, or malformed characters.
- Correct punctuation, numerals, and symbols.

### Glyph geometry
- Silhouette, skeleton/topology, stroke count, width variation, taper, terminals, corners, joins, counters, negative spaces, and local deformation.
- Chinese component proportions and structural tension.
- No accidental normalization of irregularities.

### Composition
- Reading direction, line breaks, glyph scale, baseline, optical center, pair spacing, and overall text-block silhouette.

### Rendering and export
- Correct foreground color.
- Real alpha transparency—not a white rectangle or checkerboard baked into the image.
- Clean edges at 100%, 200%, and enlarged inspection views.
- Correct dimensions and file format.
- No unintended shadow, halo, fringe, matte, compression artifacts, or clipped strokes.

### Quantitative comparison
Use `scripts/font_compare.py` only when the reference and candidate are correctly aligned and comparable. Prefer validated glyph masks for shape comparisons. Do not report metrics that were not actually computed. Explain metric limitations: IoU does not prove character identity; full-canvas metrics can be dominated by background; equal dimensions do not prove alignment. Follow the README's mask and metric guidance.

Do not invent a score or claim that an unrun script passed. If a numerical comparison is unavailable, report a visual inspection rather than fabricating precision.

## 7. Repair locally; preserve accepted work

When a glyph or junction fails:
1. Identify the exact failed glyph, junction, or effect layer.
2. Name the failed attribute (for example, left component too wide, hook terminal too blunt, counter too narrow, spacing too tight).
3. Freeze all accepted glyphs and regions.
4. Repair only the smallest affected region.
5. Re-render and recheck the repaired region plus its neighboring spacing/junctions.
6. Re-run the full phrase check to ensure the repair did not introduce regressions.

Never regenerate the whole phrase merely because one character is wrong. For connected lettering, repair both participating strokes together while freezing the rest of the word.

## 8. Deliverables and completion report

Default deliverable:
- High-resolution PNG.
- Black lettering on a genuinely transparent background.
- Lettering only, with no extra decoration or background.

If the user asks for another color, composition, dimensions, or file format, follow that request. If the user requests editable vector artwork, provide actual vector paths/layers where possible and clearly distinguish SVG/PDF/vector source from a raster PNG. Do not promise an editable AI file unless one was actually produced and verified.

Accompany the asset with a concise report:
- Exact target wording.
- Reconstruction method used.
- Count or list of traced/reused, reconstructed, and constructed/style-matched glyphs.
- Output format and transparency status.
- QA checks actually completed.
- Any remaining limitation or low-confidence glyph.

Do not bury the result under a long explanation. The report should make the provenance and limitations clear.

## 9. Invocation template

Use the short form when the request and reference are obvious:

```text
$font-reference-replica v3.0
文案：{准确文字}
参考：图1
输出：纯黑字，透明背景 PNG
要求：尽可能 1:1 高还原；禁止相似字体替代；逐字质检。
```

Use the expanded form when needed:

```text
$font-reference-replica v3.0

目标文案：
主参考：
补充参考及用途：
是否更换文案：
版式要求：
输出格式/颜色/背景：
必须保留：
禁止改变：
特殊说明：
```

## 10. Final operating principle

**Reference evidence outranks font labels. Character identity outranks decoration. Geometry outranks material effects. Verified extraction outranks plausible invention.**

The goal is maximum faithful reconstruction—not an unsupported promise of perfect identity.
