#!/usr/bin/env python3
"""og.png 1200x630 — Shibuya Sushi & Bar — 'lantern & ink' poster.
Warm charcoal ink, torii vermillion disc, ochre rules, washi cream type. Shop identity only."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "og.png")

INK = (22, 17, 15); INK2 = (36, 27, 22); CREAM = (245, 239, 227)
VER = (200, 64, 47); VER_D = (163, 49, 35); OCHRE = (201, 144, 67); GOLD = (217, 169, 92)
SAND = (138, 122, 104)

def font(paths, size):
    bases = ["/System/Library/Fonts/Supplemental/", "/System/Library/Fonts/"]
    for b in bases:
        for n in paths:
            p = b + n
            if os.path.exists(p):
                try: return ImageFont.truetype(p, size)
                except Exception: pass
    return ImageFont.load_default()

serif = lambda s: font(["Iowan Old Style.ttc", "Palatino.ttc", "Georgia.ttf", "Times New Roman.ttf"], s)
sans = lambda s: font(["Futura.ttc", "HelveticaNeue.ttc", "HelveticaNeue.ttc", "Arial.ttf"], s)
JP = font(["Hiragino Sans GB.ttc", "Osaka.ttc", "Apple LiGothic Medium.ttf"], 150)

img = Image.new("RGB", (W, H), INK)
d = ImageDraw.Draw(img)

# vermillion lantern disc, upper-center-right
cx, cy, r = 600, 300, 235
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=VER)
# kanji watermark inside disc (semi-transparent blend toward ink)
JK = (225, 120, 100)
try:
    bb = d.textbbox((0, 0), "渋谷", font=JP)
    d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1]), "渋谷", font=JP, fill=JK)
except Exception as e:
    print("no kanji glyph:", e)
# lantern ribs across the disc (ink hairlines)
for yy in range(cy - r + 40, cy + r - 30, 55):
    half = int(((r - abs(yy - cy)) ** 2 - 0) ** 0.5 * 0.94) if abs(yy - cy) < r else 0
    if half: d.line([(cx - half, yy), (cx + half, yy)], fill=(120, 38, 28), width=3)
# lower band
d.rectangle([0, 500, W, H], fill=INK2)
# ochre frame rules
d.rectangle([0, 0, W, 6], fill=OCHRE)
d.rectangle([0, H - 6, W, H], fill=OCHRE)

def center(text, f, y, fill, tracking=0):
    if tracking:
        widths = [d.textbbox((0, 0), ch, font=f)[2] - d.textbbox((0, 0), ch, font=f)[0] for ch in text]
        tw = sum(widths) + tracking * (len(text) - 1)
        x = (W - tw) / 2
        for ch, w in zip(text, widths):
            bb = d.textbbox((0, 0), ch, font=f)
            d.text((x - bb[0], y), ch, font=f, fill=fill)
            x += w + tracking
        return tw
    bb = d.textbbox((0, 0), text, font=f)
    d.text(((W - (bb[2] - bb[0])) / 2 - bb[0], y), text, font=f, fill=fill)
    return bb[2] - bb[0]

# kicker above disc
center("LEESBURG  ·  LOUDOUN COUNTY  ·  VIRGINIA", sans(24), 36, GOLD, tracking=6)
# brand over the disc
center("SHIBUYA", serif(150), 220, CREAM, tracking=4)
center("S U S H I   &   B A R", sans(34), 396, INK if False else CREAM, tracking=6)
# double rule
d.rectangle([W / 2 - 140, 458, W / 2 + 140, 461], fill=OCHRE)
d.rectangle([W / 2 - 140, 467, W / 2 + 140, 470], fill=OCHRE)
# identity line on the band
center("Izakaya  ·  Sushi  ·  Ramen  ·  Small Plates  ·  Sake", sans(26), 512, GOLD, tracking=3)
center("Now in soft opening — 101 S King St, Leesburg, VA  ·  (571) 918-0306", sans(21), 556, SAND if False else (170, 152, 130))

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, os.path.getsize(OUT), "bytes")
