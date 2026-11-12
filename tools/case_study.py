#!/usr/bin/env python3
"""Real-world case studies: scaffold, then aggregate the reviews into metrics.

  new ID [--root test-projects/cases]     create a case folder from evals/case-template/
  report [--root test-projects/cases]     aggregate every review.md: issue recall, precision, scores

Case folders live in test-projects/ (git-ignored): real client work never enters the repository.
Workflow per case (see TESTING.md):
  1. designer fills brief.md and designer-verdict.md and puts files in input/  (verdict BEFORE the skill runs)
  2. run the skill on input/ with the brief; save its output in skill-output/
  3. fill review.md comparing the two; then `report`
"""
import argparse
import pathlib
import re
import shutil
import statistics

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "evals" / "case-template"
SCORE_KEYS = ["accuracy", "usefulness_of_fixes", "specificity", "tone_peer_not_teacher", "respected_decisions",
              "honesty_about_limits", "min_size_agreement"]


def new(case_id, root):
    d = root / case_id
    if d.exists():
        raise SystemExit(f"{d} already exists")
    (d / "input").mkdir(parents=True)
    (d / "skill-output").mkdir()
    for f in TEMPLATE.glob("*.md"):
        (d / f.name).write_text(f.read_text(encoding="utf-8").replace("{{ID}}", case_id), encoding="utf-8")
    print(f"Created {d}\n  1. fill brief.md and designer-verdict.md (before running the skill)\n  2. put files in input/")


def table_rows(text, header_start):
    i = text.find(header_start)
    if i < 0:
        return []
    rows = []
    for line in text[i:].splitlines()[2:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip("|").split("|")]
        if any(cells):
            rows.append(cells)
    return rows


def report(root):
    cases = sorted(p for p in root.glob("*/review.md"))
    if not cases:
        print(f"No reviews found under {root}")
        return
    found = partly = missed = 0
    valid = new_ins = false = taste = 0
    scores = {k: [] for k in SCORE_KEYS}
    for rv in cases:
        t = rv.read_text(encoding="utf-8")
        for r in table_rows(t, "| Designer issue #"):
            v = (r[1] if len(r) > 1 else "").lower()
            found += v.startswith("yes"); partly += v.startswith("partly"); missed += v.startswith("no")
        for r in table_rows(t, "| Skill issue"):
            v = (r[1] if len(r) > 1 else "").lower()
            valid += v.startswith("valid"); new_ins += v.startswith("new"); false += v.startswith("false"); taste += v.startswith("taste")
        for k in SCORE_KEYS:
            m = re.search(rf"^- {k}:\s*([1-5](?:\.\d)?)", t, re.M)
            if m:
                scores[k].append(float(m.group(1)))
    total_designer = found + partly + missed
    total_skill_extra = valid + new_ins + false + taste
    print(f"Cases reviewed: {len(cases)}")
    if total_designer:
        print(f"Issue recall: {(found + .5 * partly) / total_designer:.0%}  (found {found}, partly {partly}, missed {missed})")
    if total_skill_extra:
        print(f"Extra skill issues: {total_skill_extra}  → valid {valid}, new insight {new_ins}, false alarm {false}, taste {taste}")
        print(f"False-alarm rate among extra issues: {false / total_skill_extra:.0%}")
    for k, v in scores.items():
        if v:
            print(f"  {k:24} mean {statistics.mean(v):.1f}  (n={len(v)})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new"); p.add_argument("id"); p.add_argument("--root", type=pathlib.Path, default=ROOT / "test-projects" / "cases")
    p = sub.add_parser("report"); p.add_argument("--root", type=pathlib.Path, default=ROOT / "test-projects" / "cases")
    a = ap.parse_args()
    new(a.id, a.root) if a.cmd == "new" else report(a.root)


if __name__ == "__main__":
    main()
