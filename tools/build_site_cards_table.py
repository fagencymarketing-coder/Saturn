#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Единый справочник карточек сайта (только препараты, без семян).
Источник — живой магазин Tilda (API), то есть ровно то, что видит покупатель.
Выход:
  docs/KARTOCHKI-SAYTA.md    — таблица для просмотра с телефона (GitHub)
  docs/KARTOCHKI-SAYTA.xlsx  — та же таблица, сортируемая
Запуск:  python3 tools/build_site_cards_table.py
Пересобирать после любой правки цен/описаний на сайте.
"""
import json, re, sys, urllib.request, pathlib, datetime

API = ("https://store.tildaapi.com/api/getproductslist/"
       "?storepartuid=527746460323&recid=4384406801&size=500")
ROOT = pathlib.Path(__file__).resolve().parent.parent
SNAP = ROOT / "catalogs" / "store_api_snapshot.json"  # не обязателен


def load():
    # Берём живой API; если сети нет — локальный снимок рядом.
    try:
        req = urllib.request.Request(API, headers={"User-Agent": "saturn-sync"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        if SNAP.exists():
            sys.stderr.write(f"API недоступен ({e}); беру снимок {SNAP}\n")
            return json.loads(SNAP.read_text("utf-8"))
        raise


def price_str(p):
    """Строка цены, как на карточке, без рассрочки и хвоста про предоплату."""
    if p.get("price") in (None, "", "0", 0):
        return "Цена по запросу"
    t = p.get("text") or ""
    m = re.search(r"Цена:\s*(.+?)(?:\.\s|\.$|$)", t)
    s = m.group(1).strip() if m else ""
    s = re.sub(r"\(?\s*рассрочк\S*[^)]*\)?", "", s)      # убрать рассрочку
    s = re.sub(r"\s{2,}", " ", s).strip(" ·,")
    if not s:  # запасной вариант — число + ₽
        v = str(p["price"]).rstrip("0").rstrip(".").replace(".", ",")
        s = f"{v} ₽"
    return s


def full_descr(p):
    """Полное описание без ценового хвоста и html-переносов."""
    t = p.get("text") or ""
    t = re.split(r"Цена:", t)[0]
    t = re.sub(r"<br\s*/?>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\s{2,}", " ", t).strip()
    return t or (p.get("descr") or "")


def ch_get(p, title):
    """Первое значение характеристики с данным заголовком."""
    for c in (p.get("characteristics") or []):
        if c.get("title") == title:
            return (c.get("value") or "").strip()
    return ""


def cultures(p):
    vals = [c["value"] for c in (p.get("characteristics") or [])
            if c.get("title") == "Культура"]
    # уникальные, с сохранением порядка
    seen, out = set(), []
    for v in vals:
        if v not in seen:
            seen.add(v); out.append(v)
    return ", ".join(out)


def main():
    data = load()
    prep = [p for p in data["products"] if "/catalog/" in (p.get("url") or "")]
    prep.sort(key=lambda p: p.get("sort", 0))
    rows = []
    for i, p in enumerate(prep, 1):
        rows.append({
            "n": i,
            "name": (p.get("title") or "").strip(),
            "price": price_str(p),
            "sub": (p.get("descr") or "").strip(),
            "descr": full_descr(p),
            "cult": cultures(p),
            "sku": p.get("sku") or "",
        })

    # --- Семена (отдельный лист) ---
    sem = [p for p in data["products"] if "/semena/" in (p.get("url") or "")]
    sem.sort(key=lambda p: p.get("sort", 0))
    srows = []
    for i, p in enumerate(sem, 1):
        srows.append({
            "n": i,
            "name": (p.get("title") or "").strip(),
            "sub": (p.get("descr") or "").strip(),       # Культура · Тип
            "yield": ch_get(p, "Урожайность"),
            "ripe": ch_get(p, "Спелость"),
            "veg": ch_get(p, "Вегетационный период"),
            "qual": ch_get(p, "Качество"),
            "orig": ch_get(p, "Оригинатор"),
            "descr": full_descr(p),
            "sku": p.get("sku") or "",
        })

    today = datetime.date.today().isoformat()
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)

    # --- Markdown ---
    md = [f"# Карточки сайта — справочник",
          "",
          f"Единый источник: что реально на живом сайте. Собрано {today}. "
          f"Препаратов: **{len(rows)}**, семян: **{len(srows)}**. "
          "Пересобирается из магазина: `python3 tools/build_site_cards_table.py`. "
          "Руками не править — перезатрётся.",
          "",
          "## Препараты",
          "",
          "| № | Название | Цена | Подзаголовок | Описание | Культуры |",
          "|--:|---|---|---|---|---|"]
    for r in rows:
        cells = [str(r["n"]), r["name"], r["price"], r["sub"],
                 r["descr"].replace("|", "\\|"), r["cult"]]
        md.append("| " + " | ".join(c.replace("\n", " ") for c in cells) + " |")
    md += ["",
           "## Семена",
           "",
           "Цена договорная (по запросу). Ключевое — урожайность и характеристики.",
           "",
           "| № | Название | Культура · Тип | Урожайность | Спелость | Вег. период | Качество | Описание |",
           "|--:|---|---|---|---|---|---|---|"]
    for r in srows:
        cells = [str(r["n"]), r["name"], r["sub"], r["yield"], r["ripe"],
                 r["veg"], r["qual"].replace("|", "\\|"),
                 r["descr"].replace("|", "\\|")]
        md.append("| " + " | ".join(c.replace("\n", " ") for c in cells) + " |")
    (docs / "KARTOCHKI-SAYTA.md").write_text("\n".join(md) + "\n", "utf-8")

    # --- XLSX (если есть openpyxl) ---
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font, Alignment, PatternFill
        wb = Workbook(); ws = wb.active; ws.title = "Препараты"
        heads = ["№", "Название", "Цена (на сайте)", "Подзаголовок",
                 "Описание", "Культуры", "sku"]
        ws.append(heads)
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="141210")
            c.alignment = Alignment(vertical="center")
        for r in rows:
            ws.append([r["n"], r["name"], r["price"], r["sub"],
                       r["descr"], r["cult"], r["sku"]])
        widths = [5, 32, 22, 34, 70, 30, 24]
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[chr(64 + i)].width = w
        for row in ws.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(vertical="top", wrap_text=True)
        ws.freeze_panes = "A2"

        # Лист «Семена»
        ws2 = wb.create_sheet("Семена")
        heads2 = ["№", "Название", "Культура · Тип", "Урожайность", "Спелость",
                  "Вег. период", "Качество", "Оригинатор", "Описание", "sku"]
        ws2.append(heads2)
        for c in ws2[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="141210")
            c.alignment = Alignment(vertical="center")
        for r in srows:
            ws2.append([r["n"], r["name"], r["sub"], r["yield"], r["ripe"],
                        r["veg"], r["qual"], r["orig"], r["descr"], r["sku"]])
        widths2 = [5, 26, 26, 34, 16, 16, 44, 40, 60, 22]
        for i, w in enumerate(widths2, 1):
            ws2.column_dimensions[chr(64 + i)].width = w
        for row in ws2.iter_rows(min_row=2):
            for c in row:
                c.alignment = Alignment(vertical="top", wrap_text=True)
        ws2.freeze_panes = "A2"

        wb.save(docs / "KARTOCHKI-SAYTA.xlsx")
        xlsx_ok = True
    except ImportError:
        xlsx_ok = False

    print(f"готово: {len(rows)} препаратов")
    print(f"  docs/KARTOCHKI-SAYTA.md")
    print(f"  docs/KARTOCHKI-SAYTA.xlsx" if xlsx_ok else "  (xlsx пропущен: нет openpyxl)")


if __name__ == "__main__":
    main()
