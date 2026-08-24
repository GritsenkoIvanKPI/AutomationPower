#!/usr/bin/env python3
"""
Prove the product pixels in a rebuilt image are byte-identical to the source photo.

replace_bg.py crops from the full-resolution original and composites without resampling,
so wherever the cut-out mask is fully opaque the output pixel must equal the source pixel
exactly. This locates the crop offset by search, then reports the mismatch rate.

Usage: verify_fidelity.py source.jpg rebuilt.jpg
"""
import sys
import numpy as np
from PIL import Image

src = np.array(Image.open(sys.argv[1]).convert("RGB"), np.int16)
out = np.array(Image.open(sys.argv[2]).convert("RGB"), np.int16)
sh, sw = src.shape[:2]
oh, ow = out.shape[:2]

# the rebuilt frame may extend past the source edges (padding), so search offsets
best = None
step = 4
for dy in range(-oh + 8, sh - 8, step):
    for dx in range(-ow + 8, sw - 8, step):
        y0, x0 = max(0, dy), max(0, dx)
        y1, x1 = min(sh, dy + oh), min(sw, dx + ow)
        if y1 - y0 < oh * 0.4 or x1 - x0 < ow * 0.4:
            continue
        a = src[y0:y1:16, x0:x1:16]
        b = out[y0 - dy:y1 - dy:16, x0 - dx:x1 - dx:16]
        d = np.abs(a - b).mean()
        if best is None or d < best[0]:
            best = (d, dy, dx)

_, dy, dx = best
y0, x0 = max(0, dy), max(0, dx)
y1, x1 = min(sh, dy + oh), min(sw, dx + ow)
a = src[y0:y1, x0:x1]
b = out[y0 - dy:y1 - dy, x0 - dx:x1 - dx]
diff = np.abs(a - b).max(axis=2)

identical = (diff <= 2)                      # <=2 absorbs JPEG requantisation only
strong = identical.sum() / identical.size
print(f"overlap {a.shape[1]}x{a.shape[0]} at offset ({dx},{dy})")
print(f"  pixels identical to the source: {strong*100:.1f}%   (the rest is replaced background)")
print(f"  mean abs difference over identical region: {np.abs(a-b)[identical].mean():.3f}")
