---
name: font-reference-replica
description: >
  Reconstruct typography from a reference image with fidelity-first rules.
  Prioritizes direct glyph reconstruction over approximate font substitution.
  Use when the user asks to copy, reproduce, restore, replace, or generate text
  that must match typography visible in a reference image, poster, logo, packaging,
  UI, title card, or graphic.
version: 1.0.0
---

# $font-reference-replica

## Mission

Reproduce the typography in a reference image as faithfully as the available evidence allows.

**Highest priority: visual identity of the reference glyphs.**

Do NOT treat “same font category” or “similar-looking font” as success.

For text already visible in the reference, prefer **direct glyph reconstruction / tracing / extraction** over retyping with a substitute font.

---

# Non-negotiable truthfulness rule

Never claim mathematically perfect 100% replication unless the final rendered pixels have actually been compared against the source and meet the defined tolerance.

There are three task classes:

1. **CLASS A — Exact existing text**
   - The target text is already visible in the reference.
   - Goal: near-pixel-identical reconstruction.
   - Preferred method: extract/trace the original glyphs and effects.
   - Do not replace with a “similar font”.

2. **CLASS B — Rearrangement using glyphs already present**
   - The requested new text can be composed entirely from characters already visible in the reference.
   - Goal: reuse reconstructed glyph masters, then match original spacing/effects.
   - Do not invent missing glyph shapes.

3. **CLASS C — New characters not present in the reference**
   - Exact visual identity cannot be guaranteed from the image alone.
   - First try to identify the exact font.
   - If the exact font cannot be verified, create the closest reconstruction but explicitly mark it as an approximation.
   - For true exactness, request one of:
     - original font file,
     - editable source artwork,
     - vector glyphs,
     - a complete alphabet/character sample at sufficient resolution.

---

# Fidelity priority order

When conflicts occur, preserve features in this order:

1. Glyph silhouette / outline geometry
2. Stroke terminals and corner shapes
3. Character width and height proportions
4. Internal counters / holes
5. Stroke contrast and weight
6. Glyph-specific distortions or custom lettering
7. Baseline, rotation, skew, warp and perspective
8. Kerning between specific character pairs
9. Tracking / overall spacing
10. Line spacing and paragraph composition
11. Fill color / gradient
12. Outline / stroke layers
13. Inline / double-line details
14. Extrusion / 3D depth
15. Shadow geometry
16. Highlight / bevel
17. Texture / distress / grain
18. Opacity and edge softness
19. Interaction with background
20. Final antialiasing and raster character

A cleaner result is NOT automatically a better result.
If the reference has uneven edges, handmade distortion, print defects, blur, ink bleed, or compression artifacts that are part of the visible typography, preserve them when requested.

---

# Forbidden shortcuts

Never do any of the following when exact reproduction is requested:

- Do not use a vaguely similar font and call it exact.
- Do not redraw words from memory.
- Do not normalize irregular custom glyphs.
- Do not auto-center text if the original is optically offset.
- Do not equalize kerning if the source has pair-specific spacing.
- Do not remove intentional distortion, tilt, warp, stretching or compression.
- Do not convert crystal, chrome, embroidered, furry, inflated, hand-painted, printed, embossed or stitched letter effects into a flat fill.
- Do not merge outline and fill into one shape when the source clearly contains layered typography.
- Do not silently invent unseen glyphs.
- Do not “beautify” away reference-specific defects.
- Do not alter the background, composition, subject, colors, or other graphic elements unless the user explicitly asks.

---

# Input inspection

Before editing or generating, inspect the reference at high magnification.

Record:

## 1. Text content
- Exact visible characters
- Case
- Punctuation
- Numerals
- Symbols
- Ligatures
- Alternate glyphs
- Repeated letters

## 2. Glyph geometry
For every unique visible glyph, estimate or trace:
- bounding box
- cap height / x-height
- ascender
- descender
- advance width
- left/right sidebearing
- stroke thickness
- stroke contrast
- terminal shape
- corner radius
- aperture
- counter shape
- serif shape, if any
- overshoot
- slant
- width class
- vertical/horizontal scaling
- unique custom deformation

## 3. Layout
Record:
- line count
- baseline coordinates
- individual glyph x/y positions
- rotation per glyph
- kerning per pair
- tracking
- line height
- alignment
- optical offset
- text block bounding box
- perspective / arc / envelope warp

