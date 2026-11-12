#!/usr/bin/env python3
"""Export logo variants from a master SVG. Dependency-free for SVG; PNG needs a rasteriser.

Usage:
  python3 export_variants.py master.svg -o exports/logo --name brand_logo_primary
  python3 export_variants.py symbol.svg -o exports --name brand_symbol --favicon --dark "#14213D"

SVG outputs (always):
  <name>_color.svg           cleaned copy of the master
  <name>_one-color.svg       every fill/stroke set to --dark (default #000000)
  <name>_reversed.svg        every fill/stroke set to --light (default #FFFFFF)
With --favicon (use on the symbol, not a long wordmark):
  favicon/favicon.svg        square, padded, one colour, switches to light in dark mode
  favicon/head-snippet.html  <link> tags and a web manifest snippet

PNG outputs (when rsvg-convert, Inkscape, cairosvg or ImageMagick is available):
  png/<name>_<variant>_<w>w.png at 256/512/1024 px wide
  favicon/favicon-16/32/48.png, apple-touch-icon.png (180), icon-192.png, icon-512.png, favicon.ico (ImageMagick)

One-colour and reversed are mechanical recolours. They're a starting point: some marks need a designed
one-colour version (e.g. where two colours overlap). Always open and check every file.
"""
import argparse
import importlib.util
import pathlib
import re
import shutil
import subprocess
import sys

COLOR_ATTR = re.compile(r'\b(fill|stroke|stop-color)\s*=\s*"(?!none")(?!transparent")[^"]*"', re.I)
COLOR_CSS = re.compile(r'\b(fill|stroke|stop-color)\s*:\s*(?!none)(?!transparent)[^;}"]+', re.I)
EDITOR_JUNK = [
    re.compile(r"<!--.*?-->", re.S),
    re.compile(r"<metadata\b.*?</metadata>", re.S),
    re.compile(r"<sodipodi:namedview\b.*?(/>|</sodipodi:namedview>)", re.S),
    re.compile(r'\s(?:inkscape|sodipodi|sketch|serif):[\w-]+="[^"]*"'),
]


def clean(svg):
    for rx in EDITOR_JUNK:
        svg = rx.sub("", svg)
    return svg


def recolor(svg, color):
    svg = COLOR_ATTR.sub(lambda m: f'{m.group(1)}="{color}"', svg)
    svg = COLOR_CSS.sub(lambda m: f"{m.group(1)}:{color}", svg)
    # elements with no fill attribute default to black: force the colour on the root
    svg = re.sub(r"<svg\b", f'<svg fill="{color}"', svg, count=1) if not re.search(r"<svg\b[^>]*\bfill=", svg) else svg
    return svg


def viewbox(svg):
    m = re.search(r'viewBox\s*=\s*"([^"]+)"', svg)
    if not m:
        w = re.search(r'<svg\b[^>]*\bwidth="([\d.]+)', svg)
        h = re.search(r'<svg\b[^>]*\bheight="([\d.]+)', svg)
        if w and h:
            return 0.0, 0.0, float(w.group(1)), float(h.group(1))
        raise SystemExit("Master SVG needs a viewBox (or numeric width/height).")
    v = [float(x) for x in re.split(r"[\s,]+", m.group(1).strip())]
    return tuple(v)


def square_favicon(svg_one_color, pad=0.08):
    x, y, w, h = viewbox(svg_one_color)
    side = max(w, h) * (1 + 2 * pad)
    nx, ny = x - (side - w) / 2, y - (side - h) / 2
    inner = re.sub(r"^.*?<svg\b[^>]*>", "", svg_one_color, count=1, flags=re.S)
    inner = re.sub(r"</svg>\s*$", "", inner.strip())
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{nx:g} {ny:g} {side:g} {side:g}">'
            '<style>@media (prefers-color-scheme: dark){*{fill:#FFFFFF}}</style>'
            f'<g>{inner}</g></svg>\n')


def find_rasteriser():
    if shutil.which("rsvg-convert"):
        return "rsvg"
    if shutil.which("inkscape"):
        return "inkscape"
    if importlib.util.find_spec("cairosvg"):
        return "cairosvg"
    if shutil.which("magick"):
        return "magick"
    return None


