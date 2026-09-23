const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1280,height:860}, deviceScaleFactor:1.4 });
  await p.goto('file://'+process.cwd()+'/site-prototype.html',{waitUntil:'load'});
  await p.waitForTimeout(900);
  console.log('overflow=', await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1));
  await p.screenshot({path:'site-hero-check.png', clip:{x:0,y:0,width:1280,height:900}});
  await b.close();
})();
