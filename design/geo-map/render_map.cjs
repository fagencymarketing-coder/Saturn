const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const fs = require('fs');
  const svg = fs.readFileSync('map_ref.svg','utf8');
  const b = await chromium.launch({ args:['--no-sandbox'] });
  const p = await b.newPage({ viewport:{width:1600,height:900}, deviceScaleFactor:2 });
  await p.setContent(`<body style="margin:0">${svg}</body>`);
  await p.locator('svg').screenshot({ path:'saturn-map-geo.png' });
  await b.close(); console.log('rendered saturn-map-geo.png');
})();
