# Usage: python tools/vyrobnytstvo.py
# Production pack in vyrobnytstvo/ from the 3D model export (vyrobnytstvo/detali.json, made by window.__mangal.cutParts()):
#   rozkriy.html                 cut list: every tube/bar piece (length x qty, where) + cutting maps of 6 m sticks
#   zamovlennya.xlsx             order workbook: what to buy (sticks from the nesting + all other materials), cut list, maps
#   kreslennia-druk.html / .pdf  printable pack, A4 landscape: drawings + cut list + order
#   model-3d.html                copy of the interactive 3D model (opens in any browser, needs internet)
# The nesting is first-fit decreasing on 6000 mm sticks with a 3 mm saw kerf.
import html
import json
import os
import subprocess
import sys
from collections import Counter, defaultdict
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'vyrobnytstvo')
STICK, KERF = 6000, 3
DRAWINGS = [  # current drawings made by tools/gen_kompleks.py, in print order
    ('kompleks-1-plan.svg', 'План комплексу'),
    ('kompleks-2-fasad.svg', 'Фасад'),
    ('kompleks-3-rozriz-AA.svg', 'Розріз А–А через умивальник'),
    ('karkas-1-speredu.svg', 'Спільний каркас мангала і печі · спереду'),
    ('karkas-2-zgory.svg', 'Спільний каркас · згори'),
    ('karkas-3-styk.svg', 'Спільний каркас · розріз по стику'),
    ('pich-3-zadnia-stinka.svg', 'Піч · задня стінка'),
    ('pich-4-plyta.svg', 'Піч · плита'),
    ('pich-5-dvertsiata.svg', 'Піч · дверцята'),
    ('mangal-1-vyd-speredu.svg', 'Мангал · вид спереду'),
    ('mangal-2-rozriz.svg', 'Мангал · розріз поперек'),
    ('mangal-4-vytyazhka.svg', 'Витяжка над мангалом · розріз збоку'),
    ('dakh-1-rozriz.svg', 'Дах · розріз збоку'),
    ('dakh-2-speredu.svg', 'Дах · вид спереду'),
    ('drovnyk-stinka.svg', 'Дровник-стінка · вид збоку і ферма з торця'),
    ('mangal-3-tumba-zliva.svg', 'Тумба зліва на інвентар · спереду і розріз'),
    ('tumba-1-stilnytsi.svg', 'Стільниці · вид згори'),
    ('tumba-2-shary-stilnytsi.svg', 'Стільниці · шари'),
    ('tumba-3-kamyana-panel.svg', 'Кам’яна панель · типово'),
]
SEC_ORDER = ['40×40×2', '40×40×3', '60×40×3', '60×40×2', '100×100×3', '40×20×2', '20×20×1,5', 'смуга 40×4']
SEC_NAME = {s: (s if s.startswith('смуга') else 'Труба профільна ' + s) for s in SEC_ORDER}

data = json.load(open(os.path.join(OUT, 'detali.json'), encoding='utf-8'))
parts = data['parts']
version = data.get('model', '')

# ---- cut list: pieces grouped by section and length (rounded to 5 mm) ----
groups = defaultdict(Counter)        # sec -> Counter((L, zone))
for p in parts:
    L = int(round(p['L'] / 5.0) * 5)
    groups[p['sec']][(L, p['zone'])] += 1
secs = [s for s in SEC_ORDER if s in groups] + sorted(s for s in groups if s not in SEC_ORDER)


def nest(lengths):
    sticks = []
    for L in sorted(lengths, reverse=True):
        if L > STICK:
            sticks.append({'cuts': [L], 'free': 0, 'long': True}); continue
        for st in sticks:
            if not st.get('long') and st['free'] >= L + (KERF if st['cuts'] else 0):
                st['free'] -= L + (KERF if st['cuts'] else 0); st['cuts'].append(L); break
        else:
            sticks.append({'cuts': [L], 'free': STICK - L})
    return sticks


plan = {}
for s in secs:
    lengths = [L for (L, z), n in groups[s].items() for _ in range(n)]
    st = nest(lengths)
    used = sum(lengths)
    plan[s] = {'sticks': st, 'n': len(st), 'used': used, 'waste': len(st) * STICK - used}

# ---- other materials from the purchase sheet (everything except profile tube and flat bar 40x4) ----
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

