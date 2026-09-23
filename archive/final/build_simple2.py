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
.btn.sm{padding:8px 12px;font-size:12px}
.inp{border:1.5px solid #9aa0a6;border-radius:6px;background:#fff;padding:12px;color:#6b7280;font-size:13px}
.hdr{display:flex;align-items:center;gap:14px;border:1.5px solid #9aa0a6;background:#eef0f2;margin:8px;padding:12px 16px;border-radius:6px}
.logo{border:1.5px solid #9aa0a6;border-radius:6px;padding:8px 14px;font-weight:bold;background:#fff}
.nav{display:flex;gap:16px;color:#5a6067;font-size:13px;flex-wrap:wrap}
.spacer{flex:1}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.card{border:1.5px dashed #9aa0a6;border-radius:6px;background:#fff;padding:12px;min-height:110px}
.ph{background:repeating-linear-gradient(45deg,#e5e7eb,#e5e7eb 8px,#eef0f2 8px,#eef0f2 16px);border:1px solid #d1d5db;border-radius:4px;height:80px;display:flex;align-items:center;justify-content:center;color:#9aa0a6;font-size:12px}
.tbl{width:100%;border-collapse:collapse;background:#fff;font-size:12px}
.tbl td,.tbl th{border:1px solid #d1d5db;padding:7px 9px;text-align:left}
.big{font-size:24px;font-weight:bold}
.mid{font-size:16px;font-weight:bold}
.hero{min-height:200px}
.tag{display:inline-block;background:#111;color:#fff;font-size:11px;padding:3px 8px;border-radius:4px;margin-left:8px;vertical-align:middle}
.lbl{font-size:12px;color:#5a6067;font-weight:bold;margin:10px 0 6px}
.chip{display:inline-block;border:1.4px solid #9aa0a6;border-radius:20px;padding:7px 14px;font-size:13px;background:#fff;margin:0 6px 6px 0}
.chip.on{background:#111;color:#fff;border-color:#111;font-weight:bold}
</style>'''

def pcard(n, prod, cat):
    return f"<div class='card'><div class='ph' style='height:50px'>фото</div><div style='margin-top:6px'><b>Препарат №{n}</b></div><div class='note'>{prod} · {cat}</div><div style='margin-top:4px'><span class='btn sm'>Подробнее</span><span class='btn sm solid'>Запросить цену</span></div></div>"

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
</div>

<div class='b'><div class='t'>2 · Цифры о компании</div>
  <div class='grid4'>
    <div class='card' style='min-height:70px'><b>15+ лет</b><div class='note'>на рынке</div></div>
    <div class='card' style='min-height:70px'><b>500+</b><div class='note'>препаратов в наличии</div></div>
    <div class='card' style='min-height:70px'><b>3</b><div class='note'>производителя-партнёра</div></div>
    <div class='card' style='min-height:70px'><b>1000+ т</b><div class='note'>отгружаем в год</div></div>
  </div></div>

<div class='b'><div class='t'>3 · Каталог товаров <span class='tag'>1 сетка + 2 фильтра</span></div>
  <div class='lbl'>Категория:</div>
  <span class='chip on'>Все</span><span class='chip'>Минеральные удобрения</span><span class='chip'>Защита растений (СЗР)</span>
  <div class='lbl'>Бренд:</div>
  <span class='chip on'>Все</span><span class='chip'>Реликт ДВ</span><span class='chip'>Волский Биохим</span><span class='chip'>Фертика</span>
  <div class='note' style='margin:8px 0'>Клик по кнопкам отбирает карточки, фильтры совмещаются (напр. «СЗР» + «Фертика»). По умолчанию — «Все / Все».</div>
  <div class='grid3'>
    {pcard(1,'Реликт ДВ','СЗР')}{pcard(2,'Фертика','Удобрения')}{pcard(3,'Волский Биохим','СЗР')}
    {pcard(4,'Фертика','Удобрения')}{pcard(5,'Реликт ДВ','Удобрения')}{pcard(6,'Волский Биохим','СЗР')}
  </div>
  <div style='margin-top:10px'><span class='btn'>Показать ещё</span></div>
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
html = f"<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>Прототип — простая версия (обновл.)</title>{CSS}</head><body><div class='page'>{body}</div></body></html>"
open('wireframe-SIMPLE.html','w').write(html)
print("updated SIMPLE")
