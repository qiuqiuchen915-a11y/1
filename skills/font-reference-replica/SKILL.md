---
name: font-reference-replica
description: >
  Ultra-strict reference typography reconstruction skill. Rebuilds glyph structure
  from reference imagery by analyzing skeletons, stroke topology, terminals, joins,
  width/height ratios, local deformation, spacing, outlines, texture, and effects.
  Use when the user requires exact or near-pixel reproduction of lettering and forbids
  similar-font substitution.
version: 2.0.0
---

# $font-reference-replica

## Core objective

Reconstruct the typography in the reference image with the highest fidelity technically possible.

This skill does **not** treat the reference as merely a "font style".
It treats each visible character as a **forensic glyph specimen**.

The workflow must recover and preserve:

- glyph skeleton
- stroke topology
- stroke order impression
- stroke width profile
- stroke contrast
- local thickening/thinning
- terminals
- hooks
- corners
- joins
- bowls
- counters
- apertures
- crossbars
- overshoot
- center of gravity
- aspect ratio
- local stretching/compression
- slant
- rotation
- irregularity
- handwritten deviations
- optical corrections
- pair-specific spacing
- outlines
- texture
- highlights
- shadows
- extrusion
- raster edge character

**Reference glyph geometry always has higher priority than font identification.**

---

# Absolute prohibition

When the user says any equivalent of:

- 100%复刻
- 完全一样
- 字形必须一致
- 禁止相似字体
- 严格复制
- 一比一复刻

the system must NOT:

- substitute a visually similar font and claim success;
- normalize unusual glyph proportions;
- simplify handwritten or custom modifications;
- straighten intentionally bent strokes;
- equalize uneven stroke widths;
- center a glyph that is visually off-center in the source;
- repair irregular corners unless the irregularity is clearly an artifact;
- silently invent unseen glyph shapes;
- redraw the word from general stylistic memory;
- use a one-pass text-to-image redraw as the primary reconstruction method;
- regenerate the whole image when only a local glyph is wrong.

---

# Truthfulness boundary

There are two fundamentally different cases.

## Case 1 — Glyph is visible in the reference

This is the highest-confidence case.

The target is not "find the font".
The target is:

**extract, trace, reconstruct, and reuse the exact visible glyph geometry.**

When resolution is sufficient, the skill should aim for near-pixel reconstruction.

## Case 2 — Glyph is NOT visible in the reference

A mathematically exact reconstruction cannot be guaranteed from one image alone.

For unseen glyphs, use this priority:

1. exact original font file
2. editable vector/source file
3. another reference containing the missing glyph
4. verified exact font identification
5. glyph construction from the same reference type system
6. closest approximation

Levels 5–6 are never called exact.

---

# Glyph forensic model

For every unique visible character, build a **Glyph Record**.

## Glyph Record fields

### A. Identity
- character
- occurrence index
- source crop coordinates
- confidence level

### B. Bounding geometry
- x
- y
- width
- height
- baseline offset
- optical center x
- optical center y
- top overshoot
- bottom overshoot

### C. Skeleton
Represent the visual centerline structure of the glyph.

Record:
- skeleton nodes
- skeleton branches
- endpoints
- junctions
- loops
- intersections
- dominant stroke directions
- curvature at each segment

Do not assume typographic textbook structure.
Use the actual visual specimen.

### D. Stroke topology
For each stroke-like region record:
- start point
- end point
- path shape
- direction
- thickness profile
- taper profile
- curvature
- pressure impression
- join behavior
- overlap behavior
- terminal type

### E. Stroke width profile

Measure thickness at multiple locations.

Example:
- top horizontal: 18 px → 22 px → 20 px
- left vertical: 24 px → 27 px → 25 px
- diagonal: 15 px → 20 px

Never replace this with a single "font weight" value when strict replication is requested.

### F. Terminal library

Classify and preserve terminals such as:
- flat
- rounded
- pointed
- hooked
- flared
- cut
- brush-like
- ink-swollen
- serifed
- wedge
- teardrop
- custom asymmetric

Record terminal angle, width and curvature.

### G. Join library

Preserve:
- miter joins
- rounded joins
- soft brush joins
- overlap joins
- broken joins
- fused joins
- custom pinched joins

### H. Counter and negative space

Measure:
- counter width
- counter height
- counter shape
- aperture opening
- negative-space asymmetry

Negative space is part of the glyph design and must not be "cleaned up".

### I. Local deformation

Record per-glyph:
- horizontal scale
- vertical scale
- shear
- skew
- rotation
- bend
- arc
- perspective
- envelope warp
- localized bulge
- localized pinch
- asymmetric stretching

### J. Irregularities

Record visible irregularities separately from noise:
- hand-drawn wobble
- uneven edges
- print bleed
- paint drag
- rough outline
- broken ink
- scan softness
- compression

Do not automatically remove them.

---

# Chinese-character structure analysis

For Chinese, Japanese Kanji, or Han-derived glyphs, additionally analyze:

## 1. Character frame
- overall square occupancy
- top/bottom/left/right margins
- optical center
- center-of-mass bias

## 2. Component proportions
Measure relative component boxes.

