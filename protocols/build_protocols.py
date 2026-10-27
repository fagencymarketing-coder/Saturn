# -*- coding: utf-8 -*-
"""Копии актов производственной проверки для публикации — HTML для печати в PDF.

Текст и показатели набраны заново по оригиналу, поэтому замазанных мест в
документе нет. Не раскрывается только то, что защищено договором с хозяйством:
его название и адрес (остался регион), ФИО и должности участников, подписи,
печати, блок ЭДО, номер и дата договора.

Решение 27.10.2026: производителей называем открыто — ООО НПП «Генезис»
(бренд Relict Organics) и ООО «Волски Биохим». Культура и сорт всегда
указываются; если сорта нет в наборе — его нет и в оригинале акта.
"""
import base64, html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, 'catalogs', '_fonts')


def b64(path):
    return base64.b64encode(open(path, 'rb').read()).decode()


def face(w, f):
    return ("@font-face{font-family:Montserrat;font-weight:%s;font-style:normal;"
            "src:url(data:font/ttf;base64,%s) format('truetype')}" % (w, b64(os.path.join(FONTS, f))))


FONTCSS = ''.join(face(w, f) for w, f in
                  [(400, 'Montserrat-400.ttf'), (600, 'Montserrat-600.ttf'),
                   (700, 'Montserrat-700.ttf'), (800, 'Montserrat-800.ttf')])
LOGO = b64(os.path.join(ROOT, 'assets', 'logo', 'saturn-logo-color.png'))

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:Montserrat,sans-serif;color:#141210;font-size:11pt;line-height:1.55;
     width:210mm;padding:18mm 20mm 16mm}
.top{display:flex;justify-content:space-between;align-items:flex-start;
     border-bottom:1px solid #EDE9E4;padding-bottom:14px;margin-bottom:26px}
.top img{height:30px}
.tag{font-size:8pt;font-weight:600;letter-spacing:.08em;text-transform:uppercase;
     color:#8A837C;text-align:right;line-height:1.5}
h1{font-size:19pt;font-weight:800;line-height:1.2;margin-bottom:6px}
.sub{font-size:10.5pt;color:#8A837C;margin-bottom:26px}
h2{font-size:9pt;font-weight:700;letter-spacing:.08em;text-transform:uppercase;
   color:#8A837C;margin:24px 0 10px}
table{width:100%;border-collapse:collapse}
td{padding:8px 0;border-bottom:1px solid #EDE9E4;vertical-align:top}
td.k{width:42%;color:#8A837C;padding-right:16px}
td.v{font-weight:600}
.res{display:flex;gap:10px;margin-top:4px}
.cell{flex:1;background:#F6F5F3;border-radius:12px;padding:14px 16px}
.cell .lab{font-size:8.5pt;color:#8A837C;margin-bottom:4px}
.cell .num{font-size:17pt;font-weight:800;line-height:1.1}
.cell.acc{background:#FF4200;color:#fff}
.cell.acc .lab{color:#FFD9CC}
.cell .add{font-size:9.5pt;font-weight:600;margin-top:2px}
.cell.acc .add{color:#FFD9CC}
ul{list-style:none}
li{position:relative;padding-left:16px;margin-bottom:6px;color:#4A4540;font-size:10pt}
li:before{content:'';position:absolute;left:0;top:8px;width:5px;height:5px;
          border-radius:50%;background:#FF4200}
.foot{margin-top:30px;padding-top:12px;border-top:1px solid #EDE9E4;
      font-size:8.5pt;color:#8A837C;line-height:1.6}
"""


def esc(s):
    return html.escape(str(s))


def render(a):
    sort = a['sort']
    if ',' in sort:
        base, tail = sort.split(',', 1)
        title_sort = ' «%s», %s' % (esc(base.strip()), esc(tail.strip()))
    else:
        title_sort = ' «%s»' % esc(sort) if sort else ''
    name = esc(a['crop']) + title_sort
    scheme = ''.join('<tr><td class="k">%s</td><td class="v">%s</td></tr>' % (esc(k), esc(v))
                     for k, v in a['scheme'])
    eco = ''.join('<tr><td class="k">%s</td><td class="v">%s</td></tr>' % (esc(k), esc(v))
                  for k, v in a['eco'])
    notes = ''.join('<li>%s</li>' % esc(n) for n in a['notes'])
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8">
<title>Акт производственной проверки № {a['n']} — Сатурн</title>
<style>{FONTCSS}{CSS}</style></head><body>
<div class="top">
  <img src="data:image/png;base64,{LOGO}" alt="Сатурн">
  <div class="tag">Акт производственной проверки<br>Копия для публикации № {a['n']}</div>
</div>

<h1>{name}</h1>
<div class="sub">{esc(a['region'])} · {esc(a['season'])} · опытная площадь {esc(a['area'])}</div>

<h2>Результат</h2>
<div class="res">
  <div class="cell"><div class="lab">Контроль</div><div class="num">{esc(a['control'])} ц/га</div></div>
  <div class="cell"><div class="lab">Опыт</div><div class="num">{esc(a['exp'])} ц/га</div></div>
  <div class="cell acc"><div class="lab">Прибавка</div><div class="num">+{esc(a['pct'])}%</div><div class="add">+{esc(a['gain'])} ц/га</div></div>
</div>

<h2>Схема обработки</h2>
<table>{scheme}</table>

<h2>Экономика</h2>
<table>{eco}</table>

<h2>Примечания</h2>
<ul>{notes}</ul>

<div class="foot">
Копия акта производственной проверки: текст и показатели набраны по оригиналу.
Хозяйство указано по региону — его название и реквизиты защищены договором.
Оригинал с подписями сторон хранится в ООО «Сатурн» и предоставляется по запросу.<br>
Продукция в схеме обработки: ООО НПП «Генезис», бренд Relict Organics
(«Реликт Р», «Реликт М») · ООО «Волски Биохим» (Страда, Микроэл, Микромак,
Биосил, Экомак, Моно-, Диформа).<br>
ООО «Сатурн» · sssaturn.ru · +7 (960) 953-48-88
</div>
</body></html>"""


if __name__ == '__main__':
    acts = json.load(open(os.path.join(HERE, 'trials.json'), encoding='utf-8'))
    out = os.path.join(HERE, 'html')
    os.makedirs(out, exist_ok=True)
    for a in acts:
        p = os.path.join(out, 'protokol-%d.html' % a['n'])
        open(p, 'w', encoding='utf-8').write(render(a))
    print('готово:', len(acts), 'файлов в', out)
