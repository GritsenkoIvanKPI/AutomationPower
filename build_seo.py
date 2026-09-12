#!/usr/bin/env python3
"""
Adds the discovery layer: canonical/social meta, JSON-LD structured data, robots.txt,
sitemap.xml and llms.txt.

Structured data is generated FROM the page content (FAQ answers are scraped out of the
built HTML, product specs come from build_pages.py's PAGES dict), so the markup can never
claim something the visible page does not say — which is what both search engines and
AI answer engines penalise.

Run:  python3 build_seo.py     (after build_pages.py)
"""
import re, json, html, datetime, pathlib

SITE = "https://automatonpower.com.ua"
ORG_ID, SITE_ID = f"{SITE}/#organization", f"{SITE}/#website"
TODAY = datetime.date.today().isoformat()

PAGES = {
    "index.html":         ("/",                   "Automaton Power — контрактне виробництво акумуляторів"),
    "21700.html":         ("/21700.html",         "Акумуляторні збірки на елементах 21700"),
    "high-density.html":  ("/high-density.html",  "Акумулятори високої питомої енергії"),
    "ev-packs.html":      ("/ev-packs.html",      "Акумуляторні пакети для електротранспорту"),
}

def clean(t):
    t = re.sub(r"<[^>]+>", "", t)
    return html.unescape(re.sub(r"\s+", " ", t)).strip()

def faq_of(src):
    """Scrape the visible Q&A so the schema always matches what a reader sees."""
    qs = re.findall(r'<span class="(?:fq|q)">(.*?)</span>', src, re.S)
    ans = re.findall(r'<p class="(?:lead fans|a)">(.*?)</p>', src, re.S)
    return [{"@type": "Question", "name": clean(q),
             "acceptedAnswer": {"@type": "Answer", "text": clean(a)}}
            for q, a in zip(qs, ans)]

ORG = {
    "@type": "Organization", "@id": ORG_ID,
    "name": "Automaton Power",
    "alternateName": "Автоматон Пауер",
    "url": SITE + "/",
    "logo": {"@type": "ImageObject", "url": f"{SITE}/images/favicon-512.png", "width": 512, "height": 512},
    "image": f"{SITE}/images/hero-21700.jpg",
    "description": ("Контрактне виробництво літієвих акумуляторних збірок для FPV-дронів, БПЛА, "
                    "систем РЕБ та роботизованих комплексів. Виробництво з елементів замовника, "
                    "до 500+ акумуляторів на день."),
    "foundingDate": "2023",
    "email": "sales@automatonpower.com.ua",
    "telephone": "+380677198474",
    "address": {"@type": "PostalAddress", "addressCountry": "UA"},
    "areaServed": {"@type": "Country", "name": "Україна"},
    "knowsLanguage": ["uk"],
    "contactPoint": [
        {"@type": "ContactPoint", "telephone": "+380677198474", "contactType": "sales",
         "name": "Відділ продажу 01", "availableLanguage": ["uk"], "areaServed": "UA"},
        {"@type": "ContactPoint", "telephone": "+380677198402", "contactType": "sales",
         "name": "Відділ продажу 02", "availableLanguage": ["uk"], "areaServed": "UA"},
        {"@type": "ContactPoint", "telephone": "+380960562868", "contactType": "technical support",
         "name": "Технічна підтримка", "availableLanguage": ["uk"], "areaServed": "UA"},
        {"@type": "ContactPoint", "email": "sales@automatonpower.com.ua",
         "contactType": "customer support", "availableLanguage": ["uk"]},
    ],
    "makesOffer": {
        "@type": "Offer",
        "itemOffered": {
            "@type": "Service",
            "name": "Контрактне виробництво акумуляторних збірок",
            "serviceType": "Contract battery pack manufacturing",
            "provider": {"@id": ORG_ID},
            "areaServed": {"@type": "Country", "name": "Україна"},
        },
    },
}

WEBSITE = {"@type": "WebSite", "@id": SITE_ID, "url": SITE + "/", "name": "Automaton Power",
           "inLanguage": "uk", "publisher": {"@id": ORG_ID}}


