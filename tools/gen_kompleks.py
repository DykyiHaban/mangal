# Usage: python tools/gen_kompleks.py  ->  kreslennia-kompleks.html, materialy.md, kreslennia/kompleks-*.svg
# Drawings of the whole grill zone (model v13) and the bill of materials.
# Units: mm. Plan: world x from the left edge of the paving, z from the rear edge. Heights from the paving.
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafting import View, PAGE_CSS, HEAD

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'kreslennia')
S = 100  # the whole rig is shifted 100 from the left post line

def gx(x):  # model-local x -> world x
    return x + S

def mesh_lines(v, x0, x1, y0, y1, step=100):
    for x in range(int(x0) + step, int(x1), step): v.line(x, y0, x, y1, 'hid')
    for y in range(int(y0) + step, int(y1), step): v.line(x0, y, x1, y, 'hid')

def stones(v, x0, x1, y0, y1):
    v.rect(x0, y0, x1, y1, 'stone')
    mesh_lines(v, x0, x1, y0, y1, 50 if (x1 - x0) < 400 else 100)
    v.rect(x0, y0, x1, y1, 'ol')

# ======================= 1. PLAN =======================
p = View(0, 3000, -160, 1500, pad=(190, 90, 90, 240), flip=False, k=2.6)
p.rect(0, 0, 3000, 1500, 'ol thin')
for x, z in ((0, 0), (2900, 0), (0, 1400), (2900, 1400)): p.rect(x, z, x + 100, z + 100, 'fill')
# part 1 mangal
p.rect(gx(100), 0, gx(900), 600)
p.rect(gx(173), 73, gx(827), 527, 'brick'); p.rect(gx(173), 73, gx(827), 527, 'ol thin')
for z0, z1 in ((0, 75), (525, 600)): p.rect(gx(100), z0, gx(900), z1, 'fill')
for x in (320, 380, 440, 500): p.line(gx(x), -40, gx(x), 640, 'ol thin')
p.text(gx(500), 310, 'мангал · частина 1', 'note', 'middle')
# gap + part 2 kazan
p.rect(gx(897), 0, gx(933), 600, 'ol thin')
p.rect(gx(930), 0, gx(1430), 600)
p.rect(gx(937), 7, gx(1423), 593, 'ol thin')
p.circle(gx(1180), 270, 170); p.circle(gx(1180), 270, 150, 'hid')
p.circle(gx(1180), -92, 55); p.text(gx(1180) + 70, -100, 'труба Ø110', 'note')
p.text(gx(1180), 520, 'казан · частина 2', 'note', 'middle')
# part 3: lid outline, gabions and fridge under it
lid = [(gx(1430), 0), (gx(2800), 0), (gx(2800), 1320), (gx(2080), 1320), (gx(2080), 620), (gx(1430), 620)]
p.poly(lid)
p.rect(gx(1430), 0, gx(1630), 600, 'hid'); p.text(gx(1530), 300, 'габіон', 'note', 'middle')
p.rect(gx(2100), 1100, gx(2600), 1300, 'hid'); p.text(gx(2350), 1215, 'габіон', 'note', 'middle')
p.rect(gx(2600), 0, gx(2800), 1300, 'hid'); p.text(gx(2700), 700, 'габіон', 'note', 'middle')
p.rect(gx(1645), 110, gx(2117), 556, 'hid'); p.text(gx(1880), 340, 'холодильник', 'note', 'middle')
p.rect(gx(2160), 660, gx(2540), 1040); p.rect(gx(2180), 680, gx(2520), 1020, 'ol thin')
p.circle(gx(2350), 850, 25, 'ol thin'); p.circle(gx(2600), 850, 18)
p.text(gx(2350), 1080, 'умивальник', 'note', 'middle')
p.text(gx(1800), 680, 'стільниця · частина 3', 'note', 'middle')
p.line(gx(2350), 560, gx(2350), 1360, 'cl'); p.text(gx(2350) + 8, 1390, 'А', 'ttl'); p.text(gx(2350) + 8, 590, 'А', 'ttl')
# dims
p.dimH(0, 3000, -140, ext_from=0)
p.dimH(0, 100, 1560, ext_from=1500); p.dimH(100, gx(100), 1560, '100'); p.dimH(gx(100), gx(900), 1560, '800')
p.dimH(gx(900), gx(930), 1640, '30', ext_from=600); p.dimH(gx(930), gx(1430), 1560, '500', ext_from=600)
p.dimH(gx(1430), gx(2800), 1560, '1370', ext_from=1320); p.dimH(gx(2800), 3000, 1560, '200')
p.dimH(gx(100), gx(2800), 1720, '2700')
p.dimV(0, 1500, -50, ext_from=0)
p.dimV(0, 600, gx(100) - 30, '600', ext_from=gx(100))
p.dimV(620, 1320, gx(2080) - 30, '700', ext_from=gx(2080))
p.dimH(gx(2080), gx(2800), 1360, '720', ext_from=1320)
p.dimH(gx(2160), gx(2540), 630, '380'); p.dimV(660, 1040, gx(2540) + 30, '380', side='right')
p.dimV(1040, 1320, gx(2540) + 30, '280', side='right')
plan_svg = p.svg('План')

