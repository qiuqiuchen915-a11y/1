# font-reference-replica v2

This version focuses on **glyph-structure reconstruction**, not simple font matching.

## What changed in v2

- Adds glyph skeleton analysis
- Adds stroke-topology reconstruction
- Adds stroke-width profiles
- Adds Chinese component/radical proportion analysis
- Adds terminals, joins, counters and negative-space reconstruction
- Adds per-glyph deformation fields
- Adds anti-AI-drift rules
- Adds character-by-character QA
- Adds stricter geometry thresholds
- Explicitly forbids similar-font substitution

## Recommended use

```text
按 $font-reference-replica 执行。
参考图：图1
目标文字：早秋上新季

要求：
完全按照参考图重建字体结构、字形、笔画数量、笔画粗细变化、转折、收笔、
局部拉伸压缩、倾斜、重心、字距、描边、颜色、纹理和阴影。
禁止任何相似字体替代。
```

## Important limitation

If a character is visible in the reference, tracing/reuse can approach pixel-level fidelity.

If a requested character never appears in the reference, mathematical identity cannot be proven
without the original font/vector source or another reference containing that character.

## Comparison helper: dependencies and regression tests

Python 3.9+ with `numpy` and `Pillow` is required. `scikit-image` is optional
and enables SSIM. Tests use the standard-library `unittest` runner and synthetic
stroke images (no font download or external fixtures).

From the repository root:

```bash
python -m pip install numpy Pillow
# Optional, to enable and test numerical SSIM:
python -m pip install scikit-image
python -m unittest discover -s skills/font-reference-replica/tests -v
python skills/font-reference-replica/scripts/font_compare.py reference.png candidate.png --diff font_diff.png
```

### Glyph masks

The helper reports **Glyph mask IoU**, replacing the misleading `Alpha IoU`
label. Consumers parsing the old label must update. It also reports each mask's
source and a separate **Mask Edge F1**.

- With alpha values <=127, the automatic mask uses alpha >127. This assumes
  alpha actually isolates the lettering, not an opaque panel, shadow or prop.
- Otherwise (including RGB/JPEG and fully opaque PNG), it estimates background
  RGB from the median image-border color, and selects pixels whose maximum
  channel difference exceeds `--background-tolerance` (default 16, range 0–254).
  This supports dark or light lettering on plain backgrounds. The crop must have
  clean background padding on every side. Non-uniform borders fail explicitly.
- This is a plain-background heuristic, not semantic segmentation. Interior
  decorations, gradients, similar foreground/background colors, shadows and
  texture can defeat it even with a uniform border. Inspect the segmentation;
  for complex images or base-glyph-only QA, provide independently verified masks:

  ```bash
  python skills/font-reference-replica/scripts/font_compare.py reference.png candidate.png \
    --reference-mask reference_mask.png --candidate-mask candidate_mask.png
  ```

  Each mask must match its image size: grayscale white=lettering, black=background
  (threshold >127; mask alpha is not used). Explicit masks override automatic
  extraction independently for either image. Both empty masks report IoU `N/A`,
  never a perfect match; one empty mask scores zero.

### Metric scope and alignment

All metrics compare the same pixel coordinates. Equal dimensions alone do not
prove alignment. Prepare matching per-glyph crops, scale, baseline, rotation and
perspective first; do not independently stretch each crop to hide proportion
errors. The script rejects unequal dimensions and never resizes or auto-aligns.
Keep a separate unaligned check when evaluating layout, position or spacing.

| Metric | What it measures / conditions for glyph QA |
|---|---|
| Glyph mask IoU | Binary foreground overlap, including holes and missing strokes. Requires validated background separation and alignment; ignores color and within-stroke texture. |
| Mask Edge F1 | Exact-pixel contour overlap on extracted masks. Requires the same separation and alignment; no positional tolerance, skeleton or Hausdorff calculation. Empty contours yield zero, not evidence of success. |
| Edge F1 | Existing grayscale gradient threshold (0.10). Includes background, texture and effect edges; separate background/effects first for contour conclusions. Color differences with equal luminance may be missed. |
| MAE | Full-canvas RGB error in [0,1], after compositing transparency on white. Background and blank padding can dominate/dilute it. Use tightly matched crops on a common background for glyph raster/texture QA; masks do not automatically restrict this metric. |
| SSIM | Full-canvas grayscale structural similarity, also white-composited. Needs aligned, background-normalized crops; not a color or standalone glyph-accuracy score. Optional dependency absent or unsupported image dimensions produce `N/A`; other unexpected failures are not silently swallowed. |

Transparent hidden RGB is ignored. The saved difference image is RGB so that
identical alpha channels do not make the differences invisible. An explicit mask
only changes mask metrics; it does not remove background from MAE, Edge F1, SSIM
or the difference image. None of these aggregate scores proves correct character
identity or local scratch/texture fidelity. Preserve the SKILL.md per-character,
geometry-first reconstruction rules and inspect local crops and effects separately.


## Revision 2.4: reference-style extraction and changed-text transfer

The skill now requires a **Reference Style Sheet** before reconstructing new wording. It separates observed source features from reusable style rules and one-off glyph inventions, inherits the reference layout unless the user requests a change, and requires a two-pass process for unseen Chinese characters: preserve character identity/topology first, then transfer measured stroke and contour behavior.

For bold, geometric-organic or expressive display lettering, follow [heavy-geometric-display.md](references/heavy-geometric-display.md). This guide emphasizes stroke-width ranges, terminals, curve tension, counters, intentional gaps/bridges, whole-word rhythm and transparent-PNG validation. It does not promise mathematical 100% reproduction for unseen characters; use “traced/reused” for source-visible forms and “constructed/style-matched” for inferred forms.
