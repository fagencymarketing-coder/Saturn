# -*- coding: utf-8 -*-
"""Прайс-лист ООО «Сатурн» в фирменном стиле → HTML → PDF.

🔴 Требование заказчика (2026-09-28): СУТЬ — ровно как в подтверждённой
таблице, ОФОРМЛЕНИЕ — единое. Цифры и слова не меняются и не сокращаются;
единообразие знаков (валюта, тире, единицы) даёт catalogs/typography.py.
Название позиции не трогается вовсе — там 13-40-13 это марка, а не диапазон.
Источник данных: catalogs/catalog_tech.json (99 позиций, подтверждён заказчиком).
Рендер: Playwright/Chromium, A4.
"""
import json, io, base64, os, html, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from typography import polish, price as price_fmt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def b64(p, mime):
    with open(os.path.join(ROOT, p), 'rb') as f:
        return f"data:{mime};base64," + base64.b64encode(f.read()).decode()

FONTS = {w: b64(f"catalogs/_fonts/Montserrat-{w}.ttf", "font/ttf") for w in (400,600,700,800)}
LOGO  = b64("assets/logo/saturn-logo-white.png", "image/png")

ORDER = ["Удобрения","Листовые подкормки","Обработка семян",
         "Гербициды","Десиканты","Протравители","Инсектициды","Фунгициды",
         "Адъюванты и спецпрепараты"]
# подпись колонки «состав» зависит от раздела
DV = {"Гербициды":"Действующее вещество","Десиканты":"Действующее вещество",
      "Протравители":"Действующее вещество","Инсектициды":"Действующее вещество",
      "Фунгициды":"Действующее вещество","Адъюванты и спецпрепараты":"Состав"}