Examples:
- left radical width = 31% of glyph
- right component width = 63%
- inner gap = 6%
- top component height = 42%
- bottom component height = 51%

## 3. Stroke hierarchy
Record:
- 横 width profile
- 竖 width profile
- 撇 angle and taper
- 捺 angle and flare
- 点 shape and placement
- 提 angle
- 钩 curvature
- 折 corner shape

Do NOT generalize strokes merely by Unicode radical identity.
Use the visible form in the reference.

## 4. Structural tension
Record:
- whether the glyph leans
- whether left/right parts compress
- whether top/bottom are dense
- whether the center opens
- whether outer strokes flare
- whether inner strokes are intentionally crowded

## 5. Repeated stroke family consistency
When the same stroke type appears repeatedly:
- compare them;
- identify intentional family resemblance;
- preserve meaningful differences.

---

# Latin-letter structure analysis

For Latin text, additionally record:

- cap height
- x-height
- ascender
- descender
- stem width
- bowl curvature
- shoulder form
- spur
- ear
- tail
- crossbar position
- apex
- vertex
- serif geometry
- stress axis
- contrast axis

Distinctive letters must receive special attention:
A, B, G, M, Q, R, S, a, e, g, k, r, s, y, 1, 2, 4, 7, &, @.

---

# Reconstruction modes

## MODE A — Pixel reuse

Use when:
- target word is unchanged;
- source resolution is adequate;
- background can be separated.

Method:
1. isolate original glyph pixels;
2. reconstruct only occluded/contaminated edge pixels;
3. preserve original raster edge character;
4. reuse original glyphs directly.

This is the preferred mode for maximum fidelity.

## MODE B — Vector contour reconstruction

Use when:
- scaling is required;
- source is clean enough for tracing.

Method:
1. trace outer contour;
2. trace holes/counters;
3. preserve every visible corner and irregularity above tolerance;
4. rasterize at target size;
5. compare against source;
6. iteratively correct contour control points.

## MODE C — Stroke-model reconstruction

Use when:
- the glyph is stylized;
- vector contour alone is insufficient;
- handwritten/brush geometry matters.

Method:
1. reconstruct skeleton;
2. reconstruct width profile along skeleton;
3. rebuild terminals;
4. rebuild joins;
5. apply local deformation;
6. compare final contour to source.

## MODE D — Hybrid exact-font + custom deformation

Use only when exact font identification is verified.

Method:
1. render exact font;
2. convert to outline;
3. compare to source;
4. apply per-glyph geometric corrections;
5. apply reference-specific effects.

The exact font is only a starting geometry, not an excuse to skip correction.

---

# Reference resolution rules

For strict glyph-structure work:

- >= 160 px glyph height: excellent
- 100–159 px: strong
- 60–99 px: usable
- 40–59 px: risky
- < 40 px: insufficient for micro-structure certainty

If the user asks for absolute fidelity and glyphs are too small:
- do not invent stroke micro-shape;
- request a larger crop or source image.

---

# Preprocessing

Before measuring glyph structure:

1. crop typography region with 15–25% padding;
2. correct perspective only for measurement;
3. preserve original uncorrected image for final compositing;
4. separate color channels if contrast is poor;
5. generate:
   - grayscale
   - high-contrast mask
   - edge map
   - skeleton map
   - effect masks
6. inspect at:
   - 100%
   - 200%
   - 400%
   - 800% when needed

Never rely on OCR alone for shape reconstruction.

---

# Font-identification policy

Font recognition is secondary.

A candidate font may be accepted only after geometric verification.

Compare at least 5 distinctive glyph features when available.

Scoring:
- contour silhouette: 30%
- skeleton topology: 20%
- stroke width behavior: 15%
- terminals/joins: 15%
- proportions: 10%
- counters/negative space: 5%
- spacing behavior: 5%

Reject if:
- signature terminals differ;
- stroke modulation differs;
- counters differ materially;
- proportions require extreme scaling;
- a custom glyph is obviously altered;
- the source behaves like lettering rather than an untouched font.

---

# Layout reconstruction

For every glyph occurrence, record:

- left x
- top y
- width
- height
- baseline
- rotation
- optical offset
- previous-glyph gap
- next-glyph gap

Pair spacing is authoritative.

Do not assume uniform tracking.

Measure:
- actual black-shape gap
- bounding-box gap
- optical gap

Use optical gap for final tuning.

---

# Effect separation

Typography effects must be reconstructed as separate layers.

Recommended stack:

1. base glyph alpha
2. base color
3. inner gradient
4. local texture
5. inner highlight
6. inner shadow
7. primary stroke
8. secondary stroke
9. inline decoration
10. bevel
11. extrusion
12. cast shadow
13. outer glow
14. grain/distress
15. final blur/print/raster character

Effect styling must never alter the recovered glyph contour unless the reference shows that it does.

---

# Material lettering

For:
- chrome
- crystal
- rhinestone
- embroidery
- chenille
- puff print
- flocking
- sequins
- glitter
- fur
- glass
- jelly
- candy
- neon
- carved
- embossed
- debossed

separate:

**glyph geometry** from **material appearance**.

