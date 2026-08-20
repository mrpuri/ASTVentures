#!/usr/bin/env python3
"""Generate the AST Ventures logo suite as SVG."""
import os
from text2path import build

F = "assets/fonts/plus-jakarta-sans-latin-{}-normal.woff2"
EXTRABOLD = F.format(800)
SEMIBOLD = F.format(600)
MEDIUM = F.format(500)

NAVY = "#0A2145"
BLUE = "#1F6FEB"
MUTED = "#4B6A9B"

# ---------------------------------------------------------------- the mark
def mark(size=88, idsuffix="a", light=False):
    """Rounded-square tile containing the geometric A-node monogram."""
    s = size / 88.0
    def p(*vals):
        return " ".join(f"{v * s:.2f}" for v in vals)

    grad_id = f"astg{idsuffix}"
    if light:
        tile = f'<rect x="0" y="0" width="{size:.2f}" height="{size:.2f}" rx="{24*s:.2f}" fill="#ffffff"/>'
        stroke_main, stroke_bar, dot = BLUE, "#8FB8F7", BLUE
    else:
        tile = (f'<rect x="0" y="0" width="{size:.2f}" height="{size:.2f}" rx="{24*s:.2f}" fill="url(#{grad_id})"/>')
        stroke_main, stroke_bar, dot = "#FFFFFF", "#A9CBFF", "#FFFFFF"

    w = 9.5 * s
    parts = [
        f'<defs><linearGradient id="{grad_id}" x1="0" y1="0" x2="1" y2="1">'
        f'<stop offset="0%" stop-color="#3B86F7"/><stop offset="55%" stop-color="#1F6FEB"/>'
        f'<stop offset="100%" stop-color="#123A8F"/></linearGradient></defs>',
        tile,
        # crossbar of the A, rendered as a lighter circuit trace
        f'<path d="M {p(30.5, 54)} L {p(57.5, 54)}" stroke="{stroke_bar}" stroke-width="{w:.2f}" stroke-linecap="round" fill="none"/>',
        # the chevron / apex of the A
        f'<path d="M {p(20, 68)} L {p(44, 21)} L {p(68, 68)}" stroke="{stroke_main}" stroke-width="{w:.2f}" '
        f'stroke-linecap="round" stroke-linejoin="round" fill="none"/>',
        # network nodes at the two feet
        f'<circle cx="{20*s:.2f}" cy="{68*s:.2f}" r="{9.5*s:.2f}" fill="{dot}"/>',
        f'<circle cx="{68*s:.2f}" cy="{68*s:.2f}" r="{9.5*s:.2f}" fill="{dot}"/>',
        f'<circle cx="{20*s:.2f}" cy="{68*s:.2f}" r="{4.0*s:.2f}" fill="{"#1F6FEB" if not light else "#ffffff"}"/>',
        f'<circle cx="{68*s:.2f}" cy="{68*s:.2f}" r="{4.0*s:.2f}" fill="{"#1F6FEB" if not light else "#ffffff"}"/>',
    ]
    return "".join(parts)


# ------------------------------------------------------------ the wordmark
def wordmark(dark_bg=False, descriptor=True):
    """Returns (svg_body, width, height) with baseline geometry already applied."""
    c_main = "#FFFFFF" if dark_bg else NAVY
    c_second = "#BFD6FF" if dark_bg else MUTED
    c_desc = "#8FB8F7" if dark_bg else BLUE

    ast_d, ast_w = build(EXTRABOLD, "AST", 58, -0.012)
    ven_d, ven_w = build(MEDIUM, "VENTURES", 58, 0.012)
    gap = 15.0
    line1_w = ast_w + gap + ven_w

    body = [
        f'<g transform="translate(0,42)"><path d="{ast_d}" fill="{c_main}"/></g>',
        f'<g transform="translate({ast_w + gap:.2f},42)"><path d="{ven_d}" fill="{c_second}"/></g>',
    ]
    height = 42
    if descriptor:
        des_d, des_w = build(SEMIBOLD, "AI SKILLS & TRAINING", 15.5, 0.19)
        body.append(f'<g transform="translate(2,68)"><path d="{des_d}" fill="{c_desc}"/></g>')
        line1_w = max(line1_w, des_w + 2)
        height = 68
    return "".join(body), line1_w, height


def svg(w, h, body, extra=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.2f}" height="{h:.2f}" role="img" aria-label="AST Ventures — AI Skills and Training"{extra}>'
            f'{body}</svg>')


def horizontal(dark_bg=False, descriptor=True, suffix="h"):
    m = 88
    body, ww, wh = wordmark(dark_bg, descriptor)
    gapx = 26
    total_w = m + gapx + ww
    total_h = 88
    wm_y = (total_h - (wh + 8)) / 2 if descriptor else (total_h - 42) / 2 - 4
    inner = (f'<g>{mark(m, suffix, light=False)}</g>'
             f'<g transform="translate({m + gapx},{wm_y:.2f})">{body}</g>')
    return svg(total_w, total_h, inner)


def stacked(dark_bg=False, suffix="s"):
    body, ww, wh = wordmark(dark_bg, True)
    m = 96
    total_w = max(ww, m) + 8
    total_h = m + 26 + wh + 6
    inner = (f'<g transform="translate({(total_w - m)/2:.2f},0)">{mark(m, suffix)}</g>'
             f'<g transform="translate({(total_w - ww)/2:.2f},{m + 26})">{body}</g>')
    return svg(total_w, total_h, inner)


def write(path, content):
    with open(path, "w") as f:
        f.write(content)
    print("wrote", path, len(content), "bytes")


if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    write("assets/logo.svg", horizontal(False, True, "h1"))
    write("assets/logo-white.svg", horizontal(True, True, "h2"))
    write("assets/logo-stacked.svg", stacked(False, "s1"))
    write("assets/logo-mark.svg", svg(88, 88, mark(88, "m1")))
    write("assets/favicon.svg", svg(88, 88, mark(88, "f1")))
