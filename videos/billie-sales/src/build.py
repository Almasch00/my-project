"""Generate the Billie sales video compositions (index.html + compositions/*.html).

Style follows the Lisa (v.1.1) reference: pale blue-grey stage, royal-blue / navy /
orange-red accents, Poppins headlines, Roboto pills, YouTube-style grey caption boxes.

Run from the project root:  python3 src/build.py
Scene timings are written in GLOBAL voiceover seconds; each scene converts with T().
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1920, 1080
TOTAL = 69.0

FONTS = """
@font-face{font-family:'Poppins';font-weight:400;src:url('assets/fonts/poppins-latin-400-normal.woff2') format('woff2');}
@font-face{font-family:'Poppins';font-weight:500;src:url('assets/fonts/poppins-latin-500-normal.woff2') format('woff2');}
@font-face{font-family:'Poppins';font-weight:600;src:url('assets/fonts/poppins-latin-600-normal.woff2') format('woff2');}
@font-face{font-family:'Poppins';font-weight:700;src:url('assets/fonts/poppins-latin-700-normal.woff2') format('woff2');}
@font-face{font-family:'Poppins';font-weight:800;src:url('assets/fonts/poppins-latin-800-normal.woff2') format('woff2');}
@font-face{font-family:'Roboto';font-weight:500;src:url('assets/fonts/roboto-latin-500-normal.woff2') format('woff2');}
@font-face{font-family:'Roboto';font-weight:700;src:url('assets/fonts/roboto-latin-700-normal.woff2') format('woff2');}
"""

# palette (Lisa reference + Billie red)
BASE = """
#__RID__{position:absolute;inset:0;overflow:hidden;background:#DDE7F1;font-family:'Poppins',sans-serif;color:#141B3C;}
#__RID__ *{box-sizing:border-box;}
#__RID__ .abs{position:absolute;}
#__RID__ .fill{position:absolute;inset:0;}
#__RID__ .center{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;}
#__RID__ img.ic{display:block;}
#__RID__ .cursor{position:absolute;left:0;top:0;width:54px;height:54px;}
#__RID__ .ripple{position:absolute;width:90px;height:90px;border-radius:50%;border:4px solid #2563EB;opacity:0;}
"""

CURSOR = (
    '<svg viewBox="0 0 32 32" width="54" height="54"><path d="M6 3 L6 25 L11.5 20 L15.5 29 L19.5 27.3 '
    'L15.6 18.6 L23 18.6 Z" fill="#fff" stroke="#111" stroke-width="1.8" stroke-linejoin="round"/></svg>'
)


def icon(code, size, extra=""):
    return (f'<i class="ic" style="display:block;flex:none;width:{size}px;height:{size}px;'
            f'background:url(assets/icons/{code}.svg) center/contain no-repeat;{extra}"></i>')


def odoo(height):
    # original Odoo logo (assets/odoo.png, 747x238 with transparency)
    return f'<img class="odoo" src="assets/odoo.png" alt="Odoo" style="height:{height}px;width:{height * 747 / 238:.0f}px;display:block">'


SCENES = []
CHECK = ('<svg viewBox="0 0 24 24"><path d="M4 12.5l5 5L20 7" stroke="#2E6BF0" stroke-width="3.4" fill="none" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')


def exchip(e):
    return f'<div class="ex">{icon("26a0", 30)}{e[0]}</div>' if e else ""


def scene(sid, start, end, css, html, js):
    SCENES.append(dict(id=sid, start=start, end=end, css=css, html=html, js=js))


# ------------------------------------------------------------------ S1 hook
words1 = [("When", .06), ("did", .30), ("someone", .48), ("last", .90), ("touch", 1.24), ("your", 1.50),
          ("reorder", 1.68), ("rules?", 2.19)]
scene("s01-hook", 0.0, 3.05, """
#__RID__ .bgw{position:absolute;inset:0;overflow:hidden;}
#__RID__ .bgw video{position:absolute;left:0;top:0;width:1920px;height:1080px;object-fit:cover;}
#__RID__ .veil{position:absolute;inset:0;background:linear-gradient(180deg,rgba(221,231,241,.92) 0%,rgba(221,231,241,.55) 38%,rgba(221,231,241,.25) 70%,rgba(221,231,241,.45) 100%);}
#__RID__ .stack{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:56px;padding-bottom:170px;}
#__RID__ .head{font-weight:700;font-size:64px;letter-spacing:-.5px;display:flex;gap:18px;}
#__RID__ .head .w{display:inline-block;}
#__RID__ .head .hl{color:#2563EB;}
#__RID__ .card{width:1120px;background:#fff;border-radius:32px;box-shadow:0 30px 60px rgba(20,27,60,.14);padding:40px 54px;}
#__RID__ .row1{display:flex;align-items:center;gap:18px;font-weight:600;font-size:42px;}
#__RID__ .row1 .ref{margin-left:auto;font-weight:500;font-size:24px;color:#8A94A6;}
#__RID__ .prod{margin-top:6px;font-weight:500;font-size:30px;color:#6B7487;}
#__RID__ .grid{margin-top:26px;display:grid;grid-template-columns:1fr 1fr 1.4fr;gap:20px;}
#__RID__ .cell{background:#F3F6FA;border-radius:18px;padding:16px 22px;}
#__RID__ .lbl{font-size:24px;font-weight:500;color:#8A94A6;}
#__RID__ .val{font-size:58px;font-weight:700;}
#__RID__ .stale{display:inline-block;color:#E5322D;}
""", f"""
<div class="bgw"><video id="s01-bg" class="clip" src="assets/footage/warehouse-floor.mp4" muted playsinline data-start="0" data-duration="3.05" data-track-index="0"></video></div>
<div class="veil"></div>
<div class="stack">
  <div class="head">{''.join(f'<span class="w{" hl" if w in ("reorder", "rules?") else ""}">{w}</span>' for w, _ in words1)}</div>
  <div class="card">
    <div class="row1">{icon('2699', 44)}<span>Reorder Rule</span><span class="ref">WH/OP/00417</span></div>
    <div class="prod">Office Chair Pro · Warehouse A</div>
    <div class="grid">
      <div class="cell"><div class="lbl">Min Qty</div><div class="val">40</div></div>
      <div class="cell"><div class="lbl">Max Qty</div><div class="val">120</div></div>
      <div class="cell"><div class="lbl">Last modified</div><div class="val"><span class="stale">2 years ago</span></div></div>
    </div>
  </div>
</div>
<div class="cursor">{CURSOR}</div><div class="ripple"></div>
""", """
tl.fromTo(P+' .bgw',{scale:1.12},{scale:1.0,duration:3.05,ease:'none'},0);
tl.fromTo(P+' .card',{y:70,opacity:0,filter:'blur(14px)'},{y:0,opacity:1,filter:'blur(0px)',duration:.7,ease:'power3.out'},T(0.05));
""" + "".join(f"tl.fromTo(P+' .head .w:nth-child({i+1})',{{y:34,opacity:0}},{{y:0,opacity:1,duration:.32,ease:'back.out(2.2)'}},T({t:.2f}));\n" for i, (w, t) in enumerate(words1)) + """
tl.fromTo(P+' .cursor',{x:1500,y:900},{x:1400,y:700,duration:1.0,ease:'power2.inOut'},T(1.0));
tl.fromTo(P+' .ripple',{x:1360,y:660,scale:.3,opacity:.9},{scale:1.4,opacity:0,duration:.5,ease:'power2.out'},T(2.2));
tl.to(P+' .stale',{scale:1.18,duration:.18,yoyo:true,repeat:1,ease:'power2.out'},T(2.2));
tl.to(P+' .stack',{opacity:0,y:-30,filter:'blur(10px)',duration:.28,ease:'power2.in'},T(2.78));
tl.to(P+' .cursor',{opacity:0,duration:.2},T(2.8));
""")

# ------------------------------------------------------------------ S2 timeline
items2 = [("Lead Times", 3.15, "23f1", "Lead time: 14 → 26 days"),
          ("Demand", 4.68, "1f4c8", "Demand up 45%"),
          ("Prices", 6.00, "1f3f7", "Prices up 8%")]
scene("s02-changed", 3.05, 7.40, """
#__RID__ .list{position:absolute;left:250px;top:200px;}
#__RID__ .it{position:relative;height:200px;display:flex;align-items:flex-start;gap:44px;}
#__RID__ .dot{position:relative;width:84px;height:84px;border-radius:50%;border:10px solid #C9D0D9;background:#DDE7F1;flex:none;}
#__RID__ .dot i{position:absolute;left:12px;top:12px;width:40px;height:40px;border-radius:50%;background:#2B7BE0;display:block;}
#__RID__ .lab{font-weight:700;font-size:66px;line-height:84px;color:#747D8B;}
#__RID__ .seg{position:absolute;left:37px;top:84px;width:10px;height:116px;background:#C9D0D9;}
#__RID__ .seg b{display:block;width:100%;height:100%;background:#2B7BE0;transform-origin:50% 0;}
#__RID__ .stage{position:absolute;left:1180px;top:170px;width:480px;height:600px;}
#__RID__ .ico{position:absolute;left:60px;top:0;width:360px;height:360px;}
#__RID__ .chip{position:absolute;left:0;right:0;top:420px;text-align:center;}
#__RID__ .chip span{display:inline-block;background:#fff;border-radius:40px;padding:14px 30px;font-weight:600;font-size:32px;color:#141B3C;box-shadow:0 14px 30px rgba(20,27,60,.12);}
""", f"""
<div class="list">
{''.join(f'<div class="it it{i}"><div class="dot"><i></i></div><div class="lab">{l}</div>{"<div class=seg><b></b></div>" if i < 2 else ""}</div>' for i, (l, t, c, ch) in enumerate(items2))}
</div>
<div class="stage">
{''.join(f'<div class="ico ico{i}">{icon(c, 360)}</div>' for i, (l, t, c, ch) in enumerate(items2))}
{''.join(f'<div class="chip chip{i}"><span>{ch}</span></div>' for i, (l, t, c, ch) in enumerate(items2))}
</div>
""", "tl.fromTo(P+' .it',{x:-60,opacity:0},{x:0,opacity:1,duration:.45,stagger:.08,ease:'power3.out'},0);\n"
   "tl.set(P+' .dot i',{scale:0},0);tl.set(P+' .seg b',{scaleY:0},0);tl.set(P+' .ico',{opacity:0},0);tl.set(P+' .chip',{opacity:0},0);\n"
   + "".join(f"""
