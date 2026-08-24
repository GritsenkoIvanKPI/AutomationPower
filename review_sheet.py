#!/usr/bin/env python3
"""Pair each rebuilt image with its source photo so the cut-out can be eyeballed at a glance."""
import sys, re
from PIL import Image, ImageDraw

OUT = "/private/tmp/claude-501/-Users-ivan-Downloads------------AutomationPower/d27350bd-8caf-42c6-8ce0-04bbdad379b4/scratchpad"

pairs = []
for line in open("rebuild_images.sh", encoding="utf-8"):
    m = re.match(r'run\s+(\S+\.jpg)\s+"([^"]+)"', line.strip())
    if m:
        pairs.append((m.group(1), m.group(2)))

group = sys.argv[1] if len(sys.argv) > 1 else ""
pairs = [p for p in pairs if p[0].startswith(group)]   # prefix match: ".jpg" contains "g"

CW, CH = 430, 330
cols = 2                      # source | rebuilt
rows = len(pairs)
sheet = Image.new("RGB", (CW * cols, CH * rows), (14, 14, 14))
d = ImageDraw.Draw(sheet)
for r, (dst, src) in enumerate(pairs):
    for c, path in enumerate((f"photos_jpg/{src}", f"images/{dst}")):
        try:
            im = Image.open(path).convert("RGB")
        except Exception:
            continue
        im.thumbnail((CW - 8, CH - 26))
        sheet.paste(im, (c * CW + 4, r * CH + 20))
    d.text((4, r * CH + 5), f"{src}", fill=(255, 190, 120))
    d.text((CW + 4, r * CH + 5), f"-> {dst}", fill=(140, 255, 170))
name = f"{OUT}/review_{group or 'all'}.jpg"
sheet.save(name, quality=88)
print(f"{name}  ({rows} pairs)")
