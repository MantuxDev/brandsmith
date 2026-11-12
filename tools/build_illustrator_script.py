#!/usr/bin/env python3
"""Build the Logo Lab script for Adobe Illustrator.

  python3 tools/build_illustrator_script.py      → illustrator/LogoLab.jsx (+ README.md)

Use (no terminal): in Illustrator, select the logo (or nothing, to test the whole artboard) and run
File → Scripts → Other Script… → LogoLab.jsx. To keep it in the menu, copy it into Illustrator's Scripts folder
(Presets/<language>/Scripts) and restart. The script exports the selection as SVG with text outlined, writes a
self-contained Logo Lab page in the system temp folder and opens it in the default browser. Nothing is uploaded.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "skills" / "brandsmith" / "templates" / "logo-lab.html"
OUT = ROOT / "illustrator"

JSX = r"""// Logo Lab for Adobe Illustrator (brandsmith). Exports the selection as SVG and opens the Logo Lab report.
#target illustrator
(function () {
  if (app.documents.length === 0) { alert('Logo Lab: open a document and select your logo.'); return; }
  var doc = app.activeDocument, sel = doc.selection, work = doc, made = false;
  var stamp = new Date().getTime();
  var svgFile = new File(Folder.temp + '/logolab_' + stamp + '.svg');
  try {
    if (sel && sel.length) {
      app.copy();
      work = app.documents.add(doc.documentColorSpace); made = true;
      app.paste();
      work.artboards[0].artboardRect = work.visibleBounds;
    }
    var opt = new ExportOptionsSVG();
    opt.embedRasterImages = true;
    opt.fontType = SVGFontType.OUTLINEFONT;
    opt.coordinatePrecision = 3;
    opt.cssProperties = SVGCSSPropertyLocation.PRESENTATIONATTRIBUTES;
    opt.documentEncoding = SVGDocumentEncoding.UTF8;
    opt.DTD = SVGDTDVersion.SVG1_1;
    work.exportFile(svgFile, ExportType.SVG, opt);
  } finally {
    if (made) work.close(SaveOptions.DONOTSAVECHANGES);
  }
  svgFile.encoding = 'UTF-8'; svgFile.open('r'); var svg = svgFile.read(); svgFile.close(); svgFile.remove();
  var name = String(doc.name || 'logo').replace(/\.[^.]+$/, '');
  function q(s) {
    return '"' + String(s).replace(/\\/g, '\\\\').replace(/"/g, '\\"').replace(/\r/g, '\\r').replace(/\n/g, '\\n')
      .replace(/\u2028/g, '\\u2028').replace(/\u2029/g, '\\u2029').replace(/<\//g, '<\\/') + '"';
  }
  var data = 'window.DATA = {"file":' + q(name + '.svg') + ',"name":' + q(name) + ',"color":"#1F2937","svg":' + q(svg) + '};';
  var html = TEMPLATE.split('/*__DATA__*/').join(data);
  var out = new File(Folder.temp + '/logolab_' + name.replace(/[^A-Za-z0-9]+/g, '_') + '_' + stamp + '.html');
  out.encoding = 'UTF-8'; out.open('w'); out.write(html); out.close();
  if (!out.execute()) alert('Logo Lab: report saved to ' + out.fsName + ' — open it in your browser.');
})();
"""


def main():
    template = TEMPLATE.read_text(encoding="utf-8")
    jsx = JSX.replace("(function () {", "var TEMPLATE = " + json.dumps(template, ensure_ascii=True) + ";\n(function () {", 1)
    OUT.mkdir(exist_ok=True)
    (OUT / "LogoLab.jsx").write_text(jsx, encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Logo Lab for Adobe Illustrator\n\nRuns the Logo Lab on your selection. No AI, no account, nothing uploaded.\n\n"
        "## Use\n1. Select the logo (or nothing, to test everything on the artboard).\n"
        "2. **File → Scripts → Other Script…** and pick `LogoLab.jsx`.\n"
        "3. The report opens in your browser; the PDF and PNG buttons work as usual.\n\n"
        "To keep it in the **File → Scripts** menu, copy `LogoLab.jsx` into Illustrator's `Presets/<language>/Scripts` folder and restart Illustrator.\n",
        encoding="utf-8")
    print(f"Wrote {OUT / 'LogoLab.jsx'} ({len(jsx) // 1024} KB)")


if __name__ == "__main__":
    main()
