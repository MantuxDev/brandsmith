#!/usr/bin/env python3
"""Generate an HTML test sheet for logo SVGs. Dependency-free; open the result in any browser.

Usage:
  python3 preview_sheet.py mark.svg [other.svg …] -o test-sheet.html
  python3 preview_sheet.py mark.svg --compare competitors/*.svg -o shelf.html
  python3 preview_sheet.py mark.svg --brand-color "#14213D" --name "Brand" -o sheet.html

Per logo the sheet shows:
  size ladder (512 → 16 px) · real 16/32/48 px pixel rendering, enlarged · one-colour black · reversed white
  backgrounds (white, black, brand colour, mid grey, busy pattern) · squint blur · mirror and 180° rotation
  contexts: browser tab favicon, app icon on light/dark, website header, circle avatar, business card
With several logos: a side-by-side comparison. With --compare: a shelf test against reference marks,
in colour and in greyscale, all normalised to the same height.
"""
import argparse
import base64
import html
import pathlib
import sys


def data_uri(path):
    raw = pathlib.Path(path).read_bytes()
    return "data:image/svg+xml;base64," + base64.b64encode(raw).decode()


CSS = """
:root{--ink:#111;--muted:#666;--line:#e3e3e3;--paper:#fff;--bg:#f5f5f4}
*{box-sizing:border-box} body{margin:0;font:14px/1.45 system-ui,-apple-system,Segoe UI,sans-serif;background:var(--bg);color:var(--ink)}
header.top{padding:24px 32px;background:var(--paper);border-bottom:1px solid var(--line)}
header.top h1{margin:0 0 4px;font-size:20px} header.top p{margin:0;color:var(--muted)}
main{padding:24px 32px;max-width:1280px} section{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:20px;margin:0 0 20px}
h2{font-size:16px;margin:0 0 4px} h3{font-size:12px;text-transform:uppercase;letter-spacing:.06em;color:var(--muted);margin:20px 0 10px}
.row{display:flex;flex-wrap:wrap;gap:16px;align-items:flex-end}
.cell{display:flex;flex-direction:column;align-items:center;gap:6px} .cell small{color:var(--muted);font-size:11px}
.tile{width:180px;height:140px;display:flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.tile img{max-width:70%;max-height:60%}
.mono img,.mono-black{filter:brightness(0)} .rev img{filter:brightness(0) invert(1)}
.pix canvas{image-rendering:pixelated;image-rendering:crisp-edges;border:1px solid var(--line);background:#fff}
.busy{background:repeating-linear-gradient(45deg,#c9b8a3 0 12px,#8d7b68 12px 24px),#aaa}
.photo{background:radial-gradient(circle at 30% 30%,#f2c48d,transparent 50%),radial-gradient(circle at 70% 60%,#4a6b8a,transparent 55%),linear-gradient(135deg,#d9a066,#3b4f63)}
.squint img{filter:blur(3px)} .squint.mono img{filter:brightness(0) blur(3px)}.mirror img{transform:scaleX(-1)} .rot img{transform:rotate(180deg)}
.tab{width:260px;background:#dfe1e5;border-radius:8px 8px 0 0;padding:8px 12px;display:flex;gap:8px;align-items:center;font-size:12px}
.tab img{width:16px;height:16px} .tab.dark{background:#35363a;color:#eee}
.app{width:72px;height:72px;border-radius:16px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 1px 3px rgba(0,0,0,.25)}
.app img{width:62%;height:62%;object-fit:contain} .home{padding:18px;border-radius:12px;display:flex;gap:18px}
.home.light{background:linear-gradient(160deg,#e9eef5,#c7d3e3)} .home.dark{background:linear-gradient(160deg,#1d2533,#0b0f17)}
.site{width:520px;border:1px solid var(--line);border-radius:6px;overflow:hidden} .site .bar{height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 20px;background:#fff;border-bottom:1px solid var(--line)}
.site .bar img{height:28px;max-width:180px;object-fit:contain} .site .nav{display:flex;gap:16px;color:var(--muted);font-size:12px}
.site .hero{height:110px;background:#f7f7f7}
.avatar{width:96px;height:96px;border-radius:50%;background:#fff;border:1px solid var(--line);display:flex;align-items:center;justify-content:center;overflow:hidden}
.avatar img{width:64%;height:64%;object-fit:contain}
.card{width:340px;height:220px;border-radius:6px;background:#fff;box-shadow:0 2px 8px rgba(0,0,0,.15);padding:26px;display:flex;flex-direction:column;justify-content:space-between}
.card img{height:40px;max-width:200px;object-fit:contain;object-position:left} .card p{margin:0;font-size:11px;color:#444}
.shelf{display:flex;flex-wrap:wrap;gap:12px} .shelf .tile{width:200px;height:120px} .shelf .tile img{height:48px;max-width:80%;object-fit:contain}
.shelf .ours{outline:2px solid #2563eb;outline-offset:2px} .grey img{filter:grayscale(1)}
footer{padding:0 32px 32px;color:var(--muted);font-size:12px}
"""

