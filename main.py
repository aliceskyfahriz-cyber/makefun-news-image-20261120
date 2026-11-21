#!/usr/bin/env python3
"""
News-image generator for the make.fun daily news-image bounty
"news-image-20261120" - "Sum up 20 November's world news in one image".

Draws a 1024x1024 PNG news infographic from scratch using only Pillow
shapes, lines, fills, gradients and text. No photographs, no logos,
no pasted images, no network access, no API keys.

Run:  python3 main.py
Writes output.png + entry.png next to this file, and /output/entry.png
when an /output directory exists (the make.fun harness path).
Deterministic: two runs write identical bytes.
"""

from PIL import Image, ImageDraw, ImageFont
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_LOCAL = os.path.join(HERE, "output.png")
OUT_ENTRY = os.path.join(HERE, "entry.png")
OUT_HARNESS = "/output/entry.png"

W, H = 1024, 1024

# ---- palette ------------------------------------------------------------
BG_TOP = (13, 21, 38)        # deep navy
BG_BOT = (10, 16, 30)
PANEL = (22, 35, 61)          # card navy
PANEL_LINE = (48, 68, 104)
HERO_PANEL = (24, 40, 70)
INK = (240, 244, 252)         # near-white
MUTED = (159, 176, 204)       # grey-blue
AMBER = (242, 183, 5)         # accent gold
TEAL = (45, 212, 191)
RED = (248, 113, 113)
BLUE = (96, 165, 250)
GREEN = (74, 222, 128)
PURPLE = (192, 132, 252)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(FONT_B if bold else FONT, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, fill, max_w, leading):
    lines = wrap(draw, text, fnt, max_w)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def rounded(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)


# ---- story data (20 Nov 2026 news; see sources.md for dates) ------------
HERO = {
    "rank": "01",
    "tag": "WAR  ·  KYIV",
    "headline": "Missiles hit Kyiv on Friday morning",
    "summary": ("Ballistic missiles struck bridges across Kyiv and started a fire "
                "in a three-storey building in the Obolonskyi district, mayor "
                "Vitali Klitschko said on Friday; a Reuters witness heard "
                "explosions in the early hours."),
    "sources": "Reuters  ·  Daily Baku",
}

STORIES = [
    {
        "rank": "02",
        "tag": "WEATHER  ·  INDIA",
        "headline": "Cyclone Akvan bears down on India's east coast",
        "summary": ("Severe Cyclone Akvan is due to cross the Odisha-Andhra coast "
                    "near Gopalpur by noon on Friday, winds 90-100 km/h; Odisha "
                    "has moved more than 80,000 people to safety."),
        "sources": "IMD  ·  The Hindu BusinessLine",
        "icon": "cyclone",
        "accent": TEAL,
    },
    {
        "rank": "03",
        "tag": "ENERGY  ·  HORMUZ",
        "headline": "Oil rises as Hormuz tanker mines rattle supply",
        "summary": ("Brent crude rose to $92.22 a barrel on Friday as Houthi "
                    "attacks on Riyadh and reports of tankers hitting mines in "
                    "the Strait of Hormuz revived fears over supply."),
        "sources": "Reuters",
        "icon": "oil",
        "accent": AMBER,
    },
    {
        "rank": "04",
        "tag": "TECH  ·  MARKETS",
        "headline": "Anthropic's record IPO closes; shares up 17%",
        "summary": ("Anthropic closed its Nasdaq debut at $97.17, up 17% on its "
                    "$83 IPO price, after raising $81.3bn in the largest IPO on "
                    "record; the offering closes on Friday."),
        "sources": "The Hindu BusinessLine  ·  CoinStats",
        "icon": "chart",
        "accent": GREEN,
    },
    {
        "rank": "05",
        "tag": "TRADE  ·  SOUTH KOREA",
        "headline": "South Korea's exports pass $1 trillion",
        "summary": ("Cumulative exports crossed $1 trillion for the first time, "
                    "the trade ministry said, driven by AI chip demand; "
                    "President Lee Jae Myung hailed the milestone on Friday."),
        "sources": "Aju Press  ·  MarketBriefLine",
        "icon": "ship",
        "accent": BLUE,
    },
]


