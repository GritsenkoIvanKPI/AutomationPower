#!/usr/bin/env python3
"""
Build the three product pages: 21700.html, high-density.html, ev-packs.html

They share the home page's tokens, typography, buttons, header furniture and footer — the
stylesheet is lifted straight out of index.html at build time so the palette can never drift.
Everything below that is new: each content block on these pages uses a different layout from
its counterpart on the home page (see PAGE BLOCK CSS).

Run:  python3 build_pages.py
"""
import re, html

SRC = "index.html"
shared_css = re.search(r"<style>(.*?)</style>", open(SRC, encoding="utf-8").read(), re.S).group(1)

# ---------------------------------------------------------------- page-only block styles
PAGE_CSS = r"""
/* =========================================================================
   PRODUCT PAGE BLOCKS
   Deliberately different layouts from the home page:
     hero      – full-bleed image to the right edge (home: contained card + tab strip)
     apps      – columns divided by vertical rules (home: image cards)
     specs     – definition table + sticky download card (home: has no table)
     adv       – outlined numerals, no cards, no images (home: image cards / bordered cards)
     gallery   – asymmetric mosaic (home: uniform 4-column grid)
     faq       – single wide accordion (home: split heading + accordion)
     form      – bordered card (home: split with copy on the left)
     contacts  – three cards (home: stacked link rows)
   ========================================================================= */

/* ---------- breadcrumb ---------- */
.crumb{display:flex;flex-wrap:wrap;align-items:center;gap:9px;font-family:'IBM Plex Mono',monospace;
  font-size:10.5px;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.36)}
.crumb a{color:rgba(255,255,255,.6);text-decoration:none;transition:color .3s ease}
.crumb a:hover{color:var(--accent)}
.crumb a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.crumb i{width:4px;height:4px;background:rgba(255,255,255,.24);transform:rotate(45deg);flex:none}

/* ---------- hero ---------- */
.phero{position:relative;padding-top:74px;overflow:hidden}
/* the hero column is narrow, so the display size is capped to keep the <br> layout */
.phero h1{font-size:clamp(30px,3.9vw,54px)}
.phero-in{display:grid;grid-template-columns:1fr;gap:clamp(30px,4vw,56px);align-items:center;
  padding-top:clamp(34px,5vw,72px);padding-bottom:clamp(34px,5vw,64px)}
@media(min-width:1000px){.phero-in{grid-template-columns:1.02fr .98fr;gap:clamp(40px,4vw,72px)}}
.phero-media{position:relative;overflow:hidden;background:#0E0E0E;aspect-ratio:4/3}
.phero-media img{width:100%;height:100%;object-fit:cover;display:block}
@media(min-width:1000px){
  /* bleed the photo to the right edge of the viewport */
  /* Bleed to the viewport's right edge. `50% - 50vw` is the full-bleed trick for an
     element spanning a centred container — but this sits in the right grid COLUMN, so
     its 50% is half the column, not half the container, and it overshot the viewport by
     ~400px (a third of the image sat off-screen). Measure from the wrap's content edge. */
  .phero-media{margin-right:calc((min(1620px, 100vw) - 2 * var(--gut)) / 2 - 50vw);
    aspect-ratio:auto;height:clamp(420px,52vw,560px)}
}
.phero-tag{position:absolute;left:0;top:0;z-index:2;font-family:'IBM Plex Mono',monospace;
  font-size:10px;letter-spacing:.2em;padding:9px 13px;background:rgba(17,17,17,.66);
  backdrop-filter:blur(8px);border-right:1px solid var(--line-d);border-bottom:1px solid var(--line-d);
  color:var(--bone)}
.pkeys{display:grid;grid-template-columns:repeat(2,1fr);margin-top:clamp(30px,3.4vw,42px);
  border-top:1px solid var(--line-d)}
@media(min-width:760px){.pkeys{grid-template-columns:repeat(4,1fr)}}
.pkey{padding:18px 18px 18px 0;border-bottom:1px solid var(--line-d)}
@media(min-width:760px){
  .pkey{border-bottom:none;border-left:1px solid var(--line-d);padding-left:20px}
  .pkey:first-child{border-left:none;padding-left:0}
}
.pkey b{display:block;font-family:'Onest',sans-serif;font-weight:700;font-size:clamp(20px,2vw,27px);
  letter-spacing:-.03em;line-height:1;color:var(--accent)}
.pkey span{display:block;margin-top:9px;font-size:12px;line-height:1.5;color:var(--txt-d)}

/* ---------- applications: columns split by vertical rules ---------- */
.apps{display:grid;grid-template-columns:1fr;border-top:1px solid var(--line-d)}
.app{padding:30px 22px 34px 0;border-bottom:1px solid var(--line-d)}
/* six items: 2 cols on tablet, 3 cols x 2 rows on desktop. The left rule opens each
   column and the bottom rule closes each row, so the last row carries no bottom rule. */
@media(min-width:620px){
  .apps{grid-template-columns:repeat(2,1fr)}
  .app{border-left:1px solid var(--line-d);padding:30px clamp(16px,1.6vw,24px) 34px}
  .app:nth-child(2n+1){border-left:none;padding-left:0}
  .app:nth-last-child(-n+2){border-bottom:none}
}
@media(min-width:1080px){
  .apps{grid-template-columns:repeat(3,1fr)}
  .app:nth-child(n){border-left:1px solid var(--line-d);padding-left:clamp(16px,1.6vw,24px)}
  .app:nth-child(3n+1){border-left:none;padding-left:0}
  .app:nth-last-child(-n+3){border-bottom:none}
}
.app-ico{display:block;width:30px;height:30px;color:var(--accent);margin-bottom:22px;
  transition:transform .55s var(--ease)}
.app:hover .app-ico{transform:translateY(-3px)}
.app-ico svg{width:100%;height:100%;display:block}
.app h3{font-family:'Onest',sans-serif;font-weight:600;font-size:16.5px;line-height:1.25;
  letter-spacing:-.015em;margin:0}
.app p{margin:10px 0 0;font-size:13px;line-height:1.6;color:var(--txt-d)}

/* ---------- specifications ---------- */
.specs{display:grid;grid-template-columns:1fr;gap:clamp(32px,4vw,56px);align-items:start}
@media(min-width:1000px){.specs{grid-template-columns:1.55fr .85fr}}
.spec-table{border-top:1px solid var(--line-d)}
.spec-row{display:grid;grid-template-columns:1fr;gap:4px;padding:16px 0;
  border-bottom:1px solid var(--line-d);transition:background-color .4s ease}
@media(min-width:680px){.spec-row{grid-template-columns:minmax(190px,.85fr) 1.4fr;gap:24px;align-items:baseline}}
.spec-row:hover{background:rgba(255,255,255,.03)}
.spec-row dt{font-size:13.5px;color:var(--txt-d)}
.spec-row dd{margin:0;font-size:14.5px;line-height:1.6;color:var(--bone)}
.spec-note{margin-top:22px;font-size:12.5px;line-height:1.65;color:rgba(255,255,255,.42);max-width:70ch}
.dl-card{background:#181818;border:1px solid var(--line-d);padding:clamp(24px,2.4vw,32px)}
@media(min-width:1000px){.dl-card{position:sticky;top:104px}}
.dl-ico{width:44px;height:44px;display:grid;place-items:center;border:1px solid var(--line-d);
  background:#1A1A1A;color:var(--accent);margin-bottom:20px}
.dl-ico svg{width:22px;height:22px}
.dl-card h3{font-family:'Onest',sans-serif;font-weight:600;font-size:19px;letter-spacing:-.02em;margin:0}
.dl-card p{margin:12px 0 0;font-size:13px;line-height:1.65;color:var(--txt-d)}
.dl-meta{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 24px}
.dl-meta span{font-family:'IBM Plex Mono',monospace;font-size:10px;letter-spacing:.12em;
  padding:5px 9px;border:1px solid var(--line-d);color:rgba(255,255,255,.55)}
.dl-card .btn{width:100%;justify-content:center}

/* ---------- advantages: outlined numerals, no cards ---------- */
.adv{display:grid;grid-template-columns:1fr;gap:0}
@media(min-width:760px){.adv{grid-template-columns:repeat(2,1fr);column-gap:clamp(36px,4vw,72px)}}
.adv-item{display:grid;grid-template-columns:auto 1fr;gap:clamp(18px,2vw,28px);
  padding:26px 0;border-top:1px solid var(--line-d)}
.adv-no{font-family:'Onest',sans-serif;font-weight:800;font-size:clamp(30px,3vw,40px);
  line-height:.9;letter-spacing:-.05em;color:transparent;-webkit-text-stroke:1px rgba(239,127,61,.55);
  transition:-webkit-text-stroke-color .4s ease}
.adv-item:hover .adv-no{-webkit-text-stroke-color:var(--accent)}
.adv-item h3{font-family:'Onest',sans-serif;font-weight:600;font-size:17.5px;line-height:1.25;
  letter-spacing:-.015em;margin:0}
.adv-item p{margin:10px 0 0;font-size:13.5px;line-height:1.65;color:var(--txt-d)}

/* ---------- gallery: asymmetric mosaic ---------- */
.mosaic{display:grid;grid-template-columns:repeat(2,1fr);gap:clamp(10px,1.1vw,16px)}
@media(min-width:900px){.mosaic{grid-template-columns:repeat(3,1fr)}}
.mo{position:relative;overflow:hidden;background:#0E0E0E;margin:0;aspect-ratio:4/3}
@media(min-width:900px){.mo-lg{grid-column:span 2;grid-row:span 2;aspect-ratio:auto}}
.mo img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .9s var(--ease)}
.mo:hover img{transform:scale(1.06)}
.mo figcaption{position:absolute;left:14px;bottom:12px;z-index:2;font-family:'IBM Plex Mono',monospace;
  font-size:10px;letter-spacing:.14em;text-transform:uppercase;color:var(--bone);
  opacity:0;transform:translateY(8px);transition:opacity .5s ease,transform .5s var(--ease)}
.mo::after{content:'';position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(to top,rgba(17,17,17,.75),transparent 55%);opacity:0;transition:opacity .5s ease}
.mo:hover::after,.mo:hover figcaption{opacity:1}
.mo:hover figcaption{transform:translateY(0)}

/* ---------- faq: one wide accordion ---------- */
.pfaq{border-top:1px solid var(--line-d)}
.pfaq details{border-bottom:1px solid var(--line-d)}
.pfaq summary{list-style:none;cursor:pointer;display:grid;grid-template-columns:auto 1fr auto;
  gap:clamp(14px,2vw,28px);align-items:start;padding:24px 0}
.pfaq summary::-webkit-details-marker{display:none}
.pfaq summary:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.pfaq .q{font-family:'Onest',sans-serif;font-weight:600;font-size:clamp(15.5px,1.4vw,19px);
  line-height:1.3;letter-spacing:-.015em;transition:color .3s ease}
.pfaq summary:hover .q,.pfaq details[open] .q{color:var(--accent)}
.pfaq .sign{position:relative;width:15px;height:15px;flex:none;margin-top:4px}
.pfaq .sign::before,.pfaq .sign::after{content:'';position:absolute;background:var(--bone);
  transition:transform .5s var(--ease)}
.pfaq .sign::before{left:0;right:0;top:7px;height:1px}
.pfaq .sign::after{top:0;bottom:0;left:7px;width:1px}
.pfaq details[open] .sign::after{transform:scaleY(0)}
.pfaq .a{margin:0;padding:0 0 26px calc(clamp(14px,2vw,28px) + 26px);max-width:84ch;
  font-size:14.5px;line-height:1.75;color:var(--txt-d)}

/* ---------- form: bordered card ---------- */
.pform{background:#181818;border:1px solid var(--line-d);padding:clamp(26px,3.4vw,54px)}
.pform-head{display:grid;grid-template-columns:1fr;gap:16px;margin-bottom:clamp(26px,3vw,38px)}
@media(min-width:900px){.pform-head{grid-template-columns:1.1fr .9fr;gap:40px;align-items:end}}

/* ---------- contacts: three cards ---------- */
.pcont{display:grid;grid-template-columns:1fr;gap:clamp(14px,1.4vw,20px)}
@media(min-width:700px){.pcont{grid-template-columns:repeat(3,1fr)}}
.pcont a,.pcont div{display:block;background:#181818;border:1px solid var(--line-d);
  padding:clamp(22px,2.2vw,30px);text-decoration:none;color:var(--bone);
  transition:transform .5s var(--ease),border-color .4s ease}
.pcont a:hover{transform:translateY(-4px);border-color:rgba(239,127,61,.45)}
.pcont a:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.pcont-ico{width:38px;height:38px;display:grid;place-items:center;border:1px solid var(--line-d);
  background:#1A1A1A;color:var(--accent);margin-bottom:18px}
.pcont-ico svg{width:19px;height:19px}
.pcont b{display:block;font-family:'Onest',sans-serif;font-weight:600;font-size:clamp(15px,1.4vw,18px);
  letter-spacing:-.02em;line-height:1.3;color:var(--bone)}
.pcont-role{display:block;margin-top:8px;font-size:12.5px;color:var(--txt-d)}

/* ---------- next-direction strip ---------- */
.nextrow{display:grid;grid-template-columns:1fr;gap:clamp(14px,1.4vw,20px)}
@media(min-width:700px){.nextrow{grid-template-columns:repeat(2,1fr)}}
.nextcard{display:flex;align-items:center;justify-content:space-between;gap:18px;
  padding:24px clamp(20px,2vw,28px);background:#181818;border:1px solid var(--line-d);
  text-decoration:none;color:var(--bone);transition:transform .5s var(--ease),border-color .4s ease}
.nextcard:hover{transform:translateY(-4px);border-color:rgba(239,127,61,.45)}
.nextcard:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.nextcard b{display:block;margin-top:6px;font-family:'Onest',sans-serif;font-weight:600;font-size:16.5px;
  letter-spacing:-.02em;color:var(--bone);text-transform:none}
.nextcard-kicker{display:block;font-family:'IBM Plex Mono',monospace;font-size:10px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--accent)}
"""

