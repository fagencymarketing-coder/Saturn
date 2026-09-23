logo = open('/tmp/logo_datauri.txt').read().strip()

HEAD = '''<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Сатурн · Макет заглушки (моб.)</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box}
html,body{height:100%}
body{margin:0;background:#141210;color:#F4EEE7;font-family:"IBM Plex Sans",system-ui,sans-serif;
  line-height:1.55;-webkit-font-smoothing:antialiased;position:relative;overflow-x:hidden;min-height:100%}
h1{font-family:"Archivo";margin:0;line-height:1.05;letter-spacing:-.02em}
.wrap{position:relative;z-index:2;padding:34px 20px 26px;min-height:100%;display:flex;flex-direction:column}
.brand-logo{height:50px;width:auto;display:block}
.status{display:inline-flex;align-items:center;gap:9px;margin-top:28px;
  font-family:"IBM Plex Mono";font-size:12px;letter-spacing:.06em;text-transform:uppercase;
  color:#8CDCAE;background:rgba(31,158,87,.15);border:1px solid rgba(31,158,87,.42);
  padding:7px 14px;border-radius:30px}
.status .pulse{width:8px;height:8px;border-radius:50%;background:#39BE72}
h1{font-size:clamp(34px,10vw,46px);text-transform:uppercase;font-weight:900;margin-top:20px}
h1 .accent{color:#EE4A0E}
.lead{margin-top:18px;font-size:16px;color:#F1EAE2;max-width:34ch}
.chips{display:flex;gap:9px;flex-wrap:wrap;margin-top:22px}
.chip{font-family:"Archivo";font-weight:700;text-transform:uppercase;letter-spacing:.04em;font-size:12.5px;
  color:#F4EEE7;border:1px solid rgba(255,255,255,.18);background:rgba(20,18,16,.55);padding:9px 14px;border-radius:10px}
.contacts{margin-top:30px}
.contacts .lbl{font-family:"IBM Plex Mono";font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:#8A8078;margin-bottom:12px}
.cbtns{display:flex;flex-direction:column;gap:11px}
.cbtn{display:flex;align-items:center;gap:12px;text-decoration:none;font-weight:600;font-size:15px;
  padding:14px 18px;border-radius:12px;border:1px solid rgba(255,255,255,.22);color:#F4EEE7;background:rgba(20,18,16,.66)}
.cbtn .i{width:24px;height:24px;flex:none;display:grid;place-items:center;font-size:16px;color:#5AD08C}
.cbtn .sub{display:block;font-size:11.5px;font-weight:500;color:#CFC5BB;margin-top:1px}
.cbtn b{font-weight:700}
.cbtn.pri{background:#1F9E57;border-color:#1F9E57;color:#fff}
.cbtn.pri .i{color:#fff}
.cbtn.pri .sub{color:rgba(255,255,255,.9)}
footer{position:relative;z-index:2;margin-top:auto;padding-top:22px;
  font-family:"IBM Plex Mono";font-size:11.5px;color:#8A8078;letter-spacing:.04em}
'''

BODY = '''
<div class="wrap">
  <img class="brand-logo" src="LOGO">
  <div class="status"><span class="pulse"></span>Идёт обновление сайта</div>
  <h1>Скоро здесь<br>будет новый <span class="accent">сайт</span></h1>
  <p class="lead">«Сатурн» — поставщик удобрений, СЗР и семян для профессионального земледелия. Каталог откроется совсем скоро. А пока свяжитесь с нами напрямую.</p>
  <div class="chips">
    <span class="chip">Удобрения</span><span class="chip">СЗР</span>
    <span class="chip">Семена</span><span class="chip">Агросопровождение</span>
  </div>
  <div class="contacts">
    <div class="lbl">Связаться сейчас</div>
    <div class="cbtns">
      <a class="cbtn pri" href="#"><span class="i">&#9742;</span><span><b>+7 960 953-48-88</b><span class="sub">Позвонить</span></span></a>
      <a class="cbtn" href="#"><span class="i">&#9990;</span><span><b>WhatsApp</b><span class="sub">Написать в мессенджер</span></span></a>
      <a class="cbtn" href="#"><span class="i">&#9992;</span><span><b>Telegram</b><span class="sub">Написать в мессенджер</span></span></a>
      <a class="cbtn" href="#"><span class="i">&#9993;</span><span><b>nilov@sssaturn.ru</b><span class="sub">Написать на почту</span></span></a>
    </div>
  </div>
  <footer>sssaturn.ru &nbsp;·&nbsp; © 2026 «Сатурн» · Система успеха</footer>
</div>
'''.replace("LOGO", logo)

