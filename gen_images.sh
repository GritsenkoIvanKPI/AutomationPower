#!/bin/bash
# Batch retouch of Automaton Power product photos via Gemini.
# Rule: the battery itself must stay pixel-faithful — only the environment changes.

GEN="/Users/ivan/Downloads/Клод сайти/google-image-gen-api-starter-main копія"
SRC="/Users/ivan/Downloads/Клод сайти/AutomationPower/photos_jpg"
OUT="/Users/ivan/Downloads/Клод сайти/AutomationPower/images"
mkdir -p "$OUT"

RULE="CRITICAL RULE: the battery pack must remain absolutely identical to the source photo — exact same shape, proportions, dimensions, colours, wrapping material and texture, seams, number and layout of cells, welded strips, wires, balance lead and connector. Do not redesign it, do not stylize it, do not add or remove any component, do not change its colour. ONLY change the environment: completely remove the green cutting mat, the metal ruler, the scale, papers and every other background object, and place the pack on a seamless dark charcoal studio backdrop with a soft subtle vignette gradient. Add clean professional studio lighting with a soft realistic contact shadow beneath the pack, improve sharpness, micro-detail and colour accuracy. Ultra-realistic commercial product photography, 4K, no text, no watermark."

gen () { # $1=src $2=out $3=aspect $4=subject
  if [ -f "$OUT/$2" ]; then echo "skip $2"; return; fi
  echo ">>> $2"
  (cd "$GEN" && uv run python main.py "$OUT/$2" "$4 $RULE" --edit "$SRC/$1" --aspect "$3" 2>&1 | tail -1)
}

gen "IMG_4055.jpg"     "hero.jpg"       "16:9" "Hero product shot of this exact lithium-ion battery pack: a block of green 21700 cylindrical cells with red insulator rings, joined by copper and nickel welded busbar strips across the top, dark green fibreglass wrap around the sides, red and black silicone wires with a yellow XT connector."
gen "IMG_4034 (1).jpg" "cta.jpg"        "16:9" "Wide product shot of this exact battery pack: a rectangular assembly of green 21700 cylindrical cells wrapped in dark green fibreglass insulation, with red and black wires, a white balance connector and a yellow XT connector on the left side."

gen "IMG_4054.jpg"     "type-21700.jpg" "4:3" "Product shot of this exact battery assembly: a flat rectangular array of green 21700 cylindrical cells with red insulator rings, joined by copper and nickel welded strips, black cell holder frame, red and black wires with a white balance lead."
gen "IMG_4006.jpg"     "type-hd.jpg"    "4:3" "Product shot of this exact high-density battery pack: a block of stacked silver aluminium-foil pouch cells with visible layered edges, black tape wrap on the sides, red and black wires with a yellow XT connector at one end."
gen "IMG_4019 (1).jpg" "type-ev.jpg"    "4:3" "Product shot of this exact battery pack: a rectangular block sealed in glossy blue heat-shrink wrap with rounded edges, red and black silicone wires and a white balance connector emerging from one end, yellow XT connector."

gen "IMG_4058.jpg"     "about.jpg"      "4:3" "Close-up macro product shot of this exact battery assembly: green 21700 cylindrical cells with red insulator rings, spot-welded copper and nickel busbar strips running across the cell tops, dark green fibreglass wrap, shallow depth of field on the weld points."

gen "IMG_4008.jpg"     "g1.jpg" "4:3" "Product shot of this exact battery pack: a slim flat rectangular pack sealed in black heat-shrink wrap, red and black wires with a yellow XT connector at the right end."
gen "IMG_4017.jpg"     "g2.jpg" "4:3" "Product shot of this exact battery pack: a slim flat rectangular pack sealed in glossy blue heat-shrink wrap, white balance connector and red-black wires with a yellow XT connector at the right end."
gen "IMG_4010.jpg"     "g3.jpg" "4:3" "Product shot of this exact battery pack: a thick rectangular block sealed in glossy black heat-shrink wrap with visible shrink seams along the top edge, viewed at a three-quarter angle."
gen "IMG_4052.jpg"     "g4.jpg" "4:3" "Product shot of this exact battery pack: a flat rectangular lithium polymer pouch pack in golden-yellow foil wrap with rounded corners, black and red wires exiting the right side with a yellow XT connector."
gen "IMG_4013.jpg"     "g5.jpg" "4:3" "Product shot of this exact battery pack: a compact block in glossy black heat-shrink wrap standing at a three-quarter angle, grey foam pad on the visible end face, red and black wires with a yellow XT connector lying in front."
gen "IMG_4037 (3).jpg" "g6.jpg" "4:3" "Product shot of this exact battery pack: a small upright block of green 21700 cylindrical cells wrapped in dark green fibreglass insulation, standing vertically, red and black wires rising from the top."

echo "DONE"
