# Handoff — open items

Items deliberately left open. Each has the context needed to pick it up cold.

## 1. Figma plugin (MVP built, not yet tested inside Figma)

`tools/build_figma_plugin.py` builds `figma-plugin/` (manifest, `code.js`, `ui.html` generated from the Logo Lab
template). The UI was tested in Firefox by simulating Figma's messages (selection → SVG bytes → full report);
it has **not** been run inside the Figma app yet.

**To do:** import it in Figma desktop (Plugins → Development → Import plugin from manifest), test on frames,
groups, components and text layers; check that the PDF and PNG downloads work inside the plugin iframe (if not,
send the files back to `code.js` and save them with `figma.ui`/clipboard alternatives); then publish to Figma
Community (needs the author's Figma account).

## 2. Installation instructions: partly verified (2026-11-12)

Checked against Anthropic's help centre and the skills CLI docs:
- Custom skills are uploaded as a ZIP with the skill folder at the top level (our ZIP: `brandsmith/SKILL.md`, OK)
  and need code execution enabled. The menu path differs between help-centre pages (*Settings → Capabilities*
  or *Customize → Skills*); both READMEs now mention both.
- On Team/Enterprise, a skill uploaded by one person is private until shared with the organisation.
- `npx skills add <owner>/<repo>` is the documented syntax (Vercel Labs `skills` CLI).

**Still to do:** a real upload of `dist/brandsmith-skill.zip` in the Claude app, then fix the menu wording;
Repository published at https://github.com/MantuxDev/brandsmith; `LICENSE` filled. Checklist in `PUBLISHING.md`.

## 3. Logo Lab: report isolated specks in the Lab itself

The score ignores parts under ~0.4% of the ink by design (see `references/logo-lab-calibration.md`); today only
`svg_audit.py` reports them. Add a "small details" line to the Lab (count, and the size below which they vanish)
so the page and the audit never seem to disagree. Engine code: `featureSizes()` / `measure()` in
`templates/logo-lab.html`. Deferred on 2026-11-12 while the Lab UI is being redesigned.
