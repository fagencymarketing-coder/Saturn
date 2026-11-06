# -*- coding: utf-8 -*-
"""Проверка блока перед отдачей агенту.

Ловит три ошибки, на которых Tilda отказывается сохранять блок или молча
ломает вёрстку (все три пойманы на живом проекте 06.11.2026):

1. Непарные теги — Tilda отвечает «присутствует незакрытый тег».
2. Комментарий с тегом внутри разметки — редактор может не сохранить блок.

Отдельно, как предупреждение, показывает дочерние селекторы со знаком
«больше». Сами по себе они не мешают: такие стоят в подвале, «Популярных»
и «Семенах», и эти блоки работают. Но писать их вплотную, без пробелов
(.a>.b, а не .a > .b), безопаснее: так они точно не попадут под разбор
разметки.

Запуск: python3 tools/check_block.py design/blocks/имя.html
Без аргументов проверяет все блоки.
"""
import io, os, re, sys
from collections import Counter

PAIRED = ('div', 'p', 'h1', 'h2', 'h3', 'a', 'span', 'button', 'details',
          'summary', 'section', 'ul', 'li', 'table', 'tr', 'td', 'th', 'b', 'i', 'em')


def check(path):
    s = io.open(path, encoding='utf-8').read()
    errs = []

    warns = []
    css = ''.join(re.findall(r'<style>([\s\S]*?)</style>', s))
    for line in css.split('\n'):
        code = line.split('/*')[0]
        if re.search(r'[\w\]\)]\s+>\s+[.\w*\[]', code):
            warns.append('дочерний селектор с пробелами: ' + line.strip()[:66])

    # шапку файла (комментарий до первого <style>) не проверяем: это наши
    # заметки для людей, в блок они идут как есть и ничего не ломают
    head_end = s.find('<style>')
    body = s[head_end:] if head_end > 0 else s
    body = re.sub(r'<style>[\s\S]*?</style>', '', body)
    body = re.sub(r'<script>[\s\S]*?</script>', '', body)
    for c in re.findall(r'<!--[\s\S]*?-->', body):
        if re.search(r'<[a-zA-Z]', c):
            errs.append('комментарий с тегом в разметке: ' + c.strip()[:60])

    nocom = re.sub(r'<!--[\s\S]*?-->', '', body)
    for tag in PAIRED:
        o = len(re.findall(r'<%s[\s>]' % tag, nocom))
        c = len(re.findall(r'</%s>' % tag, nocom))
        if o != c:
            errs.append('тег <%s>: открыт %d, закрыт %d' % (tag, o, c))

    return len(s), errs, warns


if __name__ == '__main__':
    files = sys.argv[1:]
    if not files:
        d = 'design/blocks'
        files = [os.path.join(d, f) for f in sorted(os.listdir(d))
                 if f.endswith('.html') and f != 'head-code.html']
    bad = 0
    for f in files:
        n, errs, warns = check(f)
        mark = '✗' if errs else ('!' if warns else '✓')
        if errs:
            bad += 1
        if errs or warns:
            print('%s %-26s %6d символов' % (mark, os.path.basename(f), n))
            for e in errs:
                print('    ошибка: ' + e)
            for w in warns:
                print('    внимание: ' + w)
        else:
            print('✓ %-26s %6d символов' % (os.path.basename(f), n))
    sys.exit(1 if bad else 0)
