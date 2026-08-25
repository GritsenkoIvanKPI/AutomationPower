#!/usr/bin/env python3
"""
Replace the background of a product photo WITHOUT touching the product.

Gemini was re-rendering the packs — it changed wrap colour, invented wires and
connectors. The client's hard rule is that the batteries must look exactly as
photographed, so this does a real cut-out instead of a re-render: rembg produces
an alpha mask, and the product's own pixels are composited onto a studio backdrop.
The subject pixels are copied verbatim; only what is outside the mask changes.

Usage: replace_bg.py in.jpg out.jpg [--pad 0.06] [--ratio 1.333]
"""
import sys, argparse
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from rembg import remove, new_session

BG_TOP, BG_BOTTOM = (26, 26, 26), (14, 14, 14)   # neutral, matches the site's #111111
SESSION = new_session("isnet-general-use")        # sharper edges than u2net on hard goods


def largest_component(mask, thresh=8):
    """Keep only the biggest blob — drops the steel ruler / stray objects in frame."""
    m = mask > thresh
    h, w = m.shape
    lab = np.zeros((h, w), np.int32)
    cur, sizes = 0, {}
    for y in range(h):
        row = m[y]
        if not row.any():
            continue
        xs = np.flatnonzero(row)
        for x in xs:
            if lab[y, x]:
                continue
            cur += 1
            stack, n = [(y, x)], 0
            lab[y, x] = cur
            while stack:
                cy, cx = stack.pop()
                n += 1
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < h and 0 <= nx < w and m[ny, nx] and not lab[ny, nx]:
                        lab[ny, nx] = cur
                        stack.append((ny, nx))
            sizes[cur] = n
    if not sizes:
        return mask
    keep = max(sizes, key=sizes.get)
    return np.where(lab == keep, mask, 0).astype(np.uint8)


def studio_bg(size):
    w, h = size
    grad = np.linspace(0, 1, h, dtype=np.float32)[:, None]
    top = np.array(BG_TOP, np.float32)
    bot = np.array(BG_BOTTOM, np.float32)
    img = (top * (1 - grad) + bot * grad)[:, None, :].repeat(w, axis=1)
    # soft vignette so the plate reads as a lit backdrop rather than flat fill
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.sqrt(((xx / w - .5) * 1.15) ** 2 + ((yy / h - .5) * 1.15) ** 2)
    img *= (1.0 - 0.55 * np.clip(r, 0, 1) ** 1.7)[:, :, None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), "RGB")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src"); ap.add_argument("dst")
    ap.add_argument("--pad", type=float, default=0.06)
    ap.add_argument("--ratio", type=float, default=4 / 3)
    ap.add_argument("--clear", default=None,
                    help="x0,y0,x1,y1 in source px: drop backdrop-coloured pixels only "
                         "inside this box (for mat the matte wrongly keeps near wires)")
    ap.add_argument("--cleartol", type=float, default=44.0,
                    help="colour tolerance for --clear")
    ap.add_argument("--anchor", default="center", choices=["center", "right"],
                    help="where the subject sits in the frame (banners use right)")
    a = ap.parse_args()

    # Several photos carry EXIF orientation 6. PIL ignores it on open but rembg applies
    # it, so src and the mask came back transposed and the composite failed. Strip EXIF
    # by round-tripping through an array: rembg then cannot re-orient, and the output
    # keeps the same orientation the client has been reviewing for every other photo.
    src = Image.fromarray(np.array(Image.open(a.src).convert("RGB")))
    cut = remove(src, session=SESSION, alpha_matting=True,
                 alpha_matting_foreground_threshold=250,
                 alpha_matting_background_threshold=15,
                 alpha_matting_erode_size=6)
    alpha = np.array(cut.split()[-1])
    alpha = largest_component(alpha)

    if a.clear:
        # A global colour key is impossible here: the cells sit closer to the mat colour
        # than the mat's own mid-field. Inside a small box around the leak, though, the only
        # things present are mat, wires and the connector, which separate cleanly.
        cx0, cy0, cx1, cy1 = (int(v) for v in a.clear.split(","))
        box = np.array(src, np.int16)[cy0:cy1, cx0:cx1]
        sub = alpha[cy0:cy1, cx0:cx1]
        held = box[sub > 8]
        if len(held):
            local = np.median(held[np.argsort(np.abs(held[:, 1].astype(int) - held[:, 2]))[:len(held)//2]], axis=0)
            dist = np.sqrt(((box - local) ** 2).sum(axis=2))
            drop = (dist < a.cleartol) & (sub > 8)
            alpha[cy0:cy1, cx0:cx1] = np.where(drop, 0, sub)
            print(f"  cleared {int(drop.sum()):,} backdrop px inside {a.clear}")

    ys, xs = np.nonzero(alpha > 8)
    if len(xs) == 0:
        raise SystemExit(f"{a.src}: nothing segmented")
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()

    # frame the product with an even margin, in the requested aspect
    pad = int(max(x1 - x0, y1 - y0) * a.pad)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    bw, bh = (x1 - x0) + 2 * pad, (y1 - y0) + 2 * pad
    if bw / bh < a.ratio: bw = bh * a.ratio
    else:                 bh = bw / a.ratio
    # banners put the pack in the right third so headline copy has clear space
    fx = 0.66 if a.anchor == "right" else 0.5
    L, T = int(round(cx - bw * fx)), int(round(cy - bh / 2))
    W, H = int(round(bw)), int(round(bh))

    fg = Image.fromarray(np.dstack([np.array(src), alpha]), "RGBA").crop((L, T, L + W, T + H))
    out = studio_bg((W, H))

    # contact shadow, built from the mask so it matches the real silhouette
    sh = Image.fromarray(alpha, "L").crop((L, T, L + W, T + H))
    sh = sh.filter(ImageFilter.GaussianBlur(max(6, W // 55)))
    sh = sh.point(lambda v: int(v * 0.55))
    out.paste(Image.new("RGB", (W, H), (0, 0, 0)),
              (0, max(4, H // 90)), sh)

    out.paste(fg, (0, 0), fg)
    out.save(a.dst, quality=95)
    cov = (alpha > 8).sum() / alpha.size
    print(f"{a.src} -> {a.dst}  {W}x{H}  subject covers {cov*100:.1f}% of source")


if __name__ == "__main__":
    main()
