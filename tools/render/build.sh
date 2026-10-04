#!/bin/bash
# Локальный стенд: собирает блоки главной в одну страницу и готовит
# всё, что ей нужно (шрифты из репозитория, фото из Saturnphoto).
# Работает в свежем контейнере с нуля.
#
#   bash tools/render/build.sh              — вся главная
#   bash tools/render/build.sh agro.html    — один блок
#
# Результат: $WORK/t2.html, открывать через file://

set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WORK="${SATURN_WORK:-/tmp/blk}"
BLOCKS="$ROOT/design/blocks"
RAW="https://raw.githubusercontent.com/fagencymarketing-coder/Saturnphoto/main/files"
CA="${CURL_CA_BUNDLE:-/root/.ccr/ca-bundle.crt}"

mkdir -p "$WORK"
cp -n "$ROOT/tools/render/fonts/"m*.ttf "$WORK/" 2>/dev/null || true

PORYADOK="shapka geroy populyarnye semena agro rezultaty geografiya dokumenty kontakty podval"
if [ $# -gt 0 ]; then FILES="$@"; else
  FILES=""; for b in $PORYADOK; do FILES="$FILES $BLOCKS/$b.html"; done
fi

# фото: качаем только то, на что ссылаются блоки, и только если ещё нет
for f in $FILES; do
  grep -o "$RAW/[^\"')]*" "$f" 2>/dev/null | sed "s#$RAW/##" | sort -u | while read -r img; do
    [ -z "$img" ] && continue
    mkdir -p "$WORK/$(dirname "$img")"
    [ -f "$WORK/$img" ] || curl -sS --cacert "$CA" "$RAW/$img" -o "$WORK/$img" || true
  done
done

cat > "$WORK/t2.html" <<'HEAD'
<!doctype html><html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
@font-face{font-family:Montserrat;font-weight:400;src:url(m400.ttf) format('truetype')}
@font-face{font-family:Montserrat;font-weight:600;src:url(m600.ttf) format('truetype')}
@font-face{font-family:Montserrat;font-weight:700;src:url(m700.ttf) format('truetype')}
@font-face{font-family:Montserrat;font-weight:800;src:url(m800.ttf) format('truetype')}
html,body{margin:0;padding:0}
</style></head><body>
HEAD
# Шкала сайта живёт в :root кода HEAD, а блоки только ею пользуются.
# Без неё стенд показывал бы кегль по умолчанию, то есть 16px у всего.
python3 - "$BLOCKS/head-code.html" >> "$WORK/t2.html" <<'TOK'
import re, sys
h = open(sys.argv[1], encoding='utf-8').read()
m = re.search(r':root\{.*?\n\}', h, re.S)
print('<style>' + (m.group(0) if m else '') + '</style>')
TOK

for f in $FILES; do sed "s#$RAW/##g" "$f" >> "$WORK/t2.html"; done
echo '</body></html>' >> "$WORK/t2.html"
echo "собрано: $WORK/t2.html"
