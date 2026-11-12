# Mode: Continue

For picking up an identity already in progress: the designer's own paused project, a colleague's handover,
a client's existing brand that needs extending, or work from another agency.

## Case A — `.brand/` exists

1. Read `status.md` → `decisions.md` → `brand.md` → `identity.json` → latest `feedback.md` round.
2. Check that the files on disk match the memory (e.g. logo paths in `identity.json` exist; newer files in
   `concepts/` that the memory doesn't know about). Report mismatches.
3. Summarise in at most five lines: phase, what's approved, what's open, last feedback, proposed next step.
4. Ask "carry on with <next step>?" — or just proceed if the designer already said what to do. You may run checks
   (audits, Lab, contrast) without asking, but don't produce new design work (variants, concepts, copy) until the
   designer confirms the next step: "let's resume" is not a brief.

## Case B — no `.brand/`, but existing material

Reconstruct the memory from evidence. Accept anything: a folder of files, a PDF of guidelines, a Figma export,
a website URL, screenshots, a pitch deck, an old brief.

1. **Inventory.** List what you were given and what each item tells you. Run `svg_audit.py` on logo SVGs.
2. **Extract.**
   - Colours: from SVG/CSS/guidelines (exact values), from images (approximate — flag as such).
   - Type: from CSS `font-family`, PDF fonts, guidelines; from images only as a guess (`(assumption)`).
   - Logo: master file, variants present, clear space and minimum size if stated.
   - Voice and messaging: from site copy, about page, social bios, decks.
   - Strategy: from brief or deck; otherwise infer and tag `(assumption)`.
3. **Initialise** `.brand/` with `brand_init.py` and fill it. Every inferred item gets `(assumption)`;
   every value from an authoritative source gets its source noted.
4. **Gap report.** What's missing or inconsistent for the work ahead: e.g. "no reversed logo", "three different
   blues across site and deck", "no voice definition", "logo exists only as PNG".
5. **Confirm with the designer** the assumptions that matter for the next step (not all of them).
6. **Proceed** in Create or Evaluate mode from the right phase.

## Respecting existing equity

When continuing someone else's work, the default is **evolution, not revolution**. Identify the brand's
distinctive assets (the shape, colour, word, sound people already recognise) and protect them unless the designer
or the brief says otherwise. Record them in `brand.md` → Visual direction → "Distinctive assets to keep".

## Handover out

When the designer is about to pause or hand the project on, offer a handover: update `status.md` thoroughly
(including "Waiting on" and "Open questions") so the next session, or the next person, starts cold without losing
anything.
