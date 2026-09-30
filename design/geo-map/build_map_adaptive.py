# -*- coding: utf-8 -*-
"""Карта «География поставок» для телефона и планшета.

На узком экране ПК-карта целиком даёт подписи по 8–9px, а шесть сибирских
точек сливаются в одно пятно. Поэтому карта собрана как атлас:

  1. обзор — вся Россия, все 10 регионов подсвечены, две рамки-«видоискателя»
     показывают, какие места увеличены ниже; Амурская обл. подписана прямо тут;
  2. врезка «Сибирь» — 6 регионов крупно, подпись у каждой точки;
  3. врезка «Юг России» — 3 региона крупно.

Телефон: блоки друг под другом. Планшет: обзор сверху, врезки в ряд.
Размеры в SVG — логические CSS-пиксели ширины контента (358 и 704),
PNG рендерится с плотностью 3× (телефон) и 2× (планшет).

Геометрия, проекция и точки — из build_map.py (одна правда на все версии).

    python3 build_map_adaptive.py            # → map_mobile_v2.svg, map_tablet_v2.svg
    node render_map.cjs map_mobile_v2.svg saturn-map-mobile-v2.png 3
    node render_map.cjs map_tablet_v2.svg saturn-map-tablet-v2.png 2
"""
import io, os, math, runpy, contextlib

os.environ['MAP_SITE'] = '1'
here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(here, 'build_map.py'))
PIN, all_regions, path = g['PIN'], g['all_regions'], g['path']
OFFICE = g['OFFICE']

BG = "#141210"; CARD = "#1A1714"; CARDLINE = "rgba(255,255,255,.07)"
LAND = "#231E1A"; LANDS = "rgba(255,255,255,.075)"
HIL = "#3A2A20"; HILS = "#FF4200"; ORANGE = "#FF4200"
TXT = "#F3F1EE"; MUTED = "#8C847C"; LEAD = "rgba(255,255,255,.38)"

# рамка всей России в координатах build_map (1600×900)
RUS = (70, 60, 1460, 760)
# что показывают врезки (x, y, w, h в координатах build_map)
SIB = (478, 448, 480, 360)
SOUTH = (92, 470, 205, 160)
SIB_F = (530, 440, 420, 320)     # рамка Сибири на обзоре — плотнее, чем врезка

# ---------- общий слой земли (один раз, дальше <use>) ----------
defs = ['<defs>', '<g id="land">']
for nm, rr, t in all_regions:
    if not t:
        for ring in rr:
            defs.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width="0.6" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>')
defs.append('</g><g id="hil">')
for nm, rr, t in all_regions:
    if t:
        for ring in rr:
            defs.append(f'<path d="{path(ring)}" fill="{HIL}" vector-effect="non-scaling-stroke" stroke-linejoin="round"/>')
defs.append('</g>')
defs.append('<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.5"/></filter>')
defs.append('<linearGradient id="scrim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1A1714" stop-opacity=".97"/><stop offset=".13" stop-color="#1A1714" stop-opacity=".55"/><stop offset=".3" stop-color="#1A1714" stop-opacity="0"/><stop offset=".85" stop-color="#1A1714" stop-opacity="0"/><stop offset="1" stop-color="#1A1714" stop-opacity=".6"/></linearGradient>')
defs.append('<radialGradient id="vign" cx="50%" cy="45%" r="70%"><stop offset="0" stop-color="#FF4200" stop-opacity=".07"/><stop offset="1" stop-color="#FF4200" stop-opacity="0"/></radialGradient>')
defs.append('</defs>')


class Panel:
    """Прямоугольник на холсте, в который вписан кусок карты view."""
    def __init__(self, view, X, Y, W, H):
        vx, vy, vw, vh = view
        self.k = min(W / vw, H / vh)
        # центрируем view внутри прямоугольника
        self.ox = X + (W - vw * self.k) / 2 - vx * self.k
        self.oy = Y + (H - vh * self.k) / 2 - vy * self.k
        self.rect = (X, Y, W, H)

    def P(self, x, y):
        return self.ox + x * self.k, self.oy + y * self.k

    def pin(self, nm):
        return self.P(*PIN[nm])

    def map(self, out, cid, hil_w, glow=True, clip=None):
        X, Y, W, H = clip or self.rect
        out.append(f'<clipPath id="{cid}"><rect x="{X}" y="{Y}" width="{W}" height="{H}" rx="{0 if cid == "c0" else 14}"/></clipPath>')
        tr = f'translate({self.ox:.2f} {self.oy:.2f}) scale({self.k:.5f})'
        out.append(f'<g clip-path="url(#{cid})"><g transform="{tr}">')
        out.append('<use href="#land"/>')
        if glow:
            out.append(f'<use href="#hil" fill="none" stroke="{ORANGE}" stroke-opacity=".28" stroke-width="{hil_w * 2.2}" filter="url(#glow)"/>')
        out.append(f'<use href="#hil" stroke="{HILS}" stroke-width="{hil_w}"/>')
        out.append('</g></g>')


