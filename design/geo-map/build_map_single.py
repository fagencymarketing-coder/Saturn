# -*- coding: utf-8 -*-
"""Карта «География поставок» для телефона и планшета — одна карта, одним блоком.

Та же композиция, что на ПК (вся Россия, 10 подсвеченных регионов, подпись у
каждого), но подписи разложены под узкий экран (9,5px на телефоне, 11px на
планшете) и вынесены в свободное место — южные
регионы подписаны над и под Кавказом, сибирские разведены «веером» во все
стороны от кластера, нижний ряд подписей стоит под картой, где нет суши.

Размеры SVG — логические CSS-пиксели ширины контента: телефон 358 (390 − 2×16),
планшет 704 (768 − 2×32). PNG: телефон 3×, планшет 2×.
Геометрия, проекция и точки — из build_map.py (одна правда на все версии).

    python3 build_map_single.py      # → map_mobile_v3.svg, map_tablet_v3.svg
    node render_map.cjs map_mobile_v3.svg saturn-map-mobile-v3.png 3
    node render_map.cjs map_tablet_v3.svg saturn-map-tablet-v3.png 2
"""
import io, os, math, runpy, contextlib

os.environ['MAP_SITE'] = '1'
here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(here, 'build_map.py'))
PIN, all_regions, path, OFFICE = g['PIN'], g['all_regions'], g['path'], g['OFFICE']

BG = "#141210"; LAND = "#211C18"; LANDS = "rgba(255,255,255,.075)"
HIL = "#3A2A20"; ORANGE = "#FF4200"
TXT = "#F3F1EE"; MUTED = "#9A928A"; LEAD = "rgba(255,255,255,.4)"
RUS = (70, 60, 1460, 760)   # рамка всей России в координатах build_map (1600×900)
# телефон: Калининград и край Чукотки/Камчатки за кадром — регионы поставок
# лежат между Кубанью и Амуром, так карта на 25% крупнее
RUS_M = (95, 60, 1170, 740)
FULL = RUS


def tw(text, size, weight=600):
    """Ширина строки Montserrat (оценка, кириллица чуть шире латиницы)."""
    return len(text) * size * (.64 if weight >= 700 else .61)


