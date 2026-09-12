# CLIENT BRIEF — Automaton Power

## Company
Automaton Power — B2B contract manufacturer of lithium battery assemblies (Ukraine).
Site language: **Ukrainian**. Existing site: https://automatonpower.com.ua/ (being redesigned).

## Positioning (from `AutomatonPower _ Бриф.txt` — takes priority over the old site)
- Core direction: **contract manufacturing of battery assemblies from the customer's own cells and components**.
- Can additionally help with: cell procurement, design development, prototype manufacture, testing, launch of serial production.
- The three battery directions **remain relevant** — but they are directions, not a retail catalogue:
  - 21700 cells (cylindrical assemblies)
  - High-density batteries (pouch / high energy density)
  - Electric vehicle battery packs
- History: project formed around **2023**, starting with battery modules for electric transport and power systems; moved on to development and serial manufacture of assemblies for EW (РЕБ) systems, FPV drones, UAVs and other specialised equipment.
- Own equipment and processes for **incoming and final QC**: cell and assembly parameters, weld and solder joint quality, assembly correctness, voltage, internal resistance, load testing per spec.
- **No external certificates / patents.** Describe the internal QC system, inspection protocols, batch traceability, multi-stage control instead.
- MOQ: **the 100-unit figure must NOT appear on the site** — the client asked for it to be removed
  everywhere (2026-09-03). The brief originally said serial B2B orders from 100 batteries; the site now
  says only that volume is agreed per order and depends on complexity, configuration, components and
  whether new design work is needed. A pilot sample or test batch can be produced first.
  Removed from: page copy, the About stat row, the FAQ answer, spec tables, hero key figures,
  meta descriptions, `llms.txt`, and `eligibleQuantity` in the Organization and Product JSON-LD.
- Testimonials: anonymous only, no client names, no sensitive specs.
- Capacity claim carried over from the live site: **up to 500+ batteries / day**.

## Contacts
- Technical support: +380960562868
- Sales 01: +380677198474
- Sales 02: +380677198402
- The brief's original "менеджер 1 / менеджер 2" labels are superseded: the client gave roles
  (technical support / sales) on 2026-09-12 and added the third line. The two sales lines are
  labelled 01 and 02 on the site so two identical labels can't read as a duplicated row.
  Sales is the primary number: it is the `telephone` in the Organization JSON-LD and the one the
  quote form quotes when submission fails.
- Email: sales@automatonpower.com.ua

## Homepage structure (fixed, agreed with client)
1. Header
2. Hero
3. Battery types (links to individual pages)
4. Tasks we undertake
5. Call to action
6. About the company
7. Benefits
8. Workflow
9. Call to action
10. Gallery
11. FAQ
12. Feedback form
13. Contact details

Sub-pages (later, same template, only text + images differ): 21700 cells / High-density batteries / EV battery packs.

## Hero — type switcher
The old site's hero (full-bleed photo, four-line headline, paragraph, two buttons, pull-quote and a
static three-block strip) is **not** to be reproduced. The hero is a split card — text panel left,
product photo right — with a three-tab switcher across the base, modelled on the Enepaq reference.

**Headline is a fixed frame + a rotating noun phrase**, so the type name is the thing that animates:

> Серійне виробництво *(muted grey, static)*
> **акумуляторів 21700** / **батарей високої щільності** / **пакетів для EV** *(accent, rotating)*

All three read grammatically in the genitive after «виробництво». `пакетів для EV` is deliberately
short — the full «для електротранспорту» is spelled out in the tab beneath it.

Selecting a tab drives **five** things at once: the rotating word, the background photo (cross-fade),
the spec chip, the secondary link's href + label, and the active tab state.

| slide | word | image | link |
|---|---|---|---|
| 0 | акумуляторів 21700 | `hero.jpg` | `21700.html` |
| 1 | батарей високої щільності | `type-hd.jpg` | `high-density.html` |
| 2 | пакетів для EV | `type-ev.jpg` | `ev-packs.html` |

Implementation notes:
- Rotates every **7 s**; the active tab's top rule doubles as a progress bar (`@keyframes tabfill`,
  driven by the `--slide` custom property so the duration lives in one place).
- The bar's resting state must stay **empty** — it represents time actually elapsed on the slide.
  An earlier version rested at `scaleX(1)`, so any hold snapped it to full and it read as
  "countdown finished but nothing advanced". The active tab is marked by a faint track behind the
  fill, not by the fill itself.
- Holding is scoped to the **tab strip only**. The hero card covers the whole first screen, so
  holding on the card meant the pointer sat on it permanently and the slider never rotated.
