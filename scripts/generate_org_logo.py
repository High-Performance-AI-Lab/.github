#!/usr/bin/env python3
"""Generate the High-Performance-AI-Lab brand assets.

Two deterministic outputs, no randomness, no external inputs:

- assets/org-logo.png          1024x1024 organization avatar
- assets/org-social-card.png   1200x630 social preview for this repository

The mark: a pointy-top hexagon ring with a horizontal teal -> blue gradient
(a chip/lattice outline) around a bold H. Everything sits inside the
circle-mask safe area and stays legible down to ~40px avatars.
assets/org-logo.svg is the hand-maintained vector twin of the same
geometry; keep the three artifacts in sync.

    python3 scripts/generate_org_logo.py --check   # verify committed files
    python3 scripts/generate_org_logo.py           # regenerate
"""

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (13, 17, 23)          # deep charcoal, matches the family cards
TEAL = (63, 185, 170)
BLUE = (98, 160, 255)
FG = (240, 246, 252)       # near-white
DIM = (139, 148, 158)      # muted grey

FONT_PATHS = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SUPPLEMENTARY/Arial Bold.ttf",
]

HEX_R = 370        # hexagon circumradius (logo coordinates, 1024x1024)
RING_W = 72        # hexagon ring stroke width
H_SIZE = 500       # H glyph size
H_Y_OFFSET = 12    # optical centering


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3))


def gradient_rgb(c1=TEAL, c2=BLUE, size: int = 1024) -> Image.Image:
    img = Image.new("RGB", (size, size))
    d = ImageDraw.Draw(img)
    for i in range(size):
        d.line([(i, 0), (i, size)], fill=lerp(c1, c2, i / (size - 1)))
    return img


def hex_points(cx: float, cy: float, r: float) -> list[tuple[float, float]]:
    # pointy-top: one vertex straight up
    return [(cx + r * math.cos(math.radians(60 * i - 90)),
             cy + r * math.sin(math.radians(60 * i - 90))) for i in range(6)]


def draw_mark(img: Image.Image, scale: float = 1.0) -> Image.Image:
    """Hex ring + H, drawn centered onto `img` (RGBA compositing for the gradient)."""
    size = img.size[0]
    grad = gradient_rgb(size=size)
    r, w = HEX_R * scale, RING_W * scale
    cx = cy = size / 2
    ring = Image.new("L", (size, size), 0)
    ImageDraw.Draw(ring).polygon(hex_points(cx, cy, r), outline=255, width=round(w))
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    layer.paste(grad, (0, 0), ring)
    img = Image.alpha_composite(img.convert("RGBA"), layer)
    d = ImageDraw.Draw(img)
    d.text((cx, cy + H_Y_OFFSET * scale), "H",
           font=font(max(8, round(H_SIZE * scale))), fill=FG + (255,), anchor="mm")
    return img


def render_logo() -> Image.Image:
    img = Image.new("RGB", (1024, 1024), BG)
    return draw_mark(img).convert("RGB")


def render_card() -> Image.Image:
    img = Image.new("RGB", (1200, 630), BG)
    mark = draw_mark(Image.new("RGB", (1024, 1024), BG), scale=0.62)
    mark = mark.resize((635, 635), Image.LANCZOS)
    img.paste(mark, (-60, 0))
    d = ImageDraw.Draw(img)
    x = 610
    d.text((x, 190), "High-Performance", font=font(78), fill=FG)
    d.text((x, 280), "AI Lab", font=font(78), fill=FG)
    d.text((x, 420), "Memory-first LLM infrastructure,", font=font(40), fill=TEAL)
    d.text((x, 472), "measured end to end.", font=font(40), fill=TEAL)
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