other = []
try:
    ws0 = load_workbook(os.path.join(ROOT, 'spysok-materialiv.xlsx'))['Закупівля']
    cat = None
    for row in ws0.iter_rows(min_row=6, values_only=True):
        a, b, c, d, e, f = (row + (None,) * 6)[:6]
        if a and not b and isinstance(a, str):
            cat = a; continue
        if not b or not isinstance(c, (int, float)):
            continue
        if str(b).startswith('Труба профільна') or str(b).startswith('Смуга 40×4'):
            continue
        other.append((cat, b, c, d, e, f))
except Exception as ex:  # the order still works without it
    print('note: purchase sheet not read:', ex)

# ---- Excel ----
AR = 'Arial'
F = Font(name=AR, size=10); FB = Font(name=AR, size=10, bold=True); FH = Font(name=AR, size=14, bold=True); FM = Font(name=AR, size=9, color='5D676D')
HEAD = PatternFill('solid', fgColor='1C2226'); HF = Font(name=AR, size=10, bold=True, color='FFFFFF'); GROUP = PatternFill('solid', fgColor='E8ECEA')
thin = Side(style='thin', color='CFD6D3'); BOX = Border(bottom=thin); WRAP = Alignment(wrap_text=True, vertical='top')


def header(ws, r, cols):
    for c, h in enumerate(cols, 1):
        cell = ws.cell(r, c, h); cell.font = HF; cell.fill = HEAD; cell.alignment = Alignment(vertical='center', wrap_text=True)


wb = Workbook()
ws = wb.active; ws.title = 'Замовлення'
ws['A1'] = 'Зона мангала — замовлення матеріалів'; ws['A1'].font = FH
ws['A2'] = f'{version}. Труба і смуга пораховані з 3D-моделі по деталях і розкладені на хлисти 6 м (різ 3 мм); решта — зі списку матеріалів.'; ws['A2'].font = FM
header(ws, 4, ['№', 'Позиція', 'Кількість', 'Одиниця', 'Примітка'])
r = 4; n = 0
r += 1; ws.cell(r, 1, 'Профільна труба і смуга (хлисти по 6 м)').font = FB
for c in range(1, 6): ws.cell(r, c).fill = GROUP
for s in secs:
    pl = plan[s]; r += 1; n += 1
    note = f"деталей {sum(groups[s].values())}, потрібно {pl['used'] / 1000:.1f} м, відхід {pl['waste'] / 1000:.1f} м — див. лист «Різка»".replace('.', ',')
    for c, v in enumerate([n, SEC_NAME[s], pl['n'], 'хлист 6 м', note], 1):
        cell = ws.cell(r, c, v); cell.font = F; cell.alignment = WRAP; cell.border = BOX
cur = None
for cat, b, c, d, e, f in other:
    if cat != cur:
        cur = cat; r += 1; ws.cell(r, 1, cat or 'Інше').font = FB
        for k in range(1, 6): ws.cell(r, k).fill = GROUP
    r += 1; n += 1
    for k, v in enumerate([n, b, c, d, f or e], 1):
        cell = ws.cell(r, k, v); cell.font = F; cell.alignment = WRAP; cell.border = BOX
for col, w in zip('ABCDE', (5, 52, 11, 16, 60)): ws.column_dimensions[col].width = w
ws.freeze_panes = 'A5'

w2 = wb.create_sheet('Різка')
w2['A1'] = 'Різка труби і смуги: яку довжину, скільки штук, куди'; w2['A1'].font = FH
w2['A2'] = 'Довжини — з 3D-моделі, округлені до 5 мм. Перед різкою звірити по місцю.'; w2['A2'].font = FM
header(w2, 4, ['Профіль', 'Довжина, мм', 'Штук', 'Куди', 'Разом, м'])
r = 4
for s in secs:
    r += 1; w2.cell(r, 1, SEC_NAME[s]).font = FB
    for c in range(1, 6): w2.cell(r, c).fill = GROUP
    for (L, z), q in sorted(groups[s].items(), key=lambda t: (-t[0][0], t[0][1])):
        r += 1
        for c, v in enumerate([SEC_NAME[s], L, q, z, round(L * q / 1000, 2)], 1):
            cell = w2.cell(r, c, v); cell.font = F; cell.border = BOX
for col, w in zip('ABCDE', (30, 13, 8, 30, 10)): w2.column_dimensions[col].width = w

