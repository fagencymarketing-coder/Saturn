#!/usr/bin/env node
// Контрольный лист: сайт на восьми ширинах рядом, одной картинкой.
//
//   node tools/render/setka.js [файл.html] [выход.png]
//
// Числами проверяются переполнение, кегли и отступы — это делает check.js.
// А «гармонично или нет» числами не измеряется, это смотрят глазами.
// Лист нужен, чтобы смотреть все ширины разом, а не по одной в день.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const SHIRINY = [390, 768, 1024, 1263, 1366, 1440, 1680, 1920];
const VYSOTA  = 1100;          // сколько показываем от верха страницы
const MASHTAB = 0.42;          // чтобы восемь колонок влезли в один кадр

const [ist = '/tmp/blk/t2.html', out = '/tmp/blk/setka.png'] = process.argv.slice(2);

(async () => {
  const b = await chromium.launch();
  const kadry = [];
  for (const w of SHIRINY) {
    const ctx = await b.newContext({ viewport: { width: w, height: VYSOTA } });
    const p = await ctx.newPage();
    await p.goto(ist.startsWith('http') ? ist : 'file://' + ist);
    await p.waitForTimeout(900);
    const buf = await p.screenshot();
    kadry.push({ w, data: 'data:image/png;base64,' + buf.toString('base64') });
    await ctx.close();
    process.stderr.write(`  снято ${w}\n`);
  }

  // склейка: каждая колонка ужимается, подписи сверху
  const ctx = await b.newContext({
    viewport: { width: Math.round(SHIRINY.reduce((s, w) => s + w * MASHTAB + 16, 0)) + 16,
                height: Math.round(VYSOTA * MASHTAB) + 56 },
  });
  const p = await ctx.newPage();
  await p.setContent(`<body style="margin:0;background:#1a1a1a;font:600 13px/1.4 system-ui;
      display:flex;gap:16px;padding:8px">
    ${kadry.map(k => `<div>
      <div style="color:#bbb;padding:6px 0">${k.w}</div>
      <img src="${k.data}" style="width:${Math.round(k.w * MASHTAB)}px;display:block;
        border:1px solid #333">
    </div>`).join('')}
  </body>`);
  await p.waitForTimeout(600);
  await p.screenshot({ path: out, fullPage: true });
  await b.close();
  console.log('контрольный лист: ' + out);
})();