# ── Нормы расхода ───────────────────────────────────────────────────────────
# 🔴 2026-09-28: заказчик объявил подтверждённую таблицу единым первоисточником
# И ДЛЯ САЙТА, И ДЛЯ ПРАЙСА. Поэтому нормы берутся ИЗ НЕЁ, а не из старого
# прайса. Словарь ниже оставлен как след сверки со старым прайсом
# (source-files/Prais-Saturn.pdf) — он БОЛЬШЕ НЕ ПРИМЕНЯЕТСЯ.
USE_OLD_PRICE_NORMS = False
NORM = {
 "Реликт Р Старт (протравитель)":"0,4 л/т",
 "Микромак":"2 л/т",
 "Экомак":"0,5 л/т",
 "Реликт Р":"0,2–0,5 л/га",
 "Микроэл Универсальный":"0,2 л/га",
 "Страда N":"2–5 л/га", "Страда P":"2–5 л/га", "Страда K":"2–5 л/га",
 "FERTIKA Листовое Старт 13-40-13":"Семена 1–2 кг/т; по вегетации 2–3 кг/га",
 "FERTIKA Листовое 18-18-18":"2–4 кг/га",
 "FERTIKA Листовое 10-5-40":"2–4 кг/га",
 "FERTIKA Листовое 4-13-36":"2–4 кг/га",
 "FERTIKA Листовое 19-6-20":"2–3 кг/га",
 "FERTIKA Плюс 16-20-27":"2–4 кг/га",
 "FERTIKA Плюс 6,4-11-31":"2–4 кг/га",
 "FERTIKA Плюс 12-11-26":"2–4 кг/га",
 "Реликт М Молибден":"0,2–0,5 л/га", "Реликт М Сера":"0,3–1,5 л/га",
 "Реликт М Бор":"0,5–1,5 л/га", "Реликт М Цинк":"0,3–1,5 л/га",
 "Реликт М Кремний":"0,2–0,5 л/га",
 "Волски Моно-Бор":"0,2–1 л/га", "Волски Моно-Цинк":"0,2–1 л/га",
 "Волски Моно-Железо":"0,2–1 л/га", "Волски Моно-Сера":"0,2–1 л/га",
 "Волски Моно-Медь":"0,2–1 л/га",
 "Диформа Марганец-Цинк":"0,5–2 л/га", "Диформа Бор-Молибден":"0,5–1,5 л/га",
 "Диформа Магний-Цинк":"0,5–2 л/га", "Диформа Марганец-Бор":"0,5–2 л/га",
 "Диформа Кальций-Азот":"0,5–2 л/га", "Диформа Магний-Марганец":"0,5–2 л/га",
 "Диформа Кремний-Калий":"0,2–1 л/га", "Диформа Кобальт-Селен":"0,5–1 л/га",
 "Волски Оптим":"30–150 мл на 100 л", "Биостик Терра":"1 л/га на 100–200 л воды/га",
 "Вега 90, Ж":"0,2–0,5", "Вега АнтиПена, КЭ":"0,01–0,05", "Вега Баланс, ВР":"0,1–1",
 "Вега Голд, Ж":"0,01–0,1", "Вега Клей":"0,8–1,5", "Вега Турбо":"0,1–0,3",
 "Вега Эмульс, КЭ":"0,5–1",
 # СЗР — нормы из прайса (мин–макс, л/кг на га или т)
 "Альфард, ВР":"1,5–2", "Ампир Экстра, ВР":"1,4–5", "Ампир, ВР":"2–8",
 "Ранголи-Базорон, ВР":"1,5–4", "Гекстар, ВДГ":"0,01–0,05", "Зазофен, ВР":"1–1,5",
 "Злакофф, КЭ":"0,2–1", "Кирасир, СЭ":"0,3–0,5", "Клео, ВДГ":"0,12",
 "Клордин, КЭ":"0,7–1", "Курсар, ВР":"0,75–1", "Метолс, КЭ":"1,3–1,6",
 "Поллукс, ЭМВ":"0,8–1", "Спика, КЭ":"0,5–1", "Тифилагро, ВДГ":"0,006–0,025",
 "Торпеда, ВДГ":"0,025–0,035", "Укротитель, КЭ":"0,4–0,9", "Царумин, ВК":"0,5–1,5",
 "Челленджер, ВРК":"1–1,2",
 "Ранголи-Реголон, ВР":"2", "Ригель Форте, ВР":"0,7–1,8",
 "Анкер Трио, КС":"0,4–0,5", "Тиара, КС":"0,5–1", "Тиль Про, КС":"0,5–9",
 "Тореадор Макси, КС":"0,3–12",
 "Альфацин, КЭ":"0,1–0,3", "Гарпун, КС":"0,1–0,5", "Кастра, КС":"0,1–0,25",
 "Ранголи Норил, КЭ":"0,5–1",
 "Атлант Супер":"0,4–0,75", "Гранберг Про, КЭ":"0,2–0,6", "Гранберг, КЭ":"0,75–1",
}
# Уточнения состава по прайсу
SOSTAV = {
 "Диформа Магний-Цинк":"Магний 75 г/л · Цинк 30 г/л · Азот 52 г/л · Сера 37 г/л · "
                       "Фосфор 14 г/л · Калий 37 г/л",
}

rows = json.load(io.open(os.path.join(ROOT,'catalogs/catalog_tech.json'), encoding='utf-8'))
groups = {c: [r for r in rows if r['Категория'] == c] for c in ORDER}
# ни одна позиция не должна потеряться: всё, что не попало в известные
# разделы (например, с пустой категорией), уходит в «Прочие позиции»
_placed = {id(r) for g in groups.values() for r in g}
_rest = [r for r in rows if id(r) not in _placed]
if _rest:
    groups["Прочие позиции"] = _rest
    ORDER = ORDER + ["Прочие позиции"]
assert sum(len(g) for g in groups.values()) == len(rows), "позиции потерялись при группировке"

def esc(x): return html.escape(str(x or ''))

def short(t, limit):
    """Для прайса нужна основная норма, а не вся агротехника:
    обрезаем по первому предложению, если строка длинная."""
    t = str(t or '').strip()
    if len(t) <= limit: return t
    cut = t[:limit]
    for sep in ('. ', '; ', ' · ', ', ', ' '):
        i = cut.rfind(sep)
        if i > limit * 0.45: return cut[:i].rstrip(' ,;·') + '…'
    return cut.rstrip(' ,;·') + '…'

