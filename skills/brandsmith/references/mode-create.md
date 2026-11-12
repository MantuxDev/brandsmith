# Mode: Create

For a new identity, or a new piece of an existing one (a sub-brand, a tagline, a refreshed palette).

## Principle

The designer leads; you accelerate. At each phase you produce material the designer can **react to** (options,
drafts, test sheets) and you stop at checkpoints for their call. Never run the whole pipeline unattended unless the
designer explicitly asks ("go all the way, I'll review at the end").

## Entry: find the starting phase

Read `.brand/status.md`. If there's no memory, ask what already exists. Designers rarely start from zero: there may
be a brief from the client, a name already chosen, a strategy from an agency. Start at the first phase that isn't
done, and record the starting point in `status.md`.

**Fast track.** If the designer wants speed ("give me directions for a coffee roaster by tonight"), ask at most
five questions in one message — or none: state your assumptions in a short list, tag them `(assumption)` in
`brand.md`, and go. They can correct you after seeing work.

## Phases and checkpoints

| # | Phase | Module | Output | Checkpoint (stop and ask) |
|---|---|---|---|---|
| 1 | Discovery | `discovery.md` | Brief in `brand.md` | Brief confirmed |
| 2 | Research | `research.md` | `research/competitor-audit.md`, conventions map, white space | White space agreed |
| 3 | Strategy | `strategy.md` | Positioning, personality, messaging in `brand.md` | Strategy approved |
| 4 | Naming (if needed) | `naming.md` | Shortlist with screening | Name chosen (and checks owned by a human) |
| 5 | Directions | `research.md` §Directions | 2–3 visual directions (moodboard + words) | One direction picked |
| 6 | Logo | `logo.md` | Concepts + test sheet | Concept picked |
| 7 | Visual identity | `visual-identity.md` | Palette, type, system → `identity.json` | System approved |
| 8 | Copy | `copywriting.md` | Voice guide, tagline, core copy in `copy/` | Voice approved |
| 9 | Applications | `applications.md` | Key touchpoints mocked | Applications approved |
| 10 | Guidelines & handoff | `guidelines-handoff.md` | Brand book, asset kit, tokens | Delivered |

Phases 6–8 often overlap; that's fine. Copy can start right after strategy.

## At each checkpoint

1. Show the work as files (paths) plus a short summary: one line per option, your recommendation, why.
2. Ask for the decision in one clear question.
3. When the designer decides: log it in `decisions.md`, update `brand.md`/`identity.json`, set the phase to
   `approved` in `status.md`, move on.
4. If the designer wants changes, iterate in a new round folder (`concepts/round-2/`); never overwrite round 1.

## Self-check before showing anything

Run the relevant evaluation on your own work first (`mode-evaluate.md`, quick depth). Fix what you can, and
mention honestly what's still weak. A designer will spot it anyway; better that you said it first.
