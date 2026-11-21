#!/usr/bin/env python3
"""Render the news-image-20261120 entry: one 1024x1024 infographic summing up
the world news of Friday, 20 November 2026. Deterministic output (fixed
layout, fixed fonts, no timestamps inside the image)."""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 36  # margin
PAPER = (247, 243, 234)
INK = (22, 22, 22)
MUTED = (96, 94, 88)
NAVY = (20, 33, 61)
RED = (178, 44, 34)
TEAL = (14, 107, 107)
GOLD = (166, 110, 20)
CARD = (255, 255, 255)
LINE = (205, 200, 188)
STRIP = (236, 231, 219)

NOTO = "/usr/share/fonts/truetype/noto/"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(NOTO + "NotoSansDisplay-Black.ttf", 58)
F_DATE = font(NOTO + "NotoSans-Bold.ttf", 30)
F_KICK = font(NOTO + "NotoSans-Bold.ttf", 20)
F_LABEL = font(NOTO + "NotoSans-Bold.ttf", 22)
F_HERO = font(NOTO + "NotoSansDisplay-Black.ttf", 48)
F_SUM = font(NOTO + "NotoSans-Regular.ttf", 24)
F_CHIP = font(NOTO + "NotoSans-Bold.ttf", 19)
F_HEAD = font(NOTO + "NotoSans-Bold.ttf", 28)
F_BODY = font(NOTO + "NotoSans-Regular.ttf", 21)
F_STRIP = font(NOTO + "NotoSans-Regular.ttf", 21)
F_STRIP_B = font(NOTO + "NotoSans-Bold.ttf", 22)
F_FOOT = font(NOTO + "NotoSans-Regular.ttf", 18)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        words, cur = para.split(), ""
        for w in words:
            trial = (cur + " " + w).strip()
            if draw.textlength(trial, font=fnt) <= width:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# ---- Masthead ----
d.rectangle([0, 0, W, 118], fill=NAVY)
d.text((M, 30), "THE WORLD IN ONE PAGE", font=F_TITLE, fill=(255, 255, 255))
date_lines = ["FRIDAY,", "20 NOV 2026"]
y = 26
for ln in date_lines:
    tw = d.textlength(ln, font=F_DATE)
    d.text((W - M - tw, y), ln, font=F_DATE, fill=(255, 214, 90))
    y += 34

# ---- Kicker ----
d.text((M, 132), "THE DAY IN WORLD NEWS  ·  FROM WORLD WIRES",
       font=F_KICK, fill=MUTED)

# ---- Lead story ----
hy = 168
d.rectangle([M, hy, M + 10, hy + 216], fill=RED)
d.text((M + 26, hy), "LEAD STORY", font=F_LABEL, fill=RED)
hero = wrap(d, "Trump, Putin and Xi agree \u2018peace declaration\u2019 after historic meeting",
            F_HERO, W - 2 * M - 26)
y = draw_lines(d, hero, M + 26, hy + 34, F_HERO, INK, 54)
summary = wrap(d, "The three leaders issued a joint declaration after their first three-way "
               "talks, praised abroad and questioned at home in Washington.",
               F_SUM, W - 2 * M - 26)
draw_lines(d, summary, M + 26, y + 10, F_SUM, (60, 58, 52), 30)
d.line([M, 402, W - M, 402], fill=LINE, width=2)

# ---- 2x2 story grid ----
cards = [
    ("WORLD COURT", RED, "Myanmar committed genocide, top UN court rules",
     "The ICJ found Myanmar responsible for genocide against the Rohingya."),
    ("CLIMATE · COP31", TEAL, "Fossil fuels cut from COP31 draft deal",
     "Language on phasing out fossil fuels was scrubbed from the near-final text."),
    ("UKRAINE", NAVY, "Three Kyiv bridges hit in missile barrage",
     "Britain pledged 1,000+ drones in a \u00a3260m package as Russia vowed a \u2018painful\u2019 attack."),
    ("MARKETS", GOLD, "Anthropic lists in landmark AI debut",
     "The first purely AI company to go public, now among the world\u2019s most valuable."),
]
gx, gy = M, 420
cw, chh, gap = 464, 184, 24
for i, (tag, color, head, body) in enumerate(cards):
    x = gx + (i % 2) * (cw + gap)
    yy = gy + (i // 2) * (chh + gap)
    d.rectangle([x, yy, x + cw, yy + chh], fill=CARD, outline=LINE, width=2)
    # category chip
    tw = d.textlength(tag, font=F_CHIP)
    d.rectangle([x + 16, yy + 14, x + 16 + tw + 20, yy + 42], fill=color)
    d.text((x + 26, yy + 17), tag, font=F_CHIP, fill=(255, 255, 255))
    hl = wrap(d, head, F_HEAD, cw - 32)
    y2 = draw_lines(d, hl[:2], x + 16, yy + 54, F_HEAD, INK, 33)
    bl = wrap(d, body, F_BODY, cw - 32)
    draw_lines(d, bl[:2], x + 16, y2 + 6, F_BODY, (70, 68, 62), 26)

# ---- Also today strip ----
sy = 832
d.rectangle([M, sy, W - M, sy + 118], fill=STRIP)
d.text((M + 18, sy + 12), "ALSO TODAY", font=F_STRIP_B, fill=INK)
also = [
    ("UK and EU agree a youth mobility scheme in the post-Brexit reset.", RED),
    ("Trump posthumously pardons baseball legend Pete Rose.", TEAL),
    ("Van Gogh sells for a record $190.4m after an ownership dispute.", GOLD),
]
y = sy + 44
for text, color in also:
    d.ellipse([M + 18, y + 7, M + 28, y + 17], fill=color)
    d.text((M + 38, y), text, font=F_STRIP, fill=(50, 48, 44))
    y += 25

# ---- Footer ----
foot = "Compiled from world news wires  ·  All events first reported on Friday, 20 November 2026"
tw = d.textlength(foot, font=F_FOOT)
d.text(((W - tw) / 2, 972), foot, font=F_FOOT, fill=MUTED)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
