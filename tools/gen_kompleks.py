# Usage: python tools/gen_kompleks.py  ->  kreslennia-kompleks.html, materialy.md, kreslennia/kompleks-*.svg
# Drawings of the whole grill zone (model v33) and the bill of materials.
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

# ======================= 1. PLAN (v33) =======================
# world x from the left edge of the paving (rig-local + 100), z from the rear edge
MX0, MX1 = 480, 1130; MW = MX1 - MX0; MXC = (MX0 + MX1) // 2
NOTCH = list(range(MX0 + 55, MX1 - 54, 60))
KX = 1380                                   # kazan centre, rig-local
p = View(-1100, 4100, -560, 1850, pad=(150, 90, 90, 220), flip=False, k=3.4)
p.rect(-1000, -450, 4000, 1750, 'hid'); p.text(-980, -470, 'дах 5000 × 2200 (пунктир)', 'note')
p.rect(0, 0, 3000, 1500, 'ol thin')
for x, z in ((0, 0), (2900, 0), (0, 1400), (2900, 1400)): p.rect(x, z, x + 100, z + 100, 'fill')
for x0 in (-400, 3000):                      # firewood walls with trusses at the posts
    p.rect(x0, 70, x0 + 400, 1430, 'brick'); p.rect(x0, 70, x0 + 400, 1430, 'ol thin')
    for zc in (50, 1450): p.rect(x0, zc - 20, x0 + 400, zc + 20, 'fill')
    p.text(x0 + 200, 760, 'дрова', 'note', 'middle')
p.rect(gx(50), 0, gx(480), 610); p.text(gx(265), 300, 'тумба', 'note', 'middle')      # left cabinet worktop
p.rect(gx(MX0), 0, gx(MX1), 600)
p.rect(gx(MX0 + 73), 73, gx(MX1 - 73), 527, 'brick'); p.rect(gx(MX0 + 73), 73, gx(MX1 - 73), 527, 'ol thin')
for z0, z1 in ((0, 75), (525, 600)): p.rect(gx(MX0), z0, gx(MX1), z1, 'fill')
p.text(gx(MXC), 310, 'мангал', 'note', 'middle')
p.rect(gx(1130), 0, gx(1630), 600); p.circle(gx(KX), 270, 170); p.circle(gx(KX), 270, 150, 'hid')
p.circle(gx(KX), -92, 55); p.text(gx(KX) + 70, -110, 'труба Ø110', 'note')
p.text(gx(KX), 520, 'піч під казан', 'note', 'middle')
p.rect(gx(1630), 0, gx(2780), 610); p.rect(gx(1733), 110, gx(2113), 490)              # right cabinet, sink cut-out
p.text(gx(1923), 560, 'умивальник', 'note', 'middle')
p.rect(gx(2231), 110, gx(2703), 556, 'hid'); p.text(gx(2467), 340, 'холодильник', 'note', 'middle')
p.rect(gx(380), -320, gx(1230), 650, 'hid'); p.circle(gx(805), 260, 125, 'hid'); p.text(gx(805), -340, 'витяжка 850 × 970', 'note', 'middle')
p.rect(gx(1670), 40, gx(2800), 160, 'hid'); p.text(gx(2300), 190, 'полиця на 1500', 'note', 'middle')
p.line(gx(1923), 640, gx(1923), 1500, 'cl'); p.text(gx(1923) + 10, 1530, 'А', 'ttl'); p.text(gx(1923) + 10, -10, 'А', 'ttl')
p.dimH(-1000, 4000, -520, '5000', ext_from=-450)
p.dimH(-400, 0, 1800, '400', ext_from=1500); p.dimH(0, gx(50), 1800, '150'); p.dimH(gx(50), gx(480), 1800, '430')
p.dimH(gx(480), gx(1130), 1800, '650'); p.dimH(gx(1130), gx(1630), 1800, '500'); p.dimH(gx(1630), gx(2780), 1800, '1150')
p.dimH(gx(2780), 3000, 1800, '120'); p.dimH(3000, 3400, 1800, '400')
p.dimV(0, 1500, -1060, '1500', ext_from=-1000, side='left'); p.dimV(0, 610, gx(2780) + 160, '610', ext_from=gx(2780), side='right')
plan_svg = p.svg('План')

