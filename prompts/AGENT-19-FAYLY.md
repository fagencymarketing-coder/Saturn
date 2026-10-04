# Промт 19. Перенос файлов сайта в хранилище Тильды

## Если ты не помнишь, что это за проект — прочитай этот раздел

**Проект.** Сайт `sssaturn.ru` для ООО «Сатурн», Барнаул: поставщик
удобрений, средств защиты растений и семян для хозяйств. Проект в
Тильде — `34592909`. Работаем вдвоём: я готовлю код и промты, ты
делаешь руками то, что требует браузера и доступа к Тильде. Код сам
не пиши и не правь.

**Страницы.** «Главная» (`/home`), «Каталог» (`/catalog`), «Политика»,
«Согласие», «Страница не найдена», плюс страницы-шаблоны «Шапка» и
«Подвал». На корне домена стоит заглушка — так и задумано, не трогать.

**Полные правила прогона:**
https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/claude/nifty-fermat-az604f/prompts/PRAVILA.md

**Чего не делать никогда.** Не нажимать «Опубликовать все страницы».
Не трогать настройки проекта: домен, почта, платежи, тариф,
получатели форм. Не трогать магазин, товары, разделы и цены. Не
трогать штатный блок формы T678. Не удалять ничего сверх названного.

**Формат отчёта.** Таблица: шаг · статус · что именно. Статус только
один из трёх: `сделано`, `сделано иначе`, `не сделано`. Отчёт веди по
ходу, а не в конце. Вопросов не задавай — заказчицы не будет
несколько часов. Не получилось за два захода — пиши «не сделано» с
причиной и иди дальше.

---

Ориентировочное время: 1 час 10 минут. Работа однообразная, но
сломать ничего нельзя: мы только **добавляем** файлы в Тильду, ничего
не удаляя и не меняя на сайте.

## Зачем это

Сейчас логотип, фотография поля в герое, карта, логотипы
производителей, фотографии товаров, прайс и сертификаты — двадцать
девять файлов — лежат на гитхабе и грузятся оттуда каждому
посетителю. Гитхаб для этого не предназначен: он запрещает браузеру
хранить файл дольше **пяти минут**. То есть человек отошёл и вернулся
— браузер качает фотографию поля (353 КБ) и карту (251 КБ) заново.
А если гитхаб у клиента в Барнауле притормозит, тот увидит сайт без
логотипа, без героя и без карты.

Хранилище Тильды уже оплачено, работает в России быстро и отдаёт
файлы с нормальным сроком хранения. Переносим туда.

## Что от тебя нужно — и чего не нужно

**Нужно:** загрузить двадцать девять файлов в Тильду и прислать
таблицу «старый адрес → новый адрес».

**Не нужно:** менять код блоков. Адреса в коде поменяю я по твоей
таблице, одним заходом. Если начнёшь править блоки сам — мы наложим
правки друг на друга и собьём счёт символов.

## Как загрузить

В Тильде файлы живут в общей библиотеке проекта. Путь примерно такой:
любой блок с картинкой → «Контент» → кнопка выбора изображения →
окно загрузки, в нём вкладка с ранее загруженными файлами. Там же
кнопка «Загрузить». Названия Тильда периодически меняет — ищи по
смыслу и **запиши в отчёт, как этот раздел называется на самом
деле**: это пригодится в следующий раз.

Для каждого файла:

1. Скачай файл по адресу из таблицы (просто открой ссылку, браузер
   предложит сохранить).
2. Загрузи его в библиотеку Тильды.
3. Скопируй адрес загруженного файла — он начинается с
   `https://static.tildacdn.com/`.
4. Впиши строку в таблицу отчёта.

Имя файла при загрузке менять не надо. Если Тильда сама переименует —
не страшно, главное адрес.

**Если какой-то файл не грузится** (слишком большой, не тот формат) —
пропусти, напиши «не сделано» и причину, иди дальше. Три PDF в конце
списка весят по полтора-три мегабайта, они самые рискованные, поэтому
и стоят последними.

---

## Файлы

### Видно сразу на экране — переносить первыми

| № | Файл | Откуда скачать |
|---|---|---|
| 1 | `saturn-logo-white.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/saturn-logo-white.png |
| 2 | `saturn-logo-color.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/saturn-logo-color.png |
| 3 | `saturn-emblem.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/saturn-emblem.png |
| 4 | `hero-field.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/hero-field.jpg |
| 5 | `cycle-bg.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/cycle-bg.jpg |
| 6 | `geo-map-desktop.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/geo-map-desktop.png |
| 7 | `geo-map-mobile.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/geo-map-mobile.png |
| 8 | `fertika.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/fertika.png |
| 9 | `volsky.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/volsky.png |
| 10 | `relict-organics.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/relict-organics.png |

### Фотографии товаров в блоке «Популярные позиции»

| № | Файл | Откуда скачать |
|---|---|---|
| 11 | `fertika-listovoe-18-18-18.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/fertika-listovoe-18-18-18.png |
| 12 | `strada-n.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/strada-n.png |
| 13 | `ampir-ekstra-vr.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/ampir-ekstra-vr.png |
| 14 | `chellendzher-vrk.png` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/chellendzher-vrk.png |
| 15 | `ampir-10-express.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/ampir-10-express.jpg |
| 16 | `ampir-25-express.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/ampir-25-express.jpg |
| 17 | `kvs-akvilon.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/kvs-akvilon.jpg |
| 18 | `novosel-cl.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/tilda-photos/novosel-cl.jpg |

### Превью документов

| № | Файл | Откуда скачать |
|---|---|---|
| 19 | `preview-sertifikat-fertika.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/docs/preview-sertifikat-fertika.jpg |
| 20 | `preview-sgr-strada.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/docs/preview-sgr-strada.jpg |
| 21 | `preview-sgr-diforma.jpg` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/docs/preview-sgr-diforma.jpg |

### Файлы на скачивание — последними, они тяжёлые

| № | Файл | Откуда скачать |
|---|---|---|
| 22 | `price-saturn-2026.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/price-saturn-2026.pdf |
| 23 | `saturn-rekvizity.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/saturn-rekvizity.pdf |
| 24 | `01-sertifikat-dilera-fertika-do-2026.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/01-sertifikat-dilera-fertika-do-2026.pdf |
| 25 | `07-sgr-strada-n-p-k-2855-do-2030.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/07-sgr-strada-n-p-k-2855-do-2030.pdf |
| 26 | `08-sgr-diforma-2899-do-2030.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/08-sgr-diforma-2899-do-2030.pdf |
| 27 | `protokol-1.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/protocols/protokol-1.pdf |
| 28 | `protokol-4.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/protocols/protokol-4.pdf |
| 29 | `protokol-7.pdf` | https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files/protocols/protokol-7.pdf |

---

## Отчёт

Главное в этом промте — таблица адресов. Без неё перенос бесполезен:
я не смогу поправить код.

| № | Файл | Новый адрес в Тильде |
|---|---|---|
| 1 | `saturn-logo-white.png` | `https://static.tildacdn.com/...` |
| … | … | … |

Плюс, как обычно: сколько файлов загрузилось, где споткнулся, и как
на самом деле называется раздел с файлами в нынешней Тильде.

## Чего не делать

- Не менять код блоков и код HEAD. Адреса поменяю я.
- Не публиковать страницы: пока мы только складываем файлы, на сайте
  ничего не меняется.
- Не удалять ничего из уже загруженного в Тильду.
- Не трогать магазин, товары, настройки проекта, форму T678.
