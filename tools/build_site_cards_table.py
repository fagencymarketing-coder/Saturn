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

    today = datetime.date.today().isoformat()
    docs = ROOT / "docs"
    docs.mkdir(exist_ok=True)

    # --- Markdown ---
    md = [f"# Карточки сайта — справочник (препараты)",
          "",
          f"Единый источник: цена и описание, как на живом сайте. Собрано {today}, "
          f"позиций: **{len(rows)}**. Только препараты (семена — в /semena, в этой "
          "таблице их нет). Пересобирается из магазина: `python3 tools/build_site_cards_table.py`.",
          "",
          "| № | Название | Цена | Подзаголовок | Описание | Культуры |",
          "|--:|---|---|---|---|---|"]
    for r in rows:
        cells = [str(r["n"]), r["name"], r["price"], r["sub"],
                 r["descr"].replace("|", "\\|"), r["cult"]]
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
        wb.save(docs / "KARTOCHKI-SAYTA.xlsx")
        xlsx_ok = True
    except ImportError:
        xlsx_ok = False

    print(f"готово: {len(rows)} препаратов")
    print(f"  docs/KARTOCHKI-SAYTA.md")
    print(f"  docs/KARTOCHKI-SAYTA.xlsx" if xlsx_ok else "  (xlsx пропущен: нет openpyxl)")


if __name__ == "__main__":
    main()