def build(fn, W, size, r, labels, bottom, view=RUS):
    RUS = view
    k = W / RUS[2]
    H = math.ceil(RUS[3] * k + bottom)     # дробная высота даёт белую полоску снизу PNG
    P = lambda nm: ((PIN[nm][0] - RUS[0]) * k, (PIN[nm][1] - RUS[1]) * k)
    tr = f'translate({-RUS[0] * k:.2f} {-RUS[1] * k:.2f}) scale({k:.5f})'
    ns = 'vector-effect="non-scaling-stroke" stroke-linejoin="round"'
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="Montserrat,Arial,sans-serif">',
         f'<defs><filter id="glow" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="{2.2 / k:.2f}"/></filter></defs>',
         f'<rect width="{W}" height="{H}" fill="{BG}"/>', f'<g transform="{tr}">']
    hil = []
    for nm, rr, t in all_regions:
        for ring in rr:
            if t: hil.append(path(ring))
            else: o.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width=".6" {ns}/>')
    d = "".join(hil)
    o.append(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-opacity=".6" stroke-width="{3.2 / k:.2f}" filter="url(#glow)"/>')
    o.append(f'<path d="{d}" fill="{HIL}" stroke="{ORANGE}" stroke-width="{1.3 if W < 500 else 1.6}" {ns}/>')
    o.append('</g>')
    if view != FULL:   # карта кадрирована — края растворяются в фоне, а не обрезаны
        o.append(f'<linearGradient id="fade"><stop offset="0" stop-color="{BG}"/><stop offset=".04" stop-color="{BG}" stop-opacity="0"/>'
                 f'<stop offset=".9" stop-color="{BG}" stop-opacity="0"/><stop offset="1" stop-color="{BG}"/></linearGradient>')
        o.append(f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')

    # подписи: имя → (x, y, выравнивание, текст[, подстрока]); выноска — от точки
    # к ближайшей точке прямоугольника подписи
    placed = []
    for nm, (x, y, anc, text, *sub) in labels.items():
        off = nm == OFFICE
        w = max([tw(text, size, 700 if off else 600)] + [tw(s, size - 1) for s in sub])
        x0 = {"start": x, "end": x - w, "middle": x - w / 2}[anc]
        top, bot = y - size * .8, y + ((size + 2) * len(sub) if sub else size * .25)
        placed.append((nm, *P(nm), x0, w, y, top, bot, text, sub, off))
    for nm, px, py, x0, w, y, top, bot, *_ in placed:
        qx = min(max(px, x0 - 3), x0 + w + 3); qy = min(max(py, top - 3), bot + 3)
        dist = math.hypot(qx - px, qy - py); gap = r * (2.1 if nm == OFFICE else 1.5)
        if dist > gap + 3:
            sx, sy = px + (qx - px) * gap / dist, py + (qy - py) * gap / dist
            o.append(f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{qx:.1f}" y2="{qy:.1f}" stroke="{LEAD}" stroke-width="1"/>')
    for nm in labels:
        px, py = P(nm)
        if nm == OFFICE:
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * 1.8:.1f}" fill="{BG}" stroke="#fff" stroke-width="{r * .42:.1f}"/><circle cx="{px:.1f}" cy="{py:.1f}" r="{r * .72:.1f}" fill="#fff"/>')
        else:
            o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{r * 2:.1f}" fill="{ORANGE}" fill-opacity=".2"/><circle cx="{px:.1f}" cy="{py:.1f}" r="{r:.1f}" fill="{ORANGE}"/>')
    halo = f'stroke="{BG}" stroke-width="{size * .34:.1f}" stroke-linejoin="round" paint-order="stroke"'
    for nm, px, py, x0, w, y, top, bot, text, sub, off in placed:
        assert x0 >= 2 and x0 + w <= W - 2, f'{nm}: подпись вылезла за край ({x0:.0f}…{x0 + w:.0f} из {W})'
        o.append(f'<text x="{x0:.1f}" y="{y:.1f}" fill="{"#fff" if off else TXT}" font-size="{size}" font-weight="{700 if off else 600}" {halo}>{text}</text>')
        for i, s in enumerate(sub):
            o.append(f'<text x="{x0:.1f}" y="{y + (size + 2) * (i + 1):.1f}" fill="{MUTED}" font-size="{size - 1}" font-weight="500" {halo}>{s}</text>')
    o.append('</svg>')
    io.open(os.path.join(here, fn), 'w', encoding='utf-8').write('\n'.join(o))
    print('wrote', fn, W, '×', H)


# Раскладка подписей, координаты — px холста. Точки (телефон / планшет):
# Ростов 29,141 / 57,222 · Краснодар 13,145 / 32,228 · Ставрополь 22,158 / 47,248
# Омск 149,169 / 247,266 · Новосибирск 167,180 / 276,284 · Барнаул 172,198 / 283,312
# Томск 180,164 / 295,258 · Кемерово 190,189 / 312,298 · Красноярск 222,129 / 362,203
# Амур 327,182 / 527,286
MOBILE = {
    "Краснодарский край":    (4, 106, "start", "Краснодарский край"),
    "Ростовская область":    (40, 123, "start", "Ростовская обл."),
    "Ставропольский край":   (4, 186, "start", "Ставропольский край"),
    "Омская область":        (134, 150, "end", "Омская обл."),
    "Томская область":       (190, 122, "middle", "Томская обл."),
    "Красноярский край":     (230, 133, "start", "Красноярский край"),
    "Новосибирская область": (152, 224, "end", "Новосибирская обл."),
    "Алтайский край":        (172, 241, "middle", "Алтайский край", "офис · Барнаул"),
    "Кемеровская область":   (202, 224, "start", "Кемеровская обл."),
    "Амурская область":      (354, 160, "end", "Амурская обл."),
}
TABLET = {
    "Краснодарский край":    (6, 192, "start", "Краснодарский край"),
    "Ростовская область":    (74, 214, "start", "Ростовская обл."),
    "Ставропольский край":   (6, 286, "start", "Ставропольский край"),
    "Омская область":        (234, 244, "end", "Омская обл."),
    "Томская область":       (302, 228, "middle", "Томская обл."),
    "Красноярский край":     (376, 207, "start", "Красноярский край"),
    "Новосибирская область": (250, 334, "end", "Новосибирская обл."),
    "Алтайский край":        (283, 362, "middle", "Алтайский край", "офис · Барнаул"),
    "Кемеровская область":   (324, 336, "start", "Кемеровская обл."),
    "Амурская область":      (527, 320, "middle", "Амурская обл."),
}

if __name__ == '__main__':
    build('map_mobile_v3.svg', 358, 9.5, 2.8, MOBILE, 36, RUS_M)
    build('map_tablet_v3.svg', 704, 11, 4, TABLET, 18)