# ======================= 2. FRONT ELEVATION =======================
f = View(0, 3000, 0, 1150, pad=(200, 220, 60, 280), k=2.6)
f.line(-60, 0, 3060, 0, 'ol')
for x in (0, 2900): f.rect(x, 0, x + 100, 1150, 'fill')
f.text(50, 1120, '', 'note')
def frame_front(x0, x1, top, rings):
    for x in (x0, x1 - 40): f.rect(x, 0, x + 40, top)
    for y in rings: f.rect(x0 + 40, y, x1 - 40, y + 40)
    f.rect(x0, 140, x1, 143, 'ol thin')
# mangal
frame_front(gx(100), gx(900), 498, (100, 458))
f.rect(gx(100), 498, gx(900), 800, 'fill')
f.rect(gx(100), 800, gx(900), 840, 'fill')
prev = gx(100)
for x in range(140, 861, 60):
    f.rect(prev, 840, gx(x) - 6, 850, 'fill'); prev = gx(x) + 6
f.rect(prev, 840, gx(900), 850, 'fill')
for x in (320, 380, 440, 500): f.circle(gx(x), 844, 4)
for x, y in ((250, 188), (350, 188), (450, 188), (550, 188), (650, 188), (750, 188), (300, 270), (400, 270), (500, 270), (600, 270), (700, 270)):
    f.circle(gx(x), y, 40, 'ol thin')
# kazan
frame_front(gx(930), gx(1430), 374, (100, 334))
f.rect(gx(934), 377, gx(1426), 750, 'brick')
f.rect(gx(930), 374, gx(1430), 377, 'ol thin')
for x in (gx(930), gx(1390)): f.rect(x, 377, x + 40, 796)
f.rect(gx(930), 756, gx(1430), 796)
for a in (995, 1325): f.rect(gx(a), 334, gx(a + 40), 756)
f.rect(gx(1040), 425, gx(1320), 695, 'fill')
f.rect(gx(937), 795, gx(1423), 800, 'ol thin')
pts = []
for i in range(0, 21):
    y = 800 + 80 * i / 20; hw = math.sqrt(max(0, 170 ** 2 - (880 - y) ** 2)); pts.append((gx(1180) - hw, y))
for i in range(20, -1, -1):
    y = 800 + 80 * i / 20; hw = math.sqrt(max(0, 170 ** 2 - (880 - y) ** 2)); pts.append((gx(1180) + hw, y))
f.poly(pts, 'fill'); f.rect(gx(1003), 876, gx(1357), 884, 'fill')
f.rect(gx(1125), 884, gx(1235), 1150, 'hid'); f.text(gx(1235) + 10, 1120, 'труба Ø110 до ≈ 2300', 'note')
# part 3
stones(f, gx(1430), gx(1630), 0, 730)
f.rect(gx(1630), 0, gx(2150), 60, 'fill'); f.rect(gx(1630), 600, gx(2132), 618, 'fill')
f.rect(gx(1645), 60, gx(2117), 552, 'ol thin'); f.text(gx(1880), 300, 'холодильник', 'note', 'middle')
stones(f, gx(2100), gx(2600), 0, 730)
stones(f, gx(2600), gx(2800), 0, 730)
f.rect(gx(1430), 730, gx(2800), 800, 'fill'); f.line(gx(1430), 790, gx(2800), 790, 'ol thin')
f.rect(gx(2582), 800, gx(2618), 1060, 'ol thin'); f.rect(gx(2410), 1040, gx(2618), 1064, 'ol thin')
# dims
for x0, x1 in ((0, 100), (100, 200), (gx(100), gx(900)), (gx(900), gx(930)), (gx(930), gx(1430)), (gx(1430), gx(1630)),
               (gx(1630), gx(2100)), (gx(2100), gx(2600)), (gx(2600), gx(2800)), (gx(2800), 3000)):
    f.dimH(x0, x1, -45, ext_from=0)
