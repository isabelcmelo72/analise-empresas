import sys,json,html
from playwright.sync_api import sync_playwright
CSS='''
.hd2{background:#0C2340;color:#fff;padding:16px 15px 14px}.hd2 .r1{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.hd2 .t{font-size:24px;font-weight:700}.hd2 .n{font-size:15px;margin-left:10px;color:#dbe3ef}
.chips{margin-top:8px}.chip{display:inline-block;background:#E6EBF2;color:#0C2340;font-size:10.5px;font-weight:700;padding:2px 8px;border-radius:6px;margin-right:6px}
.hd2 .s{font-size:10.5px;color:#aebbd0;margin-top:8px}
.pe{text-align:right;white-space:nowrap}.pe .l{font-size:9.5px;color:#aebbd0;text-transform:uppercase;letter-spacing:.5px}.pe .v{font-size:25px;font-weight:700;line-height:1.1}.pe .p{font-size:9.5px;color:#aebbd0}
.base{margin-top:11px;padding-top:9px;border-top:1px solid #35507a;font-size:11px;color:#c9d5e8;line-height:1.45}

*{box-sizing:border-box}body{margin:0;width:540px;background:#fff;font-family:"DejaVu Sans",Verdana,sans-serif;color:#1c2430;font-size:13.5px;line-height:1.5}
.hd{background:#0C2340;color:#fff;padding:16px 15px 13px;display:flex;justify-content:space-between;align-items:flex-start}
.hd .t{font-size:24px;font-weight:700}.hd .n{font-size:15px;margin-left:12px;color:#dbe3ef}.hd .s{font-size:10.5px;color:#aebbd0;margin-top:10px}.hd .p{font-size:20px;font-weight:700}
.seal{display:inline-block;margin:12px 15px 0;padding:7px 12px;font-weight:700;font-size:15px;border-radius:3px}
.kpi{display:grid;grid-template-columns:repeat(3,1fr);gap:10px 8px;padding:12px 15px 4px}
.kpi .l{font-size:9px;letter-spacing:.5px;color:#666;text-transform:uppercase}.kpi .v{font-size:16px;font-weight:700}
.note{padding:4px 15px 10px;font-size:10.5px;color:#8a5a00}
.sec{background:#0C2340;color:#fff;font-weight:700;font-size:14.5px;letter-spacing:.3px;padding:10px 15px;text-transform:uppercase;margin-top:6px}
.body{padding:11px 15px}.body p{margin:0 0 8px}
ul{margin:0;padding:0 0 0 2px;list-style:none}li{margin-bottom:7px;padding-left:16px;position:relative}li:before{content:"-";position:absolute;left:0;font-weight:700}
table{width:100%;border-collapse:collapse;font-size:12px;margin:0 0 4px}
th{background:#0C2340;color:#fff;text-align:left;padding:6px 8px;font-size:11.5px}td{padding:7px 8px;vertical-align:top}
tr:nth-child(even) td{background:#EFEDE6}td:first-child{font-weight:600}
.tb{padding:0 15px 8px}
.entry{margin:10px 15px 4px;background:#0C2340;color:#fff;border-radius:8px;padding:12px 14px;display:flex;gap:14px;align-items:center}
.entry .v{white-space:nowrap;font-size:28px;font-weight:700;line-height:1.1}.entry .s{font-size:10px;color:#b9c6da}.entry .b{font-size:11.5px;line-height:1.45}
.g{color:#0b6b4d}.a{color:#9a6700}.r{color:#8b1d1d}
.foot{padding:10px 15px 14px;font-size:10px;color:#666;border-top:1px solid #ddd;margin-top:8px}
'''
def tbl(head,rows,cls=None):
    h=''.join(f'<th>{x}</th>' for x in head)
    b=''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)
    return f'<div class="tb"><table><tr>{h}</tr>{b}</table></div>'
def render(d,out):
    c1,c2=d['seal_colors']
    o=f'<html><head><meta charset="utf-8"><style>{CSS}</style></head><body>'
    ch=''.join(f'<span class="chip">{x}</span>' for x in d.get('chips',[]))
    e=d.get('entrada')
    pe=f'<div class="pe"><div class="l">Preço de entrada</div><div class="v">{e[0]}</div><div class="p">{e[1]}</div></div>' if e else '<div class="pe"><div class="l">Preço de entrada</div><div class="v" style="font-size:16px">Sem preço</div></div>'
    base=f'<div class="base">{e[2]}</div>' if e else f'<div class="base">{d.get("semmotivo","")}</div>'
    o+=f'<div class="hd2"><div class="r1"><div><span class="t">{d["ticker"]}</span><span class="n">{d["nome"]}</span><div class="chips">{ch}</div><div class="s">{d["setor"]}{(" · "+d["origem"]) if d["origem"] else ""}</div></div>{pe}</div>{base}</div>'
    o+=f'<div class="seal" style="background:{c2};color:{c1}">{d["selo"]}</div>'
    o+='<div class="kpi">'+''.join(f'<div><div class="l">{l}</div><div class="v {c}">{v}</div></div>' for l,v,c in d['kpi'])+'</div>'
    if d.get('aviso'): o+=f'<div class="note">{d["aviso"]}</div>'
    for sec in d['secoes']:
        o+=f'<div class="sec">{sec[0]}</div>'
        k=sec[1]
        if k=='p': o+='<div class="body">'+''.join(f'<p>{t}</p>' for t in sec[2])+'</div>'
        elif k=='ul': o+='<div class="body"><ul>'+''.join(f'<li>{t}</li>' for t in sec[2])+'</ul></div>'
        elif k=='t': o+=tbl(sec[2],sec[3])
        elif k=='tp': o+=tbl(sec[2],sec[3])+'<div class="body">'+''.join(f'<p>{t}</p>' for t in sec[4])+'</div>'
    o+=f'<div class="foot">{d["rodape"]}</div></body></html>'
    open(out+'.html','w',encoding='utf-8').write(o)
    with sync_playwright() as p:
        b=p.chromium.launch();pg=b.new_page(viewport={'width':540,'height':800},device_scale_factor=2)
        pg.goto('file://'+__import__('os').path.abspath(out+'.html'));pg.screenshot(path=out+'.jpg',full_page=True,type='jpeg',quality=92);b.close()
