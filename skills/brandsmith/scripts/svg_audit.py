#!/usr/bin/env python3
"""Technical audit of logo SVG files. Dependency-free.

Usage:
  python3 svg_audit.py logo.svg [more.svg …] [--json]

Checks (severity: ERROR = breaks a production master, WARN = likely problem, INFO = worth knowing):
  - viewBox present; fixed width/height on the root
  - live text (<text>) — must be outlined in a master
  - raster images (<image>), filters, masks, blend modes, opacity
  - gradients; number of distinct colours
  - strokes (should be outlined in final masters)
  - near-miss angles (e.g. 44.6° instead of 45°) and near-miss horizontals/verticals
  - tiny details that vanish at 32 px and 16 px
  - optical centring of the artwork within the viewBox
  - complexity (path commands / nodes)
  - editor metadata left in the file

Limitations: bounding boxes include Bézier control points (slightly generous); arcs use endpoints only.
"""
import argparse
import json
import math
import re
import sys
import xml.etree.ElementTree as ET

SVG_NS = "http://www.w3.org/2000/svg"
SHAPES = {"path", "rect", "circle", "ellipse", "line", "polyline", "polygon"}
EDITOR_NS = ("inkscape", "sodipodi", "sketch", "adobe", "illustrator", "figma", "serif", "affinity")
NAMED_NONE = {"none", "transparent", "currentcolor", "inherit"}


def local(tag):
    return tag.split("}", 1)[-1] if "}" in tag else tag


# ---------- transforms ----------

def mat_mul(a, b):
    a1, b1, c1, d1, e1, f1 = a
    a2, b2, c2, d2, e2, f2 = b
    return (a1 * a2 + c1 * b2, b1 * a2 + d1 * b2, a1 * c2 + c1 * d2, b1 * c2 + d1 * d2,
            a1 * e2 + c1 * f2 + e1, b1 * e2 + d1 * f2 + f1)


IDENT = (1, 0, 0, 1, 0, 0)