- Holds pause rather than cancel: `left` keeps the unelapsed time and the bar freezes via
  `animation-play-state`, so releasing resumes mid-slide instead of restarting. Hold reasons live in
  a `Set` (`pointer` / `focus` / `hidden`) so overlapping holds can't unbalance each other.
- Tabs are real `<button role="tab">` in a `role="tablist"` with ←/→ key support. They **switch**
  rather than navigate — navigation stays on the panel's secondary link, which avoids nesting an
  anchor inside a button.
- The rotating line uses an invisible `.hero-swap-sizer` holding the longest string, with the three
  variants absolutely positioned over it. That keeps the box the height of the tallest variant at
  every viewport, so nothing jumps when the word changes or wraps.
- `prefers-reduced-motion` disables auto-rotation and the cross-fades; tabs still work on click.
- Below 520px the tab descriptions are hidden — titles + arrows only, so the strip stays compact.

## References
- `style.png` — **colours, fonts, content** (this is the current live site).
- `design.png` — **layout / design language** (Enepaq: rounded hero card, numbered product rows,
  image + text grid, two-tone headings, full-bleed CTA banner, large wordmark footer).

## Design tokens — client-specified palette
The client set: **background `#111111`, main text `#FFFFFF`, accent `#EF7F3D`**.

> The background was first specified as `#110600` and then changed to `#111111` — the warm
> near-black read as an orange tint across large areas. **Every dark in the file is now a neutral
> grey.** If a warm value creeps back in (`rgba(17,6,0,…)`, `#170A02`, a warm `--muted`, etc.) it
> will show as a tint on the big flat areas. Keep the darks neutral.

Pure white as the *main text colour* only works on dark surfaces, so the site is now **dark
throughout** — the former light (bone / greige) sections became warm dark panels. Section rhythm
comes from three surface tiers instead of light/dark flips.

| Token | Value | Role |
|---|---|---|
| `--ink` / `--ink2` / `--ink3` | `#111111` | **every** section background (client-specified) |
| `--surface` / `--greige` | `#111111` | kept as aliases so section classes still resolve |
| `--raised` | `#1A1A1A` | cards only — process steps |
| `--bone` | `#FFFFFF` | main text (client-specified) |
| `--accent` / `--accentd` | `#EF7F3D` | accent (client-specified) |
| `--muted` | `rgba(255,255,255,.34)` | the second line of two-tone headings |

The complete set of darks in the file, all neutral: `#0E0E0E` `#111111` `#141414` `#161616`
`#181818` `#1A1A1A` `#1E1E1E`. Plus `#FFFFFF`, `#EF7F3D` and `#F79457` (button hover).

### The background must stay flat — do not re-add atmosphere
The client explicitly asked for a **solid** background with no grain and no glow. Removed, and not
to be reintroduced:

- the fixed SVG `feTurbulence` grain overlay on `<body>`
- `.glowfield` — the large orange radial gradients in the types and form sections
- `.hairgrid` — the 12-column hairline overlay in the benefits section
- the warm radial behind the hero panel
- the orange bloom on `.btn-primary` and the brand mark
- the orange `mix-blend-mode: multiply` layers over the product photos
  (these also tinted the packs, which conflicts with the client's hard rule that batteries must
  look exactly as photographed)

All section backgrounds are now the same value — verified by sampling `#110600` at seven points
down the page. Section separation comes from hairlines and card borders only; `.ctaband` gained
top/bottom hairlines since it no longer differs by fill.

`--accentd` used to be a darkened orange for legibility on light panels. With no light panels left
it is simply the accent; keep them equal unless light sections come back. `--muted` is warm, not
neutral grey — plain white at low opacity reads cold against `#110600`.

Note: the product photos carry their own studio backdrop, which is lighter than `#110600`, so image
rectangles read as panels against the page. That is the photography, not a background artefact.

Type: **Onest** (display, heavy, tight tracking) + **IBM Plex Sans** (body) + **IBM Plex Mono** (section labels / numerals). All full Cyrillic.

Layout: every section is wrapped in `.wrap`, so the horizontal inset is controlled from exactly two
places — `--gut: clamp(16px,2.4vw,44px)` and `.wrap{max-width:1620px}`. Change those to retune the
side margins site-wide; `.rowitem::before` reads `--gut` so full-bleed row hovers follow automatically.

## Imagery
Source: `images automationPower/` (42 HEIC photos of real packs on a green cutting mat)
→ converted to `photos_jpg/` with `sips` (keep this folder — it is the working library for the sub-pages).

