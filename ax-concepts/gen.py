import math

def ring(n, cx, cy, r, start=-90):
    return [(cx + r*math.cos(math.radians(start + 360*i/n)), cy + r*math.sin(math.radians(start + 360*i/n))) for i in range(n)]

def complete_graph(pts, cls):
    out = []
    for i in range(len(pts)):
        for j in range(i+1, len(pts)):
            out.append(f'<line class="{cls}" x1="{pts[i][0]:.1f}" y1="{pts[i][1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}"/>')
    return "\n".join(out)

def person(x, y, r=9, cls="p", label=None, dy=22):
    s = f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{r}"/>'
    if label:
        s += f'<text class="lab" x="{x:.1f}" y="{y+dy:.1f}" text-anchor="middle">{label}</text>'
    return s

# ---------- ④ 지금 vs 목표 ----------
def fig4():
    W, H = 1000, 520
    parts = []
    # left: 대표 허브
    cx, cy, R = 250, 262, 140
    ring10 = ring(10, cx, cy, R)
    names = ["민규","상용","지헌","정우","도형","한일","연구원","연구원","연구원","연구원"]
    for (x,y) in ring10:
        parts.append(f'<line class="e now" x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" marker-end="url(#a-now)" marker-start="url(#a-now-s)"/>')
    for i,(x,y) in enumerate(ring10):
        parts.append(person(x,y,10,"p"))
        # 개인 AI 점: 바깥쪽에 작은 점, 연결 없음
        ax = cx + (R+34)*math.cos(math.atan2(y-cy, x-cx)); ay = cy + (R+34)*math.sin(math.atan2(y-cy, x-cx))
        if i in (1,2,4,6,8):
            parts.append(f'<rect class="ai-solo" x="{ax-13:.1f}" y="{ay-9:.1f}" width="26" height="18" rx="4"/><text class="tiny" x="{ax:.1f}" y="{ay+4:.1f}" text-anchor="middle">AI</text>')
    parts.append(f'<circle class="hub-now" cx="{cx}" cy="{cy}" r="30"/><text class="hub-t" x="{cx}" y="{cy+5}" text-anchor="middle">대표</text>')
    parts.append(f'<text class="h" x="{cx}" y="34" text-anchor="middle">지금 · 로마 군단식</text>')
    parts.append(f'<text class="sub" x="{cx}" y="56" text-anchor="middle">정보가 사람을 거쳐 오르내린다</text>')
    parts.append(f'<text class="note now-t" x="{cx}" y="{H-18}" text-anchor="middle">통로가 막히면 회사가 멈춘다 · 개인 AI는 각자 계정에 흩어진다</text>')

    # right: 회사의 두뇌 허브
    cx2 = 750
    ring10b = ring(10, cx2, cy, R)
    for (x,y) in ring10b:
        parts.append(f'<line class="e ax" x1="{cx2}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" marker-end="url(#a-ax)" marker-start="url(#a-ax-s)"/>')
        # 바깥: 현실과 만나는 선
        ang = math.atan2(y-cy, x-cx2)
        ox, oy = x + 30*math.cos(ang), y + 30*math.sin(ang)
        parts.append(f'<line class="e out" x1="{x:.1f}" y1="{y:.1f}" x2="{ox:.1f}" y2="{oy:.1f}"/>')
    for (x,y) in ring10b:
        parts.append(person(x,y,10,"p"))
    parts.append(f'<rect class="hub-ax" x="{cx2-62}" y="{cy-40}" width="124" height="80" rx="12"/>')
    parts.append(f'<text class="hub-t ax-t" x="{cx2}" y="{cy-10}" text-anchor="middle">회사의 두뇌</text>')
    parts.append(f'<text class="tiny ax-t" x="{cx2}" y="{cy+10}" text-anchor="middle">메일 · 슬랙 · 녹취</text>')
    parts.append(f'<text class="tiny ax-t" x="{cx2}" y="{cy+26}" text-anchor="middle">데이터 · 노하우</text>')
    parts.append(f'<text class="h" x="{cx2}" y="34" text-anchor="middle">목표 · 회사의 두뇌</text>')
    parts.append(f'<text class="sub" x="{cx2}" y="56" text-anchor="middle">기록은 한곳에, 사람은 가장자리에서 현실을 만난다</text>')
    # 현실 라벨 (바깥 고리)
    for lbl, ang in (("영업 대화",-150),("중대 결정",-30),("윤리 판단",90)):
        lx = cx2 + (R+70)*math.cos(math.radians(ang)); ly = cy + (R+70)*math.sin(math.radians(ang))
        parts.append(f'<text class="real" x="{lx:.1f}" y="{ly+4:.1f}" text-anchor="middle">{lbl}</text>')
    parts.append(f'<text class="note ax-t" x="{cx2}" y="{H-18}" text-anchor="middle">누구나 두뇌에 직접 묻고, 쓴 것은 두뇌에 쌓인다</text>')
    parts.append(f'<line class="divider" x1="500" y1="20" x2="500" y2="{H-20}"/>')
    return W, H, "\n".join(parts)

