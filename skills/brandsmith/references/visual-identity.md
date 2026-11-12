# Visual identity system

Goal: a system — not a collection of assets — that makes the brand recognisable even without the logo and is easy
for others to apply. Approved values go into `.brand/identity.json`.

## 1. Colour

### Build the palette
- **Roles first, hues second:** primary (recognition), secondary (support), accent (action/emphasis),
  neutrals (text, backgrounds, UI), functional (success/warning/error) if digital.
- **Proportion:** state the intended balance (e.g. 60% neutrals / 30% primary / 10% accent). Distinctive brands
  often own one colour used boldly rather than many used timidly.
- **Category check:** compare with the competitor audit. A colour the category already owns is hard to win.
- **Meaning check:** colour associations vary by culture and sector; mention relevant ones for target markets.
- Work in a perceptual space (OKLCH) when building tints/shades so steps look even:
  `python3 scripts/color_tools.py scale "#1F6FEB" --steps 9`.

### Verify
```bash
python3 scripts/color_tools.py convert "#1F6FEB" "#F4B400"     # HEX/RGB/HSL/OKLCH/CMYK (approx.)
python3 scripts/color_tools.py contrast "#14213D" "#FCA311" "#FFFFFF" "#E5E5E5"   # WCAG matrix
python3 scripts/color_tools.py cvd "#D62828" "#2A9D8F"           # colour-blind simulation
python3 scripts/color_tools.py swatch "#14213D" "#FCA311" -o research/palette.html
```
- Text pairs: WCAG AA needs 4.5:1 for body text, 3:1 for large text (≥24 px regular / ≥18.66 px bold) and UI
  components. AAA: 7:1 / 4.5:1.
- Don't rely on colour alone to distinguish meaning (check `cvd` output).
- **Print:** CMYK values from the script are a naive conversion — a starting point only. Final CMYK and Pantone
  references must be chosen by the designer with a swatch book and confirmed with a print proof. Say so.

## 2. Typography

- **Roles:** display/headline, text/body, optionally a utility (mono, condensed, numerals).
- **Pairing logic:** contrast in one dimension (e.g. serif vs sans) with harmony in another (proportions,
  x-height, era). Or one superfamily used across roles for discipline.
- **Practical checks:**
  - Licence covers the uses: desktop, web, app embedding, logo use, number of users. Mark as `license: to verify`
    in `identity.json` until the designer confirms. Free alternatives (Google Fonts/OFL) when budget matters.
  - Language support: accents and characters for all target languages (and Cyrillic/Greek/other scripts if needed).
  - Weights and styles needed, true italics, tabular figures if data-heavy.
  - Web performance (variable font? subsetting?), fallback stack.
- **Type scale:** base size + ratio (1.2 minor third for dense UI, 1.25 major third general, 1.333 perfect fourth
  editorial, 1.5+ expressive). `tokens.py` generates the scale from `identity.json`.
- Line length 45–75 characters for body text; line height ~1.4–1.6 body, ~1.0–1.2 display.

## 3. Layout & grid
- Define margins, columns and a base spacing unit (4 or 8 px for digital; mm-based for print).
- A **signature layout device** (a fixed logo position, a band, a crop, an alignment rule) helps recognition more
  than another colour.

## 4. Graphic elements
- **Shapes / pattern / supergraphic** derived from the logo idea, not added decoration. Test that it scales from a
  social post to a wall.
- **Iconography:** grid size, stroke weight matched to type weight, corner radius, filled vs outlined, style rules.
- **Illustration** (if any): style, line, colour use, level of detail, who draws it.

## 5. Imagery & photography direction
- Subject, composition, light, colour treatment, depth of field, people (casting, diversity, poses), what to avoid.
- Give 3 do / 3 don't descriptions. Recommend stock search terms or a shot list when relevant.

## 6. Motion (basic)
- Easing personality (snappy vs smooth), duration ranges, logo animation idea (reveal, build, loop), transitions.
- Respect `prefers-reduced-motion` in digital guidance.

## 7. System test

Before approval, mock 4–6 varied applications (see `applications.md`) and evaluate with rubric B. A system that
only works on the business card isn't a system.
