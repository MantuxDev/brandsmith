#!/usr/bin/env python3
"""Create the .brand/ project memory and the standard project folders.

Usage:
  python3 brand_init.py <project-dir> --name "Brand Name"
  python3 brand_init.py <project-dir> --name "Brand" --no-folders   # only .brand/

Existing files are never overwritten (use --force to overwrite .brand/ templates).
"""
import argparse
import datetime
import pathlib
import sys

TEMPLATES = pathlib.Path(__file__).resolve().parent.parent / "templates"
MEMORY_FILES = ["status.md", "brand.md", "decisions.md", "feedback.md", "identity.json"]
FOLDERS = ["research", "concepts", "copy", "exports", "guidelines"]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("project_dir", type=pathlib.Path)
    ap.add_argument("--name", required=True, help="Brand or project name")
    ap.add_argument("--no-folders", action="store_true", help="Do not create research/, concepts/, … folders")
    ap.add_argument("--force", action="store_true", help="Overwrite existing .brand/ files")
    args = ap.parse_args()

    root = args.project_dir.expanduser().resolve()
    mem = root / ".brand"
    mem.mkdir(parents=True, exist_ok=True)
    today = datetime.date.today().isoformat()
    name_json_safe = args.name.replace("\\", "\\\\").replace('"', '\\"')

    for fname in MEMORY_FILES:
        src = TEMPLATES / fname
        dst = mem / fname
        if dst.exists() and not args.force:
            print(f"skip   {dst} (exists)")
            continue
        text = src.read_text(encoding="utf-8")
        name = name_json_safe if fname.endswith(".json") else args.name
        text = text.replace("{{NAME}}", name).replace("{{DATE}}", today)
        dst.write_text(text, encoding="utf-8")
        print(f"create {dst}")

    if not args.no_folders:
        for d in FOLDERS:
            p = root / d
            if not p.exists():
                p.mkdir(parents=True)
                print(f"create {p}/")

    print(f"\n.brand/ ready in {root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
