#!/usr/bin/env python3
"""Проверяет настройки блока каталога ST340F на живой странице.

    python3 tools/audit/live-catalog.py

Tilda кладёт все настройки блока прямо в HTML страницы, в объекты
options, parts_optsObj и breadcrumbs_optsObj. Их видно через curl, и
по ним точно понятно, что в админке переключили, а что нет. Это
дешевле скриншота и честнее отчёта.
"""
import re, subprocess, sys

ADRES = sys.argv[1] if len(sys.argv) > 1 else 'https://sssaturn.ru/catalog'

# что проверяем: имя настройки → (ожидаемое, пояснение)
ZHDEM = {
    'storePartsPosition': ('sidebar', 'разделы только на боковой панели'),
    'homeItem': ('Главная', 'первый пункт хлебных крошек — текст, не домик'),
}


def main():
    r = subprocess.run(['curl', '-s', '--cacert', '/root/.ccr/ca-bundle.crt', ADRES],
                       capture_output=True, text=True, timeout=120)
    html = r.stdout
    if not html:
        sys.exit(f'не удалось скачать {ADRES}')
    print(f'{ADRES} · {len(html)} байт\n')

    plohih = 0
    for klyuch, (nado, zachem) in ZHDEM.items():
        m = re.search(r"%s:\s*'([^']*)'" % klyuch, html)
        est = m.group(1) if m else None
        ok = est == nado
        plohih += 0 if ok else 1
        vidno = f"'{est}'" if est is not None else 'нет в странице'
        print(f"  {'ok ' if ok else 'НЕТ'} {klyuch:20} {vidno:18} надо '{nado}' — {zachem}")

    # закрепление боковой панели
    m = re.search(r"panelStyles:\{[^}]*?fixed:(true|false)", html)
    fixed = m.group(1) if m else '?'
    ok = fixed == 'false'
    plohih += 0 if ok else 1
    print(f"  {'ok ' if ok else 'НЕТ'} {'панель закреплена':20} {fixed:18} надо 'false' — "
          f'иначе у панели своя полоса прокрутки')

    # английские надписи
    for slovo in ('Load more', 'Disabled'):
        est = slovo in html
        plohih += 1 if est else 0
        print(f"  {'НЕТ' if est else 'ok '} {'англ. «%s»' % slovo:20} "
              f"{'есть на странице' if est else 'нет':18} надо убрать")

    print(f'\n  не сделано: {plohih}')
    return 1 if plohih else 0


if __name__ == '__main__':
    sys.exit(main())