def rasterise(tool, src, dst, width):
    dst.parent.mkdir(parents=True, exist_ok=True)
    if tool == "rsvg":
        cmd = ["rsvg-convert", "-w", str(width), "-o", str(dst), str(src)]
    elif tool == "inkscape":
        cmd = ["inkscape", str(src), "--export-type=png", f"--export-filename={dst}", f"--export-width={width}"]
    elif tool == "magick":
        cmd = ["magick", "-background", "none", "-density", "600", str(src), "-resize", f"{width}x", str(dst)]
    else:
        import cairosvg  # noqa: PLC0415
        cairosvg.svg2png(url=str(src), write_to=str(dst), output_width=width)
        return True
    return subprocess.run(cmd, capture_output=True).returncode == 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("master")
    ap.add_argument("-o", "--out", default="exports/logo")
    ap.add_argument("--name", help="File name stem, e.g. brand_logo_horizontal (default: master file stem)")
    ap.add_argument("--dark", default="#000000", help="Colour for the one-colour version")
    ap.add_argument("--light", default="#FFFFFF", help="Colour for the reversed version")
    ap.add_argument("--favicon", action="store_true", help="Also build favicon set from this (square-ish) mark")
    ap.add_argument("--no-png", action="store_true")
    args = ap.parse_args()

    src = pathlib.Path(args.master)
    svg = clean(src.read_text(encoding="utf-8"))
    name = args.name or src.stem
    out = pathlib.Path(args.out)
    svg_dir = out / "svg"
    svg_dir.mkdir(parents=True, exist_ok=True)

    variants = {
        "color": svg,
        "one-color": recolor(svg, args.dark),
        "reversed": recolor(svg, args.light),
    }
    distinct = {c.upper() for c in re.findall(r'(?:fill|stroke|stop-color)\s*[=:]\s*"?\s*(#[0-9A-Fa-f]{3,6})', svg)}
    if len(distinct) > 1:
        print(f"WARNING: the master uses {len(distinct)} colours ({', '.join(sorted(distinct))}); the one-colour and "
              "reversed versions merge them into one. Shapes that sit on top of other shapes will disappear into "
              "them. If the mark relies on overlaps, draw a dedicated one-colour version with knock-outs.\n")
    written = {}
    for v, content in variants.items():
        p = svg_dir / f"{name}_{v}.svg"
        p.write_text(content, encoding="utf-8")
        written[v] = p
        print(f"Wrote {p}")

    fav_svg = None
    if args.favicon:
        fdir = out / "favicon"
        fdir.mkdir(parents=True, exist_ok=True)
        fav_svg = fdir / "favicon.svg"
        fav_svg.write_text(square_favicon(variants["one-color"]), encoding="utf-8")
        print(f"Wrote {fav_svg}")
        (fdir / "head-snippet.html").write_text(
            '<link rel="icon" href="/favicon.ico" sizes="48x48">\n'
            '<link rel="icon" href="/favicon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n'
            '<link rel="manifest" href="/site.webmanifest">\n\n'
            '<!-- site.webmanifest -->\n'
            '<!-- {"icons":[{"src":"/icon-192.png","type":"image/png","sizes":"192x192"},'
            '{"src":"/icon-512.png","type":"image/png","sizes":"512x512"}]} -->\n', encoding="utf-8")
        print(f"Wrote {fdir / 'head-snippet.html'}")

    if args.no_png:
        return 0
    tool = find_rasteriser()
    if not tool:
        print("\nNo rasteriser found (rsvg-convert, inkscape, cairosvg or ImageMagick). SVGs written; for PNGs install "
              "one (e.g. `apt install librsvg2-bin`, `brew install librsvg`, `pip install cairosvg`) or export from "
              "your design tool.")
        return 0
    print(f"\nRasterising with {tool}")
    for v, p in written.items():
        for w in (256, 512, 1024):
            dst = out / "png" / f"{name}_{v}_{w}w.png"
            if rasterise(tool, p, dst, w):
                print(f"Wrote {dst}")
    if fav_svg:
        fdir = fav_svg.parent
        # PNG icons from the colour version, squared
        sq_color = fdir / "_square_color.svg"
        sq_color.write_text(square_favicon(variants["color"]).replace(
            "<style>@media (prefers-color-scheme: dark){*{fill:#FFFFFF}}</style>", ""), encoding="utf-8")
        for fname, size in (("favicon-16.png", 16), ("favicon-32.png", 32), ("favicon-48.png", 48),
                            ("apple-touch-icon.png", 180), ("icon-192.png", 192), ("icon-512.png", 512)):
            if rasterise(tool, sq_color, fdir / fname, size):
                print(f"Wrote {fdir / fname}")
        if shutil.which("magick"):
            ico = fdir / "favicon.ico"
            subprocess.run(["magick", str(fdir / "favicon-16.png"), str(fdir / "favicon-32.png"),
                            str(fdir / "favicon-48.png"), str(ico)], capture_output=True)
            if ico.exists():
                print(f"Wrote {ico}")
        sq_color.unlink(missing_ok=True)
        print("Note: apple-touch-icon usually needs a solid background — check it on a home screen.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