# ---------- ⑤ 업무 연결 ----------
def fig5():
    W, H = 1000, 490
    p = []
    stages = [("사업","수주 조건·단가"),("기술","사양·BoM"),("생산","재고·조립 일정"),("경영지원","구매·입고")]
    xs = [250, 410, 570, 730]
    bw, bh = 120, 56
    # 질문/답
    def q_and_a(y, cls):
        p.append(f'<rect class="cust" x="40" y="{y-bh/2}" width="130" height="{bh}" rx="8"/>')
        p.append(f'<text class="b" x="105" y="{y-4}" text-anchor="middle">고객</text><text class="tiny" x="105" y="{y+14}" text-anchor="middle">“납기가 언제죠?”</text>')
        p.append(f'<line class="e {cls}" x1="170" y1="{y}" x2="{xs[0]-bw/2-4}" y2="{y}" marker-end="url(#a-{cls})"/>')
        for i,(n,d) in enumerate(stages):
            x = xs[i]
            p.append(f'<rect class="dept" x="{x-bw/2}" y="{y-bh/2}" width="{bw}" height="{bh}" rx="8"/>')
            p.append(f'<text class="b" x="{x}" y="{y-4}" text-anchor="middle">{n}</text><text class="tiny" x="{x}" y="{y+14}" text-anchor="middle">{d}</text>')
            if i < 3:
                p.append(f'<line class="e {cls}" x1="{x+bw/2}" y1="{y}" x2="{xs[i+1]-bw/2-4}" y2="{y}" marker-end="url(#a-{cls})"/>')
        p.append(f'<line class="e {cls}" x1="{xs[3]+bw/2}" y1="{y}" x2="826" y2="{y}" marker-end="url(#a-{cls})"/>')
        p.append(f'<rect class="ans {cls}-box" x="830" y="{y-bh/2}" width="130" height="{bh}" rx="8"/>')
        p.append(f'<text class="b" x="895" y="{y-4}" text-anchor="middle">답변</text>')
    # 지금
    y1 = 95
    p.append(f'<text class="h now-t" x="40" y="36">지금 · 단계마다 사람에게 묻고 기다린다</text>')
    q_and_a(y1, "now")
    p.append(f'<text class="tiny" x="895" y="{y1+14}" text-anchor="middle">며칠 뒤, 근거 없이</text>')
    for i in range(4):
        x = xs[i]
        p.append(f'<path class="e now dash" d="M{x},{y1+bh/2+2} v22" marker-end="url(#a-now)"/>')
        p.append(f'<text class="tiny now-t" x="{x}" y="{y1+bh/2+42}" text-anchor="middle">담당자에게 묻고</text>')
        p.append(f'<text class="tiny now-t" x="{x}" y="{y1+bh/2+57}" text-anchor="middle">기다린다</text>')
    p.append(f'<text class="note now-t" x="500" y="{y1+118}" text-anchor="middle">4번 묻고 4번 기다린다 · 묻는 상대가 자리에 없으면 흐름이 선다 · 답에 근거가 남지 않는다</text>')
    p.append(f'<line class="divider" x1="40" y1="238" x2="960" y2="238"/>')
    # 목표
    y2 = 316
    p.append(f'<text class="h ax-t" x="40" y="268">목표 · 같은 흐름, 답은 공동 DB에서 바로 읽는다</text>')
    q_and_a(y2, "ax")
    p.append(f'<text class="tiny" x="895" y="{y2+14}" text-anchor="middle">당일, 근거 링크 첨부</text>')
    dbx, dby, dbw, dbh = 190, 400, 620, 54
    p.append(f'<rect class="db" x="{dbx}" y="{dby}" width="{dbw}" height="{dbh}" rx="10"/>')
    p.append(f'<text class="b ax-t" x="{dbx+dbw/2}" y="{dby+22}" text-anchor="middle">통합 DB</text>')
    p.append(f'<text class="tiny ax-t" x="{dbx+dbw/2}" y="{dby+40}" text-anchor="middle">견적 이력 · BoM · 재고 · 입고 예정 · 작업일지 · 회의 녹취</text>')
    for i in range(4):
        x = xs[i]
        p.append(f'<line class="e ax" x1="{x}" y1="{y2+bh/2+2}" x2="{x}" y2="{dby-4}" marker-end="url(#a-ax)" marker-start="url(#a-ax-s)"/>')
        p.append(f'<text class="tiny ax-t" x="{x+6}" y="{(y2+bh/2+dby)/2+4}">읽고 · 쓴다</text>')
    p.append(f'<text class="note ax-t" x="500" y="{H-10}" text-anchor="middle">사람은 판단만 한다 · 한 사람이 자리를 비워도 흐름이 선다 · 답과 근거가 같이 남아 다음 질문의 재료가 된다</text>')
    return W, H, "\n".join(p)

