#!/usr/bin/env node
// Снимок живой страницы sssaturn.ru из контейнера.
//
//   node tools/audit/live.js https://sssaturn.ru/home 1440 /tmp/home-1440.png
//
// Контейнер ходит наружу через прокси с собственным сертификатом, поэтому
// Chromium ругается на TLS. Лечится не отключением проверки на уровне
// системы, а ignoreHTTPSErrors у контекста: это касается только этого
// браузера и только на время снимка.
//
// Раньше в CLAUDE.md было записано, что браузер до sssaturn.ru не достучится
// и живой визуальный контроль — работа агента. Это неверно: достукивается.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const [url, width = '1440', out = '/tmp/live.png'] = process.argv.slice(2);
if (!url) {
  console.error('нужен адрес: node tools/audit/live.js <url> [ширина] [файл]');
  process.exit(1);
}

// Прокси контейнера рвёт соединения, когда страница тянет два десятка
// картинок разом: goto с networkidle падает на ERR_TOO_MANY_RETRIES, хотя
// сама страница открывается. Поэтому ждём domcontentloaded, а не тишины в
// сети, и пробуем трижды. Картинки для замеров высоты не нужны.
async function otkryt(p, url) {
  let posledn;
  for (let i = 1; i <= 3; i++) {
    try {
      return await p.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    } catch (e) {
      posledn = e;
      console.error(`  попытка ${i} не вышла: ${String(e.message).split('\n')[0]}`);
      await p.waitForTimeout(3000);
    }
  }
  throw posledn;
}

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({
    ignoreHTTPSErrors: true,
    viewport: { width: Number(width), height: 900 },
  });
  const p = await ctx.newPage();
  const r = await otkryt(p, url);
  await p.waitForTimeout(6000);

  const m = await p.evaluate(() => ({
    height: document.body.scrollHeight,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    title: document.title,
  }));
  // Высота — величина справочная: часть картинок грузится из
  // raw.githubusercontent.com, прокси часть соединений рвёт, и
  // незагруженная картинка схлопывается. Из-за этого одна и та же
  // страница меряется то 8262, то 7634. Для приёмки смотреть не высоту,
  // а live-blocks.py: он считает отступы в разметке, их прокси не portit.
  console.log(`${r.status()} · ${url} · ${width}px · высота ${m.height} (справочно) · переполнение ${m.overflow}`);
  console.log(`title: ${m.title}`);

  await p.screenshot({ path: out, fullPage: true });
  console.log('снимок:', out);
  await b.close();
})();