# ======================= 2. FRONT ELEVATION (v33) =======================
f = View(-1100, 4100, -60, 4200, pad=(160, 160, 60, 240), k=3.4)
f.line(-1100, 0, 4100, 0, 'ol')
f.rect(-1020, 2925 + 80, 4020, 2925 + 115, 'fill')                                  # front edge of the roof (sheet on the rafters)
f.rect(-1020, 2925, 4020, 2925 + 80, 'ol thin')                                      # rafter ends + purlin
f.rect(-1000, 2750, 4000, 2850, 'fill')                                               # front beam
for x0 in (0, 2900): f.rect(x0, 0, x0 + 100, 2750, 'fill')
for xa, xb in ((0, -600), (100, 700), (2900, 2300), (3000, 3600)): f.line(xa, 2150, xb, 2750, 'ol thin')
for x0, d in ((-400, 1), (3000, 1)):                 # firewood walls: log ends between the truss
    for yy in range(190, 1960, 75):                                                  # log ends
        for xx in range(x0 + 40, x0 + 400, 75): f.circle(xx + (yy // 75 % 2) * 30 - 15, yy, 34, 'ol thin')
    xo = x0 if x0 < 0 else x0 + 360
    f.rect(xo, -41, xo + 40, 2000, 'fill'); f.rect(x0, 110, x0 + 400, 150, 'fill'); f.rect(x0, 1960, x0 + 400, 2000, 'fill')
    xp, xq = (0, -380) if x0 < 0 else (3000, 3380)
    ys = [150, 600, 1050, 1500, 1960]
    for i in range(4): f.line(xp if i % 2 == 0 else xq, ys[i], xq if i % 2 == 0 else xp, ys[i + 1], 'ol')
# left cabinet: stone-panel door
f.rect(gx(50), 0, gx(480), 788, 'ol thin'); f.rect(gx(50), 788, gx(480), 800, 'fill')
f.rect(gx(52), 40, gx(455), 780, 'stone'); f.rect(gx(52), 40, gx(455), 780, 'ol')
# mangal: frame, box, angle, drawer, closed lid dashed
for x in (gx(MX0), gx(MX1) - 40): f.rect(x, 0, x + 40, 498)
f.rect(gx(MX0), 498, gx(MX1), 800, 'fill'); f.rect(gx(MX0), 800, gx(MX1), 850, 'fill')
f.rect(gx(MX0 + 45), 148, gx(MX1 - 45), 452); f.rect(gx(MXC - 160), 389, gx(MXC + 160), 401, 'ol thin')
f.rect(gx(MX0 - 3), 830, gx(MX1 + 3), 1000, 'hid')
# oven: frame, facing brick, door, kazan, flue
for x in (gx(1130), gx(1590)): f.rect(x, 0, x + 40, 796)
f.rect(gx(1134), 377, gx(1626), 756, 'brick'); f.rect(gx(1130), 756, gx(1630), 796)
f.rect(gx(1240), 425, gx(1520), 695, 'fill')
pts = []
for i in range(21):
    y = 800 + 80 * i / 20; hw = math.sqrt(max(0, 170 ** 2 - (880 - y) ** 2)); pts.append((gx(KX) - hw, y))
for i in range(20, -1, -1):
    y = 800 + 80 * i / 20; hw = math.sqrt(max(0, 170 ** 2 - (880 - y) ** 2)); pts.append((gx(KX) + hw, y))
f.poly(pts, 'fill'); f.rect(gx(KX) - 55, 884, gx(KX) + 55, 3100, 'hid')
# right cabinet: sink cabinet door, fridge stone-panel door, worktop, side panel
f.rect(gx(1630), 0, gx(2780), 788, 'ol thin'); f.rect(gx(1630), 788, gx(2780), 800, 'fill')
f.rect(gx(1672), 60, gx(2172), 760); f.rect(gx(2140), 360, gx(2150), 480, 'fill')
f.rect(gx(2180), 50, gx(2756), 750, 'stone'); f.rect(gx(2180), 50, gx(2756), 750, 'ol')
f.rect(gx(1911), 800, gx(1935), 1060, 'ol thin')                                         # mixer
# rail wall above the right cabinet
for x in (1630, 2176): f.rect(gx(x), 800, gx(x + 40), 1650, 'fill')
f.rect(gx(1670), 1610, gx(2800), 1650, 'fill'); f.rect(gx(1670), 1500, gx(2800), 1522, 'ol')
f.rect(gx(1670), 1142, gx(2176), 1158, 'ol'); f.rect(gx(2300), 1325, gx(2750), 1355, 'fill')
f.text(gx(2235), 1540, 'полиця', 'note', 'middle'); f.text(gx(1923), 1175, 'рейлінг Ø16', 'note', 'middle')
f.rect(0, 1142, gx(460), 1158, 'ol'); f.rect(gx(440), 800, gx(460), 1160, 'fill')    # left rail
# hood and chimney
f.rect(gx(380), 1950, gx(1230), 1975, 'fill')
f.poly([(gx(380), 1975), (gx(1230), 1975), (gx(930), 2300), (gx(680), 2300)], 'ol')
f.rect(gx(680), 2300, gx(930), 3900, 'ol'); f.poly([(gx(630), 3920), (gx(980), 3920), (gx(805), 4120)], 'fill')
f.rect(gx(380), 1450, gx(390), 1950, 'hid'); f.rect(gx(1220), 1450, gx(1230), 1950, 'hid')
# dims
f.dimH(-1000, 4000, -170, '5000', ext_from=0)
for x0, x1, t in ((-400, 0, '400'), (gx(50), gx(480), '430'), (gx(480), gx(1130), '650'), (gx(1130), gx(1630), '500'),
                  (gx(1630), gx(2780), '1150'), (3000, 3400, '400')):
    f.dimH(x0, x1, -60, t, ext_from=0)
f.dimV(0, 800, -1060, '800', ext_from=-1000, side='left'); f.dimV(0, 2000, -540, '2000', ext_from=-400, side='left')
f.dimV(0, 2750, 4060, '2750', ext_from=3000, side='right'); f.dimV(0, 1950, gx(1230) + 60, '1950', ext_from=gx(1230), side='right')
f.dimV(0, 3900, gx(930) + 80, '3900', ext_from=gx(930), side='right'); f.dimV(800, 1650, gx(1630) - 60, '850', side='left')
front_svg = f.svg('Фасад')

# ======================= 3. SECTION A-A through the sink (v33) =======================
a = View(-560, 1850, -60, 3100, pad=(120, 200, 60, 120), k=2.4)
a.line(-560, 0, 1850, 0, 'ol')
a.rect(0, -40, 1500, 0, 'fill')                                                      # paving
for z0, top in ((0, 2400), (1400, 2750)): a.rect(z0, 0, z0 + 100, top, 'hid')       # posts beyond the cut
a.rect(-2, 20, 0, 788, 'fill')                                                         # back sheet
for z0 in (0, 560):
    for y0 in (20, 748): a.rect(z0, y0, z0 + 40, y0 + 40, 'fill')
a.rect(0, 788, 610, 790, 'fill'); a.rect(0, 790, 610, 800, 'brick'); a.rect(0, 790, 610, 800, 'ol thin')   # sheet + tile
a.rect(110, 600, 490, 800, 'ol'); a.rect(290, 520, 310, 600, 'ol thin'); a.text(320, 540, 'сифон', 'note')
a.rect(42, 800, 78, 1060, 'ol thin'); a.rect(60, 1040, 245, 1060, 'ol thin')          # mixer
a.rect(600, 60, 622, 760, 'ol'); a.text(640, 400, 'дверцята', 'note')
a.rect(0, 800, 40, 1650, 'fill'); a.rect(0, 1610, 20, 1650, 'fill')                    # rail-wall upright, top bar
a.rect(40, 1500, 160, 1502, 'fill'); a.rect(157, 1502, 160, 1522, 'fill'); a.text(60, 1530, 'полиця', 'note')
a.circle(60, 1150, 8, 'fill'); a.text(80, 1160, 'рейлінг', 'note')
ry_ = lambda z: 2500 + 0.25 * (z - 50)
a.poly([(-450, ry_(-450)), (1750, ry_(1750)), (1750, ry_(1750) + 60), (-450, ry_(-450) + 60)], 'ol')
a.poly([(-480, ry_(-480) + 80), (1780, ry_(1780) + 80), (1780, ry_(1780) + 115), (-480, ry_(-480) + 115)], 'fill')
a.rect(0, 2400, 100, 2500, 'fill'); a.rect(1400, 2750, 1500, 2850, 'fill')
a.dimH(0, 610, -40 - 0, '610', ext_from=0); a.dimH(110, 490, 900, '380', ext_from=800)
a.dimV(0, 800, 1620, '800', ext_from=1500, side='right'); a.dimV(800, 1650, 1620, '850', side='right')
a.dimV(1650, ry_(0), 1620, '≈ 840', side='right')
a.text(700, 2950, 'дах · нахил 1 : 4', 'note', 'middle'); a.text(700, -110, 'зад ліворуч, перед праворуч', 'note', 'middle')
sect_svg = a.svg('Розріз А–А')

# ======================= 4. MANGAL front + section =======================
W = MW  # 650
NR = [x - MX0 for x in NOTCH]  # notches relative to the mangal edge: 55 ... 595
m = View(-3, W + 3, 0, 1000, pad=(130, 120, 60, 110), k=1.3)
for x in (0, W - 40): m.rect(x, 0, x + 40, 498)
for y in (100, 458): m.rect(40, y, W - 40, y + 40)
m.rect(0, 140, W, 143, 'ol thin')
m.rect(0, 498, W, 800)
m.rect(8, 501, W - 8, 800, 'hid')
m.rect(0, 800, W, 806); m.rect(0, 806, W, 840)
prev = 0
for x in NR:
    m.rect(prev, 840, x - 6, 850); prev = x + 6
m.rect(prev, 840, W, 850)
m.dimH(0, W, -40, ext_from=0)
m.dimH(0, NR[0], 900, str(NR[0]), ext_from=850); m.dimH(NR[0], NR[1], 900, '60'); m.dimH(NR[-1], W, 900, str(W - NR[-1]), ext_from=850)
m.dimH(NR[0] - 6, NR[0] + 6, 870, '12')
m.text(200, 905, f'{len(NR)} пропилів 12 × 10, крок 60', 'note', 'middle')
m.dimV(0, 498, -40, ext_from=0); m.dimV(498, 800, -40, '302'); m.dimV(800, 850, -40, '50')
m.dimV(0, 100, W + 40, '100', ext_from=W, side='right'); m.dimV(100, 140, W + 40, '40', side='right')
m.dimV(458, 498, W + 40, '40', side='right')
m.pos(1, 20, 250, -60, 300); m.pos(2, W / 2, 120, W / 2, 300); m.pos(3, W - 150, 141, W - 100, 300)
m.pos(4, W / 2, 650, W / 2 + 80, 720); m.pos(5, 250, 830, 210, 760)
# v15 lid, dashed: hood 656 wide, front wall down to 830, top on 1000; wooden handle on two brackets
m.rect(-3, 830, W + 3, 1000, 'hid'); m.rect(-3, 998, W + 3, 1000, 'hid')
for x in (W / 2 - 80, W / 2 + 80): m.rect(x - 3, 915, x + 3, 945, 'ol thin')
m.rect(W / 2 - 110, 916, W / 2 + 110, 944, 'ol')
m.dimV(850, 1000, W + 40, '150', ext_from=W + 3, side='right'); m.dimH(-3, W + 3, 1040, str(W + 6), ext_from=1000)
m.pos(6, 150, 970, 70, 1030)
# v17 drawer front between the front rings
m.rect(45, 148, W - 45, 452); m.rect(W / 2 - 160, 389, W / 2 + 160, 401, 'ol thin')
m.dimV(148, 452, W + 40, '304', side='right'); m.pos(7, W - 150, 300, W - 70, 220)
mangal_front_svg = m.svg('Мангал спереду')

ms = View(-330, 600, 0, 1450, pad=(130, 130, 60, 110), k=1.3)
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
# v15 lid in section: rear wall, top and front wall of 2 mm sheet; hinge pin Ø20 at z -16, y 840; lower leaf on the rear angle
for r in ((-3, 830, -1, 1000), (-3, 998, 603, 1000), (601, 830, 603, 1000), (-1, 973, 2, 998), (598, 973, 601, 998)): ms.rect(*r, 'fill')
ms.rect(-8, 806, 0, 829, 'fill'); ms.circle(-16, 840, 10, 'fill'); ms.rect(-7, 846, -3, 900, 'fill')
ms.rect(603, 915, 643, 945, 'ol thin'); ms.circle(640, 930, 14, 'ol')
# open position, 100°, dashed
_a = math.radians(-100); _c, _s = math.cos(_a), math.sin(_a)
def _rot(z, y):
    dz, dy = z + 16, y - 840
    return (-16 + dy * _s + dz * _c, 840 + dy * _c - dz * _s)
ms.poly([_rot(z, y) for z, y in ((-3, 830), (-3, 1000), (603, 1000), (603, 830), (601, 830), (601, 998), (-1, 998), (-1, 830))], 'hid')
ms.text(-300, 1420, 'відкрита на 100°', 'note')
ms.text(-310, 800, 'петля Ø20 × 80, 2 шт', 'note')
ms.dimV(850, 1000, 690, '150', ext_from=603, side='right'); ms.dimV(0, 1000, -60, '1000', side='left')
ms.dimH(-16, 0, 780, '16')
# v17 drawer in section: body 545 deep on bottom-mount runners on the shelf, front
ms.rect(50, 166, 595, 441, 'ol thin'); ms.rect(597, 148, 600, 452, 'fill'); ms.rect(45, 143, 560, 158, 'ol thin')
ms.text(320, 300, 'ящик, висув 450', 'note', 'middle')
mangal_side_svg = ms.svg('Мангал розріз')

# v29 natural-draft hood over the mangal, section from the side (rear on the left)
hd = View(-450, 760, 0, 4200, pad=(130, 170, 60, 110), k=2.2)
hd.line(-450, 0, 760, 0, 'ol')
hd.rect(0, 0, 600, 800, 'ol thin'); hd.text(300, 650, 'мангал', 'note', 'middle')
hd.poly([(0, 800), (600, 800), (600, 850), (0, 850)], 'fill')
_a = math.radians(-100); _c, _s = math.cos(_a), math.sin(_a)
def _r(z, y):
    dz, dy = z + 16, y - 840
    return (-16 + dy * _s + dz * _c, 840 + dy * _c - dz * _s)
hd.poly([_r(z, y) for z, y in ((-3, 830), (-3, 1000), (603, 1000), (603, 830))], 'hid')
hd.text(-430, 1250, 'кришка відкрита', 'note')
hd.rect(-380, -41, -320, 1975, 'fill')                              # upright 60x40
hd.rect(-322, 1450, -320, 1950, 'fill')                             # back screen
hd.poly([(-320, 1450), (100, 1450), (300, 1950), (-320, 1950)], 'hid')  # side cheek beyond
hd.rect(-320, 1950, 650, 1975, 'fill')                              # rim
hd.poly([(-320, 1975), (650, 1975), (385, 2300), (135, 2300)], 'ol')  # pyramid
hd.rect(135, 2300, 385, 3900, 'ol')                                 # chimney Ø250
hd.poly([(85, 3920), (435, 3920), (420, 4040), (260, 4120), (100, 4040)], 'fill')  # turbo-deflector
hd.poly([(-500, 2447), (760, 2763)], 'ol')  # roof sheet line (v30)
hd.circle(900, 1700, 0.1, 'ol thin')
hd.dimV(0, 1950, 720, '1950', ext_from=650, side='right'); hd.dimV(1450, 1950, -430, '500', side='left')
hd.dimV(1975, 2300, 720, '325', side='right'); hd.dimV(2300, 3900, 720, '1600', side='right')
hd.dimH(-320, 650, 1880, '970', ext_from=1950); hd.dimH(135, 385, 3960, 'Ø250')
hd.text(200, 3000, 'труба Ø250, чорна сталь 2 мм', 'note', 'middle')
hd.text(200, 4170, 'турбодефлектор', 'note', 'middle')
hd.text(-120, 1700, 'екран і щоки до 1450', 'note', 'middle')
hd.text(500, 1800, 'зона кухаря відкрита', 'note', 'middle')
hood_svg = hd.svg('Витяжка')

# v30 shed roof: side section (rear on the left) and front view
RKs, ry_ = 0.25, (lambda z: 2500 + 0.25 * (z - 50))
rs = View(-700, 2000, -100, 3300, pad=(130, 170, 60, 110), k=2.4)
rs.line(-700, 0, 2000, 0, 'ol')
rs.rect(0, 0, 1500, -40, 'fill'); rs.text(750, -80, 'майданчик 1500', 'note', 'middle')
for z0, top in ((0, 2400), (1400, 2750)): rs.rect(z0, 0, z0 + 100, top, 'fill')
rs.rect(1400, 2400, 1500, 2750, 'ol')                                  # front post extension
rs.rect(0, 2400, 100, 2500, 'fill'); rs.rect(1400, 2750, 1500, 2850, 'fill')   # beams
rs.poly([(-450, ry_(-450)), (1750, ry_(1750)), (1750, ry_(1750) + 60), (-450, ry_(-450) + 60)], 'ol')   # rafter
rs.poly([(-480, ry_(-480) + 80), (1780, ry_(1780) + 80), (1780, ry_(1780) + 115), (-480, ry_(-480) + 115)], 'fill')  # sheet
rs.circle(-530, ry_(-480) + 10, 62, 'ol')                                # gutter
rs.rect(0, 0, 600, 800, 'ol thin'); rs.text(300, 400, 'мангал', 'note', 'middle')
rs.rect(-320, 1950, 650, 1975, 'ol thin'); rs.rect(135, 1975, 385, 3200, 'hid')
rs.dimV(0, 2400, -650, '2400', ext_from=0, side='left'); rs.dimV(0, 2750, 1950, '2750', ext_from=1500, side='right')
rs.dimH(-450, 0, 3150, '450', ext_from=2600); rs.dimH(0, 1500, 3150, '1500'); rs.dimH(1500, 1750, 3150, '250')
rs.text(650, 3000, 'нахил 1 : 4 ≈ 14°', 'note', 'middle')
rs.text(650, 2250, 'профнастил НС35 · обрешітка 40×20 · крокви 60×40', 'note', 'middle')
roof_side_svg = rs.svg('Дах збоку')
rf = View(-1100, 4100, 0, 3100, pad=(110, 110, 60, 110), k=3.4)
rf.line(-1100, 0, 4100, 0, 'ol')
for x0 in (0, 2900): rf.rect(x0, 0, x0 + 100, 2750, 'ol')
rf.rect(-1000, 2750, 4000, 2850, 'fill')                                # front beam
rf.rect(-1020, 2850, 4020, 2960, 'fill')                                # roof edge
for xa, xb in ((0, -600), (100, 700), (2900, 2300), (3000, 3600)): rf.line(xa, 2150, xb, 2750, 'ol')
rf.rect(150, 0, 2880, 800, 'ol thin'); rf.text(1500, 400, 'кухня', 'note', 'middle')
rf.dimH(-1000, 0, 3020, '1000', ext_from=2960); rf.dimH(0, 3000, 3020, '3000'); rf.dimH(3000, 4000, 3020, '1000')
rf.dimH(-1000, 4000, -60, '5000', ext_from=0)
roof_front_svg = rf.svg('Дах спереду')

# v32 firewood wall: side elevation (rear on the left) and the truss welded to the post (end view)
fw = View(-150, 2300, -60, 2150, pad=(130, 120, 60, 110), k=2.0)
fw.line(-150, -41, 2300, -41, 'ol')
fw.rect(0, 0, 100, 2100, 'ol'); fw.rect(1400, 0, 1500, 2100, 'ol')     # main posts (cut)
fw.rect(70, 110, 1430, 150, 'fill')                                   # base rail
fw.rect(70, 1960, 1430, 2000, 'fill')                                 # top tie
for z in (35, 1435, 735): fw.rect(z, -41, z + 30, 110 if z == 735 else -21, 'ol thin')   # feet
import random as _rnd
_g = _rnd.Random(7); _P = []
for _ in range(6000):
    r = _g.uniform(40, 78); z = _g.uniform(72 + r, 1428 - r); y = _g.uniform(152 + r, 1955 - r)
    if all((q[0] - z) ** 2 + (q[1] - y) ** 2 >= (q[2] + r + 1) ** 2 for q in _P): _P.append((z, y, r))
for z, y, r in _P: fw.circle(z, y, r, 'ol thin')
fw.dimH(100, 1400, 2080, '1300 між стовпами', ext_from=2000); fw.dimV(0, 2000, -110, '2000', ext_from=0, side='left')
fw.dimV(-41, 150, 1560, '150', side='right')
# end view: the truss in the plane of the post, the post is the inner chord
X0 = 1800
fw.rect(X0, 0, X0 + 100, 2100, 'fill')                                # post
fw.rect(X0 + 100 + 360, -41, X0 + 100 + 400, 2000, 'fill')            # outer chord 40x40, 400 from the post face
for y0 in (110, 1960): fw.rect(X0 + 100, y0, X0 + 500, y0 + 40, 'fill')
ys = [150, 600, 1050, 1500, 1960]
for i in range(4):
    a_ = (X0 + 100, ys[i]) if i % 2 == 0 else (X0 + 480, ys[i]); b_ = (X0 + 480, ys[i + 1]) if i % 2 == 0 else (X0 + 100, ys[i + 1])
    fw.line(a_[0], a_[1], b_[0], b_[1], 'ol')
fw.dimH(X0 + 100, X0 + 500, -20, '400', ext_from=150)
fw.text(X0 + 300, 2080, 'ферма: стовп + пояс + розкоси 40×40', 'note', 'middle')
fw.text(750, -110, 'поліна ≈ 400 поперек, торцями назовні', 'note', 'middle')
firewood_svg = fw.svg('Дровник')

# v34 left inventory cabinet 430 x 600, top 800: front view (left) and section along the depth (right, rear on the left)
hs = View(-40, 1260, -41, 900, pad=(130, 150, 60, 110), k=1.6)
LC0, LC1 = 50, 480
hs.line(-40, -41, 1260, -41, 'ol')
for x in (LC0, LC1 - 40): hs.rect(x, 20, x + 40, 788, 'hid')               # posts behind the door
for x in (LC0 + 8, LC1 - 32): hs.rect(x, -41, x + 24, 20, 'ol thin')        # feet
hs.rect(LC0, 788, LC1, 800, 'fill')                                          # sheet + tile
hs.rect(LC0 + 2, 40, LC1 - 25, 780, 'stone'); hs.rect(LC0 + 2, 40, LC1 - 25, 780, 'ol')   # door: stone panel
hs.rect(LC1 - 25, 40, LC1 - 2, 780, 'fill')                                  # fixed strip next to the mangal
for y in (150, 650): hs.rect(LC0 - 2, y - 25, LC0 + 4, y + 25, 'fill')      # hinges, outer side
hs.rect(LC1 - 60, 360, LC1 - 48, 480, 'fill')                                # grip
hs.dimH(LC0, LC1, 860, '430', ext_from=800); hs.dimH(LC0 + 2, LC1 - 25, 40 - 80, '403', ext_from=40)
hs.dimV(0, 800, LC0 - 70, '800', ext_from=LC0, side='left'); hs.dimV(40, 780, LC1 + 30, '740', side='right')
hs.text((LC0 + LC1) / 2, 420, 'дверцята — кам\'яна панель 22', 'note', 'middle')
Z = 620                                                                        # section origin
hs.rect(Z, 20, Z + 600, 788, 'ol thin'); hs.rect(Z, 788, Z + 610, 800, 'fill'); hs.rect(Z - 2, 20, Z, 788, 'fill')
for z in (0, 560): hs.rect(Z + z, 20, Z + z + 40, 788, 'hid')
for y in (20, 748): hs.rect(Z + 40, y, Z + 560, y + 40, 'fill')
hs.rect(Z + 40, 60, Z + 560, 62, 'fill')                                      # bottom
hs.rect(Z + 40, 420, Z + 560, 422, 'fill'); hs.text(Z + 300, 440, 'полиця на 420 (зліва)', 'note', 'middle')
hs.rect(Z + 50, 728, Z + 550, 732, 'fill'); hs.text(Z + 300, 705, 'рейка для шампурів на 740, 10 прорізів', 'note', 'middle')
for i, z in enumerate(range(80, 530, 45)):
    if i % 2 == 0: hs.line(Z + z, 120, Z + z, 732, 'ol thin'); hs.rect(Z + z - 6, 732, Z + z + 6, 790, 'ol thin')
hs.rect(Z + 600, 40, Z + 622, 780, 'stone')                                   # door in section
hs.dimH(Z, Z + 600, 860, '600', ext_from=800)
hs.text(Z + 300, 250, 'мішок вугілля на дні', 'note', 'middle')
holder_svg = hs.svg('Тумба зліва')

# ======================= 5. WORKTOPS plan + layers (v34) =======================
L = View(gx(0), gx(2840), -40, 700, pad=(140, 160, 90, 110), flip=False, k=2.6)
for x0, x1 in ((50, 480), (1630, 2780)):
    L.rect(gx(x0), 0, gx(x1), 610)                                            # tile top, 10 over the front
for x0, x1 in ((50, 480), (1630, 2758)):                                      # frame rings
    L.rect(gx(x0), 0, gx(x1), 600, 'hid')
L.rect(gx(255), 40, gx(275), 560, 'hid')                                      # cross bar, left
for x in (1700, 2146, 2457): L.rect(gx(x), 40, gx(x + 20), 560, 'hid')        # cross bars, right
for z in (110, 470): L.rect(gx(1720), z, gx(2146), z + 20, 'hid')
L.rect(gx(1733), 110, gx(2113), 490); L.text(gx(1923), 300, 'виріз 380 × 380', 'note', 'middle')
L.text(gx(265), 650, 'ліва 430 × 610', 'note', 'middle'); L.text(gx(2205), 650, 'права 1150 × 610', 'note', 'middle')
L.text(gx(800), 300, 'мангал', 'note', 'middle'); L.text(gx(1380), 300, 'піч', 'note', 'middle')
L.dimH(gx(50), gx(480), -20, '430', ext_from=0); L.dimH(gx(1630), gx(2780), -20, '1150', ext_from=0)
L.dimV(0, 610, gx(2780) + 40, '610', ext_from=gx(2780), side='right')
L.dimH(gx(1630), gx(1733), 540, '103'); L.dimH(gx(1733), gx(2113), 540, '380')
L.text(gx(2205), 690, 'пунктир — обв\'язка 40×40 і поперечки 20×20 під листом', 'note', 'middle')
lid_svg = L.svg('Стільниці')

ls = View(-30, 260, -60, 60, pad=(80, 190, 40, 50), k=0.9)
ls.rect(0, -40, 40, 0, 'fill'); ls.text(48, -24, 'обв\'язка 40×40', 'note')
ls.rect(120, -20, 140, 0, 'fill'); ls.text(148, -14, 'поперечка 20×20', 'note')
ls.rect(-10, 0, 240, 0.5 * 4, 'fill'); ls.rect(-10, -20, -8, 0, 'fill')       # sheet 0.5 (drawn x4), front edge bent down 20
ls.rect(-10, 2, 240, 8, 'ol thin'); ls.rect(-10, 8, 240, 48, 'brick'); ls.rect(-10, 8, 240, 48, 'ol thin')
ls.text(248, 1, 'лист 0,5, край загнутий на 20', 'note'); ls.text(248, 6, 'герметик ПУ / MS ≈ 1,5', 'note'); ls.text(248, 30, 'плитка керамограніт 10', 'note')
ls.dimV(-40, 0, -24, '40', side='left')
lid_layers_svg = ls.svg('Шари стільниці')

# ======================= 6. Stone panel (typical, v34) =======================
g = View(-40, 1000, -60, 760, pad=(130, 80, 60, 110), k=1.6)
g.rect(0, 0, 576, 700, 'stone')
for x0 in (0, 556): g.rect(x0, 0, x0 + 20, 700, 'fill')
for y0 in (0, 680): g.rect(20, y0, 556, y0 + 20, 'fill')
g.dimH(0, 576, 740, '576', ext_from=700); g.dimV(0, 700, -30, '700', ext_from=0, side='left'); g.dimH(0, 20, -40, '20', ext_from=0)
g.text(288, 350, 'камінець 10–20 у поліефірній смолі', 'note', 'middle')
# section: sheet 0.5 + frame 20 + resin with stones, ~22
g.rect(760, 0, 761, 700, 'fill'); g.rect(761, 0, 781, 20, 'fill'); g.rect(761, 680, 781, 700, 'fill'); g.rect(761, 20, 783, 680, 'stone'); g.rect(761, 0, 783, 700, 'ol')
g.dimH(760, 783, 740, '22', ext_from=700); g.text(800, 360, 'лист 0,5 + рамка 20×20 + смола з камінцем', 'note')
g.text(800, 300, 'панелі: дверцята холодильника 576 × 700,', 'note'); g.text(800, 270, 'бік біля стовпа 600 × 788,', 'note'); g.text(800, 240, 'дверцята лівої тумби 403 × 740', 'note')
gab_svg = g.svg('Кам\'яна панель')

# ======================= 7. COMMON FRAME of the mangal and the kazan oven (v33) =======================
# x as in the model (rig-local): mangal 480..1130, oven 1130..1630; heights from the paving
cf = View(420, 1690, -60, 860, pad=(130, 120, 60, 120), k=1.9)
cf.line(420, 0, 1690, 0, 'ol')
for x, top in ((480, 498), (1590, 374)): cf.rect(x, 0, x + 40, top, 'fill')              # legs 40x40x3
cf.rect(1090, 160, 1130, 498, 'fill'); cf.rect(1130, 160, 1170, 374, 'fill')             # joint stubs
cf.rect(520, 458, 1090, 498, 'fill'); cf.rect(1170, 334, 1590, 374, 'fill')              # upper rings, front
cf.rect(520, 100, 1590, 160, 'fill')                                                     # bottom rail 60x40x3
cf.rect(1110, 100, 1150, 160, 'ol')                                                      # cross rail end
cf.rect(480, 498, 1130, 800, 'hid'); cf.text(805, 650, 'короб мангала', 'note', 'middle')
cf.rect(1130, 374, 1630, 796, 'hid'); cf.text(1380, 600, 'піч: кутники, пояс, кладка', 'note', 'middle')
cf.dimH(480, 1130, 840, '650', ext_from=800); cf.dimH(1130, 1630, 840, '500', ext_from=796)
cf.dimH(520, 1590, -40, '1070 нижня обв\'язка 60×40×3', ext_from=100)
cf.dimV(0, 498, 440, '498', ext_from=480, side='left'); cf.dimV(458, 498, 1060, '40', side='left')
cf.dimV(0, 374, 1660, '374', ext_from=1630, side='right'); cf.dimV(100, 160, 1660, '60', side='right')
cf.dimV(0, 100, 1660, '100', side='right')
cf.pos(1, 500, 250, 450, 300); cf.pos(2, 1610, 200, 1650, 260); cf.pos(3, 1110, 300, 1060, 380); cf.pos(4, 1150, 250, 1200, 300)
cf.pos(5, 800, 478, 800, 560); cf.pos(6, 1380, 354, 1380, 430); cf.pos(7, 900, 130, 900, 60)
frame_front_svg = cf.svg('Спільний каркас спереду')

cp = View(420, 1690, -60, 660, pad=(130, 120, 60, 110), flip=False, k=1.9)
for x in (480, 1590):
    for z in (0, 560): cp.rect(x, z, x + 40, z + 40, 'fill')
for x in (1090, 1130):
    for z in (0, 560): cp.rect(x, z, x + 40, z + 40, 'fill')
cp.rect(520, 0, 1090, 40, 'ol'); cp.rect(520, 560, 1090, 600, 'ol'); cp.rect(480, 40, 520, 560, 'ol'); cp.rect(1090, 40, 1130, 560, 'ol')
cp.rect(1170, 0, 1590, 40, 'ol'); cp.rect(1170, 560, 1590, 600, 'ol'); cp.rect(1130, 40, 1170, 560, 'ol'); cp.rect(1590, 40, 1630, 560, 'ol')
cp.rect(1110, 40, 1150, 560, 'hid')
cp.text(805, 300, 'кільце 458–498 під коробом', 'note', 'middle'); cp.text(1380, 300, 'кільце 334–374 під кладкою', 'note', 'middle')
cp.dimH(480, 1630, -30, '1150', ext_from=0); cp.dimV(0, 600, 1670, '600', ext_from=1630, side='right')
cp.text(1130, 640, 'пунктир — поперечка 60×40 під стиком', 'note', 'middle')
frame_plan_svg = cp.svg('Спільний каркас згори')

cs = View(-60, 700, -60, 560, pad=(130, 120, 60, 110), k=1.6)
cs.line(-60, 0, 700, 0, 'ol')
for z in (0, 560): cs.rect(z, 160, z + 40, 498, 'fill')                                 # stubs (mangal side)
for z in (0, 560): cs.rect(z, 100, z + 40, 160, 'fill')                                 # bottom rails in section
cs.rect(40, 100, 560, 160, 'ol'); cs.text(300, 125, 'поперечка 60×40×3 під стиком', 'note', 'middle')
cs.rect(40, 458, 560, 498, 'ol'); cs.text(300, 478, 'кільце мангала', 'note', 'middle')
cs.rect(40, 334, 560, 374, 'hid'); cs.text(300, 354, 'кільце печі (за стиком)', 'note', 'middle')
cs.rect(40, 160, 560, 163, 'fill')
cs.dimH(0, 600, -40, '600', ext_from=0); cs.dimV(160, 498, 640, '338 стійка-вставка', ext_from=600, side='right')
cs.dimV(0, 100, 640, '100', side='right'); cs.text(300, 540, 'розріз по стику мангала і печі, зад ліворуч', 'note', 'middle')
frame_side_svg = cs.svg('Спільний каркас — стик')

# ======================= BILL OF MATERIALS =======================
TUBE = 2.31; A40 = 2.42; F40 = 1.26; A25 = 1.12; A75 = 5.69; A50 = 3.77; A30 = 1.36; SQ10 = 0.785
SH3 = 23.55; SH5 = 39.25; SH2 = 15.7; SH15 = 11.78

grating = 6 * 1364 + 7 * 714 - 4 * 380 + 6 * 614 + 8 * 1314 - 4 * 380  # sink still cuts 4 bars each way   # mm, from the model
lid_area = 1.370 * 0.620 + 0.720 * 0.700 - 0.38 * 0.38
gab = {}  # v24: no bulky gabions any more, only thin pebble cassettes (counted below)
CAS = {'side by the post': (1.22, 0.73), 'end of the return': (0.70, 0.73), 'cargo by the oven': (0.156, 0.661), 'cargo for skewers': (0.182, 0.731)}
pebble_vol = sum(a * b * 0.08 for a, b in CAS.values())  # v17: the one next to the kazan is now a cargo niche with a false-gabion front
H = 0.73
gab_angle = sum(4 * H + 4 * (a + b) for a, b in gab.values())
gab_mesh = sum(2 * (a * b + a * H + b * H) for a, b in gab.values())
gab_vol = sum(a * b * H for a, b in gab.values())

# ---- v26 quantities (counted from the model) ----
# grating under the worktop lid (lid from x 1630, sink cut-out 1695..2075 x 110..490)
grating = 0   # v27: no concrete lid any more
lid_area = 1.170 * 0.620 + 0.720 * 0.700 - 0.38 * 0.38
panel_area = 0.403 * 0.74 + 0.576 * 0.70 + 0.60 * 0.788           # v27: left door, fridge door, post side
top_area = 1.15 * 0.61 + 0.43 * 0.61                               # worktops: sheet 0.5 + tile on sealant
sheet05 = 1.19 * 0.63 + 0.47 * 0.63 + panel_area                   # with the bent edges
tube_m = {
    'Стійки рейлінгової стінки над правою тумбою': 2 * .85,
    'Мангал і піч: кільця і бічні обв\'язки': 2 * .57 + 2 * .52 + 2 * .42 + 2 * .52 + 2 * .52,
    'Ліва тумба': 4 * .768 + 2 * (2 * .35 + 2 * .52),
    'Тумба': 6 * .768 + 2 * (.506 + .502 + .506 + .502 + 3 * .52) + 2 * .52,
}
tube40x3 = 2 * .498 + 2 * .374 + 2 * .338 + 2 * .214      # 4 legs + 4 stubs at the joint
tube60 = 2 * 1.07 + .52                                    # long bottom rails + cross rail
tube20 = 2 * (.403 + .74) + 2 * (.576 + .70) + 2 * (.60 + .788) + 3 * .52 + 2 * .426 + .52   # panel frames + cross bars under the worktops

parts = [
 ('Частина 1 · Мангал 650 і піч під казан 500 на спільному каркасі', [
   ('Труба 40×40×3', f'{tube40x3:.1f} м', '4 ніжки (2 × 498, 2 × 374) і 4 стійки-вставки на стику (2 × 338, 2 × 214)'),
   ('Труба 60×40×3', f'{tube60:.1f} м', 'нижні поздовжні обв\'язки 2 × 1070 на ребро і поперечка під стиком 520'),
   ('Труба 40×40×2', f"{tube_m['Мангал і піч: кільця і бічні обв\'язки']:.1f} м", 'кільце під мангалом 2 × 570 + 2 × 520, під піччю 2 × 420 + 2 × 520, бічні нижні 2 × 520'),
   ('Лист 3 мм', '1 лист 1250×2500', 'короб і полиця мангала, полиця, дно, задня стінка і полотно дверцят печі'),
   ('Кутник 75×50×6', '2 × 650', 'накриває торці рядів, 10 пропилів під шампури'),
   ('Лист 2 мм', '0,86 м²', 'кришка мангала'),
   ('Кутник 25×25×3', '2,5 + 1,1 м', 'рамка кришки мангала; рамка дверцят печі'),
   ('Петля приварна Ø20 × 80, ланцюжок, дерев’яна ручка', '2 + 1 + 1', 'кришка мангала'),
   ('Лист 1,5 мм', '0,9 м²', 'ящик під мангалом'),
   ('Кульові напрямні 500, ручка-рейлінг 320', '1 пара + 1', 'ящик'),
   ('Смуга 40×4', '2 × 520 + 2,5 м', 'планки під напрямні ящика; пояс і стійки дверцят печі'),
   ('Лист 5 мм', '0,35 м²', 'плита печі 486×586, фланець Ø160, накладка 90×100'),
   ('Кутник 40×40×4', '4 × 419', 'кути печі'),
   ('Кутник 50×50×5', '280', 'перемичка над дверцятами печі'),
   ('Шамот ША-5 230×114×65', '≈ 75 шт', 'мангал і піч, ≈ 64 нетто + підрізка'),
   ('Облицювальна цегла 250×120×65', '7 шт', 'фасад печі, розрізати вздовж'),
   ('Базальтовий картон 5 мм, шнур Ø10–12', '0,2 м² + 2 м', 'між шамотом і облицюванням; під плиту'),
   ('Розчин жаростійкий', '2 мішки', 'шамот і облицювання'),
   ('Труба димохідна Ø110 чорна сталь, коліно, грибок', '1,6 м + 1 + 1', 'фарбувати термофарбою; казан уже є'),
 ]),
 ('Ліва тумба на інвентар 430 × 600', [
   ('Труба 40×40×2', f"{tube_m['Ліва тумба']:.1f} м", '4 стійки 777, обв\'язки 2 × (2 × 350 + 2 × 520)'),
   ('Лист 0,5 мм + плитка на герметику', '430 × 610', 'стільниця, поперечка 20×20 посередині'),
   ('Лист 1,5 мм', '1,6 м²', 'зад, боки, дно, полиця, планка біля мангала'),
   ('Базальтовий картон 8–10 мм', '0,36 м²', 'бік до мангала'),
   ('Смуга 40×4', '500', 'рейка для шампурів, 10 прорізів'),
   ('Ніжки M10, петлі, ручка, защіпка', '4 + 2 + 1 + 1', ''),
   ('Кам\'яна панель 403 × 740', '1', 'дверцята, див. «Кам\'яні панелі»'),
 ]),
 ('Частина 2 · Тумба з умивальником і холодильником', [
   ('Труба 40×40×2', f"{tube_m['Тумба']:.1f} м", '6 стійок 768 + обв\'язки на двох рівнях + напрямні полиці'),
   ('Лист 1,5 мм', '2,8 м²', 'зад, бік до печі, перегородка, два дна, полиця над холодильником, дверцята шафи 510 × 700'),
   ('Базальтовий картон 8–10 мм', '0,33 м²', 'бік до печі'),
   ('Лист 4 мм', '6 × 40×40', 'пластини під ніжки'),
   ('Ніжки M10, петлі, ручки, защіпки', '6 + 4 + 2 + 2', 'дверцята шафи і холодильника'),
   ('Лист 0,5 мм + плитка на герметику', '1150 × 610', 'стільниця; поперечки 20×20 і рамка навколо вирізу умивальника'),
   ('Кам\'яні панелі 576 × 700 і 600 × 788', '2', 'дверцята холодильника, бік біля стовпа'),
   ('Умивальник 380 накладний, змішувач, сифон; холодильник Ardesto DFM-50X', '1 + 1', 'купуються окремо'),
 ]),
 ('Кам\'яні панелі (3 шт)', [
   ('Труба 20×20×1,5', f'{tube20:.1f} м', 'рамки трьох панелей і поперечки під стільницями'),
   ('Лист 0,5 мм', f'{sheet05:.2f} м²', 'дно панелей і обидві стільниці — розкрій на 1 лист 1250×2500 перевірено'),
   ('Смола поліефірна з затверджувачем', '≈ 5 кг', 'камінь приклеюється на шар ≈ 5 мм'),
   ('Гелькоут прозорий / лак з УФ-захистом', '1 кг', 'верхній шар від пожовтіння'),
   ('Камінець декоративний 10–20', '≈ 20 кг', ''),
   ('Болти M6 × 20 + гайки', '16', 'кріплення бічної панелі; дверцята — на петлях'),
 ]),
 ('Дровники-стінки зліва і справа (2 шт)', [
   ('Труба 40×40×2', '2 × 14,7 м', 'на кожну: 2 ферми, приварені до стовпів (зовнішній пояс 2040, горизонталі 2 × 360, 4 розкоси ≈ 580), рейки-основа 2 × 1360 + 2 поперечки, верхня зв\'язка 1360'),
   ('Ніжки регульовані M10', '2 × 3', 'під зовнішні пояси і посередині зовнішньої рейки'),
   ('Дрова колоті, поліно ≈ 400', '≈ 2 скл. м³', 'по ≈ 1 на стінку'),
 ]),
 ('Дах односкатний 5000 × 2200', [
   ('Труба 100×100×3', '2 × 5000 + 2 × 350', 'балки на стовпах з випусками по 1 м; надставки передніх стовпів'),
   ('Труба 60×40×2', '10 × 2270', 'крокви, крок до 600'),
   ('Труба 40×20×2', '5 × 5000', 'обрешітка, крок ≈ 440'),
   ('Труба 40×40×2', '8 × 850', 'підкоси біля стовпів і під випусками'),
   ('Профнастил НС35 0,5 мм з полімерним покриттям', '≈ 12 м²', '5040 × 2330 + напуск'),
   ('Саморізи покрівельні 4,8×35 з EPDM', '≈ 150', ''),
   ('Планки торцеві і карнизна', '2 × 2,4 + 5 м', ''),
   ('Водостік: жолоб Ø125, труба Ø90', '5 м + 2,5 м', 'кронштейни, заглушки, воронка, 2 коліна'),
   ('Прохідники покрівельні (майстер-флеш)', '2', 'для Ø250 і Ø110'),
   ('Сендвіч-труба Ø250/350 і Ø110/200', '1 м + 0,7 м', 'утеплена ділянка в зоні даху'),
 ]),
 ('Витяжка над мангалом', [
   ('Лист 1,5 мм', '≈ 0,8 м²', 'піраміда: рот 850 × 970, горловина 250 × 250, висота 325'),
   ('Лист 1 мм', '≈ 1,1 м²', 'задній екран 850 × 500 і дві щоки'),
   ('Кутник 25×25×3', '3,7 м', 'рамка по низу витяжки + край щік'),
   ('Труба 60×40×3', '2 × 2,0 м', 'стійки позаду мангала, на бетонних п\'ятах'),
   ('Труба димохідна Ø250, чорна сталь 2 мм', '1,6 м', 'над витяжкою, розкріпити до даху або стовпів'),
   ('Турбодефлектор Ø250', '1', 'на верх труби'),
   ('Сітка іскрогасна нерж.', '300 × 300', 'у горловину'),
 ]),
 ('Тримачі над стільницями', [
   ('Труба 40×40×2', '2 × 850', 'стійки над задніми стійками правої тумби (біля печі і над перегородкою), до 1650'),
   ('Труба 40×20×2', '1130', 'верхня перекладина на 1610–1650'),
   ('Смуга 40×4', '2 × 550 + 3 × 160', 'планки під магнітну планку на 1320–1360; кронштейни полиці'),
   ('Лист 4 мм', '2 × 60×60', 'пластини на правий стовп'),
   ('Труба нерж. Ø16 + 4 тримачі', '510 + 440', 'рейлінги: над правою тумбою між стійками і зліва біля мангала'),
   ('Труба 20×20×1,5', '360', 'стійка лівого рейлінга на задній обв\'язці лівої тумби'),
   ('Магнітна планка для ножів 450', '1', 'на смузі над робочою стільницею біля холодильника'),
   ('Лист перфорований 1,5 мм', '1130 × 140', 'полиця для спецій, глибина 120 + бортик 20'),
   ('Тримач паперових рушників', '1', 'під полицею над умивальником'),
   ('S-гачки', '8', 'по 4 на кожен рейлінг'),
 ]),
]

steel = [
 ('Труба 40×40×2', sum(tube_m.values()), TUBE, 'м'),
 ('Труба 40×40×3', tube40x3, 3.30, 'м'),
 ('Труба 60×40×3', tube60, 4.25, 'м'),
 ('Труба 20×20×1,5', tube20, 0.82, 'м'),
 ('Кутник 75×50×6', 1.3, A75, 'м'),
 ('Кутник 50×50×5', 0.28, A50, 'м'),
 ('Кутник 40×40×4', 1.68, A40, 'м'),
 ('Кутник 25×25×3', 3.6, A25, 'м'),
 ('Смуга 40×4', 5.6, F40, 'м'),
 ('Труба 40×20×2', 1.13, 1.78, 'м'),
 ('Лист 5 мм', 0.35, SH5, 'м²'),
 ('Лист 3 мм', 2.7, SH3, 'м²'),
 ('Лист 2 мм', 0.9, SH2, 'м²'),
 ('Лист 1,5 мм', 5.3, SH15, 'м²'),
 ('Лист 0,5 мм', sheet05, 3.93, 'м²'),
]
steel_mass = sum(q * k for _, q, k, _ in steel)

def num(x, d=1):
    return f'{x:.{d}f}'.replace('.', ',')

# ---- materialy.md ----
md = ['# Зона мангала — список матеріалів', '',
      'Модель v33 від 22.11.2026 Кількості пораховано з моделі. Креслення ще під v24 — їх треба перерахувати.', '']
# (name, qty, unit, how to buy, what for) — qty/unit feed the Excel sheet
SHOP = [
 ('Метал', [
   ('Труба профільна 40×40×2', math.ceil(sum(tube_m.values()) * 1.1 / 6), 'хлист 6 м', f'{math.ceil(sum(tube_m.values()) * 1.1 / 6)} хлистів по 6 м', f"потрібно {num(sum(tube_m.values()))} м + 10% на різ: кільця мангала й печі, обидві тумби"),
   ('Труба профільна 40×40×3', 1, 'хлист 6 м', '1 хлист 6 м', f'потрібно {num(tube40x3)} м — 4 ніжки і стійки-вставки спільного каркаса'),
   ('Труба профільна 60×40×3', 1, 'хлист 6 м', '1 хлист 6 м (або 3 м)', f'потрібно {num(tube60)} м — нижні поздовжні обв\'язки 2 × 1070 і поперечка'),
   ('Труба профільна 20×20×1,5', 2, 'хлист 6 м', '2 хлисти по 6 м', f'потрібно {num(tube20)} м — рамки кам\'яних панелей і поперечки під стільницями'),
   ('Смуга 40×4', 6, 'м', '6 м', 'пояс і стійки печі 2,5 + планки під напрямні ящика 1,04 + рейка для шампурів 0,5 + тримачі над стільницями 1,6'),
   ('Кутник 75×50×6', 1.5, 'м', '1,5 м', 'опори шампурів 2 × 650'),
   ('Кутник 40×40×4', 2, 'м', '2 м', 'кути печі 4 × 419'),
   ('Кутник 25×25×3', 4, 'м', '4 м', 'рамка кришки мангала 2,5 + рамка дверцят печі 1,1'),
   ('Кутник 50×50×5', 0.3, 'м', '0,3 м', 'перемичка над дверцятами печі'),
   ('Лист 3 мм', 1, 'лист 1250×2500', '1 лист 1250×2500', 'мангал і піч — розкрій перевірено'),
   ('Лист 1,5 мм', 2, 'лист 1250×2500', '2 листи 1250×2500', 'потрібно ≈ 5,3 м²: тумба 2,8, ліва тумба 1,6, ящик 0,9'),
   ('Лист 2 мм', 0.9, 'м²', 'шматок ≈ 1000×900', 'кришка мангала, екран дверцят печі'),
   ('Лист 5 мм', 0.6, 'м²', 'шматок ≈ 1000×600', 'плита печі, фланець, накладка'),
   ('Лист 0,5 мм', 1, 'лист 1250×2500', '1 лист 1250×2500', f'потрібно {num(sheet05, 2)} м²: дві стільниці з загнутими краями і дно трьох панелей — розкрій перевірено'),
   ('Смуга 25×6', 0.2, 'м', 'обрізок 200', 'кронштейни ручки кришки мангала'),
   ('Лист 4 мм', 1, 'обрізок', 'обрізок 40×500', '10 пластин 40×40 під ніжки'),
 ]),
 ('Цегла, кладка, термоізоляція', [
   ('Шамот ША-5 230×114×65', 75, 'шт', '75 шт', '≈ 64 у кладці + підрізка'),
   ('Облицювальна цегла 250×120×65', 7, 'шт', '7 шт', 'фасад печі, розрізати вздовж'),
   ('Розчин жаростійкий (шамотний)', 2, 'мішок 20–25 кг', '2 мішки по 20–25 кг', 'мангал і піч'),
   ('Базальтовий картон 5 мм', 0.2, 'м²', '0,2 м²', 'між шамотом і облицюванням'),
   ('Базальтовий картон 8–10 мм', 0.7, 'м²', '0,7 м²', 'ліва тумба до мангала 0,36 + тумба до печі 0,33'),
   ('Шнур жаростійкий Ø10–12', 2, 'м', '2 м', 'під плиту печі'),
 ]),
 ('Кам\'яні панелі', [
   ('Смола поліефірна з затверджувачем', 5, 'кг', '5 кг', f'{num(panel_area, 2)} м²: камінь приклеюється на тонкий шар ≈ 5 мм'),
   ('Гелькоут прозорий / лак з УФ-захистом', 1, 'кг', '1 кг', 'верхній шар, щоб смола не жовтіла'),
   ('Камінець декоративний 10–20', 1, 'мішок 20 кг', '1 мішок 20 кг', 'потрібно ≈ 20 кг'),
   ('Болт M6 × 20 + гайка', 16, 'шт', '16 шт', 'кріплення бічної панелі до каркаса'),
 ]),
 ('Стільниці', [
   ('Плитка керамограніт 10 мм', round(top_area * 1.15, 1), 'м²', f'{num(top_area * 1.15)} м²', f'{num(top_area, 2)} м² + запас на підрізку'),
   ('Герметик поліуретановий / MS-полімер 290 мл', 3, 'шт', '3 тюбики', 'клеїти плитку на лист смугами або гребінкою'),
   ('Ґрунт по металу під герметик', 0.5, 'л', '0,5 л', 'лист знежирити й заґрунтувати'),
   ('Затирка вулична', 1, 'кг', '1 кг', 'шви ≈ 2 мм, можна тим самим герметиком'),
 ]),
 ('Кріплення і фурнітура', [
   ('Болт M10 × 120 + гайка самоконтрячна + 2 шайби', 4, 'компл.', '4 компл.', 'піч–тумба'),
   ('Болт M8 × 30 + гайка + шайби', 8, 'компл.', '8 компл.', 'фланець труби 4, накладка 4'),
   ('Болт M6 + втулка Ø16 × 15', 4, 'компл.', '4 компл.', 'екран дверцят печі'),
   ('Ніжка регульована M10, п\'ята Ø40', 10, 'шт', '10 шт', 'тумба 6, ліва тумба 4'),
   ('Петля приварна', 8, 'шт', '8 шт', 'дверцята печі, шафи, холодильника і лівої тумби — по 2'),
   ('Петля приварна Ø20 × 80', 2, 'шт', '2 шт', 'кришка мангала'),
   ('Ланцюжок 3 мм + вушка', 1, 'компл.', '0,6 м + 4 вушка', 'обмежувач кришки мангала'),
   ('Ручка дерев’яна Ø28 × 220', 1, 'шт', '1 шт', 'кришка мангала'),
   ('Кульові напрямні повного висуву 500, 45 мм, 70 кг, нержавійка', 1, 'пара', '1 пара', 'ящик під мангалом'),
   ('Ручка-рейлінг 320', 1, 'шт', '1 шт', 'ящик під мангалом'),
   ('Засувка з ручкою', 1, 'шт', '1 шт', 'дверцята печі'),
   ('Ручка + магнітна защіпка', 3, 'компл.', '3 компл.', 'дверцята шафи, холодильника і лівої тумби'),
 ]),
 ('Дровники-стінки', [
   ('Труба профільна 40×40×2 (дровники)', 6, 'хлист 6 м', '6 хлистів по 6 м', 'потрібно 2 × 14,7 м + різ; ферми варяться до стовпів'),
   ('Ніжка регульована M10 (дровники)', 6, 'шт', '6 шт', ''),
   ('Дрова колоті, поліно ≈ 400', 2.0, 'скл. м³', '≈ 2 скл. м³', 'якщо свої — не купувати'),
 ]),
 ('Дах', [
   ('Труба профільна 100×100×3', 11, 'м', '2 × 5 м + 1 м', 'балки 5000 з випусками по 1 м і надставки передніх стовпів 2 × 350'),
   ('Труба профільна 60×40×2 (крокви)', 4, 'хлист 6 м', '4 хлисти по 6 м', 'потрібно 10 × 2,27 м'),
   ('Труба профільна 40×20×2 (обрешітка)', 5, 'хлист 6 м', '5 хлистів по 6 м', 'потрібно 5 × 5 м'),
   ('Труба профільна 40×40×2 (підкоси)', 1, 'хлист 6 м', '1 хлист 6 м', '8 підкосів по 850'),
   ('Профнастил НС35 0,5 мм з полімерним покриттям', 12, 'м²', '≈ 12 м²', 'лист на всю довжину ската 2330, напуск по хвилі'),
   ('Саморізи покрівельні 4,8×35 з EPDM', 150, 'шт', '≈ 150 шт', ''),
   ('Планка торцева (вітрова) 2 м', 3, 'шт', '3 шт', ''),
   ('Планка карнизна 2 м', 3, 'шт', '3 шт', ''),
   ('Жолоб Ø125', 5, 'м', '5 м', 'з кронштейнами і заглушками'),
   ('Труба водостічна Ø90 + 2 коліна + воронка', 1, 'компл.', '2,5 м + 2 + 1', 'правий задній кут'),
   ('Прохідник покрівельний (майстер-флеш)', 2, 'шт', '2 шт', 'Ø250 і Ø110'),
   ('Сендвіч-труба Ø250/350, 1 м', 1, 'шт', '1 шт', 'утеплена ділянка труби витяжки крізь дах'),
   ('Сендвіч-труба Ø110/200, 1 м', 1, 'шт', '1 шт', 'утеплена ділянка труби печі крізь дах'),
 ]),
 ('Витяжка над мангалом', [
   ('Лист 1,5 мм (витяжка)', 1, 'лист 1250×2500', '1 лист 1250×2500', 'піраміда витяжки 0,8 м²; з того ж листа — екран і щоки, якщо не брати 1 мм'),
   ('Труба профільна 60×40×3 (стійки витяжки)', 1, 'хлист 6 м', '1 хлист 6 м (потрібно 4 м)', 'дві стійки позаду мангала'),
   ('Кутник 25×25×3 (витяжка)', 4, 'м', '4 м', 'рамка по низу і край щік'),
   ('Труба димохідна Ø250, чорна сталь 2 мм', 1.6, 'м', '≈ 1,6 м', 'від горловини вгору'),
   ('Турбодефлектор Ø250', 1, 'шт', '1', 'тяга від вітру без електрики, захист від дощу'),
   ('Сітка іскрогасна нерж.', 1, 'шматок', '300 × 300', 'у горловину'),
   ('Бетон для п\'ят стійок (суха суміш М300)', 2, 'мішок 25 кг', '2 мішки', 'дві п\'яти 300×300×400 за плиткою'),
 ]),
 ('Тримачі над стільницями', [
   ('Труба профільна 40×20×2', 1.2, 'м', '1,2 м', 'верхня перекладина рейлінгової стінки'),
   ('Труба нерж. Ø16 (рейлінг)', 1, 'м', '1 м', 'рейлінги 510 і 440'),
   ('Тримачі рейлінгу Ø16', 4, 'шт', '4 шт', ''),
   ('Магнітна планка для ножів 450', 1, 'шт', '1 шт', ''),
   ('Лист перфорований 1,5 мм', 1, 'шматок', 'шматок 1200×150', 'полиця для спецій'),
   ('Тримач паперових рушників', 1, 'шт', '1 шт', ''),
   ('S-гачки', 8, 'шт', '8 шт', 'ополоник, шумівка, лопатка, щипці; інструмент мангала'),
 ]),
 ('Димохід і розетка', [
   ('Труба димохідна Ø110, чорна сталь 2 мм', 2.4, 'м', '≈ 2,4 м', 'вивід угору до ≈ 3100 крізь дах, фарбувати термофарбою'),
   ('Коліно 90° Ø110, чорна сталь', 1, 'шт', '1', 'від фланця печі вгору'),
   ('Грибок Ø110, чорна сталь', 1, 'шт', '1', 'на верх труби'),
   ('Розетка вулична IP44 + УЗО', 1, 'компл.', '1', 'для холодильника — ще не вирішено'),
 ]),
 ('Фарба і витратні', [
   ('Фарба термостійка до 600 °C', 1.5, 'л', '1,5 л (або 4 балончики)', 'мангал, піч і димохід'),
   ('Ґрунт по металу', 1, 'л', '1 л', 'тумби, рамки панелей'),
   ('Фарба по металу вулична', 1, 'л', '1 л', 'тумби, рамки панелей (темна)'),
   ('Електроди 3 мм або дріт для напівавтомата', 3, 'кг', '≈ 3 кг', ''),
   ('Диски відрізні 125', 10, 'шт', '10', ''),
   ('Диски зачисні 125', 3, 'шт', '3', ''),
 ]),
]

# Bought separately, shown with a price but NOT counted in the total; the kazan is already there
EXTRA = [
   ('Холодильник Ardesto DFM-50X', 1, 'шт', '1', '50 л'),
   ('Умивальник 380×380', 1, 'шт', '1', ''),
   ('Змішувач, сифон, крани', 1, 'компл.', '1 компл.', ''),
]
# Rough unit prices, UAH per the "unit" column (Ukraine, 2026, retail; metal ~45-50 UAH/kg). Estimates, not quotes.
PRICE = {
 'Труба профільна 40×40×2 (дровники)': 510, 'Ніжка регульована M10 (дровники)': 60, 'Пластина 60×60×4 + болт M8 (дровники)': 40,
 'Дрова колоті, поліно ≈ 400': 1500,
 'Труба профільна 100×100×3': 450, 'Труба профільна 60×40×2 (крокви)': 450, 'Труба профільна 40×20×2 (обрешітка)': 360,
 'Труба профільна 40×40×2 (підкоси)': 510, 'Профнастил НС35 0,5 мм з полімерним покриттям': 330, 'Саморізи покрівельні 4,8×35 з EPDM': 3,
 'Планка торцева (вітрова) 2 м': 180, 'Планка карнизна 2 м': 150, 'Жолоб Ø125': 250, 'Труба водостічна Ø90 + 2 коліна + воронка': 900,
 'Прохідник покрівельний (майстер-флеш)': 450, 'Сендвіч-труба Ø250/350, 1 м': 2500, 'Сендвіч-труба Ø110/200, 1 м': 1300,
 'Лист 1,5 мм (витяжка)': 1850, 'Труба профільна 60×40×3 (стійки витяжки)': 1300, 'Кутник 25×25×3 (витяжка)': 38,
 'Труба димохідна Ø250, чорна сталь 2 мм': 1100, 'Турбодефлектор Ø250': 1500, 'Сітка іскрогасна нерж.': 150,
 "Бетон для п'ят стійок (суха суміш М300)": 160,
 'Труба профільна 40×20×2': 60, 'Труба нерж. Ø16 (рейлінг)': 250, 'Тримачі рейлінгу Ø16': 80, 'Магнітна планка для ножів 450': 400,
 'Лист перфорований 1,5 мм': 300, 'Тримач паперових рушників': 250, 'S-гачки': 20,
 'Труба профільна 40×40×2': 510, 'Труба профільна 40×40×3': 1000, 'Труба профільна 60×40×3': 1300, 'Труба профільна 20×20×1,5': 300,
 'Квадрат 10×10': 150, 'Смуга 70×3': 360, 'Смуга 40×4': 45,
 'Кутник 75×50×6': 200, 'Кутник 40×40×4': 85, 'Кутник 25×25×3': 40, 'Кутник 50×50×5': 160,
 'Лист 3 мм': 3300, 'Лист 3 мм, шматок 430×600': 350, 'Лист 1,5 мм': 1850, 'Лист 5 мм': 1800, 'Лист 2 мм': 850,
 'Лист 0,5 мм': 750, 'Смуга 25×6': 100, 'Лист 4 мм': 30,
 'Шамот ША-5 230×114×65': 55, 'Облицювальна цегла 250×120×65': 25, 'Розчин жаростійкий (шамотний)': 450,
 'Базальтовий картон 5 мм': 1000, 'Базальтовий картон 8–10 мм': 800, 'Шнур жаростійкий Ø10–12': 80,
 'Смола поліефірна з затверджувачем': 260, 'Гелькоут прозорий / лак з УФ-захистом': 600, 'Камінець декоративний 10–20': 350,
 'Болт M6 × 20 + гайка': 5,
 'Плитка керамограніт 10 мм': 650, 'Герметик поліуретановий / MS-полімер 290 мл': 280, 'Ґрунт по металу під герметик': 250,
 'Затирка вулична': 100,
 'Болт M10 × 120 + гайка самоконтрячна + 2 шайби': 35, 'Болт M8 × 30 + гайка + шайби': 15,
 'Болт M6 + втулка Ø16 × 15': 20, "Ніжка регульована M10, п'ята Ø40": 60, 'Петля приварна': 40, 'Петля приварна Ø20 × 80': 80,
 'Ланцюжок 3 мм + вушка': 150, 'Ручка дерев’яна Ø28 × 220': 150,
 'Кульові напрямні повного висуву 500, 45 мм, 70 кг, нержавійка': 2000, 'Ручка-рейлінг 320': 150,
 'Засувка з ручкою': 150, 'Ручка + магнітна защіпка': 150,
 'Труба димохідна Ø110, чорна сталь 2 мм': 300, 'Коліно 90° Ø110, чорна сталь': 250, 'Грибок Ø110, чорна сталь': 250,
 'Умивальник 380×380': 2000, 'Змішувач, сифон, крани': 2000, 'Холодильник Ardesto DFM-50X': 7500, 'Розетка вулична IP44 + УЗО': 1000,
 'Фарба термостійка до 600 °C': 700, 'Ґрунт по металу': 250, 'Фарба по металу вулична': 350,
 'Електроди 3 мм або дріт для напівавтомата': 130, 'Диски відрізні 125': 30, 'Диски зачисні 125': 60,
}
APPLIANCES = set()
def money(x):
    return f'{round(x / 10) * 10:,.0f}'.replace(',', ' ')
md += ['## Що купити — загальний список', '',
       'Однакові позиції з усіх частин складено разом і округлено до того, як матеріал продають. Майданчик і стовпи вже є (надставки передніх стовпів — у розділі «Дах»), у список не входять.', '']
missing = [a for _, rows in SHOP for a, *_ in rows if a not in PRICE]
assert not missing, missing
cat_sum = {}
for cat, rows in SHOP:
    md += [f'### {cat}', '', '| | Матеріал | Купити | Для чого | ≈ грн |', '|---|---|---|---|---:|']
    md += [f'| ☐ | {a} | {buy} | {c} | {money(q * PRICE[a])} |' for a, q, u, buy, c in rows]
    cat_sum[cat] = sum(q * PRICE[a] for a, q, *_ in rows)
    md += [f'| | **Разом** | | | **≈ {money(cat_sum[cat])}** |', '']
total = sum(cat_sum.values())
appl = sum(q * PRICE[a] for _, rows in SHOP for a, q, *_ in rows if a in APPLIANCES)
md += ['### Орієнтовна вартість', '',
       'Ціни приблизні, роздріб в Україні, 2026 (метал ≈ 45–50 грн/кг). Реальні можуть відрізнятися на ±20–30 % залежно від міста й магазину. '
       'Не входять: доставка, різка металу в магазині, робота зварювальника, майданчик і стовпи.', '',
       '| Що | ≈ грн |', '|---|---:|']
md += [f'| {cat} | {money(v)} |' for cat, v in cat_sum.items()]
extra_sum = sum(q * PRICE[a] for a, q, *_ in EXTRA)
md += [f'| **Усе разом** | **≈ {money(total)}** |', '',
       'Казан уже є. Холодильник, умивальник і змішувач купуються окремо й у суму не входять:', '',
       '| | Що | ≈ грн |', '|---|---|---:|']
md += [f'| ☐ | {a} | {money(q * PRICE[a])} |' for a, q, u, buy, c in EXTRA]
md += [f'| | разом окремо | ≈ {money(extra_sum)} |', '']
md += ['---', '', '# Розбивка по частинах', '']
md += ['## Прокат разом (з запасом під різ брати +10%)', '', '| Профіль | Кількість | Маса, кг |', '|---|---:|---:|']
for n, q, k, u in steel:
    md.append(f'| {n} | {num(q, 2)} {u} | {num(q * k)} |')
md += [f'| **Разом** | | **≈ {steel_mass:.0f}** |', '']
for title, rows in parts:
    md += [f'## {title}', '', '| Матеріал | Кількість | Примітка |', '|---|---|---|']
    md += [f'| {a} | {b} | {c} |' for a, b, c in rows]
    md.append('')
md += ['## Шамот і цегла разом', '',
       '- Шамот ША-5 230×114×65: ≈ 75 шт (≈ 64 нетто в моделі + підрізка).',
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
      <p>Версія 33: в одну лінію глибиною 600 — тумба зліва 430, мангал 650 і піч під казан 500 на спільному каркасі, тумба з умивальником і холодильником 1150; над мангалом витяжка, над тумбою рейлінгова стінка; односкатний дах з випусками по 1 м, з боків дровники 2 м на фермах, приварених до стовпів. Майданчик 3000 × 1500.</p>
    </div>
    <dl class="meta">
      <dt>Модель</dt><dd>v33 · 22.11.2026</dd>
      <dt>Розміри</dt><dd>мм, висоти від плитки</dd>
      <dt>Сталь</dt><dd>≈ {steel_mass:.0f} кг</dd>
    </dl>
  </header>

  <h2 class="sheet-h">Аркуш 1 · Комплекс</h2>
  <div class="grid">
    <section class="v wide"><h2>План <span>зад угорі; дах, витяжка, полиця і холодильник пунктиром; лінія А–А через умивальник</span></h2><div class="sc">{plan_svg}</div></section>
    <section class="v wide"><h2>Фасад <span>стовпи і труба обрізані</span></h2><div class="sc">{front_svg}</div></section>
    <section class="v"><h2>Розріз А–А <span>через умивальник</span></h2><div class="sc">{sect_svg}</div></section>
    <section class="notes">
      <h2>Збирання</h2>
      <ul>
        <li>Мангал і піч стоять на спільному каркасі з 4 ніжками; права тумба прикручена до правих ніжок печі 4 болтами M10 і пластиною ззаду.</li>
        <li>Ліва тумба стоїть окремо на своїх ніжках, впритул до мангала; бік до мангала з базальтовим картоном.</li>
        <li>Стільниці: лист 0,5 на обв'язці й поперечках 20×20, плитка на герметику, верх на 800.</li>
        <li>Рейлінгова стінка: стійки продовжують задні стійки правої тумби, правий кінець — на болтах до стовпа.</li>
        <li>Витяжка стоїть на двох стійках 60×40 позаду мангала; труба Ø250 крізь дах.</li>
        <li>Дровники: ферми 40×40 приварені до стовпів, зовнішні пояси на ніжках.</li>
        <li>Майданчик і стовпи 100×100 вже є; передні стовпи надставлені до 2750.</li>
      </ul>
    </section>
  </div>

  <h2 class="sheet-h">Аркуш 2 · Мангал 650 × 600, витяжка, дах, ліва тумба, дровник</h2>
  <div class="grid">
    <section class="v"><h2>Вид спереду</h2><div class="sc">{mangal_front_svg}</div></section>
    <section class="v"><h2>Розріз поперек <span>зад ліворуч</span></h2><div class="sc">{mangal_side_svg}</div></section>
    <section class="v"><h2>Витяжка, природна тяга <span>розріз збоку, зад ліворуч</span></h2><div class="sc">{hood_svg}</div></section>
    <section class="v"><h2>Дах, розріз збоку <span>зад ліворуч, скат назад</span></h2><div class="sc">{roof_side_svg}</div></section>
    <section class="v wide"><h2>Дах спереду <span>випуски по 1 м з боків</span></h2><div class="sc">{roof_front_svg}</div></section>
    <section class="v wide"><h2>Дровник-стінка, вид збоку <span>зад ліворуч; праворуч — ферма, приварена до стовпа (з торця); таких 2: зліва і справа</span></h2><div class="sc">{firewood_svg}</div></section>
    <section class="v"><h2>Тумба зліва на інвентар <span>спереду і розріз уздовж (зад ліворуч)</span></h2><div class="sc">{holder_svg}</div></section>
    <section class="notes">
      <h2>Мангал: позиції</h2>
      <ol>
        <li>Ніжки — труба 40×40×2, L 498, 4 шт; отвори Ø11 на 120 і 300 з боку печі.</li>
        <li>Обв'язка — труба 40×40×2: 4 × 570 і 4 × 520, рівні 100 і 458.</li>
        <li>Полиця під ящик — лист 3 мм 650×600, вирізи 40×40 по кутах; ящик на 2 кульових напрямних повного висуву 500 (45 мм, 70 кг, нержавійка), бічне кріплення на планки 40×4 між ніжками.</li>
        <li>Короб — лист 3 мм: дно 650×600 на 498, борти висотою 302 до 800.</li>
        <li>Кутник 75×50×6, L 650, 2 шт: полиця 75 лягає на цеглу і край короба, полиця 50 вгору до 850, 10 пропилів 12×10 з кроком 60, перший і останній за 55 від краю.</li>
        <li>Кришка — ковпак з листа 2 мм: верх 656×606, передній і задній борт 656×170 (до 830, заходять на 20 на кутник), бокові 606×195 (до 805); зсередини по верху рамка з кутника 25×25×3; ручка дерев'яна Ø28×220 на двох кронштейнах зі смуги 25×6, винос 40.</li>
        <li>Ящик під мангалом для пательні, казана, кришок: корпус 550 × 545 × 275 з листа 1,5 мм, фасад 560 × 304 з листа 1,5 мм з відбортовкою, ручка-рейлінг 320; висув 450. Між ящиком і дном короба повітряний зазор ≈ 55, дно короба під шамотом.</li>
        <li>Тумба зліва на інвентар 430 × 600: каркас 40×40, дверцята — кам'яна панель 403 × 740 на петлях з зовнішнього боку, полиця на 420, рейка для шампурів на 740, бік до мангала з базальтовим картоном.</li>
        <li>Петлі приварні Ø20 × 80, 2 шт, на 50 від країв: нижня половина до заднього кутника нижче борту кришки, верхня — до заднього борту; вісь на 840, на 16 за кутником. Кришка відкривається на 100°, тримають 2 ланцюжки-обмежувачі. Ручки шампурів — спереду.</li>
      </ol>
    </section>
  </div>

  <h2 class="sheet-h">Аркуш 3 · Спільний каркас мангала і печі під казан</h2>
  <div class="grid">
    <section class="v wide"><h2>Каркас спереду <span>короб мангала і піч пунктиром</span></h2><div class="sc">{frame_front_svg}</div></section>
    <section class="v"><h2>Каркас згори <span>верхні кільця</span></h2><div class="sc">{frame_plan_svg}</div></section>
    <section class="v"><h2>Розріз по стику <span>стійки-вставки і поперечка</span></h2><div class="sc">{frame_side_svg}</div></section>
    <section class="notes">
      <h2>Каркас: позиції</h2>
      <ol>
        <li>Ніжки мангала — труба 40×40×3, L 498, 2 шт (зовнішні кути зліва).</li>
        <li>Ніжки печі — труба 40×40×3, L 374, 2 шт (зовнішні кути справа).</li>
        <li>Стійки-вставки на стику з боку мангала — 40×40×3, L 338 (від 160 до 498), 2 шт; до підлоги не доходять.</li>
        <li>Стійки-вставки з боку печі — 40×40×3, L 214 (від 160 до 374), 2 шт.</li>
        <li>Верхнє кільце мангала 458–498: 40×40×2, 2 × 570 і 2 × 520.</li>
        <li>Верхнє кільце печі 334–374: 40×40×2, 2 × 420 і 2 × 520; на ньому лист 3 мм під кладку 500 × 600.</li>
        <li>Нижні поздовжні обв'язки — 60×40×3 на ребро (100–160), L 1070, 2 шт; поперечка під стиком 60×40×3, L 520; бічні нижні 40×40×2, L 520, 2 шт; полиці з листа 3 мм на 160.</li>
      </ol>
      <p>Кутники 40×40×4, пояс 40×4, задня стінка, плита і дверцята печі — як на окремих кресленнях печі; точні довжини всіх труб — у пакеті «виробництво».</p>
    </section>
  </div>

  <h2 class="sheet-h">Аркуш 4 · Стільниці і кам'яні панелі</h2>
  <div class="grid">
    <section class="v wide"><h2>Стільниці, вид згори <span>обв'язка і поперечки під листом пунктиром</span></h2><div class="sc">{lid_svg}</div></section>
    <section class="v"><h2>Шари стільниці <span>переріз біля переднього краю, не в масштабі по товщині</span></h2><div class="sc">{lid_layers_svg}</div></section>
    <section class="v"><h2>Кам'яна панель <span>типово, на прикладі дверцят холодильника 576 × 700</span></h2><div class="sc">{gab_svg}</div></section>
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
cf.save(os.path.join(K, 'karkas-1-speredu.svg'), 'Спільний каркас мангала і печі · спереду')
cp.save(os.path.join(K, 'karkas-2-zgory.svg'), 'Спільний каркас · згори')
cs.save(os.path.join(K, 'karkas-3-styk.svg'), 'Спільний каркас · розріз по стику')
hd.save(os.path.join(K, 'mangal-4-vytyazhka.svg'), 'Витяжка над мангалом · розріз збоку')
rs.save(os.path.join(K, 'dakh-1-rozriz.svg'), 'Дах · розріз збоку')
rf.save(os.path.join(K, 'dakh-2-speredu.svg'), 'Дах · вид спереду')
fw.save(os.path.join(K, 'drovnyk-stinka.svg'), 'Дровник-стінка · вид збоку і з торця')
hs.save(os.path.join(K, 'mangal-3-tumba-zliva.svg'), 'Тумба зліва · спереду і розріз')
L.save(os.path.join(K, 'tumba-1-stilnytsi.svg'), 'Стільниці · вид згори')
ls.save(os.path.join(K, 'tumba-2-shary-stilnytsi.svg'), 'Стільниці · шари')
g.save(os.path.join(K, 'tumba-3-kamyana-panel.svg'), 'Кам\'яна панель · типово')
print('ok, steel', round(steel_mass), 'kg; grating', grating, 'mm')

# ======================= EXCEL =======================
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.comments import Comment

AR = 'Arial'
F = Font(name=AR, size=10); FB_ = Font(name=AR, size=10, bold=True); FH = Font(name=AR, size=14, bold=True)
FI = Font(name=AR, size=10, color='0000FF'); FM = Font(name=AR, size=9, color='5D676D')
HEAD_FILL = PatternFill('solid', fgColor='1C2226'); HEAD_FONT = Font(name=AR, size=10, bold=True, color='FFFFFF')
GROUP_FILL = PatternFill('solid', fgColor='E8ECEA'); INPUT_FILL = PatternFill('solid', fgColor='FFFF00')
thin = Side(style='thin', color='CFD6D3'); BOX = Border(bottom=thin)
WRAP = Alignment(wrap_text=True, vertical='top'); TOP = Alignment(vertical='top')

wb = Workbook()
ws = wb.active; ws.title = 'Закупівля'
ws['A1'] = 'Зона мангала — що купити'; ws['A1'].font = FH
ws['A2'] = 'Модель v33 від 22.11.2026 Кількості пораховано з моделі й округлено до того, як матеріал продають. Майданчик і стовпи вже є (надставки передніх стовпів — у розділі «Дах»).'
ws['A2'].font = FM
ws['A3'] = 'Жовті клітинки — ціна за одиницю: уже вписані орієнтовні ціни (Україна, 2026), замініть на ціни свого магазину. Сума і разом рахуються самі. У колонці «Куплено» ставте «так».'
ws['A3'].font = FM
hdr = ['№', 'Матеріал', 'Кількість', 'Одиниця', 'Як купувати', 'Для чого', 'Ціна за од., грн', 'Сума, грн', 'Куплено']
r = 5
for c, h in enumerate(hdr, 1):
    cell = ws.cell(r, c, h); cell.font = HEAD_FONT; cell.fill = HEAD_FILL; cell.alignment = Alignment(vertical='center', wrap_text=True)
first = r + 1; n = 0
for cat, rows in SHOP:
    r += 1
    ws.cell(r, 1, cat).font = FB_
    for c in range(1, 10): ws.cell(r, c).fill = GROUP_FILL
    for name, q, u, buy, note in rows:
        r += 1; n += 1
        vals = [n, name, q, u, buy, note]
        for c, v in enumerate(vals, 1):
            cell = ws.cell(r, c, v); cell.font = F; cell.alignment = WRAP if c in (2, 5, 6) else TOP; cell.border = BOX
        ws.cell(r, 3).number_format = '0.##'
        pc = ws.cell(r, 7, PRICE[name]); pc.fill = INPUT_FILL; pc.font = FI; pc.number_format = '#,##0.00'; pc.border = BOX
        sc = ws.cell(r, 8, f'=IF(G{r}="","",C{r}*G{r})'); sc.font = F; sc.number_format = '#,##0.00'; sc.border = BOX
        ws.cell(r, 9).border = BOX; ws.cell(r, 9).font = F
last = r
r += 2
ws.cell(r, 7, 'Разом, грн').font = FB_
tc = ws.cell(r, 8, f'=SUM(H{first}:H{last})'); tc.font = FB_; tc.number_format = '#,##0.00'
xr = r + 3
ws.cell(xr, 2, 'Окремо, не входить у суму (казан уже є)').font = FB_
for c in range(1, 10): ws.cell(xr, c).fill = GROUP_FILL
for name, q, u, buy, note in EXTRA:
    xr += 1
    for c, v in enumerate(['', name, q, u, buy, note], 1):
        cell = ws.cell(xr, c, v); cell.font = F; cell.alignment = WRAP if c in (2, 5, 6) else TOP; cell.border = BOX
    pc = ws.cell(xr, 7, PRICE[name]); pc.fill = INPUT_FILL; pc.font = FI; pc.number_format = '#,##0.00'; pc.border = BOX
    sc = ws.cell(xr, 8, f'=IF(G{xr}="","",C{xr}*G{xr})'); sc.font = F; sc.number_format = '#,##0.00'; sc.border = BOX
ws.cell(r + 1, 7, 'Позицій куплено').font = F
ws.cell(r + 1, 8, f'=COUNTIF(I{first}:I{last},"так")&" з {n}"').font = F
for col, w in zip('ABCDEFGHI', (5, 40, 10, 15, 24, 46, 14, 14, 10)):
    ws.column_dimensions[col].width = w
ws.freeze_panes = 'A6'
ws.cell(5, 7).comment = Comment('Орієнтовні ціни за одиницю з колонки «Одиниця», роздріб в Україні 2026. Замініть на ціни свого магазину.', 'Claude')

# --- steel ---
w2 = wb.create_sheet('Прокат')
w2['A1'] = 'Прокат разом'; w2['A1'].font = FH
w2['A2'] = 'Кількість без запасу, з моделі. Маса за одиницю — довідкова (ГОСТ/ДСТУ), сині цифри можна змінити.'; w2['A2'].font = FM
for c, h in enumerate(['Профіль', 'Кількість', 'Одиниця', 'кг за од.', 'Маса, кг'], 1):
    cell = w2.cell(4, c, h); cell.font = HEAD_FONT; cell.fill = HEAD_FILL
r = 4
for name, q, k, u in steel:
    r += 1
    w2.cell(r, 1, name).font = F
    qc = w2.cell(r, 2, round(q, 2)); qc.font = FI; qc.number_format = '0.00'
    w2.cell(r, 3, u).font = F
    kc = w2.cell(r, 4, k); kc.font = FI; kc.number_format = '0.00'
    mc = w2.cell(r, 5, f'=B{r}*D{r}'); mc.font = F; mc.number_format = '0.0'
w2.cell(r + 1, 1, 'Разом').font = FB_
t2 = w2.cell(r + 1, 5, f'=SUM(E5:E{r})'); t2.font = FB_; t2.number_format = '0'
w2.cell(r + 2, 1, 'З запасом +10% на різ').font = F
t3 = w2.cell(r + 2, 5, f'=E{r + 1}*1.1'); t3.font = F; t3.number_format = '0'
for col, w in zip('ABCDE', (24, 12, 10, 10, 12)): w2.column_dimensions[col].width = w

# --- per part ---
w3 = wb.create_sheet('По частинах')
w3['A1'] = 'Розбивка по частинах'; w3['A1'].font = FH
for c, h in enumerate(['Матеріал', 'Кількість', 'Примітка'], 1):
    cell = w3.cell(3, c, h); cell.font = HEAD_FONT; cell.fill = HEAD_FILL
r = 3
for title, rows in parts:
    r += 1; w3.cell(r, 1, title).font = FB_
    for c in range(1, 4): w3.cell(r, c).fill = GROUP_FILL
    for a_, b_, c_ in rows:
        r += 1
        for c, v in enumerate((a_, b_, c_), 1):
            cell = w3.cell(r, c, v); cell.font = F; cell.alignment = WRAP; cell.border = BOX
for col, w in zip('ABC', (40, 24, 60)): w3.column_dimensions[col].width = w

for sh in wb.worksheets:
    sh.sheet_view.showGridLines = False
# --- savings options: tick "так" in the "Беру" column, the new total follows ---
SAVE = [
 ('Без компромісів', [
   ('Метал на металобазі замість роздрібного магазину (≈ 38–42 грн/кг замість 45–50)', 2000, 2500, 'нічого'),
   ('Лист 0,5, 2 і 5 мм — обрізками з металобази, а не цілими листами', 500, 800, 'нічого'),
 ]),
 ('Невеликі компроміси', [
   ('Камінь на панелях клеїти на цементний клей / розчин замість поліефірки', 1600, 1800, 'панель важча; на дверцята лівої тумби 3 петлі. Зате не боїться жару і сонця, гелькоут не потрібен'),
   ('Ящик під мангалом на саморобних напрямних з кутника замість кульових', 1600, 1800, 'ходить туго, висувається не повністю'),
   ('Замість ящика полиця на дрова (не брати разом з попереднім рядком)', 2200, 2400, 'ящика немає'),
   ('Мангал без кришки', 1200, 1400, 'не можна запікати під кришкою і закрити від дощу'),
 ]),
]
w4 = wb.create_sheet('Економія', 1)
w4['A1'] = 'Як здешевити'; w4['A1'].font = FH
w4['A2'] = 'У колонці «Беру» напишіть «так» біля варіантів, які підходять. Унизу — нова орієнтовна сума. Економія — діапазон «від–до», у підсумку береться середнє.'
w4['A2'].font = FM
w4['A3'] = 'Не варто економити на шамоті, жаростійкому розчині й базальтовому картоні: економія мізерна, а прогорілий мангал дорожчий.'
w4['A3'].font = FM
for c, h in enumerate(['№', 'Що зробити', 'Економія від, грн', 'Економія до, грн', 'Що втрачаємо', 'Беру'], 1):
    cell = w4.cell(5, c, h); cell.font = HEAD_FONT; cell.fill = HEAD_FILL; cell.alignment = Alignment(vertical='center', wrap_text=True)
r = 5; n4 = 0; f4 = 6
for cat, rows in SAVE:
    r += 1; w4.cell(r, 1, cat).font = FB_
    for c in range(1, 7): w4.cell(r, c).fill = GROUP_FILL
    for what, lo, hi, loss in rows:
        r += 1; n4 += 1
        for c, v in enumerate((n4, what, lo, hi, loss), 1):
            cell = w4.cell(r, c, v); cell.font = FI if c in (3, 4) else F; cell.alignment = WRAP if c in (2, 5) else TOP; cell.border = BOX
            if c in (3, 4): cell.number_format = '#,##0'
        bc = w4.cell(r, 6); bc.fill = INPUT_FILL; bc.font = F; bc.border = BOX
l4 = r
r += 2
rows_sum = [
  ('Кошторис зараз, грн', f"='Закупівля'!{tc.coordinate}"),
  ('Економія за вибраними, грн', f'=(SUMIF(F{f4}:F{l4},"так",C{f4}:C{l4})+SUMIF(F{f4}:F{l4},"так",D{f4}:D{l4}))/2'),
  ('Нова сума, грн', f'=C{r}-C{r + 1}'),
]
for i, (lab, frm) in enumerate(rows_sum):
    w4.cell(r + i, 2, lab).font = FB_ if i != 1 else F
    cc = w4.cell(r + i, 3, frm); cc.font = FB_ if i != 1 else F; cc.number_format = '#,##0'
for col, w in zip('ABCDEF', (5, 58, 14, 14, 48, 9)):
    w4.column_dimensions[col].width = w
w4.freeze_panes = 'A6'
w4.sheet_view.showGridLines = False
wb.calculation.fullCalcOnLoad = True  # no cached values from openpyxl; Excel computes on open
wb.save(os.environ.get('XLSX_OUT') or os.path.join(ROOT, 'spysok-materialiv.xlsx'))  # XLSX_OUT: when the file is open in Excel
print('xlsx ok,', n, 'items')
