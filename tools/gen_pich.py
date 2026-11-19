# Usage: python tools/gen_pich.py  ->  kreslennia-pich.html + kreslennia/pich-*.svg
# Generates the welder's drawing for the kazan stove frame (v13 of the grill-zone model).
# Units: mm. Absolute heights from the floor (bottom of the legs).
import sys



import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafting import View

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------- key dimensions ----------
W, D = 500, 600          # footprint
LEG = 374                # legs and rings: tube 40x40x2
RINGS = [(100, 140), (334, 374)]
SHEET = 377              # top of 3 mm base sheet
TOP = 796                # top of corner angles and band
BAND = TOP - 40
POSTS = [(65, 105), (395, 435)]
FR = (105, 395, 420, 700)        # door frame outer
OPEN = (130, 370, 445, 675)      # brick opening 240 x 230
LEAF = (110, 390, 425, 695)      # 280 x 270
FLUE_Y = 700

# ---------- front view (door removed) ----------
f = View(0, W, 0, 800, pad=(110, 90, 70, 70))
f.rect(4, SHEET, 496, 750, 'brick'); f.text(250, 735, 'кладка — не входить у зварювання', 'note', 'middle')
for x in (0, W - 40): f.rect(x, 0, x + 40, LEG)
for y0, y1 in RINGS: f.rect(40, y0, W - 40, y1)
f.rect(0, 140, W, 143, 'ol thin'); f.rect(0, LEG, W, SHEET, 'ol thin')
for x in (0, W - 40): f.rect(x, SHEET, x + 40, TOP)
f.rect(0, BAND, W, TOP)
for a, b in POSTS: f.rect(a, 334, b, BAND)
f.rect(FR[0], FR[2], FR[1], FR[3]); f.rect(OPEN[0] + 3, OPEN[2] + 3, OPEN[1] - 3, OPEN[3] - 3, 'ol thin')
f.line(250, 400, 250, 720, 'cl'); f.line(80, 560, 420, 560, 'cl')
for y in (470, 650): f.rect(FR[0] - 9, y - 25, FR[0] - 1, y + 25, 'ol thin')
f.rect(FR[1] + 2, 548, FR[1] + 12, 572, 'ol thin')
# dims
f.dimH(0, W, -32, ext_from=0)
f.dimH(0, POSTS[0][0], 830, ext_from=TOP)
f.dimH(POSTS[0][0], POSTS[0][1], 830); f.dimH(POSTS[0][1], POSTS[1][0], 830, '290'); f.dimH(POSTS[1][0], POSTS[1][1], 830)
f.dimH(OPEN[0], OPEN[1], 600, '240 отвір')
f.dimV(0, LEG, -30, ext_from=0); f.dimV(LEG, TOP, -30, '422', ext_from=0)
f.dimV(0, TOP, -62, '796', ext_from=0)
f.dimV(FR[2], FR[3], 535, '280', ext_from=FR[1], side='right')
f.dimV(0, FR[2], 560, '420', ext_from=400, side='right')
f.dimV(OPEN[2], OPEN[3], 455, '230', ext_from=OPEN[1], side='right')
f.dimV(100, 140, 470, None, ext_from=W, side='right')
f.dimV(0, 100, 470, None, side='right')
f.dimV(BAND, TOP, 530, '40', ext_from=W, side='right')
f.pos(1, 20, 60, -20, 210); f.pos(2, 250, 120, 300, 210); f.pos(5, 300, 375.5, 330, 300)
f.pos(4, 120, 141.5, 160, 230); f.pos(6, 480, 600, 530, 640) if False else f.pos(6, 480, 620, 540, 700)
f.pos(7, 300, 776, 330, 845) if False else None
f.pos(9, 85, 300, 30, 310); f.pos(10, 380, 690, 430, 760); f.pos(13, FR[0] - 5, 650, 30, 640)
f.pos(14, FR[1] + 7, 560, 455, 520) if False else None
front_svg = f.svg('Вид спереду, дверцята зняті')

