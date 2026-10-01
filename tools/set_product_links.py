#!/usr/bin/env python3
"""Подставляет настоящие адреса товаров в карточки блоков главной.

Использование:
    python3 tools/set_product_links.py links.txt

links.txt — строки вида
    fertika-listovoe-18-18-18 = /catalog/tproduct/734172745493-fertika-listovoe-18-18-18

Артикул слева — значение data-sku в блоке. Адрес справа — то, что показывает
Tilda в адресной строке при открытии товара. Скрипт меняет только href
у <a> с нужным data-sku, остальное не трогает.
"""
import re, sys, pathlib

BLOCKS = ['design/blocks/populyarnye.html', 'design/blocks/semena.html']

def main(path):
    links = {}
    for line in pathlib.Path(path).read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        sku, url = (x.strip() for x in line.split('=', 1))
        links[sku] = url

    if not links:
        sys.exit('В файле нет ни одной пары «артикул = адрес»')

    seen, changed = set(), 0
    for f in BLOCKS:
        p = pathlib.Path(f)
        s = p.read_text(encoding='utf-8')
        orig = s
        for sku, url in links.items():
            pat = re.compile(r'(<a[^>]*?)href="[^"]*"([^>]*?data-sku="%s")' % re.escape(sku))
            s, n = pat.subn(lambda m: '%shref="%s"%s' % (m.group(1), url, m.group(2)), s)
            if n:
                seen.add(sku); changed += n
        if s != orig:
            p.write_text(s, encoding='utf-8')
            print('обновлён', f)

    print('заменено ссылок:', changed)
    missing = set(links) - seen
    if missing:
        print('НЕ НАЙДЕНЫ в блоках:', ', '.join(sorted(missing)))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
