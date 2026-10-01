const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.join(__dirname, 'html');
  const out = path.join(__dirname, 'pdf');
  fs.mkdirSync(out, { recursive: true });
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage();
  for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.html')).sort()) {
    await p.goto('file://' + path.join(dir, f), { waitUntil: 'load' });
    await p.evaluate(() => document.fonts.ready);
    const ok = await p.evaluate(() => document.fonts.check('800 17pt Montserrat'));
    if (!ok) throw new Error('Montserrat не загрузился: ' + f);
    const dst = path.join(out, f.replace('.html', '.pdf'));
    await p.pdf({ path: dst, format: 'A4', printBackground: true,
                  margin: { top: '0', right: '0', bottom: '0', left: '0' } });
    console.log(dst, fs.statSync(dst).size, 'байт');
  }
  await b.close();
})();