# ---------- left side view (rear on the left) ----------
s = View(-110, D, 0, 810, pad=(70, 80, 40, 70))
for z in (0, D - 40): s.rect(z, 0, z + 40, LEG)
for y0, y1 in RINGS: s.rect(40, y0, D - 40, y1)
s.rect(0, 140, D, 143, 'ol thin'); s.rect(0, LEG, D, SHEET, 'ol thin')
s.rect(0, SHEET, 3, TOP, 'ol')
for z in (0, D - 40): s.rect(z, SHEET, z + 40, TOP)
s.rect(0, BAND, D, TOP)
s.rect(D, 334, D + 4, BAND, 'ol')
s.rect(D - 28, FR[2], D, FR[3], 'hid')
s.rect(7, 795, D - 7, 800, 'ol thin'); s.text(300, 806, 'плита поз.15 лежить вільно', 'note', 'middle')
for z in (20, D - 20):
    for y in (120, 300): s.circle(z, y, 5.5)
s.rect(-6, FLUE_Y - 80, 0, FLUE_Y + 80, 'ol'); s.rect(-100, FLUE_Y - 55, -6, FLUE_Y + 55, 'ol thin')
s.text(-100, FLUE_Y + 72, 'труба Ø110', 'note')
s.line(-110, FLUE_Y, 20, FLUE_Y, 'cl')
s.dimH(0, D, -32, ext_from=0)
s.dimV(0, 120, D + 40, '120', ext_from=D, side='right'); s.dimV(120, 300, D + 40, '180', side='right')
s.dimV(0, FLUE_Y, -60, '700', ext_from=-6)
s.dimH(0, 20, 330, None); s.dimH(D - 20, D, 330, None)
s.pos(8, 1.5, 560, 60, 520); s.pos(3, 300, 120, 300, 210); s.pos(16, -3, FLUE_Y + 60, 40, 760)
s.pos(7, 300, 776, 360, 700); s.pos(9, D + 2, 600, D + 50, 640)
s.text(300, 70, 'Ø11 наскрізь, 8 отворів', 'note', 'middle')
side_svg = s.svg('Вид зліва')

# ---------- rear wall pos. 8, seen from the front ----------
RH = TOP - SHEET   # 419
r = View(0, W, 0, RH, pad=(70, 70, 40, 60))
r.rect(0, 0, W, RH)
fy = FLUE_Y - SHEET   # 323
r.circle(250, fy, 57.5); r.circle(250, fy, 80, 'hid')
for dx in (-48, 48):
    for dy in (-48, 48): r.circle(250 + dx, fy + dy, 4.5)
r.line(150, fy, 350, fy, 'cl'); r.line(250, fy - 100, 250, fy + 100, 'cl')
jp = (410, 500, 690 - SHEET, 790 - SHEET)
r.rect(jp[0], jp[2], jp[1], jp[3], 'hid')
for x in (430, 480):
    for y in (715 - SHEET, 765 - SHEET): r.circle(x, y, 4.5)
r.dimH(0, W, -30, ext_from=0); r.dimH(0, 250, fy - 110, '250', ext_from=fy)
r.dimV(0, RH, -30, ext_from=0); r.dimV(0, fy, 160, '323', side='left')
r.dimH(250 - 48, 250 + 48, fy + 120, '96'); r.dimV(fy - 48, fy + 48, 360, '96', side='right')
r.dimH(430, 480, RH + 18, '50', ext_from=jp[3]); r.dimH(0, 430, RH + 40, '430', ext_from=RH)
r.dimV(715 - SHEET, 765 - SHEET, W + 26, '50', ext_from=480, side='right'); r.dimV(0, 715 - SHEET, W + 26, '338', side='right')
r.text(250, fy + 2 - 100, 'Ø115', 'dt', 'middle') if False else r.text(318, fy + 64, 'Ø115, 4× Ø9', 'note')
rear_svg = r.svg('Задня стінка')

# ---------- plate pos. 15, top view (rear edge at the top) ----------
PW, PD = 486, 586
pl = View(0, PW, 0, PD, pad=(70, 70, 40, 50), flip=False)
pl.rect(0, 0, PW, PD); hz = 270 - 7
pl.add(f'<circle class="ol" cx="{pl.X(243):.1f}" cy="{pl.Y(hz):.1f}" r="150"/>')
pl.line(60, hz, 426, hz, 'cl'); pl.line(243, hz - 180, 243, hz + 180, 'cl')
pl.dimH(0, PW, -26, ext_from=0); pl.dimV(0, PD, -30, ext_from=0)
pl.dimH(0, 243, hz + 200, '243'); pl.dimV(0, hz, PW + 30, '263', ext_from=243, side='right')
pl.add(f'<text class="dt" x="{pl.X(243):.1f}" y="{pl.Y(hz) + 4:.1f}" text-anchor="middle">Ø300</text>')
pl.text(243, -8, 'задній край', 'note', 'middle'); pl.text(243, PD + 22, 'передній край', 'note', 'middle')
plate_svg = pl.svg('Плита')