# ---------------------------------------------------------------- icons
def svg(paths, sw="1.4"):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round">{paths}</svg>')

I = {
 "drone":   '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(1.2 1.2) scale(0.9)" stroke-width="1.556"><g transform="translate(1.2 1.2) scale(0.9)" stroke-width="1.556"><path d="M12 9.5h0"/><rect x="8.5" y="8.5" width="7" height="7" rx="1.6"/><path d="M8.5 10.5 5 7M15.5 10.5 19 7M8.5 13.5 5 17M15.5 13.5 19 17"/><circle cx="4" cy="6" r="2"/><circle cx="20" cy="6" r="2"/><circle cx="4" cy="18" r="2"/><circle cx="20" cy="18" r="2"/></g></g></g>',
 "uav":     '<g transform="translate(-0.001 -0.001) scale(1)" stroke-width="1.399"><g transform="translate(0.632 0.632) scale(0.947)" stroke-width="1.478"><g transform="translate(0.632 0.632) scale(0.947)" stroke-width="1.478"><path d="M2.5 13.5 12 4l9.5 9.5"/><path d="M12 4v16"/><path d="M7 20h10"/></g></g></g>',
 "ew":      '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0.096 0.096) scale(0.992)" stroke-width="1.411"><g transform="translate(0.096 0.096) scale(0.992)" stroke-width="1.411"><path d="M12 12h0"/><circle cx="12" cy="12" r="1.6"/><path d="M8.4 8.4a5 5 0 0 0 0 7.2M15.6 8.4a5 5 0 0 1 0 7.2"/><path d="M5.6 5.6a9 9 0 0 0 0 12.8M18.4 5.6a9 9 0 0 1 0 12.8"/></g></g></g>',
 "robot":   '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(-0.781 0.763) scale(1.065)" stroke-width="1.314"><g transform="translate(-0.781 0.763) scale(1.065)" stroke-width="1.314"><rect x="4" y="8" width="16" height="11" rx="2"/><path d="M12 8V4.5"/><circle cx="12" cy="3.5" r="1.4"/><path d="M9 12.5h.01M15 12.5h.01"/><path d="M9.5 16h5"/></g></g></g>',
 "power":   '<g transform="translate(0 0) scale(1)" stroke-width="1.401"><g transform="translate(-0.086 -0.343) scale(1.029)" stroke-width="1.361"><g transform="translate(-0.086 -0.343) scale(1.029)" stroke-width="1.361"><rect x="3" y="6.5" width="15" height="11" rx="2"/><path d="M18 10h2.5v4H18"/><path d="M9.5 9 7 12.5h3l-.5 2.5L13 11.5h-3z"/></g></g></g>',
 "scooter": '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0.132 -1.154) scale(0.989)" stroke-width="1.416"><g transform="translate(0.132 -1.154) scale(0.989)" stroke-width="1.416"><circle cx="5.5" cy="17.5" r="2.6"/><circle cx="18.5" cy="17.5" r="2.6"/><path d="M8 17.5h8"/><path d="M16.5 17.5 14 6.5h-2.5"/><path d="M18.5 15V9.5h-3"/></g></g></g>',
 "storage": '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0 0) scale(1)" stroke-width="1.4"><rect x="3" y="4" width="18" height="6" rx="1.4"/><rect x="3" y="14" width="18" height="6" rx="1.4"/><path d="M6.5 7h.01M6.5 17h.01"/></g></g></g>',
 "weight":  '<g transform="translate(-0.001 0.001) scale(1)" stroke-width="1.399"><g transform="translate(0.632 -0.553) scale(0.947)" stroke-width="1.478"><g transform="translate(0.632 -0.553) scale(0.947)" stroke-width="1.478"><path d="M2.5 18a9.5 9.5 0 0 1 19 0"/><path d="M12 18l5-5.5"/><path d="M2.5 18h19"/></g></g></g>',
 "range":   '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0 0) scale(1)" stroke-width="1.4"><path d="M3 12h4l3-7 4 14 3-7h4"/></g></g></g>',
 "shield":  '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0.261 0.261) scale(0.978)" stroke-width="1.431"><g transform="translate(0.261 0.261) scale(0.978)" stroke-width="1.431"><path d="M12 2.8 20 6v6.5c0 4.4-3.4 7.2-8 8.7-4.6-1.5-8-4.3-8-8.7V6z"/><path d="M9 12.2l2.2 2.2L15.4 10"/></g></g></g>',
 "pdf":     '<g transform="translate(0 -0.001) scale(1)" stroke-width="1.399"><g transform="translate(0.395 0.632) scale(0.947)" stroke-width="1.478"><g transform="translate(0.395 0.632) scale(0.947)" stroke-width="1.478"><path d="M6.5 2.5h7L18 7v14.5H6.5z"/><path d="M13.5 2.5V7H18"/><path d="M12 11v6"/><path d="M9.5 14.5 12 17l2.5-2.5"/></g></g></g>',
 "phone":   '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(-0.588 0.43) scale(1.028)" stroke-width="1.362"><g transform="translate(-0.588 0.43) scale(1.028)" stroke-width="1.362"><path d="M6.5 3h3l1.5 4-2 1.4a12 12 0 0 0 6.6 6.6L17 13l4 1.5v3a2 2 0 0 1-2.2 2A17.5 17.5 0 0 1 3.5 5.2 2 2 0 0 1 5.5 3z"/></g></g></g>',
 "gear":    '<g transform="translate(-1.5 -1.5) scale(1.125)" stroke-width="1.244"><path d="M4 6.5h9M17.5 6.5H20M4 12h3.5M12 12h8M4 17.5h9M17.5 17.5H20"/><circle cx="14.5" cy="6.5" r="2.2"/><circle cx="9.5" cy="12" r="2.2"/><circle cx="14.5" cy="17.5" r="2.2"/></g>',
 "mail":    '<g transform="translate(-0.001 -0.001) scale(1)" stroke-width="1.399"><g transform="translate(0.632 0.632) scale(0.947)" stroke-width="1.478"><g transform="translate(0.632 0.632) scale(0.947)" stroke-width="1.478"><rect x="2.5" y="5" width="19" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/></g></g></g>',
}

