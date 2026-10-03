# Промт 3 из 4. Код шапки, шапка и подвал

Третий из четырёх. Правила:
https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/prompts/PRAVILA.md

Здесь всего три действия. Блоки главной — в следующих двух промтах,
по четыре блока в каждом. Так сделано нарочно: длинный список действий
в одном промте уже один раз привёл к тому, что прогон встал.

**Перезапуск безопасен.** Если ты это уже делал — вставь ещё раз, хуже
не станет: замена кода на тот же код ничего не меняет.

Ориентировочное время: 15 минут.

---

## 3.1 Код в HEAD

Настройки сайта → Ещё → «Вставка кода» → поле **HEAD**.
Удали всё, что там сейчас, и вставь целиком:

https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/head-code.html

Сохрани. В отчёт: сколько символов получилось в поле.

Этот код подставляет шапку, подвал, полосу заявки и баннер cookie на
страницы товара — без него страницы товара остаются голыми.

## 3.2 Шапка

Страницы-шаблоны → «Шапка» → блок T123 → Контент → поле HTML.
Заменить целиком на:

https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/shapka.html

## 3.3 Подвал

Страницы-шаблоны → «Подвал» → блок T123 → заменить целиком на:

https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/podval.html

---

## Дальше

Открой следующий файл и продолжай по нему:
https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/prompts/AGENT-3B-BLOKI-VERH.md
