# -*- coding: utf-8 -*-
"""Прайс-лист ООО «Сатурн» в фирменном стиле → HTML → PDF.
Источник данных: catalogs/catalog_tech.json (99 позиций, подтверждён заказчиком).
Рендер: Playwright/Chromium, A4.
"""
import json, io, base64, os, html

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


# ── Нормы расхода ИЗ ПРАЙСА «САТУРНА» ───────────────────────────────────────
# Прайс — собственный документ компании, поэтому в прайс-листе его нормы
# имеют приоритет над каталогами производителей. Сверено построчно
# с source-files/Prais-Saturn.pdf (стр. 1–5), 2026-09-28.
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
}
# Уточнения состава по прайсу
SOSTAV = {
 "Диформа Магний-Цинк":"Магний 75 г/л · Цинк 30 г/л · Азот 52 г/л · Сера 37 г/л · "
                       "Фосфор 14 г/л · Калий 37 г/л",
}

rows = json.load(io.open(os.path.join(ROOT,'catalogs/catalog_tech.json'), encoding='utf-8'))
groups = {c: [r for r in rows if r['Категория'] == c] for c in ORDER}

def esc(x): return html.escape(str(x or ''))

def short(t, limit):
    """Для прайса нужна основная норма, а не вся агротехника:
    обрезаем по первому предложению, если строка длинная."""
    t = str(t or '').strip()
    if len(t) <= limit: return t
    cut = t[:limit]
    for sep in ('. ', '; '):
        i = cut.rfind(sep)
        if i > limit * 0.45: return cut[:i]
    return cut.rstrip(' ,;·') + '…'

def first_sentence(t):
    """В прайсе нужна норма, а не вся агротехника: оставляем до первой точки."""
    t = str(t or '').strip()
    i = t.find('. ')
    return (t[:i] if i > 8 else t)[:110]

def table(cat, items):
    dv = DV.get(cat, "Состав / элементы питания")
    head = f"""<tr class="th">
      <th class="c1">Наименование</th><th class="c2">{dv}</th>
      <th class="c3">Норма расхода</th><th class="c4">Фасовка</th><th class="c5">Цена</th></tr>"""
    tr = []
    for i, r in enumerate(items):
        price = esc(r['Цена_итог'])
        cls = 'req' if 'запрос' in price.lower() else 'pr'
        pack = esc(r.get('Фасовка_прайс') or r.get('Фасовка_каталог'))
        tr.append(f"""<tr class="{'odd' if i%2 else ''}">
          <td class="c1 nm">{esc(r['Название'])}</td>
          <td class="c2 dv">{esc(SOSTAV.get(r['Название']) or short(r['Состав_ДВ'],150))}</td>
          <td class="c3 nr">{esc(NORM.get(r['Название']) or first_sentence(r['Норма_расхода']))}</td>
          <td class="c4 pk">{pack}</td>
          <td class="c5 {cls}">{price}</td></tr>""")
    return f"""<section class="sec">
      <div class="lbl"><i></i>{esc(cat)}<span>{len(items)}</span></div>
      <table>{head}{''.join(tr)}</table></section>"""

body = "".join(table(c, groups[c]) for c in ORDER if groups[c])

HTML = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<style>
@font-face{{font-family:M;src:url({FONTS[400]});font-weight:400}}
@font-face{{font-family:M;src:url({FONTS[600]});font-weight:600}}
@font-face{{font-family:M;src:url({FONTS[700]});font-weight:700}}
@font-face{{font-family:M;src:url({FONTS[800]});font-weight:800}}
@page{{size:A4;margin:0 0 17mm}}
.pad{{padding:0 12mm 4mm}}
*{{box-sizing:border-box}}
body{{font-family:M,sans-serif;color:#1A1A1A;margin:0;font-size:8.2pt;line-height:1.35}}
.cover{{background:#141210;color:#fff;padding:16mm 12mm 12mm;margin-bottom:10mm}}
.cover img{{height:13mm;display:block;margin-bottom:9mm}}
.cover h1{{font-size:26pt;font-weight:800;letter-spacing:-.02em;margin:0 0 3mm}}
.cover h1 span{{color:#FF4200}}
.cover .sub{{font-size:10pt;font-weight:600;color:rgba(255,255,255,.72);margin-bottom:8mm}}
.cover .meta{{display:flex;gap:16mm;font-size:8pt;color:rgba(255,255,255,.62);line-height:1.6}}
.cover .meta b{{display:block;color:#fff;font-weight:700;font-size:8.6pt}}
.team{{display:flex;gap:6mm;margin-top:8mm;padding-top:7mm;
 border-top:1px solid rgba(255,255,255,.14)}}
.team>div{{flex:1;font-size:7.4pt;color:rgba(255,255,255,.62);line-height:1.5}}
.team i{{display:block;font-style:normal;font-weight:700;font-size:6.6pt;
 letter-spacing:.1em;text-transform:uppercase;color:#FF4200;margin-bottom:2mm}}
.team b{{display:block;color:#fff;font-weight:700;font-size:8.2pt;margin-bottom:1mm}}
.sec{{break-inside:auto;margin-bottom:7mm}}
.lbl{{display:flex;align-items:center;gap:3mm;font-size:8pt;font-weight:700;
 letter-spacing:.14em;text-transform:uppercase;color:#1A1A1A;margin:0 0 3mm;
 break-after:avoid}}
.lbl i{{width:7mm;height:2px;background:#FF4200;display:block}}
.lbl span{{font-weight:600;letter-spacing:0;color:#B7B0A8;text-transform:none}}
table{{width:100%;border-collapse:collapse}}
.th th{{font-size:7pt;font-weight:700;letter-spacing:.06em;text-transform:uppercase;
 color:#8A837C;text-align:left;padding:2mm 2mm;border-bottom:1px solid #E7E3DE}}
td{{padding:1.8mm 2mm;vertical-align:top;border-bottom:1px solid #F0EDE9}}
tr.odd td{{background:#F7F7F6}}
tr{{break-inside:avoid}}
.th th.c5{{text-align:right}}
.c1{{width:25%}} .c2{{width:29%}} .c3{{width:19%}} .c4{{width:11%}} .c5{{width:16%}}
.nm{{font-weight:700}}
.dv{{font-size:7.2pt;color:#6B6560}}
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