# ---------------------------------------------------------------- shared copy
PHONE1, PHONE2 = "+380 96 056 28 68", "+380 67 719 84 74"
TEL1, TEL2 = "+380960562868", "+380677198474"
MAIL = "sales@automatonpower.com.ua"

COMMON_FAQ = [
 ("Чи можемо ми передати власні елементи?",
  "Так. Основний формат — контрактне виробництво з сировини та комплектуючих замовника. Ви передаєте "
  "власні елементи живлення, а ми виконуємо вхідний контроль, складання, тестування та пакування готових збірок."),
 ("Який мінімальний обсяг замовлення?",
  "Серійні B2B-замовлення — від 100 акумуляторів. Перед запуском серії можемо виготовити дослідний зразок "
  "або тестову партію для перевірки конструкції та погодження характеристик. Мінімальна кількість залежить "
  "від складності виробу, конфігурації та необхідності розроблення нової конструкції."),
 ("Як ви контролюєте якість?",
  "На виробництві є власне обладнання та процеси для вхідного й фінального контролю. Перевіряються параметри "
  "елементів і готових збірок, якість зварних та паяних з’єднань, правильність монтажу, напруга, внутрішній "
  "опір і робота виробу під навантаженням відповідно до технічного завдання. Партії комплектуючих не "
  "змішуються та залишаються простежуваними."),
 ("Які терміни виробництва?",
  "Термін залежить від конфігурації, наявності комплектуючих та обсягу партії. Після отримання технічного "
  "завдання ми надаємо прорахунок і реалістичний виробничий графік."),
]

