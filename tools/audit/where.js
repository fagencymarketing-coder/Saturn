const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1440,height:900}});
await p.goto('file:///tmp/blk/t2.html');await p.waitForTimeout(500);
const r=await p.evaluate(()=>{const o={};
document.querySelectorAll('body *').forEach(e=>{
 const c=getComputedStyle(e);const b=e.getBoundingClientRect();
 if(b.width===0||b.height===0)return;
 const t=(e.textContent||'').trim();if(!t)return;
 if([...e.children].some(ch=>(ch.textContent||'').trim()))return;
 const k=Math.round(parseFloat(c.fontSize))+'/'+c.fontWeight+'/'+c.color;
 (o[k]=o[k]||[]).push((e.className||e.tagName)+' :: '+t.slice(0,28));});
 const out={};Object.keys(o).forEach(k=>out[k]=[o[k].length,o[k][0]]);return out;});
Object.entries(r).sort((a,b)=>parseInt(b[0])-parseInt(a[0])).forEach(([k,v])=>console.log(k.padEnd(42),v[0],'|',v[1]));
await b.close();})();
