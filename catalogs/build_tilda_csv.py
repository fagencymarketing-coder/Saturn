# -*- coding: utf-8 -*-
"""Файл импорта каталога в Tilda Store.

Источники: site_catalog.csv (112 позиций, порядок, подписи, культуры, фото),
catalog_tech.json и seeds_tech.csv (характеристики для карточки товара).

Формат Tilda: разделитель «;», цена — числом, фото — прямые https-ссылки
(Tilda сама скачивает их к себе при импорте), характеристики — колонки
«Characteristics:Название». Пустая характеристика в карточке не выводится.
"""
import csv, io, json, os, re, shutil, sys
from urllib.parse import quote
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typography import polish

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PHOTO_DIR = os.path.join(ROOT, 'assets', 'tilda-photos')
# ссылка на фото в момент импорта; репозиторий должен быть доступен без входа
PHOTO_BASE = os.environ.get('PHOTO_BASE',
    'https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/')

TR = dict(zip('абвгдеёжзийклмнопрстуфхцчшщъыьэюя',
              ['a','b','v','g','d','e','e','zh','z','i','y','k','l','m','n','o','p','r','s','t','u','f','h','ts','ch','sh','sch','','y','','e','yu','ya']))


def slug(name):
    s = ''.join(TR.get(c, c) for c in name.lower())
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')


def price_num(text):
    """Первое число цены: «от 700 ₽ (рассрочка 735 ₽)» → 700. «по запросу» → пусто."""
    m = re.search(r'\d[\d\s]*(?:,\d+)?', text or '')
    if not m or 'запрос' in (text or '').lower():
        return ''
    return m.group(0).replace(' ', '').replace(',', '.')


site = list(csv.DictReader(io.open(os.path.join(HERE, 'site_catalog.csv'), encoding='utf-8-sig'), delimiter=';'))
tech = {r['Название']: r for r in json.load(io.open(os.path.join(HERE, 'catalog_tech.json'), encoding='utf-8'))}
seeds = {r['Название']: r for r in csv.DictReader(io.open(os.path.join(HERE, 'seeds_tech.csv'), encoding='utf-8-sig'), delimiter=';')}

SZR = {'Гербициды', 'Фунгициды', 'Инсектициды', 'Протравители', 'Десиканты'}
CH = ['Культура', 'Состав', 'Действующее вещество', 'Действие', 'Спектр действия', 'Норма расхода',
      'Культуры и фазы', 'Фасовка', 'Физико-химические показатели',
      'Тип', 'Оригинатор', 'Спелость', 'Вегетационный период', 'Урожайность', 'Качество']
cols = ['SKU', 'External ID', 'Brand', 'Category', 'Title', 'Description', 'Text', 'Photo', 'Price'] + \
       ['Characteristics:' + c for c in CH]

# Tilda режет значение характеристики по «;» на отдельные значения.
# Для «Культуры» это нужно — иначе фильтр не увидит каждую культуру отдельно.
# Во всех остальных полях «;» внутри текста надо убрать, иначе характеристика
# разваливается на несколько одноимённых строк в карточке.
MULTI = {'Культура'}
# Tilda обрезает значение характеристики на 200 символах — молча, посреди слова
MAXLEN = 200

# «Все культуры» разворачивается в полный список: иначе такие товары выпадают
# из фильтра по конкретной культуре, хотя подходят под любую.
ALL_CROPS = ['Пшеница', 'Ячмень', 'Рапс', 'Подсолнечник', 'Соя', 'Кукуруза',
             'Горох', 'Гречиха', 'Лён', 'Свёкла', 'Картофель', 'Овощи']


def check_len(name, value, title=''):
    if value and len(value) > MAXLEN:
        raise SystemExit(
            f'Характеристика «{name}» у «{title}» длиннее {MAXLEN} символов '
            f'({len(value)}). Tilda обрежет её посреди слова — сократите текст.')
    return value


