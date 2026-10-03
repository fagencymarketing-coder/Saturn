#!/usr/bin/env python3
"""Отступы по исходнику блоков: нечётные значения — следы ручной подгонки."""
import re, pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[2]
OK = {17}          # 17 — из утверждённого макета, блок «Агросопровождение»
bad = []
for f in sorted((ROOT / 'design' / 'blocks').glob('*.html')):
    if f.name == 'head-code.html':
        continue
    for m in re.finditer(r'(margin|padding|gap|row-gap|column-gap)[^:;{}]*:\s*([^;}]+)',
                         f.read_text(encoding='utf-8')):
        val = re.sub(r'(calc|clamp|min|max)\([^)]*\)', '', m.group(2))
        for v in re.findall(r'(\d+)px', val):
            n = int(v)
            if n % 2 and n not in OK:
                bad.append(f'{f.name}: {m.group(1)}: {m.group(2).strip()[:46]}')
print('НЕЧЁТНЫХ ОТСТУПОВ:', len(bad))
for b in dict.fromkeys(bad):
    print('  •', b)
sys.exit(1 if bad else 0)