# ---------- ⑥ 개선 루프 ----------
def fig6():
    W, H = 1000, 500
    p = []
    cx, cy, R = 400, 255, 165
    steps = [("기록","작업일지 · 조립 체크 · 회의 녹취"),("분석","AI가 이상을 찾는다"),("실행","판단 · 지시 · 작업"),("오류 확인","결과가 예상과 다른가?"),("지식 보완","원인과 규칙을 DB에 추가")]
    pts = ring(5, cx, cy, R)
    n = len(pts)
    for i in range(n):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%n]
        # arc along the circle, shortened near nodes
        a1 = math.atan2(y1-cy, x1-cx); a2 = math.atan2(y2-cy, x2-cx)
        if a2 < a1: a2 += 2*math.pi
        s = a1 + 0.26; e = a2 - 0.26
        sx, sy = cx + R*math.cos(s), cy + R*math.sin(s)
        ex, ey = cx + R*math.cos(e), cy + R*math.sin(e)
        p.append(f'<path class="e ax thick" d="M{sx:.1f},{sy:.1f} A{R},{R} 0 0 1 {ex:.1f},{ey:.1f}" marker-end="url(#a-ax)"/>')
    for i,(x,y) in enumerate(pts):
        name, desc = steps[i]
        p.append(f'<circle class="step" cx="{x:.1f}" cy="{y:.1f}" r="36"/>')
        p.append(f'<text class="b" x="{x:.1f}" y="{y+5:.1f}" text-anchor="middle">{name}</text>')
        # desc outside
        ang = math.atan2(y-cy, x-cx)
        dx, dy = x + 58*math.cos(ang), y + 58*math.sin(ang)
        anchor = "middle" if abs(math.cos(ang)) < 0.3 else ("start" if math.cos(ang) > 0 else "end")
        p.append(f'<text class="lab" x="{dx:.1f}" y="{dy+4:.1f}" text-anchor="{anchor}">{desc}</text>')
    p.append(f'<text class="hub-t ax-t" x="{cx}" y="{cy-6}" text-anchor="middle">한 바퀴마다</text><text class="hub-t ax-t" x="{cx}" y="{cy+16}" text-anchor="middle">두뇌가 똑똑해진다</text>')
    # 사례 박스
    bx, by, bw, bh = 768, 128, 212, 250
    p.append(f'<rect class="case" x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10"/>')
    p.append(f'<text class="b now-t" x="{bx+16}" y="{by+28}">사례 · 588시간</text>')
    lines = ["캐소드 미장착 셀 하나로","장기구동이 중단됐다.","","조립 확인이 기록으로","남지 않아 해체한 뒤에야","발견했다.","","루프가 돌았다면 ‘기록’","단계에서 ‘분석’이 먼저","잡았을 일이다."]
    for k,l in enumerate(lines):
        p.append(f'<text class="lab" x="{bx+16}" y="{by+54+k*19}">{l}</text>')
    # pointer from case to 기록 node
    p.append(f'<path class="e now dash" d="M{bx},{by+40} Q{pts[0][0]+120},{pts[0][1]-20} {pts[0][0]+40:.1f},{pts[0][1]-8:.1f}" marker-end="url(#a-now)"/>')
    return W, H, "\n".join(p)

