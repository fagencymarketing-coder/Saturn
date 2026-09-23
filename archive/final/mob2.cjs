const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const m = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:1 });
  await m.goto('file://'+process.cwd()+'/site-prototype.html',{waitUntil:'load'});
  await m.waitForTimeout(700);
  await m.screenshot({path:'site-mob-lite.png', fullPage:true, type:'jpeg', quality:78});
  await b.close();
})();
