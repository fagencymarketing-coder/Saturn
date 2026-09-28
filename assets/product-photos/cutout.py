# -*- coding: utf-8 -*-
"""Вырезание упаковки с белого фона + приведение к единому виду.
Фон убирается заливкой ОТ КРАЁВ, а не по цвету: иначе белые мешки
«Фертика» продырявятся насквозь.
Результат: PNG с прозрачностью, квадрат 1200×1200, поле 8%.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

SIZE = 1200
MARGIN = 0.08
THRESH = 16          # допуск по цвету: низкий, чтобы не съедать белые мешки «Фертика»
FEATHER = 1.2        # смягчение края, px

def cutout(path, out):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    # рабочая копия для заливки
    work = im.copy()
    mark = (255, 0, 255)
    seeds = [(0,0), (w-1,0), (0,h-1), (w-1,h-1),
             (w//2,0), (w//2,h-1), (0,h//2), (w-1,h//2)]
    for s in seeds:
        if all(v > 225 for v in work.getpixel(s)):
            ImageDraw.floodfill(work, s, mark, thresh=THRESH)
    # альфа: прозрачно там, где маркер
    px = work.load()
    alpha = Image.new("L", (w, h), 255)
    ap = alpha.load()
    for y in range(h):
        for x in range(w):
            if px[x, y] == mark:
                ap[x, y] = 0
    alpha = alpha.filter(ImageFilter.GaussianBlur(FEATHER))
    rgba = im.convert("RGBA"); rgba.putalpha(alpha)
    # обрезка по содержимому
    bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox: rgba = rgba.crop(bbox)
    # вписать в квадрат с полем; мелкие исходники увеличиваем, но не более чем в 2,2 раза
    inner = int(SIZE * (1 - 2*MARGIN))
    k = min(inner / rgba.width, inner / rgba.height)
    k = min(k, 2.2)
    rgba = rgba.resize((max(1,int(rgba.width*k)), max(1,int(rgba.height*k))), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    canvas.paste(rgba, ((SIZE-rgba.width)//2, (SIZE-rgba.height)//2), rgba)
    canvas.save(out, "PNG", optimize=True)
    # доля непрозрачных пикселей — грубая проверка качества
    a = canvas.split()[3]
    filled = sum(a.histogram()[200:]) / (SIZE*SIZE)
    return round(filled, 3)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        name = os.path.basename(p).rsplit('.',1)[0].replace(' — упаковка','')
        out = f"assets/product-photos/_cutout/{name}.png"
        print(f"{cutout(p,out):.3f}  {out}")
