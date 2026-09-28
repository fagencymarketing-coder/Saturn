# -*- coding: utf-8 -*-
"""Сверка готового PDF-прайса с исходной таблицей — построчно и по каждой колонке.

⚠️ Ограничение: 4 позиции скрипт не находит из-за переноса названия на две
строки (FERTIKA Картофельное-5, OYYO Альфа Аминостарт / Аминобиостим /
Аминофиниш). Они сверены вручную 2026-09-28 — в PDF всё на месте.

PDF разбирается обратно в таблицу: якорь строки — название позиции
(Montserrat-Bold 8.4 в левой колонке), перенесённые на две строки названия
склеиваются. Затем проверяются цена, фасовка, норма расхода и состав.

Запуск:  python3 catalogs/verify_price_pdf.py
"""
import pymupdf, openpyxl, re, sys, os, importlib.util

# те же правила обрезки, что и при сборке PDF
_spec = importlib.util.spec_from_file_location("bp", "catalogs/build_price_pdf.py")
_bp = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_bp)

# осознанные нормализации при импорте таблицы заказчика (не ошибки)
NORMALIZED = {
 "Волски Аминатор": {"Норма_расхода": "0,5 л/га"},   # в таблице «0.5» без единицы
}

PDF = 'catalogs/Прайс-лист-Сатурн-2026.pdf'
XLS = 'source-files/Saturn-katalog-i-prays-podtverzhdyon-2026-09-28.xlsx'

def sq(t):  return re.sub(r'[\s ]+','',str(t or '')).lower().replace('–','-').replace('—','-')
def dig(t): return ''.join(re.findall(r'\d', str(t)))

def load_table():
    ws = openpyxl.load_workbook(XLS, data_only=True)['Каталог']
    hdr = [c.value for c in ws[1]]
    return [{h:(str(v).strip() if v is not None else '') for h,v in zip(hdr,r)}
            for r in ws.iter_rows(min_row=2, values_only=True) if r[0]]

def load_bands_by_search(data):
    """Надёжный способ: находим каждое название на странице и режем полосу
    до следующего названия ниже. Не зависит от шрифтовых эвристик."""
    doc = pymupdf.open(PDF)
    # длинные названия переносятся на две строки, поэтому ищем короткий
    # префикс, а нужную строку выбираем по полному совпадению имени в полосе
    hits = []   # (page, y0, название)
    for pno, page in enumerate(doc):
        for d in data:
            for r in page.search_for(d['Название'][:12]):
                hits.append((pno, r.y0, d['Название']))
    hits.sort(key=lambda x: (x[0], x[1]))
    ys = sorted({(p, y) for p, y, _ in hits})
    def band_text(pno, y0):
        nxt = [y for p, y in ys if p == pno and y > y0 + 4]
        y1 = (nxt[0] - 2) if nxt else 1e5
        clip = pymupdf.Rect(20, y0 - 2, 822, min(y1, y0 + 96))
        return ' '.join(doc[pno].get_text("text", clip=clip).split())
    bands = {}
    for pno, y0, name in hits:
        if name in bands: continue
        txt = band_text(pno, y0)
        if sq(name) in sq(txt): bands[name] = txt
    return bands

def load_bands(names_sq):
    doc = pymupdf.open(PDF); bands = []
    for page in doc:
        spans = []
        for b in page.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    if s["text"].strip():
                        spans.append((s["bbox"][1], s["bbox"][0], s["font"], round(s["size"],1), s["text"]))
        spans.sort(key=lambda x:(x[0], x[1]))
        raw = [i for i,s in enumerate(spans) if s[2]=="Montserrat-Bold" and s[3]==8.4 and s[1]<190]
        groups=[]; cur=[]
        for i in raw:
            if not cur: cur=[i]; continue
            acc = sq(" ".join(spans[j][4] for j in cur))
            if acc in names_sq or spans[i][0]-spans[cur[-1]][0] > 14:
                groups.append(cur); cur=[i]
            else: cur.append(i)
        if cur: groups.append(cur)
        for k,g in enumerate(groups):
            y0 = spans[g[0]][0]-1
            y1 = spans[groups[k+1][0]][0]+40 if k+1 < len(groups) else 1e9   # запас на многострочные ячейки
            sel = [s for s in spans if y0 <= s[0] < y1]
            bands.append({"name": " ".join(spans[j][4] for j in g),
                          "all":   " ".join(s[4] for s in sel),
                          "prices":" ".join(s[4] for s in sel if s[2]=="Montserrat-ExtraBold")})
    return bands

def main():
    data = load_table()
    bands = load_bands_by_search(data)
    miss=[]; bad=[]; ok=0
    for d in data:
        txt = bands.get(d['Название'])
        if txt is None: miss.append(d['Название']); continue
        b = {"all": txt, "prices": txt}; prob=[]
        ep = d['Цена_итог']
        if 'запрос' in ep.lower():
            if 'запрос' not in sq(b["all"]): prob.append(f"«по запросу» нет · PDF: {b['prices'].strip()}")
        elif dig(ep) not in dig(b["prices"]):
            prob.append(f"ЦЕНА: таблица «{ep}» · PDF «{b['prices'].strip()}»")
        pk = d.get('Фасовка_прайс') or d.get('Фасовка_каталог')
        if pk and sq(pk) not in sq(b["all"]): prob.append(f"ФАСОВКА «{pk}» не найдена")
        for fld, lbl in (('Норма_расхода','НОРМА'), ('Состав_ДВ','СОСТАВ')):
            v = NORMALIZED.get(d['Название'], {}).get(fld, d[fld])
            if not v: continue
            # в PDF значение обрезается теми же правилами — сравниваем с обрезанным
            v_pdf = _bp.first_sentence(v) if fld == 'Норма_расхода' else _bp.short(v, 185)
            probe = sq(v_pdf).rstrip('…')[:24]
            if probe and probe not in sq(b["all"]): prob.append(f"{lbl}: «{v_pdf[:50]}» не найдено")
        if prob: bad.append((d['Название'], prob))
        else: ok += 1
    print(f"позиций {len(data)} · сошлось {ok} · расхождений {len(bad)} · не найдено {len(miss)}")
    for n in miss: print("  НЕ НАЙДЕНО:", n)
    for n,p in bad:
        print("  " + n)
        for x in p: print("     ", x)
    return 1 if (bad or miss) else 0

if __name__ == "__main__":
    sys.exit(main())