f.dimH(0, 3000, -170)
f.dimV(0, 800, gx(100) - 40, '800', ext_from=gx(100))
f.dimV(800, 850, gx(100) - 40, '50', side='left')
f.dimV(0, 498, gx(100) - 150, '498', ext_from=gx(100))
f.dimV(0, 730, gx(2800) + 40, '730', ext_from=gx(2800), side='right')
f.dimV(730, 800, gx(2800) + 40, '70', side='right')
f.dimV(0, 374, gx(1430) - 25, '374', ext_from=gx(1430), side='left')
front_svg = f.svg('Фасад')

# ======================= 3. SECTION A-A through the sink =======================
a = View(-50, 1500, 0, 1000, pad=(110, 200, 60, 120), k=1.9)
a.line(-50, 0, 1500, 0, 'ol')
a.rect(0, 0, 1100, 730, 'ol')
a.rect(0, 0, 20, 730, 'fill'); a.rect(0, 0, 1100, 60, 'fill')
a.text(300, 400, 'тумба (каркас і обшивка)', 'note', 'middle')
stones(a, 1100, 1300, 0, 730)
# lid layers
a.rect(-20 + 20, 730, 1320, 740, 'hid')
a.rect(0, 740, 660, 790, 'brick'); a.rect(1040, 740, 1320, 790, 'brick')
a.rect(0, 790, 660, 800, 'fill'); a.rect(1040, 790, 1320, 800, 'fill')
a.rect(0, 730, 3, 800, 'fill'); a.rect(1317, 730, 1320, 800, 'fill')
for z in range(50, 1320, 100):
    if not (660 < z < 1040): a.rect(z - 5, 730, z + 5, 740, 'fill')
# sink bowl
a.rect(660, 600, 1040, 800, 'ol'); a.line(660, 604, 1040, 604, 'ol thin')
a.rect(840, 520, 860, 600, 'ol thin'); a.text(870, 540, 'сифон', 'note')
# dims
a.dimH(0, 600, -40, ext_from=0); a.dimH(600, 1100, -40, '500'); a.dimH(1100, 1300, -40, '200')
a.dimH(0, 1320, 870, '1320 кришка', ext_from=800)
a.dimH(1300, 1320, 830, '20')
a.dimV(0, 730, 1400, '730', ext_from=1320, side='right'); a.dimV(730, 800, 1400, '70', side='right')
a.dimV(600, 800, 610, '200', ext_from=660, side='left')
a.dimH(660, 1040, 900, '380', ext_from=800)
a.text(1150, 960, 'зад ліворуч, перед праворуч', 'note', 'middle')
sect_svg = a.svg('Розріз А–А')

# ======================= 4. MANGAL front + section =======================
m = View(0, 800, 0, 860, pad=(130, 120, 60, 110), k=1.3)
for x in (0, 760): m.rect(x, 0, x + 40, 498)
for y in (100, 458): m.rect(40, y, 760, y + 40)
m.rect(0, 140, 800, 143, 'ol thin')
m.rect(0, 498, 800, 800)
m.rect(8, 501, 792, 800, 'hid')
m.rect(0, 800, 800, 806); m.rect(0, 806, 800, 840)
prev = 0
for x in range(140, 861, 60):
    m.rect(prev, 840, x - 6, 850); prev = x + 6
m.rect(prev, 840, 800, 850)
m.dimH(0, 800, -40, ext_from=0)
m.dimH(0, 140, 900, '140', ext_from=850); m.dimH(140, 200, 900, '60'); m.dimH(134, 146, 870, '12')
m.text(500, 905, '13 пропилів 12 × 10, крок 60', 'note', 'middle')
m.dimV(0, 498, -40, ext_from=0); m.dimV(498, 800, -40, '302'); m.dimV(800, 850, -40, '50')
m.dimV(0, 100, 840, '100', ext_from=800, side='right'); m.dimV(100, 140, 840, '40', side='right')
m.dimV(458, 498, 840, '40', side='right')
m.pos(1, 20, 250, -60, 300); m.pos(2, 400, 120, 400, 300); m.pos(3, 600, 141, 650, 300)
m.pos(4, 400, 650, 480, 720); m.pos(5, 300, 830, 260, 760)
mangal_front_svg = m.svg('Мангал спереду')

