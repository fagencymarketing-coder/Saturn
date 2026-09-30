// SVG → PNG. Montserrat встраивается в страницу явно: без этого Chromium
// молча подставляет Arial, и подписи регионов выпадают из шрифта сайта.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
const [src, out] = [process.argv[2] || 'map_ref.svg', process.argv[3] || 'saturn-map-geo.png'];
const scale = Number(process.argv[4]) || 2;   // плотность пикселей PNG
const fontDir = path.join(__dirname, '..', '..', 'catalogs', '_fonts');
const face = w => `@font-face{font-family:Montserrat;font-weight:${w};src:url(data:font/ttf;base64,${
  fs.readFileSync(path.join(fontDir, `Montserrat-${w}.ttf`)).toString('base64')}) format('truetype')}`;
(async () => {
  const svg = fs.readFileSync(path.join(__dirname, src), 'utf8');
  const b = await chromium.launch({ args: ['--no-sandbox'] });
  const p = await b.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: scale });
  await p.setContent(`<style>${[400, 600, 700, 800].map(face).join('')}body{margin:0}</style>${svg}`);
  await p.evaluate(() => document.fonts.ready);
  // проверять шрифт есть смысл, только если в карте есть подписи
  const ok = !svg.includes('<text') || await p.evaluate(() => document.fonts.check('600 21px Montserrat'));
  if (!ok) throw new Error('Montserrat не загрузился — подписи ушли бы в Arial');
  await p.locator('svg').screenshot({ path: path.join(__dirname, out) });
  await b.close(); console.log('rendered', out, '· Montserrat: ok');
})();
