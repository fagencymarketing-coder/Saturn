#!/usr/bin/env python3
"""Собирает HTML-версии политики и согласия для вставки в блок T123 на Tilda."""
import markdown, re, os

HERE = os.path.dirname(os.path.abspath(__file__))

CSS = """<style>
.saturn-legal{font-family:'Montserrat',-apple-system,Segoe UI,Roboto,sans-serif;color:#141210;font-size:16px;line-height:1.65;max-width:820px;margin:0 auto;padding:0 16px}
.saturn-legal h1{font-size:30px;line-height:1.2;font-weight:800;margin:0 0 24px}
.saturn-legal h2{font-size:20px;line-height:1.3;font-weight:700;margin:36px 0 12px}
.saturn-legal p{margin:0 0 14px}
.saturn-legal ul{margin:0 0 14px 0;padding-left:20px}
.saturn-legal li{margin:0 0 6px}
.saturn-legal strong{font-weight:600}
.saturn-legal a{color:#FF4200;text-decoration:underline;text-decoration-thickness:1px;word-break:break-word}
.saturn-legal a:hover{color:#D93800}
.saturn-legal .tbl{overflow-x:auto;-webkit-overflow-scrolling:touch;margin:0 0 20px;border:1px solid #EDE9E4;border-radius:8px}
.saturn-legal table{width:100%;border-collapse:collapse;margin:0;font-size:14px;min-width:560px}
.saturn-legal th{text-align:left;font-weight:600;background:#F6F5F3;padding:10px 12px;border:1px solid #EDE9E4}
.saturn-legal td{padding:10px 12px;border:1px solid #EDE9E4;vertical-align:top}
.saturn-legal .tbl th:first-child,.saturn-legal .tbl td:first-child{border-left:0}
.saturn-legal .tbl th:last-child,.saturn-legal .tbl td:last-child{border-right:0}
.saturn-legal hr{border:0;border-top:1px solid #EDE9E4;margin:28px 0}
@media (max-width:640px){.saturn-legal h1{font-size:24px}.saturn-legal h2{font-size:18px}.saturn-legal table{font-size:13px}.saturn-legal th,.saturn-legal td{padding:8px}}
</style>"""

# голые адреса сайта → кликабельные ссылки; почта → mailto
URL = re.compile(r'(?<!["\'=>])(https://sssaturn\.ru(?:/[\w\-/]*)?)')
MAIL = re.compile(r'(?<![:\w])([a-z][\w.\-]*@sssaturn\.ru)')


def linkify(html_text):
    out = []
    for chunk in re.split(r'(<a\b.*?</a>)', html_text, flags=re.S):
        if chunk.startswith('<a'):
            out.append(chunk)
            continue
        chunk = URL.sub(r'<a href="\1">\1</a>', chunk)
        chunk = MAIL.sub(r'<a href="mailto:\1">\1</a>', chunk)
        out.append(chunk)
    return ''.join(out)


def build(src, dst):
    md = open(os.path.join(HERE, src), encoding='utf-8').read()
    body = markdown.markdown(md, extensions=['tables'])
    body = re.sub(r'<table>(.*?)</table>',
                  lambda m: '<div class="tbl"><table>' + m.group(1) + '</table></div>',
                  body, flags=re.S)
    body = linkify(body)
    html = CSS + '\n<div class="saturn-legal">\n' + body + '\n</div>\n'
    open(os.path.join(HERE, dst), 'w', encoding='utf-8').write(html)
    print(dst, len(html), 'символов,', html.count('<a href'), 'ссылок')


if __name__ == '__main__':
    build('politika-obrabotki-pd.md', 'privacy.html')
    build('soglasie-na-obrabotku-pd.md', 'consent.html')