def first_sentence(t, limit=150):
    """В прайсе нужна норма, а не вся агротехника: оставляем до первой точки.
    Если и после этого длинно — режем по границе перечисления, не посреди слова."""
    t = str(t or '').strip()
    i = t.find('. ')
    if i > 8: t = t[:i]
    if len(t) <= limit: return t
    cut = t[:limit]
    for sep in ('; ', ', ', ' '):
        j = cut.rfind(sep)
        if j > limit * 0.5: return cut[:j].rstrip(' ,;') + '…'
    return cut.rstrip(' ,;') + '…'

def table(cat, items):
    dv = DV.get(cat, "Состав / элементы питания")
    head = f"""<tr class="th">
      <th class="c1">Наименование</th><th class="c2">{dv}</th>
      <th class="c3">Норма расхода</th><th class="c4">Фасовка</th><th class="c5">Цена</th></tr>"""
    tr = []
    for i, r in enumerate(items):
        price = esc(price_fmt(r['Цена_итог'], r['Название']))
        cls = 'req' if 'запрос' in price.lower() else 'pr'
        pack = esc(polish(r.get('Фасовка_прайс') or r.get('Фасовка_каталог')))
        tr.append(f"""<tr class="{'odd' if i%2 else ''}">
          <td class="c1 nm">{esc(r['Название'])}</td>
          <td class="c2 dv">{esc(polish(r['Состав_ДВ']))}</td>
          <td class="c3 nr">{esc(polish(r['Норма_расхода']))}</td>
          <td class="c4 pk">{pack}</td>
          <td class="c5 {cls}">{price}</td></tr>""")
    lbl = (f'<tr class="lblrow"><td colspan="5">'
           f'<span class="lbl"><i></i>{esc(cat)}<b>{len(items)}</b></span></td></tr>')
    return f"""<section class="sec"><table>{lbl}{head}{''.join(tr)}</table></section>"""

body = "".join(table(c, groups[c]) for c in ORDER if groups[c])

