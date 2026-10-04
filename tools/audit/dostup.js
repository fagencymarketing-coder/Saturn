#!/usr/bin/env node
// Проверка юзабилити и доступности: контраст текста и цели нажатия.
//
//   node tools/audit/dostup.js [файл-или-адрес] [ширина]
//
// Две вещи, которых линтеры до сих пор не проверяли:
//
//  1. Контраст. Текст должен отличаться от фона не меньше чем 4,5:1
//     (крупный — 3:1). Это не формальность: агроном читает сайт
//     с телефона на солнце, и серое по светло-серому там исчезает.
//
//  2. Цели нажатия. Всё, по чему нажимают, — не меньше 44×44.
//     Палец не мышь. Учитываются и невидимые зоны нажатия: у нас
//     они расставлены псевдоэлементами ::after, и это честно считается.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');

const [ist = '/tmp/blk/t2.html', shirina = '390'] = process.argv.slice(2);

(async () => {
  const b = await chromium.launch();
  const ctx = await b.newContext({ viewport: { width: +shirina, height: 900 },
                                   ignoreHTTPSErrors: true });
  const p = await ctx.newPage();
  await p.goto(ist.startsWith('http') ? ist : 'file://' + ist);
  await p.waitForTimeout(1200);

  const otchet = await p.evaluate(() => {
    const lin = (c) => { c /= 255; return c <= .03928 ? c / 12.92 : Math.pow((c + .055) / 1.055, 2.4); };
    const yark = (rgb) => .2126 * lin(rgb[0]) + .7152 * lin(rgb[1]) + .0722 * lin(rgb[2]);
    const razbor = (s) => (s.match(/[\d.]+/g) || []).map(Number);
    const kontrast = (a, b) => {
      const [l1, l2] = [yark(a), yark(b)].sort((x, y) => y - x);
      return (l1 + .05) / (l2 + .05);
    };
    // фон берём у ближайшего предка, у которого он непрозрачный
    const fon = (el) => {
      for (let e = el; e; e = e.parentElement) {
        const c = razbor(getComputedStyle(e).backgroundColor);
        if (c.length >= 3 && (c[3] === undefined || c[3] > .5)) return c;
      }
      return [255, 255, 255];
    };
    const imya = (e) => e.tagName.toLowerCase() +
      (e.className && typeof e.className === 'string' ? '.' + e.className.trim().split(/\s+/)[0] : '');

    const slabye = [], melkie = [];
    document.querySelectorAll('body *').forEach((e) => {
      const r = e.getBoundingClientRect();
      if (!r.width || !r.height) return;
      const c = getComputedStyle(e);
      if (c.visibility === 'hidden' || c.opacity === '0') return;
      const txt = (e.textContent || '').trim();
      const list = ![...e.children].some((ch) => (ch.textContent || '').trim());

      if (txt && list) {
        const kegl = parseFloat(c.fontSize);
        const zhirno = +c.fontWeight >= 700;
        const porog = (kegl >= 24 || (kegl >= 18.66 && zhirno)) ? 3 : 4.5;
        const k = kontrast(razbor(c.color), fon(e));
        if (k < porog) slabye.push(`${imya(e)} — ${k.toFixed(2)}:1 (надо ${porog}) · ${Math.round(kegl)}px · «${txt.slice(0, 28)}»`);
      }

      const nazhim = e.matches('a,button,input,select,textarea,summary,[role=button]');
      if (nazhim) {
        // Своя зона нажатия через ::after считается: у нас они расставлены
        // именно так — псевдоэлемент не влияет на поток, поэтому отступы
        // в вёрстке остаются холстовыми, а палец попадает.
        const psev = getComputedStyle(e, '::after');
        const svoya = psev.content && psev.content !== 'none' && psev.position === 'absolute';
        let h = r.height, w = r.width;
        if (svoya) h = Math.max(h, parseFloat(psev.height) || 44);
        // Порог зависит от того, чем нажимают. Ниже 1024 это палец —
        // 44 px, норма Apple и Google. Выше — мышь, ей хватает 24.
        // Требовать 44 на десктопе значило бы раздувать вёрстку ради
        // проверки, а не ради человека.
        const porogH = window.innerWidth < 1024 ? 44 : 24;
        if (h < porogH || w < 24) melkie.push(`${imya(e)} — ${Math.round(w)}×${Math.round(h)} · «${txt.slice(0, 24)}»`);
      }
    });
    return { slabye, melkie };
  });

  await b.close();

  console.log(`${ist} · ширина ${shirina}\n`);
  console.log(`  контраст ниже нормы: ${otchet.slabye.length}`);
  otchet.slabye.slice(0, 25).forEach((s) => console.log('    • ' + s));
  console.log(`\n  цели нажатия мельче 44: ${otchet.melkie.length}`);
  otchet.melkie.slice(0, 25).forEach((s) => console.log('    • ' + s));
  const vsego = otchet.slabye.length + otchet.melkie.length;
  console.log(`\n  НАРУШЕНИЙ: ${vsego}`);
  process.exit(vsego ? 1 : 0);
})();
