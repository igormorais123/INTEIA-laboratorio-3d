# Publicação do laboratório

- [Laboratório público](https://igormorais123.github.io/INTEIA-laboratorio-3d/)
- [Repositório público](https://github.com/igormorais123/INTEIA-laboratorio-3d)
- [Atlas detalhado](https://igormorais123.github.io/INTEIA-laboratorio-3d/docs/mapeamento-detalhado/index.html)
- [Atlas de arquivos e peças](https://igormorais123.github.io/INTEIA-laboratorio-3d/docs/mapas/index.html)

O GitHub Pages serve a raiz da branch `main`, com HTTPS. O [index.html da raiz](../index.html) encaminha ao [laboratório em web/](../web/index.html). O arquivo [.nojekyll](../.nojekyll) permite servir os arquivos estáticos já construídos, preservando os caminhos e dispensando a compilação Jekyll. O HTML inclui o modelo e o código necessários para executar a cena.

## Atualizar a publicação

1. Confira o estado do Git e preserve trabalho concorrente.
2. Após mudanças na aplicação, execute `npm ci` e `npm run build` dentro de `web`. O build atualiza `web/index.html`.
3. Na raiz, execute `node ferramentas/manifest.cjs` se alguma entrega do manifesto mudou. Confira o diff das entregas.
4. Execute `node docs/mapeamento-detalhado/scripts/verificar-app.mjs` para verificar o build e os testes mecânicos e aerodinâmicos sem substituir os relatórios originais.
5. Atualize os mapas com a sequência abaixo. Use um Python com `tree-sitter` e `tree-sitter-javascript` para a extração detalhada; veja [pré-requisitos](mapeamento-detalhado/ATUALIZAR.md).

```sh
python ferramentas/mapear.py
python docs/mapeamento-detalhado/scripts/gerar.py
python ferramentas/mapear.py
python docs/mapeamento-detalhado/scripts/gerar.py
python docs/mapeamento-detalhado/scripts/validar.py
python ferramentas/mapear.py --check
```

As duas passagens acomodam referências entre os inventários. As saídas geradas do atlas detalhado são inventariadas sem hash pelo primeiro mapa, evitando uma dependência circular. Os documentos editoriais e scripts continuam sujeitos à comparação de hashes.

6. Revise o diff, faça commit dos arquivos da alteração e envie à branch `main`, diretamente ou por pull request com merge.
7. Aguarde o status `built` em Settings > Pages. Abra o endereço público e confira carregamento do modelo, controles e os atlas.

## Verificação da publicação inicial

Em 13 de setembro de 2026 (UTC), o GitHub Pages confirmou a publicação da revisão `e8a7e7a44d17d5695df2e982390e372054647213`, após a integração do [PR 1](https://github.com/igormorais123/INTEIA-laboratorio-3d/pull/1). O endereço público abriu no navegador com o estado “ESTÚDIO PRONTO” e 97 componentes disponíveis.

O workflow de verificação do GitHub Actions não iniciou devido ao bloqueio de cobrança da conta informado pelo GitHub. A publicação estática do Pages funcionou. A validação local permanece registrada em [verificacao-app.json](mapeamento-detalhado/dados/verificacao-app.json); o bloqueio do Actions não equivale a testes aprovados remotamente.