tl.to(P+' .it{i} .dot',{{borderColor:'#2B7BE0',duration:.25}},T({t}));
tl.fromTo(P+' .it{i} .dot i',{{scale:0}},{{scale:1,duration:.35,ease:'back.out(3)'}},T({t}));
tl.to(P+' .it{i} .lab',{{color:'#2B7BE0',duration:.25}},T({t}));
tl.fromTo(P+' .ico{i}',{{scale:.2,rotation:-18,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:.5,ease:'back.out(1.8)'}},T({t}));
tl.fromTo(P+' .chip{i}',{{y:24,opacity:0}},{{y:0,opacity:1,duration:.35,ease:'power3.out'}},T({t + .25}));
""" + (f"""tl.to(P+' .ico{i}',{{scale:.6,opacity:0,duration:.25,ease:'power2.in'}},T({items2[i+1][1] - .25}));
tl.to(P+' .chip{i}',{{opacity:0,duration:.2}},T({items2[i+1][1] - .25}));
tl.to(P+' .it{i} .seg b',{{scaleY:1,duration:.35,ease:'power2.inOut'}},T({items2[i+1][1] - .35}));
""" if i < 2 else "") for i, (l, t, c, ch) in enumerate(items2)) + """
tl.to([P+' .list',P+' .stage'],{opacity:0,y:-40,duration:.25,ease:'power2.in'},T(7.13));
""")

# ------------------------------------------------------------------ S3 min/max
years = ["Today", "Last month", "Last year", "2 years ago"]
scene("s03-minmax", 7.40, 11.60, """
#__RID__ .top{position:absolute;left:0;right:0;top:120px;display:flex;justify-content:center;align-items:center;gap:30px;height:150px;}
#__RID__ .top .k{font-weight:600;font-size:60px;}
#__RID__ .top .k em{font-style:normal;color:#2563EB;margin-left:10px;}
#__RID__ .win{position:relative;width:520px;height:150px;overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 28%,#000 72%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0,#000 28%,#000 72%,transparent 100%);}
#__RID__ .reel{position:absolute;left:0;top:0;width:100%;}
#__RID__ .reel div{height:150px;line-height:150px;font-weight:700;font-size:76px;color:#5B7BD5;white-space:nowrap;}
#__RID__ .reel div.last{color:#E5322D;}
#__RID__ .tiles{position:absolute;left:0;right:0;top:330px;display:flex;justify-content:center;gap:70px;}
#__RID__ .tile{width:400px;height:330px;background:#fff;border-radius:34px;box-shadow:0 30px 60px rgba(20,27,60,.13);display:flex;flex-direction:column;align-items:center;justify-content:center;}
#__RID__ .tile .l{font-weight:600;font-size:34px;color:#8A94A6;letter-spacing:4px;}
#__RID__ .tile .n{font-weight:800;font-size:170px;line-height:1;color:#141B3C;}
#__RID__ .note{position:absolute;left:1230px;top:650px;width:390px;padding:26px 30px;background:#FFE27A;border-radius:10px;
  box-shadow:0 18px 30px rgba(20,27,60,.18);font-weight:600;font-size:38px;display:flex;align-items:center;gap:16px;}
""", f"""
<div class="top"><div class="k">Last updated<em>›</em></div><div class="win"><div class="reel">{''.join(f'<div class="{"last" if i == 3 else ""}">{y}</div>' for i, y in enumerate(years))}</div></div></div>
<div class="tiles"><div class="tile t0"><div class="l">MIN</div><div class="n">40</div></div><div class="tile t1"><div class="l">MAX</div><div class="n">120</div></div></div>
<div class="note">{icon('2753', 46)}<span>Just a guess</span></div>
""", """
tl.fromTo(P+' .top',{opacity:0,y:30},{opacity:1,y:0,duration:.4,ease:'power3.out'},0.05);
tl.fromTo(P+' .t0',{y:80,opacity:0,scale:.9},{y:0,opacity:1,scale:1,duration:.5,ease:'back.out(1.6)'},T(7.53));
tl.fromTo(P+' .t1',{y:80,opacity:0,scale:.9},{y:0,opacity:1,scale:1,duration:.5,ease:'back.out(1.6)'},T(8.04));
tl.to(P+' .tile',{backgroundColor:'#EEF1F5',duration:.5},T(8.79));
tl.to(P+' .tile .n',{color:'#A3ABB7',duration:.5},T(8.79));
// Lisa-style rolling carousel with motion blur, landing on "2 years ago"
tl.to(P+' .reel',{y:-150,filter:'blur(6px)',duration:.28,ease:'power2.in'},T(9.62));
tl.to(P+' .reel',{y:-300,duration:.24,ease:'none'},T(9.90));
tl.to(P+' .reel',{y:-450,filter:'blur(0px)',duration:.45,ease:'back.out(1.6)'},T(10.14));
tl.fromTo(P+' .note',{scale:1.7,rotation:16,opacity:0},{scale:1,rotation:6,opacity:1,duration:.3,ease:'power4.out'},T(9.99));
tl.fromTo(P+' .tiles',{x:0},{x:-10,duration:.05,yoyo:true,repeat:3,ease:'none'},T(10.25));
tl.to([P+' .top',P+' .tiles',P+' .note'],{opacity:0,filter:'blur(10px)',duration:.25,ease:'power2.in'},T(11.33));
""")

# ------------------------------------------------------------------ S4 shelves
def shelf_boxes(prefix, n_per, rows):
    out = []
    for r in range(rows):
        for c in range(n_per):
            out.append(f'<div class="bx {prefix}{r * n_per + c}" style="left:{70 + c * 122}px;top:{20 + r * 130}px">{icon("1f4e6", 104)}</div>')
    return "".join(out)


scene("s04-shelves", 11.60, 16.55, """
#__RID__ .cards{position:absolute;left:0;right:0;top:90px;display:flex;justify-content:center;gap:80px;}
#__RID__ .pc{position:relative;width:760px;height:680px;background:#fff;border-radius:36px;box-shadow:0 30px 60px rgba(20,27,60,.13);}
#__RID__ .tag{position:absolute;left:40px;top:34px;display:flex;align-items:center;gap:14px;padding:12px 26px;border-radius:40px;font-weight:700;font-size:34px;}
#__RID__ .tag.r{background:#FDE7E6;color:#D7261F;}
#__RID__ .tag.a{background:#FFF1D6;color:#B76E00;}
#__RID__ .shelf{position:absolute;left:40px;top:120px;width:680px;height:400px;}
#__RID__ .plank{position:absolute;left:0;width:680px;height:14px;border-radius:7px;background:#CBD3DE;}
#__RID__ .bx{position:absolute;width:104px;height:104px;}
#__RID__ .foot{position:absolute;left:40px;right:40px;bottom:26px;display:flex;justify-content:space-between;align-items:center;font-weight:600;font-size:30px;color:#6B7487;}
#__RID__ .foot b{font-weight:800;font-size:44px;color:#141B3C;}
#__RID__ .why{display:flex;align-items:center;gap:10px;}
#__RID__ .xbig{position:absolute;left:250px;top:110px;width:180px;height:180px;}
""", f"""
<div class="cards">
 <div class="pc pl"><div class="tag r">{icon('1f4e6', 40)}Overstocked</div>
  <div class="shelf"><div class="plank" style="top:124px"></div><div class="plank" style="top:254px"></div><div class="plank" style="top:384px"></div>{shelf_boxes('L', 5, 3)}</div>
  <div class="foot"><span class="why w0">{icon('1f4c9', 40)}Doesn't sell</span><span>On hand <b class="cntL">0</b></span></div></div>
 <div class="pc pr"><div class="tag a">{icon('274c', 36)}Out of stock</div>
  <div class="shelf"><div class="plank" style="top:124px"></div><div class="plank" style="top:254px"></div><div class="plank" style="top:384px"></div>{shelf_boxes('R', 2, 3)}<div class="xbig">{icon('274c', 180)}</div></div>
  <div class="foot"><span class="why w1">{icon('1f4c8', 40)}Sells fast</span><span>On hand <b class="cntR">36</b></span></div></div>