ms = View(0, 600, 0, 880, pad=(130, 130, 60, 110), k=1.3)
for z in (0, 560): ms.rect(z, 0, z + 40, 498)
for y in (100, 458): ms.rect(40, y, 560, y + 40)
ms.rect(0, 140, 600, 143, 'ol thin')
ms.rect(0, 498, 600, 501, 'ol'); ms.rect(0, 501, 3, 800); ms.rect(597, 501, 600, 800)
ms.rect(8, 501, 592, 566, 'brick'); ms.rect(8, 501, 592, 566, 'ol thin')
for z0, z1 in ((8, 73), (527, 592)):
    ms.rect(z0, 569, z1, 800, 'brick'); ms.rect(z0, 569, z1, 800, 'ol thin'); ms.line(z0, 685, z1, 685, 'ol thin')
ms.poly([(0, 800), (75, 800), (75, 806), (6, 806), (6, 850), (0, 850)], 'fill')
ms.poly([(600, 800), (525, 800), (525, 806), (594, 806), (594, 850), (600, 850)], 'fill')
ms.line(-30, 844, 630, 844, 'ol'); ms.text(300, 856, 'шампур на 840', 'note', 'middle')
ms.rect(90, 566, 510, 600, 'ol thin'); ms.text(300, 585, 'вугілля', 'note', 'middle')
ms.dimH(0, 600, -40, ext_from=0); ms.dimH(0, 75, 900, '75', ext_from=850); ms.dimH(525, 600, 900, '75', ext_from=850)
ms.dimH(73, 527, 640, '454 робоча зона')
ms.dimV(501, 566, 650, '65', ext_from=592, side='right'); ms.dimV(569, 800, 650, '231', side='right')
ms.dimV(800, 850, 650, '50', ext_from=600, side='right')
ms.dimV(600, 844, -40, '≈ 260', side='left')
mangal_side_svg = ms.svg('Мангал розріз')

# ======================= 5. LID plan + layers =======================
L = View(gx(1430), gx(2800), 0, 1320, pad=(140, 160, 90, 110), flip=False, k=2.0)
L.poly(lid)
for z in range(50, 1320, 100):
    x0 = gx(1433) if z < 620 else gx(2083); x1 = gx(2797)
    if 660 < z < 1040: L.line(x0, z, gx(2160), z, 'hid'); L.line(gx(2540), z, x1, z, 'hid')
    else: L.line(x0, z, x1, z, 'hid')
for x in range(1480, 2800, 100):
    z1 = 617 if x < 2080 else 1317
    if 2160 < x < 2540: L.line(gx(x), 3, gx(x), 660, 'hid'); L.line(gx(x), 1040, gx(x), z1, 'hid')
    else: L.line(gx(x), 3, gx(x), z1, 'hid')
L.rect(gx(2160), 660, gx(2540), 1040)
for x, z in ((gx(1470), 40), (gx(2760), 40), (gx(2760), 1280), (gx(1470), 580)): L.circle(x, z, 10)
L.dimH(gx(1430), gx(2800), -30, '1370', ext_from=0)
L.dimH(gx(2080), gx(2800), 1360, '720', ext_from=1320)
L.dimV(0, 620, gx(1430) - 30, '620', ext_from=gx(1430))
L.dimV(0, 1320, gx(2800) + 40, '1320', ext_from=gx(2800), side='right')
L.dimH(gx(2540), gx(2800), 1010, '260'); L.dimV(0, 660, gx(2350), '660', side='right')
L.dimH(gx(1430), gx(1530), 50, '100')
L.text(gx(1700), 1000, 'решітка: квадрат 10×10, крок 100', 'note', 'middle')
L.text(gx(1700), 1030, '○ — вушка для підйому, 4 шт', 'note', 'middle')
lid_svg = L.svg('Кришка тумби')

