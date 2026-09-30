# -*- coding: utf-8 -*-
"""Карта для телефона и планшета: чистый силуэт без подписей.

Подписи на такой ширине нечитаемы, поэтому названия регионов выводит вёрстка —
текстом сайта, а не пикселями. Картинка держит только силуэт страны, выделенные
регионы и офис; точки крупнее десктопных, иначе на 390px их не видно.
"""
import io, os, runpy, contextlib

os.environ['MAP_SITE'] = '1'; os.environ['MAP_NOLABELS'] = '1'
here = os.path.dirname(os.path.abspath(__file__))
with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(os.path.join(here, 'build_map.py'))
PIN, all_regions, path = g['PIN'], g['all_regions'], g['path']
TARGETS, OFFICE = g['TARGETS'], g['OFFICE']

VX, VY, VW, VH = 60, 40, 1480, 830
BG = "#141210"; LAND = "#211C18"; LANDS = "rgba(255,255,255,.07)"
HIL = "#3A2A20"; HILS = "rgba(255,66,0,.9)"; ORANGE = "#FF4200"

svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{VW}" height="{VH}" '
       f'viewBox="{VX} {VY} {VW} {VH}" font-family="Montserrat,Arial,sans-serif">',
       f'<rect x="{VX}" y="{VY}" width="{VW}" height="{VH}" fill="{BG}"/>']
for nm, rr, t in all_regions:
    if not t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{LAND}" stroke="{LANDS}" stroke-width="1" stroke-linejoin="round"/>')
for nm, rr, t in all_regions:
    if t:
        for ring in rr: svg.append(f'<path d="{path(ring)}" fill="{HIL}" stroke="{HILS}" stroke-width="3" stroke-linejoin="round"/>')
for nm in TARGETS:
    px, py = PIN[nm]
    if nm == OFFICE:
        svg.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="16" fill="{BG}" stroke="#fff" stroke-width="3.4"/><circle cx="{px:.0f}" cy="{py:.0f}" r="6" fill="#fff"/>')
    else:
        svg.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="10" fill="none" stroke="{ORANGE}" stroke-opacity=".20" stroke-width="9"/><circle cx="{px:.0f}" cy="{py:.0f}" r="10" fill="{ORANGE}"/>')
svg.append('</svg>')
io.open(os.path.join(here, 'map_mobile_clean.svg'), 'w', encoding='utf-8').write('\n'.join(svg))
print('ok')