</div>
""", """
tl.fromTo(P+' .pl',{y:60,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},T(11.75));
tl.set(P+' .pl .bx',{y:-520,opacity:0},0);
""" + "".join(f"tl.to(P+' .L{i}',{{y:0,opacity:1,duration:.38,ease:'bounce.out'}},T({12.36 + i * 0.06:.2f}));\n" for i in range(15)) + """
var cL={v:0};tl.to(cL,{v:860,duration:1.0,ease:'power2.out',onUpdate:function(){document.querySelector(P+' .cntL').textContent=Math.round(cL.v);}},T(12.4));
tl.fromTo(P+' .w0',{opacity:0,x:-20},{opacity:1,x:0,duration:.3},T(13.89));
tl.fromTo(P+' .pr',{y:60,opacity:0},{y:0,opacity:1,duration:.5,ease:'power3.out'},T(14.2));
tl.set(P+' .xbig',{scale:0,opacity:0},0);
""" + "".join(f"tl.to(P+' .R{i}',{{y:420,opacity:0,duration:.35,ease:'power2.in'}},T({14.75 + i * 0.07:.2f}));\n" for i in range(6)) + """
var cR={v:36};tl.to(cR,{v:0,duration:.6,ease:'power1.in',onUpdate:function(){document.querySelector(P+' .cntR').textContent=Math.round(cR.v);}},T(14.75));
tl.to(P+' .xbig',{scale:1,opacity:1,duration:.4,ease:'back.out(2.5)'},T(15.36));
tl.fromTo(P+' .w1',{opacity:0,x:-20},{opacity:1,x:0,duration:.3},T(15.66));
tl.to(P+' .cards',{opacity:0,scale:.96,duration:.25,ease:'power2.in'},T(16.3));
""")

# ------------------------------------------------------------------ S5 frozen cash + call
bubble = "Where's my order?"
scene("s05-pain", 16.55, 22.70, """
#__RID__ .cash{position:absolute;left:660px;top:120px;width:600px;height:600px;}
#__RID__ .cash .money{position:absolute;left:150px;top:110px;width:300px;height:300px;}
#__RID__ .cash .ice{position:absolute;left:60px;top:20px;width:480px;height:480px;opacity:0;}
#__RID__ .cash .frost{position:absolute;left:0;top:-40px;width:600px;height:600px;border-radius:50%;
  background:radial-gradient(closest-side,rgba(190,230,255,.0) 40%,rgba(190,230,255,.7) 70%,rgba(255,255,255,0) 100%);opacity:0;}
#__RID__ .flake{position:absolute;width:70px;height:70px;}
#__RID__ .cash .t{position:absolute;left:-300px;right:-300px;top:500px;white-space:nowrap;text-align:center;font-weight:700;font-size:54px;}
#__RID__ .cash .t span{color:#2B7BE0;}
#__RID__ .cash .amt{position:absolute;left:-300px;right:-300px;top:584px;white-space:nowrap;text-align:center;font-weight:600;font-size:32px;color:#D7261F;}
#__RID__ .call{position:absolute;left:1060px;top:150px;width:620px;height:500px;border-radius:56px;background:#0D111C;color:#fff;padding:52px 56px;}
#__RID__ .call .in{display:flex;align-items:center;gap:26px;}
#__RID__ .call .av{width:110px;height:110px;border-radius:28px;background:#2E6BF0;display:flex;align-items:center;justify-content:center;}
#__RID__ .call .nm{font-weight:600;font-size:40px;}
#__RID__ .call .sub{font-family:'Roboto';font-weight:500;font-size:28px;color:#9AA4B8;}
#__RID__ .bub{margin-top:56px;display:inline-block;background:#fff;color:#141B3C;border-radius:30px 30px 30px 8px;padding:22px 34px;font-weight:600;font-size:42px;min-height:110px;min-width:460px;}
#__RID__ .bub i{font-style:normal;opacity:0;}
#__RID__ .bell{position:absolute;right:50px;top:50px;width:70px;height:70px;}
""", f"""
<div class="cash"><div class="frost"></div><div class="ice">{icon('1f9ca', 480)}</div><div class="money">{icon('1f4b5', 300)}</div>
 <div class="flake f0" style="left:40px;top:60px">{icon('2744', 70)}</div><div class="flake f1" style="left:500px;top:110px">{icon('2744', 56)}</div><div class="flake f2" style="left:470px;top:400px">{icon('2744', 64)}</div>
 <div class="t">Cash <span>frozen</span> on a shelf</div><div class="amt">€<b class="cnt">0</b> tied up in stock</div></div>
<div class="call"><div class="bell">{icon('1f514', 70)}</div>
 <div class="in"><div class="av">{icon('1f4de', 70)}</div><div><div class="nm">Incoming call</div><div class="sub">Customer · Order #4471</div></div></div>
 <div class="bub">{''.join(f'<i>{c}</i>' if c != ' ' else '<i>&nbsp;</i>' for c in bubble)}</div></div>
""", """
tl.fromTo(P+' .money',{scale:0,rotation:-20},{scale:1,rotation:0,duration:.5,ease:'back.out(2)'},T(16.65));
tl.fromTo(P+' .t',{opacity:0,y:20},{opacity:1,y:0,duration:.35},T(17.0));
tl.to(P+' .frost',{opacity:1,duration:.6},T(17.58));
tl.fromTo(P+' .ice',{opacity:0,scale:.6},{opacity:.85,scale:1,duration:.5,ease:'back.out(1.5)'},T(17.58));
tl.to(P+' .money',{filter:'saturate(.25) brightness(1.15) hue-rotate(160deg)',duration:.6},T(17.6));
tl.fromTo(P+' .flake',{scale:0,opacity:0},{scale:1,opacity:1,duration:.35,stagger:.12,ease:'back.out(2)'},T(17.7));
var c={v:0};tl.fromTo(P+' .amt',{opacity:0},{opacity:1,duration:.3},T(17.9));
tl.to(c,{v:48200,duration:1.1,ease:'power2.out',onUpdate:function(){document.querySelector(P+' .cnt').textContent=Math.round(c.v).toLocaleString('en-US');}},T(17.9));
tl.to(P+' .cash',{x:-480,scale:.78,duration:.6,ease:'power3.inOut'},T(19.25));
tl.fromTo(P+' .call',{x:500,opacity:0},{x:0,opacity:1,duration:.6,ease:'power3.out'},T(19.4));
tl.fromTo(P+' .call',{rotation:0},{rotation:2.5,duration:.06,yoyo:true,repeat:9,ease:'none'},T(20.3));
tl.fromTo(P+' .bell',{rotation:-18},{rotation:18,duration:.08,yoyo:true,repeat:9,ease:'none'},T(20.3));
""" + "".join(f"tl.set(P+' .bub i:nth-child({i+1})',{{opacity:1}},T({20.82 + i * 0.065:.3f}));\n" for i in range(len(bubble))) + """
// Lisa collapse: card squeezes to a bar, then a line
tl.to(P+' .cash',{opacity:0,duration:.25},T(22.05));
tl.to(P+' .call > *',{opacity:0,duration:.12},T(22.15));
tl.to(P+' .call',{x:-490,width:60,paddingLeft:0,paddingRight:0,borderRadius:30,duration:.28,ease:'power3.in'},T(22.2));
tl.to(P+' .call',{height:4,y:248,width:4,duration:.18,ease:'power2.in'},T(22.48));
tl.to(P+' .call',{opacity:0,duration:.05},T(22.66));
""")

# ------------------------------------------------------------------ S6 meet Billie
RIB = "M -260 760 C 300 300, 1100 250, 2200 480"
scene("s06-meet", 22.70, 27.85, """
#__RID__ svg.rib{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible;}
#__RID__ .r1,#__RID__ .r2{transform-origin:960px 540px;}
#__RID__ .lab{position:absolute;left:0;right:0;top:470px;display:flex;justify-content:center;}
#__RID__ .lab span{display:block;background:linear-gradient(180deg,#F7682D,#E5322D);color:#fff;font-weight:500;font-size:64px;padding:8px 34px;border-radius:6px;}
#__RID__ .lock{position:absolute;left:0;right:0;top:80px;height:700px;display:flex;align-items:center;justify-content:center;gap:70px;}
#__RID__ .bot{width:360px;height:372px;}
#__RID__ .bot img{width:360px;height:372px;display:block;}
#__RID__ .col{display:flex;flex-direction:column;align-items:flex-start;gap:20px;}
#__RID__ .name{font-weight:800;font-size:190px;line-height:.95;letter-spacing:-4px;background:linear-gradient(180deg,#F7682D 0%,#E5322D 60%,#B5244A 100%);-webkit-background-clip:text;background-clip:text;color:transparent;}
#__RID__ .role{display:block;background:linear-gradient(180deg,#F7682D,#E5322D);color:#fff;font-weight:500;font-size:40px;padding:6px 24px;border-radius:6px;}
#__RID__ .by{display:flex;align-items:center;gap:18px;font-weight:500;font-size:30px;color:#6B7487;}
#__RID__ .by img{height:130px;width:267px;display:block;margin:-20px 0;}
#__RID__ .od{display:flex;align-items:center;gap:16px;background:#fff;border-radius:40px;padding:12px 26px;box-shadow:0 14px 30px rgba(20,27,60,.12);font-weight:600;font-size:30px;}
#__RID__ .wipe{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#2563EB;transform-origin:0 50%;}
""", f"""
<svg class="rib" viewBox="0 0 1920 1080" data-layout-allow-overlap>
 <defs>
  <linearGradient id="s06-g1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F7682D"/><stop offset=".6" stop-color="#E5322D"/><stop offset="1" stop-color="#6B2A8C"/></linearGradient>
  <linearGradient id="s06-g2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3A4A8C"/><stop offset=".55" stop-color="#1A2456"/><stop offset="1" stop-color="#0B1030"/></linearGradient>
  <path id="s06-p" d="{RIB}"/>
 </defs>
 <g class="r1"><path d="{RIB}" stroke="url(#s06-g1)" stroke-width="330" fill="none"/>
  <text data-layout-allow-overlap font-family="Poppins" font-weight="500" font-size="190" fill="#fff" dy="64"><textPath href="#s06-p" startOffset="22%">Meet</textPath></text></g>
 <g class="r2"><path d="{RIB}" stroke="url(#s06-g2)" stroke-width="330" fill="none"/>
  <text data-layout-allow-overlap font-family="Poppins" font-weight="500" font-size="200" fill="#fff" dy="66"><textPath href="#s06-p" startOffset="20%">Billie</textPath></text></g>