HTML = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<style>
@font-face{{font-family:M;src:url({FONTS[400]});font-weight:400}}
@font-face{{font-family:M;src:url({FONTS[600]});font-weight:600}}
@font-face{{font-family:M;src:url({FONTS[700]});font-weight:700}}
@font-face{{font-family:M;src:url({FONTS[800]});font-weight:800}}
@page{{size:A4 landscape;margin:0 0 14mm}}
.pad{{padding:0 14mm 4mm}}
*{{box-sizing:border-box}}
body{{font-family:M,sans-serif;color:#1A1A1A;margin:0;font-size:8.4pt;line-height:1.38}}
.cover{{background:#141210;color:#fff;padding:14mm 14mm 11mm;margin-bottom:9mm}}
.cover img{{height:13mm;display:block;margin-bottom:9mm}}
.cover h1{{font-size:24pt;font-weight:800;letter-spacing:-.02em;margin:0 0 3mm}}
.cover h1 span{{color:#FF4200}}
.cover .sub{{font-size:10pt;font-weight:600;color:rgba(255,255,255,.72);margin-bottom:8mm}}
.cover .meta{{display:flex;gap:16mm;font-size:8pt;color:rgba(255,255,255,.62);line-height:1.6}}
.cover .meta b{{display:block;color:#fff;font-weight:700;font-size:8.6pt}}
.team{{display:flex;gap:5mm;margin-top:8mm;padding-top:7mm;
 border-top:1px solid rgba(255,255,255,.14)}}
.team>div{{flex:1;font-size:7pt;color:rgba(255,255,255,.62);line-height:1.5}}
.team i{{display:block;font-style:normal;font-weight:700;font-size:6.2pt;
 letter-spacing:.1em;text-transform:uppercase;color:#FF4200;margin-bottom:2mm}}
.team b{{display:block;color:#fff;font-weight:700;font-size:7.8pt;margin-bottom:1mm}}
.sec{{break-inside:auto;margin-bottom:0}}
.lblrow td{{border:0;padding:7mm 0 3mm;background:#fff!important}}
.lbl{{display:inline-flex;align-items:center;gap:3mm;font-size:8pt;font-weight:700;
 letter-spacing:.14em;text-transform:uppercase;color:#1A1A1A}}
.lbl i{{width:7mm;height:2px;background:#FF4200;display:block}}
.lbl b{{font-weight:600;letter-spacing:0;color:#B7B0A8;text-transform:none}}
/* заголовок раздела и шапка таблицы не должны разъезжаться по страницам */
tr.lblrow{{break-after:avoid;break-inside:avoid}}
tr.th{{break-after:avoid;break-inside:avoid}}
table{{width:100%;border-collapse:collapse}}
.th th{{font-size:7pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
 color:#8A837C;text-align:left;padding:2mm 2mm;border-bottom:1px solid #E7E3DE}}
td{{padding:1.45mm 2.5mm;vertical-align:top;border-bottom:1px solid #F0EDE9}}
tr.odd td{{background:#F7F7F6}}
tr{{break-inside:avoid}}
.th th.c5{{text-align:right}}
.c1{{width:19%}} .c2{{width:36%}} .c3{{width:20%}} .c4{{width:14%}} .c5{{width:11%}}
.nm{{font-weight:700}}
.dv{{font-size:7.4pt;color:#6B6560}}
.nr{{font-size:7.4pt;color:#3D3A37}}
.pk{{font-size:7.4pt;color:#6B6560}}
.pr{{font-weight:800;color:#FF4200;text-align:right;white-space:nowrap}}
.req{{font-weight:600;color:#8A837C;text-align:right;font-size:7.4pt}}
.note{{margin-top:6mm;background:#F7F7F6;border-left:3px solid #FF4200;
 padding:4mm 5mm;font-size:8pt;line-height:1.5}}
.note b{{font-weight:700}}
</style></head><body>
<div class="cover">
  <img src="{LOGO}" alt="Сатурн">
  <h1>Прайс-лист <span>2026</span></h1>
  <div class="sub">Удобрения · средства защиты растений · адъюванты</div>
  <div class="meta">
    <div><b>ООО «Сатурн»</b>ИНН 2801274078 · КПП 222501001<br>ОГРН 1232800002709<br>
      г. Барнаул, пр. Ленина 56 / Шевченко 52А, пом. Н13</div>
    <div><b>sssaturn.ru</b>Прайс действует с 12.01.2026<br>Цены при 100% предоплате, за 1 л / 1 кг</div>
  </div>
  <div class="team">
    <div><i>Генеральный директор</i><b>Нилова Анастасия</b>+7 (913) 022-48-88<br>nilova.anastasia@sssaturn.ru</div>
    <div><i>Коммерческие вопросы</i><b>Нилов Алексей</b>+7 (960) 953-48-88<br>nilov@sssaturn.ru</div>
    <div><i>Агрономический отдел</i><b>Хаблак Андрей</b>+7 (963) 502-38-55<br>khablak.a@sssaturn.ru</div>
    <div><i>Семена</i><b>Боровиков Виталий</b>+7 (960) 948-83-40<br>borovikov.v@sssaturn.ru</div>
    <div><i>Закуп</i><b>Пекарский Сергей</b>+7 (903) 947-73-53<br>psv@sssaturn.ru</div>
    <div><i>Документы и договоры</i><b>Слободина Марина</b>+7 (983) 170-01-70<br>slobodina.marina@sssaturn.ru</div>
  </div>
</div>
<div class="pad">{body}
<div class="note"><b>В стоимость препаратов входит доставка, хранение и полное
сопровождение по циклу от посевной до уборки урожая.</b><br>
Цены указаны при 100% предоплате, за 1 л или 1 кг. Действуют с 12.01.2026.
Актуальную цену по позициям «по запросу» уточняйте в отделе продаж.</div></div>
</body></html>"""

out = os.path.join(ROOT, 'catalogs/_price.html')
io.open(out, 'w', encoding='utf-8').write(HTML)
print("html:", out, len(HTML)//1024, "КБ")
