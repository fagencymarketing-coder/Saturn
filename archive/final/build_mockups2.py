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
.wrap{position:relative;z-index:2;padding:30px 20px 26px;min-height:100%;display:flex;flex-direction:column}
/* ЛОГО: строгие пропорции 1212x405 = 3:1, без апскейла и растяжения */
.brand-logo{display:block;height:46px;width:auto;aspect-ratio:1212/405;max-width:70%;object-fit:contain}
.status{display:inline-flex;align-items:center;gap:9px;margin-top:26px;
  font-family:"IBM Plex Mono";font-size:12px;letter-spacing:.06em;text-transform:uppercase;
  color:#8CDCAE;background:rgba(31,158,87,.15);border:1px solid rgba(31,158,87,.42);
  padding:7px 14px;border-radius:30px}
.status .pulse{width:8px;height:8px;border-radius:50%;background:#39BE72}
h1{font-size:clamp(32px,9vw,44px);text-transform:uppercase;font-weight:900;margin-top:20px}
h1 .accent{color:#EE4A0E}
.lead{margin-top:18px;font-size:15.5px;color:#F1EAE2;max-width:36ch}
.chips{display:flex;gap:9px;flex-wrap:wrap;margin-top:22px}
.chip{font-family:"Archivo";font-weight:700;text-transform:uppercase;letter-spacing:.04em;font-size:12.5px;
  color:#F4EEE7;border:1px solid rgba(255,255,255,.18);background:rgba(20,18,16,.55);padding:9px 14px;border-radius:10px}
.contacts{margin-top:30px}
.contacts .lbl{font-family:"IBM Plex Mono";font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:#8A8078;margin-bottom:12px}
.cbtns{display:flex;flex-direction:column;gap:11px}
.cbtn{display:flex;align-items:center;gap:12px;text-decoration:none;font-weight:600;font-size:15px;
  padding:14px 18px;border-radius:12px;border:1px solid rgba(255,255,255,.22);color:#F4EEE7;background:rgba(20,18,16,.72)}
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
  <img class="brand-logo" src="LOGO" alt="Сатурн">
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

GRADS = '''<defs>
<linearGradient id="g1" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#FF9A5A"/><stop offset="1" stop-color="#F0490F"/></linearGradient>
<linearGradient id="g2" x1="0.1" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#F5560F"/><stop offset="1" stop-color="#C43C08"/></linearGradient>
<linearGradient id="g3" x1="0.1" y1="0" x2="0.9" y2="1"><stop offset="0" stop-color="#D53E08"/><stop offset="1" stop-color="#9A2D05"/></linearGradient>
</defs>'''

# ---------- VARIANT A: волны в правом-верхнем углу, ЛОГО слева на тёмном ----------
A_CSS = '''
.bg-top{position:absolute;top:0;right:0;width:66%;height:260px;z-index:0;pointer-events:none;
  -webkit-mask-image:linear-gradient(200deg,#000 0%,#000 42%,transparent 78%);
          mask-image:linear-gradient(200deg,#000 0%,#000 42%,transparent 78%)}
.bg-top svg{position:absolute;inset:0;width:100%;height:100%}
</style></head><body>
<div class="bg-top"><svg viewBox="0 0 280 260" preserveAspectRatio="xMaxYMin slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
GRADS
<path d="M 120,-20 C 108,25 60,70 78,115 C 96,160 210,190 235,235 L 300,300 L 300,-40 Z" fill="url(#g1)"/>
<path d="M 175,-20 C 163,20 108,80 126,125 C 142,165 235,200 258,245 L 300,300 L 300,-40 Z" fill="url(#g2)"/>
<path d="M 225,-15 C 214,22 170,88 185,132 C 197,170 262,205 285,245 L 300,285 L 300,-30 Z" fill="url(#g3)"/>
</svg></div>
'''.replace("GRADS", GRADS)

# ---------- VARIANT B: волны в правом-нижнем углу, за подвалом (не под кнопками) ----------
B_CSS = '''
.bg-bot{position:absolute;right:0;bottom:0;width:78%;height:300px;z-index:0;pointer-events:none;
  -webkit-mask-image:linear-gradient(20deg,#000 0%,#000 40%,transparent 82%);
          mask-image:linear-gradient(20deg,#000 0%,#000 40%,transparent 82%)}
.bg-bot svg{position:absolute;inset:0;width:100%;height:100%}
.wrap{min-height:100vh}
footer{color:#F0DCCF}
</style></head><body>
<div class="bg-bot"><svg viewBox="0 0 320 300" preserveAspectRatio="xMaxYMax slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
GRADS
<path d="M 340,60 C 300,95 210,120 190,175 C 172,225 250,270 300,300 L 360,320 L 360,40 Z" fill="url(#g1)"/>
<path d="M 350,110 C 315,140 235,165 218,215 C 205,255 270,285 320,310 L 360,320 L 360,90 Z" fill="url(#g2)"/>
<path d="M 355,160 C 325,185 260,210 246,255 C 236,288 300,305 340,320 L 360,325 L 360,140 Z" fill="url(#g3)"/>
</svg></div>
'''.replace("GRADS", GRADS)

open('mockup-A2-waves-top.html','w').write(HEAD + A_CSS + BODY + "</body></html>")
open('mockup-B2-waves-bottom.html','w').write(HEAD + B_CSS + BODY + "</body></html>")
print("built A2 and B2")
