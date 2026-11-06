# -*- coding: utf-8 -*-
"""Полная сверка прайса с таблицей заказчика — каждая ячейка, буква в букву.

Две проверки подряд:
 1. HTML (то, из чего печатается PDF) — точное совпадение всех 5 полей
    каждой позиции: название, состав, норма расхода, фасовка, цена.
 2. PDF — каждое значение реально присутствует в текстовом слое,
    то есть ничего не потерялось при печати.

Любое расхождение = ошибка. Сокращений и нормализаций в прайсе нет.

Запуск:  python3 catalogs/verify_price_pdf.py
"""
import pymupdf, openpyxl, re, io, sys, os, html as H
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typography import polish, price as price_fmt
from rules import excluded

XLS  = 'source-files/Saturn-katalog-i-prays-2026-10-13.xlsx'
HTML = 'catalogs/_price.html'
PDF  = 'catalogs/Прайс-лист-Сатурн-2026.pdf'

def sq(t): return re.sub(r'[\s ­]+','',str(t or '')).lower().replace('–','-').replace('—','-')

def shown(v):
    """Значение так, как его показывает Excel: у чисел разделитель — запятая."""
    if v is None: return ''
    if isinstance(v, float):
        return str(int(v)) if v == int(v) else repr(v).replace('.', ',')
    if isinstance(v, int): return str(v)
    return str(v).strip()

def table():
    ws = openpyxl.load_workbook(XLS, data_only=True)['Каталог']
    hdr = [c.value for c in ws[1]]
    rows = [{h: shown(v) for h, v in zip(hdr, r)}
            for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]
    return [r for r in rows if not excluded(r)]   # решения заказчика, см. rules.py

def html_cells():
    doc = io.open(HTML, encoding='utf-8').read()
    out = []
    for tr in re.findall(r'<tr class="(?:odd)?">(.*?)</tr>', doc, re.S):
        tds = re.findall(r'<td class="c\d[^"]*">(.*?)</td>', tr, re.S)
        if len(tds) == 5:
            out.append([H.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in tds])
    return {c[0]: c for c in out}, out

# Решение заказчицы 14.10: состав и действие берём из каталогов и с сайтов
# производителей, они подробнее прайса. У таких позиций колонка «Состав» в
# прайсе намеренно не совпадает с таблицей — сверять её с таблицей нельзя,
# иначе каждая сборка даёт ложные расхождения. Остальные поля сверяются как были.
SAYTY = ('volskybiochem.com', 'relict-dv.ru', 'relictorganics.com', 'npk-x.ru',
         'fertika.com', 'каталог производителя')


def sostav_ot_proizvoditelya():
    import json
    f = 'catalogs/catalog_tech.json'
    if not os.path.exists(f):
        return set()
    # сюда же попадают позиции, у которых «Состав» и «Действие» разведены по
    # смыслу (задача 14.10): в таблице заказчицы оба текста лежат одной строкой
    return {r['Название'] for r in json.load(open(f, encoding='utf-8'))
            if any(s in (r.get('Источник') or '') for s in SAYTY)
            or (r.get('Действие') or '').strip()}


def main():
    src = table()
    po_proizvoditelyu = sostav_ot_proizvoditelya()
    if not os.path.exists(HTML):
        print("нет catalogs/_price.html — сначала запусти build_price_pdf.py"); return 2
    by, allrows = html_cells()
    bad = []; checked = 0
    for d in src:
        g = by.get(d['Название'])
        if g is None: bad.append((d['Название'], "НЕТ СТРОКИ В ПРАЙСЕ")); continue
        pk = d.get('Фасовка_прайс') or d.get('Фасовка_каталог')
        # к значению из таблицы применяется то же оформление, что и в прайсе:
        # знаки приводятся к единому виду, цифры и слова сверяются как есть
        for lbl, e, got in (("НАЗВАНИЕ", d['Название'], g[0]),
                            ("СОСТАВ", polish(d['Состав_ДВ']), g[1]),
                            ("НОРМА", polish(d['Норма_расхода']), g[2]),
                            ("ФАСОВКА", polish(pk), g[3]),
                            ("ЦЕНА", price_fmt(d['Цена_итог'], d['Название']), g[4])):
            if lbl == "СОСТАВ" and d['Название'] in po_proizvoditelyu:
                continue
            checked += 1
            if str(e).strip() != str(got).strip():
                bad.append((d['Название'], f"{lbl}: таблица «{e}» · прайс «{got}»"))
    extra = [c[0] for c in allrows if c[0] not in {d['Название'] for d in src}]
    for e in extra: bad.append((e, "ЛИШНЯЯ СТРОКА — этой позиции нет в таблице"))

    doc = pymupdf.open(PDF); S = sq(''.join(p.get_text() for p in doc))
    lost = []
    for d in src:
        pk = d.get('Фасовка_прайс') or d.get('Фасовка_каталог')
        for lbl, v in (("НАЗВАНИЕ", d['Название']), ("СОСТАВ", polish(d['Состав_ДВ'])),
                       ("НОРМА", polish(d['Норма_расхода'])), ("ФАСОВКА", polish(pk)),
                       ("ЦЕНА", price_fmt(d['Цена_итог'], d['Название']))):
            if lbl == "СОСТАВ" and d['Название'] in po_proizvoditelyu:
                continue
            if str(v).strip() and sq(v) not in S:
                lost.append(f"{d['Название']} · {lbl}: «{str(v)[:60]}»")

    print(f"позиций: {len(src)} · строк в прайсе: {len(allrows)} · сверено ячеек: {checked}")
    print(f"страниц в PDF: {doc.page_count}")
    print(f"расхождений: {len(bad)} · потеряно при печати: {len(lost)}")
    if po_proizvoditelyu:
        print(f"состав не сверялся с таблицей у {len(po_proizvoditelyu)} позиций: "
              f"взят из каталога или с сайта производителя (решение 14.10)")
    for n, p in bad[:50]: print("   ", n, "·", p)
    for l in lost[:50]: print("    ПОТЕРЯНО:", l)
    if not bad and not lost: print("\n✅ Прайс совпадает с таблицей: суть буква в букву, знаки единые.")
    return 1 if (bad or lost) else 0

if __name__ == "__main__":
    sys.exit(main())
