# -*- coding: utf-8 -*-
"""catalog-data.json для макета каталога (Claude Design).

Те же 112 позиций и поля, что в site_catalog.csv, плюс «yield» —
короткая урожайность для карточки сорта/гибрида вместо «Запросить цену».
Правило: «до <потенциал или максимум> ц/га»; у Новосёла — диапазон как в
данных оригинатора; т/га переводим в ц/га (×10). Нет цифр — поле пустое.
"""
import csv, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(HERE, 'site_catalog.csv'), encoding='utf-8-sig'), delimiter=';'))
tech = {r['Название']: r for r in csv.DictReader(open(os.path.join(HERE, 'seeds_tech.csv'), encoding='utf-8-sig'), delimiter=';')}

NUM = r'(\d+(?:,\d+)?)'

def short_yield(s):
    s = (s or '').strip()
    if not s:
        return ''
    t_ha = 'т/га' in s
    m = re.match(NUM + r'–' + NUM + r' ц/га', s)
    if m and 'средняя' not in s:                       # «12,5–15 ц/га (+11% …)»
        return f'{m.group(1)}–{m.group(2)} ц/га'
    for key in (r'потенциал\w*\s*(?:до\s*)?', r'максимальная\s*(?:по ГСИ\s*)?'):
        m = re.search(key + NUM, s)
        if m:
            v = m.group(1)
            if t_ha:
                v = f'{float(v.replace(",", ".")) * 10:g}'.replace('.', ',')
            return f'до {v} ц/га'
    return ''

MAP = {'n': '№', 'sec': 'Раздел', 'sub': 'Подраздел', 'name': 'Название', 'brand': 'Бренд',
       'sig': 'Подпись в карточке', 'crops': 'Культуры (фильтр)', 'price': 'Цена', 'pack': 'Фасовка', 'photo': 'Фото'}
out = []
for r in rows:
    a = {k: (int(r[c]) if k == 'n' else r[c]) for k, c in MAP.items()}
    a['src'] = 'assets/foto/' + r['Фото'].replace(' — ', ' - ').replace('«', '"').replace('»', '"') if r['Фото'] else ''  # в архиве макета тире в именах заменено дефисом
    a['yield'] = short_yield(tech[r['Название']]['Урожайность']) if r['Раздел'] == 'Семена' and r['Название'] in tech else ''
    out.append(a)
json.dump(out, open(os.path.join(HERE, 'catalog-data.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
seeds = [a for a in out if a['sec'] == 'Семена']
print(f"позиций: {len(out)} · сортов с урожайностью: {sum(bool(a['yield']) for a in seeds)}/{len(seeds)}")
for a in seeds:
    print(f"  {a['name']}: {a['yield'] or '—'}")