Processed with Gemini via `gen_images.sh` → `images/`: cutting mat, ruler, scale and clutter removed,
seamless dark charcoal studio backdrop, studio lighting, contact shadow, sharpening.
**The batteries themselves stay pixel-faithful** — no redesign, no colour change, no added or removed parts.

| Output | Source | Used for |
|---|---|---|
| `hero.jpg` | IMG_4055 | hero media panel |
| `hero-wide.jpg` | IMG_4055 (reframed 16:9) | og:image (was the hero before the split layout) |
| `cta-wide.jpg` | IMG_4034 (reframed 16:9) | CTA banner 06 |
| `type-21700.jpg` | IMG_4054 | type card 01 + gallery |
| `type-hd.jpg` | IMG_4006 | type card 02 |
| `type-ev.jpg` | IMG_4019 | type card 03 + gallery |
| `about.jpg` | IMG_4058 | about grid + gallery |
| `g1`–`g6.jpg` | 4008 / 4017 / 4010 / 4052 / 4013 / 4037 | gallery + about grid |
| `b1`–`b6.jpg` | 4053 / 4005 / 4029 / 4022 / 4038 / 4015 | benefits grid 04 (`gen_images2.sh`) |

`b3.jpg` is the one exception to "remove all background objects" — the digital scale is kept in frame
because it carries the QC meaning of that card.

| `hero-21700 / -hd / -ev.jpg` | tight re-crops of `hero` / `type-hd` / `type-ev` | hero slides |

Note: `--aspect` is ignored in Gemini **edit** mode — all edits come back 4:3. To get a wide frame,
run a second pass on the retouched file asking it to *extend the backdrop to the left* and place the
pack in the right third (this is how `hero-wide` / `cta-wide` were made).

### The hero media panel must stay at 4:3
The hero photos are 4:3 and the panel uses `object-fit: cover`, so **any mismatch between the
panel's aspect and 4:3 is cut straight off the pack** — and since the packs were re-cropped to fill
~90% of the frame, even a small mismatch clips the connector. It is not a crop that can be nudged
away with `object-position`.

Current geometry keeps them equal (measured: panel 1.339, image 1.339 → 0% crop):
- desktop `.hero-card` `min-height: clamp(520px,66vh,650px)` with columns `1.06fr / 1fr`
- mobile `.hero-media` `aspect-ratio: 4/3` (was 16/10, which cut 25% off the top and bottom)

If the card height, column ratio or panel padding changes, re-measure. `object-fit: contain` is
**not** a usable fallback here: the three photos' edge tones run from `#16181D` to `#45454A`, so
letterbox bars would show a seam against any single panel colour.

### Making a pack fill its frame
The retouched shots leave the pack fairly small inside a lot of empty backdrop. Two things do **not**
work: scaling up in CSS (only softens it), and asking Gemini to re-frame closer (it zooms ~10% per
pass, no matter how the prompt is worded). The working pipeline is:

1. `python3 crop_product.py in.jpg out.jpg [pad]` — finds the pack and crops to it in a 4:3 frame.
   It keys on **local edge energy**, not brightness: the backdrop carries a bright pool of light that
   a brightness threshold reads as product, whereas the backdrop is smooth and the pack is not.
2. Feed that crop back through Gemini with an *enhance-only* prompt (keep composition/crop/angle
   identical, raise resolution and micro-detail). This restores the ~1200×896 the crop gave up.

This is how the three hero slides were made; the same pass can be run on the type cards and gallery.

## Section headings — check with `node audit.mjs`
Section headings use `<br>` to set their intended line breaks, but several sit in narrow left
columns where each line then wraps *again* at the full `.h2` size. The display size is therefore
capped per block:

| Block | Cap |
|---|---|
| `.why-head .h2` (Переваги) | `clamp(28px,3.4vw,50px)` |
| `#about .h2` | `clamp(28px,3.2vw,52px)` |
| `#form .h2` | `clamp(26px,2.9vw,44px)` |

`audit.mjs` renders the page at eight widths and compares each heading's actual line count against
its intended one (`<br>` count + 1), flagging any that overflow. **Run it after changing any
column ratio, gutter or heading size** — currently 0 overflows at 390–1920px.

Note: the About heading's second half is 42 characters, which cannot fit one line at any sensible
section-heading size. It is deliberately broken into three lines rather than shrunk further.

## Navigation
The three battery-type pages are reachable from both navs:
- **Desktop** — «Акумулятори» is a dropdown (`.navdrop`) with the three pages, each an icon + name +
  one-line description. Opens on hover (CSS) and on click/keyboard (JS), closes on Escape or focusout.
  The panel carries its own `padding-top` so the hover path from button to card is unbroken.