# ---------------------------------------------------------------- per-page content
PAGES = {}

PAGES["21700"] = dict(
 file="21700.html", tag="21700 · LI-ION",
 nav_title="Елементи 21700",
 title="Акумуляторні збірки на елементах 21700",
 title_br="Акумуляторні збірки<br>на елементах 21700",
 eyebrow="Напрям · Циліндричні збірки",
 lead="Контрактне виробництво циліндричних збірок за вашим технічним завданням — з ваших або наших "
      "елементів. Точкове зварювання, мідні та нікелеві шини, балансувальні виводи, конфігурація S/P "
      "під габарити й параметри вашої платформи.",
 meta="Контрактне виробництво акумуляторних збірок на циліндричних елементах 21700 для FPV, БПЛА, "
      "систем РЕБ та роботизованих комплексів. Серії від 100 шт.",
 hero_img="images/hero-21700.jpg",
 hero_alt="Акумуляторна збірка на циліндричних елементах 21700 з мідними та нікелевими шинами",
 keys=[("500+","акумуляторів на день"),("від 100","мінімальна серійна партія"),
       ("3S–20S","типові конфігурації"),("2×","вхідний і фінальний контроль")],
 apps_lead="Циліндричні збірки на 21700 — універсальний формат для платформ, де потрібні передбачувана "
           "геометрія, ремонтопридатність і стабільна віддача під навантаженням.",
 apps=[("drone","FPV-дрони","Компактні збірки під раму та потрібний політний час."),
       ("uav","БПЛА та розвідувальні платформи","Збірки підвищеної ємності для тривалих місій."),
       ("ew","Системи РЕБ","Живлення передавачів, антенних блоків і систем керування."),
       ("robot","Наземні роботи","Бортові та тягові збірки для роботизованих комплексів."),
       ("power","Станції живлення","Модулі для мобільних і стаціонарних систем живлення."),
       ("gear","Спеціалізоване обладнання","Збірки під нестандартні вироби за окремим технічним завданням.")],
 specs=[("Тип елементів","Циліндричні 21700, Li-ion"),
        ("Конфігурація","S/P за технічним завданням замовника"),
        ("Типові конфігурації","від 3S до 20S"),
        ("Міжелементні з’єднання","Точкове зварювання, нікелеві та комбіновані нікель-мідні шини"),
        ("Силові виводи","Пайка, силіконовий провід перерізом за ТЗ"),
        ("Балансування","Балансувальний шлейф із роз’ємом за специфікацією"),
        ("Вихідні роз’єми","XT30 / XT60 / XT90 або за специфікацією замовника"),
        ("Ізоляція та фіксація","Тримачі елементів, фіброскло, термоусадка, компаунд — за кресленням"),
        ("Контроль","Вхідний контроль елементів, напруга, внутрішній опір, робота під навантаженням"),
        ("Мінімальна партія","від 100 шт."),
        ("Виробнича спроможність","до 500+ акумуляторів на день")],
 adv=[("Конфігурація під ваш виріб","Розраховуємо S/P під габарити, напругу та струм платформи, а не навпаки."),
      ("Стабільна якість з’єднань","Контроль режиму зварювання та перевірка кожної шини перед складанням."),
      ("Робота з вашими елементами","Приймаємо елементи замовника й виконуємо вхідний контроль партії."),
      ("Простежуваність партій","Партії комплектуючих не змішуються на жодному етапі виробництва."),
      ("Від зразка до серії","Дослідний зразок, тестова партія, погодження характеристик, серійний випуск."),
      ("Швидка зміна конфігурацій","Нова геометрія або ємність без переналаштування вашої лінії.")],
 gallery=[("images/hero-21700.jpg","21700 / Pack"),
          ("images/p21-1.jpg","Fibreglass wrap"),
          ("images/p21-2.jpg","Spot weld"),
          ("images/p21-5.jpg","Busbar / Detail"),
          ("images/p21-3.jpg","Assembly"),
          ("images/p21-6.jpg","Cell array")],
 faq=[("Які конфігурації на 21700 ви збираєте?",
       "Конфігурацію S/P розраховуємо під ваше технічне завдання — типово від 3S до 20S. Погоджуємо напругу, "
       "струм, габарити, тип роз’ємів і вимоги до кріплення у вашому виробі."),
      ("Як виконуються з’єднання між елементами?",
       "Міжелементні з’єднання — точкове зварювання нікелевими та комбінованими нікель-мідними шинами з "
       "контролем режиму. Силові виводи та балансувальний шлейф — пайка з контролем нагріву й чистоти з’єднань.")],
)

