# Atualizar e verificar os mapas

[Índice](README.md) · [Cobertura computada](cobertura.json)

## Atualização cotidiana

Na raiz do clone, com Python 3.10 ou mais recente e Git disponíveis:

```powershell
python ferramentas/mapear.py
python ferramentas/mapear.py --check
```

O primeiro comando regenera inventário JSON/Markdown, símbolos, controles, catálogo de componentes, dependências, grafos Mermaid, atlas HTML e cobertura. O segundo recompõe os resultados em memória e compara com os arquivos salvos; retorna erro se faltar arquivo, uma relação perder sua evidência, um import local não resolver, um vínculo interno quebrar, os IDs de peças divergirem ou os mapas estiverem desatualizados. `--check` não grava arquivos. A CI executa essa verificação.

O gerador [mapear.py](../../ferramentas/mapear.py) usa a biblioteca padrão Python. [mapa-template.html](../../ferramentas/mapa-template.html) é a fonte editável do atlas. Nenhum desses comandos inicia servidor, reconstrói Blender, modifica modelos, altera o manifesto das entregas ou publica o projeto.

Antes de atualizar, confira `git status --short`. Mudanças paralelas devem ser preservadas e isoladas antes de gerar um snapshot para commit. Durante esta entrega houve outra tarefa em `docs/mapeamento-detalhado/` e uma revisão simultânea de materiais, luzes e ambientes. A documentação foi iniciada em uma worktree de `1ae4fd1`, na branch `codex/mapas-inteia`, e atualizada sobre `e3d58af` (incluindo materiais/luzes de `0346e58` e a assinatura lateral) após a conclusão dos materiais/luzes. Ao integrar outras linhas de trabalho, regenere os mapas sobre o código integrado e reveja as descrições humanas.

O escopo é a união dos arquivos rastreados por Git com novos arquivos não ignorados. Uma exceção explícita preserva a pasta concorrente `docs/mapeamento-detalhado/` enquanto não versionada; se for adicionada ao Git, entra automaticamente. Caches/dependências instaladas/backups ignorados ficam fora. Em `graphify-out`, apenas JSON, HTML e relatório finais entram. Não adicione exportações temporárias ao commit por um `git add .` indiscriminado.

## Quando uma relação muda

Imports JavaScript e CommonJS literais são extraídos automaticamente. A tabela `production_edges` no gerador descreve etapas adicionais de produção; cada relação exige um trecho real no arquivo de evidência. Ao mudar uma ferramenta ou uma saída, atualize essa tabela e confira o trecho de origem. Não adicione uma aresta só porque dois arquivos têm nomes parecidos.

Funções, classes e constantes exportadas são um índice lexical. Callbacks anônimos, resolução de tipos, chamadas dinâmicas, CSS e IDs concatenados não têm cobertura exaustiva. Os controles são todos os IDs do template e suas referências literais. A existência de um arquivo ou ID não comprova execução. O grafo de importação da aplicação parte exclusivamente de `app-v2.js`.

O inventário lê JSON incorporado nos quatro GLBs e compara o conjunto de `partId` do modelo base com o documento de procedência. Números de triângulos são calculados a partir dos accessors de primitivas triangulares. Não abre `.blend`, não reimporta em motores de jogos e não faz avaliação física. A cobertura de arquivos não representa cobertura de testes nem de todas as relações possíveis.

Textos têm bytes e SHA-256 calculados após normalizar CRLF para LF; binários usam os bytes exatos. Os mapas gerados não contêm hashes deles próprios, evitando dependência circular. O fingerprint deriva da lista e dos hashes das fontes e entregas. O relatório de cobertura informa os critérios; não contém porcentagem inventada de compreensão do código.

## Graphify complementar

[graphify-out/graph.json](../../graphify-out/graph.json), [HTML](../../graphify-out/graph.html) e [relatório](../../graphify-out/GRAPH_REPORT.md) são um snapshot estrutural/semântico separado, ancorado na revisão de origem `1ae4fd1`. Os documentos novos deste atlas estão no inventário principal; não foram retroativamente tratados como documentos existentes nessa revisão.

Para refazer a análise, use a skill `graphify` sobre o clone integrado. Ela faz detecção, extração estrutural e leitura semântica dos documentos/imagens, registra `EXTRACTED`, `INFERRED` e `AMBIGUOUS`, diagnostica integridade e gera comunidades/HTML/JSON. Na extração Python pelo Windows, use `extract(..., parallel=False)` ou um script com proteção `if __name__ == '__main__'`; a chamada paralela por stdin pode falhar e recorrer à extração sequencial. Dependências de runtime do graphify são opcionais para o atlas principal.

`graphify update .` pode atualizar a parte estrutural, mas não substitui nova leitura das imagens/documentos e revisão dos vínculos semânticos. Confira fontes, linhas, revisão, classificação das arestas e diagnóstico antes de substituir o snapshot. Não use `--force` para contornar uma redução de nós sem investigar. Os arquivos brutos da extração ficam em [graphify-extracao.json](graphify-extracao.json), preservando inclusive relações múltiplas que o grafo simples possa resumir.

## Verificação visual e integração

Abra `docs/mapas/index.html` offline ou sirva a raiz do clone em uma porta livre. Confira as seis visões, pesquisa sem acentos, filtros, estados sem resultados, teclado, links, histórico de navegação e largura estreita. Os grafos têm rolagem horizontal própria e tabela equivalente acessível. A busca filtra a tabela de relações; o diagrama mantém o contexto completo.

Para alterações na aplicação, execute separadamente:

```powershell
npm --prefix web ci
npm --prefix web run build
npm --prefix web test
python ferramentas/mapear.py
python ferramentas/mapear.py --check
```

Os testes de mecânica gravam `validacao-mecanica-web.json` e o build gera `web/index.html`: confira os diffs antes de versionar. Não rode os exportadores Blender nem o gerador do manifesto por mera atualização de documentação. Revise e selecione apenas os arquivos do trabalho autorizado.
