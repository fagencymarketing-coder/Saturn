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
/* ===== Шкала сайта =======================================================
   Один слой на весь «Сатурн». Блоки не держат своих чисел — только эти
   переменные. Меняем здесь — меняется согласованно везде.

   Каждая величина не число, а отрезок: от окна 1024 до окна 1440 растёт
   линейно, выше 1440 замирает на холстовом значении, ниже 1024 — на
   нижнем. Поэтому между ступенями ничего не прыгает.

   Кегли уменьшены относительно холста по решению заказчика 04.10.2026:
   заголовок секции 40 → 30, заголовок героя 42 → 34. Причина — «тихая
   дороговизна»: отношение заголовка к тексту стало 2,0 вместо 2,7.
   Дорогое впечатление даёт воздух, а не размер букв. Холст в этой части
   перебит сознательно, как иконки в шапке и мелкие логотипы партнёров.
   ========================================================================= */
:root{{
  /* типографика: 1024 → 1440 */
  --sa-h1:    clamp(28px, 1.442vw + 13.23px, 34px);
  --sa-h2:    clamp(24px, 1.442vw +  9.23px, 30px);
  --sa-h3:    clamp(16px, 0.481vw + 11.08px, 18px);
  --sa-lead:  clamp(15px, 0.240vw + 12.54px, 16px);
  --sa-body:  clamp(14px, 0.240vw + 11.54px, 15px);
  --sa-small: 13px;
  --sa-cap:   12px;
  --sa-kick:  clamp(11px, 0.240vw +  8.54px, 12px);

  /* межстрочное — отдельными числами, чтобы заголовки не разъезжались */
  --sa-h1-lh: 1.08;
  --sa-h2-lh: 1.15;

  /* органы управления */
  --sa-btn-h:  clamp(48px, 1.923vw + 28.31px, 56px);
  --sa-fld-h:  clamp(46px, 1.442vw + 31.23px, 52px);
  --sa-chip-h: clamp(32px, 0.962vw + 22.15px, 36px);

  /* ритм */
  --sa-sec-y: clamp(48px, 7.692vw - 30.77px, 80px);
  --sa-gap-l: clamp(28px, 2.885vw -  1.54px, 40px);
  --sa-gap-m: clamp(20px, 1.923vw +  0.31px, 28px);
  --sa-gap-s: clamp(12px, 0.962vw +  2.15px, 16px);

  /* движение: одна длительность на весь сайт */
  --sa-t: .18s;
  --sa-ease: cubic-bezier(.2,.6,.2,1);

  /* форма */
  --sa-r-card: 22px;
  --sa-r-ctrl: 12px;
  --sa-r-pill: 999px;
}}
/* ===== Фокус с клавиатуры ===============================================
   Человек, который ходит по сайту клавишей Tab — а это и доступность,
   и просто те, у кого не работает мышь, — до сих пор не видел, где
   находится: правило не было задано ни в одном из тринадцати блоков.
   :focus-visible, а не :focus, чтобы обводка не вспыхивала от мыши.
   Обводка снаружи элемента, поэтому вёрстка не сдвигается. */
:where(a,button,input,select,textarea,summary,[tabindex]):focus-visible{{
  outline:2px solid #FF4200;outline-offset:3px;border-radius:4px}}
/* На тёмном фоне оранжевый по чёрному читается плохо — там белая. */
:where(.sa-hero,.sa-ag,.sa-geo,.sa-ct,.sa-hd,.sa-kc,#sa-tp-cta)
  :where(a,button,input,summary,[tabindex]):focus-visible{{
  outline-color:#fff}}

{hd_css}
{ft_css}

/* Полоса заявки на страницах товаров */
#sa-tp-cta,#sa-tp-cta *{{box-sizing:border-box}}
#sa-tp-cta{{background:#141210;color:#fff;
  font-family:Montserrat,-apple-system,Segoe UI,Roboto,sans-serif}}
#sa-tp-cta .sa-tp-cta__in{{max-width:1240px;margin:0 auto;padding:56px 20px}}
#sa-tp-cta .sa-tp-cta__t{{font-size:28px;font-weight:800;line-height:1.15;
  overflow-wrap:break-word}}
#sa-tp-cta .sa-tp-cta__x{{font-size:15px;font-weight:400;line-height:22.5px;
  color:#B5B0AA;margin-top:10px;max-width:560px}}
#sa-tp-cta .sa-tp-cta__b{{display:flex;align-items:center;gap:20px;margin-top:28px;
  flex-wrap:wrap}}