def dot(out, x, y, r, office=False):
    if office:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 1.75:.1f}" fill="{BG}" stroke="#fff" stroke-width="{max(1.5, r * .32):.1f}"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * .7:.1f}" fill="#fff"/>')
    else:
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * 1.8:.1f}" fill="{ORANGE}" fill-opacity=".12"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{ORANGE}"/>')


def label(out, text, x, y, size, anchor="start", weight=600, col=TXT, halo=True):
    h = f' stroke="{BG}" stroke-width="{size * .32:.1f}" stroke-linejoin="round" paint-order="stroke"' if halo else ''
    out.append(f'<text x="{x:.1f}" y="{y:.1f}" fill="{col}" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}"{h}>{text}</text>')


def leader(out, pts):
    out.append(f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{LEAD}" stroke-width="1"/>')


def tw(text, size, weight=600):
    """Ширина строки Montserrat (оценка, кириллица чуть шире латиницы)."""
    return len(text) * size * (.64 if weight >= 700 else .61)


def callouts(out, panel, spec, size, r, box):
    """spec: имя → (dx, dy, anchor, текст[, подстрока]) — смещение подписи от точки, px.
    Подпись не выходит за карточку box; выноска идёт от точки к ближайшей
    точке подписи и рисуется, только если подпись не вплотную к точке."""
    bx0, by0, bx1, by1 = box
    placed = []
    for nm, (dx, dy, anc, text, *sub) in spec.items():
        px, py = panel.pin(nm)
        off = nm == OFFICE
        w = max([tw(text, size, 700 if off else 600)] + [tw(t, size - 2) for t in sub])
        x0 = {"start": px + dx, "end": px + dx - w, "middle": px + dx - w / 2}[anc]
        x0 = min(max(x0, bx0 + 12), bx1 - 12 - w)          # не вылезать за карточку
        y = py + dy
        top, bot = y - size * .78, y + (size * 1.25 if sub else size * .22)
        placed.append((nm, px, py, x0, w, y, top, bot, text, sub, off))
    for nm, px, py, x0, w, y, top, bot, *_ in placed:
        qx = min(max(px, x0 - 3), x0 + w + 3)
        if nm in LEAD_TO: qx = x0 + w * LEAD_TO[nm]   # увести выноску в сторону от соседней точки
        qy = min(max(py, top - 3), bot + 3)
        if ((qx - px) ** 2 + (qy - py) ** 2) ** .5 > r * 2.6:
            k = 1 - (r * 1.9 if nm == OFFICE else r * 1.2) / ((qx - px) ** 2 + (qy - py) ** 2) ** .5
            leader(out, [(px + (qx - px) * (1 - k), py + (qy - py) * (1 - k)), (qx, qy)])
    for nm, px, py, *_ in placed:
        dot(out, px, py, r, nm == OFFICE)
    for nm, px, py, x0, w, y, top, bot, text, sub, off in placed:
        label(out, text, x0, y, size, "start", 700 if off else 600, "#fff" if off else TXT)
        for i, t in enumerate(sub):
            label(out, t, x0, y + (size + 3) * (i + 1), size - 2, "start", 500, MUTED)


def card(out, X, Y, W, H, title, count, fs):
    out.append(f'<rect x="{X + .5}" y="{Y + .5}" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{CARDLINE}"/>')
    hx, hy = X + 16, Y + 26
    out.append(f'<rect x="{hx}" y="{hy - fs * .42:.1f}" width="14" height="1.6" fill="{ORANGE}"/>')
    out.append(f'<text x="{hx + 22}" y="{hy}" fill="{TXT}" font-size="{fs}" font-weight="700" letter-spacing="{fs * .14:.2f}">{title}</text>')
    out.append(f'<text x="{X + W - 16}" y="{hy}" fill="{MUTED}" font-size="{fs}" font-weight="600" text-anchor="end" letter-spacing="{fs * .06:.2f}">{count}</text>')


def frame(out, panel, view, tag, anchor, fs):
    """Рамка-видоискатель на обзорной карте: уголки + подпись."""
    x0, y0 = panel.P(view[0], view[1]); x1, y1 = panel.P(view[0] + view[2], view[1] + view[3])
    c = min(8, (x1 - x0) / 4)
    st = f'fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="1.2"'
    for (x, y, sx, sy) in ((x0, y0, 1, 1), (x1, y0, -1, 1), (x0, y1, 1, -1), (x1, y1, -1, -1)):
        out.append(f'<polyline points="{x + sx * c:.1f},{y:.1f} {x:.1f},{y:.1f} {x:.1f},{y + sy * c:.1f}" {st}/>')
    tx = {"start": x0, "end": x1, "middle": (x0 + x1) / 2}[anchor]
    out.append(f'<text x="{tx:.1f}" y="{y1 + fs + 6:.1f}" fill="{MUTED}" font-size="{fs * .9:.1f}" font-weight="700" letter-spacing="{fs * .14:.2f}" text-anchor="{anchor}">{tag}</text>')


def build(W, layout, fn):
    out = []
    H = math.ceil(layout(out, W))   # дробная высота даёт белую полоску снизу PNG
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Montserrat,Arial,sans-serif">',
           *defs, f'<rect width="{W}" height="{H}" fill="{BG}"/>', *out, '</svg>']
    io.open(os.path.join(here, fn), 'w', encoding='utf-8').write('\n'.join(svg))
    print('wrote', fn, W, '×', round(H))


