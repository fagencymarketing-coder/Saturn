# Эталонные рендеры главной

Собраны из блоков `design/blocks/` на дату коммита. Это то, как страница
должна выглядеть после публикации — с ними и сверяется живой сайт.

| Файл | Ширина | Для чего |
|---|---|---|
| `glavnaya-pk-1920.png` | 1920 | широкий монитор |
| `glavnaya-pk-1440.png` | 1440 | базовая ширина макета |
| `glavnaya-noutbuk-1280.png` | 1280 | ноутбук, самая частая ширина |
| `glavnaya-planshet-gorizont-1024.png` | 1024 | планшет горизонтально |
| `glavnaya-planshet-768.png` | 768 | планшет вертикально |
| `glavnaya-telefon-430.png` | 430 | iPhone Pro Max |
| `glavnaya-telefon-390.png` | 390 | iPhone базовый |
| `glavnaya-telefon-320.png` | 320 | самый узкий экран, который поддерживаем |

Пересобрать:

```
cd /tmp/blk && bash mk2.sh /home/user/saturn/design/blocks/{shapka,geroy,\
populyarnye,semena,agro,geografiya,rezultaty,dokumenty,kontakty,podval}.html
node etalon.js
```

Высота страницы: 6885 на ПК, 7401 на планшете, 8432 на телефоне.
Горизонтальной прокрутки нет ни на одной ширине, стыки секций — ноль.
