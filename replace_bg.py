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

BG_LOW, BG_HIGH = 9.0, 46.0        # plate falls off to near-black, lifts behind the product
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


def studio_bg(size, subject):
    """Lit studio plate: a soft light pool behind the product, falling off to near-black,
    plus a faint floor band under it. Keyed to where the subject actually sits so the
    light reads as aimed at the product rather than a flat fill."""
    w, h = size
    sx0, sy0, sx1, sy1 = subject
    cx, cy = (sx0 + sx1) / 2 / w, (sy0 + sy1) / 2 / h
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nx, ny = xx / w, yy / h

    # main light pool, centred a little above the product
    r = np.sqrt(((nx - cx) * 1.05) ** 2 + ((ny - (cy - 0.10)) * 1.30) ** 2)
    pool = np.clip(1.0 - r / 0.92, 0, 1) ** 1.55

    # faint floor band just under the product, suggesting a surface
    floor_y = sy1 / h
    band = np.exp(-(((ny - floor_y - 0.05) / 0.20) ** 2)) * np.clip(1.0 - abs(nx - cx) / 0.75, 0, 1)

    L = BG_LOW + (BG_HIGH - BG_LOW) * pool + 7.0 * band
    # corner vignette keeps the frame from feeling like a lit box
    v = np.sqrt(((nx - .5) * 1.2) ** 2 + ((ny - .5) * 1.2) ** 2)
    L *= 1.0 - 0.42 * np.clip(v, 0, 1) ** 2.0
    img = np.repeat(np.clip(L, 0, 255)[:, :, None], 3, axis=2)
    return Image.fromarray(img.astype(np.uint8), "RGB")


def contact_shadow(alpha_crop, size):
    """Shadow traced along the product's actual bottom contour.

    A uniformly squashed silhouette only grounds objects that sit flat; for a pack shot
    at an angle it smears the whole shape and the product appears to float. Taking the
    lowest opaque pixel per column instead puts the darkness exactly where the product
    meets the surface, whatever its pose."""
    w, h = size
    m = alpha_crop > 8
    if not m.any():
        return None
    plate = np.zeros((h, w), np.float32)
    cols = np.nonzero(m.any(axis=0))[0]
    lows = np.array([np.nonzero(m[:, x])[0].max() for x in cols])
    # vertical falloff below each contact point
    span = max(8, int(h * 0.10))
    yy = np.arange(h)[:, None]
    d = yy - lows[None, :]
    blob = np.exp(-(d / (span * 0.55)) ** 2) * (d >= -span * 0.25)
    plate[:, cols] = blob
    img = Image.fromarray((np.clip(plate, 0, 1) * 255).astype(np.uint8), "L")
    img = img.filter(ImageFilter.GaussianBlur(max(9, w // 42)))
    return img.point(lambda v: int(v * 0.72))


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

    alpha_crop = np.array(Image.fromarray(alpha, "L").crop((L, T, L + W, T + H)))
    fg = Image.fromarray(np.dstack([np.array(src), alpha]), "RGBA").crop((L, T, L + W, T + H))

    sub = np.nonzero(alpha_crop > 8)
    subject = (sub[1].min(), sub[0].min(), sub[1].max(), sub[0].max()) if len(sub[0]) else (0, 0, W, H)
    out = studio_bg((W, H), subject)

    sh = contact_shadow(alpha_crop, (W, H))
    if sh is not None:
        out.paste(Image.new("RGB", (W, H), (0, 0, 0)), (0, 0), sh)

    # the product's own pixels go down last and are never modified
    out.paste(fg, (0, 0), fg)
    out.save(a.dst, quality=95)
    cov = (alpha > 8).sum() / alpha.size
    print(f"{a.src} -> {a.dst}  {W}x{H}  subject covers {cov*100:.1f}% of source")


if __name__ == "__main__":
    main()
