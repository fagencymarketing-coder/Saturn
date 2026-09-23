const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1280,height:900}, deviceScaleFactor:2 });
  await p.goto('file://'+process.cwd()+'/site-prototype-v2.html',{waitUntil:'load'});
  await p.emulateMedia({media:'screen'});
  await p.waitForTimeout(1000);
  const H = await p.evaluate(()=>document.body.scrollHeight);
  await p.pdf({path:'Saturn-prototype-v2.pdf', width:'1280px', height:H+'px', printBackground:true, pageRanges:'1'});
  console.log('pdf H=',H);
  await b.close();
})();
