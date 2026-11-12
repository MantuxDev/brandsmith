# Brandsmith

**English** · [Italiano](README.it.md)

**A studio partner for professional brand designers.** Brandsmith is an open-source agent skill for Claude, plus
Logo Lab, a free logo stress test that runs in your browser, in Figma and in Illustrator. It takes the tedious,
checkable parts of identity work off your plate (logo tests, accessibility, exports, tokens, guidelines,
critique) and, only when you ask, helps with strategy, concepts and copy.

**Try Logo Lab in your browser:** https://mantuxdev.github.io/brandsmith/ (nothing is uploaded)

> **It supports designers. It does not replace them.**
> Brandsmith is built for people who already do this job: brand designers, identity studios, art directors.
> It doesn't design for you and it doesn't decide for you. It measures, checks, documents and proposes;
> the ideas, the drawing, the judgement and the relationship with the client stay with you.
> It is not a tool for producing a brand without a designer.

## Four ways to use it

| | What you get | What you need |
|---|---|---|
| **Logo Lab in the browser** | The full logo stress test, a minimum size and PDF reports | Nothing: open `docs/index.html` and drop your logo. No install, no account, no AI, nothing uploaded |
| **Logo Lab for Figma** | The same Lab on the layer you select | Figma desktop: *Plugins → Development → Import plugin from manifest* → `figma-plugin/manifest.json` |
| **Logo Lab for Illustrator** | The same Lab on your selection, opened in the browser | Illustrator: *File → Scripts → Other Script…* → `illustrator/LogoLab.jsx` |
| **Brandsmith skill for Claude** | Critique, project memory, strategy, copy, guidelines, plus the Lab | A Claude plan with skills and code execution (see *Install*) |

## Logo Lab (no AI, nothing uploaded)

Drop an SVG or PNG on the page, paste it from Figma or Illustrator (Ctrl+V), or select a layer in Figma.
Everything runs on your computer and takes a few seconds.

- **Verdict first:** a score out of 10 and the **minimum size** at which the mark holds, with the reason in plain
  words, and a short "To check" list that links to each test that needs attention.
- **The measurements behind it:** thinnest stroke, narrowest gap, fidelity at 16 and 32 px, parts that merge or
  split, fill ratio, symmetry, negative space. Two-tone marks are measured on the silhouette and on the internal
  shapes.
- **More than 20 tests in five sections.** *Size & legibility:* scale from 128 to 16 px, real pixels, blur.
  *Form:* negative space, visual weight, clear space, app-icon grid, curvature and anchor points (SVG).
  *In context:* favicon in browser tabs, type lockups, business card and badge, photography, billboard, pattern,
  watermark. *Reproduction:* one colour and reversed, materials, emboss and deboss, halftone, embroidery.
  *File & export:* SVG source check and a PNG kit (16–1024 px, apple-touch-icon, 192, 512).
- **Every flagged test says what happens and how to fix it.** Sections where everything passes stay folded.
- **Two PDF reports**, from the *Export report* panel:
  - *For me / the studio* (4 A4 pages): verdict and metrics, size and legibility, form and context,
    reproduction, and next steps drawn from the warnings. See `docs/sample-report.pdf`.
  - *For the client* (2 pages): no score and no jargon. The mark, which version to use from which size, where
    it will live, what to avoid, and your studio's note.
- Italian and English, light and dark theme, works on a phone.

The score is a measurement, not a matter of taste. The thinnest stroke and the narrowest gap are measured
(within ±0.5 px on synthetic marks) and converted into the smallest size at which both stay at least 1 px.
It was calibrated on a few hundred real marks (`skills/brandsmith/references/logo-lab-calibration.md`).
It flags reproduction risks. **It does not judge the idea, and a high score does not make a good logo.**
That judgement is yours.

## The skill: three modes

| Mode | When | What it does |
|---|---|---|
| **Evaluate** | Your work, a colleague's, a client's, a competitor's | Critique on explicit rubrics (logo, identity system, copy, consistency, strategy): main issues by priority, concrete fixes, what to keep. Every point refers to something you can check. Optional client-friendly version |
| **Continue** | Picking up work in progress | Reads your files, guidelines, site or deck, rebuilds the project memory, lists the gaps and carries on from the right phase |
| **Create** | When you want a sparring partner | Brief → research → strategy → naming → directions → logo → identity → copy → applications → guidelines → handoff, stopping at every step for your decision |

**Checks-only mode:** say "just check, don't generate" and it never proposes concepts, names or copy.
Concepts it does sketch are starting points for you to redraw, and it says so.