PAGES["hd"] = dict(
 file="high-density.html", tag="POUCH · HIGH ENERGY",
 nav_title="Висока щільність",
 title="Акумулятори високої питомої енергії",
 title_br="Акумулятори високої<br>питомої енергії",
 eyebrow="Напрям · Pouch-збірки",
 lead="Збірки на pouch-елементах із максимальною енергією на одиницю ваги — для платформ, де критична "
      "кожна грама та кожна хвилина роботи. Компонування, ізоляція та захист розраховуємо під ваш виріб.",
 meta="Контрактне виробництво високощільних акумуляторних збірок на pouch-елементах для FPV, БПЛА та "
      "носимих комплексів. Серії від 100 шт.",
 hero_img="images/hero-hd.jpg",
 hero_alt="Високощільна акумуляторна збірка зі стосу pouch-елементів у сріблястій фользі",
 keys=[("500+","акумуляторів на день"),("від 100","мінімальна серійна партія"),
       ("Pouch","тип елементів"),("2×","вхідний і фінальний контроль")],
 apps_lead="Pouch-збірки застосовують там, де вага виробу прямо визначає дальність, тривалість роботи або "
           "корисне навантаження платформи.",
 apps=[("drone","FPV-дрони","Мінімальна вага збірки при потрібній віддачі."),
       ("range","Дрони дальньої дії","Максимальний запас енергії на одиницю ваги."),
       ("uav","Аеророзвідка","Тривалий час у повітрі для розвідувальних платформ."),
       ("shield","Носимі комплекси","Компактні збірки для переносного обладнання."),
       ("robot","Легкі платформи","Живлення для полегшених роботизованих систем."),
       ("ew","Системи РЕБ","Компактні збірки живлення для переносних станцій РЕБ.")],
 specs=[("Тип елементів","Pouch-елементи високої питомої енергії"),
        ("Конфігурація","S/P за технічним завданням замовника"),
        ("Компонування","Плоскі стеки з фіксацією та міжелементною ізоляцією"),
        ("Пріоритет конструкції","Максимальна енергія на одиницю ваги виробу"),
        ("Силові виводи","Пайка, силіконовий провід перерізом за ТЗ"),
        ("Балансування","Балансувальний шлейф із роз’ємом за специфікацією"),
        ("Вихідні роз’єми","XT30 / XT60 / XT90 або за специфікацією замовника"),
        ("Захист і фіксація","Демпферні прокладки, ізоляційні матеріали, термоусадка — за кресленням"),
        ("Контроль","Напруга, внутрішній опір, робота під навантаженням, контроль ваги збірки"),
        ("Мінімальна партія","від 100 шт."),
        ("Виробнича спроможність","до 500+ акумуляторів на день")],
 adv=[("Вага як проєктний параметр","Компонування підбираємо так, щоб зайва вага не потрапила у виріб."),
      ("Контроль ваги партії","Фіксуємо вагу готових збірок, щоб серія залишалася повторюваною."),
      ("Акуратне компонування","Щільне укладання стеку з ізоляцією та демпферами за кресленням."),
      ("Робота з вашими елементами","Приймаємо елементи замовника й виконуємо вхідний контроль партії."),
      ("Повторюваність серії","Однакова геометрія та параметри від партії до партії."),
      ("Від зразка до серії","Дослідний зразок, тестова партія, погодження характеристик, серійний випуск.")],
 gallery=[("images/hero-hd.jpg","Pouch / Stack"),
          ("images/phd-2.jpg","Foil edges"),
          ("images/type-hd.jpg","High density"),
          ("images/phd-1.jpg","Assembly"),
          ("images/phd-3.jpg","End face"),
          ("images/phd-4.jpg","Pouch / Yellow")],
 faq=[("Чим високощільні збірки відрізняються від циліндричних?",
       "Pouch-елементи дають більше енергії на одиницю ваги та дозволяють щільніше компонування у плоскому "
       "форматі. Циліндричні 21700 виграють у передбачуваній геометрії та ремонтопридатності. Вибір залежить "
       "від того, що критичніше для вашої платформи — вага чи конструктивна простота."),
      ("Чи контролюєте ви вагу готових збірок?",
       "Так. Для цього напряму вага — робочий параметр: ми фіксуємо її під час фінального контролю, щоб "
       "збірки в серії залишалися повторюваними за вагою та габаритами.")],
)

PAGES["ev"] = dict(
 file="ev-packs.html", tag="EV · МОДУЛІ",
 nav_title="Пакети для електротранспорту",
 title="Акумуляторні пакети для електротранспорту",
 title_br="Акумуляторні пакети<br>для електротранспорту",
 eyebrow="Напрям · EV-модулі",
 lead="Модулі та пакети для електротранспорту й систем живлення — від геометрії корпусу до силових шин, "
      "захисту та вихідних роз’ємів. Саме з цього напряму почалося виробництво Automaton Power у 2023 році.",
 meta="Контрактне виробництво акумуляторних модулів і пакетів для електротранспорту та систем живлення. "
      "Серії від 100 шт.",
 hero_img="images/hero-ev.jpg",
 hero_alt="Акумуляторний пакет для електротранспорту в синій термоусадці",
 keys=[("500+","акумуляторів на день"),("від 100","мінімальна серійна партія"),
       ("2023","досвід у напрямі з"),("2×","вхідний і фінальний контроль")],
 apps_lead="Модулі для електротранспорту — напрям, з якого компанія починала: акумуляторні модулі для "
           "електротранспорту та систем живлення.",
 apps=[("scooter","Електротранспорт","Тягові модулі для легкого електротранспорту."),
       ("power","Системи живлення","Модулі для стаціонарних і мобільних систем."),
       ("storage","Резервне живлення","Накопичувачі для безперебійного живлення."),
       ("robot","Наземні комплекси","Тягові збірки для роботизованих платформ."),
       ("weight","Спецобладнання","Пакети під нестандартні габарити та кріплення."),
       ("ew","Системи РЕБ","Модулі живлення для стаціонарних і мобільних комплексів РЕБ.")],
 specs=[("Тип елементів","Циліндричні або pouch — за технічним завданням"),
        ("Конфігурація","S/P за технічним завданням замовника"),
        ("Формат виробу","Модуль або готовий пакет у зборі"),
        ("Міжелементні з’єднання","Точкове зварювання, нікелеві та комбіновані нікель-мідні шини"),
        ("Силові шини та виводи","Переріз і тип виводів за ТЗ, пайка силових з’єднань"),
        ("Балансування","Балансувальний шлейф із роз’ємом за специфікацією"),
        ("Корпус і геометрія","Габарити, кріплення та вихід кабелів — за кресленням замовника"),
        ("Ізоляція та фіксація","Тримачі, ізоляційні матеріали, термоусадка, компаунд"),
        ("Контроль","Напруга, внутрішній опір, робота під навантаженням, перевірка монтажу"),
        ("Мінімальна партія","від 100 шт."),
        ("Виробнича спроможність","до 500+ акумуляторів на день")],
 adv=[("Досвід із напряму","Виробництво починалося саме з модулів для електротранспорту та систем живлення."),
      ("Геометрія під корпус","Габарити, кріплення та вихід кабелів підганяємо під ваш виріб."),
      ("Силова частина під навантаження","Переріз шин і виводів розраховуємо під робочі струми."),
      ("Робота з вашими елементами","Приймаємо елементи замовника й виконуємо вхідний контроль партії."),
      ("Контроль кожної партії","Напруга, внутрішній опір і робота під навантаженням за ТЗ."),
      ("Серійна повторюваність","Повторюваний виробничий цикл із фіксованими параметрами.")],
 gallery=[("images/hero-ev.jpg","EV / Module"),
          ("images/pev-2.jpg","Shrink / Blue"),
          ("images/pev-1.jpg","Module / Black"),
          ("images/g3.jpg","Pack"),
          ("images/pev-3.jpg","Weight control"),
          ("images/g2.jpg","Balance lead")],
 faq=[("Чи виготовляєте ви пакети під нестандартні габарити?",
       "Так. Геометрію пакета, кріплення та вихід кабелів погоджуємо за вашим кресленням. Якщо конструкції "
       "ще немає, можемо допомогти з її розробленням, виготовити зразок і після тестування запустити серію."),
      ("Чи можете ви допомогти із закупівлею елементів?",
       "Так. Базовий формат — виробництво з елементів замовника, але за потреби допомагаємо із закупівлею "
       "елементів і комплектуючих під погоджену специфікацію.")],
)

ORDER = ["21700", "hd", "ev"]

# ---------------------------------------------------------------- template pieces
def esc(t): return html.escape(t, quote=False)

ARW = ('<svg class="arw" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">'
       '<path d="M2 10 10 2M4 2h6v6" stroke="currentColor" stroke-width="1.4"/></svg>')

