# -*- coding: utf-8 -*-
"""Извлечение фирменных логотипов производителей из каталогов, присланных заказчиком.

Логотипы в этих PDF векторные, поэтому рендерим область с большим разрешением
и получаем оригинальные цвета и форму — никакой перерисовки «по памяти».
Фон снимается заливкой от краёв, как в assets/product-photos/cutout.py.

Источники: source-files/ (каталоги партнёров, сентябрь 2026).
"""
import os
from collections import deque
import pymupdf
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, 'assets', 'partner-logos')
DPI = 600

# файл, страница (с нуля), область в пунктах, имя результата, допуск заливки.
# Допуск подбирается по фону: у «Фертики» и «Волски» он белый, у «Реликта» —
# зелёный градиент, по нему заливка идёт только с бо́льшим допуском.
JOBS = [
    ('Katalog-Fertika-ProLine.pdf', 0, (372, 44, 566, 106), 'fertika', 14),
    ('Buklet-Volski-Biokhim.pdf',  31, (205, 615, 415, 675), 'volsky', 14),
    ('Katalog-Genezis-NEW-2026.pdf', 0, (205, 32, 314, 88), 'relict-organics', 20),
]

PAD = 0.06        # поле вокруг логотипа, доля от большей стороны


def drop_background(img, tol):
    """Заливка от краёв: всё, что связано с краем и близко к его цвету, — прозрачное."""
    img = img.convert('RGBA')
    w, h = img.size
    px = img.load()
    seeds = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1),
             (w // 2, 0), (w // 2, h - 1), (0, h // 2), (w - 1, h // 2)]
    seen = bytearray(w * h)
    q = deque()
    for x, y in seeds:
        if not seen[y * w + x]:
            seen[y * w + x] = 1
            q.append((x, y, px[x, y][:3]))
    while q:
        x, y, ref = q.popleft()
        px[x, y] = (255, 255, 255, 0)
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                c = px[nx, ny][:3]
                # сравниваем с соседом, а не с первым пикселем: так берётся градиент
                if max(abs(c[i] - ref[i]) for i in range(3)) <= tol:
                    seen[ny * w + nx] = 1
                    q.append((nx, ny, c))
    return img


def drop_gradient_background(img, tol, probe=10):
    """Фон-градиент: эталон берётся по каждому столбцу из верхних строк кадра.

    Заливка от краёв на градиенте не работает — она либо не доходит до
    середины, либо перепрыгивает в сам знак. Здесь фон вычитается: пиксель
    прозрачен, если он близок к цвету фона в своём столбце.
    """
    img = img.convert('RGBA')
    w, h = img.size
    px = img.load()
    for x in range(w):
        col = sorted(px[x, y][:3] for y in range(probe))
        ref = col[len(col) // 2]
        for y in range(h):
            c = px[x, y]
            if max(abs(c[i] - ref[i]) for i in range(3)) <= tol:
                px[x, y] = (255, 255, 255, 0)
    return img


def main():
    for fname, page, rect, name, tol in JOBS:
        doc = pymupdf.open(os.path.join(ROOT, 'source-files', fname))
        pix = doc[page].get_pixmap(dpi=DPI, clip=pymupdf.Rect(*rect))
        img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
        img = (drop_gradient_background(img, tol) if name == 'relict-organics'
               else drop_background(img, tol))
        bbox = img.getchannel('A').getbbox()
        if bbox:
            img = img.crop(bbox)
        pad = int(max(img.size) * PAD)
        canvas = Image.new('RGBA', (img.width + pad * 2, img.height + pad * 2), (255, 255, 255, 0))
        canvas.paste(img, (pad, pad), img)
        canvas.save(os.path.join(OUT, name + '.png'))
        print('%-18s %4d×%-4d' % (name, canvas.width, canvas.height))


if __name__ == '__main__':
    main()
