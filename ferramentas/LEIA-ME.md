# Ferramentas de atualização
- dados.js: todos os dados da app (cartões, preços de entrada, motivos, carteiras, discrepâncias). É o ficheiro que se edita a cada vaga de relatórios.
- atualizar_app.py: injeta dados.js no index.html (python3 ferramentas/atualizar_app.py).
- word/lib.js + word/data.js: gerador dos relatórios Word (NODE_PATH=$(npm root -g) node data.js), depois soffice → PDF → pdftoppm → JPG em relatorios/TICKER.jpg.
