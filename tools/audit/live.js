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

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({
    ignoreHTTPSErrors: true,
    viewport: { width: Number(width), height: 900 },
  });
  const p = await ctx.newPage();
  const r = await p.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await p.waitForTimeout(4000);

  const m = await p.evaluate(() => ({
    height: document.body.scrollHeight,
    overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
    title: document.title,
  }));
  console.log(`${r.status()} · ${url} · ${width}px · высота ${m.height} · переполнение ${m.overflow}`);
  console.log(`title: ${m.title}`);

  await p.screenshot({ path: out, fullPage: true });
  console.log('снимок:', out);
  await b.close();
})();
