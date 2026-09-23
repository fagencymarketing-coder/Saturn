const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const files = [['mockup-A-waves-top.html','A'],['mockup-B-waves-bottom.html','B']];
  const b = await chromium.launch();
  for (const [f,name] of files){
    const p = await b.newPage({ viewport:{width:375,height:812}, deviceScaleFactor:2 });
    await p.goto('file://'+process.cwd()+'/'+f,{waitUntil:'networkidle'});
    await p.waitForTimeout(700);
    const overflow = await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
    await p.screenshot({path:'mockup-'+name+'.png', fullPage:true});
    console.log(name+' -> ok, horizontalOverflow='+overflow);
    await p.close();
  }
  await b.close();
})();