TYPE_ICONS = {
 "21700": '<g transform="translate(0 0.001) scale(1)" stroke-width="1.399"><g transform="translate(-0.857 -0.429) scale(1.071)" stroke-width="1.307"><g transform="translate(-0.857 -0.429) scale(1.071)" stroke-width="1.307"><ellipse cx="12" cy="6" rx="4.8" ry="2.5"/><path d="M7.2 6v11.5c0 1.4 2.15 2.5 4.8 2.5s4.8-1.1 4.8-2.5V6"/><path d="M9.6 3.2h4.8"/></g></g></g>',
 "hd":    '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0 0.2) scale(1)" stroke-width="1.4"><g transform="translate(0 0.2) scale(1)" stroke-width="1.4"><rect x="3" y="7.2" width="18" height="3" rx="1.1"/><rect x="3" y="11.6" width="18" height="3" rx="1.1"/><rect x="3" y="16" width="18" height="3" rx="1.1"/><path d="M6.5 7.2V4.6M17.5 7.2V4.6"/></g></g></g>',
 "ev":    '<g transform="translate(0 0) scale(1)" stroke-width="1.4"><g transform="translate(0.772 1.307) scale(0.891)" stroke-width="1.571"><g transform="translate(0.772 1.307) scale(0.891)" stroke-width="1.571"><rect x="2.5" y="6" width="19" height="12" rx="2"/><path d="M21.5 10.5h1.2v3h-1.2"/><path d="M13.4 8.6 10 13h2.6l-.7 3 3.4-4.4h-2.6z"/></g></g></g>',
}
TYPE_SUB = {"21700":"Циліндричні збірки на 21700","hd":"Pouch-збірки з максимумом енергії",
            "ev":"Модулі та пакети для EV"}

BRAND = """<a href="index.html" class="brand" aria-label="Automaton Power — на головну">
        <span class="brand-mk">
          <img src="images/logo-mark.png" alt="" width="38" height="38" decoding="async">
        </span>
        <span>
          <span class="brand-t">Automaton Power</span>
          <span class="brand-s">CONTRACT BATTERY MANUFACTURING</span>
        </span>
      </a>"""


def dropdown_links(cls):
    out = []
    for k in ORDER:
        p = PAGES[k]
        out.append(f'''<a class="{cls}" href="{p["file"]}">
            <span class="navico" aria-hidden="true">{svg(TYPE_ICONS[k])}</span>
            <span class="navtxt"><b>{esc(p["nav_title"])}</b><span>{esc(TYPE_SUB[k])}</span></span>
          </a>''')
    return "\n          ".join(out)


def header(cur):
    return f"""<header class="hdr" id="hdr">
  <div class="wrap hdr-in">
    {BRAND}

    <nav class="nav" aria-label="Головна навігація">
      <div class="navdrop" id="navdrop">
        <button class="navdrop-btn" id="navdropBtn" type="button" aria-expanded="false" aria-controls="navdropPanel">
          Акумулятори
          <svg class="navdrop-chev" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2 4.5 6 8.5l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </button>
        <div class="navdrop-panel" id="navdropPanel">
          <div class="navdrop-card">
          {dropdown_links("")}
          </div>
        </div>
      </div>
      <a href="#apps">Застосування</a>
      <a href="#specs">Характеристики</a>
      <a href="#gallery">Галерея</a>
      <a href="#faq">FAQ</a>
    </nav>

    <div class="flex items-center gap-3">
      <a href="#form" class="btn btn-primary hdr-cta">Отримати прорахунок {ARW}</a>
      <button class="burger" id="burger" aria-label="Меню" aria-expanded="false">
        <svg width="18" height="12" viewBox="0 0 18 12" fill="none" aria-hidden="true">
          <path d="M0 1h18M0 6h18M0 11h18" stroke="#FFFFFF" stroke-width="1.3"/>
        </svg>
      </button>
    </div>
  </div>
</header>

<div class="mnav" id="mmenu" role="dialog" aria-modal="true" aria-label="Меню">
  <div class="mnav-top">
    {BRAND}
    <button class="mnav-close" id="mnavClose" type="button" aria-label="Закрити меню">
      <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
        <path d="M2 2l12 12M14 2L2 14" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
      </svg>
    </button>
  </div>
  <div class="mnav-body">
    <button class="mnav-item" id="mnavGroup" type="button" aria-expanded="false" aria-controls="mnavSub">
      Акумулятори
      <svg class="mnav-chev" viewBox="0 0 12 12" fill="none" aria-hidden="true"><path d="M2 4.5 6 8.5l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
    </button>
    <div class="mnav-sub" id="mnavSub">
      {dropdown_links("mnav-link")}
    </div>
    <a class="mnav-item" href="#apps" data-close>Застосування</a>
    <a class="mnav-item" href="#specs" data-close>Характеристики</a>
    <a class="mnav-item" href="#gallery" data-close>Галерея</a>
    <a class="mnav-item" href="#faq" data-close>FAQ</a>
    <a href="#form" class="btn btn-primary mnav-cta" data-close>Отримати прорахунок {ARW}</a>
  </div>
</div>"""


FOOTER = f"""<footer class="ftr">
  <div class="wrap ftr-in">
    <div class="ftr-top">
      {BRAND}
      <nav class="ftr-nav" aria-label="Футер">
        <a href="index.html" class="tlink tlink-mute">Головна</a>
        <a href="21700.html" class="tlink tlink-mute">Елементи 21700</a>
        <a href="high-density.html" class="tlink tlink-mute">Високої щільності</a>
        <a href="ev-packs.html" class="tlink tlink-mute">Пакети для EV</a>
        <a href="index.html#form" class="tlink tlink-mute">Прорахунок</a>
      </nav>
    </div>

    <svg class="wordmark" viewBox="0 0 1000 108" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
      <text x="500" y="86" font-size="106" text-anchor="middle" textLength="990" lengthAdjust="spacingAndGlyphs">AUTOMATON POWER</text>
    </svg>

    <div class="ftr-bot">
      <p class="micro">© 2026 Automaton Power. B2B виробництво.</p>
      <p class="micro">Контрактне виробництво акумуляторних збірок для FPV, БПЛА та роботизованих систем.</p>
    </div>
  </div>
</footer>"""


SCRIPT = """<script>
const io = new IntersectionObserver((es) => {
  es.forEach(e => { if (e.isIntersecting) { e.target.classList.add('visible'); io.unobserve(e.target); } });
}, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

const hdr = document.getElementById('hdr');
let last = 0;
addEventListener('scroll', () => {
  const y = scrollY;
  hdr.style.transform = (y > 420 && y > last) ? 'translateY(-100%)' : 'translateY(0)';
  last = y;
}, { passive: true });

const burger = document.getElementById('burger');
const mmenu  = document.getElementById('mmenu');
const mclose = document.getElementById('mnavClose');
const mgroup = document.getElementById('mnavGroup');
const msub   = document.getElementById('mnavSub');
const setMenu = (open) => {
  mmenu.classList.toggle('open', open);
  burger.setAttribute('aria-expanded', String(open));
  document.body.classList.toggle('nav-open', open);
  if (open) mclose.focus(); else burger.focus();
};
burger.addEventListener('click', () => setMenu(true));
mclose.addEventListener('click', () => setMenu(false));
mmenu.querySelectorAll('[data-close], .mnav-link').forEach(el =>
  el.addEventListener('click', () => setMenu(false)));
mgroup.addEventListener('click', () => {
  const open = msub.classList.toggle('open');
  mgroup.setAttribute('aria-expanded', String(open));
});

const drop = document.getElementById('navdrop');
const dropBtn = document.getElementById('navdropBtn');
const setDrop = (open) => {
  drop.classList.toggle('open', open);
  dropBtn.setAttribute('aria-expanded', String(open));
};
dropBtn.addEventListener('click', () => setDrop(!drop.classList.contains('open')));
drop.addEventListener('focusout', e => { if (!drop.contains(e.relatedTarget)) setDrop(false); });

addEventListener('keydown', e => {
  if (e.key !== 'Escape') return;
  if (mmenu.classList.contains('open')) setMenu(false);
  if (drop.classList.contains('open')) setDrop(false);
});

document.querySelectorAll('.pfaq details').forEach(d => {
  d.addEventListener('toggle', () => {
    if (d.open) document.querySelectorAll('.pfaq details').forEach(o => { if (o !== d) o.open = false; });
  });
});

document.getElementById('quote').addEventListener('submit', e => {
  e.preventDefault();
  const f = e.target;
  if (!f.checkValidity()) { f.reportValidity(); return; }
  document.getElementById('formmsg').classList.add('show');
  f.reset();
});
</script>"""


