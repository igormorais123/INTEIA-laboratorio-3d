# Índice rápido para agentes

Use este arquivo para chegar à fonte certa sem carregar o repositório inteiro.

| Necessidade | Fonte mínima |
| --- | --- |
| Índice documental | `docs/README.md` |
| Visão do sistema | `.planning/architecture/system-architecture.html` |
| Relações de código | `graphify-out/graph.html` ou `graphify query "termos" --budget 1200` |
| Árvore navegável | `graphify-out/GRAPH_TREE.html` |
| Entrada da aplicação | `web/src/app-v2.js` |
| Interface e controles | `web/src/template-v2.html`, `web/src/customize.js` |
| Cena e materiais | `web/src/studio.js`, `web/src/car-look.js`, `web/src/surface-library.js` |
| Mecânica e sistemas | `web/src/mechanics.js`, `web/src/systems.js`, `web/src/engine/` |
| Aerodinâmica didática | `web/src/aero-physics.mjs`, `web/src/wind-tunnel.js`, `web/src/tunnel-visual.js` |
| Piloto e capacete | `web/src/senna-driver.js`, `web/src/helmet-1991.js` |
| Assets e procedência | `docs/README.md`, depois o atlas indicado para a pergunta |
| Produção dos sistemas internos | `ferramentas/gerar_sistemas.py`, `ferramentas/sistemas/sNN_<id>.py` |
| Build e execução | `web/package.json`, `web/build.cjs`, `web/server.cjs` |
| Testes | `cd web; npm test` |

Fontes de verdade: `web/src/` para o runtime; `web/assets/` para os arquivos carregados; `INTEIA_F1_Master.blend` para edição Blender. Não use `web/index.html` como fonte editável.

Limites: túnel por coeficientes não é CFD; movimentos são ilustrativos; Graphify é índice estrutural e relações inferidas precisam de confirmação na fonte.

Antes de alterar `ferramentas/gerar_sistemas.py` ou `ferramentas/sistemas/`, confira o Git e a estabilidade dos arquivos: o gerador descobre módulos dinamicamente e pode estar produzindo GLBs e prévias.
