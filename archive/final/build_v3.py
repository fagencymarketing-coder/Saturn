import json
logo_white = open('/tmp/logo_datauri.txt').read().strip()
logo_color = open('/tmp/logo_color.txt').read().strip()
d=json.load(open('/tmp/icons.json'))
ic=[x['svg'] for x in d['icons']]; szr=[x['svg'] for x in d['szr']]
IC={'udobreniya':ic[0],'szr':ic[1],'semena':ic[2],'agro':ic[3],'diagnostika':ic[4],
    'zernovye':ic[5],'zernobob':ic[6],'kukuruza':ic[7],'podsolnechnik':ic[8],
    'zashita':szr[0],'gerbicid':szr[1],'fungicid':szr[2],'insekticid':szr[3],'protravitel':szr[4]}
def icon(slug,size=44):
    return f'<svg class="ic" viewBox="0 0 96 96" width="{size}" height="{size}" aria-hidden="true" xmlns="http://www.w3.org/2000/svg">{IC[slug]}</svg>'

CSS = r'''<style>
:root{
  --ink:#141210; --ink-soft:#1E1A16; --panel-d:#241F1A;
  --paper:#FAF8F4; --paper-2:#F1ECE4; --white:#fff;
  --text-d:#F4EEE7; --muted-d:#B9ADA2; --muted-d2:#8A8078;
  --text-l:#17130F; --muted-l:#726657; --line-l:#E7DFD3;
  --line-d:rgba(255,255,255,.10); --line-d2:rgba(255,255,255,.16);
  --orange:#EE4A0E; --orange-deep:#C43C08; --orange-soft:#FFB48F;
  --green:#1F9E57; --green-light:#43C47D; --green-soft:#8CDCAE;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--ink);color:var(--text-d);font-family:"IBM Plex Sans",system-ui,sans-serif;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
h1,h2,h3{font-family:"Archivo",sans-serif;margin:0;line-height:1.06;letter-spacing:-.02em}
a{color:inherit;text-decoration:none}
.wrap{max-width:1160px;margin:0 auto;padding:0 24px}
.ic{color:var(--orange);display:block}
.eyebrow{font-family:"IBM Plex Mono";font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:var(--orange-deep);font-weight:600}
.sec--dark .eyebrow{color:var(--orange-soft)}
.sec-h{font-family:"Archivo";font-weight:800;text-transform:uppercase;font-size:clamp(22px,3vw,32px);margin-top:10px}
.sec-lead{margin-top:10px;max-width:60ch}
.sec--light .sec-lead{color:var(--muted-l)} .sec--dark .sec-lead{color:var(--muted-d)}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;font-size:14px;border-radius:10px;padding:12px 20px;border:1.5px solid transparent;cursor:pointer;transition:.15s}
.btn.o{background:var(--orange);color:#fff}.btn.o:hover{background:var(--orange-deep)}
.btn.g{background:var(--green);color:#fff}.btn.g:hover{background:#188047}
.btn.sm{padding:9px 14px;font-size:13px}
.sec--light .btn.ghost{background:transparent;color:var(--text-l);border-color:var(--line-l)}
.sec--dark .btn.ghost{background:transparent;color:var(--text-d);border-color:var(--line-d2)}

/* hero (dark, approved coming-soon) */
.hero{position:relative;overflow:hidden;padding:44px 0 66px;background:linear-gradient(105deg,#14100c 0%,#1f1710 40%,#7d2c08 92%,var(--orange-deep) 122%)}
.hero .bg-art{position:absolute;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
.hero .bg-mob{display:none}
.hero::after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(0deg,rgba(20,16,12,.5),transparent 55%)}
.hero .in{position:relative;z-index:2;max-width:940px}
.hero .brand-logo{height:52px;width:auto;display:block;aspect-ratio:1212/405;object-fit:contain;margin-bottom:34px}
.status{display:inline-flex;align-items:center;gap:9px;font-family:"IBM Plex Mono";font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:var(--green-soft);background:rgba(31,158,87,.15);border:1px solid rgba(31,158,87,.42);padding:6px 13px;border-radius:30px}
.status span{width:8px;height:8px;border-radius:50%;background:var(--green-light);display:block}
.hero h1{font-size:clamp(32px,5vw,54px);text-transform:uppercase;font-weight:900;margin:16px 0 0}
.hero h1 .accent{color:var(--orange)}
.hero p{color:#EBE0D6;margin:18px 0 0;font-size:17px;max-width:60ch}
.hero .chips{display:flex;gap:9px;flex-wrap:wrap;margin-top:22px}
.hero .chip{font-family:"IBM Plex Mono";font-size:12px;border:1px solid rgba(255,255,255,.24);border-radius:20px;padding:6px 13px;color:#F4E7DE}
.lbl{font-family:"IBM Plex Mono";font-size:11.5px;letter-spacing:.18em;text-transform:uppercase;color:var(--muted-d2);margin:34px 0 14px}
.cbtns{display:flex;gap:12px;flex-wrap:wrap}
.cbtn{flex:1 1 205px;display:inline-flex;align-items:center;gap:11px;font-weight:600;font-size:15px;padding:14px 20px;border-radius:12px;border:1px solid var(--line-d2);color:var(--text-d);background:rgba(20,18,16,.55)}
.cbtn .i{width:26px;height:26px;flex:none;display:grid;place-items:center;font-size:17px;color:var(--green-light)}
.cbtn.pri{background:var(--green);border-color:var(--green);color:#fff}.cbtn.pri .i{color:#fff}
.cbtn .sub{display:block;font-size:11px;font-weight:500;color:var(--muted-d);margin-top:1px}
.cbtn b{font-weight:700;white-space:nowrap}

/* sections */
.sec{padding:66px 0}
.sec--light{background:var(--paper);color:var(--text-l);border-bottom:1px solid var(--line-l)}
.sec--dark{background:var(--ink);color:var(--text-d);border-bottom:1px solid var(--line-d)}
.sec--paper2{background:var(--paper-2)}

/* stats */
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}
.stat{background:var(--white);border:1px solid var(--line-l);border-radius:14px;padding:24px}
.stat b{font-family:"Archivo";font-size:38px;color:var(--orange);display:block;line-height:1}
.stat span{color:var(--muted-l);font-size:14px;display:block;margin-top:8px}

/* feature/direction cards with icons */
.feat{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}
.fcard{border-radius:14px;padding:22px}
.sec--dark .fcard{background:var(--ink-soft);border:1px solid var(--line-d)}
.sec--light .fcard{background:var(--white);border:1px solid var(--line-l)}
.fcard .ic{margin-bottom:14px}
.fcard h3{font-size:18px}
.fcard p{font-size:13px;margin:6px 0 0}
.sec--dark .fcard p{color:var(--muted-d)} .sec--light .fcard p{color:var(--muted-l)}
.cults{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:16px}
.cult{display:flex;align-items:center;gap:12px;border-radius:12px;padding:12px 14px;font-weight:600;font-size:14px}
.sec--dark .cult{background:rgba(255,255,255,.03);border:1px solid var(--line-d)}
.sec--light .cult{background:var(--white);border:1px solid var(--line-l)}
.cult .ic{flex:none}

/* szr quick strip */
.szrstrip{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:18px 0 6px}
.szr{text-align:center;border-radius:12px;padding:16px 8px;cursor:pointer}
.sec--light .szr{background:var(--white);border:1px solid var(--line-l)}
.szr .ic{margin:0 auto 8px}
.szr span{font-size:13px;font-weight:600}

/* filters + catalog */
.fil .lab{font-family:"IBM Plex Mono";font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted-l);margin:16px 0 8px}
.chip2{display:inline-block;border:1.4px solid var(--line-l);border-radius:22px;padding:8px 16px;font-size:13px;margin:0 8px 8px 0;color:var(--text-l);background:var(--white);cursor:pointer}
.chip2.on{background:var(--orange);border-color:var(--orange);color:#fff;font-weight:700}
.chip2.on.g{background:var(--green);border-color:var(--green)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:20px}
.card{border-radius:14px;padding:16px;transition:.15s}
.sec--light .card{background:var(--white);border:1px solid var(--line-l)}
.sec--dark .card{background:var(--ink-soft);border:1px solid var(--line-d)}
.card:hover{transform:translateY(-2px)}
.card .img{height:140px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:13px}
.sec--light .card .img{background:linear-gradient(135deg,#F1ECE4,#E7DFD3);color:#B9ADA2;border:1px solid var(--line-l)}
.sec--dark .card .img{background:linear-gradient(135deg,#2a231d,#1c1712);color:var(--muted-d2);border:1px solid var(--line-d)}
.card h3{font-size:18px;margin:14px 0 0}
.card .meta{font-size:13px;margin:4px 0 0;font-family:"IBM Plex Mono"}
.sec--light .card .meta{color:var(--muted-l)} .sec--dark .card .meta{color:var(--muted-d2)}
.card .row{display:flex;gap:8px;margin-top:14px}

/* product detail (dark) */
.detail{display:grid;grid-template-columns:1fr 1.1fr;gap:24px;background:var(--ink-soft);border:1px solid var(--line-d);border-radius:16px;padding:22px;margin-top:24px}
.detail .gal{background:linear-gradient(135deg,#2a231d,#1c1712);border:1px solid var(--line-d);border-radius:12px;min-height:260px;display:flex;align-items:center;justify-content:center;color:var(--muted-d2)}
.tabs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}
.tab{font-size:13px;padding:8px 14px;border-radius:9px;border:1px solid var(--line-d);background:transparent;color:var(--muted-d)}
.tab.on{background:var(--text-d);color:var(--ink);border-color:var(--text-d);font-weight:700}
.spec{width:100%;border-collapse:collapse;font-size:14px}
.spec td{padding:11px 4px;border-bottom:1px solid var(--line-d)}
.spec td:first-child{color:var(--muted-d);width:46%}
.detail .price{margin-top:18px;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.detail .price .pq{font-family:"Archivo";font-weight:800;font-size:20px;color:var(--orange-soft)}

/* tiles / clients */
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}
.tile{border-radius:12px;height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;font-size:13px}
.sec--light .tile{background:var(--white);border:1px solid var(--line-l);color:var(--muted-l)}
.tile .dic{font-size:34px}
.clients{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}
.client{border-radius:12px;height:88px;display:flex;align-items:center;justify-content:center;font-size:13px}
.sec--dark .client{background:var(--panel-d);border:1px dashed var(--line-d2);color:var(--muted-d2)}

/* form CTA (light section, orange card) */
.cta{position:relative;overflow:hidden;background:linear-gradient(100deg,#17130F,#3a2011 78%,#7d2c08 130%);border-radius:20px;padding:40px;color:var(--text-d)}
.cta .eyebrow{color:var(--orange-soft)}
.cta h2{font-size:clamp(24px,3.2vw,34px);text-transform:uppercase;font-weight:900;margin-top:10px}
.cta p{color:#EBE0D6;margin:10px 0 0}
.form{display:grid;grid-template-columns:1fr 1fr 1fr auto;gap:12px;margin-top:22px}
.form input{background:rgba(255,255,255,.08);border:1px solid var(--line-d2);border-radius:10px;padding:14px;color:var(--text-d);font-size:14px;font-family:inherit}
.form input::placeholder{color:var(--muted-d)}
.cta .note{color:var(--muted-d);font-size:13px;margin-top:12px}

/* footer */
footer{background:#100d0b;padding:44px 0 60px;color:var(--muted-d)}
.fgrid{display:grid;grid-template-columns:1.4fr 1fr 1.2fr 1fr;gap:24px}
footer img{height:32px;margin-bottom:12px}
footer .col b{display:block;font-size:14px;margin-bottom:10px;font-family:"Archivo";text-transform:uppercase;letter-spacing:.04em;color:var(--text-d)}
footer .col p,footer .col a{color:var(--muted-d);font-size:14px;margin:5px 0;display:block}
footer .copy{color:var(--muted-d2);font-size:13px;margin-top:30px;padding-top:18px;border-top:1px solid var(--line-d);font-family:"IBM Plex Mono"}

@media(max-width:900px){
  .detail{grid-template-columns:1fr}
  .stats,.feat,.cults,.tiles,.clients,.form,.fgrid{grid-template-columns:repeat(2,1fr)}
  .szrstrip{grid-template-columns:repeat(3,1fr)}
  .grid{grid-template-columns:1fr 1fr}
  .hero .bg-art{display:none}
  .hero .bg-mob{display:block;position:absolute;top:0;right:0;width:70%;height:280px;z-index:0;pointer-events:none;-webkit-mask-image:linear-gradient(200deg,#000 0%,#000 42%,transparent 80%);mask-image:linear-gradient(200deg,#000 0%,#000 42%,transparent 80%)}
  .hero .bg-mob svg{position:absolute;inset:0;width:100%;height:100%}
}
@media(max-width:560px){
  .grid,.stats,.feat,.cults,.tiles,.clients,.fgrid,.form,.szrstrip{grid-template-columns:1fr}
  .cbtns{flex-direction:column;align-items:stretch}
  .cta{padding:26px}
}

/* ===== правки: контраст заглушек, тёмный каталог, светлая форма ===== */
.chip2{display:inline-flex;align-items:center;gap:8px;vertical-align:middle}
.chip2 .ic{width:18px;height:18px}
.chip2.on .ic{color:#fff}
.sec--dark .chip2{background:rgba(255,255,255,.04);border-color:var(--line-d2);color:var(--text-d)}
.sec--dark .fil .lab{color:var(--muted-d2)}
/* деталь-карточка на светлом */
.sec--light .detail{background:#fff;border-color:var(--line-l)}
.sec--light .tab{border-color:var(--line-l);color:var(--muted-l)}
.sec--light .tab.on{background:var(--text-l);color:#fff;border-color:var(--text-l)}
.sec--light .spec td{border-bottom-color:var(--line-l)}
.sec--light .spec td:first-child{color:var(--muted-l)}
.sec--light .detail .price .pq{color:var(--orange-deep)}
/* ЗАГЛУШКИ: на тёмном — светлые, на светлом — тёмные */
.sec--dark .card .img,.sec--dark .detail .gal,.sec--dark .tile{background:#EFE9E1;border:1px solid #E0D8CB;color:#8A8078}
.sec--light .card .img,.sec--light .detail .gal,.sec--light .client{background:#241F1A;border:1px solid rgba(255,255,255,.14);color:#9A9088}
/* форма на светлом */
.sec--paper2{background:var(--paper-2)}
.form--light input{background:#fff;border:1px solid var(--line-l);color:var(--text-l)}
.form--light input::placeholder{color:var(--muted-l)}
.note--light{color:var(--muted-l)}

/* ===== V3 conversion components ===== */
.hdr{position:sticky;top:0;z-index:50;background:rgba(20,18,16,.90);backdrop-filter:blur(10px);border-bottom:1px solid var(--line-d)}
.hdr .in{display:flex;align-items:center;gap:22px;padding:12px 0}
.hdr img{height:30px;width:auto}
.hdr nav{display:flex;gap:20px;color:var(--muted-d);font-size:14px;font-weight:500}
.hdr nav a:hover{color:var(--text-d)}
.hdr .sp{flex:1}
.hdr .ph{font-weight:700;font-size:15px;color:var(--text-d);white-space:nowrap}
.microtrust{display:flex;gap:24px;flex-wrap:wrap;margin-top:22px;color:#EBE0D6;font-size:14px}
.microtrust span{display:inline-flex;align-items:center;gap:8px}
.microtrust b{color:var(--green-soft);font-weight:800}
.hero .btns{display:flex;gap:12px;flex-wrap:wrap;margin-top:26px}
.brandrow{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:26px}
.brandbox{background:#fff;border:1px solid #E7DFD3;border-radius:12px;padding:24px;text-align:center;color:#17130F;font-weight:800;font-family:"Archivo";letter-spacing:.01em}
.brandbox small{display:block;font-weight:500;font-family:"IBM Plex Sans";color:#8A8078;font-size:12px;margin-top:4px}
.steps{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:26px}
.stepc{border-radius:14px;padding:22px}
.sec--dark .stepc{background:var(--ink-soft);border:1px solid var(--line-d)}
.sec--light .stepc{background:#fff;border:1px solid var(--line-l)}
.stepc .n{font-family:"Archivo";font-weight:900;font-size:30px;color:var(--orange);line-height:1}
.stepc h3{font-size:17px;margin:10px 0 0}
.stepc p{font-size:13px;margin:6px 0 0}
.sec--dark .stepc p{color:var(--muted-d)} .sec--light .stepc p{color:var(--muted-l)}
.ctaband{display:flex;align-items:center;gap:16px;flex-wrap:wrap;margin-top:30px;padding-top:24px;border-top:1px solid var(--line-d)}
.ctaband .t{font-family:"Archivo";font-weight:800;font-size:20px}
.stock{display:inline-block;font-family:"IBM Plex Mono";font-size:11px;color:var(--green);background:var(--green-soft);border:1px solid rgba(31,158,87,.35);border-radius:20px;padding:3px 9px;margin-top:8px}
.sec--dark .stock{color:var(--green-light)}
.formwrap{display:grid;grid-template-columns:1.1fr .9fr;gap:26px;align-items:start;margin-top:26px}
.formcard{background:#fff;border:1px solid var(--line-l);border-radius:16px;padding:24px}
.formcard .frow{display:flex;gap:12px;flex-wrap:wrap}
.formcard input{flex:1 1 180px;background:#FBF8F3;border:1px solid var(--line-l);border-radius:10px;padding:14px;font-size:14px;color:var(--text-l);font-family:inherit}
.formcard input::placeholder{color:var(--muted-l)}
.formcard .full{width:100%}
.reassure{display:flex;gap:18px;flex-wrap:wrap;color:var(--muted-l);font-size:13px;margin-top:12px}
.reassure b{color:var(--green-dark)}
.sidecta{background:var(--ink-soft);border:1px solid var(--line-d);border-radius:16px;padding:24px;color:var(--text-d)}
.sidecta h3{font-size:19px}
.sidecta p{color:var(--muted-d);font-size:14px;margin:8px 0 16px}
.msgs{display:flex;flex-direction:column;gap:10px}
.msg{display:flex;align-items:center;gap:11px;border:1px solid var(--line-d2);border-radius:12px;padding:12px 16px;font-weight:600;color:var(--text-d)}
.msg .i{color:var(--green-light);width:22px;text-align:center}
@media(max-width:900px){.steps,.brandrow{grid-template-columns:repeat(2,1fr)}.formwrap{grid-template-columns:1fr}.hdr nav,.hdr .ph{display:none}}
@media(max-width:560px){.steps,.brandrow{grid-template-columns:1fr}}
</style>'''

