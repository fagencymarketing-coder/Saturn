const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1280,height:900}, deviceScaleFactor:1 });
  await p.goto('file://'+process.cwd()+'/site-prototype.html',{waitUntil:'load'});
  await p.waitForTimeout(900);
  await p.screenshot({path:'site-desk-final.png', fullPage:true});
  await b.close();
})();
