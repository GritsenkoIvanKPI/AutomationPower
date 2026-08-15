#!/bin/bash
# Third batch: tighter re-framing of the three hero slides.
# The packs sat small inside a lot of empty backdrop — this recomposes them to fill the frame
# at full resolution, instead of scaling up in CSS (which only softens them).

GEN="/Users/ivan/Downloads/Клод сайти/google-image-gen-api-starter-main копія"
OUT="/Users/ivan/Downloads/Клод сайти/AutomationPower/images"

RULE="CRITICAL RULE: the battery pack must remain absolutely identical to the source photo — exact same shape, proportions, viewing angle, colours, wrapping material and texture, seams, number and layout of cells, welded strips, wires, balance lead and connector. Do not redesign it, do not stylize it, do not add or remove any component, do not change its colour or its orientation. ONLY change the framing: compose much closer so the battery pack fills roughly 85 percent of the frame width, with just a small even margin of seamless dark charcoal studio backdrop around it. Keep the same studio lighting direction, the same soft contact shadow and the same subtle vignette. Maximum sharpness and micro-detail on the cells, welds and wrapping. Ultra-realistic commercial product photography, 4K, no text, no watermark."

gen () {
  if [ -f "$OUT/$2" ]; then echo "skip $2"; return; fi
  echo ">>> $2"
  (cd "$GEN" && uv run python main.py "$OUT/$2" "$3 $RULE" --edit "$OUT/$1" --aspect 4:3 2>&1 | tail -1)
}

gen "hero.jpg"     "hero-21700.jpg" "Tightly framed hero product shot of this exact battery pack: a block of green 21700 cylindrical cells with red insulator rings, copper and nickel welded busbar strips across the top, dark green fibreglass wrap around the sides, red and black silicone wires with a yellow XT connector."
gen "type-hd.jpg"  "hero-hd.jpg"    "Tightly framed hero product shot of this exact high-density battery pack: stacked silver aluminium-foil pouch cells with visible layered foil edges, black wrap at the front, red and black wires with a yellow XT connector and a white balance lead."
gen "type-ev.jpg"  "hero-ev.jpg"    "Tightly framed hero product shot of this exact battery pack: a rectangular block sealed in glossy blue heat-shrink wrap with rounded edges, red and black silicone wires and a white balance connector emerging from one end, yellow XT connector."

echo "DONE"
