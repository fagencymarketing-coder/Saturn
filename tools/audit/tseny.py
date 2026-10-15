# -*- coding: utf-8 -*-
"""Сверка цен живого магазина с прайсом заказчицы — по всем позициям.

Эталон: catalogs/catalog_tech.json (перенос из прайса 13.10 один в один).
Живое: API магазина Tilda, четыре раздела препаратов.

Запуск: python3 tools/audit/tseny.py
Выход: 0 — расхождений нет, 1 — есть (и они напечатаны).
"""
import json, os, re, ssl, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAZDELY = ['466293242973', '861744703283', '144241272913', '571551155283']
RECID = '4384406801'
CA = '/root/.ccr/ca-bundle.crt'


def число(s):
    s = str(s or '').replace(' ', '').replace(' ', '')
    if 'запрос' in s.lower():
        return None
    m = re.search(r'\d+[.,]?\d*', s)
    return float(m.group().replace(',', '.')) if m else None


def живые():
    ctx = ssl.create_default_context(cafile=CA) if os.path.exists(CA) else None
    out = {}
    for uid in RAZDELY:
        url = ('https://store.tildacdn.com/api/getproductslist/'
               f'?storepartuid={uid}&recid={RECID}&c=1&slice=1&size=300')
        d = json.load(urllib.request.urlopen(url, context=ctx, timeout=60))
        for p in d.get('products', []):
            out[p['title']] = p
    return out


def main():
    прайс = {r['Название']: r for r in json.load(
        open(os.path.join(ROOT, 'catalogs', 'catalog_tech.json'), encoding='utf-8'))}
    сайт = живые()
    расхождения, лишние = [], []
    for имя, p in сайт.items():
        t = прайс.get(имя)
        if not t:
            лишние.append(имя)
            continue
        a, b = число(p.get('price')), число(t['Цена_итог'])
        if (a is None) != (b is None) or (a and b and abs(a - b) > 0.001):
            расхождения.append((имя, a, b))
    нет_на_сайте = [n for n in прайс if n not in сайт]

    print(f'на сайте {len(сайт)} позиций · в прайсе {len(прайс)}')
    print(f'расхождений цены: {len(расхождения)}')
    for имя, a, b in расхождения:
        print(f'   {имя}: на сайте {a}, в прайсе {b}')
    if лишние:
        print(f'есть на сайте, нет в прайсе: {", ".join(лишние)}')
    if нет_на_сайте:
        print(f'есть в прайсе, нет на сайте: {", ".join(нет_на_сайте)}')
    плохо = расхождения or лишние or нет_на_сайте
    print('❌ требует правки' if плохо else '✅ цены сайта совпадают с прайсом')
    return 1 if плохо else 0


if __name__ == '__main__':
    sys.exit(main())