w3 = wb.create_sheet('Карти різки')
w3['A1'] = 'Карти різки хлистів 6 м'; w3['A1'].font = FH
w3['A2'] = f'Різ {KERF} мм. Відрізати по порядку зліва направо, залишок — у відхід або на дрібні деталі.'; w3['A2'].font = FM
header(w3, 4, ['Профіль', 'Хлист №', 'Відрізки, мм', 'Залишок, мм'])
r = 4
for s in secs:
    for i, st in enumerate(plan[s]['sticks'], 1):
        r += 1
        for c, v in enumerate([SEC_NAME[s], i, ' + '.join(str(x) for x in st['cuts']), st['free']], 1):
            cell = w3.cell(r, c, v); cell.font = F; cell.border = BOX; cell.alignment = WRAP
for col, w in zip('ABCD', (30, 9, 70, 12)): w3.column_dimensions[col].width = w
for sh in wb.worksheets: sh.sheet_view.showGridLines = False
wb.save(os.path.join(OUT, 'zamovlennya.xlsx'))

# ---- printable HTML ----
CSS = '''
@page { size: A4 landscape; margin: 10mm; }
* { box-sizing: border-box; }
body { font: 10pt/1.35 Arial, sans-serif; color: #1c2226; margin: 0; }
.page { page-break-after: always; break-after: page; position: relative; min-height: 186mm; padding-bottom: 14mm; }
.page:last-child { page-break-after: auto; break-after: auto; }
h1 { font-size: 18pt; margin: 0 0 4mm; } h2 { font-size: 13pt; margin: 0 0 3mm; }
.tb { position: absolute; left: 0; right: 0; bottom: 0; border-top: 1.2pt solid #1c2226; display: flex; justify-content: space-between; font-size: 8.5pt; padding-top: 1.5mm; }
.dw { display: flex; align-items: center; justify-content: center; height: 168mm; }
.dw svg { max-width: 100%; max-height: 168mm; width: auto; height: auto; }
table { border-collapse: collapse; width: 100%; font-size: 9pt; }
th, td { border-bottom: .5pt solid #b9c2bf; padding: 1.2mm 2mm; text-align: left; vertical-align: top; }
th { background: #1c2226; color: #fff; } td.n { text-align: right; font-variant-numeric: tabular-nums; }
tr.g td { background: #e8ecea; font-weight: bold; }
.cols { columns: 2; column-gap: 8mm; } .cols table { break-inside: auto; }
.stick { display: flex; height: 5mm; border: .5pt solid #1c2226; margin: .6mm 0 1.6mm; }
.stick span { border-right: .5pt solid #1c2226; font-size: 6.5pt; text-align: center; overflow: hidden; background: #dfe5e3; }
.stick span.w { background: repeating-linear-gradient(45deg, #fff 0 2px, #cfd6d3 2px 4px); }
.lbl { font-size: 8pt; color: #5d676d; }
'''
pages = []
total = 1 + len(DRAWINGS) + 3


def tb(i, title):
    return f'<div class="tb"><span>Зона мангала · {html.escape(version)}</span><span>{html.escape(title)}</span><span>Аркуш {i} з {{TOTAL}}</span></div>'


toc = ''.join(f'<li>{html.escape(t)}</li>' for _, t in DRAWINGS)
pages.append(f'''<section class="page"><h1>Зона мангала — креслення для виробництва</h1>
<p>{html.escape(version)}. Розміри в мм, висоти від плитки майданчика. Довжини деталей узято з 3D-моделі; перед різкою звірити по місцю.</p>
<h2>Зміст</h2><ol>{toc}<li>Різка труби і смуги</li><li>Карти різки хлистів 6 м</li><li>Замовлення матеріалів</li></ol>
<p class="lbl">Файли поруч: zamovlennya.xlsx (замовлення, різка, карти), rozkriy.html.</p>{tb(1, 'Титул')}</section>''')
for i, (fn, title) in enumerate(DRAWINGS, 2):
    path = os.path.join(ROOT, 'kreslennia', fn)
    svg = open(path, encoding='utf-8').read() if os.path.exists(path) else f'<p>немає файлу {fn}</p>'
    pages.append(f'<section class="page"><h2>{html.escape(title)}</h2><div class="dw">{svg}</div>{tb(i, title)}</section>')
pn = len(DRAWINGS) + 2
rows = ''
for s in secs:
    rows += f'<tr class="g"><td colspan="4">{html.escape(SEC_NAME[s])} — {sum(groups[s].values())} шт, {plan[s]["used"] / 1000:.1f} м → {plan[s]["n"]} хлист.</td></tr>'.replace('.', ',', 1)
    for (L, z), q in sorted(groups[s].items(), key=lambda t: (-t[0][0], t[0][1])):
        rows += f'<tr><td class="n">{L}</td><td class="n">{q}</td><td>{html.escape(z)}</td><td class="n">{L * q / 1000:.2f}</td></tr>'
