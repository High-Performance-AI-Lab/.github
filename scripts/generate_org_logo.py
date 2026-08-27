#!/usr/bin/env python3
"""Generate the High-Performance-AI-Lab brand assets.

Two deterministic outputs, no randomness, no external inputs:

- assets/org-logo.png          1024x1024 organization avatar
- assets/org-social-card.png     1200x630 social preview for this repo

The mark: three ascending compute lanes (teal -> blue, the family accent
range) under a rising trend line — everything inside the circle-mask safe
area. assets/org-logo.svg is the hand-maintained vector twin of the logo
geometry; keep the three artifacts in sync.

    python3 scripts/generate_org_logo.py --check   # verify committed files
    python3 scripts/generate_org_logo.py           # regenerate
"""

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BG = (13, 17, 23)          # deep charcoal, matches the family cards
TEAL = (63, 185, 170)
MID = (80, 172, 212)
BLUE = (98, 160, 255)
FG = (240, 246, 252)       # near-white
DIM = (139, 148, 158)      # muted grey

FONT_PATHS = [
    "/System/Library/Fonts/SFNS.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/SUPPLEMENTARY/Arial Bold.ttf",
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


BARS = [  # staircase bars, logo coordinates (1024x1024)
    (182, 700, 260, 150, TEAL),
    (382, 480, 260, 150, MID),
    (582, 260, 260, 150, BLUE),
]
TREND = [(192, 672), (392, 452), (592, 232), (796, 148)]
LINE_W = 40


def draw_mark(d: ImageDraw.ImageDraw, scale: float = 1.0, dx: int = 0, dy: int = 0) -> None:
    lw = max(4, round(LINE_W * scale))
    for x, y, w, h, color in BARS:
        x0, y0 = round(x * scale) + dx, round(y * scale) + dy
        d.rounded_rectangle([x0, y0, x0 + round(w * scale), y0 + round(h * scale)],
                            radius=round(44 * scale), fill=color)
    pts = [(round(x * scale) + dx, round(y * scale) + dy) for x, y in TREND]
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        d.line([x1, y1, x2, y2], fill=FG, width=lw)
    for x, y in pts:
        r = lw // 2
        d.ellipse([x - r, y - r, x + r, y + r], fill=FG)
    (hx, hy), (px_, py_) = pts[-1], pts[-2]
    ddx, ddy = hx - px_, hy - py_
    ln = (ddx * ddx + ddy * ddy) ** 0.5
    ux, uy = ddx / ln, ddy / ln
    qx, qy = -uy, ux
    wing = round(96 * scale)
    for side in (1, -1):
        d.line([hx, hy,
                round(hx + wing * (-ux + side * qx * 0.72)),
                round(hy + wing * (-uy + side * qy * 0.72))], fill=FG, width=lw)


def render_logo() -> Image.Image:
    img = Image.new("RGB", (1024, 1024), BG)
    draw_mark(ImageDraw.Draw(img))
    return img


def render_card() -> Image.Image:
    img = Image.new("RGB", (1200, 630), BG)
    d = ImageDraw.Draw(img)
    # mark at ~0.62 scale, vertically centered on the left
    draw_mark(d, scale=0.62, dx=-40, dy=110)
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
