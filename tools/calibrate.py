#!/usr/bin/env python3
"""Calibrate the Logo Lab score by running the real Lab code in headless Firefox on sets of logos.

Commands:
  synth OUTDIR                      generate synthetic marks with known stroke/gap sizes (+ truth.json)
  run SET=DIR [SET=DIR …] -o FILE   run the Lab on every SVG in each set; append JSON lines to FILE
        [--limit N] [--sample N --seed S] [--frac F --k K]
  report FILE                       summary per set (min-size distribution, score percentiles)

Requires Firefox + geckodriver on PATH. Logos used for calibration stay outside the repository
(e.g. test-projects/calibration/, which is git-ignored): third-party marks are never committed.
"""
import argparse
import json
import math
import os
import pathlib
import random
import re
import socket
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
LAB = ROOT / "skills" / "brandsmith" / "scripts" / "logo_lab.py"


# ---------------- synthetic marks with known geometry ----------------

def synth(out: pathlib.Path):
    out.mkdir(parents=True, exist_ok=True)
    truth = {}
    V = 200.0  # viewBox size; the mark spans the full viewBox
    for w in (0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8, 12):  # stroke width as % of mark size
        sw = V * w / 100
        r = V / 2 - sw / 2
        name = f"ring_stroke_{w}pct.svg"
        (out / name).write_text(
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {V:g} {V:g}"><circle cx="{V/2:g}" cy="{V/2:g}" '
            f'r="{r:g}" fill="none" stroke="#000" stroke-width="{sw:g}"/></svg>')
        truth[name] = {"kind": "stroke", "pct": w}
    for g in (0.5, 0.75, 1, 1.5, 2, 3, 4, 6, 8):  # gap width as % of mark size, between solid blocks
        gw = V * g / 100
        bw = (V - 2 * gw) / 3
        rects = "".join(f'<rect x="{i * (bw + gw):g}" y="0" width="{bw:g}" height="{V:g}"/>' for i in range(3))
        name = f"bars_gap_{g}pct.svg"
        (out / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {V:g} {V:g}">{rects}</svg>')
        truth[name] = {"kind": "gap", "pct": g}
    # a solid disc plus a comb of thin lines making up a known share of the ink (tests the frac tolerance)
    for share in (0.5, 1, 2, 4, 8):
        sw, ln = V * 0.01, V * 0.28
        disc = math.pi * (V * 0.3) ** 2
        count = max(1, round(share / 100 * disc / (ln * sw - share / 100 * ln * sw)))
        lines = "".join(f'<rect x="{V*0.7:g}" y="{V*0.06 + i * V*0.06:g}" width="{ln:g}" height="{sw:g}"/>' for i in range(count))
        real = count * ln * sw / (disc + count * ln * sw) * 100
        name = f"disc_plus_lines_{share}pctink.svg"
        (out / name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {V:g} {V:g}">'
                                f'<circle cx="{V*0.33:g}" cy="{V/2:g}" r="{V*0.3:g}"/>{lines}</svg>')
        truth[name] = {"kind": "detail", "ink_share_pct": round(real, 2), "pct": 1}
    (out / "truth.json").write_text(json.dumps(truth, indent=2))
    print(f"Wrote {len(truth)} synthetic marks to {out}")


# ---------------- WebDriver (plain HTTP, no Selenium) ----------------

class Firefox:
    def __init__(self):
        s = socket.socket(); s.bind(("127.0.0.1", 0)); self.port = s.getsockname()[1]; s.close()
        self.proc = subprocess.Popen(["geckodriver", "--port", str(self.port)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        self.base = f"http://127.0.0.1:{self.port}"
        for _ in range(50):
            try:
                urllib.request.urlopen(self.base + "/status", timeout=1); break
            except Exception:
                time.sleep(.2)
        caps = {"capabilities": {"alwaysMatch": {"browserName": "firefox", "moz:firefoxOptions": {"args": ["-headless"]}}}}
        self.sid = self._req("POST", "/session", caps)["value"]["sessionId"]

    def _req(self, method, path, body=None):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read() or b"{}")

    def get(self, url):
        self._req("POST", f"/session/{self.sid}/url", {"url": url})

    def js(self, script):
        return self._req("POST", f"/session/{self.sid}/execute/sync", {"script": script, "args": []})["value"]

    def close(self):
        try:
            self._req("DELETE", f"/session/{self.sid}")
        finally:
            self.proc.terminate()


def run(sets, out, limit=None, sample=None, seed=1, frac=None, k=None):
    work = pathlib.Path(tempfile.mkdtemp(prefix="lab-", dir=str(ROOT / "test-projects")))
    ff = Firefox()
    n = 0
    try:
        with open(out, "a", encoding="utf-8") as fh:
            for spec in sets:
                label, d = spec.split("=", 1)
                files = sorted(pathlib.Path(d).glob("*.svg"))
                if sample and len(files) > sample:
                    files = random.Random(seed).sample(files, sample)
                if limit:
                    files = files[:limit]
                for f in files:
                    html = work / (f.stem + ".html")
                    subprocess.run([sys.executable, str(LAB), str(f), "-o", str(html)], check=True, capture_output=True)
                    if frac is not None or k is not None:
                        t = html.read_text(encoding="utf-8")
                        t = re.sub(r"const CAL = \{ k: [\d.]+, frac: [\d.]+",
                                   f"const CAL = {{ k: {k if k is not None else 1.0}, frac: {frac if frac is not None else 0.02}", t, count=1)
                        html.write_text(t, encoding="utf-8")
                    ff.get("about:blank")
                    ff.get(html.as_uri() + "#metrics")
                    res = None
                    for _ in range(300):
                        res = ff.js("return window.__LAB_RESULT__ || null")
                        if res and res.get("file") == f.name:
                            break
                        res = None
                        time.sleep(.1)
                    rec = {"set": label, "file": f.name, "frac": frac, "k": k, **(res or {"error": "timeout"})}
                    fh.write(json.dumps(rec) + "\n")
                    n += 1
                    if n % 25 == 0:
                        print(f"  {n} done", flush=True)
                    html.unlink(missing_ok=True)
    finally:
        ff.close()
        try:
            work.rmdir()
        except OSError:
            pass
    print(f"Measured {n} logos → {out}")


def pct(vals, p):
    vals = sorted(vals)
    if not vals:
        return float("nan")
    i = (len(vals) - 1) * p
    lo, hi = math.floor(i), math.ceil(i)
    return vals[lo] + (vals[hi] - vals[lo]) * (i - lo)


def report(path):
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    sets = {}
    for r in rows:
        sets.setdefault((r["set"], r.get("frac"), r.get("k")), []).append(r)
    for (s, frac, k), rs in sets.items():
        ok = [r for r in rs if "score" in r]
        print(f"\n## {s}  (n={len(rs)}, frac={frac}, k={k}, errors={len(rs) - len(ok)})")
        if not ok:
            continue
        ms = [r["minSize"] for r in ok]
        sc = [r["score"] for r in ok]
        print("  min size distribution: " + ", ".join(f"{v}px:{ms.count(v)}" for v in sorted(set(ms))))
        print(f"  score p10/p50/p90: {pct(sc, .1):.1f} / {pct(sc, .5):.1f} / {pct(sc, .9):.1f}")
        print(f"  share ≤24px: {sum(v <= 24 for v in ms) / len(ms):.0%} · ≤32px: {sum(v <= 32 for v in ms) / len(ms):.0%} · ≥64px: {sum(v >= 64 for v in ms) / len(ms):.0%}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("synth"); p.add_argument("out", type=pathlib.Path)
    p = sub.add_parser("run"); p.add_argument("sets", nargs="+"); p.add_argument("-o", "--out", required=True)
    p.add_argument("--limit", type=int); p.add_argument("--sample", type=int); p.add_argument("--seed", type=int, default=1)
    p.add_argument("--frac", type=float); p.add_argument("--k", type=float)
    p = sub.add_parser("report"); p.add_argument("file")
    a = ap.parse_args()
    if a.cmd == "synth":
        synth(a.out)
    elif a.cmd == "run":
        run(a.sets, a.out, a.limit, a.sample, a.seed, a.frac, a.k)
    else:
        report(a.file)


if __name__ == "__main__":
    main()
