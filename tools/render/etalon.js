#!/usr/bin/env node
// Пересобирает эталонные рендеры главной в design/etalon/.
//
//   bash tools/render/build.sh          # сначала собрать страницу
//   node tools/render/etalon.js         # потом снять её на всех ширинах
//
// Раньше порядок блоков для эталона задавался руками в /tmp — и разошёлся
// с настоящей страницей: «География» и «Результаты» стояли наоборот.
// Теперь порядок один и тот же, он живёт в tools/render/build.sh.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

const SHIRINY = [
  [1920, 'glavnaya-pk-1920.png'],
  [1440, 'glavnaya-pk-1440.png'],
  [1280, 'glavnaya-noutbuk-1280.png'],
  [1024, 'glavnaya-planshet-gorizont-1024.png'],
  [768, 'glavnaya-planshet-768.png'],
  [430, 'glavnaya-telefon-430.png'],
  [390, 'glavnaya-telefon-390.png'],
  [320, 'glavnaya-telefon-320.png'],
];

const ISTOCHNIK = process.argv[2] || '/tmp/blk/t2.html';
const KUDA = path.join(__dirname, '..', '..', 'design', 'etalon');

(async () => {
  const b = await chromium.launch();
  for (const [w, file] of SHIRINY) {
    const p = await b.newPage({ viewport: { width: w, height: 900 } });
    await p.goto('file://' + ISTOCHNIK);
    await p.waitForTimeout(2500);
    const m = await p.evaluate(() => ({
      h: document.body.scrollHeight,
      o: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    }));
    await p.screenshot({ path: path.join(KUDA, file), fullPage: true });
    console.log(`${String(w).padStart(4)}px · высота ${m.h} · переполнение ${m.o} · ${file}`);
    await p.close();
  }
  await b.close();
})();
