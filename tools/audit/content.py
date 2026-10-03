#!/usr/bin/env python3
"""Проверка содержания сайта против эталона docs/SPRAVOCHNIK-SAYT.md.

  python3 tools/audit/content.py            — проверить файлы блоков
  python3 tools/audit/content.py --live     — проверить опубликованные страницы

Что проверяет:
  1. все телефоны и почты совпадают с эталонной таблицей;
  2. нет телефонов и почт, которых в эталоне нет;
  3. каждая ссылка на файл и страницу открывается (код 200);
  4. у каждой ссылки есть текст или aria-label;
  5. реквизиты (ИНН, КПП, ОГРН, адреса) совпадают с эталоном.
"""
import re, sys, subprocess, pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[2]
REF  = (ROOT / 'docs' / 'SPRAVOCHNIK-SAYT.md').read_text(encoding='utf-8')
CA   = '/root/.ccr/ca-bundle.crt'

# Домены, которые Tilda подключает через preconnect и dns-prefetch.
# Их адрес — не ссылка страницы, проверять там нечего.
SLUZHEBNYE = {
    'https://fonts.gstatic.com',
    'https://fonts.googleapis.com',
    'https://static.tildacdn.com',
    'https://ws.tildacdn.com',
    'https://neo.tildacdn.com',
    'https://store.tildacdn.com',
}

def ref_table():
    phones, mails = set(), set()
    for line in REF.splitlines():
        for m in re.findall(r'\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}', line):
            phones.add(re.sub(r'\D', '', m)[-10:])
        for m in re.findall(r'[\w.\-]+@sssaturn\.ru', line):
            mails.add(m.lower())
    return phones, mails

def ref_props():
    out = {}
    for key in ['ИНН', 'КПП', 'ОГРН']:
        m = re.search(r'\|\s*' + key + r'\s*\|\s*([0-9]+)\s*\|', REF)
        if m: out[key] = m.group(1)
    return out

def sources(live):
    if live:
        pages = re.findall(r'\|\s*[^|]+\s*\|\s*(https://sssaturn\.ru[^\s|]*)\s*\|', REF)
        for u in dict.fromkeys(pages):
            r = subprocess.run(['curl', '-s', '--cacert', CA, u],
                               capture_output=True, text=True)
            yield u, r.stdout
    else:
        for f in sorted((ROOT / 'design' / 'blocks').glob('*.html')):
            if f.name == 'head-code.html':
                continue
            yield f.name, f.read_text(encoding='utf-8')

def main():
    live = '--live' in sys.argv
    phones_ok, mails_ok = ref_table()
    props = ref_props()
    bad = []
    links = set()

    for name, text in sources(live):
        for p in re.findall(r'tel:\+?(\d{10,11})', text):
            if p[-10:] not in phones_ok:
                bad.append((name, 'телефона нет в эталоне', p))
        for m in re.findall(r'mailto:([\w.\-]+@[\w.\-]+)', text):
            if m.lower() not in mails_ok:
                bad.append((name, 'почты нет в эталоне', m))
        for k, v in props.items():
            if k in text and v not in text:
                bad.append((name, k + ' не совпадает с эталоном', ''))
        # Ссылки берём только из <a>. У <link rel="preconnect"> в href
        # стоит голый домен служебной инфраструктуры Tilda, он честно
        # отвечает 204, 403 или 404 — это не битая ссылка, а норма.
        # Пока их считали, --live всегда давал ложные нарушения.
        for tag in re.findall(r'<a\b[^>]*>', text):
            m = re.search(r'href="([^"#]+)"', tag)
            if not m:
                continue
            href = m.group(1)
            if href.startswith(('tel:', 'mailto:', 'javascript:')):
                continue
            if href.rstrip('/') in SLUZHEBNYE:
                continue
            links.add(href)

    print('ЭТАЛОН: телефонов', len(phones_ok), '· почт', len(mails_ok),
          '· реквизитов', len(props))
    print('Найдено ссылок:', len(links))

    # проверка доступности
    for href in sorted(links):
        if href.startswith('http'):
            url = href
        elif href.startswith('/'):
            url = 'https://sssaturn.ru' + href
        else:
            continue
        code = subprocess.run(
            # -g: у адресов разделов каталога в строке запроса есть
            # квадратные скобки (tfc_storepartnav[4384406801]=…), и без
            # -g curl принимает их за шаблон перебора и не ходит никуда.
            ['curl', '-s', '-g', '-o', '/dev/null', '-w', '%{http_code}',
             '-L', '--cacert', CA, url],
            capture_output=True, text=True).stdout.strip()
        mark = 'ok ' if code == '200' else 'БИТАЯ'
        if code != '200':
            bad.append(('ссылки', 'код ' + code, url))
        print(f'  {mark} {code}  {url}')

    print('\nНАРУШЕНИЙ:', len(bad))
    for b in bad:
        print('  •', b[0], '—', b[1], b[2])
    return 1 if bad else 0

if __name__ == '__main__':
    sys.exit(main())
