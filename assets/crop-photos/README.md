# assets/crop-photos — фото культур

Извлечено из каталогов партнёров (`source-files/`) через pymupdf.
Используются в блоке «Семена»: одно фото на культуру, общее для всех её сортов.

| Файл | Размер | Источник | Где нужно |
|---|---|---|---|
| рапс.png | 1081×402 | Буклет «Волски Биохим» | гибрид «Новосёл» |
| подсолнечник.png | 1081×469 | Буклет «Волски Биохим» | гибрид «Ампир» |
| пшеница.png | 1081×727 | Буклет «Волски Биохим» | 4 сорта пшеницы яровой |
| ячмень.png | 895×495 | Буклет «Волски Биохим» | 3 сорта ячменя |
| соя.png | 1089×739 | Буклет «Волски Биохим» | 6 сортов сои |
| кукуруза.png | 1081×727 | Буклет «Волски Биохим» | запас |
| всходы-зерновых.png | 610×516 | Буклет «Волски Биохим» | запас |
| клевер.png | 1081×727 | Буклет «Волски Биохим» | запас |

🔴 **Не хватает: горох и гречиха** — ни в одном каталоге партнёров их нет.
Нужен подбор со стоков либо фото от заказчика.

⚠️ Рапс и подсолнечник — горизонтальные (1081×402 и 1081×469). Для карточек
4:3 их придётся кадрировать, запас по высоте небольшой.

## cards/ — фото для карточек гибридов (4:3), 2026-09-29
Временные, до фото упаковок от заказчика. Вырезаны из снимков культур выше.
- `seed-novosel-cl.jpg` — рапс, 536×402
- `seed-ampir-10.jpg` — подсолнечник, левая часть кадра, 625×469
- `seed-ampir-25.jpg` — подсолнечник, правая часть кадра, 625×469

У двух Ampir разные фрагменты одного снимка — чтобы соседние карточки не
повторяли друг друга. Разрешение хватает для карточки ~300px на обычном
экране; на ретине будет мягковато — заменить, когда появятся исходники.

## cards/seed-crop-*.jpg — квадраты 1:1 для внутренних карточек сортов, 2026-09-29
Одно фото на культуру, общее для всех её сортов.
- `seed-crop-pshenitsa.jpg` — пшеница озимая и яровая, 727×727
- `seed-crop-yachmen.jpg` — ячмень, 495×495 (на ретине мягковато)
- `seed-crop-soya.jpg` — соя, 739×739
Для гороха, гречихи и картофеля фото нет — карточка без фото идёт в одну колонку.

## cards/seed-crop-<культура>-<n>.jpg — фото культур для карточек сортов (4:3, 1200×900), 2026-09-29
По 1–3 кадра на культуру, у соседних сортов разные кадры. Вариант 1 у пшеницы, ячменя, сои — из наших снимков выше.
Остальные — Wikimedia Commons, **только CC0 и общественное достояние**: разрешено коммерческое использование без указания автора.

| Файл | Лицензия | Источник |
|---|---|---|
| `seed-crop-pshenitsa-2.jpg` | cc0 | https://commons.wikimedia.org/wiki/File:Arno_Smit_2016_(Unsplash).jpg |
| `seed-crop-pshenitsa-3.jpg` | cc0 | https://commons.wikimedia.org/wiki/File:Wheat_stalks.jpg |
| `seed-crop-yachmen-2.jpg` | cc0 | https://commons.wikimedia.org/wiki/File:Barley_field,_Ehrenbach,_detail.jpg |
| `seed-crop-yachmen-3.jpg` | cc0 | https://commons.wikimedia.org/wiki/File:Barley_field,_Ehrenbach,_evening_sun.jpg |
| `seed-crop-soya-2.jpg` | public domain | https://commons.wikimedia.org/wiki/File:An_unhealthy_soybean_field_in_South_Dakota_on_8_August_2024_-_4.jpg |
| `seed-crop-goroh-1.jpg` | public domain | https://commons.wikimedia.org/wiki/File:Vora_Tosca_pea_field_200809.jpg |
| `seed-crop-goroh-2.jpg` | cc0 | https://commons.wikimedia.org/wiki/File:Peas_in_a_Pod_(Unsplash).jpg |
| `seed-crop-grechiha-1.jpg` | cc0 | https://commons.wikimedia.org/wiki/File:Buckwheat_fields_in_Minamiaso.jpg |
| `seed-crop-grechiha-2.jpg` | public domain | https://commons.wikimedia.org/wiki/File:Buckwheat_Bhutan.jpg |
| `seed-crop-kartofel-1.jpg` | public domain | https://commons.wikimedia.org/wiki/File:Potato_flowers1.jpg |

Отброшены: «гречиха» из выдачи в основном дикий эриогонум (тоже buckwheat), не посевная гречиха; соя с подтопленным больным полем — не для сайта поставщика удобрений.
