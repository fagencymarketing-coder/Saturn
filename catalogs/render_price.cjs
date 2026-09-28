const {chromium}=require('/opt/node22/lib/node_modules/playwright');
(async()=>{
 const b=await chromium.launch({args:['--no-sandbox']});
 const p=await b.newPage();
 await p.goto('file://'+__dirname+'/_price.html',{waitUntil:'networkidle'});
 await p.pdf({path:__dirname+'/Прайс-лист-Сатурн-2026.pdf',format:'A4',printBackground:true,
   margin:{top:'0',bottom:'14mm',left:'0',right:'0'},
   displayHeaderFooter:true, headerTemplate:'<div></div>',
   footerTemplate:`<div style="width:100%;font:400 7pt -apple-system,sans-serif;color:#8A837C;padding:0 12mm;display:flex;justify-content:space-between">
     <span>ООО «Сатурн» · sssaturn.ru · +7 (960) 953-48-88</span>
     <span class="pageNumber"></span></div>`});
 await b.close(); console.log('pdf готов');
})();
