# -*- coding: utf-8 -*-
"""Пересборка catalog_tech.json / .csv из подтверждённой таблицы заказчика.

Первоисточник — source-files/Saturn-katalog-i-prays-podtverzhdyon-2026-09-28.xlsx.
Данные переносятся дословно, с единственным правилом: числовая ячейка выводится
так, как её показывает Excel в русской локали (десятичный разделитель — запятая).
Без этого правила норма «Волски Аминатор» 0,5 превращалась в «0.5» с точкой.

Служебные колонки (фото, показ на главной и в каталоге) сохраняются из
существующего catalog_tech.json — они не приходят из таблицы.
"""
import csv, json, os
import openpyxl

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(ROOT, 'source-files',
                    'Saturn-katalog-i-prays-podtverzhdyon-2026-09-28.xlsx')
JSON = os.path.join(ROOT, 'catalogs', 'catalog_tech.json')
CSV  = os.path.join(ROOT, 'catalogs', 'catalog_tech.csv')

SERVICE = ['Файл_фото', 'Есть_фото', 'На_главной', 'В_каталоге', 'Файл_вырезанный']

# Категория, которой в таблице нет, но заказчик её подтвердил отдельно.
FIX_CATEGORY = {'Волски Аминатор': 'Листовые подкормки'}


def cell(c):
    """Значение ячейки так, как его видно в таблице."""
    v = c.value
    if v is None:
        return ''
    if isinstance(v, float):
        if v == int(v):
            return str(int(v))
        return repr(v).replace('.', ',')   # 0.5 -> «0,5», как показывает Excel
    if isinstance(v, int):
        return str(v)
    return str(v).strip()


ws = openpyxl.load_workbook(XLSX, data_only=True)['Каталог']
head = [c.value for c in ws[1]]
rows = []
for r in ws.iter_rows(min_row=2):
    if not r[0].value:
        continue
    d = {k: cell(c) for k, c in zip(head, r) if k}
    if not d.get('Категория') and d['Название'] in FIX_CATEGORY:
        d['Категория'] = FIX_CATEGORY[d['Название']]
    rows.append(d)

old = {r['Название']: r for r in json.load(open(JSON, encoding='utf-8'))}
for d in rows:
    prev = old.get(d['Название'], {})
    for k in SERVICE:
        d[k] = prev.get(k, '')

cols = [k for k in head if k] + SERVICE
json.dump(rows, open(JSON, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(CSV, 'w', encoding='utf-8-sig', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=';')
    w.writeheader()
    w.writerows(rows)

print('позиций: %d · колонок: %d' % (len(rows), len(cols)))
