const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1280,height:900}, deviceScaleFactor:1.3 });
  await p.goto('file://'+process.cwd()+'/site-prototype.html',{waitUntil:'load'});
  await p.waitForTimeout(900);
  console.log('desktop overflow=', await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1),'H=',await p.evaluate(()=>document.body.scrollHeight));
  await p.screenshot({path:'site-desk.png', fullPage:true});
  await p.close();
  const m = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:2 });
  await m.goto('file://'+process.cwd()+'/site-prototype.html',{waitUntil:'load'});
  await m.waitForTimeout(700);
  console.log('mobile overflow=', await m.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1));
  await m.screenshot({path:'site-mob.png', fullPage:true});
  await m.close();
  await b.close();
})();
