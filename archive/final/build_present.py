logo_color = open('/tmp/logo_color.txt').read().strip()
logo_white = open('/tmp/logo_datauri.txt').read().strip()

HTML = r'''<title>Прототип сайта «Сатурн»</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#F4EEE7; --surface:#FFFFFF; --surface-2:#FBF8F3;
  --text:#17130F; --muted:#726657; --line:#E4DDD2;
  --orange:#EE4A0E; --orange-deep:#C43C08; --orange-soft:#FCE7DC;
  --green:#1F9E57; --green-dark:#147A41; --green-soft:#E4F4EB;
  --ink:#141210; --paper-dark:#211B16;
}
:root:not([data-theme="light"]){}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#151210; --surface:#211B16; --surface-2:#1B1712;
    --text:#F4EEE7; --muted:#B9ADA2; --line:rgba(255,255,255,.12);
    --orange-soft:rgba(238,74,14,.16); --green-soft:rgba(31,158,87,.16);
  }
}
:root[data-theme="dark"]{
  --bg:#151210; --surface:#211B16; --surface-2:#1B1712;
  --text:#F4EEE7; --muted:#B9ADA2; --line:rgba(255,255,255,.12);
  --orange-soft:rgba(238,74,14,.16); --green-soft:rgba(31,158,87,.16);
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--text);
  font-family:"IBM Plex Sans",system-ui,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:"Archivo",sans-serif;margin:0;line-height:1.08;letter-spacing:-.015em}
.mono{font-family:"IBM Plex Mono",monospace}
.wrap{max-width:1180px;margin:0 auto;padding:0 22px}

/* ---- Заголовок презентации ---- */
.top{padding:54px 0 22px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:"IBM Plex Mono";font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--orange-deep);font-weight:600}
.top h1{font-size:clamp(30px,4.6vw,50px);text-transform:uppercase;font-weight:900;margin:14px 0 0;text-wrap:balance}
.top p{max-width:64ch;color:var(--muted);font-size:17px;margin:14px 0 0}
.legend{display:flex;gap:16px;flex-wrap:wrap;margin-top:22px;font-size:13px;color:var(--muted)}
.legend b{color:var(--text)}
.dotc{display:inline-block;width:11px;height:11px;border-radius:50%;vertical-align:middle;margin-right:6px}

/* ---- Шаг: превью + пояснение ---- */
.step{display:grid;grid-template-columns:1.35fr 1fr;gap:26px;align-items:start;padding:40px 0;border-bottom:1px solid var(--line)}
.preview{position:relative}
.frame{border:1px solid var(--line);border-radius:14px;overflow:hidden;box-shadow:0 1px 2px rgba(23,19,15,.05),0 22px 50px -30px rgba(23,19,15,.35);background:#fff}
.chrome{display:flex;align-items:center;gap:7px;padding:9px 12px;background:#ECE6DE;border-bottom:1px solid var(--line)}
.chrome i{width:10px;height:10px;border-radius:50%;background:#C9BEB0;display:block}
.chrome .url{margin-left:10px;font-family:"IBM Plex Mono";font-size:11px;color:#8A8078;background:#fff;border-radius:5px;padding:3px 10px}

.explain{position:sticky;top:16px}
.badge{display:inline-flex;align-items:center;gap:8px;font-family:"IBM Plex Mono";font-size:12px;font-weight:600;letter-spacing:.08em;text-transform:uppercase;color:var(--orange-deep);background:var(--orange-soft);border:1px solid rgba(238,74,14,.28);padding:5px 11px;border-radius:30px}
.explain h2{font-size:23px;margin:14px 0 0;text-wrap:balance}
.explain .card{margin-top:14px;background:var(--surface);border:1px solid var(--line);border-radius:12px;padding:16px 18px}
.explain .k{font-family:"IBM Plex Mono";font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);font-weight:600}
.explain .v{margin:4px 0 14px;font-size:15px}
.explain .v:last-child{margin-bottom:0}
.explain .v.why{color:var(--text)}
.explain .v.why b{color:var(--green-dark)}

/* ================= МИНИ-САЙТ (фирменные цвета) ================= */
.site{font-size:13px;color:#17130F;background:#fff}
.site *{box-sizing:border-box}
.s-hdr{display:flex;align-items:center;gap:14px;padding:12px 16px;background:#fff;border-bottom:1px solid #EEE7DD}
.s-hdr img{height:26px;width:auto}
.s-nav{display:flex;gap:14px;color:#3C352D;font-size:12px;font-weight:500}
.s-sp{flex:1}
.s-ph{font-weight:700;font-size:12px;white-space:nowrap;color:#17130F}
.s-btn{display:inline-block;font-weight:700;font-size:12px;border-radius:8px;padding:8px 14px;border:1.5px solid transparent;text-decoration:none;white-space:nowrap}
.s-btn.o{background:#EE4A0E;color:#fff}
.s-btn.g{background:#1F9E57;color:#fff}
.s-btn.ghost{background:#fff;color:#17130F;border-color:#D3C9BB}
.s-btn.sm{padding:6px 11px;font-size:11px}

.s-hero{position:relative;overflow:hidden;color:#fff;padding:34px 22px;
  background:linear-gradient(105deg,#14100c 0%,#1f1710 42%,#7d2c08 96%,#C43C08 120%)}
.s-hero::after{content:"";position:absolute;right:-8%;top:-30%;width:62%;height:180%;
  background:radial-gradient(60% 55% at 70% 45%,#FF7A3C 0%,#F0490F 45%,#C43C08 78%,transparent 100%);
  border-radius:48% 40% 46% 54%;opacity:.92}
.s-hero .in{position:relative;z-index:2;max-width:74%}
.s-eye{font-family:"IBM Plex Mono";font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:#FFC7A6;font-weight:600}
.s-hero h3{font-family:"Archivo";font-weight:900;text-transform:uppercase;font-size:26px;line-height:1.05;margin:8px 0 0;letter-spacing:-.02em}
.s-hero p{color:#EBE0D6;font-size:12.5px;margin:10px 0 0;max-width:44ch}
.s-hero .btns{margin-top:16px;display:flex;gap:9px;flex-wrap:wrap}

.s-sec{padding:22px}
.s-sec.paper{background:#FAF8F4}
.s-h{font-family:"IBM Plex Mono";font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8A8078;font-weight:600;margin-bottom:14px}
.s-stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.s-stat{background:#fff;border:1px solid #EAE2D6;border-radius:10px;padding:14px}
.s-stat b{font-family:"Archivo";font-size:24px;color:#EE4A0E;display:block;line-height:1}
.s-stat span{font-size:11px;color:#726657;display:block;margin-top:6px}

.s-fil{margin-bottom:6px}
.s-fil .lab{font-size:11px;color:#726657;font-weight:600;margin:8px 0 6px}
.chip{display:inline-block;border:1.4px solid #D3C9BB;border-radius:20px;padding:6px 13px;font-size:11.5px;background:#fff;margin:0 6px 6px 0;color:#17130F}
.chip.o{background:#EE4A0E;border-color:#EE4A0E;color:#fff;font-weight:700}
.chip.g{background:#1F9E57;border-color:#1F9E57;color:#fff;font-weight:700}
.s-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-top:10px}
.s-card{border:1px solid #EAE2D6;border-radius:10px;background:#fff;padding:11px}
.s-card .img{height:70px;border-radius:6px;background:linear-gradient(135deg,#F1ECE4,#E7DFD3);display:flex;align-items:center;justify-content:center;color:#B9ADA2;font-size:11px}
.s-card b{display:block;margin-top:8px;font-size:13px}
.s-card .meta{font-size:11px;color:#8A8078;margin:2px 0 8px}
.s-card .row{display:flex;gap:6px}

.s-tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px}
.s-tab{font-size:11.5px;padding:6px 11px;border-radius:7px;border:1px solid #EAE2D6;background:#fff;color:#3C352D}
.s-tab.on{background:#17130F;color:#fff;border-color:#17130F;font-weight:700}
.s-tbl{width:100%;border-collapse:collapse;font-size:12px;background:#fff;border:1px solid #EAE2D6;border-radius:8px;overflow:hidden}
.s-tbl td{border-bottom:1px solid #EEE7DD;padding:8px 11px}
.s-tbl tr:last-child td{border-bottom:0}
.s-tbl td:first-child{color:#726657;width:48%}

.s-docs{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.s-doc{height:92px;border:1px solid #EAE2D6;border-radius:8px;background:#FBF8F3;display:flex;align-items:center;justify-content:center;color:#8A8078;font-size:11px;text-align:center;padding:6px}
.s-doc .ic{font-size:22px}
.s-cli{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
.s-cli div{height:56px;border:1px dashed #D3C9BB;border-radius:8px;background:#fff;display:flex;align-items:center;justify-content:center;color:#B9ADA2;font-size:11px}

.s-cta{background:linear-gradient(100deg,#17130F,#3C2110);color:#fff;padding:24px 22px}
.s-cta h3{font-family:"Archivo";font-weight:800;font-size:20px;margin:0 0 4px}
.s-cta p{color:#EBE0D6;font-size:12px;margin:0 0 14px}
.s-form{display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:9px}
.s-inp{background:#fff;border-radius:8px;padding:11px 12px;font-size:12px;color:#8A8078}
.s-ftr{background:#141210;color:#B9ADA2;padding:20px 22px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px;font-size:11.5px}
.s-ftr b{color:#fff;display:block;margin-bottom:6px;font-size:12px}

.foot{padding:40px 0 70px;color:var(--muted);font-size:14px}
.foot b{color:var(--text)}

@media(max-width:900px){
  .step{grid-template-columns:1fr;gap:18px}
  .explain{position:static}
  .s-hero .in{max-width:100%}
  .s-form{grid-template-columns:1fr 1fr}
  .s-stats,.s-docs,.s-cli{grid-template-columns:repeat(2,1fr)}
  .s-grid{grid-template-columns:1fr 1fr}
  .s-ftr{grid-template-columns:1fr 1fr}
}
@media(max-width:560px){
  .s-nav,.s-ph{display:none}
  .s-grid,.s-stats,.s-docs,.s-cli,.s-form{grid-template-columns:1fr}
}
</style>

<div class="wrap top">
  <div class="eyebrow">Прототип сайта · для согласования</div>
  <h1>Сайт компании «Сатурн»</h1>
  <p>Так будет устроена главная страница: слева — как это увидит ваш клиент, справа — простыми словами, что делает каждый блок и чем он помогает продавать. Дизайн черновой, важна структура и логика.</p>
  <div class="legend">
    <span><span class="dotc" style="background:#EE4A0E"></span>Оранжевый — <b>действие</b> (кнопки, ссылки)</span>
    <span><span class="dotc" style="background:#1F9E57"></span>Зелёный — <b>заявка / контакт</b></span>
    <span><span class="dotc" style="background:#8C949C"></span>Серым — <b>фото/контент</b>, добавим позже</span>
  </div>
</div>

<!-- 1. ШАПКА -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site">
      <div class="s-hdr"><img src="LOGO_COLOR" alt="Сатурн">
        <div class="s-nav"><span>Каталог</span><span>О компании</span><span>Сертификаты</span><span>Контакты</span></div>
        <span class="s-sp"></span><span class="s-ph">☎ +7 960 953-48-88</span><a class="s-btn o">Оставить заявку</a>
      </div>
    </div>
  </div></div>
  <div class="explain"><span class="badge">Блок 1 · Шапка</span>
    <h2>Панель навигации</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Логотип, меню разделов, телефон и заметную кнопку «Оставить заявку». Панель закреплена — видна при прокрутке всей страницы.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Связаться можно <b>с любого места</b> сайта: телефон и заявка всегда под рукой — клиент не «теряется».</div>
    </div>
  </div>
</div>

<!-- 2. HERO -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-hero"><div class="in">
      <img src="LOGO_WHITE" alt="Сатурн" style="height:30px">
      <div class="s-eye" style="margin-top:14px">Официальный дилер · опт</div>
      <h3>Удобрения и средства<br>защиты растений — оптом</h3>
      <p>Реликт ДВ · Волский Биохим · Фертика. Подберём препараты под культуру и задачу, отгрузим оптом.</p>
      <div class="btns"><a class="s-btn o">Смотреть каталог</a><a class="s-btn ghost">Оставить заявку</a></div>
    </div></div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 2 · Первый экран</span>
    <h2>Обложка сайта</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Крупный заголовок — что продаёте и кому, — и две кнопки: «Смотреть каталог» и «Оставить заявку». Без поиска, чтобы было проще.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">За <b>3 секунды</b> посетитель понимает, что попал по адресу, и сразу видит, куда нажать.</div>
    </div>
  </div>
</div>

<!-- 3. ЦИФРЫ -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-sec paper"><div class="s-stats">
      <div class="s-stat"><b>15+</b><span>лет на рынке</span></div>
      <div class="s-stat"><b>500+</b><span>препаратов в наличии</span></div>
      <div class="s-stat"><b>3</b><span>производителя-партнёра</span></div>
      <div class="s-stat"><b>1000+ т</b><span>отгружаем в год</span></div>
    </div></div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 3 · Цифры</span>
    <h2>Компания в цифрах</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">4 коротких факта: опыт, ассортимент, партнёры, объём отгрузок.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Быстро формирует <b>доверие</b>: с такой компанией имеет смысл работать. (Цифры подставим ваши реальные.)</div>
    </div>
  </div>
</div>

<!-- 4. КАТАЛОГ -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-sec">
      <div class="s-h">Каталог</div>
      <div class="s-fil"><div class="lab">Категория:</div>
        <span class="chip o">Все</span><span class="chip">Минеральные удобрения</span><span class="chip">Защита растений</span></div>
      <div class="s-fil"><div class="lab">Бренд:</div>
        <span class="chip g">Все</span><span class="chip">Реликт ДВ</span><span class="chip">Волский Биохим</span><span class="chip">Фертика</span></div>
      <div class="s-grid">
        <div class="s-card"><div class="img">фото</div><b>Препарат №1</b><div class="meta">Реликт ДВ · СЗР</div><div class="row"><a class="s-btn ghost sm">Подробнее</a><a class="s-btn o sm">Запросить цену</a></div></div>
        <div class="s-card"><div class="img">фото</div><b>Препарат №2</b><div class="meta">Фертика · удобрение</div><div class="row"><a class="s-btn ghost sm">Подробнее</a><a class="s-btn o sm">Запросить цену</a></div></div>
        <div class="s-card"><div class="img">фото</div><b>Препарат №3</b><div class="meta">Волский Биохим · СЗР</div><div class="row"><a class="s-btn ghost sm">Подробнее</a><a class="s-btn o sm">Запросить цену</a></div></div>
      </div>
    </div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 4 · Каталог</span>
    <h2>Товары с фильтрами</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Один список товаров и два ряда кнопок: по категории (удобрения / защита) и по бренду. Кнопки можно совмещать — например «Защита» + «Фертика».</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Клиент за <b>пару кликов</b> находит нужный препарат. Цены не показываем — работаем по заявке (опт): у каждого товара кнопка <b>«Запросить цену»</b>.</div>
    </div>
  </div>
</div>

<!-- 5. КАРТОЧКА -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru/product</span></div>
    <div class="site"><div class="s-sec paper">
      <div class="s-tabs"><span class="s-tab on">Описание</span><span class="s-tab">Нормы применения</span><span class="s-tab">Характеристики</span><span class="s-tab">Документы</span></div>
      <table class="s-tbl">
        <tr><td>Действующее вещество</td><td>…</td></tr>
        <tr><td>Норма расхода</td><td>…</td></tr>
        <tr><td>Культуры</td><td>…</td></tr>
        <tr><td>Фасовка</td><td>…</td></tr>
      </table>
      <div style="margin-top:12px;display:flex;gap:8px"><a class="s-btn ghost sm">Скачать паспорт (PDF)</a><a class="s-btn o sm">Запросить цену</a></div>
    </div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 5 · Карточка препарата</span>
    <h2>Характеристики препарата</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Подробная информация во вкладках: описание, нормы применения, характеристики, паспорт PDF.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Агроном получает <b>все данные для решения</b> прямо на сайте — и тут же может «Запросить цену».</div>
    </div>
  </div>
</div>

<!-- 6. СЕРТИФИКАТЫ -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-sec">
      <div class="s-h">Сертификаты и регалии</div>
      <div class="s-docs">
        <div class="s-doc"><div><div class="ic">📄</div>Сертификат</div></div>
        <div class="s-doc"><div><div class="ic">📄</div>СГР</div></div>
        <div class="s-doc"><div><div class="ic">🏅</div>Диплом</div></div>
        <div class="s-doc"><div><div class="ic">🏆</div>Награда</div></div>
      </div>
    </div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 6 · Сертификаты</span>
    <h2>Документы и регалии</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Ряд документов: сертификаты, свидетельства о госрегистрации (СГР), дипломы. Можно открыть и увеличить.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Подтверждает, что продукция <b>официальная и легальная</b> — снимает главные сомнения покупателя.</div>
    </div>
  </div>
</div>

<!-- 7. С КЕМ РАБОТАЕМ -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-sec paper">
      <div class="s-h">С кем работаем</div>
      <div class="s-cli"><div>Клиент / лого</div><div>Клиент / лого</div><div>Клиент / лого</div><div>Клиент / лого</div></div>
    </div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 7 · Клиенты</span>
    <h2>Нам доверяют</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Логотипы хозяйств и компаний, которые уже с вами работают (по желанию — короткие отзывы).</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Работает принцип «<b>другим подошло — подойдёт и мне</b>»: живое доказательство, что вам доверяют.</div>
    </div>
  </div>
</div>

<!-- 8. ФОРМА -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-cta">
      <h3>Не нашли нужный препарат?</h3>
      <p>Подберём под вашу задачу и отгрузим оптом</p>
      <div class="s-form"><span class="s-inp">Имя</span><span class="s-inp">Телефон *</span><span class="s-inp">Что интересует</span><a class="s-btn g">Отправить</a></div>
    </div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 8 · Заявка</span>
    <h2>Форма обратной связи</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Простая форма: имя, телефон, что интересует. Заявка приходит вам на почту nilov@sssaturn.ru.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Это <b>главный шаг к сделке</b>. Фраза «Не нашли препарат? Подберём» ловит даже тех, кто не нашёл товар в каталоге.</div>
    </div>
  </div>
</div>

<!-- 9. ПОДВАЛ -->
<div class="wrap step">
  <div class="preview"><div class="frame"><div class="chrome"><i></i><i></i><i></i><span class="url">sssaturn.ru</span></div>
    <div class="site"><div class="s-ftr">
      <div><b>«Сатурн»</b>Официальный дилер удобрений и СЗР</div>
      <div><b>Разделы</b>Каталог · Удобрения · СЗР · О компании</div>
      <div><b>Контакты</b>Телефон · WhatsApp · Telegram · почта · адрес</div>
      <div><b>Реквизиты</b>ИНН / ОГРН</div>
    </div></div>
  </div></div>
  <div class="explain"><span class="badge">Блок 9 · Подвал</span>
    <h2>Нижний блок</h2>
    <div class="card">
      <div class="k">Что видит клиент</div>
      <div class="v">Все контакты и мессенджеры, разделы сайта и реквизиты компании.</div>
      <div class="k">Зачем это нужно</div>
      <div class="v why">Второй шанс связаться, а реквизиты показывают, что вы <b>реальная компания</b> — это важно для оптовых закупок.</div>
    </div>
  </div>
</div>

<div class="wrap foot">
  <b>Что дальше:</b> согласуем структуру и тексты → добавим ваши фото, цифры, документы и товары → наложим фирменный дизаайн (как в заглушке) → публикуем на sssaturn.ru.
</div>
'''
HTML = HTML.replace("LOGO_COLOR", logo_color).replace("LOGO_WHITE", logo_white)
open('present-saturn.html','w').write(HTML)
print("written present-saturn.html, size:", len(HTML))
