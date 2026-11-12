# Changelog

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
