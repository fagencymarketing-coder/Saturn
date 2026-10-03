#!/usr/bin/env python3
"""Говорит, выложены ли правки уплотнения на живой сайт.

    python3 tools/audit/live-blocks.py
    python3 tools/audit/live-blocks.py https://sssaturn.ru/home

Признак простой и надёжный: уплотнение поменяло отступы секций со
128/96/72 (ПК/планшет/телефон) на 80/64/52. Старых отступов на
странице быть не должно ни одного, новых — по шесть каждого.

Проверять версию блока по кускам разметки не вышло: блоки менялись
отступами, а разметка осталась прежней, и любой кусок находился и в
старой версии тоже. Отступ — то немногое, что различает версии точно.
"""
import re, subprocess, sys

ADRES = sys.argv[1] if len(sys.argv) > 1 else 'https://sssaturn.ru/home'
STARYE = {'ПК': 128, 'планшет': 96, 'телефон': 72}
NOVYE = {'ПК': 80, 'планшет': 64, 'телефон': 52}


def zhivaya(url):
    r = subprocess.run(
        ['curl', '-s', '--cacert', '/root/.ccr/ca-bundle.crt', url],
        capture_output=True, text=True, timeout=120)
    if r.returncode != 0 or not r.stdout:
        sys.exit(f'не удалось скачать {url}')
    return r.stdout


def skolko(html, px):
    return len(re.findall(r'padding:%dpx 0' % px, html))


def main():
    html = zhivaya(ADRES)
    print(f'{ADRES} · {len(html)} байт\n')

    staryh = novyh = 0
    for imya in STARYE:
        s, n = skolko(html, STARYE[imya]), skolko(html, NOVYE[imya])
        staryh += s
        novyh += n
        print(f'  {imya:8} старых секций по {STARYE[imya]}px: {s} · '
              f'новых по {NOVYE[imya]}px: {n}')

    print()
    if staryh == 0 and novyh > 0:
        print('  ВЫЛОЖЕНО: старых отступов не осталось')
        return 0
    if novyh == 0:
        print('  НЕ ВЫЛОЖЕНО: на сайте целиком старая версия блоков')
        return 1
    print('  ВЫЛОЖЕНО ЧАСТИЧНО: на странице вперемешку старые и новые секции')
    return 1


if __name__ == '__main__':
    sys.exit(main())
