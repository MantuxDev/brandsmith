#!/usr/bin/env python3
"""Build the Logo Lab Figma plugin from the Lab template.

  python3 tools/build_figma_plugin.py            → figma-plugin/{manifest.json, code.js, ui.html}

Install (Figma desktop app, no terminal): Plugins → Development → Import plugin from manifest… → pick
figma-plugin/manifest.json. Select a frame, group, component or vector and run "Logo Lab".
The plugin exports the selection as SVG inside Figma and analyses it locally; nothing leaves the machine.
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "skills" / "brandsmith" / "templates" / "logo-lab.html"
OUT = ROOT / "figma-plugin"

CODE_JS = r"""// Logo Lab for Figma: sends the current selection to the Lab UI as SVG.
figma.showUI(__html__, { width: 1180, height: 820, themeColors: true, title: 'Logo Lab' });

async function sendSelection() {
  const sel = figma.currentPage.selection;
  if (!sel.length) { figma.ui.postMessage({ type: 'empty' }); return; }
  const node = sel.length === 1 ? sel[0] : null;
  if (!node || !('exportAsync' in node)) { figma.ui.postMessage({ type: 'multi' }); return; }
  try {
    const bytes = await node.exportAsync({ format: 'SVG', svgOutlineText: true, svgIdAttribute: false, svgSimplifyStroke: true });
    figma.ui.postMessage({ type: 'svg', name: node.name, bytes });
  } catch (e) {
    figma.ui.postMessage({ type: 'error', message: String(e) });
  }
}

figma.on('selectionchange', () => sendSelection());
figma.ui.onmessage = msg => {
  if (msg.type === 'refresh') sendSelection();
  if (msg.type === 'notify') figma.notify(msg.text);
};
sendSelection();
"""

BRIDGE = r"""
// ---- Figma bridge ----
window.FIGMA = true;
document.querySelector('label[for=open]').hidden = true;
(function () {
  const hint = (title, sub) => { $('#nav').innerHTML = ''; $('#pdf').disabled = true; $('#fname').textContent = '';
    $('#main').innerHTML = `<section class="drop"><h1>${title}</h1><p>${sub}</p></section>`; };
  const msgs = { en: ['Select your logo on the canvas', 'Select one frame, group, component or vector. The Lab analyses it as SVG, with text outlined. Nothing leaves Figma.', 'Select a single layer', 'Group the parts of the logo, or select its frame.'],
                 it: ['Seleziona il logo sulla tela', 'Seleziona un solo frame, gruppo, componente o vettore. Il Lab lo analizza come SVG, con i testi vettorializzati. Nulla esce da Figma.', 'Seleziona un solo livello', 'Raggruppa le parti del logo, oppure seleziona il suo frame.'] };
  window.onmessage = e => { const m = e.data && e.data.pluginMessage; if (!m) return; const L = msgs[LANG] || msgs.en;
    if (m.type === 'svg') { const text = new TextDecoder().decode(new Uint8Array(m.bytes)); loadSvgText(text, (m.name || 'selection') + '.svg', false); }
    else if (m.type === 'empty') hint(L[0], L[1]);
    else if (m.type === 'multi') hint(L[2], L[3]);
    else if (m.type === 'error') toast(m.message); };
})();
"""


def main():
    s = TEMPLATE.read_text(encoding="utf-8")
    # no network inside the plugin: drop web fonts (the CSS has full fallback stacks)
    s = "\n".join(l for l in s.splitlines() if "fonts.googleapis.com" not in l)
    s = s.replace("/*__DATA__*/", "window.DATA = null;", 1)
    s = s.replace("if (DATA) start(); else showDrop();", BRIDGE + "\nshowDrop = function () {}; $('#main').innerHTML = '';\nparent.postMessage({ pluginMessage: { type: 'refresh' } }, '*');", 1)
    OUT.mkdir(exist_ok=True)
    (OUT / "ui.html").write_text(s, encoding="utf-8")
    (OUT / "code.js").write_text(CODE_JS, encoding="utf-8")
    manifest = {"name": "Logo Lab", "id": "logo-lab-brandsmith", "api": "1.0.0", "main": "code.js", "ui": "ui.html",
                "editorType": ["figma"], "documentAccess": "dynamic-page", "networkAccess": {"allowedDomains": ["none"]}}
    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    (OUT / "README.md").write_text(
        "# Logo Lab for Figma\n\nRuns the Logo Lab checks on the selected layer, inside Figma. No AI, no account, nothing uploaded.\n\n"
        "## Install (Figma desktop app)\n1. Download this `figma-plugin` folder.\n2. In Figma: **Plugins → Development → Import plugin from manifest…** and pick `manifest.json`.\n"
        "3. Select your logo (one frame, group, component or vector) and run **Plugins → Development → Logo Lab**.\n\n"
        "The Lab updates when you change the selection. Text is outlined on export, so wordmarks are measured as drawn.\n"
        "The PDF report and PNG kit buttons work as in the browser version.\n", encoding="utf-8")
    print(f"Wrote {OUT}/manifest.json, code.js, ui.html, README.md")


if __name__ == "__main__":
    main()
