# Contribuir

Leia o [índice da documentação](docs/README.md), a [arquitetura](docs/ARQUITETURA.md) e o [guia de desenvolvimento](docs/DESENVOLVIMENTO.md). Preserve IDs das 97 peças quando os controles dependerem deles e não substitua geometria, mapas ou metadados sem registrar origem e impacto.

Antes de propor uma mudança:

1. Execute `npm --prefix web test` e `npm --prefix web run build`.
2. Execute `python ferramentas/mapear.py` e `python ferramentas/mapear.py --check`.
3. Confira `git diff --check` e separe fontes editáveis de saídas geradas.
4. Em mudanças visuais, registre capturas comparáveis; em mudanças Blender/GLB, registre peças, triângulos, tamanho e validação de reabertura.

Descreva comportamento anterior e novo, arquivos afetados, testes executados e limitações não verificadas. Não inclua credenciais, logs pessoais, `node_modules`, caches, backups do Blender ou arquivos cuja origem/licença não possa ser descrita. Mudanças em `web/src/` devem incluir `web/index.html` regenerado.
