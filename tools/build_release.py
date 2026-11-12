#!/usr/bin/env python3
"""Build release artefacts.

  dist/brandsmith-skill.zip   the skill folder, ready to upload as a custom skill in the Claude app
  docs/index.html             the standalone Logo Lab (drag & drop), ready for GitHub Pages

Usage: python3 tools/build_release.py
"""
import pathlib
import shutil
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "brandsmith"


def main():
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    zpath = dist / "brandsmith-skill.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(SKILL.rglob("*")):
            if f.is_file() and "__pycache__" not in f.parts and not f.name.endswith(".pyc"):
                z.write(f, pathlib.Path("brandsmith") / f.relative_to(SKILL))
    print(f"Wrote {zpath}")
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)
    # the published page makes no network requests at all: drop the web-font links (the CSS has full fallback stacks)
    page = (SKILL / "templates" / "logo-lab.html").read_text(encoding="utf-8")
    page = "\n".join(l for l in page.splitlines() if "fonts.googleapis.com" not in l)
    (docs / "index.html").write_text(page, encoding="utf-8")
    print(f"Wrote {docs / 'index.html'}")


if __name__ == "__main__":
    main()