# ---- icons (shapes only) -------------------------------------------------
def icon_burst(d, cx, cy, r, col):
    # missile-burst star over city bars
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else int(r * 0.45)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, outline=col, width=4)
    d.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=col)
    base = cy + r + 16
    for i, h in enumerate([22, 38, 28, 46, 26]):
        x0 = cx - 58 + i * 25
        d.rectangle([x0, base - h, x0 + 17, base], fill=col)


def icon_cyclone(d, cx, cy, r, col):
    # spiral: concentric arcs shrinking inward
    for k, rr in enumerate((r, int(r * 0.72), int(r * 0.45))):
        start = 20 + k * 55
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr],
              start=start, end=start + 270, fill=col, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=col)


def icon_oil(d, cx, cy, r, col):
    # oil droplet + flame
    d.polygon([(cx, cy - r), (cx + int(r * 0.62), cy + int(r * 0.1)),
               (cx, cy + r), (cx - int(r * 0.62), cy + int(r * 0.1))],
              outline=col, width=5)
    d.ellipse([cx - int(r * 0.62), cy - int(r * 0.1),
               cx + int(r * 0.62), cy + r], outline=col, width=5)
    d.polygon([(cx, cy - r - 14), (cx + 12, cy - r + 8),
               (cx - 12, cy - r + 8)], fill=AMBER)
    d.line([cx - r - 8, cy + r + 14, cx + r + 8, cy + r + 14],
           fill=col, width=4)


def icon_chart(d, cx, cy, r, col):
    # rising bars + arrow
    base = cy + r
    for i, h in enumerate([int(r * 0.5), int(r * 0.85), int(r * 1.25)]):
        x0 = cx - r + i * int(r * 0.75)
        d.rectangle([x0, base - h, x0 + int(r * 0.5), base], fill=col)
    d.line([cx - r - 4, cy + int(r * 0.55), cx + r + 6, cy - r - 6],
           fill=AMBER, width=5)
    d.polygon([(cx + r + 6, cy - r - 6), (cx + r - 8, cy - r - 6),
               (cx + r + 6, cy - r + 8)], fill=AMBER)


def icon_ship(d, cx, cy, r, col):
    # stacked containers on a hull
    d.rectangle([cx - r, cy - int(r * 0.55), cx - 6, cy - 4], fill=col)
    d.rectangle([cx + 2, cy - int(r * 0.55), cx + r, cy - 4], fill=AMBER)
    d.rectangle([cx - int(r * 0.7), cy, cx + int(r * 0.7), cy + int(r * 0.35)],
                fill=col)
    d.polygon([(cx - r - 6, cy + int(r * 0.35)), (cx + r + 6, cy + int(r * 0.35)),
               (cx + int(r * 0.6), cy + int(r * 0.8)),
               (cx - int(r * 0.6), cy + int(r * 0.8))], fill=col)
    d.line([cx - r - 10, cy + r + 8, cx + r + 10, cy + r + 8],
           fill=MUTED, width=3)


ICONS = {"cyclone": icon_cyclone, "oil": icon_oil,
         "chart": icon_chart, "ship": icon_ship}