SITE = "https://automatonpower.com.ua"
ORG_ID = f"{SITE}/#organization"


def seo_head(key, p):
    """Canonical/social meta plus a JSON-LD graph generated from this page's own content,
    so the structured data can never claim something the visible page does not say."""
    import json as _json
    url = f"{SITE}/{p['file']}"
    img = f"{SITE}/{p['hero_img']}"
    faq = p["faq"] + COMMON_FAQ
    graph = [
        {"@type": "WebPage", "@id": url + "#webpage", "url": url,
         "name": p["title"], "description": p["meta"], "inLanguage": "uk",
         "isPartOf": {"@id": f"{SITE}/#website"}, "about": {"@id": url + "#product"}},
        {"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Головна", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": "Акумулятори", "item": SITE + "/#types"},
            {"@type": "ListItem", "position": 3, "name": p["nav_title"]}]},
        {"@type": "Product", "@id": url + "#product",
         "name": p["title"], "description": p["meta"], "image": img,
         "category": "Акумуляторні збірки",
         "brand": {"@id": ORG_ID}, "manufacturer": {"@id": ORG_ID},
         "additionalProperty": [
             {"@type": "PropertyValue", "name": k, "value": v} for k, v in p["specs"]],
         "offers": {"@type": "Offer", "availability": "https://schema.org/InStock",
                    "priceCurrency": "UAH",
                    "priceSpecification": {"@type": "PriceSpecification",
                                           "description": "Ціна за технічним завданням"},
                    "eligibleQuantity": {"@type": "QuantitativeValue", "minValue": 100,
                                         "unitText": "шт."},
                    "seller": {"@id": ORG_ID}, "url": url}},
        {"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]},
    ]
    ld = _json.dumps({"@context": "https://schema.org", "@graph": graph},
                     ensure_ascii=False, indent=1)
    return f"""<link rel="canonical" href="{url}">
<meta name="theme-color" content="#111111">
<meta name="color-scheme" content="dark">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Automaton Power">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(p['title'])} — Automaton Power">
<meta name="twitter:description" content="{esc(p['meta'])}">
<meta name="twitter:image" content="{img}">
<script type="application/ld+json">
{ld}
</script>"""


