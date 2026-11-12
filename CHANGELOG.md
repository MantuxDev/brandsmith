# Changelog

## 0.4.0 — 2026-11-12
- **Logo Lab redesign** (from the design handoff). Header with file chip (name, type, colour count), IT/EN
  switch, "Change logo" and "Export report". Verdict card with score, minimum size, ruler 16–256 px and a
  "To check" list that links to each flagged test; test index by section with status and counts; filter
  "All tests / To check"; sections where everything passes start folded; every flagged test says what happens
  and how to fix it. New empty state (drop area, paste from Figma/Illustrator with Ctrl+V, sample mark).
  On phones: summary card, section chips and a fixed bottom bar.
- **Export panel** replaces the direct PDF button: "For me / the studio" or "For the client", studio name,
  client note, a page-1 preview, what each report includes, the PNG kit.
- **Reports rebuilt.** Designer report, 4 A4 pages: verdict and 8 metrics with the limiting one highlighted,
  "To check · N of 23" with page references; size and legibility (scale with below-minimum sizes marked, real
  16/32 px pixels, four blur levels); form and context; reproduction, SVG file and next steps generated from
  the warnings. Client report, 2 pages, no score or jargon: the mark, "At a glance", which version to use, the
  studio's note, where the mark will live, what to avoid.
- **New mark ("Mirino")** in the header, favicon, PDF header and Figma icon/cover; sources in `docs/brand/`.
  The handoff geometry was adjusted (ring r 12.5 → 11.5, ticks 7.5 → 5.5 units) because the gap between ticks
  and ring closed below 64 px; the adjusted mark scores 10/10 and holds at 16 px in Logo Lab.
- Colour count ignores anti-aliased edges; distorted-mark example in the client report is actually distorted.
- `tools/test_lab_ui.py`: headless smoke test of the interface and both reports (`--sample` rewrites
  `docs/sample-report.pdf`). Figma plugin bridge updated for the new layout.
- The measuring engine is unchanged: scores and minimum sizes are the same as 0.3.1.

## 0.3.1 — 2026-11-12
- Eval run of the skill (11 cases, see `evals/notes/2026-11-12-eval-run.md`) and fixes from it:
  `lab_metrics.py` reads the real Lab score headlessly (the skill never estimates it); gut checks stay short;
  Continue mode asks before new design work; `tokens.py` exports only what `identity.json` defines and prefixes
  Tailwind keys with `brand-`; `svg_audit.py` warns about painted knock-outs; generated lab pages make no network
  requests.

## 0.3.0 — 2026-11-12
- Logo Lab rebuilt: new interface (verdict first, pixel ruler, five test sections), Italian/English, light/dark,
  one-click PDF report with studio name, designer's note and a **client version** without the score.
- New score model: thinnest stroke and narrowest gap measured on a 512 px render (granulometry plus a topology
  check for breaks and merges), converted to the smallest size at which both stay ≥ 1 px. Validated within
  ±0.5 px on synthetic marks; corner-to-corner contacts (pixel art) no longer count as breaks.
- "How the score works" explanation in the page.
- Logo Lab for Figma (`figma-plugin/`, built by `tools/build_figma_plugin.py`) and for Illustrator
  (`illustrator/LogoLab.jsx`, built by `tools/build_illustrator_script.py`).
- The published page (`docs/index.html`) makes no network requests.
- Sample report (`docs/sample-report.pdf`, from `docs/sample-mark.svg`) and Figma Community listing kit.
- `tools/calibrate.py` (headless calibration) and `tools/case_study.py` (blind real-world case studies).

## 0.2.0 — 2026-11-12
- **Logo Lab** (`logo_lab.py` + standalone `templates/logo-lab.html`): score /10 with minimum size and the
  metrics behind it; two-tone marks measured on silhouette and internal shapes; 20+ tests (scale, pixels,
  blur, negative space, visual weight, clear space, app-icon grid, favicon tabs, type lockups, photo,
  billboard, pattern, watermark, materials, emboss/deboss, halftone, embroidery, one-colour/reversed,
  curvature combs, anchor points, SVG source) and an in-browser PNG export kit. Works offline by drag and drop.
- Checks-only mode, Figma/Illustrator paste-in workflow, confidentiality guidance and a no-generic-critique rule.
- `export_variants.py` warns when a multi-colour mark collapses in one colour.
- README reorganised around the checks, the no-terminal paths, plans, privacy and studio roll-out.
- `tools/build_release.py` builds the uploadable skill ZIP and the hostable Logo Lab.

## 0.1.0 — 2026-11-12
- First version: Create / Evaluate / Continue modes, ten modules, rubrics, `.brand/` project memory, six scripts,
  evals, example project.