# ---------- ⑦ 소통 비용 ----------
def fig7():
    W, H = 1000, 560
    p = []
    cy = 215
    # panel 1: 10명 45쌍
    c1, R1 = 165, 115
    pts = ring(10, c1, cy, R1)
    p.append(complete_graph(pts, "e now thin"))
    for (x,y) in pts: p.append(person(x,y,9,"p"))
    p.append(f'<text class="h" x="{c1}" y="40" text-anchor="middle">10명</text>')
    p.append(f'<text class="big now-t" x="{c1}" y="{cy+125+52}" text-anchor="middle">45쌍</text>')
    # panel 2: 20명 190쌍
    c2, R2 = 500, 125
    pts2 = ring(20, c2, cy, R2)
    p.append(complete_graph(pts2, "e now hair"))
    for (x,y) in pts2: p.append(person(x,y,7,"p"))
    p.append(f'<text class="h" x="{c2}" y="40" text-anchor="middle">20명</text>')
    p.append(f'<text class="big now-t" x="{c2}" y="{cy+R2+52}" text-anchor="middle">190쌍</text>')
    p.append(f'<text class="e-arrow now-t" x="332" y="{cy+6}" text-anchor="middle">사람 2배 →</text>')
    p.append(f'<text class="e-arrow now-t" x="332" y="{cy+26}" text-anchor="middle">쌍 4배</text>')
    # panel 3: 허브
    c3, R3 = 835, 115
    pts3 = ring(10, c3, cy, R3)
    for (x,y) in pts3:
        p.append(f'<line class="e ax" x1="{c3}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}"/>')
    for (x,y) in pts3: p.append(person(x,y,9,"p"))
    p.append(f'<rect class="hub-ax" x="{c3-44}" y="{cy-24}" width="88" height="48" rx="10"/>')
    p.append(f'<text class="b ax-t" x="{c3}" y="{cy+5}" text-anchor="middle">공동 DB</text>')
    p.append(f'<text class="h" x="{c3}" y="40" text-anchor="middle">10명 + 두뇌</text>')
    p.append(f'<text class="big ax-t" x="{c3}" y="{cy+125+52}" text-anchor="middle">10선</text>')
    p.append(f'<text class="e-arrow ax-t" x="668" y="{cy+6}" text-anchor="middle">20명이면</text>')
    p.append(f'<text class="e-arrow ax-t" x="668" y="{cy+26}" text-anchor="middle">20선</text>')
    p.append(f'<line class="divider" x1="40" y1="412" x2="960" y2="412"/>')
    # 하단: 한 번의 질문이 지나는 길
    y = 474
    p.append(f'<text class="h now-t" x="40" y="446">지금 · 질문 하나가 지나는 길</text>')
    chain = ["질문","검색","전달","재확인","또 질문"]
    x = 40
    for i,c in enumerate(chain):
        p.append(f'<rect class="chip now-box" x="{x}" y="{y-14}" width="70" height="28" rx="14"/><text class="tiny" x="{x+35}" y="{y+5}" text-anchor="middle">{c}</text>')
        if i < len(chain)-1:
            p.append(f'<line class="e now" x1="{x+72}" y1="{y}" x2="{x+96}" y2="{y}" marker-end="url(#a-now)"/>')
        x += 100
    p.append(f'<path class="e now dash" d="M{x-30},{y+16} v16 H75 v-14" marker-end="url(#a-now)"/>')
    p.append(f'<text class="tiny now-t" x="290" y="{y+48}" text-anchor="middle">사람이 바뀔 때마다 처음부터 반복</text>')
    p.append(f'<text class="h ax-t" x="660" y="446">목표</text>')
    x = 660
    for i,c in enumerate(["질문","답 + 근거"]):
        w = 70 if i == 0 else 100
        p.append(f'<rect class="chip ax-box" x="{x}" y="{y-14}" width="{w}" height="28" rx="14"/><text class="tiny" x="{x+w/2}" y="{y+5}" text-anchor="middle">{c}</text>')
        if i == 0:
            p.append(f'<line class="e ax" x1="{x+72}" y1="{y}" x2="{x+96}" y2="{y}" marker-end="url(#a-ax)"/>')
        x += 100
    p.append(f'<text class="tiny ax-t" x="750" y="{y+48}" text-anchor="middle">한 번에, 누가 물어도 같은 답과 근거</text>')
    return W, H, "\n".join(p)

