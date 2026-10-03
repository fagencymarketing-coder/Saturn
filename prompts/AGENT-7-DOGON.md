# Промт 7. Догон: в Тильду попадает текущая версия репозитория

Правила:
https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/prompts/PRAVILA.md

После твоего прогона 03.10 в репозитории поправлено десять мест: код HEAD
и девять блоков главной. В Тильде пока старые версии — их нужно заменить.

**Ничего не публикуй.** Публикация — шаг заказчика, у тебя она всё равно
отклоняется классификатором. Твоя задача: вставить код и сохранить.

**Перезапуск безопасен:** замена кода на тот же код ничего не меняет.
Если видишь, что в поле уже лежит ровно то же количество символов, что
указано ниже, — ничего не меняй, отметь в отчёте «уже стоит».

Ориентировочное время: 40 минут.

---

## 7.1 Код HEAD — **36 719 символов**

«Настройки сайта → Вставка кода → HTML-код для вставки внутрь HEAD».
Заменить **целиком**:

https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/head-code.html

Сейчас там 36 129 символов — версия, которую ты вставил в прошлый раз.
В новой изменены шапка, подвал и оформление каталога: отдельно их вставлять
не надо, всё собрано в этот один файл.

---

## 7.2–7.10 Девять блоков страницы «Главная»

В каждом блоке T123: Контент → поле HTML → заменить содержимое целиком →
сохранить → переоткрыть панель и убедиться, что записалось.
**Порядок блоков на странице не менять.**

Блоки сверху вниз:

| № | Блок | Файл | Должно стать |
|---|---|---|---|
| 7.2 | Герой, первый экран | `geroy.html` | 9 316 символов |
| 7.3 | Популярные позиции | `populyarnye.html` | 10 945 символов |
| 7.4 | Семена | `semena.html` | 5 443 символа |
| 7.5 | Агросопровождение | `agro.html` | 8 250 символов |
| 7.6 | Результаты испытаний | `rezultaty.html` | 7 060 символов |
| 7.7 | География | `geografiya.html` | 3 282 символа |
| 7.8 | Документы и сертификаты | `dokumenty.html` | 5 475 символов |
| 7.9 | Контакты | `kontakty.html` | 12 749 символов |
| 7.10 | Блок **под** формой | `forma-fix.html` | 3 673 символа |

Адрес любого файла:
`https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/<файл>`

Полные ссылки:

- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/geroy.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/populyarnye.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/semena.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/agro.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/rezultaty.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/geografiya.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/dokumenty.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/kontakty.html
- https://raw.githubusercontent.com/fagencymarketing-coder/Saturn/main/design/blocks/forma-fix.html

Две оговорки, обе уже встречались:

- Штатный блок формы Tilda между 7.9 и 7.10 **не трогать** — иначе заявки
  перестанут приходить. Меняется только блок T123 **под** ним.
- Если «Результаты» на странице оказались ниже «Географии» — ничего
  не переставляй, положи содержимое в тот блок, которому оно принадлежит
  по смыслу, и запиши это в отчёт.

---

## 7.11 Чего не делать

- Не публиковать ни одной страницы. Не нажимать «Опубликовать все страницы».
- Не трогать «Настройки страницы» — og-image и переименование заглушки
  заказчик делает руками, у тебя они блокируются.
- Не трогать настройки проекта: домен, почта, платежи, тариф, получатели форм.
- Не трогать шапку и подвал в «Страницах-шаблонах»: их оформление пришло
  с кодом HEAD из 7.1.

---

## 7.12 Отчёт

Таблица: шаг · сделано / уже стояло / не сделано · сколько символов стало.
Если где-то сохранение не прошло с первого раза — так и напиши, это бывает.

Отдельной строкой: что осталось заказчику — опубликовать «Главную»
и «Каталог» по одной.
