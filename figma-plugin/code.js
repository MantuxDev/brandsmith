// Logo Lab for Figma: sends the current selection to the Lab UI as SVG.
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