ls = View(0, 220, 0, 100, pad=(80, 170, 40, 50))
ls.rect(0, 0, 3, 80, 'fill')
for z in (50, 150): ls.rect(z - 5, 0, z + 5, 10, 'fill')
ls.rect(3, 10, 220, 18, 'ol thin'); ls.rect(3, 18, 220, 68, 'brick'); ls.rect(3, 18, 220, 68, 'ol thin'); ls.rect(3, 70, 220, 80, 'fill')
ls.text(228, 8, 'квадрат 10×10', 'note'); ls.text(228, 20, 'ЦСП 8–10 (незнімна)', 'note')
ls.text(228, 46, 'бетон 50', 'note'); ls.text(228, 78, 'плитка на клею 10', 'note')
ls.dimV(0, 80, -30, '80', ext_from=0); ls.dimH(0, 3, 95, '3')
ls.text(-10, -20, 'борт 70 × 3', 'note')
lid_layers_svg = ls.svg('Шари кришки')

# ======================= 6. Gabion (typical) =======================
g = View(0, 1300, 0, 730, pad=(130, 60, 60, 110), k=2.0)
g.rect(0, 0, 1300, 730, 'stone')
for x in range(50, 1300, 50): g.line(x, 0, x, 730, 'hid')
for y in range(50, 730, 50): g.line(0, y, 1300, y, 'hid')
for x in (0, 1270): g.rect(x, 0, x + 30, 730, 'fill')
for y in (0, 700): g.rect(30, y, 1270, y + 30, 'fill')
g.dimH(0, 1300, -40, ext_from=0); g.dimV(0, 730, -40, ext_from=0)
g.dimH(600, 650, 760, '50', ext_from=730); g.dimH(0, 30, 760, '30', ext_from=730)
gab_svg = g.svg('Габіон')

# ======================= BILL OF MATERIALS =======================
TUBE = 2.31; A40 = 2.42; F40 = 1.26; A25 = 1.12; A75 = 5.69; A50 = 3.77; A30 = 1.36; SQ10 = 0.785
SH3 = 23.55; SH5 = 39.25; SH2 = 15.7; SH15 = 11.78

grating = 6 * 1364 + 7 * 714 - 4 * 380 + 6 * 614 + 8 * 1314 - 4 * 380  # sink still cuts 4 bars each way   # mm, from the model
lid_area = 1.370 * 0.620 + 0.720 * 0.700 - 0.38 * 0.38
gab = {'біля казана': (0.2, 0.6), 'на торці тумби': (0.5, 0.2), 'справа біля стовпа': (0.2, 1.3)}
H = 0.73
gab_angle = sum(4 * H + 4 * (a + b) for a, b in gab.values())
gab_mesh = sum(2 * (a * b + a * H + b * H) for a, b in gab.values())
gab_vol = sum(a * b * H for a, b in gab.values())

tube_m = {'Мангал': 4 * .498 + 4 * .72 + 4 * .52, 'Казан': 4 * .374 + 4 * .42 + 4 * .52, 'Тумба': 16.7}

