const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1280,height:900}, deviceScaleFactor:2 });
  await p.goto('file://'+process.cwd()+'/site-prototype.html',{waitUntil:'load'});
  await p.emulateMedia({media:'screen'});
  await p.waitForTimeout(1000);
  const H = await p.evaluate(()=>document.body.scrollHeight);
  console.log('content H=',H);
  await p.pdf({path:'Saturn-prototype.pdf', width:'1280px', height:H+'px', printBackground:true, pageRanges:'1'});
  await b.close();
})();