# ---------- door pos. 11-14 ----------
dv = View(0, 280, 0, 270, pad=(170, 200, 60, 80))
dv.rect(0, 0, 280, 270)
dv.rect(20, 20, 260, 250, 'hid')
for x in (40, 240):
    for y in (40, 230): dv.circle(x, y, 3.5)
for y in (45, 225): dv.rect(-14, y - 25, -2, y + 25, 'ol thin'); dv.circle(-8, y, 5, 'ol thin')
dv.rect(255, 123, 265, 147, 'ol thin'); dv.rect(265, 130, 300, 140, 'ol thin')
dv.dimH(0, 280, -30, ext_from=0); dv.dimV(0, 270, -40, ext_from=0)
dv.dimV(0, 45, 300 + 20, '45', ext_from=0, side='right'); dv.dimV(45, 225, 320, '180', side='right')
dv.dimH(20, 260, 285, '240 екран', ext_from=250)
dv.text(140, 135, 'вид з боку вогню: екран 2 мм', 'note', 'middle')
dv.text(140, 118, 'на 4 дистанціях 15 мм', 'note', 'middle')
dv.pos(11, 140, 6, 140, -45) if False else None
door_svg = dv.svg('Дверцята')

BOM = [
 (1, 'Ніжка', 'труба 40×40×2', '374', 4, 'отвори Ø11 на висоті 120 і 300, наскрізь уздовж ширини'),
 (2, 'Обв\'язка спереду і ззаду', 'труба 40×40×2', '420', 4, 'два рівні: низ на 100, верх на 334'),
 (3, 'Обв\'язка бокова', 'труба 40×40×2', '520', 4, 'між ніжками'),
 (4, 'Полиця під дрова', 'лист 3 мм', '500×600', 1, 'вирізи 40×40 по кутах, на нижній обв\'язці'),
 (5, 'Дно під кладку', 'лист 3 мм', '500×600', 1, 'на верхній обв\'язці, верх на 377'),
 (6, 'Кутник кутовий', 'кутник 40×40×4', '419', 4, 'на дно, полиці назовні, верх на 796'),
 (7, 'Пояс верхній', 'смуга 40×4', '500 / 592', '1 + 2', 'спереду 500, боки 592; верх врівень з кутниками'),
 (8, 'Задня стінка', 'лист 3 мм', '500×419', 1, 'глуха; отвір Ø115 і 4×Ø9 під фланець, 4×Ø9 під накладку'),
 (9, 'Стійка дверцят', 'смуга 40×4', '422', 2, 'від низу передньої верхньої обв\'язки (334) до поясу (756)'),
 (10, 'Рамка дверцят', 'кутник 25×25×3', '290 / 280', '2 + 2', 'різ 45°, одна полиця в отвір, друга на фасад'),
 (11, 'Полотно дверцят', 'лист 3 мм', '280×270', 1, ''),
 (12, 'Екран дверцят', 'лист 2 мм', '240×230', 1, '4 дистанції Ø16×15, болти M6'),
 (13, 'Петля', 'пруток Ø10 + трубка', '50', 2, 'на лівій стійці, осі на 470 і 650'),
 (14, 'Засувка з ручкою', 'готова або смуга', '—', 1, 'на правій стійці, на 560'),
 (15, 'Плита', 'лист 5 мм', '486×586', 1, 'отвір Ø300; НЕ приварювати'),
 (16, 'Фланець труби', 'лист 5 мм', 'Ø160', 1, 'вварити трубу Ø110; 4×Ø9 по квадрату 96'),
 (17, 'Перемичка над дверцятами', 'кутник 50×50×5', '280', 1, 'вільно в кладці, не приварюється'),
 (18, 'Накладка казан–тумба', 'лист 5 мм', '90×100', 1, 'на задній стінці справа вгорі, 4×Ø9'),
]
rows = ''.join(f'<tr><td class="n">{n}</td><td>{a}</td><td>{b}</td><td class="m">{c}</td><td class="m">{d}</td><td class="c">{e}</td></tr>' for n, a, b, c, d, e in BOM)