## 4. Layer effects
Record independently:
- base fill
- inner fill
- gradient
- outline 1
- outline 2
- inline
- shadow
- extrusion
- glow
- bevel
- highlight
- texture
- grain
- print bleed
- distress
- blur
- opacity

## 5. Color
Sample from the actual reference whenever possible.
Record colors as:
- RGB / HEX
- approximate Lab
- gradient stops
- shadow color
- outline color
- highlight color

Do not infer “white”, “black”, “pink”, etc. if sampling is possible.

---

# Resolution gate

The system must distinguish “visible enough to reproduce” from “too small to know”.

For the main target lettering:

- Preferred glyph height: >= 120 px
- Usable: 60–119 px
- Risky: 30–59 px
- Insufficient for strict reconstruction: < 30 px

If critical details are unreadable:
- do not hallucinate terminals or micro-details;
- preserve only what is actually visible;
- request a crop, original file, higher-resolution screenshot, or close-up if strict fidelity is required.

---

# Workflow

## Stage 1 — Isolate typography

Create a working crop with 10–30% padding around the typography.

Separate:
- foreground letterforms
- outline
- shadow/extrusion
- decorative particles
- background

If the lettering overlaps complex imagery, use masks and local reconstruction instead of destructive global changes.

---

## Stage 2 — Determine reconstruction strategy

### Strategy A: Direct glyph extraction
Use when:
- text already exists in the reference;
- reference resolution is sufficient;
- user wants the same wording.

Process:
1. isolate each glyph;
2. preserve original edge shape;
3. reconstruct occluded fragments only when evidence is sufficient;
4. retain the original glyph as the master;
5. rebuild layout from recorded coordinates.

This is the default for strict reproduction.

### Strategy B: Vector tracing
Use when:
- the source is clean, high contrast, logo-like, or geometric;
- scaling is required.

Process:
1. trace the outer contour;
2. trace counters separately;
3. simplify only below visible pixel tolerance;
4. retain asymmetric/custom anomalies;
5. compare rasterized trace against the source at target size.

### Strategy C: Exact font identification
Use when new characters are required.

Verification requires more than a similar font name.
Compare:
- distinctive glyphs
- R / G / Q / S / a / g / e
- numerals 1 / 2 / 4 / 7
- punctuation
- terminals
- widths
- kerning behavior

If a candidate fails distinctive glyph comparison, reject it.

### Strategy D: Hybrid reconstruction
Use when:
- a base font is identifiable but the reference contains custom modifications.

Process:
1. render the verified base font;
2. convert to outlines;
3. edit glyph geometry;
4. apply per-glyph scale/skew/warp;
5. restore custom terminals and cuts;
6. reproduce effects.

---

# Exact-font identification rules

A font candidate is NOT accepted only because OCR/font-recognition software suggested it.

Require visual verification against multiple glyphs.

Score candidate fonts on:

- silhouette similarity: 35%
- distinctive glyph features: 20%
- proportion/width: 15%
- stroke geometry: 10%
- terminal/corner design: 10%
- default spacing behavior: 5%
- numeral/punctuation match: 5%

Reject a candidate when:
- a signature glyph differs clearly;
- width requires extreme horizontal scaling;
- terminal geometry conflicts;
- counters differ materially;
- serif structure differs;
- the source is obviously custom lettering.

---

# New-text reconstruction

When the user asks to change the wording:

## If all glyphs already exist
Build a glyph library from the reference and reuse the exact extracted/traced glyph masters.

Do not retype them with a font.

For each reused glyph preserve:
- original shape
- relative scale
- fill
- outline
- texture
- lighting

Then recompute only:
- pair spacing
- line composition
- target placement

## If some glyphs are missing
Use this priority:

1. exact identified font
2. additional user references containing the missing glyph
3. original vector/font file
4. mathematically inferred compatible glyph from the same type system
5. closest approximation

Levels 4–5 must never be described as guaranteed exact.

---

# Typography effects reconstruction

Treat effects as independent layers.

Example stack:

1. glyph mask
2. fill
3. inner texture
4. highlight
5. inner shadow
6. primary outline
7. secondary outline
8. extrusion
9. cast shadow
10. glow / ambient halo
11. distress / print texture

Never bake all effects into an uncontrolled one-pass generative redraw when strict fidelity is required.

