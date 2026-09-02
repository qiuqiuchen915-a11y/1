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
