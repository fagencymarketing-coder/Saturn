#!/usr/bin/env python3
"""Показать замеры секции макета.  Пример:  python3 show.py 0        — шапка на всех ширинах
                                            python3 show.py 10 390   — подвал только на 390"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
WANT_SEC = int(sys.argv[1]) if len(sys.argv) > 1 else None
WANT_W = int(sys.argv[2]) if len(sys.argv) > 2 else None
MAXD = int(sys.argv[3]) if len(sys.argv) > 3 else 5

frames = []
for f in ('desktop.json', 'mobile-tablet.json'):
    frames += json.load(open(os.path.join(HERE, f), encoding='utf-8'))

for fr in sorted(frames, key=lambda x: -x['W']):
    if WANT_W and fr['W'] != WANT_W:
        continue
    for s in fr['secs']:
        if WANT_SEC is not None and s['i'] != WANT_SEC:
            continue
        print(f"=== {fr['W']} · секция {s['i']} · высота {s['h']} · фон {s['bg']} · {' | '.join(s['head'])[:60]}")
        for it in s['items']:
            if it['h'] < 6 or it['d'] > MAXD:
                continue
            line = (f"{'  ' * it['d']}{it['tag']:4} x{it['x']:5} y{it['y']:5} {it['w']:4}x{it['h']:4} "
                    f"{it['fs']:>6}/{it['fw']:3} lh{it['lh']:>7} {it['color']:20} bg={it['bg']:20} "
                    f"r={it['r']:9} pad={it['pad'][:16]:16} gap={it['gap'][:7]:7} {it['txt']}")
            if it['src']:
                line += '  → ' + it['src']
            print(line)
        print()
