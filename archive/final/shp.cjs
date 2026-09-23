const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport:{width:1200,height:1000}, deviceScaleFactor:1.5 });
  await p.goto('file://'+process.cwd()+'/present-saturn.html',{waitUntil:'networkidle'});
  await p.waitForTimeout(800);
  const overflow = await p.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
  // capture top area (title + first two steps)
  await p.screenshot({path:'present-top.png', clip:{x:0,y:0,width:1200,height:1700}});
  console.log('desktop overflow=',overflow);
  // mobile
  const m = await b.newPage({ viewport:{width:390,height:844}, deviceScaleFactor:2 });
  await m.goto('file://'+process.cwd()+'/present-saturn.html',{waitUntil:'networkidle'});
  await m.waitForTimeout(600);
  const mov = await m.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth+1);
  await m.screenshot({path:'present-mob.png', clip:{x:0,y:0,width:390,height:1500}});
  console.log('mobile overflow=',mov);
  await b.close();
})();
