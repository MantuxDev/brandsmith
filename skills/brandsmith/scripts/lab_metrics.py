#!/usr/bin/env python3
"""Read the Logo Lab measurements without a person opening the page.

Usage:
  python3 lab_metrics.py logo.svg [--json]

Runs the real Logo Lab code (templates/logo-lab.html) in headless Firefox through geckodriver and prints the
score, minimum size, limiting factor, thinnest stroke and narrowest gap. Needs Firefox and geckodriver on PATH;
nothing else. If they are missing it exits with code 3 and says so: in that case, do NOT estimate the score.
Give the designer the lab page (logo_lab.py) and ask them to read the number.
"""
import argparse
import json
import pathlib
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
LAB = HERE / "logo_lab.py"


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("logo")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    if not (shutil.which("geckodriver") and (shutil.which("firefox") or shutil.which("firefox-esr"))):
        print("lab_metrics: Firefox and geckodriver are needed to read the Lab score automatically. Do not estimate it: "
              "open the page from logo_lab.py and read the score there.", file=sys.stderr)
        return 3
    src = pathlib.Path(a.logo).resolve()
    # snap-packaged Firefox can't read /tmp: keep the page next to the logo, in a hidden temp folder
    work = pathlib.Path(tempfile.mkdtemp(prefix=".lablab-", dir=str(src.parent)))
    page = work / "lab.html"
    try:
        subprocess.run([sys.executable, str(LAB), str(src), "-o", str(page)], check=True, capture_output=True)
        ff = Firefox()
        try:
            ff.get(page.as_uri() + "#metrics")
            res = None
            for _ in range(300):
                res = ff.js("return window.__LAB_RESULT__ || null")
                if res and res.get("file") == src.name:
                    break
                res = None
                time.sleep(.1)
        finally:
            ff.close()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if not res:
        print("lab_metrics: the Lab did not return a result. Do not estimate the score.", file=sys.stderr)
        return 4
    if res.get("empty"):
        print("No visible shapes found in the file.")
        return 0
    L = max(res["bw"], res["bh"])
    out = {"file": src.name, "score": res["score"], "min_size_px": res["minSize"], "min_size_raw_px": round(res["minSizeRaw"], 1),
           "limiting_factor": res["limit"], "thinnest_stroke_pct_of_mark": round(res["tInk"] / L * 100, 1),
           "narrowest_gap_pct_of_mark": round(res["tGap"] / L * 100, 1), "two_tone": bool(res.get("twoTone")),
           "parts_full_to_32px": [res["fg256"], res["fg32"]], "negative_space_pct": round(res["negRatio"] * 100),
           "note": "strokes/gaps at or above ~7.7% are capped: the mark already holds at 16 px"}
    if a.json:
        print(json.dumps(out, indent=2))
    else:
        print(f"{out['file']}: score {out['score']}/10 · minimum size {out['min_size_px']} px (raw {out['min_size_raw_px']}) · "
              f"limited by {out['limiting_factor']} · thinnest stroke {out['thinnest_stroke_pct_of_mark']}% · "
              f"narrowest gap {out['narrowest_gap_pct_of_mark']}% of the mark" + (" · two-tone" if out["two_tone"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
