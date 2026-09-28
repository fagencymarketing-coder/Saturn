# -*- coding: utf-8 -*-
"""Приведение логотипов партнёров к одной оптической высоте.

Логотипы нельзя выравнивать по габаритам файла: у «Фертики» сверху корона,
у «Реликта» знак — залитый квадрат выше букв. Если поставить их одной высоты
по рамке, «Реликт» задавит соседей, а «Фертика» окажется мелкой.

Выравниваем по высоте прописных букв словесной части. Для этого в каждом
логотипе задана полоса, где заведомо есть только буквы, по ней меряется
высота, считается масштаб — и все три кладутся на холст одной высоты,
выровненные по середине словесной части. Знак при этом свободно выступает.

После этого их можно ставить в вёрстку просто одной высотой.
"""
import os
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CAP = 56       # высота прописных букв в итоговом файле
# высота холста считается сама: столько, чтобы у всех трёх ничего не обрезалось

# доли ширины, внутри которых заведомо только буквы словесной части,
# и доли высоты, отсекающие вторую строку (у «Реликта» — ORGANICS)
PROBE = {
    'fertika':         (0.02, 0.14, 0.35, 1.00),
    'volsky':          (0.40, 0.58, 0.00, 0.70),
    'relict-organics': (0.40, 0.60, 0.00, 0.55),
}


def cap_height(img, box):
    a = np.array(img.getchannel('A')) > 40
    h, w = a.shape
    x0, x1, y0, y1 = box
    band = a[int(h * y0):int(h * y1), int(w * x0):int(w * x1)]
    rows = np.where(band.any(1))[0]
    if len(rows) == 0:
        raise SystemExit('пустая полоса замера')
    return rows.min() + int(h * y0), rows.max() + int(h * y0)


def main():
    scaled = {}
    for name, box in PROBE.items():
        img = Image.open(os.path.join(HERE, name + '.png')).convert('RGBA')
        top, bottom = cap_height(img, box)
        scale = CAP / (bottom - top + 1)
        new = img.resize((max(1, round(img.width * scale)),
                          max(1, round(img.height * scale))), Image.LANCZOS)
        scaled[name] = (new, (top + bottom) / 2 * scale, bottom - top + 1, scale)

    # холст должен вместить и то, что выше середины букв, и то, что ниже
    up = max(mid for _, mid, _, _ in scaled.values())
    down = max(im.height - mid for im, mid, _, _ in scaled.values())
    canvas_h = int(round(up + down))

    os.makedirs(os.path.join(HERE, 'row'), exist_ok=True)
    for name, (im, mid, cap, scale) in scaled.items():
        canvas = Image.new('RGBA', (im.width, canvas_h), (255, 255, 255, 0))
        canvas.alpha_composite(im, (0, int(round(up - mid))))
        canvas.save(os.path.join(HERE, 'row', name + '.png'))
        print('%-18s буквы %3dpx → масштаб %.2f → %d×%d'
              % (name, cap, scale, canvas.width, canvas.height))


if __name__ == '__main__':
    main()
