# gen.py — renders entry.png (1024x1024) for news-image-20261125, b121-numbers.
# NUMBERS front page: 50 stories, Wednesday 25 November 2026.
# Build-time only (PIL). main.py stays stdlib-only and copies entry.png.
import hashlib
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (17, 17, 17)
WHITE = (255, 255, 255)
RED = (192, 57, 43)
DARKRED = (140, 30, 22)
BLUE = (31, 78, 121)
NAVY = (20, 33, 61)
GOLD = (176, 124, 24)
GREEN = (39, 120, 70)
GREY = (90, 88, 80)
LINE = (40, 38, 34)
LIGHT = (232, 227, 214)
SKY = (214, 230, 240)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FM = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
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


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


# ---------------- DATA: 50 stories = 3 heroes + 10 cards + 37 ALSO ----------------
HEROES = [
    {
        "kicker": "TRADE WAR • WASHINGTON",
        "badge": "20%",
        "badge_sub": "CHINA TARIFF",
        "headline": "Trump hikes tariffs on 14 trade partners",
        "deck": "China hit at 20%, EU at 15%, Vietnam at 20%. Levies take effect in January.",
        "why": "WHY IT MATTERS: Higher import costs land on AI hardware, cars and groceries.",
        "tag": "C",
        "scene": "tariff",
    },
    {
        "kicker": "MARKETS • SEOUL",
        "badge": "-6.16%",
        "badge_sub": "KOSPI",
        "headline": "Kospi crashes as AI sell-off hits Seoul",
        "deck": "Samsung -9.9%, SK Hynix -11.1%. Circuit breaker trips. Foreigners sell KRW 1.95tn.",
        "why": "WHY IT MATTERS: The AI trade unwinds in Asia first — chip giants drag the whole region down.",
        "tag": "R",
        "scene": "kospi",
    },
    {
        "kicker": "SPACE • JIUQUAN",
        "badge": "40",
        "badge_sub": "YEARS OLD",
        "headline": "First foreign astronaut joins Tiangong station",
        "deck": "Shenzhou-24 carries Muhammad Zeeshan Ali of Pakistan, 40, to China's space station.",
        "why": "WHY IT MATTERS: A new space club opens — Tiangong takes its first guest from abroad.",
        "tag": "CL",
        "scene": "space",
    },
]

CARDS = [
    {"badge": "-4.5%", "tag": "R", "head": "Nasdaq plunges as AI rout deepens",
     "detail": "Nvidia -5%, Micron -6%, Marvell -6% before Thanksgiving pause.", "scene": "down"},
    {"badge": "4.3%", "tag": "C", "head": "US economy grows at fastest pace in 3 years",
     "detail": "Q3 GDP revised up from 3.4% as consumers keep spending.", "scene": "up"},
    {"badge": "3.8%", "tag": "C", "head": "Inflation lands in line at 3.8% a year",
     "detail": "October PCE rises 0.3% on the month; Fed meets in early December.", "scene": "gauge"},
    {"badge": "189K", "tag": "C", "head": "Jobless claims fall more than expected",
     "detail": "Initial claims down 13,000 to 189,000 in week to Nov 21.", "scene": "jobs"},
    {"badge": "$58,400", "tag": "R", "head": "Bitcoin slides with the risk sell-off",
     "detail": "Crypto drops as metals fall and investors dump risk assets.", "scene": "coin"},
    {"badge": "9 / 17", "tag": "R", "head": "Bogor gold mine floods: 9 dead, 17 trapped",
     "detail": "Rescue teams reach the flooded shaft as families wait at the gate.", "scene": "mine"},
    {"badge": "1", "tag": "C", "head": "Hamas security chief killed in Gaza strike",
     "detail": "Top security figure dies as ceasefire talks grind on in Cairo.", "scene": "gaza"},
    {"badge": "9,500 lbs", "tag": "R", "head": "Iowa troopers seize 9,500 lbs in bust",
     "detail": "Highway stop nets one of the state's biggest hauls this year.", "scene": "seize"},
    {"badge": "3rd", "tag": "C", "head": "Bank of Korea hikes rates a third time",
     "detail": "AI boom fuels growth as inflation stays well above target.", "scene": "bank"},
    {"badge": "4.9%", "tag": "C", "head": "Australia inflation surges to 4.9%",
     "detail": "October CPI keeps the Reserve Bank on alert for more hikes.", "scene": "gauge"},
]