</svg>
<div class="lab"><span>AI Procurement Agent</span></div>
<div class="lock">
 <div class="bot"><img src="assets/billie.png" alt="Billie"></div>
 <div class="col"><div class="name">Billie</div><div class="role">AI Procurement Agent</div>
  <div class="by">by <img src="assets/bayforward.svg" alt="Bay Forward"></div>
  <div class="od">Works inside your {odoo(40)}</div></div>
</div>
<div class="wipe"></div>
""", """
tl.set(P+' .wipe',{scaleX:0},0);
tl.fromTo(P+' .r1',{x:-1900,rotation:-14,opacity:1},{x:0,rotation:0,duration:.45,ease:'power3.out'},T(22.74));
tl.fromTo(P+' .r2',{x:-1900,rotation:-14},{x:0,rotation:0,duration:.45,ease:'power3.out'},T(23.12));
tl.to(P+' .r1',{opacity:0,duration:.1},T(23.5));
tl.to(P+' .r2',{x:2100,rotation:10,duration:.4,ease:'power3.in'},T(23.82));
tl.set(P+' .r2',{opacity:0},T(24.25));
tl.fromTo(P+' .lab span',{scaleX:2.2,scaleY:.3,opacity:0},{scaleX:1,scaleY:1,opacity:1,duration:.35,ease:'back.out(1.6)'},T(24.0));
tl.to(P+' .lab',{opacity:0,y:-40,duration:.2},T(24.55));
tl.fromTo(P+' .bot',{scale:0,rotation:-12},{scale:1,rotation:0,duration:.6,ease:'back.out(1.8)'},T(24.6));
tl.fromTo(P+' .name',{x:-60,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},T(24.7));
tl.fromTo(P+' .role',{scaleX:0,opacity:0},{scaleX:1,opacity:1,duration:.35,ease:'power3.out',transformOrigin:'0 50%'},T(24.9));
tl.fromTo(P+' .by',{y:20,opacity:0},{y:0,opacity:1,duration:.4},T(25.23));
tl.fromTo(P+' .od',{y:20,opacity:0,scale:.9},{y:0,opacity:1,scale:1,duration:.4,ease:'back.out(2)'},T(26.6));
tl.to(P+' .bot',{y:-14,duration:.7,yoyo:true,repeat:3,ease:'sine.inOut'},T(25.2));
tl.to(P+' .wipe',{scaleX:1,duration:.32,ease:'power3.in'},T(27.53));
""")

# ------------------------------------------------------------------ S7 split-screen recalculation
pills = [("1f4cd", "Reorder Point", 29.25), ("1f4ca", "Max Stock", 30.27), ("1f6e1", "Safety Stock", 31.32),
         ("1f4e6", "Every Product", 32.40), ("23f1", "Real Lead Times", 34.50), ("1f501", "Order Frequency", 35.37),
         ("1f9fe", "Order Costs", 36.99)]
products = [("Office Chair Pro", "SKU 10417", (58, 72), (140, 165), (18, 24)),
            ("Steel Shelf 120", "SKU 20981", (25, 31), (80, 96), (8, 11)),
            ("LED Panel 60W", "SKU 33102", (60, 84), (200, 240), (20, 28)),
            ("Desk Lamp Arc", "SKU 41876", (30, 26), (90, 82), (10, 9))]
PH, PG = 108, 24


def pcard(i, p):
    name, sku, rp, ms, ss = p
    rows = "".join(
        f'<div class="mr"><span>{lab}</span><b class="v{k}">{(v[0] if i == 0 else v[1])}</b><em class="d{k}">{"↑" if v[1] >= v[0] else "↓"}</em></div>'
        for k, (lab, v) in enumerate([("Reorder point", rp), ("Max stock", ms), ("Safety stock", ss)]))
    return (f'<div class="pcd pc{i}"><i class="bd"></i><div class="ph">{icon("1f4e6", 54)}<div><div class="pn">{name}</div>'
            f'<div class="ps">{sku}</div></div></div>{rows}<i class="plus">+</i></div>')


scene("s07-recalc", 27.85, 38.15, f"""
#__RID__{{background:#fff;}}
#__RID__ .blue{{position:absolute;left:0;top:0;width:1920px;height:1080px;background:#2563EB;transform-origin:0 50%;}}
#__RID__ .lw{{position:absolute;left:0;top:0;width:1000px;height:820px;overflow:hidden;-webkit-mask-image:linear-gradient(180deg,#000 0,#000 78%,transparent 100%);mask-image:linear-gradient(180deg,#000 0,#000 78%,transparent 100%);}}
#__RID__ .list{{position:absolute;left:90px;top:0;}}
#__RID__ .pill{{position:relative;height:{PH}px;margin-bottom:{PG}px;display:flex;align-items:center;gap:22px;padding:0 46px 0 30px;border-radius:{PH // 2}px;
  background:rgba(255,255,255,.14);border:2px solid rgba(255,255,255,.3);color:#fff;font-family:'Roboto';font-weight:500;font-size:52px;width:max-content;}}
