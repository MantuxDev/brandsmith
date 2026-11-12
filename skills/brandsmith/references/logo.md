# Logo

A logo is an **identifier, not an explanation**. It needs one clear idea, built with craft, that works from 16 px
to a building, in one colour, for years. The designer draws the final mark; your concepts are fast, honest starting
points they can react to, refine or redraw.

## 1. Choose the mark type

| Type | When it fits | Watch out for |
|---|---|---|
| **Wordmark** | Distinctive or short name; brand must be named every time; early-stage brands | Generic type = generic brand; needs letterfit craft |
| **Lettermark / monogram** | Long names; need for a compact symbol | Category is crowded with circle-monograms |
| **Pictorial** | A concrete, ownable image linked to the idea | Literalness (a coffee cup for a café); clichés |
| **Abstract** | Broad offer, global, needs a flexible system | Meaningless without investment; hard to differentiate |
| **Combination** | Most practical default: symbol + wordmark | The lockup must work both together and apart |
| **Emblem** | Heritage, institutions, craft, badges | Poor scalability; detail dies at small sizes |
| **Mascot** | Consumer brands with character and storytelling | Hard to keep fresh; detail; can feel childish |
| **Dynamic / system** | Brands with many outputs; culture and media | Needs a fixed core so it stays recognisable |

Recommend a type from the brief and say why. Usually a combination mark with a strong wordmark is the safe base.

## 2. Concepting

- Start from the **strategy and the chosen direction**, not from other logos. Write the idea first in words:
  "The *a* and the arrow share a stroke → movement built into the name".
- Generate idea routes: letterform manipulation, negative space, a single meaningful detail, a shape derived from
  the product or place, a typographic gesture, a geometric construction, a mark that becomes a pattern.
- For each concept: name, one-line idea, mark type, why it fits the brief, risk.
- **Three concepts per round is the default**, deliberately different (safe / stretch / in between).

## 3. Building concepts as SVG

You can build clean geometric concepts directly as SVG. Rules:
- `viewBox` set, no fixed `width`/`height` in the master, no transforms left unapplied where avoidable.
- Shapes, not strokes, in final masters (convert strokes to outlines). Strokes are fine in sketches.
- **No live text** in a logo master. If you only have a font name, keep the wordmark as text in a *sketch* file
  and tell the designer the wordmark needs setting and outlining in their tool (or with the actual font).
- Few colours (1–3), solid fills; gradients only if the idea demands it and a flat version exists.
- Build on a grid or simple geometry when it helps, but optically correct what geometry gets wrong (see §4).
- Save to `concepts/round-N/<concept>-mark.svg`, `-lockup-horizontal.svg`, `-lockup-stacked.svg`.

Be honest: AI-drawn SVG is good for geometric marks and quick sketches; organic, illustrative or typographic
finesse belongs in the designer's hands. Say which concepts need redrawing.

## 4. Optical refinement checklist (for craft critique and for the designer's refinement)

- **Overshoot:** round and pointed shapes extend slightly (≈1–3%) beyond flat ones to look the same size.
- **Optical centring:** visual centre sits slightly above the geometric centre; triangles and asymmetric marks
  need adjustment.
- **Stroke contrast:** horizontals look heavier than verticals at the same thickness; thin horizontals slightly.
- **Joins and ink traps:** where strokes meet, thin them to prevent dark blobs at small sizes.
- **Curves:** smooth tangents, extreme points on horizontals/verticals, minimal nodes, no kinks.
- **Angles:** consistent and intentional; 44.7° looks like a mistake (`svg_audit.py` flags near-misses).
- **Spacing:** letterfit in the wordmark judged on area, not distance; check round-to-straight pairs.
- **Symbol-to-wordmark ratio:** balanced weight; cap height or x-height alignment intentional.
- **Counter sizes:** open enough to survive 16 px and print gain.

## 5. Testing

Run on every concept before showing it:

```bash
python3 scripts/lab_metrics.py concepts/round-1/a-mark.svg        # score and minimum size as numbers
python3 scripts/logo_lab.py concepts/round-1/a-mark.svg -o concepts/round-1/a-lab.html --name "Brand" --color "#14213D"
python3 scripts/svg_audit.py concepts/round-1/*.svg
python3 scripts/preview_sheet.py concepts/round-1/*-mark.svg -o concepts/round-1/test-sheet.html
python3 scripts/preview_sheet.py concepts/round-1/a-mark.svg --compare research/competitors/*.svg -o concepts/round-1/shelf.html
```

Tests the sheet covers, and what to look for:
- **Size ladder** (512 → 16 px) — when does detail collapse?
- **16 / 32 px** pixel rendering — favicon and tab legibility.
- **One colour & reversed** — does the idea survive without colour? On dark?
- **Backgrounds** — white, black, brand colour, mid-grey, a busy photo-like pattern.
- **Squint (blur)** — is the silhouette distinctive?
- **Mirror / rotate** — accidental shapes or associations?
- **Contexts** — favicon, app icon (rounded square), website header, social avatar (circle crop), business card.
- **Shelf test** — next to competitors: does it stand out, does it belong to the category?

Additional checks to do mentally or ask the designer about: embroidery/engraving/stamping if relevant, animation
potential, cultural or gestural associations in target markets, accidental resemblance to existing marks
(recommend a reverse image search and a trademark check by a human).

## 6. Presenting concepts (checkpoint)

Show: the test sheet path, per concept one line (idea) + the main risk, and your recommendation. Ask the designer
to pick a direction, combine, or reject. Do not build the full kit before a direction is approved.

## 7. Lockups & rules (after approval)

- Variants: primary (horizontal), stacked, symbol only, wordmark only.
- Colour versions: full colour, one colour (dark), reversed (light on dark).
- **Clear space:** defined by an element of the mark (e.g. the height of the *x*), not an arbitrary number.
- **Minimum size:** in px for screen and mm for print, from the size-ladder results.
- **Don'ts:** stretch, recolour outside palette, add effects, rotate, rearrange lockup, place on low-contrast
  backgrounds, outline.
- Run `scripts/export_variants.py` for the kit; record paths in `identity.json` → logo.

## 8. Redesign / refresh

Diagnose first (Evaluate mode, rubric A). Then decide with the designer: **refine** (same idea, better craft),
**evolve** (keep distinctive assets, update the rest), or **replace** (new idea; needs a strategic reason).
Show the old and new side by side at the same sizes and contexts.