def head_meta(path, title, img, page_type="website"):
    url = SITE + path
    return f"""<link rel="canonical" href="{url}">
<meta name="theme-color" content="#111111">
<meta name="color-scheme" content="dark">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:url" content="{url}">
<meta property="og:site_name" content="Automaton Power">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title, quote=True)}">
<meta name="twitter:image" content="{SITE}/{img}">"""


def inject(fname, blocks, meta):
    p = pathlib.Path(fname)
    s = p.read_text(encoding="utf-8")
    s = re.sub(r'\n?<link rel="canonical".*?<meta name="twitter:image"[^>]*>\n?', "\n", s, flags=re.S)
    s = re.sub(r'\n?<script type="application/ld\+json">.*?</script>', "", s, flags=re.S)
    # absolute og:image — several crawlers reject relative ones
    s = re.sub(r'(<meta property="og:image" content=")(?!https?:)([^"]+)', rf'\1{SITE}/\2', s)
    s = s.replace('<link rel="icon"', meta + '\n<link rel="icon"', 1)
    ld = '<script type="application/ld+json">\n' + json.dumps(
        {"@context": "https://schema.org", "@graph": blocks}, ensure_ascii=False, indent=1) + '\n</script>\n'
    s = s.replace("</head>", ld + "</head>", 1)
    p.write_text(s, encoding="utf-8")
    return len(blocks)



def add_image_dims(files):
    """Stamp intrinsic width/height on every <img>, and set loading priority by role.

    Without width/height the browser cannot reserve space, so every photo shifts the
    layout as it arrives (Cumulative Layout Shift).

    Priority matters as much as dimensions: the hero photo IS the Largest Contentful
    Paint element, so it must load eagerly at high priority. Lazy-loading an
    above-the-fold hero delays LCP instead of helping it.
      images/hero-*  -> eager, first one fetchpriority=high
      logo-mark      -> eager (header chrome, above the fold)
      everything else-> lazy
    """
    from PIL import Image
    stamped = 0
    for f in files:
        path = pathlib.Path(f)
        src = path.read_text(encoding="utf-8")
        state = {"hero_done": False}

        def fix(m):
            nonlocal stamped
            tag = m.group(0)
            srcm = re.search(r'src="([^"]+)"', tag)
            if not srcm or srcm.group(1).startswith("data:"):
                return tag
            # Third-party images (the Meta tracking pixel) must be left exactly as the
            # vendor wrote them — lazy-loading a tracking pixel can stop it firing at all.
            if srcm.group(1).startswith(("http://", "https://", "//")):
                return tag
            url = srcm.group(1)
            img = pathlib.Path(url)
            # re-runnable: clear previous hints before deciding again
            tag = re.sub(r'\s(?:loading|fetchpriority)="[^"]*"', "", tag)
            if img.exists() and "width=" not in tag:
                w, h = Image.open(img).size
                tag = tag.replace("<img", f'<img width="{w}" height="{h}"', 1)
                stamped += 1
            if "decoding=" not in tag:
                tag = tag.replace("<img", '<img decoding="async"', 1)

            is_hero = url.startswith("images/hero-")
            is_chrome = "logo-mark" in url
            if is_hero and not state["hero_done"]:
                tag = tag.replace("<img", '<img fetchpriority="high"', 1)
                state["hero_done"] = True
            elif not is_hero and not is_chrome:
                tag = tag.replace("<img", '<img loading="lazy"', 1)
            return tag

        src = re.sub(r"<img\b[^>]*>", fix, src)
        path.write_text(src, encoding="utf-8")
    print(f"images: {stamped} given width/height; heroes eager, rest lazy")


