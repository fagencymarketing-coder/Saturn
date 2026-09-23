const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const sizes = [[375,812,'mob'],[768,1024,'tab'],[1440,900,'desk']];
  const b = await chromium.launch();
  for (const [w,h,name] of sizes){
    const p = await b.newPage({ viewport:{width:w,height:h}, deviceScaleFactor:(name==='mob'?3:2) });
    await p.goto('file://'+process.cwd()+'/saturn-zaglushka.html',{waitUntil:'networkidle'});
    await p.waitForTimeout(700);
    const overflow = await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
    await p.screenshot({path:'final-'+name+'.png', fullPage:true});
    console.log(name+' '+w+'x'+h+' -> ok, horizontalOverflow='+overflow);
    await p.close();
  }
  await b.close();
})();
