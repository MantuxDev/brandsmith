# Guidelines & handoff

Goal: the people who apply the brand after the designer leaves can do it right. Output in `guidelines/` and
`exports/`.

## 1. Brand book structure

Scale it to the project (a 6-page essentials sheet for a small business; a full book for a large organisation):

1. **Introduction** — purpose, positioning, personality (short).
2. **Logo** — idea/rationale, variants, colour versions, clear space, minimum sizes, placement, misuse (do/don't).
3. **Colour** — palette with roles and proportions; HEX, RGB, CMYK, Pantone (if defined); accessible text pairs.
4. **Typography** — families, roles, weights, scale, line height, fallbacks, licence notes.
5. **Graphic elements** — shapes, patterns, icons, illustration rules.
6. **Imagery** — photography/illustration direction, do/don't.
7. **Voice** — voice summary, principles, vocabulary, examples (from `copy/voice.md`).
8. **Applications** — key touchpoints and templates.
9. **Assets & contacts** — where files live, file naming, who to ask.

Build it as a single HTML page (printable to PDF) or in the designer's tool. Pull values from `identity.json` so the
book and the tokens never disagree.

## 2. Asset kit (`exports/`)

```
exports/
├── logo/
│   ├── svg/      primary, horizontal, stacked, symbol, wordmark × (color, one-color-dark, reversed)
│   ├── png/      same set at @1x/@2x/@3x, transparent background
│   └── print/    PDF/EPS (from the designer's vector tool), CMYK and Pantone versions
├── favicon/      favicon.svg, favicon.ico (16/32/48), apple-touch-icon 180, android 192/512, site.webmanifest snippet
├── social/       avatar 400×400 (circle-safe), cover images per platform
├── color/        palette swatches (ASE/HTML), tokens
└── fonts/        (only if the licence allows distribution) or links to obtain them
```

- `python3 scripts/export_variants.py master.svg -o exports/logo --color "#14213D"` generates SVG variants and,
  if a rasteriser is installed (rsvg-convert, Inkscape or cairosvg), PNGs and favicon sizes.
- Print files (CMYK PDF/EPS, Pantone) must come from the designer's vector tool; you can't reliably create them.
- **File naming:** `brand_logo_horizontal_color.svg` — lowercase, underscores, no spaces, consistent order
  (brand, asset, variant, colour, size).

## 3. Design tokens for developers

```bash
python3 scripts/tokens.py .brand/identity.json -o exports/tokens --format all
```
Outputs: `tokens.json` (W3C Design Tokens format), `tokens.css` (custom properties), `_tokens.scss`,
`tailwind.theme.js`. Share with developers alongside a short note on usage (which colour for text, which for
backgrounds, accessible pairs).

## 4. Handoff checklist

- [ ] All logo variants exported and opened to check (no stray points, correct colours, transparent background)
- [ ] Clear space and minimum sizes stated
- [ ] Colour values consistent across book, tokens and files
- [ ] Font licences confirmed for the client's uses
- [ ] Trademark/name checks done by a human (if naming was in scope)
- [ ] Guidelines reviewed by someone who wasn't on the project (can they apply it?)
- [ ] `.brand/status.md` set to `handoff: approved`; final decision logged