# ---------- ⑧ DB 기반 판단 ----------
def fig8():
    W, H = 1000, 436
    p = []
    # sources
    srcs = ["메일","슬랙","회의 녹취","ERP · 재고","작업일지","견적 · BoM"]
    sx = 60
    for i,s in enumerate(srcs):
        y = 70 + i*52
        p.append(f'<rect class="src" x="{sx}" y="{y-16}" width="110" height="32" rx="6"/><text class="tiny" x="{sx+55}" y="{y+5}" text-anchor="middle">{s}</text>')
        p.append(f'<path class="e ax" d="M{sx+112},{y} C{sx+170},{y} {sx+170},200 {sx+212},200" marker-end="url(#a-ax)"/>')
    p.append(f'<text class="h" x="{sx+55}" y="36" text-anchor="middle">① 수집</text>')
    p.append(f'<text class="tiny" x="{sx+55}" y="{70+6*52-10}" text-anchor="middle">사람이 옮기지 않는다 · 자동</text>')
    # DB cylinder
    dx, dy = 280, 200
    p.append(f'<ellipse class="db-top" cx="{dx+70}" cy="{dy-50}" rx="70" ry="16"/>')
    p.append(f'<path class="db-body" d="M{dx},{dy-50} v100 a70,16 0 0 0 140,0 v-100"/>')
    p.append(f'<ellipse class="db-top" cx="{dx+70}" cy="{dy-50}" rx="70" ry="16"/>')
    p.append(f'<text class="b ax-t" x="{dx+70}" y="{dy+2}" text-anchor="middle">통합 DB</text>')
    p.append(f'<text class="tiny ax-t" x="{dx+70}" y="{dy+20}" text-anchor="middle">한곳 · 검색 가능</text>')
    p.append(f'<text class="h" x="{dx+70}" y="36" text-anchor="middle">② 한곳에 모은다</text>')
    # 주기적 갱신 loop above DB
    lx, ly = dx+40, 98
    p.append(f'<path class="e ax dash" d="M{lx+24},{ly+8} a26,26 0 1 1 -2,-16" marker-end="url(#a-ax)"/>')
    p.append(f'<text class="tiny ax-t" x="{lx+42}" y="{ly-2}" font-weight="600">③ 주기적 갱신</text>')
    p.append(f'<text class="tiny" x="{lx+42}" y="{ly+14}">매일 수집 · 매주 요약</text>')
    # 판단 three branches
    jx = 560
    p.append(f'<text class="h" x="{jx+70}" y="36" text-anchor="middle">④ 판단</text>')
    branches = [("경영","채용 · 자금 · 우선순위", 110),("사업","견적 · 납기 · 고객 응대", 200),("기술","사양 · 레시피 · 설비", 290)]
    for name, desc, y in branches:
        p.append(f'<path class="e ax" d="M{dx+142},{dy} C{dx+200},{dy} {jx-60},{y} {jx-4},{y}" marker-end="url(#a-ax)"/>')
        p.append(f'<rect class="judge" x="{jx}" y="{y-24}" width="140" height="48" rx="8"/>')
        p.append(f'<text class="b" x="{jx+70}" y="{y-3}" text-anchor="middle">{name} 판단</text><text class="tiny" x="{jx+70}" y="{y+15}" text-anchor="middle">{desc}</text>')
    p.append(f'<text class="tiny ax-t" x="{(dx+142+jx)/2+4}" y="{dy+18}" text-anchor="middle">같은 근거로</text>')
    # 실행
    ex = 800
    p.append(f'<text class="h" x="{ex+60}" y="36" text-anchor="middle">⑤ 실행</text>')
    for name, desc, y in branches:
        p.append(f'<line class="e ax" x1="{jx+142}" y1="{y}" x2="{ex-4}" y2="{y}" marker-end="url(#a-ax)"/>')
    p.append(f'<rect class="act" x="{ex}" y="86" width="120" height="228" rx="8"/>')
    for k,l in enumerate(["사람이 결정하고","실행한다","","결과 · 이유를","기록한다"]):
        p.append(f'<text class="lab" x="{ex+60}" y="{160+k*20}" text-anchor="middle">{l}</text>')
    # return arrow to DB
    p.append(f'<path class="e ax thick" d="M{ex+60},316 V380 H{dx+70} V{dy+72}" marker-end="url(#a-ax)"/>')
    p.append(f'<text class="b ax-t" x="{(ex+60+dx+70)/2}" y="372" text-anchor="middle">⑥ 결과를 DB에 되돌린다 → 다음 판단의 근거</text>')
    p.append(f'<text class="note" x="500" y="{H-12}" text-anchor="middle">모으는 것은 시작일 뿐이다. 최신으로 유지하고, 판단에 쓰고, 결과를 다시 넣어야 두뇌가 된다.</text>')
    return W, H, "\n".join(p)

