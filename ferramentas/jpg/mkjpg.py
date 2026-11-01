import json,html,re,sys,subprocess,os
from tpl import render
D=json.load(open('dados.json',encoding='utf-8'))
C={c['ticker']:c for c in D['COMPANIES']}
def md(t):
    t=html.escape(t,quote=False)
    return re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',t)
def num(x,m='$'):
    s=f"{x:,.2f}".replace(',','X').replace('.',',').replace('X','.')
    return m+s
Q={'buffett':('#0b6b4d','#DDF1E6','ZONA BUFFETT — qualidade alta, preço baixo'),'vigiar':('#8a5a00','#FFF0CF','VIGIAR — qualidade alta, preço alto'),
   'armadilha':('#a35200','#FDE6CF','ARMADILHA DE VALOR — qualidade baixa, preço baixo'),'descartada':('#8b1d1d','#FADBD8','DESCARTADA (Evitar) — qualidade baixa, preço alto')}
def pcls(v): return 'g' if v in('Barata','Muito barata') else ('a' if v in('Neutra','Indeterminado') else 'r')
def make(e,outdir='out'):
    t=e['ticker'];c=C[t];m=c.get('moeda','$');am=c.get('alvoMoeda',m)
    col,bg,lab=Q[c['quadrante']]
    if t=='AXTI': lab='VIGIAR (provisória) — qualidade Razoável estimada'
    chips=['Carteira '+n for n in D['CARTEIRA'].get(t,[])]
    if c.get('tag'): chips.append(c['tag'])
    en=D['ENTRY'].get(t);sem=D['SEM'].get(t)
    ent=None
    if en:
        mm=en.get('m','$');v=en['v'];vs=(f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}").replace(',','.') if v<1000 else f"{v:,.0f}".replace(',','.')
        ent=(('≈ ' if en.get('prov') else '')+mm+vs,'provisório' if en.get('prov') else 'fixo',f"<b>{html.escape(en['base'])}</b> · {html.escape(en['val'])}")
    clq=c.get('clQ');clp=c.get('clP')
    kpi=[(('Qualidade ('+html.escape(str(c['nosQ']))+')') if clq else 'Qualidade (nossa leitura)',f"{clq}/100" if clq else html.escape(str(c['nosQ'])),''),
         ('Preço (nossa leitura)',c['nosP'],pcls(c['nosP'])),
         ('Clareza: preço',(f"{clp}/100 · {c['clPL']}" if clp else html.escape(c['clPL'])),'a' if clp else ''),
         ('Nosso DCF'+(' (conta)' if c['dcfFiavel'] else ' (não conta)'),num(c['dcf'],m) if c.get('dcf') else 'n/d',''),
         ('Alvo analistas',num(c['alvoAnalistas'],am),''),('Última análise',c['data'],'')]
    ind=[[html.escape(a),html.escape(b),f'<span class="{x["k"]}">{html.escape(x["c"])}</span>'] for a,b,x in e['ind']]
    cmp_=[[html.escape(a),html.escape(b),html.escape(x)] for a,b,x in e['cmp']]
    val=[[html.escape(a),html.escape(b),html.escape(x)] for a,b,x in e['val']]
    fontes=[[html.escape(a),html.escape(b),html.escape(x)] for a,b,x in e['fontes']]
    moat=e['moat']
    secs=[('Resultados do trimestre','p',[md(x) for x in e['resultados']]),
      ('O negócio, em poucas palavras','p',[md(e['negocio'])]),
      ('Moat (vantagem competitiva)','ul' if isinstance(moat,list) else 'p',[md(x) for x in (moat if isinstance(moat,list) else [moat])]),
      ('Indicadores-chave','t',['Indicador','Valor','Leitura'],ind),
      ('Clareza vs nossa leitura','tp',['','Clareza','Nossa leitura'],cmp_,[md(e['semdif'])]),
      ('Preço de entrada','p',[md(re.sub(r'^\*\*Preço de entrada:\*\*\s*','',e['entrada']))]) if not ent and e.get('entrada') else None,
      ('Valorização atual','t',['Item','Valor','Fonte / nota'],val),
      ('Conclusão','p',[md(x) for x in e['conclusao']]),
      ('Nota de verificação','p',[md(x) for x in e['verif']['lines']]),
      ('Fontes e datas','t',['Fonte','Utilização','Data'],fontes)]
    secs=[s for s in secs if s]
    d=dict(ticker=t,nome=('' if c['nome']==t else html.escape(c['nome'])),setor=html.escape(c['setor']),origem=html.escape(c.get('origem') or ''),chips=[html.escape(x) for x in chips],
      seal_colors=(col,bg),selo=lab,kpi=kpi,entrada=ent,semmotivo=html.escape((sem[0].upper()+sem[1:]) if sem else ''),secoes=secs,
      aviso=md(e['banner']) if e.get('banner') else None,
      rodape=('Fonte: pesquisa web (sem Raio-X) · ' if e.get('banner') else 'Fonte: Raio-X (Clareza) + verificação externa · ')+html.escape(c['data'])+' · Isto não é aconselhamento financeiro.')
    os.makedirs(outdir,exist_ok=True)
    render(d,f'{outdir}/{t}')
    print(t,'ok')
if __name__=='__main__':
    for f in sys.argv[1:]:
        for e in json.load(open(f,encoding='utf-8')): make(e)
