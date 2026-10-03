#!/usr/bin/env python3
"""Export the logo SVGs to transparent PNGs.

macOS only: rasterising is done by Quick Look (`qlmanage`), which renders SVG
through WebKit but always composites onto opaque white. To recover real
transparency each logo is rendered twice — once over white, once over black —
and the alpha is solved back out:

    over white: W = C·a + 255·(1-a)
    over black: B = C·a
    =>  a = 1 - (W-B)/255      and      C = B/a

Pillow then trims the padding and resizes to the target width.
Run build_logo.py first.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import numpy as np
    from PIL import Image
except ImportError:
    sys.exit("Pillow and numpy are required: python3 -m pip install pillow numpy")

# (source svg, output png, target width in px)
EXPORTS = [
    ("assets/logo.svg", "assets/logo.png", 1800),
    ("assets/logo-white.svg", "assets/logo-white.png", 1800),
    ("assets/logo-stacked.svg", "assets/logo-stacked.png", 1200),
    ("assets/logo-mark.svg", "assets/logo-mark.png", 512),
]

RENDER_AT = 2048
SVG_OPEN = re.compile(r"(<svg\b[^>]*>)")


def render_over(svg_path, colour, tmpdir, tag):
    """Rasterise the SVG with a full-bleed backing colour behind it."""
    src = open(svg_path).read()
    backed = SVG_OPEN.sub(
        r'\1<rect x="-10%" y="-10%" width="120%" height="120%" fill="' + colour + '"/>',
        src, count=1)
    stem = os.path.basename(svg_path).replace(".svg", "") + "-" + tag + ".svg"
    tmp_svg = os.path.join(tmpdir, stem)
    with open(tmp_svg, "w") as f:
        f.write(backed)
    subprocess.run(
        ["qlmanage", "-t", "-s", str(RENDER_AT), "-o", tmpdir, tmp_svg],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    out = tmp_svg + ".png"
    if not os.path.exists(out):
        raise RuntimeError(f"qlmanage produced nothing for {svg_path}")
    return np.asarray(Image.open(out).convert("RGB"), dtype=np.float64)


def unmatte(white, black):
    """Solve alpha and straight colour from the two composites."""
    alpha = 1.0 - np.clip((white - black).mean(axis=2), 0, 255) / 255.0
    # rounding noise leaves a haze of alpha≈1/255 across the empty canvas,
    # which would defeat the bounding-box crop; floor it to fully clear
    alpha[alpha < 0.02] = 0.0
    safe = np.where(alpha > 0.003, alpha, 1.0)[..., None]
    colour = np.clip(black / safe, 0, 255)
    rgba = np.dstack([colour, alpha[..., None] * 255.0])
    return Image.fromarray(np.rint(rgba).astype(np.uint8), "RGBA")


def svg_rect(black):
    """Quick Look pads the thumbnail to a square with its own white ground.
    That padding is white in both renders, so it would solve to opaque white —
    find the real SVG area as the part the black backing rect actually covers."""
    drawn = black.mean(axis=2) < 250
    rows, cols = np.any(drawn, axis=1), np.any(drawn, axis=0)
    if not rows.any() or not cols.any():
        return None
    y0, y1 = np.where(rows)[0][[0, -1]]
    x0, x1 = np.where(cols)[0][[0, -1]]
    # the backing rect's own edge is antialiased, which would solve to a
    # half-transparent hairline along the border — step inside it
    inset = 2
    if y1 - y0 > 4 * inset and x1 - x0 > 4 * inset:
        y0, y1, x0, x1 = y0 + inset, y1 - inset, x0 + inset, x1 - inset
    return slice(y0, y1 + 1), slice(x0, x1 + 1)


def main():
    if not shutil.which("qlmanage"):
        sys.exit("qlmanage not found — this exporter needs macOS.")
    with tempfile.TemporaryDirectory() as tmp:
        for src, dst, width in EXPORTS:
            white = render_over(src, "#ffffff", tmp, "w")
            black = render_over(src, "#000000", tmp, "b")
            rect = svg_rect(black)
            if rect:
                white, black = white[rect], black[rect]
            # the SVG rect already is the viewBox, so the PNG keeps the same
            # proportions and designed padding as the vector file
            img = unmatte(white, black)
            height = max(1, round(img.height * width / img.width))
            img = img.resize((width, height), Image.LANCZOS)
            img.save(dst, "PNG", optimize=True)
            print(f"wrote {dst:28} {width}x{height}  {os.path.getsize(dst)/1024:.0f} KB")


if __name__ == "__main__":
    main()