DEFS = '''<defs>
<marker id="a-ax" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--ax)"/></marker>
<marker id="a-ax-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="var(--ax)"/></marker>
<marker id="a-now" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="var(--now)"/></marker>
<marker id="a-now-s" viewBox="0 0 10 10" refX="1" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M10,0 L0,5 L10,10 z" fill="var(--now)"/></marker>
</defs>'''

boards = [
    ("④","왜 AX인가","중심에 누가 있느냐가 바뀐다",
     "같은 10명이다. 지금은 대표가 정보의 통로라서 대표가 막히면 회사가 선다. 목표는 기록이 모인 ‘회사의 두뇌’를 중심에 두고, 사람은 가장자리에서 영업·결정·윤리 같은 현실을 맡는 구조다.",
     fig4, "같은 열 명을 두 번 그렸다. 왼쪽은 대표를 중심으로 모든 선이 오가고 개인 AI는 바깥에 따로 떠 있다. 오른쪽은 회사의 두뇌가 중심이고 사람은 바깥의 현실을 향한다."),
    ("⑤","업무가 어떻게 연결되나","질문 하나가 네 부서를 지난다",
     "고객의 ‘납기가 언제죠?’ 한 마디는 사업·기술·생산·경영지원을 차례로 지난다. 지금은 단계마다 담당자에게 묻고 기다린다. 목표는 같은 흐름에서 각 단계가 통합 DB를 읽고 쓰는 것이다.",
     fig5, "위는 지금, 아래는 목표. 흐름은 같고 각 단계가 어디서 답을 얻는지만 다르다."),
    ("⑥","어떻게 계속 개선되나","루프가 한 바퀴 돌 때마다 두뇌가 똑똑해진다",
     "기록 → 분석 → 실행 → 오류 확인 → 지식 보완이 한 바퀴다. 오류가 나면 원인과 규칙이 DB로 돌아가므로 같은 실수가 두 번 나지 않는다. 588시간을 잃은 캐소드 사례는 이 루프의 첫 칸이 비어 있어서 생겼다.",
     fig6, "다섯 단계가 순환한다. 오른쪽 사례는 ‘기록’ 단계가 비어 있을 때 무엇을 잃는지 보여준다."),
    ("⑦","소통 비용은 제곱으로 는다","사람을 뽑으면 쌍이 늘고, 두뇌를 두면 선만 는다",
     "서로 물어서 일하는 조직은 쌍의 수만큼 비용이 든다. 10명이면 45쌍, 20명이면 190쌍이다. 공동 DB를 중심에 두면 선은 사람 수만큼만 늘어 10명이면 10선, 20명이면 20선이다.",
     fig7, "왼쪽 둘은 사람끼리 직접 묻는 조직, 오른쪽은 두뇌를 거치는 조직. 아래는 질문 하나가 지나는 길의 차이다."),
    ("⑧","DB 기반 판단","모으고, 갱신하고, 판단에 쓰고, 결과를 되돌린다",
     "메일·슬랙·녹취·ERP·작업일지가 자동으로 한곳에 모이고 주기적으로 갱신된다. 경영·사업·기술 판단이 같은 근거에서 나오고, 실행 결과와 이유가 다시 DB로 돌아가 다음 판단의 근거가 된다.",
     fig8, "왼쪽에서 오른쪽으로 흐르고, 아래 굵은 선으로 다시 DB에 돌아온다. 되돌아오는 선이 없으면 DB는 창고일 뿐이다."),
]

