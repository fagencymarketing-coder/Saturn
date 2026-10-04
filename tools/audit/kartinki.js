#!/usr/bin/env node
// Проверяет, что у каждой картинки в блоках заранее известна высота.
//
//   node tools/audit/kartinki.js
//
// Зачем. Пока картинка не загрузилась, браузер считает её высоту нулевой.
// Когда она приходит, всё, что ниже, съезжает вниз. Человек в этот момент
// уже листает или перешёл по якорю — и оказывается не там, где должен.
// Так сломался переход на «Контакты»: карта географии весила пол-экрана
// и места под себя не резервировала. Заказчица 04.10 поймала это на
// кнопке «Получить предложение».
//
// Высота считается известной, если у картинки или у её обёртки объявлены
// aspect-ratio, height (не auto) или padding-bottom — либо если размеры
// стоят атрибутами прямо в теге.
const fs = require('fs'), path = require('path');
const DIR = path.join(__dirname, '..', '..', 'design', 'blocks');
const DERZHIT = /aspect-ratio|(?<!min-|max-)height:\s*(?!auto)|padding-bottom:\s*(?!0)/;

function klassy(teg){ return ((teg.match(/class="([^"]*)"/) || [,''])[1]).split(/\s+/).filter(Boolean); }

let vsego = 0; const bed = [];
for (const f of fs.readdirSync(DIR).filter(n => n.endsWith('.html'))) {
  if (f === 'head-code.html') continue;                 // собирается из остальных
  const s = fs.readFileSync(path.join(DIR, f), 'utf8');
  const css = (s.match(/<style>([\s\S]*?)<\/style>/g) || []).join('\n');
  const html = s.replace(/<style>[\s\S]*?<\/style>/g, '');

  // правила CSS: селектор → тело
  const pravila = [...css.matchAll(/([^{}]+)\{([^}]*)\}/g)]
    .map(m => [m[1].trim(), m[2]]).filter(([, t]) => DERZHIT.test(t));

  for (const m of html.matchAll(/<img\b[^>]*>/g)) {
    vsego++;
    const teg = m[0];
    if (/\bwidth=|\bheight=/.test(teg)) continue;        // размеры в теге
    // классы самой картинки и всех открытых выше тегов с классами
    const vyshe = html.slice(0, m.index);
    const predki = [...vyshe.matchAll(/<(?:div|a|figure|picture|span)\b[^>]*class="([^"]*)"/g)]
      .slice(-6).flatMap(x => x[1].split(/\s+/)).filter(Boolean);
    // Первая версия считала высоту известной, если ЛЮБОЕ правило с
    // классом из цепочки предков что-то задавало. Так она пропустила
    // карту географии — ровно тот случай, ради которого написана.
    // Теперь строго: правило должно целиться либо в саму картинку
    // (селектор кончается на img), либо в её ближайшую обёртку.
    const svoi   = klassy(teg);
    const roditel = predki.slice(-2);          // ближайшая обёртка
    const nabor  = new Set([...svoi, ...roditel]);
    const est = pravila.some(([sel]) => {
      const pro_kartinku = /(^|[\s>])img\s*$/.test(sel) || /img[.#:[]/.test(sel);
      const nash = [...nabor].some(k => sel.includes('.' + k));
      if (!nash) return false;
      if (pro_kartinku) return true;
      // правило про обёртку годится, только если оно задаёт пропорцию
      return roditel.some(k => sel.includes('.' + k));
    });
    if (!est) bed.push(`${f}  ${(teg.match(/alt="([^"]*)"/) || [,''])[1] || teg.slice(0, 58)}`);
  }
}
console.log(`\nкартинок: ${vsego}`);
if (!bed.length) console.log('высота заранее известна у всех\n');
else { console.log(`без заявленной высоты: ${bed.length}`); bed.forEach(b => console.log('  ' + b)); console.log(''); }
process.exit(bed.length ? 1 : 0);
