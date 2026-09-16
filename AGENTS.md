# Regras locais — Laboratório 3D INTEIA

## Chisle

Chisle fica ativo neste projeto: resposta curta sem perder fatos decisivos e menor mudança correta depois de entender o problema.

Para código, pare no primeiro degrau suficiente: não criar; reutilizar o existente; usar biblioteca padrão; usar recurso nativo; usar dependência já instalada; resolver em uma linha; só então escrever o mínimo necessário. Não acrescente abstrações, arquivos, dependências ou explicações que o pedido não exige.

Economize contexto na origem: pesquise símbolo/caminho antes de ler, abra somente o trecho relevante, limite a saída de comandos e não releia conteúdo inalterado. Isso não autoriza reduzir validação em fronteiras de confiança, prevenção de perda de dados, segurança, acessibilidade ou requisito explícito.

Cobertura real: Claude Code usa o plugin Chisle 3.3.0 em escopo de projeto; Cursor e Copilot usam regras locais; Codex aplica este arquivo. Não atribua ao Hermes compressão de saída não verificada — nele, o repositório do Chisle declara apenas skills/comandos.

## Navegação econômica

- Comece por `00_INDICE_IA.md` e `.planning/ai/project-index.json`.
- Para perguntas sobre código, consulte primeiro `graphify query "termos" --budget 1200`; confirme fatos mutáveis nos arquivos vivos.
- O código editável do runtime está em `web/src/`. `web/index.html` é gerado por `web/build.cjs`.
- Assets grandes e binários são localizados pelos atlas em `docs/mapas/` e `docs/mapeamento-detalhado/`; não os despeje em contexto.
- Para publicar, atualizar ou mudar a audiência do Site oficial, leia `docs/PUBLICACAO.md`; reutilize o checkout irmão e o `project_id` existentes, sem criar outro Site.
- Após mudança de código, execute os testes afetados e `graphify update .`. Mudança de topologia exige regenerar `.planning/architecture/system.architecture.json` com Archify.
- Preserve trabalho concorrente e arquivos não rastreados. Confira `git status --short` antes e depois de editar.
