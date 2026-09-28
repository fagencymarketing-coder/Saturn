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

XLS  = 'source-files/Saturn-katalog-i-prays-podtverzhdyon-2026-09-28.xlsx'
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
    return [{h: shown(v) for h, v in zip(hdr, r)}
            for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]

def html_cells():
    doc = io.open(HTML, encoding='utf-8').read()
    out = []
    for tr in re.findall(r'<tr class="(?:odd)?">(.*?)</tr>', doc, re.S):
        tds = re.findall(r'<td class="c\d[^"]*">(.*?)</td>', tr, re.S)
        if len(tds) == 5:
            out.append([H.unescape(re.sub(r'<[^>]+>', '', c)).strip() for c in tds])
    return {c[0]: c for c in out}, out

def main():
    src = table()
    if not os.path.exists(HTML):
        print("нет catalogs/_price.html — сначала запусти build_price_pdf.py"); return 2
    by, allrows = html_cells()
    bad = []; checked = 0
    for d in src:
        g = by.get(d['Название'])
        if g is None: bad.append((d['Название'], "НЕТ СТРОКИ В ПРАЙСЕ")); continue
        pk = d.get('Фасовка_прайс') or d.get('Фасовка_каталог')
        for lbl, e, got in (("НАЗВАНИЕ", d['Название'], g[0]), ("СОСТАВ", d['Состав_ДВ'], g[1]),
                            ("НОРМА", d['Норма_расхода'], g[2]), ("ФАСОВКА", pk, g[3]),
                            ("ЦЕНА", d['Цена_итог'], g[4])):
            checked += 1
            if str(e).strip() != str(got).strip():
                bad.append((d['Название'], f"{lbl}: таблица «{e}» · прайс «{got}»"))
    extra = [c[0] for c in allrows if c[0] not in {d['Название'] for d in src}]
    for e in extra: bad.append((e, "ЛИШНЯЯ СТРОКА — этой позиции нет в таблице"))

    doc = pymupdf.open(PDF); S = sq(''.join(p.get_text() for p in doc))
    lost = []
    for d in src:
        pk = d.get('Фасовка_прайс') or d.get('Фасовка_каталог')
        for lbl, v in (("НАЗВАНИЕ", d['Название']), ("СОСТАВ", d['Состав_ДВ']),
                       ("НОРМА", d['Норма_расхода']), ("ФАСОВКА", pk), ("ЦЕНА", d['Цена_итог'])):
            if str(v).strip() and sq(v) not in S:
                lost.append(f"{d['Название']} · {lbl}: «{str(v)[:60]}»")

    print(f"позиций: {len(src)} · строк в прайсе: {len(allrows)} · сверено ячеек: {checked}")
    print(f"страниц в PDF: {doc.page_count}")
    print(f"расхождений: {len(bad)} · потеряно при печати: {len(lost)}")
    for n, p in bad[:50]: print("   ", n, "·", p)
    for l in lost[:50]: print("    ПОТЕРЯНО:", l)
    if not bad and not lost: print("\n✅ Прайс совпадает с таблицей буква в букву.")
    return 1 if (bad or lost) else 0

if __name__ == "__main__":
    sys.exit(main())
