---
name: clothing-extraction
description: Extract one garment from a model, street-style, buyer-show, or cluttered product photo and turn it into a faithful white-background flat-lay e-commerce image. Use when the user says 提取衣服、扒图、转平铺、抠成商品图、从买家秀提取, or invokes $clothing-extraction.
---

# Clothing Extraction

Turn an uploaded clothing photo into a clean, front-facing flat-lay product image. Use the available image-editing tool with the uploaded image as the reference.

## Choose the target

- If the user names a garment, extract only that garment.
- If one garment is clearly dominant and the user says “这件衣服”, use the dominant garment.
- If several garments are equally plausible, ask which one to extract.
- For a full outfit, create one result per garment unless the user explicitly requests a combined set.

## Preserve the product

Keep the source garment faithful:

- original color and white balance;
- fabric, weave, texture, pile, transparency, and weight;
- silhouette, proportions, length, neckline, sleeves, waist, seams, pleats, darts, and hem;
- prints, checks, stripes, embroidery, text, logos, rhinestones, lace, buttons, zippers, drawstrings, straps, sliders, pockets, and ornaments;
- the original count, size, spacing, placement, orientation, and scale of every visible design element.

Do not invent, delete, duplicate, move, resize, recolor, or simplify visible product details. Reconstruct occluded areas conservatively from symmetry and normal garment construction. Treat completely hidden details as inferred, never as verified.

## Remove everything else

Explicitly remove the person, skin, hair, body volume, invisible-mannequin shape, jewelry, bags, shoes, other garments, hangers, supports, props, furniture, text overlays, watermarks, and the original background. Nothing except the target garment may remain.

Preserve genuine branding on the garment. Do not remove a third party’s brand mark to misrepresent ownership.

## Output appearance

- One complete garment, fully inside the frame.
- Front view, centered, naturally laid flat, left-right balanced, and free of body volume.
- Pure white seamless background, RGB 255/255/255.
- Even soft studio lighting with no visible cast shadow, hard reflection, or blown highlight.
- High-resolution commercial e-commerce retouching.
- Repair lint, dust, loose threads, stains, and accidental wrinkles while retaining intentional gathers, pleats, texture, drape, and construction.
- Avoid plastic texture, painted fabric, excessive sharpening, over-smoothing, warped edges, and paper-thin appearance.

Respect a user-specified aspect ratio or crop. Otherwise use a square product-image composition with comfortable white margins.

## Editing prompt

Build the image-editing request with these four parts:

1. **Target:** Output only the exact garment, naming its category, color, and defining features.
2. **Removal:** List every non-target item visible in the source and remove each one.
3. **Layout:** Lay the garment flat, centered, front-facing, symmetric, complete, and fully unoccluded.
4. **Fidelity:** Preserve the original color, material, construction, pattern, trims, and design-element placement exactly.

Add this constraint when needed:

> Nothing but the garment may remain. The garment must be completely flat, with no human body volume or invisible mannequin. Do not add, delete, move, duplicate, resize, recolor, or reinterpret any garment detail.

## Quality check

Before returning the result, check that:

- only the requested garment remains;
- the entire garment is visible and correctly oriented;
- the white background is clean and shadowless;
- proportions and left-right construction are plausible without forced distortion;
- colors, fabric, patterns, text, hardware, trims, and decorations match the reference;
- inferred areas do not introduce unsupported design features.

If the result materially fails any check, retry the edit with a more explicit correction focused on the failed attribute.

