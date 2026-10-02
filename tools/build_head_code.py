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

/* Баннер cookie для страниц товаров */
#sa-ck{{position:fixed;right:34px;bottom:34px;z-index:9500;width:360px;max-width:calc(100vw - 40px);
  background:#1E1B18;color:#fff;border-radius:16px;padding:24px;
  font-family:Montserrat,-apple-system,Segoe UI,Roboto,sans-serif;
  box-shadow:0 12px 40px rgba(0,0,0,.35)}}
#sa-ck .sa-ck__t{{font-size:16px;font-weight:700;line-height:1.3}}
#sa-ck .sa-ck__x{{font-size:13px;font-weight:400;line-height:19.5px;color:#B5B0AA;margin-top:10px}}
#sa-ck .sa-ck__x a{{color:#FF4200;text-decoration:none}}
#sa-ck .sa-ck__b{{display:flex;flex-direction:column;gap:8px;margin-top:18px}}
#sa-ck button{{min-height:44px;border-radius:10px;border:0;cursor:pointer;
  font-family:inherit;font-size:14px;font-weight:600;padding:10px 16px}}
#sa-ck button[data-sa-ck=all]{{background:#D93800;color:#fff}}
#sa-ck button[data-sa-ck=none]{{background:transparent;color:#fff;border:1px solid #B5B0AA}}
@media (hover:hover){{
  #sa-ck button[data-sa-ck=all]:hover{{background:#C23100}}
  #sa-ck button[data-sa-ck=none]:hover{{border-color:#FF4200;color:#FF4200}}
}}
@media (max-width:640px){{
  #sa-ck{{right:12px;left:12px;bottom:12px;width:auto;padding:18px}}
}}
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
  /* Баннер cookie на страницах товаров: блока T972 там нет,
     поэтому показываем свой. Пишет те же cookie, что и Tilda,
     поэтому выбор, сделанный здесь, виден и на остальных страницах. */
  function ck(n){{
    var m = document.cookie.match('(^|;)\\s*' + n + '\\s*=\\s*([^;]+)');
    return m ? m.pop() : '';
  }}
  function setCk(n,v){{
    var d = new Date(); d.setTime(d.getTime() + 365*24*60*60*1000);
    document.cookie = n + '=' + v + ';expires=' + d.toUTCString() + ';path=/';
  }}
  function cookieBanner(){{
    if(!document.body) return;
    if(!onProductPage()) return;
    if(document.querySelector('.t972')) return;          /* штатный баннер есть */
    if(document.getElementById('sa-ck')) return;
    if(ck('t_cookiesConsentGiven') || ck('t_cookiesRejectAll')) return;
    var b = document.createElement('div');
    b.id = 'sa-ck';
    b.innerHTML =
      '<div class="sa-ck__t">Файлы cookie</div>' +
      '<div class="sa-ck__x">Мы используем файлы cookie и Яндекс Метрику, чтобы сайт работал удобнее. ' +
      'Подробнее — в <a href="/privacy">политике обработки персональных данных</a>.</div>' +
      '<div class="sa-ck__b">' +
      '<button type="button" data-sa-ck="all">Принять все</button>' +
      '<button type="button" data-sa-ck="none">Отклонить необязательные</button>' +
      '</div>';
    b.addEventListener('click', function(e){{
      var a = e.target.getAttribute && e.target.getAttribute('data-sa-ck');
      if(!a) return;
      setCk('t_cookiesConsentGiven','true');
      if(a === 'all'){{ setCk('t_cookiesCategories', encodeURIComponent('["analytics"]')); }}
      else {{ setCk('t_cookiesCategories', encodeURIComponent('[]')); setCk('t_cookiesRejectAll','true'); }}
      b.remove();
    }});
    document.body.appendChild(b);
  }}

  draw(); cookieBanner();
  document.addEventListener('DOMContentLoaded', function(){{ draw(); cookieBanner(); }});
  window.addEventListener('load', function(){{ draw(); cookieBanner(); }});
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
