#!/bin/bash
# Second batch: images for the redesigned "Переваги" grid (design.png "Why Enepaq" pattern).
# Same rule as batch 1 — the battery stays pixel-faithful, only the environment changes.

GEN="/Users/ivan/Downloads/Клод сайти/google-image-gen-api-starter-main копія"
SRC="/Users/ivan/Downloads/Клод сайти/AutomationPower/photos_jpg"
OUT="/Users/ivan/Downloads/Клод сайти/AutomationPower/images"

RULE="CRITICAL RULE: the battery pack must remain absolutely identical to the source photo — exact same shape, proportions, dimensions, colours, wrapping material and texture, seams, number and layout of cells, welded strips, wires, balance lead and connector. Do not redesign it, do not stylize it, do not add or remove any component, do not change its colour. ONLY change the environment: completely remove the green cutting mat, the metal ruler, papers and every other background object, and place the pack on a seamless dark charcoal studio backdrop with a soft subtle vignette gradient. Add clean professional studio lighting with a soft realistic contact shadow beneath the pack, improve sharpness, micro-detail and colour accuracy. Ultra-realistic commercial product photography, 4K, no text, no watermark."

gen () {
  if [ -f "$OUT/$2" ]; then echo "skip $2"; return; fi
  echo ">>> $2"
  (cd "$GEN" && uv run python main.py "$OUT/$2" "$3 $RULE" --edit "$SRC/$1" --aspect 4:3 2>&1 | tail -1)
}

gen "IMG_4053.jpg"     "b1.jpg" "Product shot of this exact battery assembly: a wide flat rectangular array of many green 21700 cylindrical cells with red insulator rings in a black holder, joined by welded nickel strips, viewed from a low three-quarter angle, red and black wires with a white balance lead at the right end."
gen "IMG_4005 (1).jpg" "b2.jpg" "Product shot of these exact high-density battery cells: a block of stacked silver aluminium-foil pouch cells with visible layered foil edges, black tape binding, red and black wires with a yellow XT connector at the right end, viewed from a low angle along the stack."
gen "IMG_4022.jpg"     "b4.jpg" "Product shot of this exact battery pack: a compact upright block sealed in glossy blue heat-shrink wrap, grey foam pad on the top face, red and black wires with a white balance connector rising from the top, standing vertically."
gen "IMG_4038 (2).jpg" "b5.jpg" "Product shot of this exact battery assembly: a block of green 21700 cylindrical cells partly wrapped in dark green fibreglass insulation with the cell bodies exposed along the open side, grey foam pad on the end face, red and black wires exiting to the left."
gen "IMG_4015.jpg"     "b6.jpg" "Product shot of this exact battery pack: a rectangular block in glossy black heat-shrink wrap with a grey foam pad on the visible end face, a bundle of red and black silicone wires and a fine multi-wire balance harness exiting the end, three-quarter angle."

# QC image — here the digital scale is meaningful, so it stays in frame.
if [ ! -f "$OUT/b3.jpg" ]; then
echo ">>> b3.jpg"
(cd "$GEN" && uv run python main.py "$OUT/b3.jpg" "Product shot of this exact battery pack being weighed: a rectangular pack in glossy black heat-shrink wrap with red and black wires and a yellow XT connector, resting on a small black digital kitchen-style scale whose LCD shows a weight reading. CRITICAL RULE: keep the battery pack and the digital scale absolutely identical to the source photo — same shape, proportions, colours, wrapping, wires and connector, same scale and its display. Do not redesign or add or remove any component. ONLY change the environment: remove the green cutting mat, the metal ruler and all other background clutter, and place the pack and scale on a seamless dark charcoal studio backdrop with a soft vignette. Add clean professional studio lighting, a soft realistic contact shadow, and improve sharpness and colour accuracy. Ultra-realistic commercial product photography, 4K, no watermark." --edit "$SRC/IMG_4029.jpg" --aspect 4:3 2>&1 | tail -1)
fi

echo "DONE"
