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
    # Крошки снова видны (04.10), поэтому первый пункт опять важен:
    # домик вместо слова рядом с заголовком в 40px смотрится мусором.
    'homeItem': ('Главная', 'первый пункт крошек — слово, а не домик'),
}

# Строки, которых не должно быть ВИДНО. Искать их в сыром исходнике
# нельзя: Тильда держит шаблоны кнопок внутри <script>, и «Load more»
# лежит там всегда, даже когда на кнопке написано «Загрузить ещё».
# Поэтому перед поиском вырезаем всё содержимое <script> и <style>.
import re as _re
def vidimyi_tekst(html):
    html = _re.sub(r'(?is)<script\b.*?</script>', ' ', html)
    html = _re.sub(r'(?is)<style\b.*?</style>', ' ', html)
    return html

# что должно присутствовать в коде страницы: подпись → (строка, пояснение)
# Искать по текстам наших комментариев больше нельзя: сборщик кода HEAD
# вырезает их, чтобы поле Тильды не упёрлось в предел и чтобы двадцать
# килобайт объяснений не ехали посетителю на каждой странице. Поэтому
# ищем сами правила — куски CSS, которые ни на что другое не похожи.
NADO_EST = {
    'крошки оформлены': ('#rec4384406801 .js-block-header', 'правило 9'),
    'штатный поиск скрыт': ('t-catalog__filter__search-and-sort', 'правило 13'),
    'панель липкая': ('position:sticky', 'правило 14'),
    'цены по запросу нет': ('.js-catalog-price-wrapper[data-sa-ask]', 'правило 7'),
    'страница товара одета': ('.sa-tp__chars', 'tovar-fix'),
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

    # Английские надписи. По исходнику судить нельзя, и это не лень,
    # а свойство страницы: «Load more» лежит в разметке кнопки всегда,
    # а на экран его заменяет наш скрипт уже в браузере. Поэтому строки
    # не считаются нарушением — они справочные, проверяются глазами.
    vidno = vidimyi_tekst(html)
    for slovo in ('Load more', 'Disabled'):
        est = slovo in vidno
        print(f"  ··  {'англ. «%s»' % slovo:20} "
              f"{'есть в разметке' if est else 'нет':18} — проверить в браузере")

    # Наши правила оформления доехали до живой страницы. Ищем не класс
    # Тильды (он есть всегда), а наш собственный комментарий рядом с ним.
    for imya, (stroka, zachem) in NADO_EST.items():
        est = stroka in html
        plohih += 0 if est else 1
        print(f"  {'ok ' if est else 'НЕТ'} {imya:20} "
              f"{'есть' if est else 'не выложено':18} — {zachem}")

    print(f'\n  не сделано: {plohih}')
    return 1 if plohih else 0


if __name__ == '__main__':
    sys.exit(main())
