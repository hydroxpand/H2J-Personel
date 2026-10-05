# A4 가로(297x210mm) 한 쪽에 보드 하나. 96dpi 기준 1123x794 CSS px.
import gen
CSS = open('gen.py').read()
style_start = CSS.index('<style>'); style_end = CSS.index('</style>')+8
style = CSS[style_start:style_end]
# 인쇄용: 흰 종이 고정(라이트 단일 테마), 페이지 박스
style = style.replace('</style>', '''
html,body{margin:0;padding:0;background:#fff}
body{padding:0}
.page{width:1123px;height:794px;box-sizing:border-box;padding:44px 56px 36px;background:#fff;color:var(--fg);
  display:grid;grid-template-rows:auto auto auto minmax(0,1fr) auto;gap:10px;page-break-after:always;break-after:page;position:relative;overflow:hidden}
.page:last-child{page-break-after:auto;break-after:auto}
.page .eyebrow{display:flex;align-items:baseline;gap:14px}
.page .num{font-family:var(--display);font-size:1.7rem;color:var(--ax);line-height:1}
.page h2{font-family:var(--display);font-size:1.5rem;margin:0}
.page .claim{font-weight:600;font-size:1.05rem;color:var(--ink);margin:0}
.page .why{margin:0;color:var(--muted);font-size:.95rem;max-width:100%}
.page figure{margin:0;min-height:0;display:grid;grid-template-rows:minmax(0,1fr);justify-items:center}
.page svg{width:100%;height:100%;min-width:0;max-width:100%}
.page figcaption{width:100%;font-size:.85rem;color:var(--muted);border-top:1px solid var(--line);padding-top:8px}
.page .folio{position:absolute;right:56px;bottom:14px;font-size:.75rem;color:var(--muted);letter-spacing:.04em}
.page .brand{position:absolute;left:56px;bottom:14px;font-size:.75rem;color:var(--muted);letter-spacing:.04em}
.legend{position:absolute;right:56px;top:18px;display:flex;gap:16px;font-size:.78rem;color:var(--muted)}
.legend span::before{content:"";display:inline-block;width:20px;height:3px;vertical-align:middle;margin-right:6px;border-radius:2px}
.legend .l-now::before{background:var(--now)} .legend .l-ax::before{background:var(--ax)}
</style>''')
out = ['<!doctype html><html lang="ko"><head><meta charset="utf-8"><title>AX 개념도 A4</title>',
       '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Noto+Serif+KR:wght@600;700&display=swap">',
       style, '</head><body>']
total = len(gen.boards)
for k,(num, title, claim, why, fn, cap) in enumerate(gen.boards, start=1):
    W, H, body = fn()
    out.append(f'''<section class="page" id="p{k}">
<div class="legend"><span class="l-now">지금 · 사람을 거친다</span><span class="l-ax">목표 · 회사의 두뇌를 거친다</span></div>
<div class="eyebrow"><span class="num">{num}</span><h2>{title}</h2></div>
<p class="claim">{claim}</p>
<p class="why">{why}</p>
<figure><svg viewBox="0 0 {W} {H}" role="img" aria-label="{claim}" preserveAspectRatio="xMidYMid meet">{gen.DEFS}
{body}
</svg><figcaption>{cap}</figcaption></figure>
<div class="brand">AX 프로젝트 · 개념도</div><div class="folio">{k} / {total}</div>
</section>''')
out.append('</body></html>')
open('a4.html','w').write("\n".join(out))
print('ok')