parts = [
 ('Частина 1 · Мангал 800 × 600', [
   ('Труба 40×40×2', f"{tube_m['Мангал']:.1f} м", 'ніжки 4×498, обв\'язка 4×720 і 4×520'),
   ('Лист 3 мм', '1,8 м²', 'короб 800×600, борти висотою 302; полиця 800×600'),
   ('Кутник 75×50×6', '2 × 800', 'накриває торці рядів, пропили під шампури 12×10 крок 60'),
   ('Шамот ША-5 230×114×65', '≈ 45 шт', 'під плашмя, стінки на ребро 2 ряди; у моделі 38 нетто'),
   ('Розчин жаростійкий (шамотний)', '1 мішок 20–25 кг', 'шов 2–3 мм'),
   ('Болти M10 × 120 + гайки + втулки 30', '4 компл.', 'кріплення до печі через зазор 30'),
   ('Смуга 40×3', '600', 'знімна накладка над зазором мангал–казан'),
 ]),
 ('Частина 2 · Піч під казан 500 × 600', [
   ('Труба 40×40×2', f"{tube_m['Казан']:.1f} м", 'див. креслення печі, поз. 1–3'),
   ('Лист 3 мм', '0,9 м²', 'полиця, дно, задня стінка, полотно дверцят'),
   ('Лист 2 мм', '240×230', 'екран дверцят'),
   ('Лист 5 мм', '0,35 м²', 'плита 486×586, фланець Ø160, накладка 90×100'),
   ('Кутник 40×40×4', '4 × 419', 'кутові'),
   ('Смуга 40×4', '2,5 м', 'пояс 500 + 2×592, стійки 2×422'),
   ('Кутник 25×25×3', '2×290 + 2×280', 'рамка дверцят'),
   ('Кутник 50×50×5', '280', 'перемичка в кладці'),
   ('Шамот ША-5 230×114×65', '≈ 35 шт', 'на ребро 3 ряди + під; у моделі 31 нетто'),
   ('Облицювальна цегла 250×120×65', '7 шт', 'розрізати вздовж на смуги 250×57×65'),
   ('Базальтовий картон 5 мм', '0,2 м²', 'між шамотом і облицюванням'),
   ('Шнур жаростійкий Ø10–12', '2 м', 'під плиту'),
   ('Розчин жаростійкий', '1 мішок 20–25 кг', 'шамот і облицювання'),
   ('Петлі, засувка з ручкою', '2 + 1', 'дверцята'),
   ('Болти M8 × 25 + гайки', '8 компл.', 'фланець труби і накладка з тумбою'),
   ('Болти M6 + втулки Ø16×15', '4 компл.', 'екран дверцят'),
   ('Труба димохідна Ø110 нерж.', '≈ 1,6 м + коліно 90° + грибок', 'вивід угору до ≈ 2300'),
   ('Казан чавунний 8 л', '1', 'по вінцю ≈ Ø340'),
 ]),
 ('Частина 3 · Тумба, габіони, кришка', [
   ('Труба 40×40×2', f"{tube_m['Тумба']:.1f} м", 'каркас тумби, див. kreslennia-tumba.html'),
   ('Лист 1,5 мм', '3,4 м²', 'обшивка, дно, полиця, дверцята 440×650'),
   ('Лист 4 мм', '9 × 40×40', 'пластини під ніжки'),
   ('Ніжки регульовані M10', '9', 'під стійки тумби'),
   ('Петлі, ручка, магнітна защіпка', '2 + 1 + 1', 'дверцята під умивальником'),
   ('Кутник 30×30×3', f'{gab_angle:.1f} м', 'рамки трьох габіонів'),
   ('Сітка зварна 50×50, дріт 4–5 мм', f'{gab_mesh * 1.1:.1f} м²', 'габіони, з запасом 10%'),
   ('Камінь 80–120', f'{gab_vol:.2f} м³ (≈ {gab_vol * 1600:.0f} кг)', 'засипка габіонів'),
   ('Смуга 70×3', '5,4 м', 'борт кришки по периметру'),
   ('Квадрат 10×10', f'{grating / 1000:.1f} м', 'решітка дна кришки, крок 100'),
   ('ЦСП 8–10 мм', '1,4 м²', 'незнімна опалубка на решітку (або плівка + сітка)'),
   ('Бетон', f'{lid_area * 0.05:.2f} м³ (≈ {lid_area * 0.05 * 2400:.0f} кг)', 'шар 50 мм'),
   ('Плитка на стільницю', f'{lid_area * 1.1:.2f} м²', 'з запасом 10%'),
   ('Клей для плитки, затирка', '≈ 8 кг + 2 кг', 'вулична, морозостійка'),
   ('Вушка для підйому', '4', 'приварити до борту'),
   ('Болти M8 + гайки для кришки', '6 компл.', 'гайки приварити до решітки'),
   ('Болти M10 × 120 + гайки', '4 компл.', 'кріплення тумби до печі'),
   ('Умивальник 380×380, змішувач, сифон, крани', '1 компл.', ''),
   ('Холодильник Ardesto DFM-50X', '1', '492 × 472 × 450, 50 л'),
 ]),
 ('Загальне', [
   ('Фарба термостійка до 600 °C', '≈ 1 л', 'мангал і піч'),
   ('Фарба по металу (вулична) + ґрунт', '≈ 1 л + 1 л', 'тумба, габіони'),
   ('Електроди 3 мм / дріт для напівавтомата', '≈ 3 кг', ''),
   ('Диски відрізні 125 і зачисні', '10 + 3', ''),
   ('Розетка вулична IP44 з УЗО', '1', 'для холодильника — ще не вирішено'),
 ]),
]

steel = [
 ('Труба 40×40×2', sum(tube_m.values()), TUBE, 'м'),
 ('Кутник 75×50×6', 1.6, A75, 'м'),
 ('Кутник 50×50×5', 0.28, A50, 'м'),
 ('Кутник 40×40×4', 1.68, A40, 'м'),
 ('Кутник 30×30×3', gab_angle, A30, 'м'),
 ('Кутник 25×25×3', 1.14, A25, 'м'),
 ('Смуга 70×3', 5.4, 1.65, 'м'),
 ('Смуга 40×4', 2.53, F40, 'м'),
 ('Смуга 40×3', 0.6, 0.94, 'м'),
 ('Квадрат 10×10', grating / 1000, SQ10, 'м'),
 ('Лист 5 мм', 0.35, SH5, 'м²'),
 ('Лист 3 мм', 2.7, SH3, 'м²'),
 ('Лист 2 мм', 0.06, SH2, 'м²'),
 ('Лист 1,5 мм', 3.4, SH15, 'м²'),
]
steel_mass = sum(q * k for _, q, k, _ in steel)

