# Testing Brandsmith on real projects

A skill isn't "trained" like a model: it improves by running it on real work, seeing where it falls short of what
a senior designer would do, and rewriting the instructions. This file is the loop.

## 0. Blind case studies (the main training loop)

```bash
python3 tools/case_study.py new 2026-11-coffee-roaster     # creates test-projects/cases/<id>/ (git-ignored)
```
1. The designer fills `brief.md` and **`designer-verdict.md` before the skill runs**: their own issues, severity,
   strengths, the minimum size they'd use. This is the ground truth; writing it afterwards contaminates it.
2. Run the skill on `input/` with the brief. Save the critique and the Logo Lab page in `skill-output/`.
3. Fill `review.md`: which designer issues the skill found, which extra issues were valid, new insights,
   false alarms or taste; scores 1–5; what a senior would have said; the file to change.
4. `python3 tools/case_study.py report` aggregates all cases: **issue recall**, **false-alarm rate**, mean scores.
5. Change the instructions (not the example), re-run the affected cases, and check the numbers move.

Targets for a first public release: recall ≥ 70%, false-alarm rate ≤ 15%, specificity and tone ≥ 4/5,
Logo Lab minimum size within one step of the designer's in ≥ 80% of cases.

## 1. Set up a test project

Keep real client material **out of the public repo**: put it in `test-projects/` (git-ignored) or anywhere outside
the repo. Anonymise anything you might later turn into a public example.

## 2. Run a session

Pick one scenario per session and use the skill as you would on a real job:

| Scenario | Example prompt |
|---|---|
| Evaluate a logo | "Critique this logo, final round, it's for …" + SVG |
| Evaluate an identity | "Audit this brand: here's the site and the guidelines PDF" |
| Evaluate copy | "Review this homepage copy against our voice" |
| Create from a brief | "New project: here's the brief, start discovery" |
| Continue | "Pick up this project" (folder with `.brand/`) or "Here are the files from the previous agency" |
| Handoff | "Prepare the asset kit and tokens" |

## 3. Score the session

After each session, write a short note in `evals/notes/YYYY-MM-DD-<scenario>.md`:

- **Score 1–5** on: accuracy of observations · usefulness of priorities · quality of fixes · tone (peer, not
  teacher) · respect for decisions/process · honesty about limits.
- **What it got wrong** (quote it).
- **What a senior designer would have said instead.**
- **Which file to change** (e.g. `references/logo.md` §4, `rubrics.md` criterion "Craft").

## 4. Fix the skill

Change the instructions, not just the example: if it missed overshoot on round letters, the fix goes into the
logo checklist so it never misses it again. Keep `SKILL.md` short; detail belongs in `references/`.

## 5. Re-run the evals

`evals/evals.json` holds repeatable test prompts with expected behaviours. Re-run them after significant
changes (manually, or with Anthropic's skill-creator eval tooling) and check nothing regressed.

After any change to the Logo Lab template, run `python3 tools/test_lab_ui.py` (headless Firefox + geckodriver):
it checks the interface, both PDF reports, the phone layout and that the published page makes no network requests.

## 6. Promote good cases

When a real project produced a great (or instructively bad) result, anonymise it and add it to `evals/evals.json`
as a new case, so the skill keeps being measured against real-world difficulty.
