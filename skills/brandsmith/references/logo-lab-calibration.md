# Logo Lab score: method and calibration

How the Logo Lab scalability score is computed, how it was checked, and what it does not tell you.
Read this before explaining a score to a designer or a client.

## What is measured

On a 512 px render of the mark (6% padding):

1. **Thinnest stroke.** Morphological opening with growing disk radii. The stroke thickness is the first radius
   at which either more than 2% of the ink disappears, or the topology changes: a stroke breaks into parts or a
   significant part vanishes. Ink is 8-connected, and the topology after the first sub-pixel step is the baseline,
   so corners that touch (pixel art, touching shapes) do not count as breaks.
2. **Narrowest gap.** The same with closing, on the background: the first radius at which gaps fill more than 2%
   of the ink area, parts merge or an enclosed counter fills.
3. **Two-tone marks.** If the mark carries its idea in internal tonal contrast (a light figure on a dark tile),
   both measurements also run on the dark/light split. The lower result counts.

Thicknesses are expressed in px of a 256 px canvas. The **minimum size** is the smallest square render size at
which the limiting feature stays at least 1 px wide (`256 × 1 / thickness`), rounded up to
16 / 20 / 24 / 32 / 48 / 64 / 96 / 128 / 192 / 256 px. The **score** is that size on a log scale where
16 px = 10 and 256 px = 0. Nothing else enters the score.

Fidelity at 16/32 px, parts, fill ratio, symmetry and negative space are shown for information. They don't change
the score.

## Validation on shapes of known thickness

There are 24 synthetic marks: rings with strokes from 0.5% to 12% of the mark, bars with gaps from 0.5% to 8%, and
a disc plus a comb of 1% lines making up 0.5% to 8% of the ink (`tools/calibrate.py synth`).

- For features under 17 px, the measured stroke and gap match the drawn geometry within **0.30 px on average,
  0.61 px at most** (n = 16).
- Hairline gaps down to 0.5% of the mark (about 1 px at 256) are detected.
- Thin details that are detached from the mark are flagged even when they are a small share of the ink, because
  they disappear entirely at small sizes.

## Behaviour on real marks (380 SVGs, 2026-11-12)

| Set | n | ≤ 24 px | ≥ 64 px | Score p10 / p50 / p90 |
|---|---:|---:|---:|---|
| Simple flags (tricolours, crosses, discs) | 23 | 96% | 4% | 9.6 / 10.0 / 10.0 |
| Simple Icons (icon-sized brand marks and wordmarks, random 300) | 300 | 46% | 26% | 4.0 / 8.3 / 10.0 |
| Flags with coats of arms | 27 | 4% | 85% | 0.0 / 0.0 / 7.2 |
| Municipal coats of arms (Wikimedia) | 6 | 0% | 100% | 0.0 / 0.0 / 1.2 |

- **Simple marks hold at small sizes; detailed emblems don't.** The separation between the two is clear.
- **Simple Icons mixes symbols and wordmarks**, so it spreads across the range. In a blind visual review of 30
  marks the Lab flagged as needing 64 px or more, 24 were clearly right: small wordmarks, hairlines and illustrated
  marks. The other 6 were too harsh. The main cause, corner contacts in pixel-art marks, has been fixed since.
- The third-party marks used for calibration are not stored in the repository.

Reproduce with:

```bash
python3 tools/calibrate.py synth test-projects/calibration/synth
python3 tools/calibrate.py run synth=… si=… -o results.jsonl
python3 tools/calibrate.py report results.jsonl
```

## Limits (say them when it matters)

- **It measures reproduction risk, not quality.** A crest on a wine label doesn't need to work at 16 px. A low
  score is a fact about small sizes, not a verdict on the mark.
- **The 1 px threshold is conservative.** Anti-aliasing keeps a 0.7 px line faintly visible. The minimum size
  is where details stop being *reliable*, not where they vanish.
- **Isolated specks are not in the score.** Parts smaller than ~0.4% of the ink (a tiny dot, a ® symbol) are ignored
  so they don't dominate the result; `svg_audit.py` reports them. Quote both when it matters.
- **Rasters (PNG) are measured at their own resolution**, after background removal if they are opaque. SVG is
  more precise.
- **Effects** (blur, shadows, gradients to transparent) are measured as rendered, so soft edges count as thin.
- **Not yet calibrated against designers' judgement on real client work.** That is the next step:
  `tools/case_study.py` records each designer's own minimum size before they see the Lab's, and reports how often
  the two agree within one step.
