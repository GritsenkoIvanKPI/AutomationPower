// Optically align every drawn icon.
//
// The icons were authored by hand on a 24x24 grid, so their ink sat wherever the paths
// happened to fall — off-centre by up to 1.5 units and ranging from 9.6 to 20.2 units in
// max dimension. Inside a fixed-size bordered box that reads as misalignment.
//
// This measures each icon's real ink bounding box in a browser, then wraps its contents in
// a <g> that centres the ink at (12,12) and scales it to a common optical size. The group's
// stroke-width is divided by the same scale, so line weight stays identical across icons.
//
// Run:  node normalize_icons.mjs        (then: python3 build_pages.py)
import puppeteer from 'puppeteer';
import fs from 'fs';

const TARGET = 18;          // max ink dimension, in viewBox units
const BASE_STROKE = 1.4;
const SVG_OPEN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round">';

const round = (n) => +n.toFixed(3);

// ---- collect every icon we want normalised -------------------------------------------
const jobs = [];   // {id, inner, where}

// a) the generator's icon dictionaries (I = {...} and TYPE_ICONS = {...})
let gen = fs.readFileSync('build_pages.py', 'utf8');
const dictRe = /^(I|TYPE_ICONS) = \{([\s\S]*?)^\}/gm;
const genEntries = [];
for (const d of gen.matchAll(dictRe)) {
  const body = d[2];
  // entries look like:  "key": '<path .../>' possibly continued over lines
  for (const e of body.matchAll(/^\s*"([\w]+)":\s*((?:'[^']*'\s*\n?\s*)+),?\s*$/gm)) {
    const inner = [...e[2].matchAll(/'([^']*)'/g)].map(m => m[1]).join('');
    if (!inner.includes('<')) continue;
    genEntries.push({ dict: d[1], key: e[1], raw: e[2].trim(), inner });
  }
}
genEntries.forEach((g, i) => jobs.push({ id: `gen${i}`, inner: g.inner }));

// b) index.html's inline 24x24 icons (process cards + nav type icons)
let idx = fs.readFileSync('index.html', 'utf8');
const inlineRe = new RegExp(SVG_OPEN.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '([\\s\\S]*?)<\\/svg>', 'g');
const inlines = [...idx.matchAll(inlineRe)].map(m => m[1]);
const uniqueInline = [...new Set(inlines)];
uniqueInline.forEach((inner, i) => jobs.push({ id: `idx${i}`, inner }));

console.log(`measuring ${genEntries.length} generator icons + ${uniqueInline.length} inline icons`);

// ---- measure ink bounding boxes --------------------------------------------------------
const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
const page = await browser.newPage();
await page.setContent(`<body style="margin:0">${jobs.map(j =>
  `<svg id="${j.id}" viewBox="0 0 24 24" width="240" height="240" fill="none" stroke="#000" stroke-width="1.4">${j.inner}</svg>`
).join('')}</body>`);

const boxes = await page.evaluate((ids) => {
  const out = {};
  for (const id of ids) {
    const svg = document.getElementById(id);
    let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
    for (const c of svg.children) {
      let bb; try { bb = c.getBBox(); } catch (e) { continue; }
      if (!bb.width && !bb.height) {          // zero-size (a dot drawn as a 0-length path)
        x0 = Math.min(x0, bb.x); y0 = Math.min(y0, bb.y);
        x1 = Math.max(x1, bb.x); y1 = Math.max(y1, bb.y); continue;
      }
      x0 = Math.min(x0, bb.x); y0 = Math.min(y0, bb.y);
      x1 = Math.max(x1, bb.x + bb.width); y1 = Math.max(y1, bb.y + bb.height);
    }
    out[id] = { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, w: x1 - x0, h: y1 - y0 };
  }
  return out;
}, jobs.map(j => j.id));
await browser.close();

// ---- build the wrapper for each icon ----------------------------------------------------
const wrap = (inner, bb) => {
  const s = TARGET / Math.max(bb.w, bb.h);
  const tx = round(12 - s * bb.cx);
  const ty = round(12 - s * bb.cy);
  const sw = round(BASE_STROKE / s);
  return `<g transform="translate(${tx} ${ty}) scale(${round(s)})" stroke-width="${sw}">${inner}</g>`;
};

// a) rewrite the generator's dict values
let changedGen = 0;
for (let i = genEntries.length - 1; i >= 0; i--) {
  const g = genEntries[i];
  const bb = boxes[`gen${i}`];
  if (!bb || !isFinite(bb.w) || bb.w <= 0) continue;
  const out = wrap(g.inner, bb).replace(/'/g, "\\'");
  gen = gen.replace(g.raw, `'${out}'`);
  changedGen++;
}
fs.writeFileSync('build_pages.py', gen);

// b) rewrite index.html's inline icons
let changedIdx = 0;
uniqueInline.forEach((inner, i) => {
  const bb = boxes[`idx${i}`];
  if (!bb || !isFinite(bb.w) || bb.w <= 0) return;
  const from = SVG_OPEN + inner + '</svg>';
  const to = SVG_OPEN + wrap(inner, bb) + '</svg>';
  let n = 0;
  while (idx.includes(from)) { idx = idx.replace(from, to); n++; }
  changedIdx += n;
});
fs.writeFileSync('index.html', idx);

console.log(`normalised ${changedGen} generator icons, ${changedIdx} inline icon instances`);
console.log(`all ink now centred at (12,12) with max dimension ${TARGET}`);