JS = """
document.querySelectorAll('canvas[data-src]').forEach(c=>{
  const img=new Image();
  img.onload=()=>{const s=+c.dataset.size;const x=c.getContext('2d');x.imageSmoothingEnabled=true;
    const r=Math.min(s/img.naturalWidth||1,s/img.naturalHeight||1);
    const w=(img.naturalWidth||s)*r,h=(img.naturalHeight||s)*r;x.drawImage(img,(s-w)/2,(s-h)/2,w,h);};
  img.src=c.dataset.src;
});
"""


def logo_section(path, uri, brand_color, name):
    title = html.escape(pathlib.Path(path).name)
    nm = html.escape(name or pathlib.Path(path).stem)
    sizes = [512, 256, 128, 64, 48, 32, 24, 16]
    ladder = "".join(
        f'<div class="cell"><img src="{uri}" style="width:{s}px;max-height:{s}px" alt=""><small>{s}px</small></div>'
        for s in sizes)
    pix = "".join(
        f'<div class="cell pix"><canvas width="{s}" height="{s}" data-size="{s}" data-src="{uri}" '
        f'style="width:{s * (8 if s <= 16 else 4 if s <= 32 else 3)}px"></canvas><small>{s}px, enlarged</small></div>'
        for s in (16, 32, 48))
    bgs = [("white", "#ffffff", ""), ("black", "#000000", ""), ("brand colour", brand_color, ""),
           ("mid grey", "#808080", ""), ("busy pattern", "", "busy"), ("photo-like", "", "photo")]
    bg_tiles = "".join(
        f'<div class="cell"><div class="tile {cls}" style="{f"background:{bg}" if bg else ""}"><img src="{uri}" alt=""></div>'
        f'<small>{label}</small></div>' for label, bg, cls in bgs)
    variants = (
        f'<div class="cell mono"><div class="tile" style="background:#fff"><img src="{uri}" alt=""></div><small>one colour (black)</small></div>'
        f'<div class="cell rev"><div class="tile" style="background:#111"><img src="{uri}" alt=""></div><small>reversed (white on black)</small></div>'
        f'<div class="cell rev"><div class="tile" style="background:{brand_color}"><img src="{uri}" alt=""></div><small>reversed on brand colour</small></div>'
        f'<div class="cell squint"><div class="tile" style="background:#fff"><img src="{uri}" alt=""></div><small>squint (blur)</small></div>'
        f'<div class="cell squint mono"><div class="tile" style="background:#fff"><img src="{uri}" alt=""></div><small>squint, one colour</small></div>'
        f'<div class="cell mirror"><div class="tile" style="background:#fff"><img src="{uri}" alt=""></div><small>mirrored</small></div>'
        f'<div class="cell rot"><div class="tile" style="background:#fff"><img src="{uri}" alt=""></div><small>rotated 180°</small></div>')
    contexts = f"""
      <div class="cell"><div class="tab"><img src="{uri}" alt=""><span>{nm} — Home</span></div><small>browser tab, light</small></div>
      <div class="cell"><div class="tab dark"><img src="{uri}" alt=""><span>{nm} — Home</span></div><small>browser tab, dark</small></div>
      <div class="cell"><div class="home light"><div class="app"><img src="{uri}" alt=""></div><div class="app" style="background:{brand_color}"><img src="{uri}" alt="" style="filter:brightness(0) invert(1)"></div></div><small>app icon, light home</small></div>
      <div class="cell"><div class="home dark"><div class="app"><img src="{uri}" alt=""></div><div class="app" style="background:{brand_color}"><img src="{uri}" alt="" style="filter:brightness(0) invert(1)"></div></div><small>app icon, dark home</small></div>
      <div class="cell"><div class="avatar"><img src="{uri}" alt=""></div><small>social avatar (circle crop)</small></div>
      <div class="cell"><div class="site"><div class="bar"><img src="{uri}" alt=""><div class="nav"><span>Work</span><span>About</span><span>Contact</span></div></div><div class="hero"></div></div><small>website header (28px tall)</small></div>
      <div class="cell"><div class="card"><img src="{uri}" alt=""><p><strong>Name Surname</strong><br>Role · name@example.com · +00 000 000 000</p></div><small>business card 85×55 mm (approx. scale)</small></div>
    """
    return f"""
  <section>
    <h2>{title}</h2>
    <h3>Size ladder</h3><div class="row">{ladder}</div>
    <h3>Actual pixel rendering</h3><div class="row">{pix}</div>
    <h3>Colour variants and stress tests</h3><div class="row">{variants}</div>
    <h3>Backgrounds</h3><div class="row">{bg_tiles}</div>
    <h3>Contexts</h3><div class="row">{contexts}</div>
  </section>"""


