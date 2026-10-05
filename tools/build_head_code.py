#!/usr/bin/env python3
"""Собирает код для «Настройки сайта → Вставка кода → HEAD».

Включает:
  1) правки оформления каталога ST340F (бывший catalog-fix.html);
  2) оформление страницы товара /tproduct/... (tovar-fix.html);
  3) дорисовку шапки и подвала на страницах товаров /tproduct/...,
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

# Страница товара. Идёт ПОСЛЕ правок каталога: часть селекторов там и
# там одна и та же, и выигрывать должен слой страницы товара.
tovar = (B / 'tovar-fix.html').read_text(encoding='utf-8')
tovar = re.sub(r'<!--.*?-->', '', tovar, flags=re.S).strip()

jsonld = (ROOT / 'seo' / 'jsonld-site.html').read_text(encoding='utf-8')
jsonld = re.sub(r'<!--.*?-->', '', jsonld, flags=re.S).strip()

out = f"""<!-- Сатурн: весь код для «Настройки сайта → Вставка кода → HEAD».
     Собран tools/build_head_code.py. Вставлять целиком, заменяя всё содержимое поля. -->
{jsonld}

{catalog}

{tovar}

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
  /* ШКАЛА. Четыре ступени вместо непрерывной линии. Прежде каждая
     величина была clamp() от окна 1024 до 1440, и на живом сайте это
     давало дробные кегли (33,99 · 15,996 · 11,612) и немонотонность:
     на ноутбуке 1024 заголовок падал в нижний упор 28, а на планшете
     768 у героя работало своё правило с жёсткими 40 — то есть на
     планшете буквы были крупнее, чем на ноутбуке. Замер аудита 04.10
     на одиннадцати ширинах.

     Теперь одно значение на диапазон, ни одной дроби, порядок
     монотонный. Ступени: ≥1200 · 1024–1199 · 768–1023 · <768.

     Потолок остаётся твой, от 04.10: герой 34, секция 30. Таблица
     аудита предлагала 48 и 40 — автор потом сам её исправил, когда
     увидел это решение. Замер подтверждает: колонка заголовка 560px,
     «сельхозпроизводителей» при 48 занимает 658 и выезжает на фото,
     при 34 — 463. Крупнее нынешнего не делаем. */
  --sa-h1:    34px;
  --sa-h2:    30px;
  --sa-h3:    18px;
  --sa-lead:  16px;
  --sa-body:  15px;
  --sa-small: 13px;
  --sa-cap:   12px;
  --sa-kick:  12px;

  /* межстрочное — отдельными числами, чтобы заголовки не разъезжались */
  --sa-h1-lh: 1.08;
  --sa-h2-lh: 1.15;

  /* Органы управления. Высота 52 на всех ширинах: прежде она ползла
     от 46 до 52, и на телефоне кнопка была ниже, чем на ПК, хотя
     палец крупнее курсора. */
  --sa-btn-h:  52px;
  --sa-btn-px: 26px;
  --sa-fld-h:  52px;
  --sa-chip-h: 36px;

  /* ритм */
  --sa-sec-y: 80px;
  --sa-gap-l: 40px;
  --sa-gap-m: 24px;
  --sa-gap-s: 12px;

  /* движение: одна длительность на весь сайт */
  --sa-t: .18s;
  --sa-ease: cubic-bezier(.2,.6,.2,1);

  /* форма */
  --sa-r-card: 22px;
  --sa-r-ctrl: 12px;
  --sa-r-pill: 999px;
}}
@media (max-width:1199px){{
  :root{{
    --sa-h1:32px; --sa-h2:28px; --sa-h3:17px;
    --sa-btn-px:24px; --sa-gap-l:32px;
  }}
}}
@media (max-width:1023px){{
  :root{{
    --sa-h1:30px; --sa-h2:28px;
    --sa-btn-px:22px; --sa-sec-y:64px; --sa-gap-m:20px;
  }}
}}
@media (max-width:767px){{
  :root{{
    --sa-h1:30px; --sa-h2:28px; --sa-h3:16px; --sa-lead:15px;
    --sa-btn-px:20px; --sa-gap-l:24px; --sa-gap-m:16px;
  }}
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
/* Тильда принудительно снимает обводку на трёх элементах каталога:
   селекте сортировки, кнопке фильтра и поле поиска. Без явного
   возврата наше правило их не перебьёт — нашёл агент 04.10. */
.t-catalog__sort-select:focus-visible,
.t-catalog__filter__btn:focus-visible,
.t-catalog__filter__input:focus-visible,
.js-catalog-filter-search:focus-visible{{
  outline:2px solid #FF4200 !important;outline-offset:2px !important}}

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

/* Попап заявки (блок Тильды rec4481961301 на кнопках «Получить
   предложение» / «Оставить заявку»). Приводим к нашему виду: поля в
   столбик и крупные, кнопка — кнопочный #D93800, а не три разных
   оранжевых из настроек блока. Таргетим и по id блока, и по .t-popup
   на случай пересоздания блока. */
#rec4481961301 .t-form__inputsbox,
.t-popup .t-form__inputsbox{{display:block !important}}
#rec4481961301 .t-input-group,
.t-popup .t-input-group{{width:100% !important;max-width:none !important;
  margin:0 0 14px !important;padding:0 !important}}
#rec4481961301 .t-input,
.t-popup .t-input{{width:100% !important;height:54px !important;
  font-size:16px !important;border-radius:12px !important}}
#rec4481961301 .t-submit,
.t-popup .t-submit{{width:100% !important;height:54px !important;
  background:#D93800 !important;border-radius:12px !important;
  font-size:15px !important;font-weight:600 !important;
  font-family:Montserrat,sans-serif !important}}
@media (hover:hover){{
  #rec4481961301 .t-submit:hover,
  .t-popup .t-submit:hover{{background:#C23100 !important}}
}}
#rec4481961301 .t-input:focus,
.t-popup .t-input:focus{{border-color:#D93800 !important;
  box-shadow:0 0 0 3px rgba(217,56,0,.18) !important}}
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
      '<a class="sa-tp-cta__btn" href="/home#contacts">Получить предложение</a>' +
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
  /* Штатный баннер cookie Тильды переведён не до конца: в окне
     настроек у переключателя категории «Аналитические» подпись
     «Disabled» по-английски, у «Обязательных» пустая. Нашёл агент
     04.10. Правим текст на месте — окно настроек рисуется по щелчку,
     поэтому смотрим за разметкой, а не правим один раз при загрузке. */
  function perevodCookie(){{
    var SLOVA = {{'Disabled':'Выключено', 'Enabled':'Включено',
                 'Settings':'Настройки', 'Accept all':'Принять все',
                 'Reject all':'Отклонить все'}};
    document.querySelectorAll('.t972__toggle-txt,.t972 .t-btn,.t972 button')
      .forEach(function(el){{
        if(el.children.length) return;
        var t = (el.textContent || '').trim();
        if(SLOVA[t]) el.textContent = SLOVA[t];
      }});
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

  function vse(){{ draw(); cookieBanner(); perevodCookie(); }}
  vse();
  document.addEventListener('DOMContentLoaded', vse);
  window.addEventListener('load', vse);
  /* Окно настроек cookie рисуется по щелчку, поэтому перевод вешаем
     и на наблюдателя: иначе «Disabled» успеет мелькнуть. */
  if (window.MutationObserver) {{
    new MutationObserver(function(){{
      clearTimeout(window.__saCkT);
      window.__saCkT = setTimeout(perevodCookie, 120);
    }}).observe(document.documentElement, {{childList:true, subtree:true}});
  }}
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
# Комментарии в поле HEAD не нужны: объяснения живут в файлах
# репозитория, а на сайт они едут на каждую страницу каждому
# посетителю. К тому же поле Тильды не резиновое — со страницей товара
# собранный код подошёл к 65 тысячам символов, и дальше расти ему
# некуда. Снимаем только блочные /* ... */; строчных // в коде нет,
# а «//» внутри адресов трогать нельзя, поэтому их и не трогаем.
out = re.sub(r'/\*[\s\S]*?\*/', '', out)
out = re.sub(r'[ \t]+\n', '\n', out)
out = re.sub(r'\n{3,}', '\n\n', out)

(B / 'head-code.html').write_text(out, encoding='utf-8')
print('собрано:', len(out), 'символов →', B / 'head-code.html')
