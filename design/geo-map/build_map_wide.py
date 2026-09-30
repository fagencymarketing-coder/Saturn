# -*- coding: utf-8 -*-
"""Карта географии для сайта: обрезана по зоне поставок, подписи на самой карте.

Полная карта России наполовину пустая: Арктика, Чукотка, Камчатка — регионов
поставки там нет. Здесь кадр обрезан до работающей области, за счёт этого
масштаб крупнее, а подписи стоят прямо на карте, а не списком под ней.
Срезы краёв растушёваны в фон, чтобы обрез не читался как «обрубленная» картинка.
"""
import io, os, runpy, contextlib

os.environ['MAP_SITE'] = '1'; os.environ['MAP_NOLABELS'] = '1'
here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(here, 'build_map.py'))
PIN, all_regions, path = g['PIN'], g['all_regions'], g['path']
TARGETS, OFFICE, LABEL = g['TARGETS'], g['OFFICE'], g['LABEL']

VX, VY, VW, VH = 95, 330, 1235, 470      # кадр: от Краснодара до Амурской
FS = 19                                   # ≈19px при показе во всю ширину контейнера
FADE = 90                                 # растушёвка срезанных краёв
BG = "#141210"; LAND = "#211C18"; LANDS = "rgba(255,255,255,.07)"
HIL = "#3A2A20"; HILS = "rgba(255,66,0,.9)"; ORANGE = "#FF4200"
TXT = "#EDE9E4"; LEAD = "rgba(255,255,255,.35)"

# подпись: x, y, выравнивание, [излом выноски]
LAB = {
 "Ростовская область":   (252, 508, "start",  None),
 "Краснодарский край":   (252, 551, "start",  None),
 "Ставропольский край":  (252, 594, "start",  None),
 "Омская область":       (455, 645, "end",    None),
 "Новосибирская область":(455, 706, "end",    (520, 690)),
 "Алтайский край":       (610, 775, "middle", None),
 "Кемеровская область":  (800, 730, "start",  (760, 712)),
 "Томская область":      (700, 520, "middle", None),
 "Красноярский край":    (905, 415, "start",  None),
 "Амурская область":     (1105, 745, "middle", None),
}

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{VW}" height="{VH}" '
       f'viewBox="{VX} {VY} {VW} {VH}" font-family="Montserrat,Arial,sans-serif">',
       '<defs>'
       f'<linearGradient id="ft" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
       f'<linearGradient id="fb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
       f'<linearGradient id="fr" x1="1" y1="0" x2="0" y2="0"><stop offset="0" stop-color="{BG}"/><stop offset="1" stop-color="{BG}" stop-opacity="0"/></linearGradient>'
       '</defs>',
       f'<rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="{BG}"/>']
for nm, rr, t in all_regions:
    if not t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width="0.9" stroke-linejoin="round"/>')
for nm, rr, t in all_regions:
    if t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{HIL}" stroke="{HILS}" stroke-width="2.6" stroke-linejoin="round"/>')
# срезы краёв уводим в фон
svg.append(f'<rect x="{VX}" y="{VY}" width="{VW}" height="{FADE}" fill="url(#ft)"/>')
svg.append(f'<rect x="{VX}" y="{VY+VH-FADE}" width="{VW}" height="{FADE}" fill="url(#fb)"/>')
svg.append(f'<rect x="{VX+VW-FADE}" y="{VY}" width="{FADE}" height="{VH}" fill="url(#fr)"/>')

for nm in TARGETS:                                   # выноски
    px, py = PIN[nm]; lx, ly, anc, knee = LAB[nm]
    tx = lx + (10 if anc == "end" else -10 if anc == "start" else 0)
    ty = ly - FS * 0.34 if anc != "middle" else ly - FS
    pts = [(px, py)] + ([knee] if knee else []) + [(tx, ty)]
    if ((px - tx) ** 2 + (py - ty) ** 2) ** .5 > 34:
        svg.append('<polyline points="' + ' '.join(f'{x:.0f},{y:.0f}' for x, y in pts) + f'" fill="none" stroke="{LEAD}" stroke-width="1.6"/>')
for nm in TARGETS:                                   # точки
    px, py = PIN[nm]
    if nm == OFFICE:
        svg.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="13" fill="{BG}" stroke="#fff" stroke-width="2.6"/><circle cx="{px:.0f}" cy="{py:.0f}" r="5" fill="#fff"/>')
    else:
        svg.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="none" stroke="{ORANGE}" stroke-opacity=".22" stroke-width="8"/><circle cx="{px:.0f}" cy="{py:.0f}" r="8" fill="{ORANGE}"/>')
for nm in TARGETS:                                   # подписи с тёмной обводкой
    lx, ly, anc, _ = LAB[nm]
    w = 700 if nm == OFFICE else 600
    svg.append(f'<text x="{lx}" y="{ly}" font-size="{FS}" font-weight="{w}" fill="{"#fff" if nm == OFFICE else TXT}" '
               f'text-anchor="{anc}" stroke="{BG}" stroke-width="5" paint-order="stroke" stroke-linejoin="round">{LABEL[nm]}</text>')
svg.append('</svg>')
io.open(os.path.join(here, 'map_wide.svg'), 'w', encoding='utf-8').write('\n'.join(svg))
print('ok')
