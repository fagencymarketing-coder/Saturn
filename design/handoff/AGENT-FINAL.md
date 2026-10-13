# Агенту — финальный промт (sssaturn.ru)

Все файлы лежат в репозитории, скачай их сам по ссылкам ниже (ничего пересылать не нужно).
Правила: работай по одной странице, «Опубликовать всё» не нажимать, длины сверяй, после
каждого шага — короткий отчёт. Если публикация блокируется средой (Production Deploy) —
не обходи, пометь «готово к публикации», заказчица опубликует сама.

Базовый адрес файлов:
`https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/`

## 1. HEAD (~51 450 символов)
Файл: `design/blocks/head-code.html`
→ https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/head-code.html
Заменить код в поле HEAD сайта целиком. Внутри: кнопка «наверх» не исчезает у подвала;
название товара в каталоге и семенах загорается оранжевым при наведении; поле поиска —
одна обводка при фокусе; поля формы (попап и инлайн) — нейтральный тёмный фокус, НЕ красный;
левое меню разделов каталога — без рамки.

## 2. Прайс-PDF — УЖЕ ОБНОВЛЁН, НИЧЕГО НЕ ДЕЛАТЬ
Кнопки «Скачать прайс» ведут на файл в репозитории Saturnphoto
(`.../Saturnphoto/main/files/price-saturn-2026.pdf`). Этот файл уже заменён на новый
выверенный прайс (Claude Code, 13.10). Ссылки прежние — менять в Tilda ничего не нужно,
загружать PDF в Tilda не нужно. Через ~5 минут кэш GitHub обновится, и кнопки отдадут
новый файл (9 страниц, Клео 4050). Для проверки — жёсткое обновление (Ctrl+F5).

## 3. Блок «Популярные позиции» на /home
Файл: `design/blocks/populyarnye.html`
→ https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/populyarnye.html
Заменить блок: у Страды N цена 315 → 409,5 ₽/л.

## 4. Подвал — опубликовать (ссылка cookie уже убрана в шаблоне)
Опубликовать страницы с подвалом, чтобы «Настройки cookie» пропала на живом сайте:
/catalog, /home, /semena, /privacy, /consent, /cookie-consent, 404, /.

## 5. Фото — на карточки /catalog (прозрачный фон, 900×900)
Папка: `design/handoff/foto/`
| Карточка | Файл |
|---|---|
| FERTIKA Универсал-2 NPK 12-8-14 | foto/fertika-universal-2.png |
| Страда N | foto/strada-n.png (и на /home в «Популярных», если несложно) |
| Царумин, ВК | foto/carumin.png |
| Анкер Трио, КС | foto/anker-trio.png |
| Вега АнтиПена, КЭ | foto/vega-antipena.png |
| Биостик Терра | foto/biostik-terra.png |

Ссылки на фото:
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/handoff/foto/fertika-universal-2.png
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/handoff/foto/strada-n.png
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/handoff/foto/carumin.png
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/handoff/foto/anker-trio.png
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/handoff/foto/vega-antipena.png
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/handoff/foto/biostik-terra.png

## 6. Заглушка — на карточки без нормального фото
Поставить стандартную заглушку (розовый кружок с «S», как уже на сайте), плохое фото убрать:
Клео, ВДГ · Зазофен, ВР · Тифилагро, ВДГ · Тиара, КС · Ранголи-Базорон, ВР · Атлант Супер ·
Вега Клей · Волски Моно-Железо · Микроэл Пивоваренный ячмень · Relict Макро N Mg+ ·
Relict Макро PK · Реликт Р Старт (протравитель).

**НЕ трогать** Реликт М Бор/Сера/Цинк/Кремний — одно фото на всю линейку у самого
производителя, это не ошибка.

## 7. Опубликовать и проверить (ПК + телефон)
По каждому пункту коротко:
- HEAD обновлён; кнопка «наверх» видна у подвала; ховер названий в каталоге и семенах;
- «Скачать прайс» везде отдаёт новый PDF;
- поиск — одна обводка; фокус поля формы не красный; у левого меню нет рамки;
- 6 фото встали; на остальных без фото — заглушка;
- Страда N на /home = 409,5; cookie-ссылки в подвале нет.
