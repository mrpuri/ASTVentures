#!/usr/bin/env python3
"""Generate the AST Ventures logo suite as SVG.

The brand pack ships its logos as <text>, which is not safe to publish: an SVG
loaded through <img> cannot reach the page's fonts, so with no font-family
declared the browser falls back to its default serif (Times, measured). Here the
lettering is converted to outlines with fontTools, so every file renders exactly
the same everywhere and carries no font dependency at all.

Geometry is computed from real glyph widths rather than hard-coded, so the rule
and the right-hand column stay aligned whatever the font metrics turn out to be.
"""
import os
from text2path import build

F = "assets/fonts/plus-jakarta-sans-latin-{}-normal.woff2"
EXTRABOLD = F.format(800)
SEMIBOLD = F.format(600)
MEDIUM = F.format(500)

# brand pack palette
NAVY = "#1d2d3d"
STEEL = "#5980a6"
BLACK = "#000000"
WHITE = "#ffffff"

# type scale, taken from the pack's proportions
AST_TRACK = -0.01
VEN_TRACK = 0.20
DESC_TRACK = 0.14
DESCRIPTOR = "AI SKILLS & TRAINING"


def svg(w, h, body, label="AST Ventures — AI Skills and Training"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.2f}" height="{h:.2f}" role="img" aria-label="{label}">'
            f'{body}</svg>')


def horizontal(color=NAVY):
    """AST | VENTURES over AI SKILLS & TRAINING — the primary lockup."""
    ast_d, ast_w = build(EXTRABOLD, "AST", 64, AST_TRACK)
    ven_d, ven_w = build(MEDIUM, "VENTURES", 20, VEN_TRACK)
    des_d, des_w = build(SEMIBOLD, DESCRIPTOR, 10, DESC_TRACK)

    gap = 21.0
    rule_x = ast_w + gap
    col_x = rule_x + gap
    total_w = col_x + max(ven_w, des_w)
    total_h = 72.0

    body = (
        f'<g transform="translate(0,60)"><path d="{ast_d}" fill="{color}"/></g>'
        f'<rect x="{rule_x:.2f}" y="13" width="1" height="53" fill="{color}"/>'
        f'<g transform="translate({col_x:.2f},41)"><path d="{ven_d}" fill="{color}"/></g>'
        f'<g transform="translate({col_x:.2f},60)"><path d="{des_d}" fill="{color}"/></g>'
    )
    return svg(total_w, total_h, body)


def vertical(color=NAVY):
    """Stacked lockup for square placements."""
    ast_d, ast_w = build(EXTRABOLD, "AST", 92, AST_TRACK)
    ven_d, ven_w = build(MEDIUM, "VENTURES", 15, 0.34)
    des_d, des_w = build(SEMIBOLD, DESCRIPTOR, 10, DESC_TRACK)

    content = max(ast_w, des_w)
    total_w = content + 24
    total_h = 164.0
    cx = total_w / 2

    body = (
        f'<g transform="translate({cx - ast_w/2:.2f},86)"><path d="{ast_d}" fill="{color}"/></g>'
        f'<rect x="{cx - content/2:.2f}" y="104" width="{content:.2f}" height="1" fill="{color}"/>'
        f'<g transform="translate({cx - ven_w/2:.2f},130)"><path d="{ven_d}" fill="{color}"/></g>'
        f'<g transform="translate({cx - des_w/2:.2f},152)"><path d="{des_d}" fill="{color}"/></g>'
    )
    return svg(total_w, total_h, body)


def icon(size=256, bg=STEEL, fg=WHITE):
    """Square app/social tile — AST centred on a solid ground."""
    s = size / 256.0
    fs = 84 * s
    ast_d, ast_w = build(EXTRABOLD, "AST", fs, AST_TRACK)
    # centre on the cap height rather than the baseline, so the block of
    # letters sits optically in the middle of the tile
    cap = fs * 0.73
    baseline = size / 2 + cap / 2
    body = (
        f'<rect width="{size:.2f}" height="{size:.2f}" fill="{bg}"/>'
        f'<g transform="translate({(size - ast_w)/2:.2f},{baseline:.2f})">'
        f'<path d="{ast_d}" fill="{fg}"/></g>'
    )
    return svg(size, size, body, label="AST Ventures")


def wordmark(color=BLACK):
    """AST on its own."""
    ast_d, ast_w = build(EXTRABOLD, "AST", 92, AST_TRACK)
    return svg(ast_w + 16, 104,
               f'<g transform="translate(8,79)"><path d="{ast_d}" fill="{color}"/></g>',
               label="AST")


def write(path, content):
    with open(path, "w") as f:
        f.write(content)
    print(f"wrote {path:34} {len(content):>6} bytes")


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    # primary lockups used by the site
    write("assets/logo.svg", horizontal(NAVY))
    write("assets/logo-white.svg", horizontal(WHITE))       # footer sits on navy
    write("assets/logo-stacked.svg", vertical(NAVY))
    write("assets/logo-mark.svg", icon())
    write("assets/favicon.svg", icon())
    # additional pack variants, kept available for decks and social
    write("assets/logo-wordmark.svg", wordmark(BLACK))
    write("assets/logo-wordmark-steel.svg", wordmark(STEEL))
    write("assets/logo-stacked-white.svg", vertical(WHITE))
