# Mode: Evaluate

Structured critique of a logo, an identity system, brand copy, or the consistency of a brand across touchpoints.
The designer may be evaluating their own work, a colleague's, a client's existing brand, or a competitor.

## 1. Establish context (before judging)

A logo can only be judged against what it's for. Before scoring, know (from `.brand/` or by asking):

- What the brand does, for whom, and where it will mostly live (app icon? shop sign? packaging? B2B decks?).
- What stage the work is at: **early concept** (judge the idea, ignore finish), **refinement** (judge craft),
  **final / live** (judge everything, including system and consistency).
- What the designer wants from you: a full audit, a gut check, a comparison of options, or a client-facing
  rationale. Match the depth.

If context is missing and the designer just wants a quick read, proceed and state your assumptions at the top.

**Match the length to the ask.** "Gut check", "quick look", "two minutes", "veloce", "al volo": reply in at most
~200 words, with a one-line verdict, the 2–3 issues that matter most with one fix each, and the path of the Lab page.
No score table and no optional sections; offer the full report in one line. A full critique is for "critique",
"review", "audit" or a final round.

## 2. Gather evidence

- **Logo SVG:** run `scripts/lab_metrics.py <file.svg>` for the Lab score and minimum size (never estimate them),
  `scripts/svg_audit.py <file.svg>` (file hygiene, construction, tiny details, painted knock-outs) and
  `scripts/logo_lab.py <file.svg> -o <dir>/lab.html --name "<Brand>" --color "<hex>"` (score, minimum size,
  scalability metrics and 20+ context tests). Give the designer the lab path; it's also their client-ready
  visual evidence. Use `preview_sheet.py --compare` for a shelf test against competitor marks.
  Look at the results (render the page to an image if you can; otherwise reason from the audit and the SVG source).
- **Raster logo (PNG/JPG):** look at it directly. Recommend getting the vector for a full audit.
- **Palette:** `scripts/color_tools.py contrast <hex…>` for the WCAG matrix, `scripts/color_tools.py cvd <hex…>`
  for colour-blind safety.
- **Copy:** read it against `brand.md` → Voice and Messaging.
- **Touchpoints (site, social, decks):** collect screenshots or text; compare against `identity.json` and
  guidelines.
- **Competitors:** if a shelf test matters, put the mark next to competitor marks in `preview_sheet.py --compare`.

## 3. Score with the rubrics

Use the matching rubric in `rubrics.md`. Score each criterion 1–5, and **justify every score with a specific
observation**. No score without evidence. Skip criteria that don't apply at this stage and say so.

## 4. Report format

Write the report to `research/critique-YYYY-MM-DD-<subject>.md` (or show it inline if short), always in this shape:

```markdown
# Critique — <subject> (<stage>)

**Verdict:** <one or two sentences: does it work, and the single most important thing to change>

## Scores
| Criterion | Score | Evidence |
|---|---|---|
| … | 4/5 | … |
**Overall:** x.x/5 (weighted as in rubrics.md)

## Priority issues
1. **[High] <issue>** — what you observed → why it matters (in use, not in theory) → **fix:** concrete action
2. **[Medium] …**
3. **[Low] …**

## Keep
- What works and must survive the revision (be specific).

## Optional explorations
- Directions worth trying that go beyond fixing (max 3).

## To verify outside this review
- e.g. trademark search, font licence, print proof, user testing.
```

Rules:
- **Priority = impact on real use**, not personal taste. Label taste-level notes as `[Taste]`.
- **At most 5 priority issues.** If there are more, the top five are what matter now.
- **Fixes are actionable**: "increase the counter of the *e* by ~8% and open the aperture" beats "improve legibility".
- **Separate the idea from the execution.** A strong idea badly drawn needs refinement, not a new concept.
- **Check before you claim.** Don't say "one-colour will be trivial" or "it holds at 16 px" from reading the
  file: verify it (`export_variants.py` warns when colours merge; the Lab's one-colour test shows it). A mark whose
  idea is one colour on top of another (a figure on a tile) usually needs a designed one-colour version.
- **No generic critique.** Every finding must point at something locatable (an element, a size, a value, a
  touchpoint) and be checkable by the designer. Banned unless followed by specifics: "clean", "modern",
  "balanced", "strong", "works well", "could be more impactful", "consider simplifying". If you can't be specific,
  leave it out. Designers drop a tool the first time it sounds like a horoscope.
- **Say what you can't judge.** Fit with a client relationship, cultural nuance in a market you don't know,
  physical production: name them as limits instead of guessing.
- **Comparison of options:** score each, then a head-to-head table and a recommendation with the deciding reason.

## 5. Client-facing version (on request)

If the designer needs to share the critique with a client, rewrite it without jargon, framed around business
outcomes, and without the `[Taste]` notes. Keep the internal version too.

## 6. Record

Save notable findings to `.brand/status.md` (open issues) so a later **Create** or **Continue** session acts on them.