ALSO = [
    ("R", "Dell slides 5% despite beating estimates"),
    ("R", "Anthropic drops 5% to near $78"),
    ("C", "WTI crude up 0.6% to $82.51 a barrel"),
    ("C", "10-year Treasury yield at 4.842%"),
    ("C", "Durable goods orders +0.2% to $346.7bn in October"),
    ("C", "Venezuela reveals an eye-popping debt load of $237bn"),
    ("CL", "EU lays out a plan to boost quantum technology"),
    ("R", "Copper slumps amid the AI roller coaster"),
    ("C", "Dimon cools on Britain after tax rise hits JPMorgan"),
    ("C", "Bank of Canada: inflation to remain persistent"),
    ("CL", "Musk would gain most from SpaceX-Tesla merger"),
    ("C", "OPEC+ meets this weekend as supply surplus looms"),
    ("C", "Fed beige book: input costs outpace selling prices"),
    ("C", "BOE's Bailey sees lower inflation peak if energy holds"),
    ("C", "World trade flows surge on AI goods despite barriers"),
    ("R", "AI bust could hit harder than dot-com crash"),
    ("C", "Next tariff fight takes shape as US-China truce frays"),
    ("C", "Nasdaq futures -2.8%, S&P -1.9%, Dow -1.2%"),
    ("R", "Gold, silver, platinum all fall in sell-off"),
    ("CL", "Thanksgiving: US markets shut Thursday"),
    ("C", "Tokyo: Nikkei follows Kospi lower on AI doubts"),
    ("C", "Taipei: chip shares slide with the global AI rout"),
    ("C", "Cairo: talks focus on Gaza ceasefire next steps"),
    ("CL", "Cartagena: Colombia hosts a regional trade summit"),
    ("CL", "Madrid: Spain pushes its EU quantum funding bid"),
    ("CL", "Honiara: Solomons weigh Pacific aid offers"),
    ("CL", "Damascus: aid convoys resume after a pause"),
    ("C", "New York: Thanksgiving travel hits record volumes"),
    ("C", "Washington: December Fed hike now widely expected"),
    ("R", "Seoul: retail investors buy the dip as the Kospi falls"),
    ("CL", "Jiuquan: Shenzhou-24 crew docks with Tiangong station"),
    ("C", "Gaza: aid crossings open for a third straight day"),
    ("C", "Iowa: harvest wraps as corn futures hold steady"),
    ("R", "Bogor: rescue teams reach the flooded gold mine"),
    ("C", "Chile copper miners miss out as prices surge"),
    ("R", "Why cheaper crude will not mean cheap gas in 2027"),
    ("C", "Stubborn inflation a bigger threat than AI worries"),
]

STRIP = [
    ("-6.16%", "KOSPI"),
    ("20%", "CHINA TARIFF"),
    ("4.3%", "US GDP Q3"),
    ("3.8%", "PCE INFLATION"),
    ("189K", "JOBLESS CLAIMS"),
    ("$58,400", "BITCOIN"),
]

PINS = ["Washington", "Seoul", "Jiuquan", "Taipei", "Tokyo", "Gaza", "Cairo",
        "Cartagena", "New York", "Madrid", "Bogor", "Iowa", "Honiara"]
PIN_XY = {"Washington": (0.22, 0.30), "Seoul": (0.83, 0.28), "Jiuquan": (0.76, 0.24),
          "Taipei": (0.85, 0.38), "Tokyo": (0.90, 0.30), "Gaza": (0.55, 0.38),
          "Cairo": (0.52, 0.44), "Cartagena": (0.28, 0.58), "New York": (0.26, 0.26),
          "Madrid": (0.44, 0.28), "Bogor": (0.80, 0.62), "Iowa": (0.20, 0.36),
          "Honiara": (0.92, 0.68)}


