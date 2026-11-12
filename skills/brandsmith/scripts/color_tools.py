#!/usr/bin/env python3
"""Colour tools for brand palettes. Dependency-free.

Commands:
  convert  <hex…>                 HEX, RGB, HSL, OKLCH and a naive CMYK for each colour
  contrast <hex…> [--json]        WCAG 2.x contrast matrix with AA/AAA verdicts
  cvd      <hex…>                 Simulate protanopia, deuteranopia, tritanopia, achromatopsia;
                                  warns when two palette colours become hard to tell apart
  scale    <hex> [--steps 9]      Perceptual tint/shade scale in OKLCH (50…900 style)
  swatch   <hex…> -o file.html    HTML swatch page with values and contrast on white/black
  identity <identity.json>        Run convert + contrast + cvd on the colours in .brand/identity.json

Names: pass "Name=#hex" to label a colour, e.g. "Ink=#14213D".

CMYK here is a mathematical approximation without an ICC profile. Final print values (CMYK, Pantone) must be
chosen with a swatch book and a proof.
"""
import argparse
import html
import json
import math
import pathlib
import sys


# ---------- parsing ----------

def parse(arg):
    """'Name=#abc' or '#aabbcc' or 'aabbcc' -> (name, (r,g,b) 0-255, hex)."""
    name = None
    if "=" in arg:
        name, arg = arg.split("=", 1)
    h = arg.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6 or any(c not in "0123456789abcdefABCDEF" for c in h):
        raise SystemExit(f"Not a hex colour: {arg!r}")
    rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    hx = "#" + h.upper()
    return (name or hx), rgb, hx


def to_hex(rgb):
    return "#" + "".join(f"{max(0, min(255, round(c))):02X}" for c in rgb)


# ---------- colour maths ----------

def srgb_to_linear(c):
    c = c / 255
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def linear_to_srgb(c):
    c = max(0.0, min(1.0, c))
    v = 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
    return v * 255


