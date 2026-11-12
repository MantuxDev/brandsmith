# Project memory — the `.brand/` folder

The `.brand/` folder is the single source of truth for a brand project. Every mode reads it before working and
updates it after. It is what lets a designer close the laptop on Tuesday and pick up exactly where they were on
Friday, or hand the project to a colleague.

## Layout

```
<project>/
├── .brand/
│   ├── status.md        # Where the project stands: phase, approved, in review, next steps, open questions
│   ├── brand.md         # The brand: brief, audience, positioning, personality, voice, messaging
│   ├── identity.json    # Machine-readable identity: colours, type, spacing, logo files (feeds the scripts)
│   ├── decisions.md     # Decision log: date, decision, reason, who decided
│   └── feedback.md      # Client feedback rounds and how each point was handled
├── research/            # Competitor audit, moodboards, references
├── concepts/            # Logo and identity concepts, by round (round-1/, round-2/…)
├── copy/                # Tone of voice, tagline options, website/social copy
├── exports/             # Final asset kit
└── guidelines/          # Brand book
```

The designer may already have their own folder structure. **Adapt to it**: keep `.brand/` but write files where
their structure says, and record the mapping in `status.md` under "Project folders".

## File rules

### `status.md`
- Always current. Rewrite the "Now" section; never let it go stale.
- Phases: `discovery → research → strategy → naming → logo → identity → copy → applications → guidelines → handoff`.
  Not every project uses every phase; mark skipped phases as `skipped` with the reason.
- Each phase is one of: `not started`, `in progress`, `in review`, `approved`, `skipped`.
- "Next steps" are concrete actions, not themes.

### `brand.md`
- Fill sections as they become known. Mark unknowns as `TBD`. Never invent client facts: if you infer something,
  tag it `(assumption)` until the designer confirms.

### `identity.json`
- Only approved or candidate values. Use `"status": "candidate" | "approved"` on each entry.
- Schema (all keys optional):

```json
{
  "name": "Brand",
  "colors": [
    {"name": "Ink", "role": "primary", "hex": "#14213D", "status": "approved",
     "cmyk": "", "pantone": "", "notes": ""}
  ],
  "typography": [
    {"role": "display", "family": "Example Grotesk", "weights": [500, 700], "source": "foundry or URL",
     "license": "to verify", "fallback": "system-ui, sans-serif", "status": "candidate"}
  ],
  "type_scale": {"base": 16, "ratio": 1.25},
  "spacing": {"base": 8},
  "radius": {"sm": 4, "md": 8, "lg": 16},
  "logo": {
    "master": "concepts/round-2/mark.svg",
    "variants": {"primary": "", "horizontal": "", "stacked": "", "symbol": "", "one_color": "", "reversed": ""},
    "clear_space": "height of the x in the wordmark",
    "min_size_px": 24, "min_size_mm": 10
  }
}
```

### `decisions.md`
- Append-only. One entry per decision: `## YYYY-MM-DD — <decision>`, then *Reason*, *Alternatives considered*,
  *Decided by*.
- Before proposing something, check it doesn't contradict a logged decision. If you think a decision should be
  revisited, say so explicitly and why; don't silently ignore it.

### `feedback.md`
- One section per round. Quote the client's words, then the designer's interpretation and the action taken.

## When to write

- After any approved choice → `decisions.md` (+ `identity.json` / `brand.md` if relevant).
- After every working session → `status.md` "Now" and "Next steps".
- After client feedback → `feedback.md`.

Tell the designer in one line what you updated.