# ---------------- SCENES (each drawn on its own layer, exact box size) ----------------
def layer(w, h, bg):
    img = Image.new("RGB", (w, h), bg)
    return img, ImageDraw.Draw(img)


def scene_tariff(w, h):
    img, d = layer(w, h, SKY)
    d.text((10, 1), "14 PARTNERS", font=font(FB, 13), fill=INK)
    d.text((w - 34, 0), "%", font=font(FB, 26), fill=RED)
    cols = [(192, 57, 43), (31, 120, 70), (176, 124, 24), (31, 78, 121)]
    bw = 48
    for row in range(2):
        y0 = 18 + row * 9
        for c in range(4):
            x0 = 14 + c * (bw + 4)
            d.rectangle([x0, y0, x0 + bw, y0 + 8], fill=cols[(c + row) % 4],
                        outline=(255, 255, 255))
    d.rectangle([0, h - 10, w, h], fill=(31, 78, 121))
    d.polygon([(8, h - 10), (26, h - 22), (w - 26, h - 22), (w - 8, h - 10)],
              fill=(60, 60, 60))
    return img


def scene_kospi(w, h):
    img, d = layer(w, h, (24, 24, 28))
    pts = [(8, 8), (50, 12), (92, 10), (134, 20), (176, 18), (218, 28), (260, 26), (302, 40)]
    d.line(pts, fill=RED, width=3)
    for (x, y) in pts:
        d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 255, 255))
    d.text((10, h - 20), "-6.16%", font=font(FB, 15), fill=(255, 90, 70))
    d.text((w - 128, 3), "CIRCUIT BREAKER", font=font(FB, 11), fill=(255, 200, 60))
    return img


def scene_space(w, h):
    img, d = layer(w, h, (10, 16, 44))
    import random
    rnd = random.Random(25)
    for _ in range(40):
        x, y = rnd.randint(0, w - 1), rnd.randint(0, h - 1)
        d.ellipse([x, y, x + 2, y + 2], fill=(255, 255, 255))
    d.polygon([(150, 8), (162, 44), (138, 44)], fill=(230, 230, 230))
    d.rectangle([140, 44, 160, 62], fill=RED)
    d.polygon([(140, 62), (152, 84), (160, 62)], fill=(255, 170, 40))
    d.ellipse([w - 84, 12, w - 24, 52], fill=(200, 210, 225))
    d.rectangle([w - 150, h - 34, w - 100, h - 22], fill=(120, 130, 150))
    d.text((12, h - 30), "SHENZHOU-24", font=font(FB, 15), fill=(255, 255, 255))
    return img