First lock geometry.
Then reconstruct material.

Never allow material generation to distort the glyph silhouette.

---

# New-word workflow

When target text differs from reference:

## Step 1
Build a glyph master library from all visible characters.

## Step 2
For repeated characters:
- reuse the same master only if the reference shows identical instances;
- otherwise preserve instance-specific variants.

## Step 3
For missing characters:
- search exact font only if permitted/available;
- otherwise construct from reference stroke families.

## Step 4
For Chinese missing glyph construction:
reuse measured stroke families:
- horizontal family
- vertical family
- left-falling family
- right-falling family
- dot family
- hook family
- turning-corner family

But preserve the truthfulness boundary:
constructed unseen glyphs are stylistically matched, not proven exact.

---

# Per-glyph deformation field

Each glyph may carry its own transform:

- sx
- sy
- shear_x
- shear_y
- rotation
- local warp grid
- perspective quad

Do not apply one global transform to all glyphs unless the source proves that transformation is global.

---

# Pixel-level QA

For visible-reference glyphs, final QA should include:

## Geometry metrics
- alpha-mask IoU
- contour Hausdorff distance
- edge F1
- skeleton overlap
- bounding-box deviation
- optical-center deviation
- stroke-width error

## Raster metrics
- SSIM
- MAE
- local contrast error
- color delta

## Layout metrics
- baseline error
- pair-spacing error
- glyph rotation error
- text-block size error

Recommended strict targets on a clean high-resolution reference:

- mask IoU >= 0.985
- edge F1 >= 0.98
- skeleton overlap >= 0.97
- SSIM >= 0.975
- average contour deviation <= 1.25 px
- baseline deviation <= 1 px
- pair-spacing deviation <= 1.5 px
- average stroke-width deviation <= 4%

These are engineering targets, not proof of metaphysical “100%”.

---

# Character-by-character QA table

Before accepting a result, inspect each glyph:

| Attribute | Must check |
|---|---|
| silhouette | yes |
| skeleton | yes |
| aspect ratio | yes |
| stroke thickness | yes |
| taper | yes |
| terminals | yes |
| joins | yes |
| counters | yes |
| local deformation | yes |
| position | yes |
| rotation | yes |
| pair spacing | yes |
| outline | yes |
| shadow | yes |
| texture | yes |
| edge softness | yes |

If any high-priority attribute fails, that glyph fails.

---

# Failure repair loop

When one glyph fails:

1. freeze every correct glyph;
2. isolate failed glyph;
3. identify the failed attribute;
4. edit only that attribute;
5. rerender;
6. compare again.

Examples:
- wrong horizontal width → adjust only width field;
- wrong left radical proportion → edit only component box;
- wrong hook → replace only hook terminal geometry;
- wrong shadow → keep contour frozen and adjust shadow layer only.

Do not regenerate the full word.

---

# Anti-AI-drift rules

Image-generation systems tend to:
- normalize proportions;
- soften corners;
- invent missing strokes;
- change stroke count;
- distort Chinese radicals;
- alter text content;
- randomize kerning.

Therefore strict execution must repeatedly state:

- exact character count
- exact character order
- exact stroke topology
- exact silhouette
- no added stroke
- no deleted stroke
- no merged stroke
- no swapped radical
- no substitute character
- no spelling change
- no font substitution
- no automatic beautification

---

# Output preservation

If typography is being edited inside an existing image:

LOCK all unrelated regions:

- subject
- face
- body
- garment
- background
- color grading
- lighting
- composition
- crop
- props

Only the typography region may change unless the user says otherwise.

---

# Execution phrase

When invoked, internally enforce:

> Treat every visible character in the reference as an individual forensic glyph specimen.
> Do not recreate the text from a similar font.
> Recover the actual glyph skeleton, stroke topology, stroke-width variation, terminals,
> joins, counters, component proportions, local deformation, optical center, pair spacing,
> outlines, texture, shadow, and raster edge character from the reference itself.
> For Chinese characters, reconstruct component boxes and every stroke family from the
> visible specimen; preserve exact stroke count, direction, hook, turn, taper and center
> of gravity. Freeze correct glyphs and only redo failed local regions.
> Existing visible glyphs must be traced/reused whenever possible.

---

# User invocation template

按 `$font-reference-replica` 执行。

参考图：图1  
目标文字：{TARGET_TEXT}

最高优先级：
- 完全按照参考图重建字形结构；
- 不得使用相似字体直接替代；
- 逐字复刻字形比例、骨架、笔画数量、笔画方向、粗细变化、转折、钩、撇、捺、收笔；
- 逐字复刻局部压缩、拉伸、倾斜、旋转和不规则形变；
- 复刻每个字的重心、部件占比、负空间和字距；
- 描边、颜色、纹理、阴影、立体效果独立复刻；
- 禁止增笔、减笔、并笔、错字、替字；
- 正确区域锁定，错误字符只局部重做；
- 参考图中已经出现的字形优先直接描摹/提取，不得重新用近似字体生成。

---

# Final principle

**Font name is optional. Glyph geometry is mandatory.**

**The reference image is the ground truth.**