HERO_WAVES = '''<svg class="bg-art" viewBox="0 0 1440 900" preserveAspectRatio="xMaxYMax slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs><linearGradient id="g1" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#FF9A5A"/><stop offset="1" stop-color="#F0490F"/></linearGradient>
<linearGradient id="g2" x1="0.1" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#F5560F"/><stop offset="1" stop-color="#C43C08"/></linearGradient>
<linearGradient id="g3" x1="0.1" y1="0" x2="0.9" y2="1"><stop offset="0" stop-color="#D53E08"/><stop offset="1" stop-color="#9A2D05"/></linearGradient></defs>
<path d="M 905,0 C 890,25 802,97 815,150 C 828,203 971,262 985,320 C 999,378 888,443 900,500 C 912,557 1015,607 1060,660 C 1105,713 1142,780 1170,820 C 1198,860 1220,887 1230,900 L 1440,900 L 1440,0 Z" fill="url(#g1)"/>
<path d="M 1120,70 C 1106,100 1022,190 1035,250 C 1048,310 1185,368 1195,430 C 1205,492 1086,558 1095,620 C 1104,682 1216,753 1250,800 C 1284,847 1292,883 1300,900 L 1440,900 L 1440,70 Z" fill="url(#g2)"/>
<path d="M 1285,230 C 1272,263 1197,367 1205,430 C 1213,493 1327,548 1335,610 C 1343,672 1253,752 1255,800 C 1257,848 1330,883 1345,900 L 1440,900 L 1440,230 Z" fill="url(#g3)"/></svg>
<div class="bg-mob"><svg viewBox="0 0 280 260" preserveAspectRatio="xMaxYMin slice" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
<defs><linearGradient id="m1" x1="0" y1="0" x2="0.7" y2="1"><stop offset="0" stop-color="#FF9A5A"/><stop offset="1" stop-color="#F0490F"/></linearGradient>
<linearGradient id="m2" x1="0.1" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#F5560F"/><stop offset="1" stop-color="#C43C08"/></linearGradient>
<linearGradient id="m3" x1="0.1" y1="0" x2="0.9" y2="1"><stop offset="0" stop-color="#D53E08"/><stop offset="1" stop-color="#9A2D05"/></linearGradient></defs>
<path d="M 120,-20 C 108,25 60,70 78,115 C 96,160 210,190 235,235 L 300,300 L 300,-40 Z" fill="url(#m1)"/>
<path d="M 175,-20 C 163,20 108,80 126,125 C 142,165 235,200 258,245 L 300,300 L 300,-40 Z" fill="url(#m2)"/>
<path d="M 225,-15 C 214,22 170,88 185,132 C 197,170 262,205 285,245 L 300,285 L 300,-30 Z" fill="url(#m3)"/></svg></div>'''