def mini_scene(kind, w, h):
    if kind == "down":
        img, d = layer(w, h, (24, 24, 28))
        d.line([(4, 6), (w // 3, h // 2), (2 * w // 3, h // 2 - 4), (w - 6, h - 6)],
               fill=RED, width=3)
        d.text((6, h - 18), "▼", font=font(FB, 12), fill=(255, 90, 70))
        return img
    if kind == "up":
        img, d = layer(w, h, (16, 60, 32))
        d.line([(4, h - 6), (w // 3, h // 2), (2 * w // 3, h // 2 + 2), (w - 6, 6)],
               fill=(90, 220, 130), width=3)
        d.text((6, 4), "▲", font=font(FB, 12), fill=(140, 240, 160))
        return img
    if kind == "gauge":
        img, d = layer(w, h, (240, 234, 220))
        d.arc([8, 6, w - 8, h + 14], 180, 360, fill=RED, width=5)
        d.line([(w // 2, h - 8), (w // 2 + 22, 12)], fill=INK, width=3)
        return img
    if kind == "jobs":
        img, d = layer(w, h, SKY)
        for i, bx in enumerate([8, 30, 52]):
            d.rectangle([bx, h - 8 - i * 5, bx + 16, h - 4], fill=BLUE)
        return img
    if kind == "coin":
        img, d = layer(w, h, (250, 220, 120))
        d.ellipse([w // 2 - 14, 4, w // 2 + 14, h - 4], fill=GOLD, outline=(120, 80, 0), width=2)
        d.text((w // 2 - 7, h // 2 - 10), "₿", font=font(FB, 18), fill=(120, 80, 0))
        return img
    if kind == "mine":
        img, d = layer(w, h, (90, 60, 40))
        d.polygon([(w // 2 - 26, h - 4), (w // 2, 6), (w // 2 + 26, h - 4)], fill=(30, 20, 12))
        d.rectangle([0, h - 10, w, h], fill=(40, 120, 200))
        return img
    if kind == "gaza":
        img, d = layer(w, h, (235, 225, 200))
        for i, bx in enumerate([6, 30, 54, 78]):
            d.rectangle([bx, h - 12 - (i % 2) * 6, bx + 18, h - 4], fill=(150, 140, 120))
        return img
    if kind == "seize":
        img, d = layer(w, h, (220, 225, 235))
        d.rectangle([6, h - 8, w - 6, h - 4], fill=(60, 60, 60))
        d.rectangle([w // 2 - 18, 3, w // 2 + 18, h - 8], fill=(200, 170, 90), outline=INK)
        return img
    if kind == "bank":
        img, d = layer(w, h, (235, 230, 215))
        d.polygon([(8, 8), (w // 2, 1), (w - 8, 8)], fill=NAVY)
        for bx in [14, w // 2 - 6, w - 26]:
            d.rectangle([bx, 10, bx + 12, h - 4], fill=NAVY)
        return img
    img, d = layer(w, h, LIGHT)
    d.ellipse([w // 2 - 12, 6, w // 2 + 12, h - 6], fill=RED)
    return img


def draw_badge(d, x, y, text, fnt, fg, bg, pad=7):
    tw = d.textlength(text, font=fnt)
    bw = int(tw) + pad * 2
    bh = fnt.size + pad
    d.rounded_rectangle([x, y, x + bw, y + bh], radius=4, fill=bg)
    d.text((x + pad, y + pad // 2), text, font=fnt, fill=fg)
    return bw, bh


def draw_tag(d, x, y, tag):
    f = font(FB, 11)
    tw = d.textlength(tag, font=f)
    bw = int(tw) + 10
    d.rounded_rectangle([x, y, x + bw, y + 17], radius=3, outline=INK, width=1)
    d.text((x + 5, y + 2), tag, font=f, fill=INK)
    return bw


# ---------------- RENDER ----------------
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 14

    # header
    d.text((mx, 10), "THE WORLD IN NUMBERS", font=font(FB, 40), fill=INK)
    d.text((W - mx - text_w(d, "WEDNESDAY, 25 NOVEMBER 2026", font(FB, 15)), 16),
           "WEDNESDAY, 25 NOVEMBER 2026", font=font(FB, 15), fill=RED)
    d.text((W - mx - text_w(d, "50 STORIES • ONE PAGE", font(FB, 12)), 38),
           "50 STORIES • ONE PAGE", font=font(FB, 12), fill=GREY)
    d.line([mx, 56, W - mx, 56], fill=INK, width=3)

    # heroes
    hw, gap, hy, hh = 326, 9, 60, 232
    scenes = {"tariff": scene_tariff, "kospi": scene_kospi, "space": scene_space}
    for i, hero in enumerate(HEROES):
        x = mx + i * (hw + gap)
        d.rounded_rectangle([x, hy, x + hw, hy + hh], radius=6, fill=WHITE, outline=LINE, width=2)
        d.text((x + 10, hy + 8), hero["kicker"], font=font(FB, 11), fill=RED)
        bw, _ = draw_badge(d, x + hw - 10 - (int(text_w(d, hero["badge"], font(FB, 20))) + 14),
                           hy + 6, hero["badge"], font(FB, 20), WHITE, RED)
        assert x + 10 + bw <= x + hw - 4, "hero badge overflows card"
        d.text((x + 10, hy + 34), hero["badge_sub"], font=font(FB, 10), fill=GREY)
        lines = wrap(d, hero["headline"], font(FB, 21), hw - 20)[:3]
        yy = hy + 50
        for ln in lines:
            d.text((x + 10, yy), ln, font=font(FB, 21), fill=INK)
            yy += 24
        deck = wrap(d, hero["deck"], font(FR, 12), hw - 20)[:2]
        yy += 2
        for ln in deck:
            d.text((x + 10, yy), ln, font=font(FR, 12), fill=(50, 48, 44))
            yy += 15
        scene = scenes[hero["scene"]](hw - 20, 44)
        img.paste(scene, (x + 10, hy + 148))
        why = wrap(d, hero["why"], font(FR, 11), hw - 20)
        yy = hy + 198
        for ln in why[:2]:
            d.text((x + 10, yy), ln, font=font(FR, 11), fill=INK)
            yy += 14
        draw_tag(d, x + hw - 34, hy + hh - 24, hero["tag"])

    # DATE CHECK band
    dy = 298
    d.rectangle([mx, dy, W - mx, dy + 40], fill=NAVY)
    l1 = "DATE CHECK — LEFT OUT: Huawei verdict 24 Nov  •  PIF Tower attack 24 Nov"
    l2 = "Sudan strikes 24 Nov  •  Nvidia CEO reinstated 23 Nov  —  NOT 25 NOV"
    d.text((mx + 10, dy + 3), l1, font=font(FB, 13), fill=(255, 255, 255))
    d.text((mx + 10, dy + 21), l2, font=font(FB, 13), fill=(255, 210, 90))
    assert text_w(d, l1, font(FB, 13)) <= W - 2 * mx - 20, "DATE CHECK line 1 too wide"
    assert text_w(d, l2, font(FB, 13)) <= W - 2 * mx - 20, "DATE CHECK line 2 too wide"

    # number strip, 6 cells
    sy, sh = 344, 48
    cw = (W - 2 * mx - 5 * 4) // 6
    for i, (num, lab) in enumerate(STRIP):
        x = mx + i * (cw + 4)
        d.rounded_rectangle([x, sy, x + cw, sy + sh], radius=5, fill=WHITE, outline=LINE, width=1)
        d.text((x + (cw - text_w(d, num, font(FB, 24))) / 2, sy + 3), num,
               font=font(FB, 24), fill=RED)
        d.text((x + (cw - text_w(d, lab, font(FB, 10))) / 2, sy + 31), lab,
               font=font(FB, 10), fill=INK)

    # grid cards 5x2
    gy, gh, gw, ggap = 398, 109, 192, 8
    gx0 = mx + 2
    for i, card in enumerate(CARDS):
        r, c = divmod(i, 5)
        x = gx0 + c * (gw + ggap)
        y = gy + r * (gh + 6)
        d.rounded_rectangle([x, y, x + gw, y + gh], radius=5, fill=WHITE, outline=LINE, width=1)
        bw, _ = draw_badge(d, x + 7, y + 6, card["badge"], font(FB, 14), WHITE, BLUE)
        assert x + 7 + bw <= x + gw - 4, "badge overflows card"
        draw_tag(d, x + gw - 32, y + 7, card["tag"])
        sc = mini_scene(card["scene"], gw - 14, 22)
        img.paste(sc, (x + 7, y + 31))
        lines = wrap(d, card["head"], font(FB, 12), gw - 14)[:2]
        yy = y + 57
        for ln in lines:
            d.text((x + 7, yy), ln, font=font(FB, 12), fill=INK)
            yy += 13
        det = wrap(d, card["detail"], font(FR, 10), gw - 14)[:2]
        for ln in det:
            d.text((x + 7, yy), ln, font=font(FR, 10), fill=(60, 58, 52))
            yy += 11

    # ALSO + map
    ay = 628
    d.text((mx, ay), "ALSO — 37 MORE STORIES", font=font(FB, 13), fill=INK)
    d.line([mx, ay + 20, 650, ay + 20], fill=INK, width=2)
    col_w, col_gap = 312, 12
    cols = [ALSO[:19], ALSO[19:]]

    def also_end_y(size, lh):
        end = ay + 28
        for col in cols:
            yy = ay + 28
            for tag, text in col:
                lines = wrap(d, text, font(FR, size), col_w - 24)
                yy += len(lines[:2]) * lh + 1
            end = max(end, yy)
        return end

    fsize, lh = 11, 14
    for size, lh_try in [(11, 14), (10, 13), (9, 12)]:
        if also_end_y(size, lh_try) <= 972:
            fsize, lh = size, lh_try
            break
    else:
        raise AssertionError("ALSO columns do not fit even at 9pt")
    for ci, col in enumerate(cols):
        cx = mx + ci * (col_w + col_gap)
        yy = ay + 28
        for tag, text in col:
            lines = wrap(d, text, font(FR, fsize), col_w - 24)
            d.text((cx, yy), tag, font=font(FB, fsize), fill=RED)
            for ln in lines[:2]:
                d.text((cx + 24, yy), ln, font=font(FR, fsize), fill=INK)
                yy += lh
            yy += 1
        assert yy <= 972, "ALSO column overflows"

    # map box
    mx0, my0, mw, mh = 662, ay, 348, 344
    d.rounded_rectangle([mx0, my0, mx0 + mw, my0 + mh], radius=6, fill=WHITE, outline=LINE, width=2)
    d.text((mx0 + 10, my0 + 8), "WHERE IT HAPPENED — 13 PINS", font=font(FB, 12), fill=INK)
    map_x, map_y, map_w, map_h = mx0 + 10, my0 + 32, mw - 20, 168
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=(210, 226, 238))
    d.ellipse([map_x + 8, map_y + 30, map_x + 150, map_y + 120], fill=(235, 225, 200))
    d.ellipse([map_x + 170, map_y + 20, map_x + 300, map_y + 110], fill=(235, 225, 200))
    d.ellipse([map_x + 200, map_y + 110, map_x + 290, map_y + 160], fill=(235, 225, 200))
    d.ellipse([map_x + 40, map_y + 105, map_x + 120, map_y + 155], fill=(235, 225, 200))
    for n, name in enumerate(PINS, 1):
        fx, fy = PIN_XY[name]
        px = map_x + int(fx * map_w)
        py = map_y + int(fy * map_h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=WHITE, width=2)
        d.text((px - 3, py - 6), str(n), font=font(FB, 9), fill=WHITE)
    ly = my0 + 212
    for i in range(0, 13, 2):
        left = f"{i + 1}. {PINS[i]}"
        d.text((mx0 + 10, ly), left, font=font(FR, 10), fill=INK)
        if i + 1 < 13:
            right = f"{i + 2}. {PINS[i + 1]}"
            d.text((mx0 + 180, ly), right, font=font(FR, 10), fill=INK)
        ly += 15
    d.text((mx0 + 10, my0 + mh - 22), "13 places behind the 50 stories.",
           font=font(FR, 10), fill=GREY)

    # footer
    d.line([mx, 978, W - mx, 978], fill=INK, width=2)
    d.text((mx, 984), "Sources: Reuters  •  AP  •  BBC  •  CNN  •  Xinhua  •  Korea Exchange  •  pm.gov.au",
           font=font(FR, 11), fill=INK)
    d.text((mx, 1000), "THE WORLD IN NUMBERS — WEDNESDAY 25 NOVEMBER 2026 — 50 STORIES, ALL COUNTED.",
           font=font(FB, 10), fill=GREY)
    return img


def main():
    assert len(HEROES) + len(CARDS) + len(ALSO) == 50, "story count != 50"
    assert len(PINS) == 13, "pin count != 13"
    img = render()
    assert img.size == (1024, 1024)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    if size > 1_048_576:
        img.convert("P", palette=Image.ADAPTIVE, colors=256).convert("RGB").save(out, optimize=True)
        size = os.path.getsize(out)
    sha = hashlib.sha256(open(out, "rb").read()).hexdigest()
    print(f"entry.png bytes={size} sha256={sha}")
    print(f"stories={len(HEROES) + len(CARDS) + len(ALSO)} heroes={len(HEROES)} "
          f"cards={len(CARDS)} also={len(ALSO)} pins={len(PINS)}")
    assert size <= 1_048_576, "entry.png over 1 MiB"


if __name__ == "__main__":
    main()
