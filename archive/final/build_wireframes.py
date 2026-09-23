CSS = '''<style>
*{box-sizing:border-box}
body{margin:0;background:#fff;color:#111;font-family:Arial,Helvetica,sans-serif;font-size:14px}
.page{max-width:1200px;margin:0 auto}
.b{border:1.5px dashed #9aa0a6;background:#f3f4f6;margin:8px;padding:14px;border-radius:6px}
.b .t{font-weight:bold;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#5a6067;margin-bottom:8px}
.note{font-size:12px;color:#6b7280}
.row{display:flex;gap:8px;flex-wrap:wrap}
.col{flex:1 1 0;min-width:0}
.btn{display:inline-block;border:1.5px solid #111;border-radius:6px;padding:8px 14px;background:#fff;font-size:13px;font-weight:bold;margin:3px 4px 3px 0}
.btn.solid{background:#111;color:#fff}
.pill{display:inline-block;border:1.2px solid #9aa0a6;border-radius:20px;padding:5px 12px;font-size:12px;background:#fff;margin:3px 4px 0 0}
.inp{border:1.5px solid #9aa0a6;border-radius:6px;background:#fff;padding:12px;color:#6b7280;font-size:13px}
.search{display:flex;gap:0;align-items:stretch}
.search .inp{flex:1;border-radius:6px 0 0 6px;border-right:0}
.search .btn{border-radius:0 6px 6px 0;margin:0}
.hdr{display:flex;align-items:center;gap:12px;border:1.5px solid #9aa0a6;background:#eef0f2;margin:8px;padding:12px;border-radius:6px}
.logo{border:1.5px solid #9aa0a6;border-radius:6px;padding:8px 14px;font-weight:bold;background:#fff}
.nav{display:flex;gap:14px;color:#5a6067;font-size:13px;flex-wrap:wrap}
.spacer{flex:1}
.grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
.grid4{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.card{border:1.5px dashed #9aa0a6;border-radius:6px;background:#fff;padding:12px;min-height:120px}
.ph{background:repeating-linear-gradient(45deg,#e5e7eb,#e5e7eb 8px,#eef0f2 8px,#eef0f2 16px);border:1px solid #d1d5db;border-radius:4px;height:70px;display:flex;align-items:center;justify-content:center;color:#9aa0a6;font-size:12px}
.tbl{width:100%;border-collapse:collapse;background:#fff;font-size:12px}
.tbl td,.tbl th{border:1px solid #d1d5db;padding:7px 9px;text-align:left}
.hero{min-height:220px}
.big{font-size:22px;font-weight:bold}
.mid{font-size:16px;font-weight:bold}
.varlabel{background:#111;color:#fff;padding:10px 16px;margin:8px;border-radius:6px;font-weight:bold}
.side{display:flex;gap:8px}
.side .filters{flex:0 0 240px}
.side .content{flex:1}
</style>'''

def page(title, body):
    return f"<!DOCTYPE html><html lang='ru'><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width, initial-scale=1'><title>{title}</title>{CSS}</head><body><div class='page'>{body}</div></body></html>"

def header(cta="Оставить заявку", with_search_mini=True):
    s = "<div class='search' style='flex:1;max-width:340px'><span class='inp'>🔍 Поиск препарата…</span><span class='btn solid'>Найти</span></div>" if with_search_mini else ""
    return f"""<div class='hdr'>
      <span class='logo'>ЛОГО «Сатурн»</span>
      <div class='nav'>Каталог · Удобрения · Защита растений · О компании · Контакты</div>
      <span class='spacer'></span>{s}
      <span class='note'>☎ +7 960 953-48-88</span>
      <span class='btn solid'>{cta}</span>
    </div>"""

def stats():
    return """<div class='b'><div class='t'>2 · Цифры о компании</div>
      <div class='grid4'>
        <div class='card' style='min-height:70px'><b>15+ лет</b><div class='note'>на рынке</div></div>
        <div class='card' style='min-height:70px'><b>500+</b><div class='note'>препаратов</div></div>
        <div class='card' style='min-height:70px'><b>3</b><div class='note'>производителя-партнёра</div></div>
        <div class='card' style='min-height:70px'><b>1000+ т</b><div class='note'>отгружено / год</div></div>
      </div></div>"""

def certs():
    return """<div class='b'><div class='t'>3 · Сертификаты и регалии</div>
      <div class='grid4'>
        <div class='ph'>Сертификат</div><div class='ph'>СГР</div><div class='ph'>Диплом</div><div class='ph'>Награда</div>
      </div><div class='note'>Ряд с возможностью открыть/увеличить документ</div></div>"""