def fix_ch(name, value):
    if not value:
        return value
    if name in MULTI:
        items = [x.strip() for x in value.split(',') if x.strip()]
        out = []
        for x in items:
            out.extend(ALL_CROPS if x.lower() == 'все культуры' else [x])
        seen, uniq = set(), []
        for x in out:
            if x not in seen:
                seen.add(x); uniq.append(x)
        return ';'.join(uniq)
    return re.sub(r'\s*;\s*', ' · ', value)


os.makedirs(PHOTO_DIR, exist_ok=True)
out, seen = [], set()
for r in site:
    name, sub, sec = r['Название'], r['Подраздел'], r['Раздел']
    sku = slug(name)
    assert sku not in seen, f'дубль SKU: {sku}'; seen.add(sku)
    ch = {c: '' for c in CH}
    ch['Культура'] = r['Культуры (фильтр)']
    ch['Фасовка'] = r['Фасовка']
    text = ''
    if sec == 'Семена':
        s = seeds[name]
        text = s['Описание']
        ch.update({'Тип': r['Подпись в карточке'].split(' · ', 1)[-1], 'Оригинатор': '' if 'не указан' in s['Оригинатор'] else s['Оригинатор'],
                   'Спелость': s['Спелость'], 'Вегетационный период': s['Вегетация'],
                   'Урожайность': s['Урожайность'], 'Качество': s['Качество']})
    else:
        t = tech[name]
        cat = t['Категория']
        if cat in SZR:
            ch['Спектр действия'] = polish(t['Описание'])
            ch['Действующее вещество'] = polish(t['Состав_ДВ'])
            ch['Культуры и фазы'] = polish(t['Культуры_и_фазы'])
        elif cat.startswith('Адъюванты'):
            text = polish(t['Описание'])
            ch['Действие'] = polish(t['Состав_ДВ'])
        else:
            text = polish(t['Описание'])
            ch['Состав'] = polish(t['Состав_ДВ'])
            ch['Культуры и фазы'] = polish(t['Культуры_и_фазы'])
            ch['Физико-химические показатели'] = polish(t['Физпоказатели'])
        ch['Норма расхода'] = polish(t['Норма_расхода'])
    # фото — копия с латинским именем, чтобы ссылка была чистой
    photo = ''
    if r['Фото']:
        src = (os.path.join(ROOT, 'assets', 'product-photos', '_cutout', r['Фото'])
               if not r['Фото'].startswith('seed-') else os.path.join(ROOT, 'assets', 'crop-photos', 'cards', r['Фото']))
        ext = os.path.splitext(src)[1]
        shutil.copyfile(src, os.path.join(PHOTO_DIR, sku + ext))
        photo = PHOTO_BASE + quote(sku + ext)
    # Tilda хранит цену числом и теряет «от», «рассрочку», вторую фасовку.
    # Точная формулировка из таблицы — в тексте карточки, чтобы смысл не менялся.
    exact = r['Цена'] if price_num(r['Цена']) else ''
    out.append({'SKU': sku, 'External ID': sku, 'Brand': r['Бренд'],
                'Category': f'{sec};{sub}' if sec != sub else sec,
                'Title': name, 'Description': r['Подпись в карточке'],
                'Text': '<br><br>'.join(x for x in (text, f'Цена: {exact}. При 100% предоплате, доставка и хранение включены.' if exact else '') if x),
                'Photo': photo, 'Price': price_num(r['Цена']),
                **{'Characteristics:' + c: fix_ch(c, v) for c, v in ch.items()}})

# колонки, пустые у всех, Tilda советует убрать
cols = [c for c in cols if any(o[c] for o in out)]
dst = os.path.join(HERE, 'tilda-import.csv')
with io.open(dst, 'w', encoding='utf-8', newline='') as f:
    w = csv.DictWriter(f, fieldnames=cols, delimiter=';', quoting=csv.QUOTE_MINIMAL, extrasaction='ignore')
    w.writeheader(); w.writerows(out)
print('товаров:', len(out), '· колонок:', len(cols), '· с фото:', sum(1 for o in out if o['Photo']),
      '· с ценой:', sum(1 for o in out if o['Price']))
