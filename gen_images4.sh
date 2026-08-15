#!/bin/bash
# Batch 4 — gallery images for the three product pages.
# Same rule as every batch: the pack stays pixel-faithful, only the environment changes.
# Sources are the client photos not yet used on the home page, so nothing repeats.

GEN="/Users/ivan/Downloads/Клод сайти/google-image-gen-api-starter-main копія"
SRC="/Users/ivan/Downloads/Клод сайти/AutomationPower/photos_jpg"
OUT="/Users/ivan/Downloads/Клод сайти/AutomationPower/images"

RULE="CRITICAL RULE: the battery pack must remain absolutely identical to the source photo — exact same shape, proportions, viewing angle, colours, wrapping material and texture, seams, number and layout of cells, welded strips, wires, balance lead and connector. Do not redesign it, do not stylize it, do not add or remove any component, do not change its colour. ONLY change the environment: completely remove the green cutting mat, the metal ruler, the scale and every other background object, and place the pack on a seamless dark charcoal studio backdrop with a soft subtle vignette. Add clean professional studio lighting with a soft realistic contact shadow beneath the pack, improve sharpness, micro-detail and colour accuracy. Compose reasonably close so the pack fills most of the frame. Ultra-realistic commercial product photography, 4K, no text, no watermark."

gen () {
  if [ -f "$OUT/$2" ]; then echo "skip $2"; return; fi
  echo ">>> $2"
  (cd "$GEN" && uv run python main.py "$OUT/$2" "$3 $RULE" --edit "$SRC/$1" --aspect 4:3 2>&1 | tail -1)
}

# ---------- 21700 cylindrical page ----------
gen "IMG_4033 (1).jpg" "p21-1.jpg" "Product shot of this exact battery pack: a block of green 21700 cylindrical cells wrapped in dark green fibreglass insulation, red and black silicone wires with a yellow XT connector."
gen "IMG_4035 (2).jpg" "p21-2.jpg" "Product shot of this exact battery assembly: green 21700 cylindrical cells with red insulator rings and spot-welded nickel strips visible across the top, dark wrap around the sides, wires exiting one end."
gen "IMG_4036 (2).jpg" "p21-3.jpg" "Product shot of this exact battery assembly on 21700 cylindrical cells, three-quarter angle, welded busbar strips over the cell tops, red and black wires with a balance lead."
gen "IMG_4039 (3).jpg" "p21-4.jpg" "Product shot of this exact compact battery pack built on green 21700 cylindrical cells with dark green fibreglass wrap, standing at an angle, wires rising from the top."
gen "IMG_4056.jpg"     "p21-5.jpg" "Close-up macro product shot of this exact battery assembly: green 21700 cylindrical cells with red insulator rings and spot-welded copper and nickel busbar strips running across the cell tops, shallow depth of field on the weld points."
gen "IMG_4057.jpg"     "p21-6.jpg" "Product shot of this exact battery assembly: a flat array of green 21700 cylindrical cells in a black holder joined by welded nickel strips, viewed from a low three-quarter angle."

# ---------- high-density pouch page ----------
gen "IMG_4007 (1).jpg" "phd-1.jpg" "Product shot of this exact high-density battery pack: a block of stacked silver aluminium-foil pouch cells with visible layered foil edges, black tape binding, red and black wires with a yellow XT connector."
gen "IMG_4005 (1).jpg" "phd-2.jpg" "Close-up macro product shot of this exact high-density battery pack: the layered silver aluminium-foil pouch cell edges filling the frame, black tape binding at the side, shallow depth of field along the stack."
gen "IMG_4006.jpg"     "phd-3.jpg" "Product shot of this exact high-density battery pack viewed end-on: the stack of silver aluminium-foil pouch cells with the black wrapped end face toward the camera, red and black wires and a white balance connector exiting the end."
gen "IMG_4052.jpg"     "phd-4.jpg" "Product shot of this exact lithium polymer pouch pack in golden-yellow foil wrap with rounded corners, viewed at a three-quarter angle, black and red wires with a yellow XT connector exiting one side."

# ---------- EV pack page ----------
gen "IMG_4012.jpg"     "pev-1.jpg" "Product shot of this exact battery pack: a large rectangular block sealed in matte black heat-shrink wrap, red and black silicone wires and a white balance connector exiting one end, three-quarter angle."
gen "IMG_4024 (1).jpg" "pev-2.jpg" "Product shot of this exact battery pack: a rectangular block sealed in glossy blue heat-shrink wrap, red and black wires with a white balance connector and a yellow XT connector, three-quarter angle."
gen "IMG_4031 (2).jpg" "pev-3.jpg" "Product shot of this exact battery pack: a rectangular block in glossy blue heat-shrink wrap resting on a small black digital scale whose LCD shows a weight reading, red and black wires with a yellow XT connector. Keep the scale in frame as it is."

echo "DONE"
