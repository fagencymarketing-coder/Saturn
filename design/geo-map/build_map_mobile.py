# -*- coding: utf-8 -*-
"""Карта для телефона: подписи регионов прямо на карте.

Берёт геометрию из build_map.py (выполняет его как модуль без записи файлов),
обрезает до зоны поставок и расставляет подписи вручную, крупным кеглем:
на экране 390px шрифт получается ~12px. Сибирский кластер разводится
выносками на пустую территорию вокруг.
"""
import io, os, runpy, contextlib
os.environ['MAP_SITE'] = '1'; os.environ['MAP_NOLABELS'] = '1'
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(os.path.dirname(__file__), 'build_map.py'))
PIN, all_regions, path = g['PIN'], g['all_regions'], g['path']
TARGETS, OFFICE, LABEL = g['TARGETS'], g['OFFICE'], g['LABEL']

VX, VY, VW, VH = 50, 300, 1250, 610          # видимая область, единицы карты
FS = 30                                        # ≈10px при ширине 390 — тише, аккуратнее
BG = "#141210"; LAND = "#211C18"; LANDS = "rgba(255,255,255,.07)"
HIL = "#3A2A20"; HILS = "rgba(255,66,0,.9)"; ORANGE = "#FF4200"; TXT = "#D9D4CE"; LEAD = "rgba(255,255,255,.35)"

# подпись: x, y, выравнивание, [точка излома выноски]
LAB = {
 "Ростовская область":   (215, 400, "start", None),
 "Краснодарский край":   (70, 700, "start", (70, 610)),
 "Ставропольский край":  (70, 750, "start", (110, 690)),
 "Омская область":       (548, 548, "end",   None),
 "Томская область":      (690, 458, "end",   None),
 "Новосибирская область":(560, 810, "end",   (600, 770)),
 "Алтайский край":       (657, 880, "middle", None),
 "Кемеровская область":  (870, 810, "start", (760, 770)),
 "Красноярский край":    (870, 400, "start", None),
 "Амурская область":     (1150, 575, "middle", None),
}

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{VW}" height="{VH}" viewBox="{VX} {VY} {VW} {VH}" font-family="Montserrat,Arial,sans-serif">',
       f'<rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="{BG}"/>']
for nm, rr, t in all_regions:
    if not t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width="0.8"/>')
for nm, rr, t in all_regions:
    if t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{HIL}" stroke="{HILS}" stroke-width="2.2"/>')
for nm in TARGETS:                                   # выноски
    px, py = PIN[nm]; lx, ly, anc, knee = LAB[nm]
    tx = lx + (8 if anc == "end" else -8 if anc == "start" else 0)
    ty = ly - FS * 0.35 if anc != "middle" else ly - FS
    pts = [(px, py)] + ([knee] if knee else []) + [(tx, ty)]
    if ((px - tx) ** 2 + (py - ty) ** 2) ** .5 > 30:
        svg.append('<polyline points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts) + f'" fill="none" stroke="{LEAD}" stroke-width="1.6"/>')
for nm in TARGETS:                                   # пины
    px, py = PIN[nm]
    if nm == OFFICE:
        svg.append(f'<circle cx="{px}" cy="{py}" r="15" fill="none" stroke="#fff" stroke-width="3"/><circle cx="{px}" cy="{py}" r="6" fill="#fff"/>')
    else:
        svg.append(f'<circle cx="{px}" cy="{py}" r="9" fill="{ORANGE}" stroke="{BG}" stroke-width="3"/>')
for nm in TARGETS:                                   # подписи с тёмной обводкой — читаются поверх контуров
    lx, ly, anc, _ = LAB[nm]
    w = 600 if nm == OFFICE else 500
    svg.append(f'<text x="{lx}" y="{ly}" font-size="{FS}" font-weight="{w}" fill="{"#fff" if nm == OFFICE else TXT}" '
               f'text-anchor="{anc}" stroke="{BG}" stroke-width="7" paint-order="stroke" stroke-linejoin="round">{LABEL[nm]}</text>')
svg.append('</svg>')
io.open(os.path.join(os.path.dirname(__file__), 'map_mobile_labels.svg'), 'w', encoding='utf-8').write('\n'.join(svg))
print('ok')
