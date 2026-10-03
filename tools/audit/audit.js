const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const W=[1440,1280,1024,768,390,320];
(async()=>{
const b=await chromium.launch();
const out={};
for(const w of W){
  const p=await b.newPage({viewport:{width:w,height:900}});
  await p.goto('file:///tmp/blk/t2.html');await p.waitForTimeout(500);
  out[w]=await p.evaluate(()=>{
    const px=v=>Math.round(parseFloat(v)||0);
    const inv={fs:{},fw:{},radius:{},colors:{},mt:{},pad:{}};
    const problems=[];
    const all=[...document.querySelectorAll('body *')];
    all.forEach(e=>{
      const c=getComputedStyle(e);
      if(e.offsetParent===null&&c.position!=='fixed')return;
      const r=e.getBoundingClientRect();
      if(r.width===0||r.height===0)return;
      const txt=(e.textContent||'').trim();
      const leaf=!([...e.children].some(ch=>(ch.textContent||'').trim()));
      if(txt&&leaf){
        const k=px(c.fontSize);inv.fs[k]=(inv.fs[k]||0)+1;
        inv.fw[c.fontWeight]=(inv.fw[c.fontWeight]||0)+1;
        inv.colors[c.color]=(inv.colors[c.color]||0)+1;
        // длина строки в символах
        const lh=px(c.lineHeight)||px(c.fontSize)*1.4;
        const lines=Math.round(r.height/lh);
        if(lines===1&&txt.length>95)problems.push(['длинная строка',txt.slice(0,40),txt.length]);
      }
      const rad=px(c.borderTopLeftRadius);if(rad)inv.radius[rad]=(inv.radius[rad]||0)+1;
      const mt=px(c.marginTop);if(mt)inv.mt[mt]=(inv.mt[mt]||0)+1;
      const pt=px(c.paddingTop);if(pt)inv.pad[pt]=(inv.pad[pt]||0)+1;
    });
    // кликабельные
    const taps=[];
    document.querySelectorAll('a,button,[role=button],input,select,textarea').forEach(e=>{
      const r=e.getBoundingClientRect();if(r.width===0&&r.height===0)return;
      const name=(e.getAttribute('aria-label')||e.textContent||'').trim().replace(/\s+/g,' ');
      taps.push({n:name.slice(0,42),h:Math.round(r.height),w:Math.round(r.width),
        href:e.getAttribute('href')||'',small:r.height<44||r.width<44});
    });
    return {inv,problems,taps,sw:document.documentElement.scrollWidth,
      cw:document.documentElement.clientWidth,h:document.body.scrollHeight};
  });
  await p.close();
}
await b.close();
console.log(JSON.stringify(out));
})();
