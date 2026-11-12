#!/usr/bin/env python3
"""Build an interactive Logo Lab: a single HTML page that stress-tests a logo in the browser. Dependency-free.

Usage:
  python3 logo_lab.py mark.svg -o concepts/round-1/lab.html --name "Brand" --color "#14213D"
  python3 logo_lab.py mark.png -o lab.html            # PNG works too (transparent background preferred)

The page runs everything locally (no upload, no network) and contains:
  Score /10 with recommended minimum size and the metrics behind it:
    thin-stroke risk, edge complexity, fidelity at 16 and 32 px, shape stability (parts merging/splitting),
    fill ratio, mirror symmetry, negative space
  Scale preview (light/dark) · real-pixel 16/32/48 px · vision-blur slider · negative-space map
  visual-weight heat map with centre of mass · clear-space overlay · app-icon keyline grid
  favicon in browser tabs · typography lockups (6 type directions) · business card & ID badge
  on photography (auto light/dark version) · billboard in perspective · pattern / brand wall · watermark
  materials (paper, kraft, concrete, chalk, metal) · emboss/deboss · halftone · embroidered patch
  one-colour & reversed · SVG only: curvature combs, anchor points & handles, source view
  PNG export kit (sizes 16–1024, apple-touch-icon, 192, 512) rendered in the browser

Scores are pixel heuristics: they flag scalability and reproduction risks. They do not judge the idea.
"""
import argparse
import base64
import html
import json
import pathlib
import re
import sys

TEMPLATE = pathlib.Path(__file__).resolve().parent.parent / "templates" / "logo-lab.html"


def svg_with_size(svg: str) -> str:
    """Firefox can't draw an SVG without intrinsic size into a canvas: add width/height from the viewBox."""
    m = re.search(r"<svg\b[^>]*>", svg, re.S)
    if not m:
        return svg
    tag = m.group(0)
    has_w = re.search(r'\swidth\s*=\s*"[\d.]+(px)?"', tag)
    has_h = re.search(r'\sheight\s*=\s*"[\d.]+(px)?"', tag)
    vb = re.search(r'viewBox\s*=\s*"([^"]+)"', tag)
    if (has_w and has_h) or not vb:
        return svg
    parts = [p for p in re.split(r"[\s,]+", vb.group(1).strip()) if p]
    if len(parts) != 4:
        return svg
    w, h = float(parts[2]), float(parts[3])
    scale = 1024 / max(w, h)  # render crisp: intrinsic size ~1024 px on the long side
    new = re.sub(r'\s(width|height)\s*=\s*"[^"]*"', "", tag)
    new = new[:-1].rstrip("/") + f' width="{w * scale:g}" height="{h * scale:g}"' + ("/>" if tag.endswith("/>") else ">")
    return svg.replace(tag, new, 1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logo", help="SVG or PNG file")
    ap.add_argument("-o", "--out", default="logo-lab.html")
    ap.add_argument("--name", default="", help="Brand name for lockups and mockups")
    ap.add_argument("--color", default="#1F2937", help="Brand colour (hex) for tiles, patterns and badges")
    args = ap.parse_args()

    src = pathlib.Path(args.logo)
    if not src.is_file():
        print(f"Not found: {src}", file=sys.stderr)
        return 2
    ext = src.suffix.lower()
    svg_text = None
    if ext == ".svg":
        svg_text = src.read_text(encoding="utf-8", errors="replace")
        payload = svg_with_size(svg_text).encode("utf-8")
        mime = "image/svg+xml"
    elif ext == ".png":
        payload = src.read_bytes()
        mime = "image/png"
    else:
        print("Only SVG or PNG are supported.", file=sys.stderr)
        return 2
    if not re.fullmatch(r"#[0-9A-Fa-f]{6}", args.color):
        print("--color must be a 6-digit hex like #14213D", file=sys.stderr)
        return 2

    data = {
        "file": src.name,
        "name": args.name,
        "color": args.color,
        "uri": f"data:{mime};base64," + base64.b64encode(payload).decode(),
        "svg": svg_text,
    }
    # </script> inside the SVG source must not close the page's script tag
    blob = json.dumps(data).replace("</", "<\\/")
    page = TEMPLATE.read_text(encoding="utf-8")
    # fully offline page: drop web-font links (the CSS has system-font fallbacks), so the browser contacts no server
    page = "\n".join(l for l in page.splitlines() if "fonts.googleapis.com" not in l and "fonts.gstatic.com" not in l)
    page = page.replace("/*__DATA__*/", f"window.DATA = {blob};", 1)
    page = page.replace("<title>Logo Lab</title>", f"<title>Logo Lab — {html.escape(src.name)}</title>", 1)
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out}  (open it in a desktop browser)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