def techspecs():
    return """<div class='b'><div class='t'>4 · Технические характеристики препаратов</div>
      <div class='note' style='margin-bottom:8px'>Пример карточки: табы «Описание · Нормы применения · Характеристики · Документы»</div>
      <table class='tbl'>
        <tr><th>Параметр</th><th>Значение</th></tr>
        <tr><td>Действующее вещество</td><td>…</td></tr>
        <tr><td>Норма расхода</td><td>…</td></tr>
        <tr><td>Культуры</td><td>…</td></tr>
        <tr><td>Фасовка</td><td>…</td></tr>
      </table>
      <div style='margin-top:8px'><span class='btn'>Скачать паспорт (PDF)</span><span class='btn solid'>Запросить цену</span></div></div>"""

def partners():
    return """<div class='b'><div class='t'>5 · С кем работаем</div>
      <div class='grid4'><div class='ph'>Клиент/лого</div><div class='ph'>Клиент/лого</div><div class='ph'>Клиент/лого</div><div class='ph'>Клиент/лого</div></div>
      <div class='note'>Отзывы / логотипы хозяйств, которым доверяют</div></div>"""

def leadform(big=False):
    h = "min-height:150px" if big else ""
    return f"""<div class='b' style='{h}'><div class='t'>Форма обратной связи (заявка)</div>
      <div class='row'>
        <span class='inp col'>Имя</span><span class='inp col'>Телефон *</span><span class='inp col'>Что интересует (препарат/культура)</span>
      </div>
      <div style='margin-top:8px'><span class='btn solid'>Отправить заявку</span> <span class='note'>→ заявка уходит на nilov@sssaturn.ru</span></div></div>"""

def footer():
    return """<div class='b' style='background:#eef0f2'><div class='t'>6 · Подвал</div>
      <div class='row'>
        <div class='col'>ЛОГО · короткое описание</div>
        <div class='col'>Меню: Каталог, Удобрения, СЗР, О компании</div>
        <div class='col'>Контакты: телефон, WhatsApp, Telegram, почта, адрес</div>
        <div class='col'>Реквизиты: ИНН/ОГРН</div>
      </div></div>"""

def product_grid(with_price_req=True):
    cards = ""
    for i in range(6):
        cards += "<div class='card'><div class='ph' style='height:50px'>фото</div><div style='margin-top:6px'><b>Препарат №%d</b></div><div class='note'>производитель · назначение</div><div style='margin-top:6px'><span class='btn'>Подробнее</span><span class='btn solid'>Запросить цену</span></div></div>" % (i+1)
    return f"<div class='grid3'>{cards}</div>"

def filters_inline():
    return """<div class='row' style='margin-bottom:8px'>
      <span class='inp col'>Категория: Удобрения / СЗР ▾</span>
      <span class='inp col'>Культура ▾</span>
      <span class='inp col'>Назначение (гербицид/фунгицид…) ▾</span>
      <span class='inp col'>Производитель ▾</span></div>"""

def producer_tabs():
    return "<div style='margin-bottom:8px'><span class='btn solid'>Все</span><span class='btn'>Реликт ДВ</span><span class='btn'>Волский Биохим</span><span class='btn'>Фертика</span></div>"

# ================= VARIANT 1: ПОИСК В ПРИОРИТЕТЕ =================
hero1 = f"""<div class='b hero'><div class='t'>1 · Главный слайд (Hero) — поиск в центре</div>
  <div class='big'>Заголовок: «Удобрения, СЗР и семена — оптом, с подбором под задачу»</div>
  <div class='note' style='margin:8px 0'>Подзаголовок 1–2 строки о выгоде</div>
  <div class='search' style='margin:10px 0'><span class='inp' style='flex:1'>🔍 Введите препарат, культуру или задачу («против сорняков в пшенице»)</span><span class='btn solid'>Найти препарат</span></div>
  <div>{('').join(["<span class='pill'>%s</span>"%x for x in ['Гербициды','Фунгициды','Инсектициды','Протравители','Мин. удобрения','По культуре']])}</div>
  <div style='margin-top:10px'><span class='btn solid'>Подобрать препарат</span><span class='btn'>Открыть каталог</span></div>
</div>"""
catalog1 = f"""<div class='b'><div class='t'>3 · Товары: Удобрения и Защита растений (3 производителя)</div>
  {producer_tabs()}{filters_inline()}{product_grid()}
  <div style='margin-top:8px'><span class='btn'>Показать ещё</span></div></div>"""