def num(x, d=1):
    return f'{x:.{d}f}'.replace('.', ',')

# ---- materialy.md ----
md = ['# Зона мангала — перелік матеріалів', '',
      'Модель v14 від 19.11.2026. Кількості пораховано з моделі.',
      'Креслення: [kreslennia-kompleks.html](kreslennia-kompleks.html), для зварювальника — каркас печі [kreslennia-pich.html](kreslennia-pich.html) і каркас тумби [kreslennia-tumba.html](kreslennia-tumba.html), окремі види — у папці [kreslennia](kreslennia).', '']
md += ['## Прокат разом (з запасом під різ брати +10%)', '', '| Профіль | Кількість | Маса, кг |', '|---|---:|---:|']
for n, q, k, u in steel:
    md.append(f'| {n} | {num(q, 2)} {u} | {num(q * k)} |')
md += [f'| **Разом** | | **≈ {steel_mass:.0f}** |', '']
for title, rows in parts:
    md += [f'## {title}', '', '| Матеріал | Кількість | Примітка |', '|---|---|---|']
    md += [f'| {a} | {b} | {c} |' for a, b, c in rows]
    md.append('')
md += ['## Шамот і цегла разом', '',
       '- Шамот ША-5 230×114×65: ≈ 80 шт (69 нетто в моделі + підрізка).',
       '- Облицювальна цегла 250×120×65: 7 шт (на фасад печі, розрізати вздовж).', '']
open(os.path.join(ROOT, 'materialy.md'), 'w', encoding='utf-8').write('\n'.join(md))

# ---- HTML ----
steel_rows = ''.join(f'<tr><td>{n}</td><td class="m">{num(q, 2)} {u}</td><td class="m">{num(q * k)}</td></tr>' for n, q, k, u in steel)
part_rows = ''
for title, rows in parts:
    part_rows += f'<tr class="sub"><td colspan="3">{title}</td></tr>'
    part_rows += ''.join(f'<tr><td>{a}</td><td class="m">{b}</td><td class="c">{c}</td></tr>' for a, b, c in rows)