- **Mobile** — full-screen panel (`.mnav`) modelled on the client's reference: brand + close X on top,
  «Акумулятори» expands to the same three items, then the section links, then the CTA.

Two traps worth remembering:
- **The panel must not live inside `<header>`.** The header gets a `transform` from the scroll
  handler, and a transformed ancestor becomes the containing block for `position: fixed` — so the
  panel sized itself to the 74px header instead of the viewport. It is now a sibling after `</header>`.
- Don't style the sub-items with bare element selectors (`.mnav-link span`). That also matches the
  icon wrapper and the text wrapper, which silently killed `.navico`'s `display:grid` and greyed the
  titles. The text block uses its own `.navtxt` class.

Opening the panel sets `body.nav-open{overflow:hidden}` to lock the page behind it.

## Product pages (21700 / high-density / EV)
Three pages built from one generator so they cannot drift apart:

    python3 build_pages.py        -> 21700.html, high-density.html, ev-packs.html
    node build_datasheets.mjs     -> datasheets/*.pdf

- `build_pages.py` lifts the `<style>` block straight out of `index.html`, so tokens, buttons,
  header and footer stay in sync with the home page automatically. Page-specific block CSS is
  appended after it. **Edit content in the `PAGES` dict, never in the generated HTML** — it is
  overwritten on every build.
- Every content block deliberately uses a *different* layout from its home-page counterpart:
  hero (image bleeds to the viewport edge), applications (columns split by vertical rules),
  specs (definition table + sticky download card), advantages (outlined numerals, no cards),
  gallery (asymmetric mosaic), FAQ (one wide accordion), form (bordered card), contacts (three cards).
- The mosaic is 3 columns with 6 items: the 2×2 hero tile plus 5 = 9 cells = exactly 3 full rows.
  At 4 columns the counts we have leave ragged empty cells.

### Datasheet PDFs
`build_datasheets.mjs` prints styled HTML through headless Chrome. That is deliberate — a
hand-rolled PDF would need a manually embedded TrueType font to render Cyrillic. The script reads
the spec rows out of the built pages, so the PDF can never disagree with the site. Re-run it after
changing any spec.

### Spec values need client sign-off
The tables list **parameter names and ranges, not invented numbers**. Anything order-dependent reads
«за ТЗ». Before launch the client should confirm: typical S/P range per direction, wire cross-section,
default connector, and whether capacity/voltage figures may be published.

### Icons: two traps
1. **Never style icon wrappers with bare element selectors.** `.pcont span` and `.nextcard span`
   also matched the icon `<span>` and the text wrapper — replacing `display:grid` with
   `display:block` (so `place-items:center` never ran and icons sat at the top of their box) and
   leaking the accent colour + uppercase onto the titles. The same trap hit `.mnav-link span`
   earlier. Give the text elements their own classes (`.navtxt`, `.pcont-role`, `.nextcard-kicker`).
2. **Icon ink must be normalised to the viewBox.** Hand-drawn 24×24 icons had ink off-centre by up
   to 1.5 units and max dimensions from 9.6 to 20.2, which reads as misalignment inside a bordered
   box. `node normalize_icons.mjs` measures each icon's real ink bbox in a browser and wraps it in a
   `<g transform="translate(...) scale(...)">` that centres it at (12,12) at a common size, with
   `stroke-width` divided by the same scale so line weight stays identical. **Re-run it after adding
   any icon**, then `python3 build_pages.py`.

## Discovery: SEO + AI answer engines
Run **after** `build_pages.py`:

    python3 build_pages.py
    python3 build_seo.py        # meta + JSON-LD on index, robots/sitemap/llms, image dimensions

`build_seo.py` scrapes the FAQ answers out of the built HTML and `build_pages.py` builds each
product page's schema from its own `PAGES` entry — so the structured data can never claim
something the visible page does not say. That is the thing both Google and AI answer engines
penalise, and it is why none of it is hand-written.

What is in place:
- **JSON-LD** — Organization + WebSite + WebPage + FAQPage + ItemList on the home page;
  WebPage + BreadcrumbList + Product (specs as `additionalProperty`) + FAQPage on each
  product page. All parse as valid JSON.
- **robots.txt** — names the AI crawlers explicitly (GPTBot, OAI-SearchBot, ClaudeBot,
  PerplexityBot, Google-Extended, Applebot-Extended, CCBot, meta-externalagent) rather than
  relying on the wildcard, plus the sitemap reference.
- **llms.txt** — plain-language summary for AI agents. It carries an explicit warning that
  the spec values are *parameters agreed per order*, not fixed product specifications, so an
  answer engine does not quote invented capacities.
- **sitemap.xml**, canonicals, Open Graph with absolute image URLs, Twitter cards, theme-color.

### Tailwind CDN removed
The markup used exactly **seven** Tailwind utilities. The CDN was a ~400KB render-blocking
script compiling CSS in the browser — delaying first paint and hiding layout from crawlers
that do not run JS. Those seven are now plain CSS (`.flex`, `.flex-wrap`, `.items-center`,
`.gap-3`, and the six step-progress widths as `:nth-child` rules). Product pages load in ~83ms
with no third-party JS. **Do not re-add Tailwind classes** — they will silently do nothing.

### `img{height:auto}` is load-bearing
Adding intrinsic `width`/`height` attributes made the About grid three times too tall. Those
attributes act as presentational hints, so with author CSS setting only `width:100%` the height
became **definite** (896px) and `aspect-ratio:1/1` was ignored. The base rule now carries
`height:auto`; rules that genuinely want a fixed height (`height:100%` with `object-fit`) set it
themselves and win on specificity. **Do not remove it** — any `aspect-ratio` image sized by width
alone will stretch to its full intrinsic height again.

### Image loading priority
`add_image_dims()` stamps intrinsic width/height (prevents layout shift) and sets priority by
role: `images/hero-*` load eagerly with `fetchpriority="high"` because the hero photo is the
LCP element; everything else is lazy. An earlier version keyed off document order and put the
high-priority hint on the header logo while lazy-loading the hero — which delays LCP rather
than improving it.

### serve.mjs MIME types
`.txt`, `.xml` and `.pdf` were falling through to `application/octet-stream`, so robots.txt
and sitemap.xml were served as downloads. Fixed in the MIME map.

## Forms → Telegram
All four forms post to one `send-form.php`, which forwards to Telegram. Setup steps are in
`TELEGRAM_SETUP.md`; the token lives in `config.php` (gitignored, never sent to the browser).

    browser -> send-form.php -> api.telegram.org
                     ^
                config.php (bot_token, chat_id)

Same structure as Петро Вікна / Богдан адвокат / DS motors, so it behaves the way the other
sites already do. Calling Telegram from client JS was not an option — the token would be
visible to every visitor, and whoever holds it controls the bot.

- The submit handler is **lifted out of `index.html` at build time** (`form_js` in
  `build_pages.py`, same mechanism as `shared_css`), so the product pages cannot drift.
- Each product page preselects its own type; the label written into Telegram comes from a
  **server-side dictionary**, so a crafted `type` value cannot inject text into the message.
- Honeypot field `website` returns a fake success — a bot gets no signal to retry.
- Per-IP rate limit, server-side revalidation, errors logged rather than echoed
  (Telegram API errors can quote the request).
- `api_base` config key (optional, defaults to `api.telegram.org`) allows a proxy where
  Telegram is blocked, and is what makes the delivery path testable.

**Requires PHP 7.4+ on the host.** The pages are static but this one script is not. On static
hosting (GitHub Pages, Netlify without functions) it will not run — port it to a serverless
function instead.

Verified before shipping, against a real PHP 8.2 (Docker) and a mock Telegram API: syntax,
selftest with and without config, 405 on GET, 422 with per-field flags, honeypot sending
nothing, happy path delivering the right chat_id and server-side type label, type injection
falling back to a dash, rate limit returning 429, plus a browser test submitting all four
forms and confirming four messages arrived with the correct type each.

### Deploy: `python3 build_deploy.py` verifies, never trust a silent copy
The first version was a shell script that read the asset list with `while read`. That drops
the **last line** of a file with no trailing newline — it shipped a `deploy/` missing exactly
one image (`images/type-hd.jpg`, last alphabetically) and reported success. The site went live
with a broken image.

`build_deploy.py` now derives the list from the pages itself (including absolute self-URLs in
Open Graph tags and JSON-LD, which a plain `src`/`href` scan misses) and **exits non-zero if
anything referenced is not in `deploy/`**. Do not replace it with a copy loop that cannot fail.

## Local tooling
- `serve.mjs` now honours `PORT` (another project already occupies 3000): `PORT=3400 node serve.mjs`
- `node_modules` is a symlink to `../DS motors/node_modules` for puppeteer — re-point or `npm i puppeteer` if it breaks.
- `node shot-mobile.mjs` captures a 390px mobile full-page shot. Keep `deviceScaleFactor: 1` —
  Chrome tiles (and duplicates) full-page captures taller than 16384px.