def luminance(rgb):
    r, g, b = (srgb_to_linear(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def rgb_to_hsl(rgb):
    r, g, b = (c / 255 for c in rgb)
    mx, mn = max(r, g, b), min(r, g, b)
    l = (mx + mn) / 2
    if mx == mn:
        return 0.0, 0.0, l * 100
    d = mx - mn
    s = d / (2 - mx - mn) if l > 0.5 else d / (mx + mn)
    if mx == r:
        h = (g - b) / d + (6 if g < b else 0)
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60, s * 100, l * 100


def rgb_to_cmyk(rgb):
    r, g, b = (c / 255 for c in rgb)
    k = 1 - max(r, g, b)
    if k >= 1:
        return 0, 0, 0, 100
    c = (1 - r - k) / (1 - k)
    m = (1 - g - k) / (1 - k)
    y = (1 - b - k) / (1 - k)
    return tuple(round(v * 100) for v in (c, m, y, k))


def rgb_to_oklab(rgb):
    r, g, b = (srgb_to_linear(c) for c in rgb)
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    l_, m_, s_ = (math.copysign(abs(v) ** (1 / 3), v) for v in (l, m, s))
    return (0.2104542553 * l_ + 0.7936177850 * m_ - 0.0040720468 * s_,
            1.9779984951 * l_ - 2.4285922050 * m_ + 0.4505937099 * s_,
            0.0259040371 * l_ + 0.7827717662 * m_ - 0.8086757660 * s_)


def oklab_to_rgb(lab):
    L, a, b = lab
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    r = 4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s
    g = -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s
    bb = -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s
    return tuple(linear_to_srgb(v) for v in (r, g, bb))


def rgb_to_oklch(rgb):
    L, a, b = rgb_to_oklab(rgb)
    C = math.hypot(a, b)
    H = math.degrees(math.atan2(b, a)) % 360
    return L, C, H


def oklch_to_rgb(L, C, H):
    h = math.radians(H)
    return oklab_to_rgb((L, C * math.cos(h), C * math.sin(h)))


def in_gamut(L, C, H):
    h = math.radians(H)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = L + 0.3963377774 * a + 0.2158037573 * b
    m_ = L - 0.1055613458 * a - 0.0638541728 * b
    s_ = L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    lin = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return all(-1e-4 <= v <= 1 + 1e-4 for v in lin)


def delta_e_ok(a, b):
    """Perceptual distance in OKLab (x100, ~1 = just noticeable, <~5 easily confused)."""
    la, lb = rgb_to_oklab(a), rgb_to_oklab(b)
    return 100 * math.dist(la, lb)


# Colour-vision-deficiency matrices (Machado et al. 2009, severity 1.0), applied in linear RGB.
CVD = {
    "protanopia": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deuteranopia": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritanopia": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}


def simulate(rgb, kind):
    lin = [srgb_to_linear(c) for c in rgb]
    if kind == "achromatopsia":
        y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
        return tuple(linear_to_srgb(y) for _ in range(3))
    m = CVD[kind]
    out = [sum(m[i][j] * lin[j] for j in range(3)) for i in range(3)]
    return tuple(linear_to_srgb(v) for v in out)


# ---------- commands ----------

def wcag_label(r):
    if r >= 7:
        return "AAA"
    if r >= 4.5:
        return "AA"
    if r >= 3:
        return "AA-large/UI"
    return "fail"


def cmd_convert(colors):
    for name, rgb, hx in colors:
        h, s, l = rgb_to_hsl(rgb)
        L, C, H = rgb_to_oklch(rgb)
        c, m, y, k = rgb_to_cmyk(rgb)
        print(f"{name}")
        print(f"  HEX    {hx}")
        print(f"  RGB    {rgb[0]}, {rgb[1]}, {rgb[2]}")
        print(f"  HSL    {h:.0f}°, {s:.0f}%, {l:.0f}%")
        print(f"  OKLCH  oklch({L * 100:.1f}% {C:.3f} {H:.1f})")
        print(f"  CMYK   {c}, {m}, {y}, {k}  (naive, no ICC profile — confirm with a proof)")
        print(f"  Contrast vs white {contrast(rgb, (255, 255, 255)):.2f}:1 · vs black {contrast(rgb, (0, 0, 0)):.2f}:1")
        print()


def cmd_contrast(colors, as_json=False):
    rows = []
    for i, (na, a, ha) in enumerate(colors):
        for nb, b, hb in colors[i + 1:]:
            r = contrast(a, b)
            rows.append({"a": na, "b": nb, "ratio": round(r, 2), "level": wcag_label(r)})
    if as_json:
        print(json.dumps(rows, indent=2))
        return
    names = [n for n, _, _ in colors]
    w = max(8, max(len(n) for n in names) + 1)
    print("WCAG 2.x contrast matrix (text: AA ≥ 4.5, large text/UI ≥ 3, AAA ≥ 7)\n")
    print(" " * w + "".join(n[:w - 1].rjust(w) for n in names))
    for na, a, _ in colors:
        line = na[:w - 1].ljust(w)
        for nb, b, _ in colors:
            line += ("—" if na == nb else f"{contrast(a, b):.2f}").rjust(w)
        print(line)
    print("\nPairs usable for body text (AA ≥ 4.5):")
    ok = [r for r in rows if r["ratio"] >= 4.5]
    for r in sorted(ok, key=lambda r: -r["ratio"]):
        print(f"  {r['a']} / {r['b']}: {r['ratio']}:1 ({r['level']})")
    if not ok:
        print("  none")
    large = [r for r in rows if 3 <= r["ratio"] < 4.5]
    if large:
        print("Large text / UI only (3–4.5):")
        for r in large:
            print(f"  {r['a']} / {r['b']}: {r['ratio']}:1")


def cmd_cvd(colors):
    kinds = ["protanopia", "deuteranopia", "tritanopia", "achromatopsia"]
    print("Colour-vision deficiency simulation (Machado 2009, full severity)\n")
    for name, rgb, hx in colors:
        sims = "  ".join(f"{k[:5]} {to_hex(simulate(rgb, k))}" for k in kinds)
        print(f"{name:14} {hx}  {sims}")
    print("\nPairs at risk of confusion (OKLab ΔE < 8 after simulation; original ΔE in brackets):")
    found = False
    for i, (na, a, _) in enumerate(colors):
        for nb, b, _ in colors[i + 1:]:
            orig = delta_e_ok(a, b)
            for k in kinds:
                d = delta_e_ok(simulate(a, k), simulate(b, k))
                if d < 8 and orig >= 8:
                    print(f"  {na} / {nb} under {k}: ΔE {d:.1f} (normal {orig:.1f})")
                    found = True
    if not found:
        print("  none — but never rely on colour alone to carry meaning.")


def make_scale(rgb, steps):
    L0, C0, H0 = rgb_to_oklch(rgb)
    lights = [0.97 - i * (0.97 - 0.25) / (steps - 1) for i in range(steps)]
    out = []
    for L in lights:
        # chroma tapers toward the extremes; reduce until in gamut
        C = C0 * (1 - abs(L - L0) * 0.8) if C0 > 0 else 0
        C = max(C, 0)
        while C > 0 and not in_gamut(L, C, H0):
            C -= 0.002
        out.append(to_hex(oklch_to_rgb(L, max(C, 0), H0)))
    return out


def cmd_scale(colors, steps):
    labels_9 = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950]
    for name, rgb, hx in colors:
        scale = make_scale(rgb, steps)
        labels = labels_9[:steps] if steps <= len(labels_9) else list(range(steps))
        print(f"{name} ({hx}) — OKLCH scale, same hue, gamut-mapped")
        for lab, h in zip(labels, scale):
            _, r, _ = parse(h)
            print(f"  {str(lab):>4}  {h}   vs white {contrast(r, (255, 255, 255)):.2f}  vs black {contrast(r, (0, 0, 0)):.2f}")
        print()


def cmd_swatch(colors, out):
    cards = []
    for name, rgb, hx in colors:
        L, C, H = rgb_to_oklch(rgb)
        c, m, y, k = rgb_to_cmyk(rgb)
        fg = "#000" if contrast(rgb, (0, 0, 0)) >= contrast(rgb, (255, 255, 255)) else "#fff"
        cards.append(f"""
  <figure class="card">
    <div class="chip" style="background:{hx};color:{fg}">
      <span>Aa</span><small>{contrast(rgb, (255,255,255)):.2f} ⟷ white · {contrast(rgb, (0,0,0)):.2f} ⟷ black</small>
    </div>
    <figcaption><strong>{html.escape(name)}</strong><br>
      {hx}<br>RGB {rgb[0]} {rgb[1]} {rgb[2]}<br>oklch({L*100:.1f}% {C:.3f} {H:.1f})<br>
      CMYK≈ {c} {m} {y} {k}</figcaption>
  </figure>""")
    names = [n for n, _, _ in colors]
    grid_rows = []
    for na, a, ha in colors:
        cells = []
        for nb, b, hb in colors:
            if na == nb:
                cells.append("<td></td>")
            else:
                r = contrast(a, b)
                cells.append(f'<td style="background:{hb};color:{ha}" title="{r:.2f}:1">Aa<br><small>{r:.1f} {wcag_label(r)}</small></td>')
        grid_rows.append(f"<tr><th>{html.escape(na)}</th>{''.join(cells)}</tr>")
    page = f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Palette swatch</title><style>
body{{font:14px/1.4 system-ui,sans-serif;margin:24px;background:#fafafa;color:#111}}
.grid{{display:flex;flex-wrap:wrap;gap:16px}} .card{{margin:0;width:200px;background:#fff;border:1px solid #ddd;border-radius:8px;overflow:hidden}}
.chip{{height:120px;display:flex;flex-direction:column;justify-content:space-between;padding:10px;font-size:28px;font-weight:700}}
.chip small{{font-size:11px;font-weight:400}} figcaption{{padding:10px;font-size:12px}}
table{{border-collapse:collapse;margin-top:24px}} td,th{{border:1px solid #ccc;padding:8px;text-align:center;font-weight:700}} td small{{font-weight:400}}
</style></head><body><h1>Palette</h1><div class="grid">{''.join(cards)}</div>
<h2>Contrast grid (row = text colour, column = background)</h2>
<table><tr><th></th>{''.join(f'<th>{html.escape(n)}</th>' for n in names)}</tr>{''.join(grid_rows)}</table>
<p><small>CMYK values are naive approximations without an ICC profile. Confirm print colours with a swatch book and proof.</small></p>
</body></html>"""
    pathlib.Path(out).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out).write_text(page, encoding="utf-8")
    print(f"Wrote {out}")


def colors_from_identity(path):
    data = json.loads(pathlib.Path(path).read_text(encoding="utf-8"))
    out = []
    for c in data.get("colors", []):
        if c.get("hex"):
            out.append(parse(f"{c.get('name') or c['hex']}={c['hex']}"))
    if not out:
        raise SystemExit("No colours with a 'hex' value in identity.json")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for c in ("convert", "contrast", "cvd", "swatch"):
        p = sub.add_parser(c)
        p.add_argument("colors", nargs="+")
        if c == "contrast":
            p.add_argument("--json", action="store_true")
        if c == "swatch":
            p.add_argument("-o", "--out", default="palette.html")
    p = sub.add_parser("scale")
    p.add_argument("colors", nargs="+")
    p.add_argument("--steps", type=int, default=9)
    p = sub.add_parser("identity")
    p.add_argument("path")
    args = ap.parse_args()

    if args.cmd == "identity":
        colors = colors_from_identity(args.path)
        cmd_convert(colors)
        cmd_contrast(colors)
        print()
        cmd_cvd(colors)
        return 0
    colors = [parse(c) for c in args.colors]
    if args.cmd == "convert":
        cmd_convert(colors)
    elif args.cmd == "contrast":
        cmd_contrast(colors, args.json)
    elif args.cmd == "cvd":
        cmd_cvd(colors)
    elif args.cmd == "scale":
        cmd_scale(colors, max(3, min(11, args.steps)))
    elif args.cmd == "swatch":
        cmd_swatch(colors, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
