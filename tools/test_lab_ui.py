#!/usr/bin/env python3
"""Headless smoke test for the Logo Lab interface and PDF reports.

Builds lab pages from the template, opens them in headless Firefox (geckodriver, as tools/calibrate.py)
and checks what the redesign promises: empty state, verdict and "To check" list, folded sections,
export panel modes, designer PDF = 4 pages, client PDF = 2 pages, no network requests in the published
page, no horizontal scroll on a phone, and that the Logo Lab mark itself holds at 16 px.

  python3 tools/test_lab_ui.py            # exits 1 on the first failed check
  python3 tools/test_lab_ui.py --sample   # also rewrites docs/sample-report.pdf

Pages and PDFs go to test-projects/ui-smoke/ (git-ignored; snap Firefox cannot read /tmp).
"""
import base64, pathlib, re, subprocess, sys, time

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from calibrate import Firefox  # noqa: E402

OUT = ROOT / "test-projects" / "ui-smoke"
LAB = ROOT / "skills" / "brandsmith" / "scripts" / "logo_lab.py"
METRICS = ROOT / "skills" / "brandsmith" / "scripts" / "lab_metrics.py"
TEMPLATE = ROOT / "skills" / "brandsmith" / "templates" / "logo-lab.html"
fails = []


def check(name, ok, detail=""):
    print(("ok   " if ok else "FAIL ") + name + (f"  ({detail})" if detail else ""))
    if not ok:
        fails.append(name)


def pages(pdf: bytes) -> int:
    return len(re.findall(rb"/Type\s*/Page\b", pdf))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(LAB), str(ROOT / "docs" / "sample-mark.svg"), "-o", str(OUT / "sample.html"),
                    "--name", "Meridiana", "--color", "#1b2a4a"], check=True, capture_output=True)
    (OUT / "empty.html").write_text("\n".join(l for l in TEMPLATE.read_text(encoding="utf-8").splitlines()
                                              if "fonts.g" not in l), encoding="utf-8")

    published = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    urls = set(re.findall(r"https?://[^\s\"')]+", published)) - {"http://www.w3.org/2000/svg"}
    check("published page has no network URLs", not urls, ", ".join(sorted(urls))[:200])

    m = subprocess.run([sys.executable, str(METRICS), str(ROOT / "docs" / "brand" / "logo-lab-mark.svg")],
                       capture_output=True, text=True).stdout
    check("Logo Lab mark holds at 16 px", "minimum size 16 px" in m, m.strip()[-120:])

    ff = Firefox()
    try:
        ff._req("POST", f"/session/{ff.sid}/window/rect", {"width": 1440, "height": 1000})
        ff.get((OUT / "empty.html").as_uri()); time.sleep(2)
        check("empty state: drop area and sample button", ff.js("return !!document.querySelector('.drop') && !!document.querySelector('#sample')"))
        check("empty state: header actions hidden", ff.js("return getComputedStyle(document.querySelector('#exportBtn')).display === 'none' && getComputedStyle(document.querySelector('#filechip')).display === 'none'"))

        ff.js("document.querySelector('#sample').click(); return 1")
        check("loading screen while analysing", ff.js("return !!document.querySelector('.loading')"))
        t0 = time.time()
        while time.time() - t0 < 30 and ff.js("return !!document.querySelector('.loading')"): time.sleep(.5)
        print(f"     analysis took {time.time() - t0:.1f} s; document.hidden =", ff.js("return document.hidden"))
        st = ff.js("return [document.querySelector('.loading') && document.querySelector('.loading .stage').textContent, !!document.querySelector('.loading'), !!document.querySelector('#main .app')]")
        check("loading screen replaced by results", st[1:] == [False, True], str(st))

        ff.get((OUT / "sample.html").as_uri()); time.sleep(6)
        r = ff.js("return window.__LAB_RESULT__ && { score: window.__LAB_RESULT__.score, min: window.__LAB_RESULT__.minSize }")
        check("sample analysed", bool(r), str(r))
        n_check = ff.js("return document.querySelectorAll('.tc-item').length")
        check("verdict card lists the tests to check", (n_check or 0) >= 1, f"{n_check} items")
        check("all-ok sections start folded", ff.js("return document.querySelectorAll('.fold').length") >= 1)
        check("flagged tests show what happens / how to fix", ff.js("return document.querySelectorAll('.test.flag .whatfix').length") >= 1)

        ff.js("document.querySelector('#exportBtn').click(); return 1"); time.sleep(1)
        check("export panel opens", ff.js("return !document.querySelector('#exback').hidden"))
        check("designer mode: no client note field", ff.js("return !document.querySelector('#exnote')"))
        ff.js("document.querySelector('[data-mode=client]').click(); return 1"); time.sleep(.5)
        check("client mode: client note field", ff.js("return !!document.querySelector('#exnote')"))
        ff.js("const set=(id,v)=>{const e=document.querySelector(id); e.value=v; e.dispatchEvent(new Event('input'));};"
              "set('#exstudio','Studio Esempio');"
              "set('#exnote','For favicon and app icon we will draw a simplified version without the outer ring.'); return 1")
        client = base64.b64decode(ff.js("return exportPdf('client', true)"))
        check("client PDF has 2 pages", pages(client) == 2, f"{pages(client)} pages")
        designer = base64.b64decode(ff.js("return exportPdf('designer', true)"))
        check("designer PDF has 4 pages", pages(designer) == 4, f"{pages(designer)} pages")
        check("PDFs have no NaN coordinates", b"NaN" not in designer and b"NaN" not in client)
        (OUT / "designer.pdf").write_bytes(designer); (OUT / "client.pdf").write_bytes(client)
        if "--sample" in sys.argv:
            (ROOT / "docs" / "sample-report.pdf").write_bytes(designer)
            print("wrote docs/sample-report.pdf")
        ff.js("document.querySelector('#exclose').click(); return 1")

        ff.js("document.querySelector('#langgroup [data-lang=it]').click(); return 1"); time.sleep(1)
        check("Italian switch", ff.js("return document.documentElement.lang") == "it")
        ff.js("document.querySelector('#langgroup [data-lang=en]').click(); return 1"); time.sleep(1)

        ff._req("POST", f"/session/{ff.sid}/window/rect", {"width": 390, "height": 860}); time.sleep(1.5)
        check("phone: no horizontal scroll", not ff.js("return document.documentElement.scrollWidth > window.innerWidth"))
        check("phone: bottom bar visible", ff.js("return getComputedStyle(document.querySelector('#mbar')).display !== 'none'"))
    finally:
        ff.close()
    print(f"\n{'all checks passed' if not fails else str(len(fails)) + ' failed'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
