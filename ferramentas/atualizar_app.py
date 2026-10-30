#!/usr/bin/env python3
"""Atualiza o index.html da app com os dados de ferramentas/dados.js.
Uso (na raiz do repositório):  python3 ferramentas/atualizar_app.py
- Lê ferramentas/dados.js (lista COMPANIES, ENTRY, SEM, CARTEIRA, DISCREP).
- Substitui em index.html o bloco entre /*DADOS_INICIO*/ e /*DADOS_FIM*/.
- Verifica a sintaxe do JavaScript e confirma contagens por separador.
Não mexe em indicadores.html nem na lógica de apresentação."""
import re, sys, subprocess, tempfile, os
d = open('ferramentas/dados.js', encoding='utf-8').read().strip()
h = open('index.html', encoding='utf-8').read()
assert '/*DADOS_INICIO*/' in h and '/*DADOS_FIM*/' in h, 'marcadores não encontrados'
assert d.startswith('/*DADOS_INICIO*/') and d.endswith('/*DADOS_FIM*/'), 'dados.js sem marcadores'
h2 = re.sub(r'/\*DADOS_INICIO\*/.*?/\*DADOS_FIM\*/', lambda m: d, h, count=1, flags=re.S)
js = h2.split('<script>\n')[1].split('</script>')[0]
with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
    f.write(js)
r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
os.unlink(f.name)
if r.returncode:
    print('ERRO de sintaxe:', r.stderr); sys.exit(1)
open('index.html', 'w', encoding='utf-8').write(h2)
print('index.html atualizado e sintaxe OK')