#sa-tp-cta .sa-tp-cta__btn{{display:inline-flex;align-items:center;justify-content:center;
  height:var(--sa-btn-h);padding:0 28px;border-radius:var(--sa-r-ctrl);
  background:#D93800;color:#fff;
  text-decoration:none;font-size:16px;font-weight:700}}
#sa-tp-cta .sa-tp-cta__tel{{color:#fff;text-decoration:none;font-size:16px;font-weight:700;
  min-height:44px;display:inline-flex;align-items:center}}
@media (hover:hover){{
  #sa-tp-cta .sa-tp-cta__btn:hover{{background:#C23100}}
  #sa-tp-cta .sa-tp-cta__tel:hover{{color:#FF4200}}
}}
@media (max-width:767px){{
  #sa-tp-cta .sa-tp-cta__in{{padding:40px 20px}}
  #sa-tp-cta .sa-tp-cta__t{{font-size:clamp(20px,6.4vw,24px)}}
  #sa-tp-cta .sa-tp-cta__b{{flex-direction:column;align-items:stretch;gap:12px}}
  #sa-tp-cta .sa-tp-cta__btn{{width:100%}}
  #sa-tp-cta .sa-tp-cta__tel{{justify-content:center}}
}}

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
    /* полоса заявки: на странице товара своей кнопки у Tilda нет,
       а именно сюда приходят из поиска и по пересланным ссылкам */
    var cta = document.createElement('div');
    cta.id = 'sa-tp-cta';
    cta.innerHTML =
      '<div class="sa-tp-cta__in">' +
      '<div class="sa-tp-cta__t">Нужна цена или подбор под вашу культуру?</div>' +
      '<div class="sa-tp-cta__x">Ответим в течение рабочего дня, подберём решение под хозяйство</div>' +
      '<div class="sa-tp-cta__b">' +
      '<a class="sa-tp-cta__btn" href="/#contacts">Получить предложение</a>' +
      '<a class="sa-tp-cta__tel" href="tel:+79609534888">+7 (960) 953-48-88</a>' +
      '</div></div>';
    document.body.appendChild(cta);

    /* Значок «Made on Tilda» стоит сразу после карточки товара, и если
       просто дописать подвал в конец body, значок окажется в середине
       страницы. Поэтому не двигаем его, а ставим свои блоки ПЕРЕД ним:
       значок остаётся последним, как и задумано платформой.

       Раньше здесь было document.body.appendChild(cp), то есть значок
       переносился вниз. Tilda это ломает намеренно: после сохранения
       кода она заменяет в слове tildacopy латинскую «o» на кириллическую,
       и обращение перестаёт находить элемент (проверено агентом дважды
       03.10.2026). Обходить защиту мы не будем — лейбл убирается
       легально, годовым тарифом. Текущий способ в защиту не упирается:
       мы не трогаем чужой элемент, а расставляем свои. */
    var cp = document.getElementById('tildacopy');
    if (!cp) {{
      /* Запасной способ найти значок: Tilda портит именно это слово в
         коде, поэтому обращение по id после сохранения может не
         сработать. Значок — единственная ссылка на tilda.cc в body.
         Ищем её только чтобы понять, куда поставить СВОИ блоки.
         Сам значок не трогаем, не прячем и не переносим. */
      var a = document.querySelector('body a[href*="tilda.cc"]');
      cp = a ? a.closest('div') || a : null;
    }}

    var bot = document.createElement('div');
    bot.innerHTML = FT;
    if (cp && cp.parentNode === document.body) {{
      document.body.insertBefore(cta, cp);
      document.body.insertBefore(bot, cp);
    }} else {{
      document.body.appendChild(bot);
    }}
  }}
  /* Баннер cookie на страницах товаров: блока T972 там нет,
     поэтому показываем свой. Пишет те же cookie, что и Tilda,
     поэтому выбор, сделанный здесь, виден и на остальных страницах. */
  function ck(n){{
    /* без регулярного выражения: в строковом литерале JS «\\s» схлопывается в «s» */
    var parts = document.cookie.split(';');
    for (var i = 0; i < parts.length; i++) {{
      var t = parts[i].replace(/^ +/, '');
      if (t.indexOf(n + '=') === 0) return t.slice(n.length + 1);
    }}
    return '';
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
