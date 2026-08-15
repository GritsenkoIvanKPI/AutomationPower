#!/usr/bin/env python3
"""
Crop a studio product shot down to the product itself.

The Gemini re-frame pass only zooms ~10% per run, so the packs stayed small in frame.
This finds the product's bounding box against the seamless dark backdrop and crops to it
with a small margin, keeping a 4:3 frame. Cast shadows are excluded (they are *darker*
than the backdrop; only brighter or saturated pixels count as product).

Usage: python3 crop_product.py in.jpg out.jpg [margin]
"""
import sys
from PIL import Image


def product_box(im, pad_frac=0.055):
    """Locate the product by local detail: the studio backdrop is smooth, the pack is not.

    Brightness alone fails here — the backdrop carries a bright pool of light that reads as
    'not background'. Edge energy separates them cleanly.
    """
    step = 4
    small = im.convert("L").resize((im.width // step, im.height // step), Image.BILINEAR)
    w, h = small.size
    px = small.load()

    # edge energy per pixel (max neighbour delta)
    energy = [[0] * w for _ in range(h)]
    peak = 0
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            c = px[x, y]
            e = max(abs(c - px[x - 1, y]), abs(c - px[x + 1, y]),
                    abs(c - px[x, y - 1]), abs(c - px[x, y + 1]))
            energy[y][x] = e
            peak = max(peak, e)

    thr = max(10, int(peak * 0.16))
    cols, rows = [0] * w, [0] * h
    for y in range(h):
        for x in range(w):
            if energy[y][x] > thr:
                cols[x] += 1
                rows[y] += 1

    def span(counts, limit):
        top = max(counts)
        if not top:
            return 0, limit - 1
        cut = max(1, top * 0.10)                   # ignore stray speckle
        idx = [i for i, c in enumerate(counts) if c > cut]
        return (idx[0], idx[-1]) if idx else (0, limit - 1)

    x0, x1 = span(cols, w)
    y0, y1 = span(rows, h)
    x0, x1, y0, y1 = x0 * step, x1 * step, y0 * step, y1 * step

    pad = int(max(x1 - x0, y1 - y0) * pad_frac)
    return x0 - pad, y0 - pad, x1 + pad, y1 + pad


def to_ratio(box, im, ratio=4 / 3):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bw, bh = x1 - x0, y1 - y0
    if bw / bh < ratio:
        bw = bh * ratio
    else:
        bh = bw / ratio
    # keep the crop inside the source
    bw = min(bw, im.width)
    bh = min(bh, im.height)
    bh = min(bh, bw / ratio)
    bw = bh * ratio
    cx = min(max(cx, bw / 2), im.width - bw / 2)
    cy = min(max(cy, bh / 2), im.height - bh / 2)
    return (round(cx - bw / 2), round(cy - bh / 2), round(cx + bw / 2), round(cy + bh / 2))


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    pad = float(sys.argv[3]) if len(sys.argv) > 3 else 0.055
    im = Image.open(src).convert("RGB")
    box = to_ratio(product_box(im, pad), im)
    im.crop(box).save(dst, quality=96)
    print(f"{src} {im.size} -> {dst} crop={box} size={(box[2]-box[0], box[3]-box[1])}")