#__RID__ .stack{{position:absolute;left:1180px;top:200px;width:580px;height:440px;}}
#__RID__ .pcd{{position:absolute;left:0;top:0;width:580px;height:440px;background:#fff;border-radius:34px;box-shadow:0 30px 60px rgba(20,27,60,.18);padding:36px 40px;}}
#__RID__ .bd{{position:absolute;left:22px;top:22px;width:16px;height:16px;border-radius:50%;background:#4F46E5;}}
#__RID__ .ph{{display:flex;align-items:center;gap:18px;margin-bottom:22px;}}
#__RID__ .pn{{font-weight:700;font-size:36px;}}
#__RID__ .ps{{font-family:'Roboto';font-weight:500;font-size:22px;color:#6F7785;}}
#__RID__ .mr{{display:flex;align-items:center;height:78px;border-top:2px solid #EEF1F5;font-weight:500;font-size:30px;color:#4B5568;}}
#__RID__ .mr b{{margin-left:auto;font-weight:800;font-size:44px;color:#141B3C;}}
#__RID__ .mr em{{font-style:normal;width:46px;text-align:right;font-weight:800;font-size:34px;color:#16A34A;}}
#__RID__ .plus{{position:absolute;right:24px;bottom:22px;width:52px;height:52px;border-radius:50%;background:#4F46E5;color:#fff;font-style:normal;font-weight:600;font-size:38px;line-height:50px;text-align:center;}}
#__RID__ .chips{{position:absolute;left:1000px;width:920px;top:700px;display:flex;justify-content:center;gap:18px;}}
#__RID__ .chip{{display:flex;align-items:center;gap:12px;background:#F1F5FB;border:2px solid #DCE5F2;border-radius:40px;padding:10px 24px;font-weight:600;font-size:28px;}}
""", f"""
<div class="blue"></div>
<div class="lw"><div class="list">{''.join(f'<div class="pill p{i}">{icon(c, 58)}<span>{t}</span></div>' for i, (c, t, _) in enumerate(pills))}</div></div>
<div class="stack">{''.join(pcard(i, p) for i, p in reversed(list(enumerate(products))))}</div>
<div class="chips"><div class="chip c0">{icon('23f1', 34)}Lead time 26d</div><div class="chip c1">{icon('1f501', 34)}4 orders / mo</div><div class="chip c2">{icon('1f9fe', 34)}€35 / order</div></div>
""", f"""
var PH={PH + PG},CY=470-{PH // 2};
tl.fromTo(P+' .blue',{{scaleX:1}},{{scaleX:1000/1920,duration:.55,ease:'power3.inOut'}},0);
tl.fromTo(P+' .list',{{y:1100}},{{y:CY+PH,duration:.7,ease:'power3.out'}},T(28.1));
tl.fromTo(P+' .pill',{{opacity:0,x:-40}},{{opacity:1,x:0,duration:.4,stagger:.05}},T(28.1));
// card stack slots: front / mid / back
var SL=[{{x:0,y:0,scale:1,opacity:1}},{{x:0,y:-46,scale:.92,opacity:1}},{{x:0,y:-88,scale:.84,opacity:1}},{{x:0,y:-120,scale:.78,opacity:0}}];
for(var i=0;i<4;i++){{tl.set(P+' .pc'+i,SL[i],0);}}
tl.fromTo(P+' .stack',{{x:200,opacity:0}},{{x:0,opacity:1,duration:.6,ease:'power3.out'}},T(28.3));
tl.set(P+' .chip',{{opacity:0,y:16}},0);
""" + "".join(f"""
tl.to(P+' .list',{{y:CY-{i}*PH,duration:.45,ease:'power3.inOut'}},T({t - .15:.2f}));
tl.set(P+' .p{i}',{{color:'#10213F'}},T({t - .05:.2f}));
tl.to(P+' .p{i}',{{backgroundColor:'#ffffff',x:46,scale:1.05,duration:.3,ease:'power2.out'}},T({t - .05:.2f}));
""" + (f"tl.set(P+' .p{i-1}',{{backgroundColor:'rgba(255,255,255,.14)',color:'#ffffff'}},T({t - .05:.2f}));\ntl.to(P+' .p{i-1}',{{x:0,scale:1,duration:.3}},T({t - .05:.2f}));\n" if i else "")
   for i, (c, lab, t) in enumerate(pills)) + "".join(f"""
var cv{k}={{v:{products[0][2 + k][0]}}};tl.to(cv{k},{{v:{products[0][2 + k][1]},duration:.6,ease:'power2.out',onUpdate:function(){{document.querySelector(P+' .pc0 .v{k}').textContent=Math.round(cv{k}.v);}}}},T({t}));
tl.fromTo(P+' .pc0 .d{k}',{{opacity:0,y:10}},{{opacity:1,y:0,duration:.3}},T({t + .3:.2f}));
""" for k, t in enumerate([29.25, 30.27, 31.32])) + """
tl.set(P+' .pc1 .mr em,'+P+' .pc2 .mr em,'+P+' .pc3 .mr em',{opacity:1},0);
tl.set([P+' .pc1 > *',P+' .pc2 > *',P+' .pc3 > *'],{opacity:0},0);
tl.set(P+' .pc0 .mr em',{opacity:0},0);
function cycle(t,out,ins){tl.to(P+' .pc'+out+' > *',{opacity:0,duration:.15},t);
  tl.to(P+' .pc'+out,{x:-260,rotation:-8,opacity:0,duration:.4,ease:'power2.in'},t);
  tl.to(P+' .pc'+ins[0]+' > *',{opacity:1,duration:.25},t+.3);
  ins.forEach(function(c,j){tl.to(P+' .pc'+c,Object.assign({duration:.45,ease:'power3.out'},SL[j]),t+.12);});}
cycle(T(32.45),0,[1,2,3]);
cycle(T(33.35),1,[2,3]);
tl.to(P+' .c0',{opacity:1,y:0,duration:.35,ease:'back.out(2)'},T(34.5));
tl.to(P+' .c1',{opacity:1,y:0,duration:.35,ease:'back.out(2)'},T(35.37));
tl.to(P+' .c2',{opacity:1,y:0,duration:.35,ease:'back.out(2)'},T(36.99));
tl.to([P+' .list',P+' .stack',P+' .chips'],{opacity:0,duration:.25},T(37.85));
tl.to(P+' .blue',{scaleX:0,duration:.3,ease:'power3.in'},T(37.85));
""")

# ------------------------------------------------------------------ S8 frequency carousel
freq = ["Daily", "Weekly", "Monthly"]
scene("s08-frequency", 38.15, 43.45, """
#__RID__{background:linear-gradient(135deg,#F1F6FC 0%,#D5E3F5 55%,#BCD2EE 100%);}
#__RID__ .streak{position:absolute;width:1400px;height:160px;background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.55),rgba(255,255,255,0));transform-origin:50% 50%;}
#__RID__ .eyebrow{position:absolute;left:0;right:0;top:250px;text-align:center;font-weight:600;font-size:30px;letter-spacing:8px;color:#2563EB;}
#__RID__ .row{position:absolute;left:0;right:0;top:300px;height:360px;display:flex;align-items:center;justify-content:center;gap:40px;}
#__RID__ .k{font-weight:600;font-size:76px;white-space:nowrap;}
#__RID__ .k em{font-style:normal;margin-left:10px;}
#__RID__ .win{position:relative;width:560px;height:360px;overflow:hidden;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.35) 22%,#000 40%,#000 60%,rgba(0,0,0,.35) 78%,transparent 100%);mask-image:linear-gradient(180deg,transparent 0,rgba(0,0,0,.35) 22%,#000 40%,#000 60%,rgba(0,0,0,.35) 78%,transparent 100%);}
#__RID__ .reel{position:absolute;left:0;top:0;width:100%;}
#__RID__ .reel div{height:120px;line-height:120px;font-weight:700;font-size:104px;white-space:nowrap;
  background:linear-gradient(180deg,#5B8DEF,#2D5BD7);-webkit-background-clip:text;background-clip:text;color:transparent;}
""", f"""
<div class="streak" style="left:-200px;top:120px;transform:rotate(-24deg)"></div>
<div class="streak s2" style="left:700px;top:620px;transform:rotate(-24deg)"></div>
<div class="eyebrow">YOU DECIDE</div>
<div class="row"><div class="k">Billie updates<em>›</em></div>
 <div class="win"><div class="reel"><div></div>{''.join(f'<div>{w}</div>' for w in freq)}<div></div></div></div></div>
<div class="cursor">{CURSOR}</div><div class="ripple"></div>
""", """
tl.fromTo(P+' .streak',{x:-300},{x:300,duration:5.3,ease:'none'},0);
tl.fromTo(P+' .eyebrow',{opacity:0,y:16},{opacity:1,y:0,duration:.4},T(38.3));
tl.fromTo(P+' .k',{opacity:0,x:-40,filter:'blur(8px)'},{opacity:1,x:0,filter:'blur(0px)',duration:.5,ease:'power3.out'},T(38.35));
tl.fromTo(P+' .win',{opacity:0},{opacity:1,duration:.5},T(38.6));
tl.set(P+' .reel',{y:0},0);
// row centre = 180px; item i (1-based in reel incl. spacer) centred when y = 180-60-120*i
tl.to(P+' .reel',{y:180-60-120,duration:.5,ease:'power3.out'},T(38.7));
tl.fromTo(P+' .cursor',{x:1500,y:900,opacity:1},{x:1330,y:520,duration:.9,ease:'power2.inOut'},T(40.2));
[41.28,41.94,42.72].forEach(function(t,i){
  tl.to(P+' .reel',{y:180-60-120*(i+1),filter:'blur(6px)',duration:.18,ease:'power2.in'},T(t)-.18);
  tl.to(P+' .reel',{filter:'blur(0px)',duration:.25,ease:'power2.out'},T(t));
  tl.fromTo(P+' .ripple',{x:1312,y:502,scale:.3,opacity:.9},{scale:1.4,opacity:0,duration:.45,ease:'power2.out'},T(t)-.02);
  tl.fromTo(P+' .cursor',{scale:1},{scale:.85,duration:.08,yoyo:true,repeat:1},T(t)-.08);
});
tl.to(P+' .row',{scale:1.15,opacity:0,filter:'blur(14px)',duration:.3,ease:'power2.in'},T(43.15));
tl.to([P+' .eyebrow',P+' .cursor'],{opacity:0,duration:.2},T(43.15));
""")

# ------------------------------------------------------------------ S9 replenishment card
rep = [("1f9ee", "Economic Order Quantity", "EOQ · 240 units per order", 46.05),
       ("1f3ed", "Supplier Minimum", "MOQ · 500 units", 47.64),
       ("1f69b", "Full Pallets", "1 pallet = 48 cartons", 49.38)]
scene("s09-replenish", 43.45, 50.60, """
#__RID__ .card{position:absolute;left:340px;top:90px;width:1240px;height:680px;border-radius:60px;background:#0D111C;color:#fff;transform-origin:50% 50%;}
#__RID__ .ttl{position:absolute;left:80px;top:250px;width:360px;font-weight:600;font-size:66px;line-height:1.1;}
#__RID__ .ttl small{display:block;font-weight:500;font-size:28px;color:#8EA0C2;margin-top:16px;line-height:1.3;}
#__RID__ .rows{position:absolute;left:470px;top:80px;width:720px;}
#__RID__ .rw{position:relative;height:172px;display:flex;align-items:center;gap:34px;padding-left:44px;border-radius:30px;margin-bottom:10px;}
#__RID__ .ck{position:absolute;left:-22px;top:18px;width:58px;height:58px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;}
#__RID__ .ck svg{width:30px;height:30px;}
#__RID__ .tileI{width:128px;height:128px;border-radius:30px;background:#2E6BF0;display:flex;align-items:center;justify-content:center;flex:none;}
#__RID__ .tx b{display:block;font-family:'Roboto';font-weight:500;font-size:42px;}
#__RID__ .tx span{display:block;font-family:'Roboto';font-weight:500;font-size:28px;color:#8EA0C2;margin-top:6px;}
""", f"""
<div class="card"><div class="ttl in">Replenish by<small>Your choice, per product</small></div>
 <div class="rows">{''.join(f'<div class="rw r{i}"><div class="ck">{CHECK}</div><div class="tileI">{icon(c, 84)}</div><div class="tx"><b>{a}</b><span>{b}</span></div></div>' for i, (c, a, b, t) in enumerate(rep))}</div></div>
""", """
tl.fromTo(P+' .card',{scaleX:.035,scaleY:.85,opacity:0},{scaleX:.035,scaleY:.85,opacity:1,duration:.08},T(43.48));
tl.to(P+' .card',{scaleX:1,scaleY:1,duration:.5,ease:'power3.out'},T(43.56));
tl.fromTo(P+' .ttl',{opacity:0,x:-30},{opacity:1,x:0,duration:.4},T(43.98));
tl.fromTo(P+' .rw',{opacity:0,x:60},{opacity:.35,x:0,duration:.4,stagger:.1,ease:'power3.out'},T(44.2));
tl.set(P+' .ck',{scale:0},0);
""" + "".join(f"""
tl.to(P+' .r{i}',{{opacity:1,backgroundColor:'rgba(46,107,240,.16)',duration:.3}},T({t}));
tl.to(P+' .r{i} .ck',{{scale:1,duration:.35,ease:'back.out(3)'}},T({t + .25:.2f}));
tl.to(P+' .r{i} .tileI',{{scale:1.1,duration:.18,yoyo:true,repeat:1}},T({t}));
""" + (f"tl.to(P+' .r{i}',{{backgroundColor:'rgba(46,107,240,0)',duration:.3}},T({rep[i+1][3]}));\n" if i < 2 else "")
   for i, (c, a, b, t) in enumerate(rep)) + """
tl.to(P+' .card > *',{opacity:0,duration:.15},T(50.2));
tl.to(P+' .card',{scaleX:.035,duration:.25,ease:'power3.in'},T(50.25));
tl.to(P+' .card',{scaleY:.004,opacity:0,duration:.1,ease:'power2.in'},T(50.5));
""")

# ------------------------------------------------------------------ S10 Odoo exceptions
rows10 = [("Office Chair Pro", 40, 120, None), ("Steel Shelf 120", 25, 80, ("Lead time +12d", 53.61)),
          ("LED Panel 60W", 60, 200, None), ("Desk Lamp Arc", 30, 90, ("Demand +45%", 54.30)),
          ("Cable Kit", 100, 400, None)]
scene("s10-exceptions", 50.60, 55.55, """
#__RID__ .top{position:absolute;left:0;right:0;top:90px;height:110px;display:flex;align-items:center;justify-content:center;gap:34px;}
#__RID__ .top .w{font-weight:600;font-size:72px;}
#__RID__ .top .w span{display:inline-block;margin-right:20px;}
#__RID__ .tbl{position:absolute;left:220px;top:260px;width:1060px;background:#fff;border-radius:30px;box-shadow:0 30px 60px rgba(20,27,60,.13);padding:20px 34px;overflow:hidden;}
#__RID__ .tr{position:relative;display:grid;grid-template-columns:400px 130px 130px 1fr;align-items:center;height:84px;border-top:2px solid #EEF1F5;font-weight:500;font-size:30px;border-radius:14px;padding:0 14px;}
#__RID__ .tr.h{border-top:none;height:60px;font-size:22px;font-weight:600;color:#8A94A6;letter-spacing:2px;}
#__RID__ .st{display:flex;align-items:center;gap:12px;}
#__RID__ .ok{color:#16A34A;font-weight:600;font-size:26px;}
#__RID__ .ex{position:absolute;right:14px;display:flex;align-items:center;gap:10px;background:#E5322D;color:#fff;border-radius:30px;padding:8px 20px;font-weight:600;font-size:26px;}
#__RID__ .beam{position:absolute;left:0;right:0;top:0;height:90px;background:linear-gradient(180deg,rgba(0,227,250,0),rgba(0,227,250,.35),rgba(0,227,250,0));}
#__RID__ .bot{position:absolute;left:1390px;top:270px;width:330px;height:341px;}
#__RID__ .bot img{width:330px;height:341px;display:block;}
#__RID__ .cnt{position:absolute;left:1350px;top:640px;width:410px;text-align:center;}
#__RID__ .cnt span{display:inline-flex;align-items:center;gap:12px;background:#141B3C;color:#fff;border-radius:40px;padding:12px 28px;font-weight:600;font-size:30px;}
""", f"""
<div class="top">{odoo(96)}<div class="w"><span>runs</span><span>on</span><span>rules</span></div></div>
<div class="tbl"><div class="tr h"><div>PRODUCT</div><div>MIN</div><div>MAX</div><div>RULE</div></div>
{''.join(f'<div class="tr t{i}"><div>{n}</div><div>{a}</div><div>{b}</div><div class="st"><span class="ok">✓ OK</span></div>{exchip(e)}</div>' for i, (n, a, b, e) in enumerate(rows10))}
<div class="beam"></div></div>
<div class="bot"><img src="assets/billie.png" alt="Billie"></div>
<div class="cnt"><span>{icon('1f50d', 34)}2 exceptions caught</span></div>
""", """
tl.fromTo(P+' .top svg',{scale:.4,opacity:0},{scale:1,opacity:1,duration:.45,ease:'back.out(2)'},T(50.73));
tl.fromTo(P+' .top .w span',{y:30,opacity:0},{y:0,opacity:1,duration:.3,stagger:.3,ease:'back.out(2)'},T(51.12));
tl.fromTo(P+' .tbl',{y:40,opacity:0},{y:0,opacity:1,duration:.4,ease:'power3.out'},T(51.6));
tl.fromTo(P+' .tr',{opacity:0,x:-30},{opacity:1,x:0,duration:.3,stagger:.07,ease:'power3.out'},T(51.75));
tl.set(P+' .ex',{opacity:0,scale:.5},0);tl.set(P+' .beam',{opacity:0},0);
tl.fromTo(P+' .bot',{x:500,rotation:15},{x:0,rotation:0,duration:.55,ease:'back.out(1.4)'},T(52.6));
tl.fromTo(P+' .beam',{y:40,opacity:1},{y:480,duration:1.6,ease:'none'},T(52.95));
tl.to(P+' .beam',{opacity:0,duration:.2},T(54.55));
tl.to(P+' .t1',{backgroundColor:'#FDE7E6',duration:.25},T(53.61));
tl.to(P+' .t1 .ok',{opacity:0,duration:.15},T(53.61));
tl.to(P+' .t1 .ex',{opacity:1,scale:1,duration:.35,ease:'back.out(2.5)'},T(53.61));
tl.to(P+' .t3',{backgroundColor:'#FDE7E6',duration:.25},T(54.30));
tl.to(P+' .t3 .ok',{opacity:0,duration:.15},T(54.30));
tl.to(P+' .t3 .ex',{opacity:1,scale:1,duration:.35,ease:'back.out(2.5)'},T(54.30));
tl.fromTo(P+' .cnt',{opacity:0,y:20},{opacity:1,y:0,duration:.35,ease:'back.out(2)'},T(54.6));
tl.to(P+' .bot',{y:-12,duration:.5,yoyo:true,repeat:1,ease:'sine.inOut'},T(53.3));
tl.to([P+' .top',P+' .tbl',P+' .bot',P+' .cnt'],{opacity:0,y:-30,duration:.25,ease:'power2.in'},T(55.3));
""")

# ------------------------------------------------------------------ S11 setup
steps = [("1f9e9", "Install the app", 57.75), (None, "Billie gets to work", 60.48)]
SX = [660, 1260]
scene("s11-setup", 55.55, 61.85, f"""
#__RID__ .mcal{{position:absolute;left:230px;top:96px;width:820px;height:620px;background:#fff;border-radius:34px;box-shadow:0 30px 60px rgba(20,27,60,.13);padding:34px 42px;}}
#__RID__ .mh{{display:flex;align-items:center;gap:16px;font-weight:700;font-size:40px;}}
#__RID__ .mh .chip{{margin-left:auto;background:#FDE7E6;color:#D7261F;border-radius:30px;padding:8px 20px;font-weight:600;font-size:24px;}}
#__RID__ .wd{{display:grid;grid-template-columns:repeat(7,100px);gap:6px;margin-top:22px;font-weight:600;font-size:22px;color:#8A94A6;text-align:center;}}
#__RID__ .mg{{position:relative;display:grid;grid-template-columns:repeat(7,100px);grid-auto-rows:76px;gap:6px;margin-top:10px;}}
#__RID__ .dc{{border-radius:14px;display:flex;align-items:center;justify-content:center;font-weight:600;font-size:28px;color:#141B3C;background:#F3F6FA;}}
#__RID__ .dc.im{{background:#FBD5D3;color:#B4231D;}}
#__RID__ .dc.bl{{background:transparent;}}
#__RID__ svg.x{{position:absolute;left:0;top:0;width:736px;height:404px;overflow:visible;}}
#__RID__ .wr{{position:absolute;left:1140px;top:250px;width:640px;}}
#__RID__ .wr .l1{{font-weight:600;font-size:62px;line-height:1.1;}}
#__RID__ .wr .l2{{font-weight:800;font-size:132px;line-height:1.05;color:#16A34A;white-space:nowrap;}}
#__RID__ .steps{{position:absolute;left:0;top:0;width:1920px;height:1080px;}}
#__RID__ .ln{{position:absolute;top:{390 - 5}px;height:10px;background:#C9D0D9;border-radius:5px;}}
#__RID__ .ln b{{display:block;width:100%;height:100%;background:#2B7BE0;border-radius:5px;transform-origin:0 50%;}}
#__RID__ .st{{position:absolute;top:{390 - 90}px;width:180px;height:180px;border-radius:50%;background:#fff;border:10px solid #C9D0D9;display:flex;align-items:center;justify-content:center;}}
#__RID__ .st img.rb{{width:112px;height:116px;display:block;}}
#__RID__ .sl{{position:absolute;top:{390 + 120}px;width:440px;text-align:center;}}
#__RID__ .sl small{{display:block;font-weight:600;font-size:26px;letter-spacing:4px;color:#2B7BE0;}}
#__RID__ .sl b{{display:block;font-weight:700;font-size:44px;}}
""", f"""
<div class="mcal"><div class="mh">{icon('1f4c5', 46)}<span>October</span><span class="chip">Implementation: 12 weeks</span></div>
 <div class="wd"><span>M</span><span>T</span><span>W</span><span>T</span><span>F</span><span>S</span><span>S</span></div>
 <div class="mg">{''.join('<div class="dc bl"></div>' for _ in range(3))}{''.join(f'<div class="dc d{d}{" im" if d >= 5 and (d + 2) % 7 not in (5, 6) else ""}">{d}</div>' for d in range(1, 32))}
  <svg class="x" viewBox="0 0 736 404"><line class="x1" x1="24" y1="24" x2="712" y2="380" stroke="#E5322D" stroke-width="18" stroke-linecap="round" stroke-dasharray="776" stroke-dashoffset="776"/><line class="x2" x1="712" y1="24" x2="24" y2="380" stroke="#E5322D" stroke-width="18" stroke-linecap="round" stroke-dasharray="776" stroke-dashoffset="776"/><circle class="ring" cx="477" cy="202" r="50" fill="none" stroke="#16A34A" stroke-width="9" stroke-dasharray="315" stroke-dashoffset="315" transform="rotate(-90 477 202)"/></svg></div></div>
<div class="wr"><div class="l1">Implementation:</div><div class="l2">Today ✓</div></div>
<div class="steps">
 <div class="ln l0" style="left:{SX[0] + 90}px;width:{SX[1] - SX[0] - 180}px"><b></b></div>
 {''.join(f'<div class="st s{i}" style="left:{x - 90}px">{icon(c, 92) if c else "<img class=rb src=assets/billie.png alt=Billie>"}</div><div class="sl sl{i}" style="left:{x - 220}px"><small>STEP {i + 1}</small><b>{t}</b></div>' for i, ((c, t, _), x) in enumerate(zip(steps, SX)))}
</div>
""", """
tl.fromTo(P+' .mcal',{opacity:0,y:40,scale:.96},{opacity:1,y:0,scale:1,duration:.35,ease:'power3.out'},T(55.58));
// slow red cross drawn over the booked implementation weeks
tl.to(P+' .x1',{strokeDashoffset:0,duration:.38,ease:'power2.inOut'},T(55.92));
tl.to(P+' .x2',{strokeDashoffset:0,duration:.38,ease:'power2.inOut'},T(56.3));
tl.to(P+' .dc.im',{backgroundColor:'#EEF1F5',color:'#A3ABB7',duration:.3},T(56.62));
tl.to(P+' .mh .chip',{opacity:.35,duration:.3},T(56.62));
// today circled, "Implementation: Today" written in
tl.to(P+' .ring',{strokeDashoffset:0,duration:.35,ease:'power2.out'},T(56.7));
tl.to(P+' .d16',{backgroundColor:'#DCFCE7',color:'#15803D',duration:.25},T(56.7));
tl.fromTo(P+' .wr .l1',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.3,ease:'power2.out'},T(56.6));
tl.fromTo(P+' .wr .l2',{clipPath:'inset(0 100% 0 0)'},{clipPath:'inset(0 0% 0 0)',duration:.35,ease:'power2.out'},T(56.85));
tl.to([P+' .mcal',P+' .wr'],{opacity:0,y:-40,filter:'blur(8px)',duration:.16,ease:'power2.in'},T(57.36));
tl.set(P+' .ln b',{scaleX:0},0);
tl.fromTo(P+' .ln',{opacity:0},{opacity:1,duration:.3},T(57.56));
tl.fromTo(P+' .st',{scale:0},{scale:1,duration:.35,stagger:.06,ease:'back.out(2)'},T(57.52));
tl.fromTo(P+' .sl',{opacity:0,y:20},{opacity:.35,y:0,duration:.3,stagger:.06},T(57.58));
""" + "".join(f"""
tl.to(P+' .s{i}',{{borderColor:'#2B7BE0',duration:.25}},T({t}));
tl.to(P+' .s{i}',{{scale:1.12,duration:.18,yoyo:true,repeat:1,ease:'power2.out'}},T({t}));
tl.to(P+' .sl{i}',{{opacity:1,duration:.25}},T({t}));
""" + (f"tl.to(P+' .l{i} b',{{scaleX:1,duration:.3,ease:'power2.inOut'}},T(60.18));\n" if i < 1 else "")
   for i, (c, lab, t) in enumerate(steps)) + """
tl.to(P+' .s1',{boxShadow:'0 0 0 22px rgba(43,123,224,.18)',duration:.4},T(60.8));
tl.to(P+' .steps',{opacity:0,y:-30,duration:.25,ease:'power2.in'},T(61.6));
""")

# ------------------------------------------------------------------ S12 CTA
letters = list("Billie")
LX = [150, 470, 640, 790, 940, 1130]
LY = [80, 260, 40, 300, 120, 230]
cta_words = [("Book", 64.68), ("a", 64.92), ("20-minute", 64.98), ("stock", 65.62), ("check", 65.94)]
scene("s12-cta", 61.85, TOTAL, """
#__RID__{background:#12163A;}
#__RID__ .L{position:absolute;font-weight:800;font-size:560px;line-height:1;
  background:linear-gradient(180deg,#FF8A3D 0%,#E5322D 52%,#7A2E8E 100%);-webkit-background-clip:text;background-clip:text;color:transparent;}
#__RID__ .end{position:absolute;inset:0;background:#DDE7F1;clip-path:circle(0% at 50% 45%);}
#__RID__ .lock{position:absolute;left:0;right:0;top:120px;display:flex;align-items:center;justify-content:center;gap:40px;}
#__RID__ .lock img{width:240px;height:248px;display:block;}
#__RID__ .wm{font-weight:800;font-size:170px;letter-spacing:-4px;line-height:1;background:linear-gradient(180deg,#F7682D 0%,#E5322D 60%,#B5244A 100%);-webkit-background-clip:text;background-clip:text;color:transparent;}
#__RID__ .cta{position:absolute;left:0;right:0;top:450px;display:flex;justify-content:center;gap:20px;font-weight:700;font-size:76px;}
#__RID__ .cta span{display:inline-block;}
#__RID__ .cta .hl{color:#2563EB;}
#__RID__ .mail{position:absolute;left:0;right:0;top:572px;text-align:center;font-family:'Roboto';font-weight:500;font-size:30px;color:#475569;letter-spacing:.5px;}
#__RID__ .bf{position:absolute;left:0;right:0;top:640px;display:flex;justify-content:center;align-items:center;gap:16px;font-weight:500;font-size:26px;color:#6B7487;}
#__RID__ .bf img{height:160px;width:329px;display:block;margin:-30px 0;}
""", f"""
{''.join(f'<div class="L L{i}" style="left:{x}px;top:{y}px">{c}</div>' for i, (c, x, y) in enumerate(zip(letters, LX, LY)))}
<div class="end">
 <div class="lock"><img src="assets/billie.png" alt="Billie"><div class="wm">Billie</div></div>
 <div class="cta">{''.join(f'<span class="{"hl" if w in ("20-minute",) else ""}">{w}</span>' for w, _ in cta_words)}</div>
 <div class="mail">info@bayforward.be</div>
</div>
""", "".join(f"tl.fromTo(P+' .L{i}',{{y:{(-900 if i % 2 else 900)},opacity:0}},{{y:0,opacity:1,duration:.55,ease:'power4.out'}},T({61.95 + i * .1:.2f}));\n" for i in range(6)) + """
tl.to(P+' .L',{x:'-=40',duration:2.3,ease:'none'},T(62.2));
tl.to(P+' .L',{scale:1.25,opacity:0,duration:.35,ease:'power2.in',stagger:.03},T(64.2));
tl.to(P+' .end',{clipPath:'circle(150% at 50% 45%)',duration:.6,ease:'power3.inOut'},T(64.3));
tl.fromTo(P+' .lock img',{scale:0,rotation:-15},{scale:1,rotation:0,duration:.6,ease:'back.out(1.8)'},T(64.55));
tl.fromTo(P+' .wm',{x:-50,opacity:0},{x:0,opacity:1,duration:.45,ease:'power3.out'},T(64.6));
""" + "".join(f"tl.fromTo(P+' .cta span:nth-child({i+1})',{{y:40,opacity:0}},{{y:0,opacity:1,duration:.35,ease:'back.out(2)'}},T({t}));\n" for i, (w, t) in enumerate(cta_words)) + """
tl.fromTo(P+' .mail',{opacity:0,y:14},{opacity:1,y:0,duration:.4},T(66.4));
tl.to(P+' .lock img',{y:-10,duration:.8,yoyo:true,repeat:1,ease:'sine.inOut'},T(66.9));
""")

# ------------------------------------------------------------------ captions (Lisa style)
CAPS = [
    ("When did someone last touch your reorder rules?", 0.06),
    ("Lead times changed, demand shifted, prices went up.", 3.15),
    ("Your min and max: still the numbers someone guessed two years ago.", 7.53),
    ("So you're overstocked on what doesn't sell and out of stock on what does.", 11.70),
    ("That's cash frozen on a shelf,", 16.65),
    ("and a customer on the phone asking where their order is.", 19.32),
    ("Meet Billie, the procurement agent from Bay Forward", 22.83),
    ("that works inside your own Odoo.", 25.98),
    ("Billie recalculates reorder point, max stock and safety stock for every product,", 27.93),
    ("based on real lead times, how often you order and what it costs.", 33.69),
    ("You decide how often Billie updates the numbers:", 38.25),
    ("daily, weekly or monthly.", 41.28),
    ("And you choose how Billie replenishes:", 43.53),
    ("economic order quantity, your supplier's minimum, or full pallets.", 46.05),
    ("Odoo runs on rules.", 50.73),
    ("Billie catches the exceptions the rules don't see.", 52.65),
    ("No implementation project.", 55.65),
    ("Install the app, and Billie gets to work.", 57.75),
    ("Curious what your reorder rules are costing you?", 61.95),
    ("Book a 20-minute stock check.", 64.68),
]
CAP_END_LAST = 67.2


def build_captions():
    groups = []
    for i, (txt, st) in enumerate(CAPS):
        en = CAPS[i + 1][1] - 0.04 if i + 1 < len(CAPS) else CAP_END_LAST
        groups.append(dict(text=txt, start=st, end=en))
    html = "".join(f'<div class="cg" id="cap-g{i}"><span>{g["text"]}</span></div>' for i, g in enumerate(groups))
    return f"""<!doctype html>
<html><head><meta charset="UTF-8" /></head><body>
<template>
<style>
{FONTS}
#captions-root{{position:absolute;inset:0;pointer-events:none;}}
#captions-root .cg{{position:absolute;left:360px;right:360px;bottom:132px;text-align:center;opacity:0;visibility:hidden;}}
#captions-root .cg span{{font-family:'Roboto';font-weight:700;font-size:42px;line-height:62px;color:#fff;background:#45494F;
  padding:3px 12px;border-radius:7px;-webkit-box-decoration-break:clone;box-decoration-break:clone;}}