html = ['''<title>AX 개념도</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;600;700&family=Noto+Serif+KR:wght@600;700&display=swap">
<style>
/* 레이아웃: 세로로 이어지는 다섯 장의 보드. 한 장에 하나의 개념, 그림이 주인공, 글은 위아래 띠. */
:root{
  --bg:#f7f8fa; --paper:#ffffff; --fg:#1b2230; --muted:#5b6474; --line:#d6dbe3;
  --ax:#1d5fb5; --ax-soft:#e4edf9;
  --now:#b5541d; --now-soft:#f8ebe2;
  --ink:#2b3442;
  --display:"Noto Serif KR","Apple SD Gothic Neo",serif;
  --body:"IBM Plex Sans KR","Apple SD Gothic Neo","Malgun Gothic",sans-serif;
}
@media (prefers-color-scheme: dark){ :root:not([data-theme="light"]){
  --bg:#0f141c; --paper:#161d28; --fg:#e8ecf3; --muted:#9aa5b7; --line:#2b3545;
  --ax:#7eb0ff; --ax-soft:#1b2a44; --now:#f09a5e; --now-soft:#3a2518; --ink:#dce3ee; color-scheme:dark } }
:root[data-theme="dark"]{
  --bg:#0f141c; --paper:#161d28; --fg:#e8ecf3; --muted:#9aa5b7; --line:#2b3545;
  --ax:#7eb0ff; --ax-soft:#1b2a44; --now:#f09a5e; --now-soft:#3a2518; --ink:#dce3ee; color-scheme:dark }
body{background:var(--bg);color:var(--fg);font-family:var(--body);padding-block:32px;padding-inline:16px;line-height:1.55}
.wrap{max-width:1040px;margin:0 auto;display:grid;gap:40px}
header{display:grid;gap:6px}
header h1{font-family:var(--display);font-size:1.7rem;margin:0;text-wrap:balance}
header p{margin:0;color:var(--muted);max-width:65ch}
.legend{display:flex;gap:18px;flex-wrap:wrap;font-size:.85rem;color:var(--muted)}
.legend span::before{content:"";display:inline-block;width:22px;height:3px;vertical-align:middle;margin-right:6px;border-radius:2px}
.legend .l-now::before{background:var(--now)} .legend .l-ax::before{background:var(--ax)}
.board{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:24px 24px 20px;display:grid;gap:14px}
.board .eyebrow{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}
.board .num{font-family:var(--display);font-size:1.5rem;color:var(--ax);line-height:1}
.board h2{font-family:var(--display);font-size:1.35rem;margin:0;text-wrap:balance}
.board .claim{font-weight:600;color:var(--ink);margin:0}
.board .why{margin:0;color:var(--muted);max-width:72ch;font-size:.95rem}
figure{margin:0;display:grid;gap:10px}
.scroll{overflow-x:auto}
svg{display:block;width:100%;height:auto;max-width:100%;min-width:640px;font-family:var(--body);color:var(--fg)}
figcaption{font-size:.85rem;color:var(--muted);border-top:1px solid var(--line);padding-top:10px}
/* svg 공통 */
svg text{fill:currentColor}
.h{font-size:16px;font-weight:700}
.sub{font-size:12px;fill:var(--muted)}
.b{font-size:14px;font-weight:600}
.lab{font-size:12.5px;fill:var(--muted)}
.tiny{font-size:11.5px}
.note{font-size:12.5px;font-weight:500}
.big{font-size:30px;font-weight:700;font-family:var(--display)}
.real{font-size:12.5px;font-weight:600;fill:var(--muted)}
.e-arrow{font-size:12.5px;font-weight:600}
.hub-t{font-size:15px;font-weight:700}
.ax-t{fill:var(--ax)} .now-t{fill:var(--now)}
.e{fill:none;stroke:currentColor;stroke-width:1.6;stroke-linecap:round}
.e.ax{stroke:var(--ax)} .e.now{stroke:var(--now)}
.e.thin{stroke-width:.9;opacity:.6} .e.hair{stroke-width:.45;opacity:.5}
.e.thick{stroke-width:2.6}
.e.dash{stroke-dasharray:5 4}
.e.out{stroke:var(--muted);stroke-width:1.2;stroke-dasharray:2 3}
.p{fill:var(--paper);stroke:var(--fg);stroke-width:1.6}
.hub-now{fill:var(--now-soft);stroke:var(--now);stroke-width:2}
.hub-ax{fill:var(--ax-soft);stroke:var(--ax);stroke-width:2}
.ai-solo{fill:var(--paper);stroke:var(--muted);stroke-width:1;stroke-dasharray:3 2}
.divider{stroke:var(--line);stroke-width:1}
.cust{fill:var(--paper);stroke:var(--fg);stroke-width:1.4}
.dept{fill:var(--paper);stroke:var(--fg);stroke-width:1.4}
.ans{fill:var(--paper);stroke-width:1.6}
.now-box{stroke:var(--now);fill:var(--now-soft)} .ax-box{stroke:var(--ax);fill:var(--ax-soft)}
.db{fill:var(--ax-soft);stroke:var(--ax);stroke-width:2}
.step{fill:var(--ax-soft);stroke:var(--ax);stroke-width:2}
.case{fill:var(--now-soft);stroke:var(--now);stroke-width:1.4}
.chip{stroke-width:1.4}
.src{fill:var(--paper);stroke:var(--fg);stroke-width:1.2}
.db-top{fill:var(--ax-soft);stroke:var(--ax);stroke-width:2}
.db-body{fill:var(--ax-soft);stroke:var(--ax);stroke-width:2}
.judge{fill:var(--paper);stroke:var(--fg);stroke-width:1.4}
.act{fill:var(--paper);stroke:var(--fg);stroke-width:1.4;stroke-dasharray:6 3}
@media (max-width:640px){ .board{padding:16px} header h1{font-size:1.4rem} }
</style>
<div class="wrap">
<header>
<h1>AX 개념도 ④~⑧</h1>
<p>글로 쓴 ①~③을 그림으로 옮긴 다섯 장. 한 장에 개념 하나만 담았다.</p>
<div class="legend"><span class="l-now">지금 · 사람을 거친다</span><span class="l-ax">목표 · 회사의 두뇌를 거친다</span></div>
</header>
''']
for num, title, claim, why, fn, cap in boards:
    W, H, body = fn()
    html.append(f'''<section class="board" id="b{num}">
<div class="eyebrow"><span class="num">{num}</span><h2>{title}</h2></div>
<p class="claim">{claim}</p>
<p class="why">{why}</p>
<figure><div class="scroll"><svg viewBox="0 0 {W} {H}" role="img" aria-label="{claim}">{DEFS}
{body}
</svg></div><figcaption>{cap}</figcaption></figure>
</section>
''')
html.append('</div>')
open('ax-concepts.html','w').write("\n".join(html))
print("ok")
