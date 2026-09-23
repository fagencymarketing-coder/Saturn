CSS = '''<style>
*{box-sizing:border-box}
body{margin:0;background:#fff;color:#111;font-family:Arial,Helvetica,sans-serif;font-size:14px}
.page{max-width:1200px;margin:0 auto}
.b{border:1.5px dashed #9aa0a6;background:#f3f4f6;margin:8px;padding:16px;border-radius:6px}
.b .t{font-weight:bold;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#5a6067;margin-bottom:10px}
.note{font-size:12px;color:#6b7280}
.row{display:flex;gap:8px;flex-wrap:wrap}
.col{flex:1 1 0;min-width:0}
.btn{display:inline-block;border:1.5px solid #111;border-radius:6px;padding:9px 16px;background:#fff;font-size:13px;font-weight:bold;margin:3px 6px 3px 0}
.btn.solid{background:#111;color:#fff}
.inp{border:1.5px solid #9aa0a6;border-radius:6px;background:#fff;padding:12px;color:#6b7280;font-size:13px}
.hdr{display:flex;align-items:center;gap:14px;border:1.5px solid #9aa0a6;background:#eef0f2;margin:8px;padding:12px 16px;border-radius:6px}
.logo{border:1.5px solid #9aa0a6;border-radius:6px;padding:8px 14px;font-weight:bold;background:#fff}
.nav{display:flex;gap:16px;color:#5a6067;font-size:13px;flex-wrap:wrap}
.spacer{flex:1}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.grid2{display:grid;grid-template-columns:repeat(2,1fr);gap:10px}
.card{border:1.5px dashed #9aa0a6;border-radius:6px;background:#fff;padding:14px;min-height:110px}
.ph{background:repeating-linear-gradient(45deg,#e5e7eb,#e5e7eb 8px,#eef0f2 8px,#eef0f2 16px);border:1px solid #d1d5db;border-radius:4px;height:80px;display:flex;align-items:center;justify-content:center;color:#9aa0a6;font-size:12px}
.tbl{width:100%;border-collapse:collapse;background:#fff;font-size:12px}
.tbl td,.tbl th{border:1px solid #d1d5db;padding:7px 9px;text-align:left}
.big{font-size:24px;font-weight:bold}
.mid{font-size:16px;font-weight:bold}
.hero{min-height:200px}
.tag{display:inline-block;background:#111;color:#fff;font-size:11px;padding:3px 8px;border-radius:4px;margin-left:8px;vertical-align:middle}
</style>'''