html = HEAD.format(title='Зона мангала: креслення', css=PAGE_CSS) + f'''
<div class="wrap">
  <header class="tb">
    <div>
      <h1>Зона мангала · креслення комплексу</h1>
      <p>Мангал, піч під казан і тумба з умивальником на майданчику 3000 × 1500. Три частини на болтах. Каркас печі окремо: <a href="https://claude.ai/artifact/H1J2R72iAaprnuJkxpDk69">креслення для зварювальника</a>.</p>
    </div>
    <dl class="meta">
      <dt>Модель</dt><dd>v14 · 19.11.2026</dd>
      <dt>Розміри</dt><dd>мм, висоти від плитки</dd>
      <dt>Сталь</dt><dd>≈ {steel_mass:.0f} кг</dd>
    </dl>
  </header>

  <h2 class="sheet-h">Аркуш 1 · Комплекс</h2>
  <div class="grid">
    <section class="v wide"><h2>План <span>зад угорі, кришка тумби суцільною лінією, габіони і холодильник під нею пунктиром</span></h2><div class="sc">{plan_svg}</div></section>
    <section class="v wide"><h2>Фасад <span>стовпи і труба обрізані</span></h2><div class="sc">{front_svg}</div></section>
    <section class="v"><h2>Розріз А–А <span>через умивальник</span></h2><div class="sc">{sect_svg}</div></section>
    <section class="notes">
      <h2>Збирання</h2>
      <ul>
        <li>Три частини ставляться окремо і стягуються болтами M10 через ніжки на висоті 120 і 300.</li>
        <li>Між мангалом і піччю зазор 30 на дистанційних втулках, зверху знімна накладка.</li>
        <li>Піч і тумба: 4 болти через ніжки + накладка 90×100 ззаду вгорі на 4 болти M8.</li>
        <li>Кришка тумби цільна, ≈ 210 кг: ставити вчотирьох або лебідкою за 4 вушка, кріпити болтами M8 знизу.</li>
        <li>Кришка звисає на 20 мм над габіонами.</li>
        <li>Майданчик і стовпи 100×100 вже є, у перелік не входять.</li>
        <li>Каркас тумби окремо: kreslennia-tumba.html.</li>
      </ul>
    </section>
  </div>

  <h2 class="sheet-h">Аркуш 2 · Частина 1, мангал 800 × 600</h2>
  <div class="grid">
    <section class="v"><h2>Вид спереду</h2><div class="sc">{mangal_front_svg}</div></section>
    <section class="v"><h2>Розріз поперек <span>зад ліворуч</span></h2><div class="sc">{mangal_side_svg}</div></section>
    <section class="notes">
      <h2>Мангал: позиції</h2>
      <ol>
        <li>Ніжки — труба 40×40×2, L 498, 4 шт; отвори Ø11 на 120 і 300 з боку печі.</li>
        <li>Обв'язка — труба 40×40×2: 4 × 720 і 4 × 520, рівні 100 і 458.</li>
        <li>Полиця під дрова — лист 3 мм 800×600, вирізи 40×40 по кутах.</li>
        <li>Короб — лист 3 мм: дно 800×600 на 498, борти висотою 302 до 800.</li>
        <li>Кутник 75×50×6, L 800, 2 шт: полиця 75 лягає на цеглу і край короба, полиця 50 вгору до 850, 13 пропилів 12×10 з кроком 60, перший на 140.</li>
      </ol>
    </section>
  </div>

  <h2 class="sheet-h">Аркуш 3 · Частина 2, піч під казан</h2>
  <div class="notes">
    <p style="margin:0">Окреме креслення з усіма розмірами: <a href="https://claude.ai/artifact/H1J2R72iAaprnuJkxpDk69">Каркас печі під казан</a> (у репозиторії — kreslennia-pich.html і kreslennia/pich-*.svg).</p>
  </div>

  <h2 class="sheet-h">Аркуш 4 · Частина 3, тумба і кришка</h2>
  <div class="grid">
    <section class="v wide"><h2>Кришка, вид згори <span>решітка дна пунктиром</span></h2><div class="sc">{lid_svg}</div></section>
    <section class="v"><h2>Шари кришки <span>переріз біля борту</span></h2><div class="sc">{lid_layers_svg}</div></section>
    <section class="v"><h2>Габіон <span>типово, на прикладі 1300 × 730</span></h2><div class="sc">{gab_svg}</div></section>
  </div>

  <section class="bom">
    <h2>Прокат разом</h2>
    <div class="tw"><table>
      <thead><tr><th>Профіль</th><th>Кількість</th><th>Маса, кг</th></tr></thead>
      <tbody>{steel_rows}<tr class="sub"><td>Разом</td><td></td><td class="m">≈ {steel_mass:.0f}</td></tr></tbody>
    </table></div>
    <p class="total">Під різ і брак брати +10%.</p>
  </section>

  <section class="bom">
    <h2>Перелік матеріалів по частинах</h2>
    <div class="tw"><table>
      <thead><tr><th>Матеріал</th><th>Кількість</th><th>Примітка</th></tr></thead>
      <tbody>{part_rows}</tbody>
    </table></div>
  </section>
</div>
'''
open(os.path.join(ROOT, 'kreslennia-kompleks.html'), 'w', encoding='utf-8').write(html)

p.save(os.path.join(K, 'kompleks-1-plan.svg'), 'Зона мангала · план')
f.save(os.path.join(K, 'kompleks-2-fasad.svg'), 'Зона мангала · фасад')
a.save(os.path.join(K, 'kompleks-3-rozriz-AA.svg'), 'Зона мангала · розріз А–А через умивальник')
m.save(os.path.join(K, 'mangal-1-vyd-speredu.svg'), 'Мангал · вид спереду')
ms.save(os.path.join(K, 'mangal-2-rozriz.svg'), 'Мангал · розріз поперек')
L.save(os.path.join(K, 'tumba-1-kryshka.svg'), 'Тумба · кришка, вид згори')
ls.save(os.path.join(K, 'tumba-2-shary-kryshky.svg'), 'Тумба · шари кришки')
g.save(os.path.join(K, 'tumba-3-gabion.svg'), 'Габіон · типово')
print('ok, steel', round(steel_mass), 'kg; grating', grating, 'mm')
