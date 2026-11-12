# Evaluation rubrics

Score 1–5. Every score needs a specific observation as evidence.

| Score | Meaning |
|---|---|
| 5 | Excellent — professional benchmark, nothing material to change |
| 4 | Strong — minor refinements |
| 3 | Works — clear weaknesses that will show in use |
| 2 | Weak — significant problems; needs real rework |
| 1 | Fails — doesn't do the job on this criterion |

Weights are defaults. Adjust them to the brief and say so (e.g. an app-first brand weighs Scalability higher).

---

## A. Logo

| Criterion | Weight | What to look at |
|---|---|---|
| **Concept & relevance** | 20% | Is there one clear idea? Is it appropriate to the brand's positioning and audience without being literal? Could it belong to any company in the category (bad) or only this one (good)? |
| **Distinctiveness** | 20% | Shelf test against competitors (`preview_sheet.py --compare`). Category clichés (swoosh, globe, lightbulb, leaf, house roof, generic monogram in a circle). Is it ownable and memorable after one glance? |
| **Simplicity & recall** | 15% | Could someone sketch it from memory after 5 seconds? Number of elements, unnecessary detail, competing ideas. |
| **Scalability & versatility** | 15% | Holds at 16 px and on a façade; one-colour, reversed, on photos; square and horizontal formats; embroidery/engraving if relevant. |
| **Craft** | 15% | Optical balance and alignment, consistent stroke/weight, curve quality (no kinks, clean nodes), overshoot, spacing/kerning, lockup proportions. `svg_audit.py` findings. |
| **Typography** (if any) | 10% | Type choice fits personality; custom vs off-the-shelf; letterfit; legibility; licence for logo use. |
| **Longevity** | 5% | Free of short-lived trends? Will it look dated in 5–10 years? |

## B. Visual identity system

| Criterion | Weight | What to look at |
|---|---|---|
| **Coherence** | 20% | Do logo, colour, type, imagery and layout feel like one voice? |
| **Distinctiveness** | 20% | Recognisable without the logo? Distinctive assets (colour, shape, pattern, typographic treatment)? |
| **Flexibility** | 15% | Enough range for all touchpoints (social, packaging, web, print, motion) without breaking? |
| **Colour** | 15% | Roles clear (primary/secondary/accent/neutrals); WCAG contrast for text pairs (`color_tools.py contrast`); colour-blind safety (`cvd`); print reproducibility. |
| **Typography** | 15% | Hierarchy, pairing, range of weights, web/print availability, language support (accents, other scripts if needed), licence. |
| **Usability for others** | 15% | Can a non-designer apply it correctly from the guidelines? Templates, clear rules, do/don't. |

## C. Brand copy

| Criterion | Weight | What to look at |
|---|---|---|
| **Clarity** | 25% | Does a newcomer understand what this is and why it matters within 5 seconds? |
| **Voice consistency** | 20% | Matches `brand.md` → Voice? Consistent across pieces? |
| **Distinctiveness** | 20% | Could a competitor sign this copy? (If yes, it's generic.) |
| **Audience fit** | 15% | Speaks to the audience's real need, in their words? |
| **Persuasion & proof** | 10% | Concrete benefits, proof points, no unsupported claims. |
| **Craft** | 10% | Rhythm, concision, no clichés or filler, correct grammar and spelling in the target language. |

Also flag: claims that may need legal substantiation ("the best", "#1", health/financial claims).

## D. Touchpoint consistency audit

For each touchpoint (site, social profiles, packaging, decks, signage, email…), record:

| Touchpoint | Logo use | Colour | Type | Imagery | Voice | Issues |
|---|---|---|---|---|---|---|
| Website | ✅ / ⚠️ / ❌ | … | … | … | … | … |

Then score overall **Consistency** 1–5 and list the fixes by impact (most-seen touchpoints first).

## E. Strategy & positioning (when evaluating a brief or brand strategy)

| Criterion | Weight | What to look at |
|---|---|---|
| **Focus** | 25% | Clear audience and a single sharp benefit, not a list |
| **Difference** | 25% | Real and relevant difference vs alternatives |
| **Credibility** | 20% | Reasons to believe exist and are true |
| **Usefulness** | 15% | Does it guide design and copy decisions in practice? |
| **Expression potential** | 15% | Does it give the designer something to make visible? |

## Overall score

Weighted average, one decimal. Never let the number replace the written verdict: the verdict and the priority issues
are what the designer acts on.