# ---- build ----------------------------------------------------------------
def build():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    # vertical gradient background
    for y in range(H):
        t = y / H
        col = tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3))
        d.line([(0, y), (W, y)], fill=col)
    # faint decorative dots
    for gx in range(60, W - 40, 46):
        for gy in (118, 136):
            d.ellipse([gx, gy, gx + 3, gy + 3], fill=(30, 46, 78))

    # ---- header ---------------------------------------------------------
    d.text((36, 26), "THE WORLD IN ONE DAY", font=font(38, bold=True), fill=INK)
    d.text((36, 76), "FRIDAY  ·  20 NOVEMBER 2026",
           font=font(18, bold=True), fill=AMBER)
    d.text((W - 36, 34), "GLOBAL EDITION", font=font(17, bold=True),
           fill=MUTED, anchor="ra")
    d.text((W - 36, 62), "5 stories  ·  Friday 20 Nov 2026",
           font=font(14), fill=MUTED, anchor="ra")
    d.line([(36, 112), (W - 36, 112)], fill=AMBER, width=3)

    # ---- hero story -----------------------------------------------------
    hx, hy, hw, hh = 36, 128, 952, 252
    rounded(d, [hx, hy, hx + hw, hy + hh], 18, fill=HERO_PANEL,
            outline=PANEL_LINE, width=2)
    ix, iy, iw, ih = hx + 22, hy + 22, 196, 208
    rounded(d, [ix, iy, ix + iw, iy + ih], 14, fill=(16, 28, 52))
    icon_burst(d, ix + iw // 2, iy + 82, 52, RED)
    d.text((ix + iw // 2, iy + ih - 24), "KYIV  ·  FRIDAY",
           font=font(14, bold=True), fill=RED, anchor="ma")
    tx = hx + 242
    d.text((tx, hy + 22), "01  ·  WAR", font=font(15, bold=True), fill=RED)
    y = draw_text_block(d, tx, hy + 48, HERO["headline"], font(27, bold=True),
                        INK, 688, 34)
    y = draw_text_block(d, tx, y + 8, HERO["summary"], font(16),
                        (205, 216, 235), 688, 23)
    d.text((tx, hy + hh - 30), "Sources:  " + HERO["sources"],
           font=font(13), fill=MUTED)

    # ---- grid of 4 stories ----------------------------------------------
    gx0, gy0 = 36, 404
    cw, ch, gap = 466, 236, 20
    for i, s in enumerate(STORIES):
        x = gx0 + (i % 2) * (cw + gap)
        y = gy0 + (i // 2) * (ch + gap)
        rounded(d, [x, y, x + cw, y + ch], 16, fill=PANEL,
                outline=PANEL_LINE, width=2)
        d.line([(x, y + 4), (x, y + ch - 4)], fill=s["accent"], width=5)
        ix, iy = x + 18, y + 18
        rounded(d, [ix, iy, ix + 96, iy + 96], 12, fill=(16, 28, 52))
        ICONS[s["icon"]](d, ix + 48, iy + 48, 30, s["accent"])
        tx = x + 130
        d.text((tx, y + 14), f"{s['rank']}  ·  {s['tag']}",
               font=font(12, bold=True), fill=s["accent"])
        yy = draw_text_block(d, tx, y + 36, s["headline"], font(17, bold=True),
                             INK, 322, 22)
        draw_text_block(d, tx, yy + 5, s["summary"], font(12),
                        (205, 216, 235), 322, 17)
        d.text((tx, y + ch - 24), "Sources:  " + s["sources"],
               font=font(11), fill=MUTED)

    # ---- footer ---------------------------------------------------------
    d.line([(36, 920), (W - 36, 920)], fill=PANEL_LINE, width=2)
    d.text((36, 934),
           "Sources: Reuters  ·  Daily Baku  ·  India Meteorological Dept  ·  "
           "The Hindu BusinessLine",
           font=font(12), fill=MUTED)
    d.text((36, 956),
           "Aju Press  ·  MarketBriefLine  ·  CoinStats  —  full sources and "
           "first-publication dates in sources.md",
           font=font(12), fill=MUTED)
    d.text((36, 984),
           "All graphics are drawn from shapes, lines and text only - "
           "no photographs.",
           font=font(12), fill=MUTED)

    img.save(OUT_LOCAL, "PNG")
    img.save(OUT_ENTRY, "PNG")
    if os.path.isdir("/output"):
        img.save(OUT_HARNESS, "PNG")
    return OUT_LOCAL


if __name__ == "__main__":
    path = build()
    print("wrote", path, os.path.getsize(path), "bytes")