# Wave gradient defs (reused)
GRADS = '''<defs>
<linearGradient id="g1" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#FF9A5A"/><stop offset="1" stop-color="#F0490F"/></linearGradient>
<linearGradient id="g2" x1="0.1" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#F5560F"/><stop offset="1" stop-color="#C43C08"/></linearGradient>
<linearGradient id="g3" x1="0.1" y1="0" x2="0.9" y2="1"><stop offset="0" stop-color="#D53E08"/><stop offset="1" stop-color="#9A2D05"/></linearGradient>
</defs>'''

# ---------- VARIANT A: волны сверху-справа (top-right corner accent) ----------
A_CSS = '''
.bg-top{position:absolute;top:0;left:0;right:0;height:300px;z-index:0;pointer-events:none;
  -webkit-mask-image:linear-gradient(180deg,#000 0%,#000 40%,transparent 100%);
          mask-image:linear-gradient(180deg,#000 0%,#000 40%,transparent 100%)}
.bg-top svg{position:absolute;inset:0;width:100%;height:100%}
.wrap{padding-top:150px}
.brand-logo{margin-top:0}
</style></head><body>
<div class="bg-top"><svg viewBox="0 0 420 300" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
GRADS
<path d="M 250,-20 C 235,20 150,70 165,120 C 180,170 320,200 340,250 C 355,290 380,310 400,320 L 460,320 L 460,-40 Z" fill="url(#g1)"/>
<path d="M 320,-20 C 305,15 235,80 250,130 C 262,175 380,210 400,255 L 460,300 L 460,-40 Z" fill="url(#g2)"/>
<path d="M 380,-10 C 368,25 315,90 325,140 C 333,182 420,215 440,255 L 460,290 L 460,-30 Z" fill="url(#g3)"/>
</svg></div>
'''.replace("GRADS", GRADS)

# ---------- VARIANT B: волны снизу (bottom band) ----------
B_CSS = '''
.bg-bot{position:absolute;left:0;right:0;bottom:0;height:340px;z-index:0;pointer-events:none;
  -webkit-mask-image:linear-gradient(0deg,#000 0%,#000 35%,transparent 100%);
          mask-image:linear-gradient(0deg,#000 0%,#000 35%,transparent 100%)}
.bg-bot svg{position:absolute;inset:0;width:100%;height:100%}
.wrap{min-height:100vh;padding-bottom:60px}
footer{color:#F0DCCF}
</style></head><body>
<div class="bg-bot"><svg viewBox="0 0 420 340" preserveAspectRatio="xMidYMax slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
GRADS
<path d="M -20,360 C 20,320 120,300 170,250 C 220,200 250,120 320,120 C 370,120 410,150 440,180 L 440,360 Z" fill="url(#g1)"/>
<path d="M -20,360 C 30,335 130,320 185,275 C 235,235 275,175 340,175 C 385,175 415,200 440,225 L 440,360 Z" fill="url(#g2)"/>
<path d="M -20,360 C 40,345 150,335 205,300 C 255,268 300,225 360,225 C 400,225 420,245 440,262 L 440,360 Z" fill="url(#g3)"/>
</svg></div>
'''.replace("GRADS", GRADS)

open('mockup-A-waves-top.html','w').write(HEAD + A_CSS + BODY + "</body></html>")
open('mockup-B-waves-bottom.html','w').write(HEAD + B_CSS + BODY + "</body></html>")
print("built A and B")