def build(key):
    p = PAGES[key]
    others = [k for k in ORDER if k != key]

    keys = "\n      ".join(
        f'<div class="pkey"><b>{esc(b)}</b><span>{esc(s)}</span></div>' for b, s in p["keys"])

    apps = "\n      ".join(
        f'''<article class="app">
        <span class="app-ico" aria-hidden="true">{svg(I[ic])}</span>
        <h3>{esc(t)}</h3><p>{esc(d)}</p>
      </article>''' for ic, t, d in p["apps"])

    specs = "\n        ".join(
        f'<div class="spec-row"><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k, v in p["specs"])

    adv = "\n      ".join(
        f'''<article class="adv-item">
        <span class="adv-no" aria-hidden="true">{i:02d}</span>
        <div><h3>{esc(t)}</h3><p>{esc(d)}</p></div>
      </article>''' for i, (t, d) in enumerate(p["adv"], 1))

    gal = []
    for i, (src, cap) in enumerate(p["gallery"]):
        cls = "mo mo-lg" if i == 0 else "mo"
        gal.append(f'<figure class="{cls}"><img src="{src}" alt="{esc(cap)} — {esc(p["nav_title"])}" '
                   f'loading="lazy"><figcaption>{esc(cap)}</figcaption></figure>')
    gal = "\n      ".join(gal)

    faq_items = p["faq"] + COMMON_FAQ
    faq = "\n      ".join(
        f'''<details{" open" if i == 0 else ""}>
        <summary><span class="mono-n">{i+1:02d}</span><span class="q">{esc(q)}</span><span class="sign"></span></summary>
        <p class="a">{esc(a)}</p>
      </details>''' for i, (q, a) in enumerate(faq_items))

    nxt = "\n      ".join(
        f'''<a class="nextcard" href="{PAGES[k]["file"]}">
        <span><span class="nextcard-kicker">Інший напрям</span><b>{esc(PAGES[k]["nav_title"])}</b></span>
        {ARW}
      </a>''' for k in others)

    pdf = f'datasheets/automaton-power-{key}.pdf'

    return f"""<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(p["title"])} — Automaton Power</title>
<meta name="description" content="{esc(p["meta"])}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(p["title"])} — Automaton Power">
<meta property="og:description" content="{esc(p["meta"])}">
<meta property="og:image" content="{SITE}/{p["hero_img"]}">
<meta property="og:locale" content="uk_UA">
{seo_head(key, p)}
<link rel="icon" type="image/png" sizes="32x32" href="images/favicon-32.png">
<link rel="apple-touch-icon" href="images/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Onest:wght@400;500;600;700;800;900&family=IBM+Plex+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{shared_css}{PAGE_CSS}</style>
</head>
<body>

{header(key)}

<main id="top">

<!-- ============ HERO ============ -->
<section class="phero">
  <div class="wrap phero-in">
    <div class="reveal">
      <nav class="crumb" aria-label="Хлібні крихти">
        <a href="index.html#types">Акумулятори</a><i></i>
        <span>{esc(p["nav_title"])}</span>
      </nav>
      <p class="eyebrow mt-3">{esc(p["eyebrow"])}</p>
      <h1 class="h1 mt-3">{p["title_br"]}</h1>
      <p class="lead mt-4">{esc(p["lead"])}</p>
      <div class="flex flex-wrap gap-3 mt-5">
        <a href="#form" class="btn btn-primary">Отримати прорахунок {ARW}</a>
        <a href="#specs" class="btn btn-ghost">Технічні характеристики</a>
      </div>
    </div>
    <div class="phero-media reveal d2">
      <span class="phero-tag">{esc(p["tag"])}</span>
      <img src="{p["hero_img"]}" alt="{esc(p["hero_alt"])}">
    </div>
  </div>
  <div class="wrap">
    <div class="pkeys reveal d3">
      {keys}
    </div>
  </div>
</section>

<!-- ============ APPLICATIONS ============ -->
<section class="sec sec-ink" id="apps">
  <div class="wrap">
    <div class="sechead">
      <div class="reveal">
        <p class="eyebrow">Застосування</p>
        <h2 class="h2 two-tone mt-3">Для чого<br><em>використовується</em></h2>
      </div>
      <p class="lead reveal d1">{esc(p["apps_lead"])}</p>
    </div>
    <div class="apps mt-6 reveal d2">
      {apps}
    </div>
  </div>
</section>

<!-- ============ SPECIFICATIONS ============ -->
<section class="sec sec-ink" id="specs">
  <div class="wrap">
    <div class="sechead">
      <div class="reveal">
        <p class="eyebrow">Характеристики</p>
        <h2 class="h2 two-tone mt-3">Технічні<br><em>характеристики</em></h2>
      </div>
      <p class="lead reveal d1">Параметри, які погоджуються за вашим технічним завданням перед запуском
        дослідного зразка та серії.</p>
    </div>

    <div class="specs mt-6">
      <div class="reveal d1">
        <dl class="spec-table">
        {specs}
        </dl>
        <p class="spec-note">Значення, позначені «за ТЗ», розраховуються під конкретний виріб: габарити,
          робочі струми, тип роз’ємів і вимоги до кріплення погоджуються до запуску зразка.</p>
      </div>

      <aside class="dl-card reveal d2">
        <span class="dl-ico" aria-hidden="true">{svg(I["pdf"])}</span>
        <h3>Специфікація у PDF</h3>
        <p>Повний перелік параметрів напряму одним файлом — зручно передати інженеру або
          додати до технічного завдання.</p>
        <div class="dl-meta"><span>PDF</span><span>A4</span><span>UA</span></div>
        <a class="btn btn-primary" href="{pdf}" download>Завантажити PDF {ARW}</a>
      </aside>
    </div>
  </div>
</section>

<!-- ============ ADVANTAGES ============ -->
<section class="sec sec-ink" id="advantages">
  <div class="wrap">
    <div class="sechead">
      <div class="reveal">
        <p class="eyebrow">Переваги</p>
        <h2 class="h2 two-tone mt-3">Що ви отримуєте<br><em>з цим напрямом</em></h2>
      </div>
      <p class="lead reveal d1">Контрактне виробництво під технічне завдання замовника — з контролем
        якості на кожному етапі та готовністю масштабувати обсяг.</p>
    </div>
    <div class="adv mt-6 reveal d2">
      {adv}
    </div>
  </div>
</section>

<!-- ============ GALLERY ============ -->
<section class="sec sec-ink" id="gallery">
  <div class="wrap">
    <div class="sechead">
      <div class="reveal">
        <p class="eyebrow">Галерея</p>
        <h2 class="h2 two-tone mt-3">Вироби<br><em>цього напряму</em></h2>
      </div>
      <p class="lead reveal d1">Реальні збірки з наших виробничих партій. Конфігурацію та зовнішній
        вигляд конкретного виробу погоджуємо за вашим технічним завданням.</p>
    </div>
    <div class="mosaic mt-6 reveal d2">
      {gal}
    </div>
  </div>
</section>

<!-- ============ FAQ ============ -->
<section class="sec sec-ink" id="faq">
  <div class="wrap">
    <div class="reveal">
      <p class="eyebrow">FAQ</p>
      <h2 class="h2 two-tone mt-3">Питання щодо<br><em>цього напряму</em></h2>
    </div>
    <div class="pfaq mt-6 reveal d1">
      {faq}
    </div>
  </div>
</section>

<!-- ============ FORM ============ -->
<section class="sec sec-ink" id="form">
  <div class="wrap">
    <div class="pform reveal">
      <div class="pform-head">
        <div>
          <p class="eyebrow">Заявка</p>
          <h2 class="h2 mt-3">Прорахунок за вашим ТЗ</h2>
        </div>
        <p class="lead">Опишіть виріб і орієнтовний обсяг. Заявка буде надіслана безпосередньо
          менеджеру Automaton Power.</p>
      </div>

      <form id="quote" novalidate>
        <div class="fgrid">
          <label class="field"><span>Ім’я *</span><input type="text" name="name" required placeholder="Як до вас звертатися"></label>
          <label class="field"><span>Телефон *</span><input type="tel" name="phone" required placeholder="+380 __ ___ __ __"></label>
          <label class="field"><span>Email *</span><input type="email" name="email" required placeholder="you@company.com"></label>
          <label class="field"><span>Тип виробу</span>
            <select name="type">
              <option{" selected" if key == "21700" else ""}>Елементи 21700</option>
              <option{" selected" if key == "hd" else ""}>Акумулятори високої щільності</option>
              <option{" selected" if key == "ev" else ""}>Пакети для електротранспорту</option>
              <option>Інше / потрібна консультація</option>
            </select>
          </label>
          <label class="field fspan"><span>Коментар або ТЗ</span>
            <textarea name="comment" placeholder="Конфігурація, елементи, геометрія, конектори, строки"></textarea></label>
        </div>
        <div class="fsubmit">
          <button type="submit" class="btn btn-primary">Надіслати заявку {ARW}</button>
          <p class="micro mw-44">Надсилаючи форму, ви погоджуєтесь на обробку контактних даних
            для підготовки прорахунку.</p>
        </div>
        <p class="body-s fmsg" id="formmsg">Дякуємо. Заявку надіслано — менеджер зв’яжеться з вами найближчим часом.</p>
      </form>
    </div>
  </div>
</section>

<!-- ============ CONTACTS ============ -->
<section class="sec sec-tight sec-ink" id="contacts">
  <div class="wrap">
    <div class="sechead">
      <div class="reveal">
        <p class="eyebrow">Контакти</p>
        <h2 class="h2 two-tone mt-3">Звʼяжіться<br><em>напряму</em></h2>
      </div>
      <p class="lead reveal d1">B2B, Україна. Серії від 100 шт., без роздрібного продажу.</p>
    </div>

    <div class="pcont mt-6 reveal d2">
      <a href="tel:{TEL1}">
        <span class="pcont-ico" aria-hidden="true">{svg(I["phone"])}</span>
        <b>{PHONE1}</b><span class="pcont-role">Менеджер 01</span>
      </a>
      <a href="tel:{TEL2}">
        <span class="pcont-ico" aria-hidden="true">{svg(I["phone"])}</span>
        <b>{PHONE2}</b><span class="pcont-role">Менеджер 02</span>
      </a>
      <a href="mailto:{MAIL}">
        <span class="pcont-ico" aria-hidden="true">{svg(I["mail"])}</span>
        <b>{MAIL}</b><span class="pcont-role">Email</span>
      </a>
    </div>

    <div class="nextrow mt-6 reveal d3">
      {nxt}
    </div>
  </div>
</section>

</main>

{FOOTER}

{SCRIPT}
</body>
</html>
"""


if __name__ == "__main__":
    for k in ORDER:
        out = PAGES[k]["file"]
        open(out, "w", encoding="utf-8").write(build(k))
        print(f"built {out}")
