const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const files = [['wireframe-V1-search.html','V1'],['wireframe-V2-filters.html','V2'],['wireframe-V3-lead.html','V3']];
  const b = await chromium.launch();
  for (const [f,name] of files){
    const p = await b.newPage({ viewport:{width:1200,height:900}, deviceScaleFactor:2 });
    await p.goto('file://'+process.cwd()+'/'+f,{waitUntil:'networkidle'});
    await p.waitForTimeout(400);
    await p.screenshot({path:'wf-'+name+'.png', fullPage:true});
    console.log(name+' ok');
    await p.close();
  }
  await b.close();
})();
