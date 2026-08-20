"""Convert a text string to an SVG path using a woff2 font.
Usage: python3 text2path.py <fontfile> <text> <fontsize> <tracking_em>
Prints: path d= data (baseline at y=0, start at x=0) and advance width.
"""
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


def build(fontpath, text, size, tracking=0.0):
    font = TTFont(fontpath)
    upem = font["head"].unitsPerEm
    scale = size / upem
    cmap = font.getBestCmap()
    gs = font.getGlyphSet()
    hmtx = font["hmtx"]
    try:
        kern = font["kern"].kernTables[0].kernTable
    except Exception:
        kern = {}

    parts = []
    x = 0.0
    prev = None
    for ch in text:
        gname = cmap.get(ord(ch))
        if gname is None:
            x += size * 0.35
            prev = None
            continue
        if prev is not None:
            x += kern.get((prev, gname), 0) * scale
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        tp = TransformPen(pen, Transform(scale, 0, 0, -scale, x, 0))
        gs[gname].draw(tp)
        d = pen.getCommands()
        if d:
            parts.append(d)
        x += hmtx[gname][0] * scale + tracking * size
        prev = gname
    if text:
        x -= tracking * size
    return " ".join(parts), x


if __name__ == "__main__":
    fp, text, size = sys.argv[1], sys.argv[2], float(sys.argv[3])
    tr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
    d, w = build(fp, text, size, tr)
    print(f"WIDTH {w:.2f}")
    print(d)
