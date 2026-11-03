# Exporta COMPANIES/ENTRY/SEM/CARTEIRA de ../dados.js para dados.json (lido pelo mkjpg.py)
import json,subprocess,os
here=os.path.dirname(os.path.abspath(__file__))
src=open(os.path.join(here,'..','dados.js'),encoding='utf-8').read()+"\nconsole.log(JSON.stringify({COMPANIES,ENTRY,SEM,CARTEIRA}))"
tmp=os.path.join(here,'_x.js'); open(tmp,'w',encoding='utf-8').write(src)
out=subprocess.check_output(['node',tmp]); os.remove(tmp)
open(os.path.join(here,'dados.json'),'wb').write(out); print('dados.json atualizado')
