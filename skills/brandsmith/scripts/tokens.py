#!/usr/bin/env python3
"""Generate design tokens from .brand/identity.json. Dependency-free.

Only what identity.json defines is exported: no default type scale, spacing or radius is invented.
In the Tailwind theme, sizes, spacing and radii are prefixed `brand-` so they extend Tailwind's own scales
instead of overriding them (e.g. `p-brand-2`, `text-brand-lg`); colours and font families keep their names.

Usage:
  python3 tokens.py .brand/identity.json -o exports/tokens [--format all|dtcg|css|scss|tailwind]
  python3 tokens.py .brand/identity.json --approved-only -o exports/tokens

Outputs:
  tokens.json        W3C Design Tokens Community Group format ($value/$type)
  tokens.css         CSS custom properties on :root
  _tokens.scss       SCSS variables
  tailwind.theme.js  a `theme.extend` object for Tailwind CSS

Colour names become kebab-case keys (e.g. "Deep Ink" → color-deep-ink). Role aliases are added
(color-primary → the colour whose role is "primary").
"""
import argparse
import json
import pathlib
import re
import sys


def kebab(s):
    s = re.sub(r"[^0-9A-Za-z]+", "-", str(s)).strip("-").lower()
    return s or "unnamed"


def build(identity, approved_only):
    keep = lambda e: (not approved_only) or e.get("status") == "approved"
    t = {"color": {}, "font": {"family": {}, "weight": {}}, "size": {}, "space": {}, "radius": {}}
    roles = {}
    for c in identity.get("colors", []):
        if not c.get("hex") or not keep(c):
            continue
        k = kebab(c.get("name") or c["hex"])
        t["color"][k] = {"$value": c["hex"].upper(), "$type": "color"}
        if c.get("role") and c["role"] not in roles:
            roles[kebab(c["role"])] = k
    for role, k in roles.items():
        if role not in t["color"]:
            t["color"][role] = {"$value": "{color." + k + "}", "$type": "color"}
    for f in identity.get("typography", []):
        if not f.get("family") or not keep(f):
            continue
        role = kebab(f.get("role") or f["family"])
        fam = [f["family"]] + [x.strip() for x in (f.get("fallback") or "sans-serif").split(",") if x.strip()]
        t["font"]["family"][role] = {"$value": fam, "$type": "fontFamily"}
        for w in f.get("weights", []) or []:
            t["font"]["weight"][f"{role}-{w}"] = {"$value": int(w), "$type": "fontWeight"}
    # type scale, spacing and radius only when the identity actually defines them (never invent design decisions)
    ts = identity.get("type_scale") or {}
    if ts.get("base") and ts.get("ratio") and keep(ts):
        base, ratio = float(ts["base"]), float(ts["ratio"])
        steps = {"xs": -2, "sm": -1, "base": 0, "lg": 1, "xl": 2, "2xl": 3, "3xl": 4, "4xl": 5, "5xl": 6}
        for name, n in steps.items():
            t["size"][name] = {"$value": f"{round(base * ratio ** n / 16, 4)}rem", "$type": "dimension"}
    spc = identity.get("spacing") or {}
    if spc.get("base") and keep(spc):
        sp = float(spc["base"])
        for mult in (0, 0.5, 1, 1.5, 2, 3, 4, 6, 8, 12, 16):
            key = str(mult).replace(".", "_") if mult != int(mult) else str(int(mult))
            t["space"][key] = {"$value": f"{sp * mult / 16:g}rem", "$type": "dimension"}
    rad = {k: v for k, v in (identity.get("radius") or {}).items() if k != "status"}
    for k, v in (rad.items() if keep(identity.get("radius") or {}) else []):
        t["radius"][kebab(k)] = {"$value": f"{v}px", "$type": "dimension"}
    return {k: v for k, v in t.items() if v and (not isinstance(v, dict) or any(v.values()))}


def flatten(tokens, prefix=()):
    for k, v in tokens.items():
        if isinstance(v, dict) and "$value" in v:
            yield prefix + (k,), v["$value"]
        elif isinstance(v, dict):
            yield from flatten(v, prefix + (k,))


def css_value(val, sep="--"):
    if isinstance(val, list):
        return ", ".join(f'"{x}"' if " " in x and not x.startswith('"') else x for x in val)
    if isinstance(val, str) and val.startswith("{") and val.endswith("}"):
        return f"var({sep}{val[1:-1].replace('.', '-')})"
    return str(val)


def to_css(tokens):
    lines = [":root {"]
    for path, val in flatten(tokens):
        lines.append(f"  --{'-'.join(path)}: {css_value(val)};")
    lines.append("}")
    return "\n".join(lines) + "\n"


def to_scss(tokens):
    out = []
    for path, val in flatten(tokens):
        v = css_value(val)
        if v.startswith("var(--"):
            v = "$" + v[6:-1]
        out.append(f"${'-'.join(path)}: {v};")
    return "\n".join(out) + "\n"


def to_tailwind(tokens):
    def resolve(val):
        if isinstance(val, str) and val.startswith("{"):
            node = tokens
            for p in val[1:-1].split("."):
                node = node[p]
            return resolve(node["$value"])
        return val
    theme = {
        "colors": {k: resolve(v["$value"]) for k, v in tokens.get("color", {}).items()},
        "fontFamily": {k: v["$value"] for k, v in tokens.get("font", {}).get("family", {}).items()},
        "fontSize": {"brand-" + k: v["$value"] for k, v in tokens.get("size", {}).items()},
        "spacing": {"brand-" + k: v["$value"] for k, v in tokens.get("space", {}).items()},
        "borderRadius": {"brand-" + k: v["$value"] for k, v in tokens.get("radius", {}).items()},
    }
    theme = {k: v for k, v in theme.items() if v}
    return "/** Generated by brandsmith/tokens.py — use as theme.extend */\nmodule.exports = " + \
        json.dumps(theme, indent=2) + ";\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("identity")
    ap.add_argument("-o", "--out", default="tokens")
    ap.add_argument("--format", default="all", choices=["all", "dtcg", "css", "scss", "tailwind"])
    ap.add_argument("--approved-only", action="store_true", help="Only include entries with status 'approved'")
    args = ap.parse_args()

    identity = json.loads(pathlib.Path(args.identity).read_text(encoding="utf-8"))
    tokens = build(identity, args.approved_only)
    if not tokens.get("color"):
        print("Warning: no colours found (check identity.json 'colors' and --approved-only).", file=sys.stderr)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    writers = {
        "dtcg": ("tokens.json", lambda: json.dumps(tokens, indent=2) + "\n"),
        "css": ("tokens.css", lambda: to_css(tokens)),
        "scss": ("_tokens.scss", lambda: to_scss(tokens)),
        "tailwind": ("tailwind.theme.js", lambda: to_tailwind(tokens)),
    }
    for key, (fname, fn) in writers.items():
        if args.format in ("all", key):
            (out / fname).write_text(fn(), encoding="utf-8")
            print(f"Wrote {out / fname}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
