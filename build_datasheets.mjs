// Renders one A4 PDF datasheet per product direction.
// Built by printing styled HTML through headless Chrome, so Cyrillic embeds properly —
// hand-rolling a PDF would need a manually embedded TrueType font for the same result.
//
// Run:  node build_datasheets.mjs        (reads specs straight out of the built pages)
import puppeteer from 'puppeteer';
import fs from 'fs';
import path from 'path';

const PAGES = [
  { key: '21700', file: '21700.html', title: 'Акумуляторні збірки на елементах 21700', tag: '21700 · Li-ion' },
  { key: 'hd',    file: 'high-density.html', title: 'Акумулятори високої питомої енергії', tag: 'Pouch · High energy' },
  { key: 'ev',    file: 'ev-packs.html', title: 'Акумуляторні пакети для електротранспорту', tag: 'EV · Модулі' },
];

const OUT = 'datasheets';
fs.mkdirSync(OUT, { recursive: true });

// pull the spec rows out of the generated page so the PDF can never disagree with the site
const specsOf = (file) => {
  const html = fs.readFileSync(file, 'utf8');
  const block = html.slice(html.indexOf('<dl class="spec-table">'), html.indexOf('</dl>'));
  return [...block.matchAll(/<dt>(.*?)<\/dt><dd>(.*?)<\/dd>/g)].map(m => [m[1], m[2]]);
};

const sheet = (p, rows) => `<!DOCTYPE html><html lang="uk"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;600;700;800&family=IBM+Plex+Sans:wght@300;400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *{box-sizing:border-box}
  @page{size:A4;margin:0}
  body{margin:0;background:#111111;color:#fff;font-family:'IBM Plex Sans',sans-serif;font-weight:300;
       -webkit-print-color-adjust:exact;print-color-adjust:exact}
  .pg{width:210mm;min-height:297mm;padding:18mm 16mm 14mm;display:flex;flex-direction:column}
  .top{display:flex;align-items:center;justify-content:space-between;gap:12mm;
       padding-bottom:6mm;border-bottom:1px solid rgba(255,255,255,.15)}
  .bd{display:flex;align-items:center;gap:3.5mm}
  .mk{width:9mm;height:9mm;display:grid;place-items:center;background:#1C1C1C;border:1px solid rgba(239,127,61,.45)}
  .nm{display:block;font-family:'Onest',sans-serif;font-weight:700;font-size:11pt;letter-spacing:-.02em;line-height:1}
  .sb{display:block;font-family:'IBM Plex Mono',monospace;font-size:5.4pt;letter-spacing:.2em;color:rgba(255,255,255,.45);margin-top:1.5mm}
  .tag{font-family:'IBM Plex Mono',monospace;font-size:6.6pt;letter-spacing:.18em;text-transform:uppercase;
       color:#EF7F3D;border:1px solid rgba(239,127,61,.4);padding:2mm 3.5mm}
  h1{font-family:'Onest',sans-serif;font-weight:800;font-size:23pt;line-height:1.05;letter-spacing:-.035em;
     margin:10mm 0 0;max-width:150mm}
  .lead{font-size:9pt;line-height:1.6;color:rgba(255,255,255,.66);margin:5mm 0 0;max-width:150mm}
  .lbl{font-family:'IBM Plex Mono',monospace;font-size:6.6pt;letter-spacing:.2em;text-transform:uppercase;
       color:#EF7F3D;margin:11mm 0 4mm}
  table{width:100%;border-collapse:collapse}
  td{padding:3.1mm 0;border-bottom:1px solid rgba(255,255,255,.12);vertical-align:top;font-size:8.6pt;line-height:1.45}
  td.k{width:52mm;color:rgba(255,255,255,.6);padding-right:6mm}
  td.v{color:#fff}
  .note{font-size:7.2pt;line-height:1.6;color:rgba(255,255,255,.42);margin-top:5mm}
  .foot{margin-top:auto;padding-top:6mm;border-top:1px solid rgba(255,255,255,.15);
        display:flex;justify-content:space-between;gap:8mm;font-size:7.4pt;color:rgba(255,255,255,.55)}
  .foot b{color:#fff;font-weight:500}
</style></head><body><div class="pg">
  <div class="top">
    <div class="bd">
      <span class="mk"><svg width="13" height="13" viewBox="0 0 24 24"><path d="M13.6 2 4 13.6h6.1L9.3 22 20 10.4h-6.4L13.6 2Z" fill="#EF7F3D"/></svg></span>
      <span><span class="nm">Automaton Power</span><span class="sb">CONTRACT BATTERY MANUFACTURING</span></span>
    </div>
    <span class="tag">${p.tag}</span>
  </div>

  <h1>${p.title}</h1>
  <p class="lead">Контрактне виробництво акумуляторних збірок за технічним завданням замовника —
     з ваших або наших елементів. Серії від 100 шт., виробнича спроможність до 500+ акумуляторів на день.</p>

  <p class="lbl">Технічні характеристики</p>
  <table>${rows.map(([k, v]) => `<tr><td class="k">${k}</td><td class="v">${v}</td></tr>`).join('')}</table>
  <p class="note">Значення, позначені «за ТЗ», розраховуються під конкретний виріб: габарити, робочі струми,
     тип роз’ємів і вимоги до кріплення погоджуються до запуску дослідного зразка.</p>

  <div class="foot">
    <span><b>+380 96 056 28 68</b> · <b>+380 67 719 84 74</b></span>
    <span><b>sales@automatonpower.com.ua</b> · automatonpower.com.ua</span>
  </div>
</div></body></html>`;

const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox'] });
for (const p of PAGES) {
  const rows = specsOf(p.file);
  const page = await browser.newPage();
  await page.setContent(sheet(p, rows), { waitUntil: 'networkidle0' });
  const out = path.join(OUT, `automaton-power-${p.key}.pdf`);
  await page.pdf({ path: out, format: 'A4', printBackground: true,
                   margin: { top: 0, right: 0, bottom: 0, left: 0 } });
  await page.close();
  console.log(`${out}  (${rows.length} spec rows, ${(fs.statSync(out).size / 1024).toFixed(0)} KB)`);
}
await browser.close();
