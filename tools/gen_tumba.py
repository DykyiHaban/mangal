# Usage: python tools/gen_tumba.py  ->  kreslennia-tumba.html + kreslennia/tumba-karkas-*.svg
# Welder's drawing of the cabinet frame (part 3) for model v14.
# Units: mm. x from the left edge of the frame (next to the gabion by the stove), z from the rear edge, heights from the paving.
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from drafting import View, PAGE_CSS, HEAD

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
K = os.path.join(ROOT, 'kreslennia')
O = 1630  # model x of the frame's left edge

def L(x): return x - O

T = 40
FB, FT = 20, 730
POSTS = [(1630, 0), (1630, 560), (2172, 0), (2172, 560), (2560, 0), (2560, 560), (2560, 1060), (2100, 1060), (2100, 600)]
RING = [
  ('2', 1670, 2172, 0, 40), ('2a', 2212, 2560, 0, 40),
  ('3', 1630, 1670, 40, 560), ('3', 2172, 2212, 40, 560),
  ('4', 1670, 2172, 560, 600),
  ('3', 2560, 2600, 40, 560), ('5', 2560, 2600, 600, 1060),
  ('6', 2140, 2560, 1060, 1100), ('6', 2100, 2140, 640, 1060),
  ('6', 2140, 2560, 600, 640),
]
SINK = (2160, 2540, 660, 1040)

# ---------- plan ----------
p = View(-200, 1170, 0, 1250, pad=(90, 60, 70, 170), flip=False, k=1.7)
p.poly([(0, 0), (970, 0), (970, 1100), (470, 1100), (470, 600), (0, 600)], 'hid')
p.rect(-200, 0, 0, 600, 'hid'); p.text(-100, 300, 'габіон', 'note', 'middle')
p.rect(970, 0, 1170, 1100, 'hid')
p.rect(470, 1100, 970, 1250, 'hid'); p.text(720, 1165, 'габіон', 'note', 'middle')
for _, x0, x1, z0, z1 in RING: p.rect(L(x0), z0, L(x1), z1, 'ol')
for x, z in POSTS: p.rect(L(x), z, L(x) + T, z + T, 'fill')
p.rect(L(1685), 110, L(2157), 556, 'hid'); p.text(L(1921), 330, 'холодильник', 'note', 'middle')
p.rect(L(SINK[0]), SINK[2], L(SINK[1]), SINK[3], 'hid'); p.text(L(2350), 860, 'умивальник', 'note', 'middle')
p.text(300, 860, 'дверцята →', 'note', 'end')
p.dimH(0, 970, -30, ext_from=0)
p.dimH(0, 40, 1150, ext_from=600); p.dimH(40, 542, 1150, '502'); p.dimH(542, 582, 1150, '40')
p.dimH(582, 930, 1310, '348', ext_from=40); p.dimH(930, 970, 1310, '40')
p.dimH(470, 970, 1380, '500', ext_from=1100)
p.dimV(0, 600, -240, '600', ext_from=-200); p.dimV(0, 1100, 1220, '1100', ext_from=970, side='right')
p.dimV(640, 1060, 420, '420', ext_from=470, side='left')
p.dimH(L(2100), L(SINK[0]), 1000, '60'); p.dimV(SINK[3], 1100, L(2350), '60', side='right')
p.dimH(L(SINK[0]), L(SINK[1]), 640, '380')
plan_svg = p.svg('План каркаса')

# ---------- front view (looking at the fridge opening and the return end) ----------
f = View(0, 970, 0, 730, pad=(130, 130, 60, 110), k=1.5)
f.line(-60, 0, 1030, 0, 'ol')
# the return (x 470..970) stands in front, so the partition post and the right end of the fridge-bay rails are hidden
for x in (1630, 2100, 2560):
    f.rect(L(x), FB, L(x) + T, FT); f.rect(L(x) + 8, 0, L(x) + 32, FB, 'ol thin')
f.rect(L(2172), FB, L(2172) + T, FT, 'hid')
for y0 in (FB, FT - T):
    f.rect(40, y0, 470, y0 + T); f.rect(470, y0, 542, y0 + T, 'hid'); f.rect(L(2140), y0, L(2560), y0 + T)
f.rect(40, 600, 470, 602, 'ol thin')
f.rect(L(1685), 62, L(2157), 554, 'hid'); f.text(L(1921), 300, 'холодильник', 'note', 'middle')
f.rect(L(2140), 60, L(2560), FT - T, 'brick')
f.text(L(2350), 380, 'обшивка зсередини', 'note', 'middle')
f.dimV(0, 730, -40, '730', ext_from=0); f.dimV(0, 20, -95, '20', ext_from=0); f.dimV(20, 60, -95, '40')
f.dimV(FT - T, FT, -95, '40')
f.dimV(62, 600, 560, '538', ext_from=542, side='right')
f.dimH(0, 582, -40, '582', ext_from=0); f.dimH(470, 970, -40, '500', ext_from=0)
f.pos(1, 20, 300, -70, 400); f.pos(2, 300, 710, 300, 800); f.pos(6, 720, 40, 720, -70) if False else f.pos(6, 720, 710, 720, 800)
front_svg = f.svg('Вид спереду')