LLMS = """# Automaton Power

> Контрактне виробництво літієвих акумуляторних збірок в Україні.
> Серійне виготовлення з елементів та комплектуючих замовника для FPV-дронів, БПЛА,
> систем РЕБ, роботизованих комплексів і електротранспорту.

## Коротко / At a glance

- **Модель роботи:** контрактне виробництво (B2B). Виготовляємо за технічним завданням
  замовника, переважно з його елементів; за потреби допомагаємо із закупівлею,
  розробленням конструкції, виготовленням зразка й запуском серії.
- **Обсяг:** узгоджується індивідуально під виріб. Перед серією — дослідний зразок або тестова партія.
- **Виробнича спроможність:** до 500+ акумуляторів на день.
- **Працює з:** 2023 року (починали з модулів для електротранспорту та систем живлення).
- **Роздрібного продажу немає.**

## Напрями виробництва

- [Елементи 21700](%(site)s/21700.html) — циліндричні збірки, точкове зварювання,
  нікелеві та комбіновані нікель-мідні шини, конфігурація S/P за ТЗ (типово 3S–20S).
- [Акумулятори високої питомої енергії](%(site)s/high-density.html) — pouch-збірки,
  максимум енергії на одиницю ваги, для платформ де критична вага.
- [Пакети для електротранспорту](%(site)s/ev-packs.html) — модулі та пакети,
  геометрія корпусу, силові шини, захист і вихідні роз'єми за кресленням.

## Що входить у цикл

Підбір комплектуючих → зварювання та пайка → складання пакетів →
балансування та тестування → контроль якості → пакування та відправка.

## Контроль якості

Власне обладнання для вхідного й фінального контролю: параметри елементів і готових
збірок, якість зварних та паяних з'єднань, правильність монтажу, напруга, внутрішній
опір, робота під навантаженням за ТЗ. Партії комплектуючих не змішуються.
Зовнішніх сертифікатів компанія не має — контроль внутрішній.

## Важливо для точного цитування

Технічні характеристики на сайті — це **параметри та діапазони, що погоджуються за
технічним завданням**, а не фіксовані специфікації готового товару. Значення, позначені
«за ТЗ», розраховуються під конкретний виріб. Не приписуйте компанії конкретних
значень ємності, напруги чи ваги — вони визначаються замовленням.

## Контакти

- Відділ продажу: +380 67 719 84 74, +380 67 719 84 02
- Технічна підтримка: +380 96 056 28 68
- Email: sales@automatonpower.com.ua
- Сайт: %(site)s/
""" % {"site": SITE}

if __name__ == "__main__":
    src = pathlib.Path("index.html").read_text(encoding="utf-8")
    home_faq = faq_of(src)
    graph = [ORG, WEBSITE,
             {"@type": "WebPage", "@id": f"{SITE}/#webpage", "url": SITE + "/",
              "name": PAGES["index.html"][1], "isPartOf": {"@id": SITE_ID},
              "about": {"@id": ORG_ID}, "inLanguage": "uk"},
             {"@type": "FAQPage", "@id": f"{SITE}/#faq", "mainEntity": home_faq},
             {"@type": "ItemList", "@id": f"{SITE}/#directions",
              "name": "Напрями виробництва",
              "itemListElement": [
                  {"@type": "ListItem", "position": i + 1, "name": n, "url": SITE + u}
                  for i, (n, u) in enumerate([
                      ("Акумуляторні збірки на елементах 21700", "/21700.html"),
                      ("Акумулятори високої питомої енергії", "/high-density.html"),
                      ("Акумуляторні пакети для електротранспорту", "/ev-packs.html")])]}]
    n = inject("index.html", graph,
               head_meta("/", PAGES["index.html"][1], "images/hero-wide.jpg"))
    print(f"index.html: {n} schema blocks, {len(home_faq)} FAQ entries")

    # ---- robots.txt ----
    pathlib.Path("robots.txt").write_text(f"""# Automaton Power
# Search crawlers and AI answer engines are both welcome — the content is public
# marketing material and we want it quotable with attribution.

User-agent: *
Allow: /

# AI crawlers, named explicitly so their access does not depend on the wildcard
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-User
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: CCBot
Allow: /
User-agent: meta-externalagent
Allow: /

Sitemap: {SITE}/sitemap.xml
""", encoding="utf-8")

    # ---- sitemap.xml ----
    urls = "\n".join(
        f"  <url>\n    <loc>{SITE}{p}</loc>\n    <lastmod>{TODAY}</lastmod>\n"
        f"    <changefreq>monthly</changefreq>\n    <priority>{'1.0' if p == '/' else '0.8'}</priority>\n  </url>"
        for p, _ in PAGES.values())
    pathlib.Path("sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n',
        encoding="utf-8")
    pathlib.Path("llms.txt").write_text(LLMS, encoding="utf-8")
    add_image_dims(PAGES.keys())
    print("wrote robots.txt, sitemap.xml, llms.txt")
