# Heavy geometric / expressive display lettering
## Reference-driven style analysis and transfer

Use this reference when the source lettering is very bold, graphic, geometric-organic, exaggerated, or built from distinctive custom silhouettes. The heading describes a family of possible traits, **not a fixed font preset**. Derive the actual rules from each supplied image.

## 1. Lock the source before interpreting it

Record the native-size text block first:
- reading direction and stacking pattern;
- visible glyph order and number of rows/columns;
- occupied width and height of each glyph;
- outer silhouette, top/bottom rhythm and optical margins;
- whether the reference uses solid fill only or has separate outlines, texture, shadow or other effects.

Keep an untouched source copy. Do not infer missing edge detail from an enlarged preview.

## 2. Build a visual fingerprint, not a mood label

Create a small feature table for the actual specimen:

| Feature | What to record |
|---|---|
| Weight | Median stem thickness and the thinnest/thickest visible stroke, normalized by glyph height |
| Straight strokes | End shape, angle, corner treatment, thickness changes and whether ends are square, clipped or wedge-like |
| Curves | Tightness, asymmetry, bulge, tangent at entry/exit and whether the curve feels circular, elliptical or hand-shaped |
| Diagonals | Direction, width profile, terminal flare, taper and intersection behavior |
| Terminals | Flat, rounded, pointed, cut, hooked, flared or custom; note each actual occurrence |
| Joins | Hard intersection, smooth tangent join, overlap, shared stroke, narrow neck or intentional separation |
| Counters | Shape, opening direction, minimum gap, asymmetry and proportion to the black area |
| Character frame | Width/height ratio, component proportions, lean, optical center and local stretching |
| Rhythm | Relative glyph size, line-to-line spacing, optical gap and repeated versus exceptional spacing |
| Surface | Solid black, antialiasing, texture, edge softness and any effects independent of the silhouette |

Use ratios measured from the source wherever possible. Do not force every stroke to the same width or every curve to a circle just because the overall style looks geometric.

## 3. Separate transferable rules from one-off inventions

For each conspicuous feature, label it:
- **family rule** — repeated enough to guide another compatible stroke;
- **glyph exception** — a unique loop, cut, flare or altered component that must stay with its source glyph;
- **uncertain** — the image does not reveal whether the shape is a connection, overlap or gap.

Never copy a visually striking feature onto every new character. Preserve the design language, not a collection of arbitrary flourishes.

## 4. Construct new Chinese glyphs in two passes

### Pass A — identity and topology
- Map the correct Chinese character and its components.
- Lay out all required strokes and counters before adding style.
- Check the character at small size for unambiguous reading.
- Mark every intended bridge, overlap, near-touch and open cut.
- Do not omit a required stroke to make the silhouette look cleaner.

### Pass B — source-specific shape language
- Adapt the measured horizontal, vertical, diagonal and curved stroke families.
- Apply the observed width contrast, corner hardness, terminal shapes and curve tension.
- Shape the negative spaces deliberately; do not leave counters as accidental leftovers.
- Use asymmetric or oversized components only where the source’s visual grammar supports them.
- Preserve the reference’s vertical or horizontal arrangement unless the user asks for a different composition.

Prefer editable vector paths or custom filled stroke outlines. Variable-width strokes may be expanded to outlines before unioning. Keep counters and intentional cuts as explicit subtractive shapes. Avoid global dilation, closing, smoothing or auto-beautification: these can erase thin strokes, close apertures or invent bridges.

## 5. Whole-word composition

Place the glyphs together before finalizing any single glyph. Tune:
- actual black-shape gaps rather than only bounding-box gaps;
- optical centers and baseline/stack rhythm;
- oversized or undersized glyphs relative to neighbors;
- collisions between diagonals and adjacent characters;
- counter visibility at delivery size;
- the full phrase’s silhouette and margins.

Do not automatically use equal-width cells, equal tracking or perfect mathematical centering. Use them only when the source supports that behavior.

## 6. Mandatory local quality check

For each target glyph, verify:
- character identity and component arrangement;
- no missing or duplicated strokes;
- stroke width family and contrast;
- terminal, corner and curve behavior;
- counters and apertures;
- intended gaps remain open;
- intended bridges remain connected;
- silhouette, aspect ratio and optical position;
- spacing in the complete phrase.

At every questionable junction, compare a tight crop of the candidate and its intended construction. Check both foreground ink and negative space. A correct total component count or a high global overlap score does not prove that the right strokes connect.

For a same-glyph source/candidate comparison, align equivalent crops without independently stretching them, then use `scripts/font_compare.py` and explicit masks where automatic segmentation is unreliable. **Do not use whole-image IoU to score different words.** For unseen glyphs, use the checklist and compare measurable style features; label them constructed/style-matched rather than exact.

## 7. Delivery check

Before export:
- foreground pixels are solid black unless the source explicitly specifies otherwise;
- background alpha is truly zero, not a white or checkerboard image baked into the PNG;
- no accidental gray panels, guides or preview checkerboard remain;
- all four edges have adequate transparent padding;
- the final-size raster retains fine strokes, open counters and intended breaks;
- inspect the exported PNG itself, not only the preview.

## Reference-specific reminder

A very bold geometric-organic Chinese display style may combine heavy black mass, straight cuts, broad curves, diagonals, asymmetric counters and unusual terminals. These are only candidate traits: measure which ones the current reference actually uses. Do not force a generic “bold geometric” look over a more distinctive specimen.
