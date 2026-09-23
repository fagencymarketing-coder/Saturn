const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:900,height:600}, deviceScaleFactor:2 });
  await p.goto('file:///tmp/icons-test.html',{waitUntil:'load'});
  await p.waitForTimeout(300);
  await p.screenshot({path:'ictest.png', fullPage:true});
  await b.close();
})();
