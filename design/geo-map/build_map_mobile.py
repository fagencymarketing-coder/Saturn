# -*- coding: utf-8 -*-
"""Карта для телефона — вся Россия, как на ПК, без обрезки.

Подписи на телефоне не помещаются у каждой точки, поэтому регионы собраны
в три группы — Юг России, Сибирь, Дальний Восток — и подписаны строкой
под силуэтом страны. От каждой группы к её точкам идёт тонкая выноска.
Офис подписан прямо у точки. Геометрия и точки — из build_map.py.
"""
import io, os, runpy, contextlib
os.environ['MAP_SITE'] = '1'; os.environ['MAP_NOLABELS'] = '1'
here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(here, 'build_map.py'))
PIN, all_regions, path = g['PIN'], g['all_regions'], g['path']
TARGETS, OFFICE = g['TARGETS'], g['OFFICE']

VX, VY, VW, VH = 70, 55, 1460, 1265        # 1460 ед. = 350px на экране 390
FH, FI = 50, 42                              # заголовок группы ≈12px, строки ≈10px
BG = "#141210"; LAND = "#211C18"; LANDS = "rgba(255,255,255,.07)"
HIL = "#3A2A20"; HILS = "rgba(255,66,0,.9)"; ORANGE = "#FF4200"
TXT = "#B5B0AA"; LEAD = "rgba(255,255,255,.28)"
ROW = 925                                    # базовая линия заголовков групп

GROUPS = [   # заголовок, x колонки, выравнивание, точка-источник выноски, строки
 ("Юг России", 95, "start", "Ставропольский край",
  ["Ростовская обл.", "Краснодарский край", "Ставропольский край"]),
 ("Сибирь", 610, "start", "Алтайский край",
  ["Алтайский край", "Новосибирская обл.", "Омская обл.", "Томская обл.", "Кемеровская обл.", "Красноярский край"]),
 ("Дальний Восток", 1505, "end", "Амурская область",
  ["Амурская обл."]),
]

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{VW}" height="{VH}" viewBox="{VX} {VY} {VW} {VH}" font-family="Montserrat,Arial,sans-serif">',
       f'<rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="{BG}"/>']
for nm, rr, t in all_regions:
    if not t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width="1" stroke-linejoin="round"/>')
for nm, rr, t in all_regions:
    if t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{HIL}" stroke="{HILS}" stroke-width="3" stroke-linejoin="round"/>')
for title, x, anc, src, _ in GROUPS:          # выноски: от точки к заголовку группы
    px, py = PIN[src]; top = ROW - FH - 18
    ex = x + (14 if anc == "start" else -14)
    svg.append(f'<polyline points="{px:.0f},{py:.0f} {ex},{top - 40} {ex},{top}" fill="none" stroke="{LEAD}" stroke-width="2"/>')
for nm in TARGETS:                             # точки
    px, py = PIN[nm]
    if nm == OFFICE:
        svg.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="21" fill="{BG}" stroke="#fff" stroke-width="4"/><circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="#fff"/>')
    else:
        svg.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="13" fill="none" stroke="{ORANGE}" stroke-opacity=".22" stroke-width="12"/><circle cx="{px:.0f}" cy="{py:.0f}" r="13" fill="{ORANGE}"/>')
ox, oy = PIN[OFFICE]                           # офис — подпись у самой точки
svg.append(f'<text x="{ox + 34:.0f}" y="{oy + 62:.0f}" fill="#fff" font-size="{FI}" font-weight="600" stroke="{BG}" stroke-width="8" paint-order="stroke">Барнаул</text>')
for title, x, anc, src, items in GROUPS:       # группы под картой
    svg.append(f'<text x="{x}" y="{ROW}" fill="#fff" font-size="{FH}" font-weight="600" text-anchor="{anc}">{title}</text>')
    for i, it in enumerate(items):
        svg.append(f'<text x="{x}" y="{ROW + 70 + i * 56}" fill="{TXT}" font-size="{FI}" font-weight="500" text-anchor="{anc}">{it}</text>')
svg.append('</svg>')
io.open(os.path.join(here, 'map_mobile_labels.svg'), 'w', encoding='utf-8').write('\n'.join(svg))
