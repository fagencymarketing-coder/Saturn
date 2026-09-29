# -*- coding: utf-8 -*-
"""Вырезание упаковки с белого фона + приведение к единому виду.

Фон убирается заливкой ОТ КРАЁВ, а не по цвету: белые мешки «Фертика»
иначе продырявятся насквозь.

Порог заливки подбирается автоматически: пробуем мягкий и жёсткий.
Жёсткий берётся только если он убрал остатки фона (белые овалы-подставки
у «Волски Диформа»), но НЕ съел саму упаковку.
"""
import os, sys
from PIL import Image, ImageDraw, ImageFilter

SIZE, MARGIN, FEATHER = 1200, 0.08, 1.2
SOFT, HARD = 16, 48        # пороги заливки
KEEP = 0.70                # жёсткий принимаем, если осталось ≥70% площади

def _alpha(im, thresh):
    w, h = im.size
    work = im.copy(); mark = (255, 0, 255)
    seeds = [(0,0),(w-1,0),(0,h-1),(w-1,h-1),(w//2,0),(w//2,h-1),(0,h//2),(w-1,h//2)]
    for s in seeds:
        if all(v > 225 for v in work.getpixel(s)):
            ImageDraw.floodfill(work, s, mark, thresh=thresh)
    mask = work.convert("RGB").point(lambda v: v)     # noop, для читаемости
    px = work.load()
    a = Image.new("L", (w, h), 255); ap = a.load()
    for y in range(h):
        row = [px[x, y] == mark for x in range(w)]
        for x, is_bg in enumerate(row):
            if is_bg: ap[x, y] = 0
    return a

def native_alpha(path):
    """Прозрачность из самого файла, если она там есть.

    Белую канистру на белом фоне заливка от краёв различает плохо и
    выедает куски пластика. Поставщики часто отдают PNG уже с прозрачным
    фоном — тогда угадывать границы не нужно, берём их как есть.
    """
    src = Image.open(path)
    if src.mode not in ("RGBA", "LA", "P"):
        return None
    a = src.convert("RGBA").getchannel("A")
    return a if a.getextrema()[0] < 250 else None


def cutout(path, out):
    native = native_alpha(path)
    if native is not None:
        rgba = Image.open(path).convert("RGBA")
        return _place(rgba, native, out), "из файла"
    im = Image.open(path).convert("RGB")
    a_soft = _alpha(im, SOFT)
    s_soft = sum(a_soft.histogram()[128:])
    a_hard = _alpha(im, HARD)
    s_hard = sum(a_hard.histogram()[128:])
    # жёсткий порог принимаем, только если он не съел упаковку
    alpha = a_hard if (s_soft and s_hard / s_soft >= KEEP) else a_soft
    used = HARD if alpha is a_hard else SOFT

    alpha = alpha.filter(ImageFilter.GaussianBlur(FEATHER))
    rgba = im.convert("RGBA")
    return _place(rgba, alpha, out), used


def _place(rgba, alpha, out):
    """Обрезать по содержимому и положить в квадрат SIZE с полями MARGIN."""
    rgba.putalpha(alpha)
    bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
    if bbox: rgba = rgba.crop(bbox)
    inner = int(SIZE * (1 - 2*MARGIN))
    k = min(inner / rgba.width, inner / rgba.height, 2.2)
    rgba = rgba.resize((max(1,int(rgba.width*k)), max(1,int(rgba.height*k))), Image.LANCZOS)
    canvas = Image.new("RGBA", (SIZE, SIZE), (0,0,0,0))
    canvas.paste(rgba, ((SIZE-rgba.width)//2, (SIZE-rgba.height)//2), rgba)
    canvas.save(out, "PNG", optimize=True)
    fill = sum(canvas.split()[3].histogram()[200:]) / (SIZE*SIZE)
    return round(fill, 3)

if __name__ == "__main__":
    for p in sys.argv[1:]:
        name = os.path.basename(p).rsplit('.',1)[0].replace(' — упаковка','').replace('&#8212;','—')
        f, t = cutout(p, f"assets/product-photos/_cutout/{name}.png")
        print(f"{f:.3f}  {t if isinstance(t, str) else 'порог ' + str(t)}  {name}")
