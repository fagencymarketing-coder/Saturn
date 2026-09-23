const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1100,height:900}, deviceScaleFactor:2 });
  await p.goto('file://'+process.cwd()+'/wireframe-block3-filters.html',{waitUntil:'networkidle'});
  await p.waitForTimeout(400);
  await p.screenshot({path:'wf-block3.png', fullPage:true});
  console.log('ok');
  await b.close();
})();
