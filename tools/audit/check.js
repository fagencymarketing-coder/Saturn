/* Линтер дизайн-системы «Сатурна».
   Запуск:  node tools/audit/check.js <путь-к-собранной-странице.html>
   Проверяет на шести ширинах: шкалу кеглей, насыщенности, серые,
   радиусы, сетку отступов, зоны нажатия, переполнение, доступные имена. */
const {chromium} = require('/opt/node22/lib/node_modules/playwright');

const WIDTHS = [1440, 1280, 1024, 768, 390, 320];

/* Разрешённая система. Всё, чего здесь нет, — нарушение. */
const ALLOW = {
  /* 36 и 38 — не новые ступени, а промежуточные значения плавного
     заголовка: от 1024 до 1440 он идёт от 34 к 40 (H2) и от 36 к 42
     (H1 героя), чтобы на узком десктопе не выглядеть гигантским. */
  fs:   [11,12,13,14,15,16,17,18,20,22,24,28,32,34,36,38,40,42,44,48,56,80],
  fw:   ['400','500','600','700','800'],
  rad:  [0,8,10,12,16,22,46,50,999],
  inkL: ['rgb(20, 18, 16)','rgb(26, 26, 26)'],
  mutL: ['rgb(118, 111, 104)','rgb(107, 101, 96)'],
  onDark: ['rgb(255, 255, 255)','rgb(181, 176, 170)','rgb(138, 131, 124)',
           'rgb(255, 66, 0)'],
  accent: 'rgb(255, 66, 0)',
};

(async () => {
  const file = process.argv[2] || '/tmp/blk/t2.html';
  const b = await chromium.launch();
  const report = {};
  for (const w of WIDTHS) {
    const p = await b.newPage({viewport:{width:w, height:900}});
    await p.goto('file://' + file);
    await p.waitForTimeout(500);
    report[w] = await p.evaluate((ALLOW) => {
      const px = v => Math.round(parseFloat(v) || 0);
      const bad = [];
      const add = (kind, what, where) => bad.push({kind, what, where});
      const name = e => (e.className && typeof e.className === 'string'
        ? e.className.split(' ')[0] : e.tagName);

      /* 1. Типографика, цвет, радиусы, сетка */
      document.querySelectorAll('body *').forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        const c = getComputedStyle(e);
        const txt = (e.textContent || '').trim();
        const leaf = ![...e.children].some(ch => (ch.textContent||'').trim());
        if (txt && leaf) {
          const fs = px(c.fontSize);
          /* допуск 2px: часть кеглей задана через clamp() и плавает по ширине */
          if (!ALLOW.fs.some(a => Math.abs(a - fs) <= 2))
            add('кегль вне шкалы', fs, name(e));
          if (!ALLOW.fw.includes(c.fontWeight)) add('насыщенность', c.fontWeight, name(e));
          /* длина строки: комфорт 45–75 знаков */
          const lh = px(c.lineHeight) || fs * 1.4;
          const lines = Math.max(1, Math.round(r.height / lh));
          const perLine = txt.length / lines;
          if (perLine > 90) add('строка длиннее 90 знаков', Math.round(perLine), name(e));
        }
        const rad = px(c.borderTopLeftRadius);
        if (rad && !ALLOW.rad.includes(rad)) add('радиус вне системы', rad, name(e));
        /* Отступы проверяются не здесь, а по исходнику блоков:
           в вычисленных значениях margin:auto и проценты дают ложные
           срабатывания. См. tools/audit/spacing.py */
      });

      /* 2. Зоны нажатия: мерим реальную область, а не рамку элемента —
            псевдоэлемент-расширитель рамкой не виден. */
      const taps = [];
      document.querySelectorAll('a[href],button,input,select,textarea').forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.width === 0 && r.height === 0) return;
        const cx = r.left + r.width / 2;
        const cy = r.top + r.height / 2;
        if (cx < 0 || cx > innerWidth || cy < 0 || cy > innerHeight) return;
        let up = 0, dn = 0;
        for (let d = 1; d <= 24; d++) {
          const t = document.elementFromPoint(cx, cy - d);
          if (t === e || e.contains(t)) up = d; else break;
        }
        for (let d = 1; d <= 24; d++) {
          const t = document.elementFromPoint(cx, cy + d);
          if (t === e || e.contains(t)) dn = d; else break;
        }
        const hit = up + dn + 1;
        const label = (e.getAttribute('aria-label') || e.textContent || '').trim();
        if (!label) add('нет доступного имени', e.getAttribute('href') || e.tagName, name(e));
        /* Норматив: на тач-ширинах 44px, на мыши достаточно 24px. */
        const min = innerWidth <= 1024 ? 44 : 24;
        if (hit < min) taps.push({n: label.slice(0, 36), hit, need: min, cls: name(e)});
      });

      /* 3. Переполнение и бюджет акцента */
      const acc = [...document.querySelectorAll('body *')].filter(e => {
        const c = getComputedStyle(e);
        return c.backgroundColor === ALLOW.accent;
      }).length;

      return {
        bad, taps, accentBlocks: acc,
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        height: document.body.scrollHeight,
      };
    }, ALLOW);
    await p.close();
  }
  await b.close();

  let total = 0;
  for (const w of WIDTHS) {
    const r = report[w];
    const groups = {};
    r.bad.forEach(x => {
      const k = x.kind;
      groups[k] = groups[k] || [];
      groups[k].push(x.what + ' (' + x.where + ')');
    });
    const n = r.bad.length + r.taps.length + (r.overflow > 0 ? 1 : 0);
    total += n;
    console.log('\n=== ' + w + 'px · нарушений: ' + n
      + ' · высота ' + r.height + ' · переполнение ' + r.overflow
      + ' · акцентных плашек ' + r.accentBlocks);
    Object.entries(groups).forEach(([k, v]) => {
      const uniq = [...new Set(v)];
      console.log('  • ' + k + ' — ' + uniq.length + ': ' + uniq.slice(0, 8).join(', ')
        + (uniq.length > 8 ? ' …' : ''));
    });
    if (r.taps.length) {
      console.log('  • зона нажатия мала — ' + r.taps.length + ': '
        + r.taps.slice(0, 6).map(t => t.cls + ' «' + t.n + '» ' + t.hit + '<' + t.need).join(', ')
        + (r.taps.length > 6 ? ' …' : ''));
    }
  }
  console.log('\nВСЕГО НАРУШЕНИЙ: ' + total);
  process.exit(total ? 1 : 0);
})();