def side_by_side(items):
    cols = "".join(
        f'<div class="cell"><div class="tile"><img src="{u}" alt=""></div><small>{html.escape(pathlib.Path(p).name)}</small></div>'
        for p, u in items)
    small = "".join(
        f'<div class="cell"><img src="{u}" style="width:32px;height:32px;object-fit:contain" alt=""><small>{html.escape(pathlib.Path(p).stem)}</small></div>'
        for p, u in items)
    mono = "".join(
        f'<div class="cell mono"><div class="tile"><img src="{u}" alt=""></div><small>{html.escape(pathlib.Path(p).stem)}</small></div>'
        for p, u in items)
    return f"""<section><h2>Side by side</h2><h3>Colour</h3><div class="row">{cols}</div>
    <h3>One colour</h3><div class="row">{mono}</div><h3>32 px</h3><div class="row">{small}</div></section>"""


def shelf(ours, refs):
    def tiles(cls=""):
        t = [f'<div class="tile ours"><img src="{u}" alt=""></div>' for _, u in ours]
        t += [f'<div class="tile"><img src="{u}" alt=""></div>' for _, u in refs]
        return f'<div class="shelf {cls}">{"".join(t)}</div>'
    return f"""<section><h2>Shelf test</h2>
    <p style="color:var(--muted);margin:0">Ours outlined in blue. Does it stand out? Does it still belong to the category?
    Reference marks are for analysis only — never include them in deliverables.</p>
    <h3>Colour</h3>{tiles()}<h3>Greyscale</h3>{tiles("grey")}</section>"""


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logos", nargs="+", help="Logo SVG file(s) to test")
    ap.add_argument("--compare", nargs="*", default=[], help="Reference/competitor SVGs for a shelf test")
    ap.add_argument("--brand-color", default="#1F2937", help="Brand colour for background tests")
    ap.add_argument("--name", default="", help="Brand name used in context mockups")
    ap.add_argument("-o", "--out", default="test-sheet.html")
    args = ap.parse_args()

    for p in args.logos + args.compare:
        if not pathlib.Path(p).is_file():
            print(f"Not found: {p}", file=sys.stderr)
            return 2
    items = [(p, data_uri(p)) for p in args.logos]
    refs = [(p, data_uri(p)) for p in args.compare]
    body = "".join(logo_section(p, u, args.brand_color, args.name) for p, u in items)
    if len(items) > 1:
        body = side_by_side(items) + body
    if refs:
        body = shelf(items, refs) + body
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Logo test sheet</title><style>{CSS}</style></head>
<body><header class="top"><h1>Logo test sheet{(" — " + html.escape(args.name)) if args.name else ""}</h1>
<p>{len(items)} logo(s){f", {len(refs)} reference mark(s)" if refs else ""}. One-colour and reversed views use CSS filters: they show the
silhouette, not a designed variant.</p></header><main>{body}</main>
<footer>Generated by brandsmith/preview_sheet.py</footer><script>{JS}</script></body></html>"""
    out = pathlib.Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