For complex treatments such as:
- metallic chrome
- rhinestone letters
- embroidery
- chenille
- puff print
- flocking
- sequins
- glitter
- fur
- inflated 3D lettering
- glass
- jelly
- candy
- neon

preserve material behavior separately from glyph geometry.

**Glyph geometry has higher priority than material beautification.**

---

# Image editing / generation behavior

If an image editing tool is available:

## Exact existing text
- use the reference image as the source;
- protect non-text regions with masks;
- modify the smallest possible region;
- reconstruct letterforms locally;
- do not regenerate the whole image if only typography needs changes.

## New text
- generate/reconstruct typography on a separate transparent layer when possible;
- composite onto the original;
- match original perspective, blur, noise and compression;
- avoid changing surrounding objects.

If a transparent-layer workflow is unavailable, simulate it by minimizing the edit region.

---

# Pixel comparison QA

After reconstruction, compare the source and result at the same scale and crop.

Recommended metrics:

- SSIM on grayscale shape mask
- edge-map overlap / F1
- alpha-mask IoU
- per-channel MAE
- glyph bounding-box deviation
- baseline deviation
- pair-spacing deviation

Recommended strict targets for CLASS A clean references:

- glyph mask IoU >= 0.98
- edge F1 >= 0.97
- SSIM >= 0.97
- average glyph position deviation <= 1.5 px at working resolution
- baseline deviation <= 1 px
- major effect-layer displacement <= 2 px

These are targets, not a license to claim perfection.

---

# Visual QA checklist

Zoom to at least:
- 100%
- 200%
- 400%

Check every character.

For each glyph verify:

- shape
- width
- height
- stroke thickness
- terminals
- counters
- corner shape
- rotation
- vertical position
- left/right spacing
- outline thickness
- shadow offset
- texture scale
- edge softness
- color

Also check the whole word at normal viewing size for optical spacing.

---

# Failure loop

If the comparison fails:

1. identify the exact glyph/effect region that differs;
2. lock all correct regions;
3. redo only the incorrect local region;
4. compare again;
5. repeat until within tolerance or evidence is insufficient.

Do NOT regenerate the entire artwork just because one letter is wrong.

---

# Stop conditions

Stop guessing and ask for better evidence when:

- the target glyph is too small or blurred;
- critical letters are occluded;
- a new requested glyph never appears and no exact font is verified;
- decorative letter detail cannot be distinguished from compression artifacts;
- the source contains perspective so extreme that the original geometry is unknowable;
- the user requires legal/trademark certainty about a proprietary font identity from appearance alone.

---

# User-facing output convention

When successful, state the result class:

- “Exact-reference reconstruction” for CLASS A
- “Reference-glyph recomposition” for CLASS B
- “Best-match new-glyph reconstruction” for CLASS C

Never say “100% exact” merely from visual judgment.

If the user explicitly asks for “100%复刻”, interpret it as:
**use the strictest fidelity workflow available, with no approximation shortcuts.**

---

# Default execution prompt

When invoked with a reference image, internally apply:

> Treat the typography in the reference as immutable visual evidence.  
> Do not substitute a merely similar font.  
> First recover the exact glyph silhouettes, proportions, terminals, spacing,
> baseline, distortion, fill, outline, shadow, texture, and raster edge character.
> If the target wording is unchanged, reconstruct from the original glyph pixels
> or traced outlines. If the target wording changes, reuse existing glyph masters
> wherever possible. Never invent unseen glyphs while claiming exactness.
> Modify only typography-related regions and preserve all unrelated image content.
> Run character-by-character comparison and redo only failed local regions.

---

# Invocation examples

## Example 1
`按 $font-reference-replica 执行，把参考图里的 “FABRIC PIG” 字体和所有效果原样复刻到新图中。`

Expected mode: CLASS A.

## Example 2
`按 $font-reference-replica 执行，用参考图现有字形重新排成 “PIG FABRIC”。`

Expected mode: CLASS B if all glyphs exist.

## Example 3
`按 $font-reference-replica 执行，把 “HELLO” 改成 “WELCOME”，字体风格必须一致。`

Expected mode: CLASS C unless all required glyphs exist or exact font is identified.

---

# Core rule summary

**Existing reference glyphs are source assets, not suggestions.**

**Trace/reuse first. Identify fonts second. Approximate only as a disclosed last resort.**
