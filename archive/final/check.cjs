const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  // desktop full height for section clips
  const p = await b.newPage({ viewport:{width:1200,height:1000}, deviceScaleFactor:1.4 });
  await p.goto('file://'+process.cwd()+'/present-saturn.html',{waitUntil:'networkidle'});
  await p.waitForTimeout(700);
  const full = await p.evaluate(()=>document.body.scrollHeight);
  const dov = await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
  console.log('desktop fullHeight=',full,'overflow=',dov);
  // clip catalog+card region (~ around middle)
  await p.screenshot({path:'chk-mid.png', clip:{x:0,y:1650,width:1200,height:1700}});
  await p.screenshot({path:'chk-bot.png', clip:{x:0,y:3350,width:1200,height:1700}});
  await p.close();
  // tablet
  const t = await b.newPage({ viewport:{width:768,height:1024}, deviceScaleFactor:1.5 });
  await t.goto('file://'+process.cwd()+'/present-saturn.html',{waitUntil:'networkidle'});
  await t.waitForTimeout(500);
  console.log('tablet overflow=', await t.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1));
  await t.screenshot({path:'chk-tab.png', clip:{x:0,y:520,width:768,height:1500}});
  await t.close();
  // mobile
  const m = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:2 });
  await m.goto('file://'+process.cwd()+'/present-saturn.html',{waitUntil:'networkidle'});
  await m.waitForTimeout(500);
  console.log('mobile overflow=', await m.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1));
  await m.screenshot({path:'chk-mob.png', clip:{x:0,y:1550,width:390,height:1600}});
  await m.close();
  await b.close();
})();