HTML = f'''<!DOCTYPE html><html lang="ru"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Сатурн · Прототип сайта</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@600;700;800;900&family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
{CSS}</head><body>

<!-- ШАПКА (sticky) -->
<header class="hdr"><div class="wrap in">
  <img src="{logo_white}" alt="Сатурн">
  <nav><a href="#catalog">Каталог</a><a href="#order">Как заказать</a><a href="#certs">Гарантии</a><a href="#form">Контакты</a></nav>
  <span class="sp"></span><span class="ph">☎ +7 960 953-48-88</span>
  <a class="btn o sm" href="#form">Оставить заявку</a>
</div></header>

<!-- 1. HERO (тёмный, продающий) -->
<section class="hero">{HERO_WAVES}
  <div class="wrap in">
    <span class="status" style="background:rgba(238,74,14,.14);border-color:rgba(238,74,14,.4);color:var(--orange-soft)"><span style="background:var(--orange)"></span>Официальный дилер · оптовые поставки</span>
    <h1>Удобрения, СЗР и семена оптом —<br><span class="accent">с подбором под культуру и задачу</span></h1>
    <p>Официальный дилер Реликт ДВ, Волский Биохим и Фертика. Наличие на складе, отгрузка от 1 тонны, все документы и СГР. Поможем подобрать препараты и рассчитать нормы.</p>
    <div class="btns"><a class="btn o" href="#form">Получить подбор и цену</a><a class="btn ghost" href="#catalog">Смотреть каталог</a></div>
    <div class="microtrust"><span><b>✓</b> Официальный дилер</span><span><b>✓</b> Отгрузка от 1 т за 24 ч</span><span><b>✓</b> Документы и СГР</span></div>
  </div>
</section>

<!-- 2. ВЫГОДЫ / ЧТО ПОСТАВЛЯЕМ (светлый) -->
<section class="sec sec--light"><div class="wrap">
  <div class="eyebrow">Почему Сатурн</div><h2 class="sec-h">Работаем как ваш агропартнёр</h2>
  <div class="feat">
    <div class="fcard">{icon('szr')}<h3>Официально и легально</h3><p>Прямые поставки от производителей, сертификаты и СГР на всю продукцию.</p></div>
    <div class="fcard">{icon('agro')}<h3>Подбор под задачу</h3><p>Поможем выбрать препарат под культуру, фазу и проблему поля.</p></div>
    <div class="fcard">{icon('diagnostika')}<h3>Нормы и расчёт</h3><p>Рассчитаем нормы расхода и подготовим КП в течение дня.</p></div>
    <div class="fcard">{icon('semena')}<h3>Всё в одном месте</h3><p>Удобрения, средства защиты и семена — одна заявка, одна отгрузка.</p></div>
  </div>
</div></section>

<!-- 3. ОФИЦИАЛЬНЫЙ ДИЛЕР (тёмный) -->
<section class="sec sec--dark" id="about"><div class="wrap">
  <div class="eyebrow">Наши производители</div><h2 class="sec-h">Официальный дилер трёх заводов</h2>
  <p class="sec-lead">Поставляем оригинальную продукцию напрямую — без переплат и подделок.</p>
  <div class="brandrow">
    <div class="brandbox">Реликт ДВ<small>удобрения · СЗР</small></div>
    <div class="brandbox">Волский Биохим<small>удобрения · СЗР</small></div>
    <div class="brandbox">Фертика<small>удобрения</small></div>
  </div>
  <div class="stats" style="margin-top:26px">
    <div class="stat"><b>15+</b><span>лет на рынке</span></div>
    <div class="stat"><b>500+</b><span>препаратов в наличии</span></div>
    <div class="stat"><b>24 ч</b><span>средний срок отгрузки</span></div>
    <div class="stat"><b>1000+ т</b><span>отгружаем в год</span></div>
  </div>
</div></section>

<!-- 4. КАТАЛОГ: удобрения и защита (светлый) -->
<section class="sec sec--light" id="catalog"><div class="wrap">
  <div class="eyebrow">Каталог</div><h2 class="sec-h">Удобрения и защита растений</h2>
  <p class="sec-lead">Выберите категорию и производителя — фильтры совмещаются. Цена по запросу, отгрузка оптом.</p>
  <div class="fil"><div class="lab">Категория</div>
    <span class="chip2 on">Все</span><span class="chip2">{icon('udobreniya',18)}Минеральные удобрения</span><span class="chip2">{icon('szr',18)}Защита растений (СЗР)</span></div>
  <div class="fil"><div class="lab">Бренд</div>
    <span class="chip2 on g">Все</span><span class="chip2">Реликт ДВ</span><span class="chip2">Волский Биохим</span><span class="chip2">Фертика</span></div>
  <div class="grid">
    <div class="card"><div class="img">Фото препарата</div><h3>Препарат №1</h3><div class="meta">Реликт ДВ · гербицид</div><span class="stock">в наличии</span><div class="row"><a class="btn ghost sm">Подробнее</a><a class="btn o sm">Запросить цену</a></div></div>
    <div class="card"><div class="img">Фото препарата</div><h3>Препарат №2</h3><div class="meta">Фертика · удобрение</div><span class="stock">в наличии</span><div class="row"><a class="btn ghost sm">Подробнее</a><a class="btn o sm">Запросить цену</a></div></div>
    <div class="card"><div class="img">Фото препарата</div><h3>Препарат №3</h3><div class="meta">Волский Биохим · фунгицид</div><span class="stock">в наличии</span><div class="row"><a class="btn ghost sm">Подробнее</a><a class="btn o sm">Запросить цену</a></div></div>
  </div>
  <div style="margin-top:24px"><a class="btn ghost" href="#form">Открыть весь каталог</a></div>
</div></section>

<!-- 5. КАТАЛОГ: семена (тёмный) -->
<section class="sec sec--dark" id="catalog-seeds"><div class="wrap">
  <div class="eyebrow">Каталог</div><h2 class="sec-h">Семена</h2>
  <p class="sec-lead">Проверенные семена под ваш регион и культуру. Цена по запросу, отгрузка оптом.</p>
  <div class="fil"><div class="lab">Культура</div>
    <span class="chip2 on">Все</span><span class="chip2">{icon('zernovye',18)}Зерновые</span><span class="chip2">{icon('kukuruza',18)}Кукуруза</span><span class="chip2">{icon('podsolnechnik',18)}Подсолнечник</span><span class="chip2">{icon('zernobob',18)}Зернобобовые</span></div>
  <div class="grid">
    <div class="card"><div class="img">Фото семян</div><h3>Пшеница озимая</h3><div class="meta">зерновые · сорт</div><span class="stock">в наличии</span><div class="row"><a class="btn ghost sm">Подробнее</a><a class="btn o sm">Запросить цену</a></div></div>
    <div class="card"><div class="img">Фото семян</div><h3>Кукуруза</h3><div class="meta">кукуруза · гибрид ФАО 200</div><span class="stock">в наличии</span><div class="row"><a class="btn ghost sm">Подробнее</a><a class="btn o sm">Запросить цену</a></div></div>
    <div class="card"><div class="img">Фото семян</div><h3>Подсолнечник</h3><div class="meta">подсолнечник · гибрид</div><span class="stock">в наличии</span><div class="row"><a class="btn ghost sm">Подробнее</a><a class="btn o sm">Запросить цену</a></div></div>
  </div>
</div></section>

<!-- 6. АГРОСОПРОВОЖДЕНИЕ (светлый) -->
<section class="sec sec--light"><div class="wrap">
  <div class="eyebrow">Услуга</div><h2 class="sec-h">Агросопровождение: подбор и нормы</h2>
  <p class="sec-lead">Не просто продаём — помогаем принять решение. Опишите задачу — предложим схему.</p>
  <div class="feat" style="grid-template-columns:repeat(3,1fr)">
    <div class="fcard">{icon('agro')}<h3>Подбор под культуру</h3><p>Схема защиты и питания под вашу культуру и фазу развития.</p></div>
    <div class="fcard">{icon('diagnostika')}<h3>Диагностика поля</h3><p>Поможем определить проблему и подобрать решение.</p></div>
    <div class="fcard">{icon('udobreniya')}<h3>Расчёт норм и КП</h3><p>Рассчитаем нормы расхода и подготовим коммерческое предложение.</p></div>
  </div>
</div></section>

<!-- 7. КАК ЗАКАЗАТЬ (тёмный) + CTA -->
<section class="sec sec--dark" id="order"><div class="wrap">
  <div class="eyebrow">Просто</div><h2 class="sec-h">Как заказать</h2>
  <div class="steps">
    <div class="stepc"><div class="n">1</div><h3>Заявка</h3><p>Оставляете заявку или пишете в мессенджер — что нужно.</p></div>
    <div class="stepc"><div class="n">2</div><h3>Подбор и КП</h3><p>Подбираем препараты, считаем нормы, присылаем цену в течение дня.</p></div>
    <div class="stepc"><div class="n">3</div><h3>Договор</h3><p>Согласуем условия и оформляем документы.</p></div>
    <div class="stepc"><div class="n">4</div><h3>Отгрузка</h3><p>Отгружаем от 1 тонны — со склада, с документами и СГР.</p></div>
  </div>
  <div class="ctaband"><span class="t">Начнём с подбора?</span><a class="btn o" href="#form">Получить подбор и цену</a><span class="sec-lead" style="margin:0">или звоните: <b style="color:var(--text-d)">+7 960 953-48-88</b></span></div>
</div></section>

<!-- 8. СЕРТИФИКАТЫ (светлый) -->
<section class="sec sec--light" id="certs"><div class="wrap">
  <div class="eyebrow">Гарантии</div><h2 class="sec-h">Сертификаты и СГР</h2>
  <p class="sec-lead">Вся продукция официальная, с документами. Предоставляем по запросу.</p>
  <div class="tiles">
    <div class="tile"><span class="dic">📄</span>Сертификат соответствия</div>
    <div class="tile"><span class="dic">📄</span>Свидетельство СГР</div>
    <div class="tile"><span class="dic">📄</span>Паспорт качества</div>
    <div class="tile"><span class="dic">🏆</span>Дипломы и награды</div>
  </div>
</div></section>

<!-- 9. НАМ ДОВЕРЯЮТ (тёмный) -->
<section class="sec sec--dark"><div class="wrap">
  <div class="eyebrow">Репутация</div><h2 class="sec-h">Нам доверяют</h2>
  <div class="clients"><div class="client">Клиент / лого</div><div class="client">Клиент / лого</div><div class="client">Клиент / лого</div><div class="client">Клиент / лого</div></div>
  <div class="detail" style="grid-template-columns:1fr;margin-top:16px"><div><p style="margin:0;font-size:16px">«Подобрали схему защиты под нашу пшеницу, отгрузили за день. Работаем второй сезон.»</p><div class="meta" style="margin-top:10px;color:var(--muted-d);font-family:IBM Plex Mono">— агроном, хозяйство в Алтайском крае</div></div></div>
</div></section>

<!-- 10. ФОРМА (светлый) -->
<section class="sec sec--light sec--paper2" id="form"><div class="wrap">
  <div class="eyebrow">Заявка</div><h2 class="sec-h">Оставьте заявку — подберём и пришлём цену</h2>
  <div class="formwrap">
    <div class="formcard">
      <div class="frow"><input placeholder="Телефон *"><input placeholder="Имя"></div>
      <input class="full" style="margin-top:12px" placeholder="Что интересует (препарат / культура)">
      <div style="margin-top:14px"><a class="btn o" href="#">Получить подбор и цену</a></div>
      <div class="reassure"><span><b>✓</b> Перезвоним за 15 минут</span><span><b>✓</b> КП сегодня</span><span><b>✓</b> Данные не передаём</span></div>
    </div>
    <div class="sidecta">
      <h3>Быстрее — в мессенджер</h3><p>Напишите нам — ответим и подберём препарат.</p>
      <div class="msgs">
        <a class="msg" href="https://wa.me/79609534888" target="_blank" rel="noopener"><span class="i">✆</span> WhatsApp</a>
        <a class="msg" href="#"><span class="i">✈</span> Telegram</a>
        <a class="msg" href="tel:+79609534888"><span class="i">☎</span> +7 960 953-48-88</a>
      </div>
      <div style="margin-top:16px"><a class="btn ghost" href="#" style="border-color:var(--line-d2);color:var(--text-d)">Скачать прайс-лист (PDF)</a></div>
    </div>
  </div>
</div></section>

<!-- 11. ПОДВАЛ (тёмный) -->
<footer id="contacts"><div class="wrap">
  <div class="fgrid">
    <div class="col"><img src="{logo_white}" alt="Сатурн"><p>Официальный дилер удобрений, средств защиты растений и семян. Оптовые поставки для профессионального земледелия.</p></div>
    <div class="col"><b>Разделы</b><a href="#catalog">Каталог</a><a href="#order">Как заказать</a><a href="#certs">Гарантии</a></div>
    <div class="col"><b>Контакты</b><a>☎ +7 960 953-48-88</a><a>WhatsApp · Telegram</a><a>nilov@sssaturn.ru</a><p>г. …, ул. …</p></div>
    <div class="col"><b>Реквизиты</b><p>ИНН —</p><p>ОГРН —</p></div>
  </div>
  <div class="copy">© 2026 «Сатурн» · Система успеха · sssaturn.ru</div>
</div></footer>

</body></html>'''
open('site-prototype-v3.html','w').write(HTML)
print("written site-prototype-v3.html size", len(HTML))
