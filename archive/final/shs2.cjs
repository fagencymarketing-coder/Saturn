const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1200,height:900}, deviceScaleFactor:2 });
  await p.goto('file://'+process.cwd()+'/wireframe-SIMPLE.html',{waitUntil:'networkidle'});
  await p.waitForTimeout(400);
  await p.screenshot({path:'wf-SIMPLE.png', fullPage:true});
  console.log('ok');
  await b.close();
})();
