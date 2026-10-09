// Замер ширин колонки и карточек по блокам на живом сайте (1280/1440/1920): node tools/audit/geometry.js
// Показывает, совпадают ли края блоков и одинаковы ли карточки. Прокси контейнера иногда рвёт загрузку — скрипт повторяет попытки.
const {chromium}=require('/opt/node22/lib/node_modules/playwright');
const SEL={шапка:'.sa-hd__in, .sa-hd',герой:'.sa-hero__in','популярные: сетка':'.sa-pop__grid','популярные: карточка':'.sa-pop__card','семена: сетка':'.sa-sd__grid','семена: карточка':'.sa-sd__card','агро: шаги':'.sa-ag__steps',результаты:'.sa-res__grid','результаты: карточка':'.sa-res__card',география:'.sa-geo__map','документы: сетка':'.sa-docs__grid','документы: карточка':'.sa-docs__card',контакты:'.sa-ct__grid',форма:'.uc-saturn-form .t-form',подвал:'.sa-ft__in'};
(async()=>{const b=await chromium.launch();
for(const [W,H] of [[1280,593],[1440,800],[1920,1000]]){
 const c=await b.newContext({ignoreHTTPSErrors:true,viewport:{width:W,height:H}});const p=await c.newPage();
 let ok=false;for(let i=0;i<4&&!ok;i++){try{await p.goto('https://sssaturn.ru/home',{waitUntil:'domcontentloaded',timeout:60000});await p.waitForSelector('.sa-ft__in',{timeout:40000});ok=true}catch(e){}}
 await p.waitForTimeout(2500);
 const r=await p.evaluate(S=>Object.entries(S).map(([n,s])=>{const e=document.querySelector(s);if(!e)return n+': —';const r=e.getBoundingClientRect();return n+': '+Math.round(r.left)+'–'+Math.round(r.right)+' ('+Math.round(r.width)+')'}),SEL);
 console.log('== '+W+'\n'+r.join('\n'));await c.close()}
await b.close()})();
