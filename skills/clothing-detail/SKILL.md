---
name: clothing-detail
description: Create faithful macro and close-up detail images from a garment photo for fashion e-commerce pages. Use when the user says 细节图、特写、面料放大、工艺展示、领口袖口下摆特写, or invokes $clothing-detail.
---

# Clothing Detail

Turn an uploaded garment image into independent, photorealistic e-commerce detail shots. Use the available image-editing tool with the uploaded garment as the product reference.

## Select the shots

Follow the user’s named parts and output count. When the user gives no shot list, default to four separate images:

| Garment | Shot 1 | Shot 2 | Shot 3 | Shot 4 |
| --- | --- | --- | --- | --- |
| Top or dress | collar / neckline | cuff or strap | hem | fabric macro |
| Trousers | waistband | pocket or featured decoration | leg opening | fabric macro |
| Skirt | waistband | pocket, bow, charm, or featured decoration | hem | fabric macro |

Choose the visible feature that best represents the actual garment. One image must show only one detail. Generate each shot independently; never combine them into a four-panel grid, collage, contact sheet, or split screen.

If the requested detail is completely hidden or too blurred to verify, do not invent it. Use another clearly visible feature or tell the user that the detail would be inferred.

## Fidelity rules

Treat the source image as the sole authority for the product unless the user explicitly assigns different reference roles.

- Keep color, white balance, fabric, weave, pile, transparency, pattern, scale, placement, construction, seams, and finishing consistent with the source.
- Preserve embroidery and printed text exactly, including letterforms, spelling, position, size, and material.
- Preserve lace motifs, checks, stripes, dots, appliqués, buttons, zippers, pullers, pockets, straps, sliders, drawstrings, charms, toys, and hardware.
- Preserve the original number, position, spacing, orientation, and scale of rhinestones and other decorations.
- Rhinestones must read as slightly raised crystal or glass particles with visible facets, highlights, reflection, and refraction—not printed dots, white spots, sequins, or part of the check pattern.
- Do not add, delete, duplicate, move, resize, recolor, simplify, or reinterpret any visible detail.
- Do not fabricate an unseen material composition or construction technique.

## Standard detail-shot appearance

Unless the user specifies otherwise:

- output four independent 4:3 images at the highest available resolution;
- use a clean white studio background for collar, cuff, waistband, pocket, trim, and hem shots;
- use a slightly oblique macro-camera angle rather than a flat diagrammatic view;
- fill most of the frame with the selected detail while keeping its construction legible;
- use even professional studio light with gentle directional modeling to reveal texture, without hard cast shadows, glare, clipping, or color shift;
- keep the target detail sharply resolved with natural, restrained depth falloff;
- render real textile structure: warp and weft, yarn plies, knit loops, fiber halo, stitch density, needle holes, edge binding, and seam joins when visible;
- avoid plastic, CG, painted, smeared, vector-clean, over-smoothed, oversharpened, and invented texture.

Commercial-camera cues may reference a Sony A7M4 with a 50 mm f/2.8 macro lens, RAW-level textile detail, and softbox lighting. These are appearance cues, not permission to change the product.

## Fabric macro shot

The default fourth image is a full-frame fabric macro:

- fabric fills the entire frame with no visible background;
- arrange it into exactly three broad, continuous, gentle wave folds;
- keep the waves natural and avoid stretching, twisting, rescaling, or bending the pattern unnaturally;
- preserve the same color, weave, pattern scale, rhinestone layout, and surface decorations;
- let rhinestones and prints follow the fabric curvature naturally without moving their source-relative positions.

## Prompt construction

For each requested image, describe:

1. the single target part and how much of the frame it occupies;
2. the exact construction, textile, and decorations that must remain visible;
3. the camera angle, focus plane, and soft directional studio lighting;
4. the source details that must not change;
5. the prohibition on invented or missing product features.

Use a correction like this when needed:

> Resolve individual yarns, weave threads, fiber ends, stitching, and crystal facets. Keep every source-visible detail at its original count, scale, position, and color. The textile must look physically real, never plastic, painted, or AI-smoothed. Do not invent construction hidden by the source.

## Quality check

Before returning the results, verify that:

- each output is a separate image containing one detail only;
- the selected part, crop, and orientation are correct;
- all outputs share the same garment color, material, pattern, exposure, and white balance;
- text, lace, checks, buttons, zippers, charms, and rhinestones remain accurate;
- the textile shows real fibers and construction without synthetic smoothing;
- the fabric macro fills the frame and contains three gentle waves with no background;
- no detail was invented from an unreadable or hidden area.

Retry only the failed shot with an explicit correction when a material requirement is visibly missed.

