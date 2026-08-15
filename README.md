# Automaton Power — website

Redesign of [automatonpower.com.ua](https://automatonpower.com.ua/) — a Ukrainian B2B contract
manufacturer of lithium battery assemblies for FPV, UAV, EW (РЕБ) and robotic systems.

Static site, Ukrainian language, no build step required to view.

## Pages

| File | Page |
|---|---|
| `index.html` | Home |
| `21700.html` | Елементи 21700 — cylindrical assemblies |
| `high-density.html` | Висока щільність — pouch assemblies |
| `ev-packs.html` | Пакети для електротранспорту — EV modules |

## Run locally

```bash
PORT=3400 node serve.mjs     # http://localhost:3400
```

`serve.mjs` honours `PORT` because port 3000 is often already taken.

## Regenerating things

The three product pages are **generated** — edit `build_pages.py`, not the HTML:

```bash
python3 build_pages.py        # -> 21700.html, high-density.html, ev-packs.html
node build_datasheets.mjs     # -> datasheets/*.pdf  (reads specs from the built pages)
node normalize_icons.mjs      # optically centres every icon; re-run after adding one
```

`build_pages.py` lifts the `<style>` block out of `index.html`, so design tokens, buttons,
header and footer stay in sync with the home page automatically.

## Images

Client photos in `images automationPower/` (HEIC) → `photos_jpg/` → retouched to `images/`
via the Gemini scripts (`gen_images*.sh`). The batteries are kept pixel-faithful — only the
background is replaced. `crop_product.py` re-crops a pack to fill its frame.

## Checks

```bash
node checklinks.mjs   # every link, anchor and image across all four pages
node audit.mjs        # section headings vs their intended line counts
node screenshot.mjs http://localhost:3400        # full-page screenshot
```

Requires `puppeteer` (see `node_modules`, gitignored — `npm i puppeteer`).

## Notes

`CLIENT_BRIEF.md` is the source of truth: positioning, palette, content decisions, and the
specific traps hit while building (why the background must stay flat, why icons need
normalising, which spec values still need client sign-off).