body = f"""
<div class='hdr'>
  <span class='logo'>ЛОГО «Сатурн»</span>
  <div class='nav'>Каталог · О компании · Сертификаты · Контакты</div>
  <span class='spacer'></span>
  <span class='note'>☎ +7 960 953-48-88</span>
  <span class='btn solid'>Оставить заявку</span>
</div>

<div class='b hero'><div class='t'>1 · Главный слайд (Hero) — без поиска</div>
  <div class='big'>Удобрения и средства защиты растений — оптом</div>
  <div class='note' style='margin:10px 0 4px'>Подзаголовок: официальный дилер Реликт ДВ, Волский Биохим, Фертика. Подбор под культуру и задачу, отгрузка оптом.</div>
  <div style='margin-top:14px'><span class='btn solid'>Смотреть каталог</span><span class='btn'>Оставить заявку</span></div>
  <div class='note' style='margin-top:6px'>(1 статичная картинка-фон, 2 кнопки. Без поиска — быстро реализуемо)</div>
</div>

<div class='b'><div class='t'>2 · Цифры о компании</div>
  <div class='grid4'>
    <div class='card' style='min-height:70px'><b>15+ лет</b><div class='note'>на рынке</div></div>
    <div class='card' style='min-height:70px'><b>500+</b><div class='note'>препаратов в наличии</div></div>
    <div class='card' style='min-height:70px'><b>3</b><div class='note'>производителя-партнёра</div></div>
    <div class='card' style='min-height:70px'><b>1000+ т</b><div class='note'>отгружаем в год</div></div>
  </div></div>

<div class='b'><div class='t'>3 · Товары <span class='tag'>простая версия</span></div>
  <div class='note' style='margin-bottom:8px'>Шаг 1 — 2 категории:</div>
  <div class='grid2'>
    <div class='card'><div class='ph'>Минеральные удобрения</div><div style='margin-top:8px'><span class='btn solid'>Открыть</span></div></div>
    <div class='card'><div class='ph'>Защита растений (СЗР)</div><div style='margin-top:8px'><span class='btn solid'>Открыть</span></div></div>
  </div>
  <div class='note' style='margin:14px 0 8px'>Шаг 2 — 3 производителя (плитки-ссылки):</div>
  <div class='grid3'>
    <div class='card'><div class='ph'>Реликт ДВ</div><div class='note' style='margin-top:6px'>удобрения · СЗР</div><span class='btn'>Смотреть препараты</span></div>
    <div class='card'><div class='ph'>Волский Биохим</div><div class='note' style='margin-top:6px'>удобрения · СЗР</div><span class='btn'>Смотреть препараты</span></div>
    <div class='card'><div class='ph'>Фертика</div><div class='note' style='margin-top:6px'>удобрения · СЗР</div><span class='btn'>Смотреть препараты</span></div>
  </div>
  <div class='note' style='margin:14px 0 8px'>Список товаров — простые карточки (без фильтра/поиска):</div>
  <div class='grid3'>
    <div class='card'><div class='ph' style='height:50px'>фото</div><b>Препарат №1</b><div class='note'>производитель · назначение</div><div style='margin-top:6px'><span class='btn'>Подробнее</span><span class='btn solid'>Запросить цену</span></div></div>
    <div class='card'><div class='ph' style='height:50px'>фото</div><b>Препарат №2</b><div class='note'>производитель · назначение</div><div style='margin-top:6px'><span class='btn'>Подробнее</span><span class='btn solid'>Запросить цену</span></div></div>
    <div class='card'><div class='ph' style='height:50px'>фото</div><b>Препарат №3</b><div class='note'>производитель · назначение</div><div style='margin-top:6px'><span class='btn'>Подробнее</span><span class='btn solid'>Запросить цену</span></div></div>
  </div>
</div>

<div class='b'><div class='t'>4 · Технические характеристики препаратов</div>
  <div class='note' style='margin-bottom:8px'>Карточка препарата: описание + таблица характеристик + PDF-паспорт</div>
  <table class='tbl'>
    <tr><th>Параметр</th><th>Значение</th></tr>
    <tr><td>Действующее вещество</td><td>…</td></tr>
    <tr><td>Норма расхода</td><td>…</td></tr>
    <tr><td>Культуры</td><td>…</td></tr>
    <tr><td>Фасовка</td><td>…</td></tr>
  </table>
  <div style='margin-top:8px'><span class='btn'>Скачать паспорт (PDF)</span><span class='btn solid'>Запросить цену</span></div>
</div>

<div class='b'><div class='t'>5 · Сертификаты и регалии</div>
  <div class='grid4'><div class='ph'>Сертификат</div><div class='ph'>СГР</div><div class='ph'>Диплом</div><div class='ph'>Награда</div></div>
</div>

<div class='b'><div class='t'>6 · С кем работаем</div>
  <div class='grid4'><div class='ph'>Клиент/лого</div><div class='ph'>Клиент/лого</div><div class='ph'>Клиент/лого</div><div class='ph'>Клиент/лого</div></div>
</div>

<div class='b'><div class='t'>7 · Форма обратной связи (главный конверсионный блок)</div>
  <div class='mid' style='margin-bottom:8px'>Не нашли нужный препарат? Подберём под вашу задачу и отгрузим оптом</div>
  <div class='row'>
    <span class='inp col'>Имя</span><span class='inp col'>Телефон *</span><span class='inp col'>Что интересует (препарат / культура)</span>
  </div>
  <div style='margin-top:8px'><span class='btn solid'>Отправить заявку</span> <span class='note'>→ заявка на nilov@sssaturn.ru</span></div>
</div>

<div class='b' style='background:#eef0f2'><div class='t'>8 · Подвал</div>
  <div class='row'>
    <div class='col'>ЛОГО · короткое описание</div>
    <div class='col'>Меню: Каталог, Удобрения, СЗР, О компании</div>
    <div class='col'>Контакты: телефон, WhatsApp, Telegram, почта, адрес</div>
    <div class='col'>Реквизиты: ИНН/ОГРН</div>
  </div>
</div>
"""

html = f"<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Прототип — простая версия</title>{CSS}</head><body><div class='page'>{body}</div></body></html>"
open('wireframe-SIMPLE.html','w').write(html)
print("built SIMPLE")