v1 = header() + hero1 + stats() + catalog1 + techspecs() + certs() + partners() + leadform(big=True) + footer()

# ================= VARIANT 2: КАТАЛОГ С ФИЛЬТРАМИ (сайдбар) =================
hero2 = f"""<div class='b'><div class='t'>1 · Главный слайд (компактный) + поиск</div>
  <div class='mid'>Короткий заголовок + подзаголовок</div>
  <div class='search' style='margin:10px 0;max-width:640px'><span class='inp' style='flex:1'>🔍 Поиск препарата по названию/культуре</span><span class='btn solid'>Найти</span></div>
  <span class='btn solid'>Оставить заявку</span><span class='btn'>Каталог</span></div>"""
catalog2 = f"""<div class='b'><div class='t'>3 · Каталог с фильтрами (сайдбар слева)</div>
  {producer_tabs()}
  <div class='side'>
    <div class='filters card'><b>Фильтры</b>
      <div class='note' style='margin-top:8px'>Категория</div><div class='inp'>Удобрения / СЗР</div>
      <div class='note' style='margin-top:8px'>Культура</div><div class='inp'>▾</div>
      <div class='note' style='margin-top:8px'>Назначение</div><div class='inp'>гербицид/фунгицид…</div>
      <div class='note' style='margin-top:8px'>Производитель</div><div class='inp'>Реликт/Волский/Фертика</div>
      <div style='margin-top:10px'><span class='btn solid'>Применить</span></div>
    </div>
    <div class='content'>{product_grid()}</div>
  </div></div>"""
v2 = header() + hero2 + catalog2 + stats() + certs() + techspecs() + partners() + leadform() + footer()

# ================= VARIANT 3: ДОВЕРИЕ + ЗАЯВКА (lead-focused) =================
hero3 = f"""<div class='b hero'><div class='t'>1 · Главный слайд — split: текст+заявка | поиск</div>
  <div class='row'>
    <div class='col b' style='background:#fff'>
      <div class='big'>Заголовок с оффером</div>
      <div class='note' style='margin:8px 0'>3 буллета: подбор под задачу · опт · документы/СГР</div>
      <div class='mid' style='margin-top:6px'>Быстрая заявка:</div>
      <div class='inp' style='margin:6px 0'>Телефон *</div>
      <span class='btn solid'>Получить подбор и цену</span>
    </div>
    <div class='col b' style='background:#fff'>
      <div class='mid'>Найти препарат</div>
      <div class='search' style='margin:10px 0'><span class='inp' style='flex:1'>🔍 препарат / культура</span><span class='btn solid'>Найти</span></div>
      <div>{('').join(["<span class='pill'>%s</span>"%x for x in ['Гербициды','Фунгициды','Удобрения','По культуре']])}</div>
    </div>
  </div></div>"""
producers_tiles = """<div class='b'><div class='t'>3 · Товары по производителям (крупные плитки → в каталог)</div>
  <div class='grid3'>
    <div class='card'><div class='ph'>Реликт ДВ</div><div class='note' style='margin-top:6px'>Удобрения / СЗР</div><span class='btn solid'>Смотреть</span></div>
    <div class='card'><div class='ph'>Волский Биохим</div><div class='note' style='margin-top:6px'>Удобрения / СЗР</div><span class='btn solid'>Смотреть</span></div>
    <div class='card'><div class='ph'>Фертика</div><div class='note' style='margin-top:6px'>Удобрения / СЗР</div><span class='btn solid'>Смотреть</span></div>
  </div>
  <div style='margin-top:8px'>""" + filters_inline() + product_grid() + "</div></div>"
cta_mid = "<div class='b' style='background:#eef0f2'><div class='t'>Промежуточный CTA</div><div class='mid'>Не нашли нужный препарат? Подберём под вашу задачу</div><span class='btn solid'>Оставить заявку</span></div>"
v3 = header() + hero3 + stats() + producers_tiles + certs() + techspecs() + partners() + cta_mid + leadform(big=True) + footer()

open('wireframe-V1-search.html','w').write(page("Прототип V1 — Поиск в приоритете", v1))
open('wireframe-V2-filters.html','w').write(page("Прототип V2 — Каталог с фильтрами", v2))
open('wireframe-V3-lead.html','w').write(page("Прототип V3 — Доверие и заявка", v3))
print("built V1, V2, V3")
