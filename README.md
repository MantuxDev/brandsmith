# Brandsmith

**A studio partner for professional brand designers.** An open-source agent skill for Claude that takes the
tedious, checkable parts of identity work off your plate — logo stress tests, accessibility, exports, tokens,
guidelines, critique — and, only when you ask, helps with strategy, concepts and copy.

> Built for people who already do this job: brand designers, identity studios, art directors.
> It doesn't design for you and it doesn't decide for you. It checks, documents and proposes; you judge.

## Three ways to use it

| | What you get | Needs |
|---|---|---|
| **Logo Lab in the browser** | The full logo stress test and a PDF report | Nothing: open one HTML file (`docs/index.html`) and drop your logo. No install, no account, no AI, nothing uploaded |
| **Logo Lab for Figma** | The same Lab on the layer you select | Figma desktop: *Plugins → Development → Import plugin from manifest* (`figma-plugin/manifest.json`). No terminal |
| **Logo Lab for Illustrator** | The same Lab on your selection, opened in the browser | Illustrator: *File → Scripts → Other Script…* → `illustrator/LogoLab.jsx`. No terminal |
| **Brandsmith skill for Claude** | Critique, project memory, strategy, copy, guidelines, plus the Lab | A Claude plan with skills; upload the ZIP in the Claude app or install in Claude Code |

## The Logo Lab (no AI, nothing uploaded)

Drop an SVG or PNG on the page, or select a layer in Figma. Everything runs locally:

- **Score /10 and recommended minimum size**, with the metrics behind it: thin-stroke risk, edge complexity,
  fidelity at 16 and 32 px, shape stability (parts merging or splitting), fill ratio, symmetry, negative space.
  Two-tone marks are measured on both the silhouette and the internal shapes.
- **Size & legibility:** scale ladder (light/dark), real 16/32/48 px pixels, vision-blur slider.
- **Form:** negative-space map, visual-weight heat map with centre of mass, clear-space overlay, app-icon keyline
  grid; for SVG, curvature combs (kinks flagged) and anchor points/handles.
- **Context:** favicon in browser tabs, type lockups in six directions, business card and badge, photography,
  billboard, pattern/brand wall, watermark.
- **Reproduction:** one-colour and reversed, paper/kraft/concrete/chalk/metal, emboss/deboss, halftone,
  embroidered patch.
- **Report:** one-click **PDF** (A4, verdict first, then every test with notes), with your studio's name and a note for the client. A **client version** hides the score and the technical tests and leads with the minimum size. See `docs/sample-report.pdf`. Plus a PNG kit (16–1024 px, apple-touch-icon, 192, 512).

The score is grounded in measurement, not taste: the thinnest stroke and the narrowest gap are measured
(validated within ±0.5 px on synthetic marks) and converted into the smallest size at which they stay ≥ 1 px.
It was calibrated on a few hundred real marks (see `skills/brandsmith/references/logo-lab-calibration.md`). It flags
reproduction risks; it doesn't judge the idea.

## The skill: three modes

| Mode | When | What it does |
|---|---|---|
| **Evaluate** | Your work, a colleague's, a client's, a competitor's | Evidence-based critique on explicit rubrics (logo, identity system, copy, consistency, strategy): top issues by priority, concrete fixes, what to keep — every point tied to something you can check. Optional client-friendly version |
| **Continue** | Picking up work in progress | Reads your files, guidelines, site or deck, rebuilds the project memory, lists the gaps, carries on from the right phase |
| **Create** | When you want a sparring partner | Brief → research → strategy → naming → directions → logo → identity → copy → applications → guidelines → handoff, stopping at every checkpoint for your decision |

**Checks-only mode:** say "just check, don't generate" and it never proposes concepts, names or copy.
Concepts it does sketch are starting points for you to redraw, and it says so.

Every project gets a `.brand/` folder (`status.md`, `brand.md`, `identity.json`, `decisions.md`, `feedback.md`),
so work resumes across sessions and can be handed to a colleague. Your decisions are logged and respected.