Every project gets a `.brand/` folder (`status.md`, `brand.md`, `identity.json`, `decisions.md`, `feedback.md`),
so work resumes across sessions and can be handed to a colleague. Your decisions are logged and respected.

## Tools included

Python 3 scripts with no dependencies. They run locally and use no AI.

| Script | What it does |
|---|---|
| `logo_lab.py` | Builds the Logo Lab page for a given logo, brand name and colour |
| `lab_metrics.py` | Reads the Lab's score and minimum size from the command line (headless Firefox) |
| `svg_audit.py` | Technical audit of SVG masters: live text, embedded images, effects, colours, strokes, near-miss angles, details lost at 16/32 px, centring, painted knock-outs, editor leftovers |
| `preview_sheet.py` | Static test sheet and **shelf test** against competitor marks |
| `color_tools.py` | HEX/RGB/HSL/OKLCH/CMYK (approx.), WCAG contrast matrix, colour-blindness simulation, OKLCH scales, swatches |
| `tokens.py` | Design tokens from `identity.json`: W3C DTCG JSON, CSS variables, SCSS, Tailwind |
| `export_variants.py` | SVG kit from a master: colour, one colour, reversed, favicon set |
| `brand_init.py` | Creates the `.brand/` memory and project folders |

## Install

**Claude app (no terminal).** Download `brandsmith-skill.zip` from *Releases*. In Claude, open the Skills
settings (*Settings → Capabilities*, or *Customize → Skills* in newer versions), choose **Upload skill** and pick
the ZIP. Turn the skill on, and make sure code execution is enabled. Custom skills need a plan that supports them:
check Anthropic's help centre for current availability.

**Claude Code.**
```bash
npx skills add MantuxDev/brandsmith
```
or copy `skills/brandsmith/` into `~/.claude/skills/`.

**A whole studio.** Put the skill in your shared project repository under `.claude/skills/brandsmith/`. On Team
and Enterprise plans, a skill uploaded by one person is private until it is shared with the organisation.

## Use

Talk to it as you would to a colleague. It answers in your language.

- "Check this logo before tomorrow's presentation. Just the checks." *(in Figma: right-click → Copy as SVG, then paste)*
- "Critique round 2. It's for a specialty coffee roaster; the favicon matters a lot."
- "Here's the client's current site and old guidelines PDF: reconstruct the brand and tell me what's missing."
- "Pick up the Lumen project where we left off."
- "Check my palette for accessibility and give the developers tokens."

## FAQ

**Will it replace designers?** No. It is made for designers and keeps every decision with you: it measures and
documents, you design and decide. Use it as you would a careful assistant or a second pair of eyes, not as a
substitute for professional work.

**Which Claude plan do I need?** Logo Lab and the scripts need nothing: no account, no AI. The skill runs inside
Claude (the Claude apps on plans with custom skills, or Claude Code). Brandsmith is free; your Claude usage is
billed by your plan as usual.

**My client work is under NDA.** Logo Lab and every script run on your machine and send nothing anywhere.
Whatever you paste into a Claude conversation is processed by Anthropic under your plan's terms: check them, use a
business plan if your contracts require it, and anonymise briefs. The skill reminds you of this when you mention
confidentiality.

**Is the critique generic?** It's instructed not to be: every finding must point at an element, a size or a value
you can check. If it isn't specific enough, open an issue with the example. That is the most useful bug report.

**Who maintains it?** See `CHANGELOG.md` and `ROADMAP.md`. Issues and pull requests are welcome, especially from
working designers.

## What it won't do

- Replace the designer's work, taste or responsibility towards the client.
- Replace trademark searches, legal advice, font-licence checks, print proofs or user research. It tells you when
  you need them.
- Copy or closely imitate existing logos or another studio's work.
- Produce final print files (CMYK/Pantone PDFs). Those come from your vector tool.

## Repository layout

```
skills/brandsmith/
├── SKILL.md            entry point: role, modes, routing, working conventions
├── references/         one file per mode and per module, loaded only when needed
├── templates/          .brand/ memory templates + logo-lab.html (Logo Lab source)
└── scripts/            Python tools, no dependencies
docs/                   Logo Lab page (generated), sample report, brand mark
figma-plugin/           Logo Lab for Figma (generated) + Community listing kit
illustrator/            Logo Lab for Illustrator (generated)
tools/                  build scripts, calibration, UI smoke test
evals/                  test prompts used to measure and improve the skill
examples/               a fictional project midway through, to try Continue mode
PUBLISHING.md           how to publish the project
TESTING.md              how to test the skill on real projects
```

## License

MIT. See `LICENSE`.
