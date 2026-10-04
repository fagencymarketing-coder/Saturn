# Промт 19. Заплатка по твоему отчёту + перенос файлов в Тильду

## ВОПРОСОВ НЕ ЗАДАВАТЬ

Заказчицы не будет несколько часов. Она не ответит. Любой вопрос —
это остановка на полдня, а не уточнение.

В прошлый раз ты остановился и спросил, публиковать ли страницы.
Отвечаю заранее и на все похожие случаи сразу:

* **Публикация в этом промте разрешена и нужна — ровно одна страница,
  «Каталог», шаг 19.2.** Переспрашивать не надо, разрешение уже дано.
* **Кнопку «Опубликовать все страницы» не нажимать никогда** — это
  единственный запрет, и он без исключений.
* Если что-то названо не так, как в Тильде, — **найди по смыслу**,
  сделай и запиши в отчёт, как оно называется на самом деле.
* Если шаг не выходит с двух попыток — **пропусти**, напиши в отчёт
  «не сделано» и причину, иди дальше. Один непройденный шаг не
  отменяет остальные.
* Если увидишь поломку, о которой в промте ничего нет, — **опиши её в
  отчёте и иди дальше**, сам не чини.
* Если сомневаешься, делать или нет, — **делай то, что прямо написано
  в промте, и ничего сверх того**.

Единственный случай, когда нужно остановиться: после публикации
«Каталога» страница выглядит сломанной. Тогда ничего больше не
публикуй, опиши что видишь — и переходи к этапу 2, он от публикации
не зависит.


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
ходу, а не в конце. Вопросов не задавай (см. самый верх промта).
Не получилось за два захода — пиши «не сделано» с причиной и иди
дальше.

---

Ориентировочное время: 1 час 20 минут. Два этапа: короткий и
длинный однообразный.

Отчёт по промту 18 разобрал, спасибо — он закрыл почти всю приёмку.
Два уточнения из него я записал: живые слуги `vega-klei` и
`mikroel-pivovarennii-yachmen` (в прошлом промте я назвал их неверно),
и ленивый загрузчик Тильды, который на первом заходе иногда оставляет
фотографию товара пустой до первой прокрутки. Второе — поведение
платформы, не наша вёрстка; трогать не будем.

Моя проверка сошлась с твоей: горизонтальной прокрутки нет ни на одной
из шести ширин, ни на главной, ни на каталоге.

---

# Этап 1. Одна замена — заплатка по твоей находке

### Что чиню

**Товары без фотографии (твой пункт 18.10).** Ты выяснил главное: у
этих семи позиций Тильда **вообще не рисует блок картинки** — элемента
`imgwrapper` в карточке нет. Моё прежнее правило красило несуществующий
элемент, потому плашки и не было, а название с ценой уезжали вверх на
118 px.

Теперь место держит сама карточка: пустой блок нужной пропорции с
бежевой плашкой и приглушённой эмблемой дорисовывается там, где
картинки не нашлось. Появится фотография — правило перестанет
срабатывать само собой, править ничего не придётся.

**Серые заготовки каталога.** Мой прогон поймал на 768 px: пока
карточки грузятся, контейнер заготовок шире экрана на 20 px, и
страница на миг разъезжается вбок. Ограничил шириной экрана.

**Честно: заплатку про семь товаров я проверить не смог** — в моём
окружении карточки каталога отрисовываются через раз, и до второй
страницы списка, где эти товары лежат, я не добрался. Логика простая и
безопасная, но подтвердить её можешь только ты. Поэтому в приёмке она
первым пунктом.

### 19.1 Код HEAD — **46 350 символов**

Заменить целиком. Было 45 842.

`https://tilda.cc/projects/editheadcode/?projectid=34592909`

https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/claude/nifty-fermat-az604f/design/blocks/head-code.html

Сверить длину после полной перезагрузки страницы редактора.

### 19.2 Опубликовать «Каталог»

Только «Каталог», одну страницу. «Главную» не трогать — на ней ничего
не менялось. Кнопку «Опубликовать все страницы» не нажимать.

### 19.3 Проверить семь товаров без фото

Там же, где смотрел в прошлый раз: `/catalog` → «Удобрения и листовые
подкормки», строка с Relict Макро N Mg+ / Relict Макро PK.

Нужны два числа:

1. Высота блока с картинкой у карточки без фото — должна совпасть с
   соседями по строке (в прошлый раз у соседей было 117 px при ширине
   карточки 157).
2. Верх названия у карточки без фото и у соседа по строке — в прошлый
   раз расходились на 118 px, должно стать 0.

И глазами: видна ли бежевая плашка с эмблемой по центру.

**Если плашки нет или карточка поехала** — напиши, что именно видишь, и
переходи к этапу 2. Сам не чини: вторая попытка за мной.

---

# Этап 2. Перенос файлов в хранилище Тильды

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

## Файлы (этап 2)

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

По этапу 1: сколько символов стало в коде HEAD, во сколько опубликован
«Каталог», и три результата проверки семи товаров.

По этапу 2 главное — таблица адресов. Без неё перенос бесполезен:
я не смогу поправить код.

| № | Файл | Новый адрес в Тильде |
|---|---|---|
| 1 | `saturn-logo-white.png` | `https://static.tildacdn.com/...` |
| … | … | … |

Плюс, как обычно: сколько файлов загрузилось, где споткнулся, и как
на самом деле называется раздел с файлами в нынешней Тильде.

## Чего не делать

- На этапе 2 не менять код блоков и код HEAD. Адреса поменяю я.
- На этапе 2 ничего не публиковать: мы только складываем файлы в
  библиотеку, на сайте от этого ничего не меняется.
- Публикация во всём промте ровно одна — «Каталог» на шаге 19.2.
- Не удалять ничего из уже загруженного в Тильду.
- Не трогать магазин, товары, настройки проекта, форму T678.
