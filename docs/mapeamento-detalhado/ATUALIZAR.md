# Atualizar e reproduzir o mapeamento

[Índice](README.md) · [Validação](VALIDACAO.md)

Execute os comandos desta página **na raiz de `INTEIA-laboratorio-3d`**. Os três scripts próprios gravam somente nesta documentação. Eles não iniciam o servidor da aplicação, não convertem assets, não alteram banco de dados e não fazem commit/push.

## Pré-requisitos

Python 3.12 ou mais recente para inventário/validação; `tree-sitter` e `tree-sitter-javascript` para recalcular símbolos JavaScript; Node e dependências de `web/package-lock.json` instaladas para verificar build/testes. Na coleta, foi usado o Python do ambiente já existente do graphify 0.9.41 para a geração. O [relatório de testes](dados/verificacao-app.json) registra as versões efetivas de Node/Three.js/esbuild.

O ambiente do graphify pode ser usado sem instalar dependências no aplicativo:

```powershell
uv tool run --from graphifyy python docs/mapeamento-detalhado/scripts/gerar.py
```

`uv tool run` pode baixar uma ferramenta se ela não estiver instalada; confira a versão quando desejar reproduzir exatamente a mesma extração. Alternativamente, use um Python que já tenha `tree-sitter` e `tree-sitter-javascript`. Com Python sem esses pacotes, o gerador só reutiliza o índice existente se todos os hashes dos fontes desse índice conferirem; caso contrário, interrompe e explica a dependência ausente.

## Sequência de atualização

Após a integração dos dois atlas, siga a [sequência completa de publicação](../PUBLICACAO.md#atualizar-a-publicação) para atualizar também `docs/mapas`. As duas passagens estabilizam as referências entre os inventários; o mapa principal omite hashes dos derivados detalhados para evitar ciclos.

1. Leia `git status --short --branch`, `git log -1` e as instruções locais aplicáveis. Identifique mudanças concorrentes; não use `reset`, `clean`, staging global ou substituição de arquivos alheios. Confira se o mapeamento deve refletir o HEAD ou também mudanças locais.
2. Revise [finalidades.json](scripts/finalidades.json) para novas fontes. Arquivos adicionais não reconhecidos aparecem como **não classificados** e fazem a validação falhar. `docs/mapas` e suas ferramentas são identificados separadamente como produção paralela.
3. Atualize as páginas editoriais quando contratos, exportações ou limitações mudarem. Revise [relacoes-curadas.json](dados/relacoes-curadas.json), com `source`, `target`, `relation`, confiança, caminho/linha e trecho de evidência reais. Preserve relações incertas como `INFERRED`/`AMBIGUOUS`; não converta suposições em fatos.
4. Gere os derivados:

```powershell
python docs/mapeamento-detalhado/scripts/gerar.py
```

5. Verifique o aplicativo com saídas isoladas:

```powershell
node docs/mapeamento-detalhado/scripts/verificar-app.mjs
```

6. Valide a documentação:

```powershell
python docs/mapeamento-detalhado/scripts/validar.py
```

7. Abra [index.html](index.html), busque um arquivo, uma peça e uma função, navegue pelas relações, use o teclado, redimensione a janela e confira voltar/avançar. Se a estrutura da interface mudar, atualize a evidência de validação do navegador. O validador estrutural não substitui esse exame.
8. Confira o diff e o relatório `dados/validacao.json`. Commit/push só devem abranger arquivos próprios e autorizados. Não há publicação automática embutida no gerador.

## O que os scripts realmente fazem

| Script | Leitura | Escrita e limites |
|---|---|---|
| [gerar.py](scripts/gerar.py) | Inventário real, bytes/hashes, JSON GLB, metadados, importações, símbolos e relações curadas | Catálogo MD/CSV/JSON, árvore, funções, grafos Mermaid/JSON e HTML neste diretório. Não extrai código de dependências nem segue worktrees/junções. |
| [verificar-app.mjs](scripts/verificar-app.mjs) | Fontes web, esbuild, testes existentes e base GLB | Build em memória (`write:false`), teste mecânico com importações e destino do relatório adaptados em memória, teste aerodinâmico original. Grava somente relatórios em `dados/`. Compara hashes antes/depois. |
| [validar.py](scripts/validar.py) | Links locais e âncoras Markdown, JSON, arquivos, símbolos, evidências, hashes e manifestos | `dados/validacao.json` e `dados/entrega.json`. Retorno diferente de zero em referências inválidas, dados desatualizados ou cobertura incompleta. |

O teste mecânico do repositório original grava `validacao-mecanica-web.json` na raiz. O adaptador conserva as asserções e desvia só os caminhos de importação/leitura e a saída; a fonte original não é alterada. O build original grava `web/index.html`: o adaptador reproduz a composição em memória e apenas compara os bytes.

## Estado, concorrência e exclusões

[estado-inicial.json](dados/estado-inicial.json) é o marco inicial desta tarefa e não é sobrescrito pelo gerador. `dados/cobertura.json` registra cada coleta posterior, revisão, status e exclusões. `dados/catalogo.json` preserva hash/tamanho por arquivo. `dados/entrega.json` lista esta documentação separadamente, excluindo seu próprio arquivo e caches para evitar autorreferência.

Git, `node_modules`, caches graphify/Python, backups, arquivos de ambiente, links/junções e checkouts aninhados são excluídos com motivo explícito. Arquivos de aplicação presentes no inventário inicial devem continuar cobertos. Em uma alteração deliberada do inventário-base, revise o marco inicial em uma nova tarefa/versão e documente a mudança; não apague silenciosamente evidências anteriores.

Se algum arquivo mudar depois da geração, a comparação de hashes falha. Gere novamente e revise as páginas afetadas. Os scripts não atualizam automaticamente a interpretação humana de mudanças semânticas.

## Reproduzir o diagnóstico graphify isolado

O resultado bruto desta tarefa é histórico. Para renová-lo, use as APIs `detect` e `extract` da versão registrada; passe `root` como a raiz do repositório e `cache_root` como `docs/mapeamento-detalhado`. Isso direciona o cache a `docs/mapeamento-detalhado/graphify-out`, sem tocar o grafo da outra conversa. Selecione explicitamente os fontes da aplicação e ferramentas; não inclua o próprio mapa nem uma cópia de worktree. Execute `diagnose_extraction` antes de interpretar os vínculos.

O diagnóstico original está em [graphify-execucao.json](dados/graphify-execucao.json). Este fluxo de atualização principal não depende desse AST histórico e não o apresenta como reextraído. A skill e o ambiente de graphify são ferramentas da estação de trabalho, não dependências de execução do laboratório.

## Abrir sem disputar a porta 5186

A forma mais simples é abrir o HTML do atlas localmente. Se for necessário servir por HTTP, use uma porta livre em `127.0.0.1` com a raiz deste repositório como diretório servido. Não execute `npm run dev` no valor padrão enquanto 5186 estiver ocupada pela conversa original. Não mate processos para liberar essa porta.