</style>
<div id="captions-root" data-composition-id="captions" data-width="{W}" data-height="{H}">{html}</div>
<script>
(function(){{
var G={json.dumps([[g['start'], g['end']] for g in groups])};
var tl=gsap.timeline({{paused:true}});
G.forEach(function(g,i){{var el='#cap-g'+i;
  tl.set(el,{{opacity:1,visibility:'visible'}},g[0]);
  tl.set(el,{{opacity:0,visibility:'hidden'}},g[1]);}});
window.__timelines["captions"]=tl;
}})();
</script>
</template></body></html>
"""


# ------------------------------------------------------------------ write files
def scene_file(s):
    rid = s["id"] + "-root"
    css = (FONTS + BASE + s["css"]).replace("__RID__", rid)
    js = s["js"]
    dur = round(s["end"] - s["start"], 3)
    return f"""<!doctype html>
<html><head><meta charset="UTF-8" /></head><body>
<template>
<style>{css}</style>
<div id="{rid}" data-composition-id="{s['id']}" data-width="{W}" data-height="{H}">
{s['html']}
</div>
<script>
(function(){{
var P='#{rid}', S={s['start']};
function T(g){{return Math.max(0, +(g - S).toFixed(3));}}
var tl=gsap.timeline({{paused:true}});
{js}
window.__timelines["{s['id']}"]=tl;
}})();
</script>
</template></body></html>
"""


def main():
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    hosts = []
    for i, s in enumerate(SCENES):
        with open(os.path.join(ROOT, "compositions", s["id"] + ".html"), "w") as f:
            f.write(scene_file(s))
        dur = round(s["end"] - s["start"], 3)
        hosts.append(f'    <div id="{s["id"]}" class="clip" data-composition-id="{s["id"]}" data-composition-src="compositions/{s["id"]}.html" '
                     f'data-start="{s["start"]}" data-duration="{dur}" data-track-index="1" data-width="{W}" data-height="{H}"></div>')
    with open(os.path.join(ROOT, "compositions", "captions.html"), "w") as f:
        f.write(build_captions())
    index = f"""<!doctype html>
<html lang="en" data-resolution="landscape">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="vendor/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #DDE7F1; }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: #DDE7F1; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{TOTAL}" data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
    <div id="captions" class="clip" data-composition-id="captions" data-track-kind="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{TOTAL}" data-track-index="2" data-width="{W}" data-height="{H}"></div>
    <audio id="vo" src="assets/vo.mp3" data-start="0" data-duration="66.43" data-track-index="3" data-volume="1"></audio>
    <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="{TOTAL}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      var tl = gsap.timeline({{ paused: true }});
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(index)
    print("wrote", len(SCENES), "scenes + captions + index.html")


if __name__ == "__main__":
    main()
