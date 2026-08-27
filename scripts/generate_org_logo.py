#!/usr/bin/env python3
"""Generate the High-Performance-AI-Lab brand assets.

Two deterministic outputs, no randomness, no external inputs:

- assets/org-logo.png          1024x1024 organization avatar
- assets/org-social-card.png   1200x630 social preview for this repository

The mark: a 4x4 grid of rounded memory pages; the lit pages climb as a
measured series (1, 3, 2, 4 — a real benchmark trace, dip included) in
flat teal -> blue steps along the diagonal, the oxide page at the top
right is the decode head writing the next token (the hot page), and the
unlit pages stay dim. Everything sits inside the circle-mask safe area
and stays legible down to ~32px avatars. assets/org-logo.svg is the
hand-maintained vector twin of the same geometry; keep the three
artifacts in sync.

Color system: the ramp colors are the on-dark lifts of the website's
palette (hpailab-site/src/styles/global.css) — teal #3fb9aa ~ site teal
#0f766e, blue #62a0ff ~ site cobalt #2563eb — and the decode head is the
site's primary accent oxide at its bright dark-surface value #ea580c.
Neutrals are GitHub Primer dark, native to where these assets live.

    python3 scripts/generate_org_logo.py --check   # verify committed files
    python3 scripts/generate_org_logo.py           # regenerate
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (13, 17, 23)          # deep charcoal, matches the family cards
TEAL = (63, 185, 170)
BLUE = (98, 160, 255)
OXIDE = (234, 88, 12)      # site primary accent, bright on-dark value
FG = (240, 246, 252)       # near-white
DIM = (139, 148, 158)      # muted grey (card text)
PAGE_DIM = (30, 38, 49)    # unlit memory page

FONT_PATHS = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SUPPLEMENTARY/Arial Bold.ttf",
]

GRID_N = 4                 # pages per side
CELL = 140                 # page size (logo coordinates, 1024x1024)
GAP = 32                   # gap between pages
RADIUS = 29                # page corner radius
HEIGHTS = [1, 3, 2, 4]     # lit pages per column, left to right


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def draw_mark(img: Image.Image, scale: float = 1.0) -> Image.Image:
    """Memory-page grid with the lit measured series, centered onto `img`."""
    size = img.size[0]
    d = ImageDraw.Draw(img)
    cell, gap = CELL * scale, GAP * scale
    total = GRID_N * cell + (GRID_N - 1) * gap
    x0 = y0 = (size - total) / 2
    for c in range(GRID_N):
        for r in range(GRID_N):        # r = 0 is the bottom row
            x = x0 + c * (cell + gap)
            y = y0 + (GRID_N - 1 - r) * (cell + gap)
            if r >= HEIGHTS[c]:
                color = PAGE_DIM
            elif c == GRID_N - 1 and r == HEIGHTS[c] - 1:
                color = OXIDE          # the decode head, the hot page
            else:
                color = lerp(TEAL, BLUE, (c + r) / (2 * (GRID_N - 1)))
            d.rounded_rectangle([x, y, x + cell, y + cell],
                                radius=RADIUS * scale, fill=color)
    return img


def render_logo() -> Image.Image:
    return draw_mark(Image.new("RGB", (1024, 1024), BG))


def render_card() -> Image.Image:
    img = Image.new("RGB", (1200, 630), BG)
    mark = draw_mark(Image.new("RGB", (1024, 1024), BG), scale=0.78)
    mark = mark.resize((635, 635), Image.LANCZOS)
    img.paste(mark, (-60, 0))
    d = ImageDraw.Draw(img)
    x = 540
    d.text((x, 190), "High Performance", font=font(78), fill=FG)
    d.text((x, 280), "AI Lab", font=font(78), fill=FG)
    d.text((x, 420), "Open systems for local inference,", font=font(40), fill=TEAL)
    d.text((x, 472), "proofs, and measured intelligence.", font=font(40), fill=TEAL)
    d.text((x, 552), "github.com/High-Performance-AI-Lab", font=font(28), fill=DIM)
    return img


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify committed assets match fresh renders")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent.parent / "assets"
    outputs = {
        "org-logo.png": render_logo(),
        "org-social-card.png": render_card(),
    }
    if args.check:
        ok = True
        for name, fresh in outputs.items():
            path = base / name
            if not path.exists():
                print("FAIL: committed asset missing:", path)
                ok = False
                continue
            if Image.open(path).convert("RGB").tobytes() != fresh.tobytes():
                print("FAIL: committed asset differs from fresh render:", name)
                ok = False
        print("PASS: brand assets match renders" if ok else "FAIL: see above")
        return 0 if ok else 1

    base.mkdir(parents=True, exist_ok=True)
    for name, fresh in outputs.items():
        fresh.save(base / name, format="PNG", optimize=True)
        print("wrote", base / name)
    return 0


if __name__ == "__main__":
    sys.exit(main())
