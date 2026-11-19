"""Tiny SVG drafting helper shared by the drawing generators. Units: mm."""
import os


class View:
    def __init__(self, x0, x1, y0, y1, pad=(70, 70, 50, 60), flip=True, k=1.0):
        self.k = k  # text/tick scale for big views
        # model box -> svg; pad = left, right, top, bottom; flip=True puts +y up (elevations)
        self.x0, self.x1, self.y0, self.y1 = x0, x1, y0, y1
        self.pl, self.pr, self.pt, self.pb = pad
        self.flip = flip
        self.parts = []

    def X(self, x): return x - self.x0 + self.pl
    def Y(self, y): return (self.y1 - y + self.pt) if self.flip else (y - self.y0 + self.pt)
    def W(self): return self.x1 - self.x0 + self.pl + self.pr
    def H(self): return self.y1 - self.y0 + self.pt + self.pb
    def add(self, s): self.parts.append(s)

    def rect(self, x0, y0, x1, y1, cls='ol'):
        X0, X1 = sorted((self.X(x0), self.X(x1)))
        Y0, Y1 = sorted((self.Y(y0), self.Y(y1)))
        self.add(f'<rect class="{cls}" x="{X0:.1f}" y="{Y0:.1f}" width="{X1-X0:.1f}" height="{Y1-Y0:.1f}"/>')

    def poly(self, pts, cls='ol'):
        p = ' '.join(f'{self.X(x):.1f},{self.Y(y):.1f}' for x, y in pts)
        self.add(f'<polygon class="{cls}" points="{p}"/>')

    def line(self, x0, y0, x1, y1, cls='ol'):
        self.add(f'<line class="{cls}" x1="{self.X(x0):.1f}" y1="{self.Y(y0):.1f}" x2="{self.X(x1):.1f}" y2="{self.Y(y1):.1f}"/>')

    def circle(self, x, y, r, cls='ol'):
        self.add(f'<circle class="{cls}" cx="{self.X(x):.1f}" cy="{self.Y(y):.1f}" r="{r}"/>')

    BASE = {'dt': 15, 'note': 14, 'lt': 13, 'bt': 13, 'ttl': 18}

    def fs(self, cls):
        return '' if self.k == 1 else f' style="font-size:{self.BASE.get(cls, 14) * self.k:.0f}px"'

    def text(self, x, y, t, cls='lt', anchor='start'):
        self.add(f'<text class="{cls}" x="{self.X(x):.1f}" y="{self.Y(y):.1f}" text-anchor="{anchor}"{self.fs(cls)}>{t}</text>')

    def tick(self, x, y):
        X, Y, t = self.X(x), self.Y(y), 4 * self.k
        self.add(f'<line class="dim" x1="{X-t:.1f}" y1="{Y+t:.1f}" x2="{X+t:.1f}" y2="{Y-t:.1f}"/>')

    def dimH(self, x1, x2, y, t=None, ext_from=None):
        t = t if t is not None else f'{abs(x2-x1):g}'
        if ext_from is not None:
            up = (self.Y(y) < self.Y(ext_from))
            for x in (x1, x2):
                self.add(f'<line class="ext" x1="{self.X(x):.1f}" y1="{self.Y(ext_from):.1f}" x2="{self.X(x):.1f}" y2="{self.Y(y) + (-6 if up else 6):.1f}"/>')
        self.line(x1, y, x2, y, 'dim'); self.tick(x1, y); self.tick(x2, y)
        X, Y = (self.X(x1) + self.X(x2)) / 2, self.Y(y) - 5 * self.k
        self.add(f'<text class="dt" x="{X:.1f}" y="{Y:.1f}" text-anchor="middle"{self.fs("dt")}>{t}</text>')

    def dimV(self, y1, y2, x, t=None, ext_from=None, side='left'):
        t = t if t is not None else f'{abs(y2-y1):g}'
        if ext_from is not None:
            for y in (y1, y2): self.line(ext_from, y, x + (6 if x > ext_from else -6), y, 'ext')
        self.line(x, y1, x, y2, 'dim'); self.tick(x, y1); self.tick(x, y2)
        X, Y = self.X(x) + (-5 if side == 'left' else 5) * self.k, (self.Y(y1) + self.Y(y2)) / 2
        a = 'end' if side == 'left' else 'start'
        self.add(f'<text class="dt" x="{X:.1f}" y="{Y + 4 * self.k:.1f}" text-anchor="{a}"{self.fs("dt")}>{t}</text>')

    def pos(self, n, x, y, tx, ty):
        self.line(x, y, tx, ty, 'lead')
        self.add(f'<circle class="bub" cx="{self.X(tx):.1f}" cy="{self.Y(ty):.1f}" r="{11 * self.k:.0f}"/>')
        self.add(f'<text class="bt" x="{self.X(tx):.1f}" y="{self.Y(ty) + 4 * self.k:.1f}" text-anchor="middle"{self.fs("bt")}>{n}</text>')

    def svg(self, title):
        return (f'<svg viewBox="0 0 {self.W():.0f} {self.H():.0f}" role="img" aria-label="{title}">'
                + ''.join(self.parts) + '</svg>')

    def save(self, path, title):
        """Standalone light-theme SVG that GitHub renders directly."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        style = ('.ol{fill:none;stroke:#1c2226;stroke-width:1.4}.thin{stroke-width:.8}'
                 '.hid{fill:none;stroke:#7b868c;stroke-width:.9;stroke-dasharray:6 4}'
                 '.cl{stroke:#7b868c;stroke-width:.7;stroke-dasharray:14 3 2 3}'
                 '.brick{fill:#efe3d0;stroke:none}.stone{fill:#e3e1dc;stroke:#7b868c;stroke-width:.6}'
                 '.fill{fill:#e8ecea;stroke:#1c2226;stroke-width:1.2}'
                 '.dim{stroke:#c4521c;stroke-width:.8}.ext{stroke:#c4521c;stroke-width:.5}'
                 '.lead{stroke:#5d676d;stroke-width:.7}'
                 '.dt{fill:#c4521c;font:500 15px "IBM Plex Mono",Consolas,monospace}'
                 '.note{fill:#5d676d;font:14px "IBM Plex Sans",Segoe UI,sans-serif}'
                 '.lt{fill:#1c2226;font:13px "IBM Plex Sans",Segoe UI,sans-serif}'
                 '.bub{fill:#fff;stroke:#1c2226;stroke-width:1}'
                 '.bt{fill:#1c2226;font:600 13px "IBM Plex Mono",Consolas,monospace}'
                 '.ttl{fill:#1c2226;font:600 18px "IBM Plex Sans",Segoe UI,sans-serif}')
        body = ''.join(self.parts)
        out = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.W():.0f} {self.H() + 34:.0f}" '
               f'width="{self.W():.0f}" height="{self.H() + 34:.0f}"><style>{style}</style>'
               f'<rect width="100%" height="100%" fill="#ffffff"/>'
               f'<text class="ttl" x="16" y="24">{title}</text><g transform="translate(0 34)">{body}</g></svg>')
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(out)


PAGE_CSS = '''
:root {
  --paper: #f6f7f5; --sheet: #ffffff; --ink: #1c2226; --muted: #5d676d; --line: #cfd6d3;
  --dim: #c4521c; --brick: #efe3d0; --hid: #7b868c; --stone: #e3e1dc; --fillc: #e8ecea;
  --font-ui: 'IBM Plex Sans', system-ui, -apple-system, 'Segoe UI', sans-serif;
  --font-mono: 'IBM Plex Mono', ui-monospace, Consolas, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --paper: #14181a; --sheet: #1b2023; --ink: #e4e9ea; --muted: #9aa4a9; --line: #313a3e;
  --dim: #f08a52; --brick: #3a3128; --hid: #8e999e; --stone: #2c3134; --fillc: #252b2e; color-scheme: dark; } }
:root[data-theme="dark"] {
  --paper: #14181a; --sheet: #1b2023; --ink: #e4e9ea; --muted: #9aa4a9; --line: #313a3e;
  --dim: #f08a52; --brick: #3a3128; --hid: #8e999e; --stone: #2c3134; --fillc: #252b2e; color-scheme: dark; }
body { background: var(--paper); color: var(--ink); font-family: var(--font-ui); font-size: 15px; line-height: 1.5;
  padding-block: 24px 48px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
.wrap { max-width: 1180px; margin: 0 auto; display: grid; gap: 20px; }
.tb { display: grid; grid-template-columns: minmax(0, 1fr) auto; gap: 8px 24px; align-items: end;
  border: 1.5px solid var(--ink); background: var(--sheet); padding: 14px 18px; }
h1 { margin: 0; font-size: 24px; font-weight: 600; text-wrap: balance; }
.tb p { margin: 2px 0 0; color: var(--muted); }
.meta { display: grid; grid-template-columns: auto auto; gap: 2px 14px; font-family: var(--font-mono); font-size: 13px; margin: 0; }
.meta dt { color: var(--muted); } .meta dd { margin: 0; }
.sheet-h { margin: 12px 0 0; font-size: 18px; font-weight: 600; border-bottom: 1.5px solid var(--ink); padding-bottom: 4px; }
.grid { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 20px; }
.v { background: var(--sheet); border: 1px solid var(--line); padding: 12px 14px 8px; min-width: 0; display: grid; gap: 4px; align-content: start; }
.v.wide { grid-column: 1 / -1; }
.v h2 { margin: 0; font-size: 15px; font-weight: 600; }
.v h2 span { font-weight: 400; color: var(--muted); }
.sc { overflow-x: auto; }
.sc svg { display: block; width: 100%; min-width: 460px; height: auto; }
.v.wide .sc svg { min-width: 760px; }
svg .ol { fill: none; stroke: var(--ink); stroke-width: 1.4; vector-effect: non-scaling-stroke; }
svg .thin { stroke-width: .8; }
svg .hid { fill: none; stroke: var(--hid); stroke-width: .9; stroke-dasharray: 6 4; vector-effect: non-scaling-stroke; }
svg .cl { stroke: var(--hid); stroke-width: .7; stroke-dasharray: 14 3 2 3; vector-effect: non-scaling-stroke; }
svg .brick { fill: var(--brick); stroke: none; }
svg .stone { fill: var(--stone); stroke: var(--hid); stroke-width: .6; vector-effect: non-scaling-stroke; }
svg .fill { fill: var(--fillc); stroke: var(--ink); stroke-width: 1.2; vector-effect: non-scaling-stroke; }
svg .dim, svg .ext { stroke: var(--dim); stroke-width: .8; vector-effect: non-scaling-stroke; }
svg .ext { stroke-width: .5; }
svg .lead { stroke: var(--muted); stroke-width: .7; vector-effect: non-scaling-stroke; }
svg .dt { fill: var(--dim); font: 500 15px var(--font-mono); }
svg .note { fill: var(--muted); font: 14px var(--font-ui); }
svg .lt { fill: var(--ink); font: 13px var(--font-ui); }
svg .bub { fill: var(--sheet); stroke: var(--ink); stroke-width: 1; vector-effect: non-scaling-stroke; }
svg .bt { fill: var(--ink); font: 600 13px var(--font-mono); }
svg .ttl { fill: var(--ink); font: 600 18px var(--font-ui); }
.notes, .bom { background: var(--sheet); border: 1px solid var(--line); padding: 14px 18px; min-width: 0; }
.notes h2, .bom h2 { margin: 0 0 8px; font-size: 15px; font-weight: 600; }
.notes ol, .notes ul { margin: 0; padding-left: 20px; display: grid; gap: 4px; max-width: 80ch; }
.tw { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; min-width: 720px; font-size: 14px; }
th, td { text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-size: 12px; font-weight: 600; color: var(--muted); letter-spacing: .04em; }
td.n { font-family: var(--font-mono); font-weight: 500; width: 2.5em; }
td.m { font-family: var(--font-mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
td.c { color: var(--muted); }
tr.sub td { font-weight: 600; background: var(--paper); }
.total { margin: 10px 0 0; font-family: var(--font-mono); font-size: 13px; color: var(--muted); }
a { color: var(--dim); }
@media (max-width: 820px) { .grid { grid-template-columns: minmax(0, 1fr); } .tb { grid-template-columns: minmax(0, 1fr); } }
'''

HEAD = '''<meta charset="utf-8">
<title>{title}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>{css}</style>
'''