cut_html = f'<div class="cols"><table><tr><th>Довжина, мм</th><th>Шт</th><th>Куди</th><th>м</th></tr>{rows}</table></div>'
pages.append(f'<section class="page"><h2>Різка труби і смуги</h2>{cut_html}{tb(pn, "Різка")}</section>')
maps = ''
for s in secs:
    maps += f'<p><b>{html.escape(SEC_NAME[s])}</b> — {plan[s]["n"]} хлист. по 6 м, відхід {plan[s]["waste"] / 1000:.1f} м</p>'
    for i, st in enumerate(plan[s]['sticks'], 1):
        if st.get('long'):
            maps += f'<div class="lbl">№{i}: деталь {st["cuts"][0]} мм довша за хлист — купити мірну або зварити</div>'; continue
        spans = ''.join(f'<span style="width:{L / STICK * 100:.2f}%">{L}</span>' for L in st['cuts'])
        if st['free'] > 0: spans += f'<span class="w" style="width:{st["free"] / STICK * 100:.2f}%"></span>'
        maps += f'<div class="lbl">№{i}: {" + ".join(map(str, st["cuts"]))} · залишок {st["free"]}</div><div class="stick">{spans}</div>'
pages.append(f'<section class="page"><h2>Карти різки хлистів 6 м (різ {KERF} мм)</h2><div class="cols">{maps}</div>{tb(pn + 1, "Карти різки")}</section>')
orows = ''.join(f'<tr><td>{html.escape(SEC_NAME[s])}</td><td class="n">{plan[s]["n"]}</td><td>хлист 6 м</td></tr>' for s in secs)
cur = None
for cat, b, c, d, e, f in other:
    if cat != cur:
        cur = cat; orows += f'<tr class="g"><td colspan="3">{html.escape(str(cat))}</td></tr>'
    orows += f'<tr><td>{html.escape(str(b))}</td><td class="n">{html.escape(str(c)).replace(".", ",")}</td><td>{html.escape(str(d))}</td></tr>'
pages.append(f'<section class="page"><h2>Замовлення матеріалів</h2><div class="cols"><table><tr><th>Позиція</th><th>К-сть</th><th>Од.</th></tr>'
             f'<tr class="g"><td colspan="3">Профільна труба і смуга — з розкрою</td></tr>{orows}</table></div>{tb(pn + 2, "Замовлення")}</section>')
doc = f'<!doctype html><html lang="uk"><meta charset="utf-8"><title>Зона мангала — виробництво</title><style>{CSS}</style><body>{"".join(pages)}</body></html>'
doc = doc.replace('{TOTAL}', str(len(pages)))
open(os.path.join(OUT, 'kreslennia-druk.html'), 'w', encoding='utf-8').write(doc)
# the cut list alone, for the workshop
cut_doc = (f'<!doctype html><html lang="uk"><meta charset="utf-8"><title>Різка — зона мангала</title><style>{CSS}</style><body>'
           f'{pages[-3]}{pages[-2]}</body></html>').replace('{TOTAL}', str(len(pages)))
open(os.path.join(OUT, 'rozkriy.html'), 'w', encoding='utf-8').write(cut_doc)

# ---- the interactive 3D model for the workshop (a copy, refreshed every run) ----
import shutil
shutil.copyfile(os.path.join(ROOT, 'zona-mangala.html'), os.path.join(OUT, 'model-3d.html'))

# ---- PDF through a headless Edge / Chrome ----
for exe in (r'C:\Program Files\Google\Chrome\Application\chrome.exe', r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'):
    if os.path.exists(exe):
        src = 'file:///' + quote(os.path.join(OUT, 'kreslennia-druk.html').replace('\\', '/'), safe='/:')
        pdf = os.path.join(OUT, 'kreslennia-i-rozkriy.pdf')
        if os.path.exists(pdf): os.remove(pdf)       # never leave an old PDF behind
        import tempfile
        prof = tempfile.mkdtemp(prefix='pdfprof')   # own profile, so a running browser does not swallow the job
        subprocess.run([exe, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--user-data-dir={prof}', f'--print-to-pdf={pdf}', src],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        print('pdf', os.path.exists(pdf) and os.path.getsize(pdf))
        break
sys.stdout.reconfigure(encoding='utf-8'); print('ok:', len(parts), 'pieces;', ', '.join(f"{s} {plan[s]['n']} хл." for s in secs))
