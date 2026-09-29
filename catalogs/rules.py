# -*- coding: utf-8 -*-
"""Решения заказчика, которые отличают сайт от таблицы-первоисточника.

Таблица заказчика остаётся нетронутой, а эти правила применяются при импорте
(import_source_xlsx.py) и при сверке прайса (verify_price_pdf.py) одинаково —
иначе сверка начнёт считать исключённые позиции «потерянными».
"""

# 2026-09-29: позиции бренда OYYO убраны из прайса и каталога на сайте.
EXCLUDE_BRANDS = {'OYYO'}


def excluded(row):
    """True, если позицию не публикуем."""
    brand = (row.get('Бренд') or '').strip()
    name = (row.get('Название') or '').strip()
    return brand in EXCLUDE_BRANDS or any(name.startswith(b + ' ') for b in EXCLUDE_BRANDS)
