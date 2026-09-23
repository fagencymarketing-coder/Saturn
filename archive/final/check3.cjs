const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  for (const [w,dsf,name] of [[1200,1,'chk-desk-full'],[390,2,'chk-mob-full']]){
    const p = await b.newPage({ viewport:{width:w,height:900}, deviceScaleFactor:dsf });
    await p.goto('file://'+process.cwd()+'/present-saturn.html',{waitUntil:'load'});
    await p.waitForTimeout(900);
    const H=await p.evaluate(()=>document.body.scrollHeight);
    const ov=await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
    await p.screenshot({path:name+'.png', fullPage:true});
    console.log(name,'H='+H,'overflow='+ov);
    await p.close();
  }
  await b.close();
})();