html = f'''<meta charset="utf-8">
<title>Каркас печі під казан</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
/* Layout: a drafting sheet — title block, then views in a two-column grid, then the parts list */
:root {{
  --paper: #f6f7f5; --sheet: #ffffff; --ink: #1c2226; --muted: #5d676d; --line: #cfd6d3;
  --dim: #c4521c; --brick: #efe3d0; --hid: #7b868c;
  --font-ui: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --paper: #14181a; --sheet: #1b2023; --ink: #e4e9ea; --muted: #9aa4a9; --line: #313a3e;
  --dim: #f08a52; --brick: #3a3128; --hid: #8e999e; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --paper: #14181a; --sheet: #1b2023; --ink: #e4e9ea; --muted: #9aa4a9; --line: #313a3e;
  --dim: #f08a52; --brick: #3a3128; --hid: #8e999e; color-scheme: dark; }}
body {{ background: var(--paper); color: var(--ink); font-family: var(--font-ui); font-size: 15px; line-height: 1.5;
  padding-block: 24px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }}
.wrap {{ max-width: 1180px; margin: 0 auto; display: grid; gap: 20px; }}
.tb {{ display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 8px 24px; align-items: end;
  border: 1.5px solid var(--ink); background: var(--sheet); padding: 14px 18px; }}
h1 {{ margin: 0; font-size: 24px; font-weight: 600; text-wrap: balance; }}
.tb p {{ margin: 2px 0 0; color: var(--muted); }}
.meta {{ display: grid; grid-template-columns: auto auto; gap: 2px 14px; font-family: var(--font-mono); font-size: 13px; }}
.meta dt {{ color: var(--muted); }} .meta dd {{ margin: 0; }}
.grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }}
.v {{ background: var(--sheet); border: 1px solid var(--line); padding: 12px 14px 8px; min-width: 0; display: grid; gap: 4px; align-content: start; }}
.v h2 {{ margin: 0; font-size: 15px; font-weight: 600; }}
.v h2 span {{ font-weight: 400; color: var(--muted); }}
.sc {{ overflow-x: auto; }}
.sc svg {{ display: block; width: 100%; min-width: 460px; height: auto; }}
svg .ol {{ fill: none; stroke: var(--ink); stroke-width: 1.4; vector-effect: non-scaling-stroke; }}
svg .thin {{ stroke-width: .8; }}
svg .hid {{ fill: none; stroke: var(--hid); stroke-width: .9; stroke-dasharray: 6 4; vector-effect: non-scaling-stroke; }}
svg .cl {{ stroke: var(--hid); stroke-width: .7; stroke-dasharray: 14 3 2 3; vector-effect: non-scaling-stroke; }}
svg .brick {{ fill: var(--brick); stroke: none; }}
svg .dim, svg .ext {{ stroke: var(--dim); stroke-width: .8; vector-effect: non-scaling-stroke; }}
svg .ext {{ stroke-width: .5; }}
svg .lead {{ stroke: var(--muted); stroke-width: .7; vector-effect: non-scaling-stroke; }}
svg .dt {{ fill: var(--dim); font: 500 15px var(--font-mono); }}
svg .note {{ fill: var(--muted); font: 14px var(--font-ui); }}
svg .lt {{ fill: var(--ink); font: 12px var(--font-ui); }}
svg .bub {{ fill: var(--sheet); stroke: var(--ink); stroke-width: 1; vector-effect: non-scaling-stroke; }}
svg .bt {{ fill: var(--ink); font: 600 13px var(--font-mono); }}
.notes {{ background: var(--sheet); border: 1px solid var(--line); padding: 14px 18px; }}
.notes h2, .bom h2 {{ margin: 0 0 8px; font-size: 15px; font-weight: 600; }}
.notes ol {{ margin: 0; padding-left: 20px; display: grid; gap: 4px; max-width: 80ch; }}
.bom {{ background: var(--sheet); border: 1px solid var(--line); padding: 14px 18px; min-width: 0; }}
.tw {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; min-width: 720px; font-size: 14px; }}
th, td {{ text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }}
th {{ font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: .04em; }}
td.n {{ font-family: var(--font-mono); font-weight: 500; width: 2.5em; }}
td.m {{ font-family: var(--font-mono); font-variant-numeric: tabular-nums; white-space: nowrap; }}
td.c {{ color: var(--muted); }}
.total {{ margin: 10px 0 0; font-family: var(--font-mono); font-size: 13px; color: var(--muted); }}
@media (max-width: 820px) {{ .grid {{ grid-template-columns: minmax(0, 1fr); }} .tb {{ grid-template-columns: minmax(0, 1fr); }} }}
</style>

<div class="wrap">
  <header class="tb">
    <div>
      <h1>Каркас печі під казан</h1>
      <p>Сталева частина модуля 500 × 600 зони мангала. Кладка з шамоту і облицювання ставиться після зварювання.</p>
    </div>
    <dl class="meta">
      <dt>Модель</dt><dd>v13 · 19.11.2026</dd>
      <dt>Розміри</dt><dd>мм, висоти від підлоги</dd>
      <dt>Маса сталі</dt><dd>≈ 52 кг</dd>
    </dl>
  </header>

  <div class="grid">
    <section class="v"><h2>Вид спереду <span>дверцята зняті</span></h2><div class="sc">{front_svg}</div></section>
    <section class="v"><h2>Вид зліва <span>зад ліворуч, перед праворуч</span></h2><div class="sc">{side_svg}</div></section>
    <section class="v"><h2>Поз. 8 · Задня стінка <span>вид спереду, лівий край з боку мангала</span></h2><div class="sc">{rear_svg}</div></section>
    <section class="v"><h2>Поз. 15 · Плита <span>вид згори, не приварюється</span></h2><div class="sc">{plate_svg}</div></section>
    <section class="v"><h2>Поз. 11–14 · Дверцята <span>вид спереду</span></h2><div class="sc">{door_svg}</div></section>
    <section class="notes">
      <h2>Вимоги до зварювання</h2>
      <ol>
        <li>Внутрішній просвіт під кладку між кутниками і поясом 492 × 593. Перед зварюванням перевірити по цеглі: шамот 230×114×65 на ребро, 2 шви по 2–3 мм.</li>
        <li>Верх кутників (поз. 6) і поясу (поз. 7) врівень, на 796. Це рівно на 5 мм вище за кладку: плита (поз. 15) лягає всередину поясу на шнур.</li>
        <li>Плиту (поз. 15) не приварювати, вона має вільно розширюватись. Зазор до поясу по 3 мм з кожного боку.</li>
        <li>Задню стінку (поз. 8) обварити по периметру до кутників і дна суцільним швом.</li>
        <li>Стійки (поз. 9) приварити внапуск до передньої верхньої обв'язки і встик до поясу. Рамку (поз. 10) вварити між стійками, полицею в отвір.</li>
        <li>Отвори Ø11 у ніжках (поз. 1) — під болти M10, якими модуль кріпиться до мангала зліва і до тумби справа. Розмітити по сусідніх модулях.</li>
        <li>Видимі шви спереду зачистити. Після зварювання — фарба термостійка до 600 °C.</li>
      </ol>
    </section>
  </div>

  <section class="bom">
    <h2>Специфікація</h2>
    <div class="tw"><table>
      <thead><tr><th>Поз.</th><th>Деталь</th><th>Матеріал</th><th>Розмір</th><th>Шт</th><th>Примітка</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="total">Разом: труба 40×40×2 ≈ 5,3 м · кутник 40×40×4 ≈ 1,7 м · смуга 40×4 ≈ 2,5 м · кутник 25×25×3 ≈ 1,2 м · лист 3 мм ≈ 0,9 м² · лист 5 мм ≈ 0,35 м²</p>
  </section>
</div>
'''
open(os.path.join(ROOT, 'kreslennia-pich.html'), 'w', encoding='utf-8').write(html)
K = os.path.join(ROOT, 'kreslennia')
f.save(os.path.join(K, 'pich-1-vyd-speredu.svg'), 'Піч під казан · вид спереду, дверцята зняті')
s.save(os.path.join(K, 'pich-2-vyd-zliva.svg'), 'Піч під казан · вид зліва')
r.save(os.path.join(K, 'pich-3-zadnia-stinka.svg'), 'Піч під казан · поз. 8 задня стінка')
pl.save(os.path.join(K, 'pich-4-plyta.svg'), 'Піч під казан · поз. 15 плита')
dv.save(os.path.join(K, 'pich-5-dvertsiata.svg'), 'Піч під казан · дверцята')
print('ok', len(html))
