# -*- coding: utf-8 -*-
"""Затирка актов производственной проверки.

Плашки ставятся по реальным рамкам слов (OCR), а не по строке целиком —
страницы отсканированы с небольшим перекосом, и правая колонка ниже левой.
Закрываем: название и адрес хозяйства, ФИО и подписи со стороны хозяйства,
печать хозяйства, строку хозяйства в блоке ЭДО.
Номер и дата договора остаются открытыми (решение 27.10).
Печать закрываем целиком: в оттиске читаются название хозяйства и ИНН.
НЕ закрываем: культуру, сорт, «Генезис», препараты, нормы, урожайность,
экономику, А.Ц. Нилову, Боровикова и печать «Сатурна».
"""
from PIL import Image, ImageDraw
import os, re, ocr

BAR = (74, 78, 84)
PX, PY = 4, 4          # запас вокруг найденных слов

def norm(s):
    return re.sub(r'[«»"().,;:—–\-_]', '', s).lower()

def find(ws, tokens, xmin=0, xmax=10**6, nth=0):
    """Рамка вокруг подряд идущих слов, начинающихся на tokens."""
    toks = [norm(t) for t in tokens]
    hits = []
    for i in range(len(ws) - len(toks) + 1):
        seq = ws[i:i + len(toks)]
        if seq[0]['x'] < xmin or seq[0]['x'] > xmax:
            continue
        if all(norm(w['t']).startswith(t) for w, t in zip(seq, toks)):
            hits.append((min(w['x'] for w in seq) - PX,
                         min(w['y'] for w in seq) - PY,
                         max(w['x'] + w['w'] for w in seq) + PX,
                         max(w['y'] + w['h'] for w in seq) + PY))
    if not hits:
        raise SystemExit('НЕ НАЙДЕНО: %s' % ' '.join(tokens))
    return hits[nth]

def row(ws, anchor, x0, x1, xmin=0):
    """Полоса по вертикали якорного слова, от x0 до x1 (для мест, где OCR врёт)."""
    b = find(ws, [anchor], xmin=xmin)
    return (x0, b[1], x1, b[3])

# tokens = что закрыть; задаётся по распечатке OCR
PLAN = {
 '169.jpg': lambda w: [
   find(w, ['ООО', '«Приозерное»'], xmin=400, xmax=600),
   find(w, ['Зональный', 'район', 'с', 'Плешково']),
   find(w, ['Хабаров', 'Алексей', 'Алексеевич']),
   find(w, ['ООО', '«Приозерное»'], xmin=700),
   find(w, ['/Артемов', 'Э.В./']),
   find(w, ['000', '"ПРИОЗЕРНОЕ"', 'Макарова', 'Маргарита', 'Евгеньевна']),
   row(w, 'Эл.доверенность', 190, 700),
   row(w, '7108993', 920, 1215),
 ],
 '170.jpg': lambda w: [
   find(w, ['ООО', '«Блиновское»'], xmin=350, xmax=600),
   find(w, ['Заринский', 'район', 'с', 'Яново']),
   find(w, ['Салиев', 'Дмитрий', 'Сайгалиевич']),
   find(w, ['ООО', '«Блиновское»'], xmin=700),
   row(w, '/Близиюк', 935, 1180),
   row(w, 'БЛИЗНЮК', 190, 640),
   row(w, '02587491', 850, 1240),
 ],
 '171.jpg': lambda w: [
   find(w, ['АО', '«Победа»'], xmin=350, xmax=600),
   find(w, ['659056']),
   find(w, ['Шелаболихинский', 'район', 'с', 'Ильинка']),
   find(w, ['Панов', 'Александр']),
   find(w, ['АО', '«Победа»'], xmin=700),
   find(w, ['/Букреев', 'М.П./']),
   row(w, '"ПОБЕДА"', 190, 620),
   row(w, '0273594', 830, 1216),
 ],
 '172.jpg': lambda w: [
   find(w, ['СПК', '«Белокуриха»'], xmin=400, xmax=700),
   find(w, ['Алтайский', 'район', 'с', 'Старобелокуриха']),
   find(w, ['директор', 'Окс', 'Дмитрий', 'Александрович']),
   find(w, ['СПК', '«Белокуриха»'], xmin=700),
   (640, 1420, 1140, 1760),      # печать, подпись и ФИО хозяйства
 ],
 '173.jpg': lambda w: [
   find(w, ['ООО', '«Агрофирма', 'Гудвилл»'], xmin=300, xmax=700),
   find(w, ['Советский', 'район', 'с', 'Советское']),
   find(w, ['Попов', 'Александр', 'Сергеевич']),
   find(w, ['ООО', '«Агрофирма', 'Гудвилл»'], xmin=700),
   (730, 1392, 1200, 1670),      # печать, подпись и ФИО хозяйства
 ],
}

def run(src='orig', out='out'):
    os.makedirs(out, exist_ok=True)
    for name, plan in sorted(PLAN.items()):
        ws = ocr.words(os.path.join(src, name))
        im = Image.open(os.path.join(src, name)).convert('RGB')
        d = ImageDraw.Draw(im)
        rects = plan(ws)
        for r in rects:
            d.rectangle(r, fill=BAR)
        im.save(os.path.join(out, name.replace('.jpg', '.png')))
        print(name, len(rects), 'плашек')

if __name__ == '__main__':
    run()