## Tools included

Dependency-free Python 3 scripts (they run locally and use no AI tokens):

| Script | What it does |
|---|---|
| `logo_lab.py` | Builds the Logo Lab page for a given logo, brand name and colour |
| `svg_audit.py` | Technical audit of SVG masters: live text, rasters, effects, colours, strokes, near-miss angles, details lost at 16/32 px, centring, complexity, editor leftovers |
| `preview_sheet.py` | Static test sheet and **shelf test** against competitor marks |
| `color_tools.py` | HEX/RGB/HSL/OKLCH/CMYK (approx.), WCAG contrast matrix, colour-blindness simulation, OKLCH tint/shade scales, swatches |
| `tokens.py` | Design tokens from `identity.json`: W3C DTCG JSON, CSS variables, SCSS, Tailwind |
| `export_variants.py` | SVG kit from a master: colour / one-colour / reversed, favicon set (PNG when a rasteriser is installed) |
| `brand_init.py` | Creates the `.brand/` memory and project folders |

## Install

**Claude app (no terminal).** Download `brandsmith-skill.zip` from *Releases* and upload it as a custom skill in
the Claude app settings (Capabilities → Skills). Custom skills need a plan with skills and code execution
enabled; check Anthropic's help centre for current availability.

**Claude Code.**
```bash
npx skills add <github-user>/brandsmith
```
or copy `skills/brandsmith/` into `~/.claude/skills/`.

**A whole studio.** Put the skill in your shared project repository under `.claude/skills/brandsmith/`, or, on
Team/Enterprise plans that support organisation skills, have an admin add it once for everyone.

## Use

Talk to it as you would to a colleague. It answers in your language.

- "Check this logo before tomorrow's presentation. Just the checks." *(paste the SVG from Figma: right-click → Copy as SVG)*
- "Critique round 2. It's for a specialty coffee roaster; the favicon matters a lot."
- "Here's the client's current site and old guidelines PDF: reconstruct the brand and tell me what's missing."
- "Pick up the Lumen project where we left off."
- "Check my palette for accessibility and give the developers tokens."

## FAQ

**Which Claude plan do I need?** The Logo Lab and the scripts need nothing: no account, no AI. The skill itself
runs inside Claude (the Claude apps on plans that support custom skills, or Claude Code). It's free; your
Claude usage is billed by your plan as usual.

**My client work is under NDA.** The Logo Lab and every script run on your machine and send nothing anywhere.
Whatever you paste into a Claude conversation is processed by Anthropic under your plan's terms: check them,
use a business plan if your contracts require it, and anonymise briefs. The skill reminds you of this when you
mention confidentiality.

**Is the critique generic?** It's instructed not to be: every finding must point at an element, a size or a value
you can check, and filler words are banned unless backed by specifics. If it isn't specific enough, open an issue
with the example. That's the most useful bug report there is.

**Will it replace designers?** No. It's for designers, and it keeps the decisions with you.

**Who maintains it?** See `CHANGELOG.md` and `ROADMAP.md`. Issues and pull requests are welcome, especially from
working designers.

## What it won't do

- Replace trademark searches, legal advice, font-licence checks, print proofs or user research. It tells you when
  you need them.
- Copy or closely imitate existing logos or another studio's work.
- Produce final print files (CMYK/Pantone PDFs). Those come from your vector tool.

## Repository layout

```
skills/brandsmith/
├── SKILL.md            entry point: role, modes, routing, working conventions
├── references/         one file per mode and per module, loaded only when needed
├── templates/          .brand/ memory templates + logo-lab.html (standalone Logo Lab)
└── scripts/            dependency-free Python tools
tools/build_release.py  builds the uploadable skill ZIP and the hostable Logo Lab page
evals/                  test prompts used to measure and improve the skill
examples/               a fictional project mid-way through, to try Continue mode
TESTING.md              how to test the skill on real projects
```

## License

MIT. See `LICENSE`.
