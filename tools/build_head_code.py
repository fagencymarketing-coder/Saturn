#!/usr/bin/env python3
"""Собирает код для «Настройки сайта → Вставка кода → HEAD».

Включает:
  1) правки оформления каталога ST340F (бывший catalog-fix.html);
  2) дорисовку шапки и подвала на страницах товаров /tproduct/...,
     куда Tilda блоки страницы не подставляет.

Шапка и подвал берутся из тех же файлов, что стоят блоками на сайте,
поэтому расходиться они не могут.

    python3 tools/build_head_code.py  →  design/blocks/head-code.html
"""
import re, pathlib, json

ROOT = pathlib.Path(__file__).resolve().parent.parent
B = ROOT / 'design' / 'blocks'

def split_block(name):
    """Возвращает (css, html) из файла блока."""
    s = (B / name).read_text(encoding='utf-8')
    s = re.sub(r'<!--.*?-->', '', s, flags=re.S)
    css = '\n'.join(m.group(1) for m in re.finditer(r'<style>(.*?)</style>', s, re.S))
    html = re.sub(r'<style>.*?</style>', '', s, flags=re.S).strip()
    return css.strip(), html

hd_css, hd_html = split_block('shapka.html')
ft_css, ft_html = split_block('podval.html')

catalog = (B / 'catalog-fix.html').read_text(encoding='utf-8')
catalog = re.sub(r'<!--.*?-->', '', catalog, flags=re.S).strip()

jsonld = (ROOT / 'seo' / 'jsonld-site.html').read_text(encoding='utf-8')
jsonld = re.sub(r'<!--.*?-->', '', jsonld, flags=re.S).strip()

out = f"""<!-- Сатурн: весь код для «Настройки сайта → Вставка кода → HEAD».
     Собран tools/build_head_code.py. Вставлять целиком, заменяя всё содержимое поля. -->
{jsonld}

{catalog}

<style>
{hd_css}
{ft_css}
</style>

<script>
/* Шапка и подвал на страницах товаров.
   Tilda рендерит на /<страница>/tproduct/<id> только блок каталога,
   поэтому шапку и подвал там дорисовываем сами. */
(function(){{
  var HD = {json.dumps(hd_html, ensure_ascii=False)};
  var FT = {json.dumps(ft_html, ensure_ascii=False)};
  function onProductPage(){{ return /\\/tproduct\\//.test(location.pathname); }}
  function draw(){{
    if(!document.body) return;            /* скрипт стоит в <head>: body ещё нет */
    if(!onProductPage()) return;
    if(document.querySelector('.sa-hd')) return;      /* шапка блоком уже есть */
    if(document.getElementById('sa-tp-chrome')) return;
    var top = document.createElement('div');
    top.id = 'sa-tp-chrome';
    top.innerHTML = HD;
    document.body.insertBefore(top, document.body.firstChild);
    var bot = document.createElement('div');
    bot.innerHTML = FT;
    document.body.appendChild(bot);
  }}
  draw();
  document.addEventListener('DOMContentLoaded', draw);
  window.addEventListener('load', draw);
  /* каталог меняет адрес без перезагрузки — следим за переходами */
  setInterval(function(){{
    if(!onProductPage()){{
      var c = document.getElementById('sa-tp-chrome');
      if(c){{ c.remove(); }}
    }} else {{ draw(); }}
  }}, 600);
}})();
</script>
"""
(B / 'head-code.html').write_text(out, encoding='utf-8')
print('собрано:', len(out), 'символов →', B / 'head-code.html')
