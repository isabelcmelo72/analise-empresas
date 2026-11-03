# Ferramentas de atualização
- dados.js: todos os dados da app (cartões, preços de entrada, motivos, carteiras, discrepâncias). É o ficheiro que se edita a cada vaga de relatórios.
- atualizar_app.py: injeta dados.js no index.html (python3 ferramentas/atualizar_app.py).
- word/lib.js + word/data.js: gerador dos relatórios Word (NODE_PATH=$(npm root -g) node data.js), depois soffice → PDF → pdftoppm → JPG em relatorios/TICKER.jpg.

- jpg/: gerador dos JPG de análise completa (formato Coca-Cola, 1080 px). Correr dentro de ferramentas/jpg: `python3 exportar_dados.py` (cria dados.json a partir do dados.js) e `python3 mkjpg.py ficheiro.json` (ent11.json, ent2.json, googl.json e rui.json são exemplos de conteúdo). Os JPG saem em jpg/out/; copiar para relatorios/TICKER.jpg. Os Word (word/) estão em stand-by.
- Botão "Copiar para o Radar" (separador Preços de entrada): usa a lista RADAR do dados.js (ticker Yahoo, nome, subsetor, notas); qualidade, preço, data e zona vêm das empresas. Separador "Falta o Raio-X": lista PENDENTE do dados.js. Novo ticker = acrescentar nas duas.
