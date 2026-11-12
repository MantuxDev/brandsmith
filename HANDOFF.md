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

## 2. Installation instructions to verify before publishing

The README states, without verification against current docs:
- Custom skills can be uploaded as a ZIP in the Claude app (Settings → Capabilities → Skills) on plans with
  skills and code execution enabled.
- Team/Enterprise plans can add organisation-wide skills via an admin.
- `npx skills add <github-user>/brandsmith` installs it (replace `<github-user>`).

**To do:** check each statement against Anthropic's current help centre and the skills CLI docs, test the ZIP
from `tools/build_release.py` with a real upload, and fix the README wording. Also fill `[AUTHOR NAME]` in
`LICENSE`.

## 3. Logo Lab: report isolated specks in the Lab itself

The score ignores parts under ~0.4% of the ink by design (see `references/logo-lab-calibration.md`); today only
`svg_audit.py` reports them. Add a "small details" line to the Lab (count, and the size below which they vanish)
so the page and the audit never seem to disagree. Engine code: `featureSizes()` / `measure()` in
`templates/logo-lab.html`. Deferred on 2026-11-12 while the Lab UI is being redesigned.