# ---------- подписи врезок (смещение от точки в px, выравнивание, текст) ----------
SIB_LAB = {
    "Красноярский край":     (0, 27, "middle", "Красноярский край"),
    "Томская область":       (24, -22, "middle", "Томская обл."),
    "Омская область":        (-24, -36, "middle", "Омская обл."),
    "Новосибирская область": (-300, 112, "start", "Новосибирская обл."),
    "Кемеровская область":   (48, 5, "start", "Кемеровская обл."),
    "Алтайский край":        (20, 32, "start", "Алтайский край", "офис · Барнаул"),
}
# куда на подписи приходит выноска (доля ширины) — если по прямой она задела бы офис
LEAD_TO = {"Новосибирская область": .2}
SOUTH_LAB = {
    "Ростовская область":  (40, -8, "start", "Ростовская обл."),
    "Краснодарский край":  (-10, -50, "middle", "Краснодарский край"),
    "Ставропольский край": (44, 26, "start", "Ставропольский край"),
}


def overview(out, X, Y, W, fs, r, amur):
    H = W * RUS[3] / RUS[2]
    p = Panel(RUS, X, Y, W, H)
    p.map(out, "c0", 1.0, glow=False)
    frame(out, p, SOUTH, "ЮГ", "start", fs)
    frame(out, p, SIB_F, "СИБИРЬ", "start", fs)
    for nm in g['TARGETS']:
        dot(out, *p.pin(nm), r, nm == OFFICE)
    ax, ay = p.pin("Амурская область")
    dx, dy, anc = amur
    leader(out, [(ax, ay + r * 1.3), (ax + dx, ay + dy - fs - 1)])
    label(out, "Амурская обл.", ax + dx, ay + dy, fs, anc, 600, MUTED)
    return H


def inset(out, view, X, Y, W, H, title, count, spec, fs_head, fs_lab, r, pad_top=40):
    out.append(f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" rx="14" fill="{CARD}"/>')
    p = Panel(view, X, Y + pad_top, W, H - pad_top)
    p.map(out, f"c{int(X)}_{int(Y)}", 1.6, clip=(X, Y, W, H))
    out.append(f'<rect x="{X}" y="{Y}" width="{W}" height="{H}" rx="14" fill="url(#scrim)"/>')
    card(out, X, Y, W, H, title, count, fs_head)
    callouts(out, p, spec, fs_lab, r, (X, Y + pad_top, X + W, Y + H))


def mobile(out, W):
    y = 4
    y += overview(out, 8, y, W - 16, 10, 2.6, (0, 26, "middle")) + 22
    hs = 356
    inset(out, SIB, 0, y, W, hs, "СИБИРЬ", "6 регионов", SIB_LAB, 10, 12.5, 5.5)
    y += hs + 12
    hso = 250
    inset(out, SOUTH, 0, y, W, hso, "ЮГ РОССИИ", "3 региона", SOUTH_LAB, 10, 12.5, 5.5)
    return y + hso


def tablet(out, W):
    y = 4
    y += overview(out, 10, y, W - 20, 12, 4, (0, 34, "middle")) + 26
    gap = 16; cw = (W - gap) / 2; h = 380
    inset(out, SIB, 0, y, cw, h, "СИБИРЬ", "6 регионов", SIB_LAB, 10.5, 13, 6)
    inset(out, SOUTH, cw + gap, y, cw, h, "ЮГ РОССИИ", "3 региона", SOUTH_LAB, 10.5, 13, 6)
    return y + h


if __name__ == '__main__':
    build(358, mobile, 'map_mobile_v2.svg')
    build(704, tablet, 'map_tablet_v2.svg')