# ---------- left view: free-zone side (door) ----------
s = View(0, 1100, 0, 730, pad=(130, 230, 60, 110), k=1.5)
s.line(-60, 0, 1160, 0, 'ol')
for z in (0, 560):
    s.rect(z, FB, z + T, FT); s.rect(z + 8, 0, z + 32, FB, 'ol thin')
for z in (600, 1060):
    s.rect(z, FB, z + T, FT); s.rect(z + 8, 0, z + 32, FB, 'ol thin')
for y0 in (FB, FT - T):
    s.rect(40, y0, 560, y0 + T); s.rect(640, y0, 1060, y0 + T)
s.rect(40, 560, 560, 600)
s.rect(630, 50, 1070, 700, 'hid'); s.text(850, 380, 'дверцята 440 × 650', 'note', 'middle')
s.rect(650, 300, 662, 420, 'ol thin')
for y in (150, 600): s.rect(1062, y - 25, 1074, y + 25, 'ol thin')
s.dimH(0, 600, -40, ext_from=0); s.dimH(600, 1100, -40, '500', ext_from=0)
s.dimH(640, 1060, 650, '420 отвір')
s.dimV(60, 690, 1140, '630 отвір', ext_from=1100, side='right')
s.dimV(0, 560, -40, '560', ext_from=0); s.dimV(560, 600, -40, '40')
s.text(300, 640, 'бік відсіку холодильника — до габіона', 'note', 'middle')
s.pos(4, 300, 580, 300, 450)
side_svg = s.svg('Вид зліва')

# ---------- right view: next to the gabion by the post ----------
r = View(0, 1100, 0, 730, pad=(130, 120, 60, 110), k=1.5)
r.line(-60, 0, 1160, 0, 'ol')
for z in (0, 560, 1060):
    r.rect(z, FB, z + T, FT); r.rect(z + 8, 0, z + 32, FB, 'ol thin')
for y0 in (FB, FT - T):
    r.rect(40, y0, 560, y0 + T); r.rect(600, y0, 1060, y0 + T)
r.dimH(0, 1100, -40, ext_from=0); r.dimH(40, 560, 650, '520'); r.dimH(600, 1060, 650, '460')
r.text(550, 380, 'обшивка зсередини, зовні габіон', 'note', 'middle')
r.pos(3, 300, 40, 300, 160); r.pos(5, 830, 40, 830, 160)
right_svg = r.svg('Вид справа')

# ---------- foot detail ----------
ft = View(-40, 80, -40, 80, pad=(90, 160, 40, 60), k=1.0)
ft.rect(0, 24, 40, 80, 'ol'); ft.rect(0, 20, 40, 24, 'fill'); ft.rect(12, 12, 28, 20, 'fill')
ft.rect(17, -20, 23, 20, 'ol thin'); ft.rect(0, -30, 40, -20, 'fill')
ft.text(50, 60, 'стійка 40×40×2', 'note'); ft.text(50, 22, 'пластина 40×40×4', 'note')
ft.text(50, 8, 'гайка M10 приварена', 'note'); ft.text(50, -26, 'ніжка M10, хід ±10', 'note')
ft.dimV(-30, 20, -20, '20…40', side='left')
foot_svg = ft.svg('Ніжка')

BOM = [
 (1, 'Стійка', 'труба 40×40×2', '710', 9, 'від 20 до 730; знизу пластина з гайкою під ніжку'),
 (2, 'Обв\'язка задня і перед відсіку', 'труба 40×40×2', '502', 4, 'зад відсіку холодильника і перед над/під ним; два рівні'),
 ('2a', 'Обв\'язка задня шафи', 'труба 40×40×2', '348', 2, 'два рівні'),
 (3, 'Обв\'язка бокова', 'труба 40×40×2', '520', 6, 'лівий бік, перегородка, правий бік; два рівні'),
 (4, 'Напрямна полиці', 'труба 40×40×2', '520', 2, 'на висоті 560–600, лівий бік і перегородка'),
 (5, 'Обв\'язка правого боку повернення', 'труба 40×40×2', '460', 2, 'два рівні'),
 (6, 'Обв\'язка повернення', 'труба 40×40×2', '420', 6, 'перед, бік з дверцятами, внутрішня зв\'язка; два рівні'),
 (7, 'Пластина під ніжку', 'лист 4 мм', '40×40', 9, 'гайка M10 приварена'),
 (8, 'Ніжка регульована', 'M10, з п\'ятою Ø40', '—', 9, ''),
 (9, 'Обшивка задня', 'лист 1,5 мм', '970×710', 1, 'зовні, на всю довжину'),
 (10, 'Перегородка', 'лист 1,5 мм', '520×630', 1, 'між відсіком і шафою'),
 (11, 'Обшивка правого боку', 'лист 1,5 мм', '1020×630', 1, 'зсередини, зовні габіон'),
 (12, 'Обшивка переду повернення', 'лист 1,5 мм', '420×630', 1, 'зсередини, зовні габіон'),
 (13, 'Дно відсіку холодильника', 'лист 1,5 мм', '502×560', 1, 'на нижній обв\'язці'),
 (14, 'Дно шафи', 'лист 1,5 мм', '348×560 + 420×460', 2, ''),
 (15, 'Полиця над холодильником', 'лист 1,5 мм', '502×560', 1, 'на напрямних поз. 4'),
 (16, 'Дверцята', 'лист 1,5 мм', '470×680', 1, 'заготовка з відгином 15 по периметру → 440×650'),
 (17, 'Петлі, ручка, магнітна защіпка', '—', '—', '2+1+1', 'петлі на передній стійці'),
]
tube_len = 9 * 710 + 4 * 502 + 2 * 348 + 8 * 520 + 2 * 460 + 6 * 420
rows = ''.join(f'<tr><td class="n">{n}</td><td>{a}</td><td>{b}</td><td class="m">{c}</td><td class="m">{d}</td><td class="c">{e}</td></tr>' for n, a, b, c, d, e in BOM)