def parse_transform(s):
    m = IDENT
    if not s:
        return m
    for name, args in re.findall(r"(\w+)\s*\(([^)]*)\)", s):
        v = [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", args)]
        if name == "matrix" and len(v) == 6:
            t = tuple(v)
        elif name == "translate":
            t = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        elif name == "scale":
            t = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "rotate":
            r = math.radians(v[0])
            t = (math.cos(r), math.sin(r), -math.sin(r), math.cos(r), 0, 0)
            if len(v) == 3:
                t = mat_mul(mat_mul((1, 0, 0, 1, v[1], v[2]), t), (1, 0, 0, 1, -v[1], -v[2]))
        elif name == "skewX":
            t = (1, 0, math.tan(math.radians(v[0])), 1, 0, 0)
        elif name == "skewY":
            t = (1, math.tan(math.radians(v[0])), 0, 1, 0, 0)
        else:
            continue
        m = mat_mul(m, t)
    return m


def apply(m, p):
    a, b, c, d, e, f = m
    return (a * p[0] + c * p[1] + e, b * p[0] + d * p[1] + f)


# ---------- path parsing ----------

TOKEN = re.compile(r"[MmZzLlHhVvCcSsQqTtAa]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?")
ARGC = {"M": 2, "L": 2, "H": 1, "V": 1, "C": 6, "S": 4, "Q": 4, "T": 2, "A": 7, "Z": 0}


def parse_path(d):
    """Return (points, straight_segments, command_count). Points include control points."""
    toks = TOKEN.findall(d or "")
    pts, segs = [], []
    cmds = 0
    i = 0
    cmd = None
    cx = cy = sx = sy = 0.0
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t
            i += 1
            cmds += 1
            if cmd in "Zz":
                if (cx, cy) != (sx, sy):
                    segs.append(((cx, cy), (sx, sy)))
                cx, cy = sx, sy
                continue
        if cmd is None:
            break
        up = cmd.upper()
        n = ARGC[up]
        if i + n > len(toks) or any(x.isalpha() for x in toks[i:i + n]):
            break
        v = [float(x) for x in toks[i:i + n]]
        i += n
        rel = cmd.islower()
        ox, oy = (cx, cy) if rel else (0.0, 0.0)
        if up == "M":
            cx, cy = v[0] + ox, v[1] + oy
            sx, sy = cx, cy
            pts.append((cx, cy))
            cmd = "l" if rel else "L"  # subsequent pairs are lineto
        elif up == "L":
            nx, ny = v[0] + ox, v[1] + oy
            segs.append(((cx, cy), (nx, ny)))
            cx, cy = nx, ny
            pts.append((cx, cy))
        elif up == "H":
            nx = v[0] + (cx if rel else 0)
            segs.append(((cx, cy), (nx, cy)))
            cx = nx
            pts.append((cx, cy))
        elif up == "V":
            ny = v[0] + (cy if rel else 0)
            segs.append(((cx, cy), (cx, ny)))
            cy = ny
            pts.append((cx, cy))
        elif up in ("C", "S", "Q", "T"):
            coords = [(v[k] + ox, v[k + 1] + oy) for k in range(0, n, 2)]
            pts.extend(coords)
            cx, cy = coords[-1]
        elif up == "A":
            cx, cy = v[5] + ox, v[6] + oy
            pts.append((cx, cy))  # endpoint only (see Limitations)
    return pts, segs, cmds


def shape_geometry(el):
    """Points, straight segments, command count for a basic shape (untransformed)."""
    tag = local(el.tag)
    g = lambda k, d=0.0: float(re.sub(r"[a-z%]+$", "", el.get(k, str(d))) or d)
    if tag == "path":
        return parse_path(el.get("d", ""))
    if tag == "rect":
        x, y, w, h = g("x"), g("y"), g("width"), g("height")
        p = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        rx = g("rx") or g("ry")
        segs = [] if rx else [(p[i], p[(i + 1) % 4]) for i in range(4)]
        return p, segs, 4
    if tag in ("circle", "ellipse"):
        cx, cy = g("cx"), g("cy")
        rx = g("r") if tag == "circle" else g("rx")
        ry = g("r") if tag == "circle" else g("ry")
        return [(cx - rx, cy - ry), (cx + rx, cy + ry)], [], 4
    if tag == "line":
        p = [(g("x1"), g("y1")), (g("x2"), g("y2"))]
        return p, [tuple(p)], 1
    if tag in ("polyline", "polygon"):
        nums = [float(x) for x in re.findall(r"[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?", el.get("points", ""))]
        p = list(zip(nums[0::2], nums[1::2]))
        segs = [(p[i], p[i + 1]) for i in range(len(p) - 1)]
        if tag == "polygon" and len(p) > 2:
            segs.append((p[-1], p[0]))
        return p, segs, len(p)
    return [], [], 0


# ---------- style helpers ----------

def style_dict(el):
    d = {}
    for part in (el.get("style") or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            d[k.strip()] = v.strip()
    for k in ("fill", "stroke", "stroke-width", "opacity", "fill-opacity", "stroke-opacity", "mix-blend-mode",
              "filter", "mask", "clip-path", "display", "visibility"):
        if el.get(k) is not None and k not in d:
            d[k] = el.get(k)
    return d


def norm_color(v):
    if not v:
        return None
    v = v.strip().lower()
    if v in NAMED_NONE or v.startswith("url("):
        return None
    m = re.fullmatch(r"#([0-9a-f]{3}|[0-9a-f]{6})", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return "#" + h.upper()
    m = re.fullmatch(r"rgba?\(([^)]*)\)", v)
    if m:
        parts = [p.strip() for p in m.group(1).replace("/", ",").split(",")]
        try:
            rgb = [round(float(p[:-1]) * 2.55) if p.endswith("%") else round(float(p)) for p in parts[:3]]
            return "#" + "".join(f"{max(0, min(255, c)):02X}" for c in rgb)
        except ValueError:
            return v
    return v  # named colour such as "black"


# ---------- audit ----------

def audit(path):
    findings = []
    add = lambda sev, msg: findings.append({"severity": sev, "message": msg})
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", errors="replace")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as e:
        return {"file": path, "findings": [{"severity": "ERROR", "message": f"Not valid XML: {e}"}], "stats": {}}

    if local(root.tag) != "svg":
        add("ERROR", "Root element is not <svg>.")

    vb = root.get("viewBox")
    vbox = None
    if not vb:
        add("ERROR", "No viewBox — the logo will not scale predictably. Add viewBox=\"0 0 W H\".")
        try:
            vbox = (0, 0, float(re.sub(r"[a-z%]+$", "", root.get("width", ""))),
                    float(re.sub(r"[a-z%]+$", "", root.get("height", ""))))
        except ValueError:
            vbox = None
    else:
        vals = [float(x) for x in re.split(r"[\s,]+", vb.strip()) if x]
        if len(vals) == 4:
            vbox = tuple(vals)
    if root.get("width") or root.get("height"):
        add("INFO", f"Root has fixed size (width={root.get('width')}, height={root.get('height')}). Fine for exports; "
                    "masters are usually more flexible with viewBox only.")

    # editor metadata
    ns_hits = sorted({n for n in EDITOR_NS if re.search(rf"xmlns:{n}|<{n}:|{n}:", text, re.I)})
    if ns_hits or "<metadata" in text or "<!--" in text:
        what = ", ".join(ns_hits) if ns_hits else "metadata/comments"
        add("INFO", f"Editor leftovers ({what}). Clean before delivery (e.g. SVGO or 'export as plain SVG').")

    colors, gradients = set(), 0
    texts = images = filters = masks = clips = strokes = blends = transparencies = 0
    total_cmds = 0
    all_pts = []
    elements = []  # (tag, bbox w, h)
    near_miss = []

    # styles in <style> blocks
    for st in root.iter():
        if local(st.tag) == "style" and st.text:
            for c in re.findall(r"(?:fill|stroke|stop-color)\s*:\s*([^;}\s]+)", st.text):
                nc = norm_color(c)
                if nc:
                    colors.add(nc)
            if re.search(r"stroke\s*:\s*(?!none)", st.text):
                strokes += 1

    def walk(el, m, inherited_hidden=False):
        nonlocal texts, images, filters, masks, clips, strokes, blends, transparencies, gradients, total_cmds
        tag = local(el.tag)
        if tag in ("defs", "metadata", "title", "desc", "style", "clipPath", "mask", "symbol", "pattern", "marker"):
            if tag in ("clipPath",):
                clips += 1
            if tag == "mask":
                masks += 1
            # still count gradients / filters defined inside defs
            for sub in el.iter():
                t = local(sub.tag)
                if t in ("linearGradient", "radialGradient"):
                    gradients += 1
                    for stop in sub.iter():
                        if local(stop.tag) == "stop":
                            sd = style_dict(stop)
                            nc = norm_color(sd.get("stop-color") or stop.get("stop-color"))
                            if nc:
                                colors.add(nc)
                elif t == "filter":
                    filters += 1
            return
        if tag in ("linearGradient", "radialGradient"):
            gradients += 1
            return
        if tag == "filter":
            filters += 1
            return
        sd = style_dict(el)
        hidden = inherited_hidden or sd.get("display") == "none" or sd.get("visibility") == "hidden"
        m2 = mat_mul(m, parse_transform(el.get("transform")))
        if sd.get("filter") and sd["filter"] != "none":
            filters += 1
        if sd.get("mix-blend-mode") and sd["mix-blend-mode"] != "normal":
            blends += 1
        for k in ("opacity", "fill-opacity", "stroke-opacity"):
            try:
                if k in sd and float(sd[k]) < 1:
                    transparencies += 1
            except ValueError:
                pass
        if tag in ("text", "tspan", "textPath"):
            if tag == "text":
                texts += 1
            return
        if tag == "image":
            images += 1
            return
        if tag in SHAPES and not hidden:
            fill = norm_color(sd.get("fill", "#000000" if "fill" not in sd else None))
            if "fill" not in sd:
                fill = "#000000"
            if fill:
                colors.add(fill)
            stroke = sd.get("stroke")
            if stroke and stroke.lower() != "none":
                strokes += 1
                nc = norm_color(stroke)
                if nc:
                    colors.add(nc)
            pts, segs, cmds = shape_geometry(el)
            total_cmds += cmds
            tp = [apply(m2, p) for p in pts]
            if tp:
                all_pts.extend(tp)
                xs, ys = [p[0] for p in tp], [p[1] for p in tp]
                elements.append((tag, el.get("id") or "", max(xs) - min(xs), max(ys) - min(ys)))
            for a, b in segs:
                a, b = apply(m2, a), apply(m2, b)
                dx, dy = b[0] - a[0], b[1] - a[1]
                length = math.hypot(dx, dy)
                if length < 1e-6:
                    continue
                ang = math.degrees(math.atan2(dy, dx)) % 180
                for target in (0, 45, 90, 135, 180):
                    diff = abs(ang - target)
                    if 0.05 < diff < 1.5:
                        near_miss.append((round(ang, 2), target, round(length, 2)))
                        break
        for child in el:
            walk(child, m2, hidden)

    walk(root, IDENT)

    # findings
    if texts:
        add("ERROR", f"{texts} live <text> element(s). Outline the wordmark for a master; live text renders with "
                     "whatever font the viewer has.")
    if images:
        add("ERROR", f"{images} embedded/linked raster <image>(s). A logo master should be pure vector.")
    if filters:
        add("WARN", f"{filters} filter(s) (blur, shadow…). Effects don't survive one-colour, embroidery or many "
                    "export pipelines. Keep a flat version.")
    if blends:
        add("WARN", f"{blends} blend mode(s). Unreliable across tools and print.")
    if transparencies:
        add("WARN", f"{transparencies} element(s) with opacity < 1. Transparency changes on every background and "
                    "is hard to print; use solid tints.")
    if masks or clips:
        add("INFO", f"{masks} mask(s), {clips} clipPath(s). Fine for construction; flatten for delivery if possible.")
    if gradients:
        add("WARN", f"{gradients} gradient(s). Make sure a flat, one-colour version exists and is the primary.")
    if strokes:
        add("WARN", f"Strokes used on {strokes} element(s). Outline strokes in final masters so scaling and "
                    "exports don't change weight.")

    # painted knock-outs: a white/near-white shape used to "cut" a hole in a darker one breaks on dark backgrounds,
    # in one colour and reversed. Real holes should be cut (compound path / evenodd), not painted.
    def _lightness(c):
        m = re.fullmatch(r"#([0-9A-F]{6})", c or "")
        if not m:
            return None
        r, g, b_ = (int(m.group(1)[i:i + 2], 16) for i in (0, 2, 4))
        return (0.2126 * r + 0.7152 * g + 0.0722 * b_) / 255
    lights = [c for c in colors if (_lightness(c) or 0) > .92]
    if lights and len(colors) > len(lights):
        add("WARN", f"White or near-white fill ({', '.join(sorted(lights))}) alongside darker colours. If it paints a "
                    "'hole' over another shape, the mark breaks on dark backgrounds, in one colour and reversed: cut the "
                    "hole instead (Figma: Subtract + Flatten; Illustrator: Pathfinder Minus Front).")
    ncol = len(colors)
    if ncol > 4:
        add("WARN", f"{ncol} distinct colours: {', '.join(sorted(colors))}. Logos usually work best with 1–3.")
    else:
        add("INFO", f"{ncol} colour(s): {', '.join(sorted(colors)) or 'none detected'}.")

    if near_miss:
        sample = ", ".join(f"{a}° (≈{t}°)" for a, t, _ in near_miss[:6])
        add("WARN", f"{len(near_miss)} straight segment(s) just off a clean angle: {sample}. Usually a construction "
                    "slip; snap them unless the deviation is an intentional optical correction.")

    stats = {"colors": sorted(colors), "path_commands": total_cmds, "elements": len(elements)}

    if vbox and all_pts:
        vx, vy, vw, vh = vbox
        xs, ys = [p[0] for p in all_pts], [p[1] for p in all_pts]
        bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
        bw, bh = bx1 - bx0, by1 - by0
        stats["bbox"] = [round(bx0, 2), round(by0, 2), round(bw, 2), round(bh, 2)]
        if bx0 < vx - 0.5 or by0 < vy - 0.5 or bx1 > vx + vw + 0.5 or by1 > vy + vh + 0.5:
            add("WARN", "Artwork extends beyond the viewBox — it will be clipped.")
        # centring
        off_x = ((bx0 + bx1) / 2 - (vx + vw / 2)) / vw * 100
        off_y = ((by0 + by1) / 2 - (vy + vh / 2)) / vh * 100
        stats["center_offset_pct"] = [round(off_x, 1), round(off_y, 1)]
        if abs(off_x) > 2 or abs(off_y) > 2:
            add("INFO", f"Artwork bounding box is off the viewBox centre by {off_x:+.1f}% x, {off_y:+.1f}% y. Check "
                        "whether that's intentional (optical centring sits slightly above geometric centre).")
        margin = min(bx0 - vx, by0 - vy, vx + vw - bx1, vy + vh - by1)
        stats["min_margin_pct"] = round(margin / max(vw, vh) * 100, 1)
        # tiny details
        scale = max(vw, vh)
        tiny16 = [e for e in elements if 0 < max(e[2], e[3]) < scale / 16]
        tiny32 = [e for e in elements if 0 < max(e[2], e[3]) < scale / 32]
        if tiny32:
            add("WARN", f"{len(tiny32)} element(s) smaller than 1 px at 32 px render size — they will disappear or "
                        "blur into mush in favicons and small UI.")
        elif tiny16:
            add("INFO", f"{len(tiny16)} element(s) smaller than 1 px at 16 px — check the 16 px rendering.")

    if total_cmds > 400:
        add("WARN", f"{total_cmds} path commands — very complex for a logo. Check for unnecessary nodes or detail.")
    elif total_cmds > 150:
        add("INFO", f"{total_cmds} path commands — moderately complex. Fine for illustrative marks.")
    else:
        add("INFO", f"{total_cmds} path commands — simple construction.")

    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    findings.sort(key=lambda f: order[f["severity"]])
    return {"file": path, "findings": findings, "stats": stats}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    results = [audit(f) for f in args.files]
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            print(f"== {r['file']}")
            for f in r["findings"]:
                print(f"  [{f['severity']}] {f['message']}")
            if r["stats"]:
                print(f"  stats: {json.dumps(r['stats'])}")
            print()
    return 1 if any(f["severity"] == "ERROR" for r in results for f in r["findings"]) else 0


if __name__ == "__main__":
    sys.exit(main())
