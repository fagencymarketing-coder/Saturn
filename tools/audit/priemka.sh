#!/usr/bin/env bash
# Приёмка живого сайта одной командой.
#
#   bash tools/audit/priemka.sh
#
# Девять проверок подряд. Каждая печатает свой итог, в конце — общий.
# Это то, чем проверяется отчёт агента: он пишет «сделано», а здесь
# видно, сделано или нет.
set -u
cd "$(dirname "$0")/../.."

ITOG=0
shag() {
  echo
  echo "=== $1"
  shift
  "$@" || ITOG=1
}

shag "блоки главной: выложено уплотнение или нет" \
  python3 tools/audit/live-blocks.py

shag "каталог: настройки блока ST340F" \
  python3 tools/audit/live-catalog.py

shag "содержание и все ссылки на живых страницах" \
  python3 tools/audit/content.py --live

shag "главная, 1440 — код ответа, высота, переполнение" \
  node tools/audit/live.js https://sssaturn.ru/home 1440 /tmp/priemka-home-1440.png

shag "главная, 390 — то же на телефоне" \
  node tools/audit/live.js https://sssaturn.ru/home 390 /tmp/priemka-home-390.png

# Доступность считается по живой странице: порог целей нажатия зависит
# от ширины окна, поэтому прогоняем четыре.
for W in 390 768 1024 1440; do
  shag "доступность на $W — контраст и цели нажатия" \
    node tools/audit/dostup.js https://sssaturn.ru/home "$W"
done

echo
if [ "$ITOG" = 0 ]; then
  echo "ПРИЁМКА ПРОЙДЕНА"
else
  echo "ПРИЁМКА НЕ ПРОЙДЕНА — смотри, какая проверка выше ругалась"
fi
echo "снимки: /tmp/priemka-home-1440.png, /tmp/priemka-home-390.png"
echo
echo "Чего эта проверка не умеет: нажать кнопку, отправить форму,"
echo "навести мышь. Это по-прежнему работа агента, список — в"
echo "docs/PROVERKA.md, уровень 2."
exit "$ITOG"