html = HEAD.format(title='Каркас тумби', css=PAGE_CSS) + f'''
<div class="wrap">
  <header class="tb">
    <div>
      <h1>Каркас тумби</h1>
      <p>Частина 3 зони мангала: відсік холодильника і шафа під умивальником з поверненням. Зверху лягає цільна кришка 70 мм з плиткою, з боків — габіони.</p>
    </div>
    <dl class="meta">
      <dt>Модель</dt><dd>v14 · 19.11.2026</dd>
      <dt>Розміри</dt><dd>мм, висоти від плитки</dd>
      <dt>Труба 40×40×2</dt><dd>{tube_len / 1000:.1f} м</dd>
    </dl>
  </header>
  <div class="grid">
    <section class="v wide"><h2>План каркаса <span>зад угорі; стійки залиті, пунктиром габіони, холодильник і умивальник</span></h2><div class="sc">{plan_svg}</div></section>
    <section class="v"><h2>Вид спереду <span>відсік холодильника і торець повернення</span></h2><div class="sc">{front_svg}</div></section>
    <section class="v"><h2>Вид зліва <span>з боку вільної зони, зад ліворуч</span></h2><div class="sc">{side_svg}</div></section>
    <section class="v"><h2>Вид справа <span>з боку габіона біля стовпа, зад ліворуч</span></h2><div class="sc">{right_svg}</div></section>
    <section class="v"><h2>Ніжка <span>під кожною стійкою</span></h2><div class="sc">{foot_svg}</div></section>
    <section class="notes wide" style="grid-column:1/-1">
      <h2>Вимоги</h2>
      <ol>
        <li>Обв'язки на двох рівнях: низ 20–60, верх 690–730. Верх каркаса рівно на 730 — на нього лягає кришка, верх кришки 800.</li>
        <li>Просвіт під холодильник між стійками — 502, не менше: холодильник 472 завширшки, по 15 мм на провітрювання.</li>
        <li>Умивальник 380 × 380 стоїть за 60 мм від зовнішніх країв повернення, між обв'язками. Під ним вільно: внутрішня зв'язка поз. 6 іде на 600–640, за чашею.</li>
        <li>Обшивку біля габіонів ставити зсередини, щоб каркас прилягав до габіонів впритул.</li>
        <li>Каркас кріпиться до габіонів болтами M8 через стійки: зліва до габіона біля печі, справа і спереду до габіонів повернення. Розмітити по місцю.</li>
        <li>Кришка кріпиться 6 болтами M8 знизу через верхню обв'язку в гайки, приварені до решітки кришки. Розмітити разом з кришкою.</li>
        <li>Перед зварюванням зібрати на прихватках і перевірити діагоналі. Після — ґрунт і вулична фарба по металу.</li>
      </ol>
    </section>
  </div>
  <section class="bom">
    <h2>Специфікація</h2>
    <div class="tw"><table>
      <thead><tr><th>Поз.</th><th>Деталь</th><th>Матеріал</th><th>Розмір</th><th>Шт</th><th>Примітка</th></tr></thead>
      <tbody>{rows}</tbody>
    </table></div>
    <p class="total">Труба 40×40×2: {tube_len / 1000:.1f} м (≈ {tube_len / 1000 * 2.31:.0f} кг) · лист 1,5 мм ≈ 3,4 м² (≈ 40 кг) · під різ +10%</p>
  </section>
</div>
'''
open(os.path.join(ROOT, 'kreslennia-tumba.html'), 'w', encoding='utf-8').write(html)
p.save(os.path.join(K, 'tumba-karkas-1-plan.svg'), 'Каркас тумби · план')
f.save(os.path.join(K, 'tumba-karkas-2-vyd-speredu.svg'), 'Каркас тумби · вид спереду')
s.save(os.path.join(K, 'tumba-karkas-3-vyd-zliva.svg'), 'Каркас тумби · вид зліва, з боку дверцят')
r.save(os.path.join(K, 'tumba-karkas-4-vyd-sprava.svg'), 'Каркас тумби · вид справа')
ft.save(os.path.join(K, 'tumba-karkas-5-nizhka.svg'), 'Каркас тумби · ніжка')
print('ok, tube', tube_len)
