# Graph Report - INTEIA-laboratorio-3d  (2026-09-16)

## Corpus Check
- 126 files · ~224,832 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1009 nodes · 1423 edges · 68 communities (50 shown, 18 thin omitted)
- Extraction: 89% EXTRACTED · 11% INFERRED · 0% AMBIGUOUS · INFERRED: 153 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `e24bac2a`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Build and Catalog Scripts
- Three.js Scene Controls
- Vehicle Systems Configuration
- Blender Production Workflow
- System Optimization and Testing
- Project Documentation and Assets
- Engine Visualization Engine
- Aerodynamics Physics Model
- Build and Verification Tools
- Web Application Source
- Project Dependencies and Scripts
- Asset Provenance and Identity
- Laboratory Environment Setup
- Animation Data Merging
- Architecture and Path Mapping
- Visual Review History
- CI/CD GitHub Workflows
- Version Release History
- Contribution and Consistency
- Laboratory Data Atlas
- SVG Brand Assets
- Agent Quick Index
- Historical Evaluation Records
- Atlas Template Data
- Local Project Rules
- Legacy Engine Context
- Turbo Architecture Specs
- Technical Dossier Analysis
- 3D Modeling Guidelines
- Verifiable Knowledge Graphs
- Contracts and Responsibilities
- Asset Production Deliverables
- Verified State Modules
- Monochrome Brand Assets
- Identity Style Guide
- Official Name Branding
- Wordmark Brand Assets
- Three.js License Info
- Navigator Validation Guides
- Asset Reutilization Guide
- Integration and Portability
- Visual Identity Inventory
- Car Material Shaders
- Technical Documentation Index
- File Manifest Generation
- Script Execution Procedures
- Graph Architecture Guidance
- Driver Model Reference
- Final Assembly Verification
- Coverage and State Analysis
- Map Update Workflow
- Mapping and Discovery Guide
- Local Development Server
- Environment Setup Guide
- Publication Verification
- Driver and Helmet Models
- Wind Tunnel Visualization
- Aerodynamics Unit Testing
- Garage UI and Branding
- Studio Material Application
- Project Directory Tree
- Symbol Inventory
- build.cjs
- test-power-unit.mjs
- branding.js
- test-aerodynamics.mjs

## God Nodes (most connected - your core abstractions)
1. `Catálogo completo de arquivos` - 215 edges
2. `Índice de funções e métodos` - 44 edges
3. `sweep()` - 28 edges
4. `cube()` - 25 edges
5. `cyl()` - 23 edges
6. `W()` - 19 edges
7. `lathe()` - 16 edges
8. `loft()` - 15 edges
9. `build()` - 15 edges
10. `sphere()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `Atlas Detalhado do Laboratório (Interface)` --conceptually_related_to--> `INTEIA Escudo Oficial SVG`  [INFERRED]
  docs/mapeamento-detalhado/scripts/interface.html → web/assets/inteia-escudo-oficial.svg
- `INTEIA — Identidade Visual` --references--> `INTEIA Negativo SVG`  [INFERRED]
  identidade/Identidade-INTEIA.html → identidade/INTEIA-negativo.svg
- `INTEIA — Identidade Visual` --references--> `INTEIA Símbolo SVG`  [INFERRED]
  identidade/Identidade-INTEIA.html → identidade/INTEIA-simbolo.svg
- `build()` --calls--> `mirror_x()`  [INFERRED]
  ferramentas/sistemas/s03_suspension.py → ferramentas/sistemas/lib.py
- `build()` --calls--> `mirror_x()`  [INFERRED]
  ferramentas/sistemas/s05_brakes.py → ferramentas/sistemas/lib.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **ROSSO Iterative Evaluation Flow** — documentacao_comparacao_iluminacao, documentacao_historico_avaliacoes [EXTRACTED 1.00]
- **Laboratory Atlas Visualization Tools** — docs_mapeamento_detalhado_scripts_interface, ferramentas_mapa_template [INFERRED 0.85]
- **INTEIA Brand Identity Assets** — identidade_identidade_inteia, identidade_inteia_monocromatico, identidade_inteia_negativo, identidade_inteia_simbolo, web_assets_inteia_wordmark, web_assets_inteia_escudo_oficial, web_assets_inteia_nome_oficial [EXTRACTED 0.95]

## Communities (68 total, 18 thin omitted)

### Community 1 - "Build and Catalog Scripts"
Cohesion: 0.06
Nodes (51): bpy (dependência externa), code_paths(), family_purpose(), gather_symbols(), git(), glb_info(), inventory(), link() (+43 more)

### Community 2 - "Three.js Scene Controls"
Cohesion: 0.12
Nodes (22): three_addons_controls_orbitcontrols_js (dependência externa), three_addons_exporters_gltfexporter_js (dependência externa), three_addons_geometries_decalgeometry_js (dependência externa), three_addons_postprocessing_effectcomposer_js (dependência externa), three_addons_postprocessing_smaapass_js (dependência externa), assemblyTo(), categoryLabels, closeEngine() (+14 more)

### Community 3 - "Vehicle Systems Configuration"
Cohesion: 0.07
Nodes (33): advanceLocalSpin(), createSystems(), FLOW_SPEEDS, flowTexture(), HIDE_GROUPS, LOCAL_SPIN_AXES, SYSTEM_CATALOG, SYSTEM_IDS (+25 more)

### Community 4 - "Blender Production Workflow"
Cohesion: 0.05
Nodes (34): Blender 4.5.9 LTS na producao registrada, Colecao de estudio separada, Colecao INTEIA Carro reutilizavel, Desvincular acoes para editar posicoes, Exportar apenas carro e pivos, Raiz INTEIA_F1 e pivos, Timeline montagem rodas direcao DRS, Build web com esbuild e GLB incorporado (+26 more)

### Community 5 - "System Optimization and Testing"
Cohesion: 0.14
Nodes (13): createMechanics(), names, b, before, box, j, json, len (+5 more)

### Community 6 - "Project Documentation and Assets"
Cohesion: 0.01
Nodes (215): 00_INDICE_IA.md, AGENTS.md, ambientes/INTEIA_Box_com_carro.blend, ambientes/INTEIA-box-laboratorio.glb, ambientes/Previa-Box.png, ambientes/validacao-box.json, Catálogo completo de arquivos, CHANGELOG.md (+207 more)

### Community 7 - "Engine Visualization Engine"
Cohesion: 0.21
Nodes (15): BOKEH, clamp(), eased(), ENGINE_PARTS, ENGINE_WINDOWS, engineShot(), FOCUS, FOV (+7 more)

### Community 8 - "Aerodynamics Physics Model"
Cohesion: 0.09
Nodes (20): Bloqueios Mach montagem e isolamento, Coeficientes externos nao determinados pelo GLB, Cores de regiao sem medicao fisica, CSV com origem e validade dos parametros, Ensaio aerodinamico por coeficientes, Envelope analitico simplificado, Exemplo hipotetico sem medicao no carro, Fumaca artistica por particulas (+12 more)

### Community 9 - "Build and Verification Tools"
Cohesion: 0.12
Nodes (14): aero, after, before, built, changed, driver, engine, esbuild (+6 more)

### Community 10 - "Web Application Source"
Cohesion: 0.05
Nodes (44): ferramentas/gerar_sistemas.py, ferramentas/otimizar_sistemas.mjs, ferramentas/package_blender.py, ferramentas/sistemas/lib.py, ferramentas/sistemas/s01_aero.py, ferramentas/sistemas/s02_structure.py, ferramentas/sistemas/s03_suspension.py, ferramentas/sistemas/s04_steering.py (+36 more)

### Community 11 - "Project Dependencies and Scripts"
Cohesion: 0.11
Nodes (18): esbuild, three, author, dependencies, three, devDependencies, esbuild, engines (+10 more)

### Community 12 - "Asset Provenance and Identity"
Cohesion: 0.10
Nodes (20): Acabamento e assinatura na revisão final, Assets, produção e procedência, Assinaturas da conferência, Box e monitores, Carro Blender/GLB, Carro web, Como interpretar a evidência, Como refazer esta conferência (+12 more)

### Community 13 - "Laboratory Environment Setup"
Cohesion: 0.14
Nodes (13): Blender com box e carro estatico, Box laboratorio original ilustrativo, Demais monitores sem telemetria real, Download GLB do box com estado das telas, GLB sem reflexo pre calculado do navegador, Identidade vetorial compartilhada na interface e box, McLaren — engineering room, Azerbaijan 2023, McLaren — Japanese Grand Prix practice report, 2024 (+5 more)

### Community 14 - "Animation Data Merging"
Cohesion: 0.18
Nodes (10): b, file, fs, j, json, merged, old, out (+2 more)

### Community 15 - "Architecture and Path Mapping"
Cohesion: 0.29
Nodes (6): Caminho GLB para HTML offline, Caminho GLB para master e exports, Fontes do visualizador em web src, Master reconstruido sem pilha original do tutorial, Regeneracao sobrescreve edicoes manuais do master, Shaders e iluminacao diferem entre caminhos

### Community 16 - "Visual Review History"
Cohesion: 0.29
Nodes (6): 30 FPS observado sem garantia, Avaliacao subjetiva sem certificacao fisica, Cinco iteracoes visuais historicas do tunel, Detalhamento informativo posterior do fluxo, Pausa conferida por imagens identicas, Revisao adicional com particulas

### Community 17 - "CI/CD GitHub Workflows"
Cohesion: 0.50
Nodes (3): Build e testes web no workflow, Node 24 no workflow, Verificar site em push e pull_request

### Community 18 - "Version Release History"
Cohesion: 0.50
Nodes (3): Nenhuma CFD da geometria executada, Versao 1.0.0 laboratorio e Blender, Versao 1.1.0 tunel por coeficientes

### Community 19 - "Contribution and Consistency"
Cohesion: 0.50
Nodes (3): Capturas comparaveis para mudancas visuais, HTML regenerado deve acompanhar mudancas de codigo, Preservacao de IDs das 97 pecas

### Community 20 - "Laboratory Data Atlas"
Cohesion: 0.67
Nodes (3): Atlas Data JSON, Atlas Detalhado do Laboratório (Interface), INTEIA Escudo Oficial SVG

### Community 21 - "SVG Brand Assets"
Cohesion: 0.67
Nodes (3): INTEIA — Identidade Visual, INTEIA Negativo SVG, INTEIA Símbolo SVG

### Community 41 - "Navigator Validation Guides"
Cohesion: 0.24
Nodes (5): Acabamento, reflexos e render do laboratório, Fontes e reutilização, Limites, O que mudou, Validação do atlas no navegador

### Community 42 - "Asset Reutilization Guide"
Cohesion: 0.15
Nodes (13): 1. Levar a entrega pronta, 2. Desenvolver outra experiência a partir das fontes, 3. Importar somente um GLB em outro site, Aceitação da reutilização, Aparência e física: o que não viaja automaticamente, Blender: reutilizar sem perder a fonte, Box e carro juntos, Carro em um arquivo próprio (+5 more)

### Community 43 - "Integration and Portability"
Cohesion: 0.17
Nodes (12): 1. Abrir ou modificar o site completo, 2. Integrar somente o carro em outro site Three.js, 3. Reutilizar no Blender, 4. Reaproveitar em jogos, 5. Reconstruir os derivados sem perder edições, Dependências fixas que precisam de adaptação, Escolha do ponto de partida, Materiais e aparência (+4 more)

### Community 44 - "Visual Identity Inventory"
Cohesion: 0.15
Nodes (12): Assets visuais e identidade INTEIA, Atualização e conferência, Box com o carro, Carro em estúdio, Fontes, derivados e limites de evidência, Inventário raster e inspeção visual, Navegação, Registro da personalização (+4 more)

### Community 45 - "Car Material Shaders"
Cohesion: 0.36
Nodes (10): caliperGeometry(), discGeometry(), discTexture(), enhanceCar(), heatTexture(), localVaryings(), paintShader(), rimPatch() (+2 more)

### Community 47 - "File Manifest Generation"
Cohesion: 0.25
Nodes (7): crypto, files, fs, out, path, root, crypto (dependência externa)

### Community 48 - "Script Execution Procedures"
Cohesion: 0.09
Nodes (17): Inventário completo, Símbolos declarados, Exclusões observadas, Árvore comentada, Abrir sem disputar a porta 5186, Atualizar e reproduzir o mapeamento, Estado, concorrência e exclusões, O que os scripts realmente fazem (+9 more)

### Community 49 - "Graph Architecture Guidance"
Cohesion: 0.29
Nodes (6): Dados na sessão, Grafos, evidências e leitura estrutural, Limites de inferência, O que o graphify forneceu, Orientação de arquitetura, Produção e portabilidade

### Community 50 - "Driver Model Reference"
Cohesion: 0.25
Nodes (7): Atualização de encaixe do site principal, Piloto, capacete e bancadas — 15/09/2026, Proporção pela referência lateral enviada, Referências visuais consultadas, Resultado, Uso, Verificação

### Community 51 - "Final Assembly Verification"
Cohesion: 0.33
Nodes (5): Carro final e motor no laboratório — 15/09/2026, Limites, Operação, Procedência, Verificação

### Community 52 - "Coverage and State Analysis"
Cohesion: 0.33
Nodes (6): Cobertura, verificação e estado analisado, Estado da coleta, Exclusões justificadas, Executado nesta tarefa, Limites de cobertura, Manifesto e alterações concorrentes

### Community 53 - "Map Update Workflow"
Cohesion: 0.40
Nodes (5): Atualizar e verificar os mapas, Atualização cotidiana, Graphify complementar, Quando uma relação muda, Verificação visual e integração

### Community 54 - "Mapping and Discovery Guide"
Cohesion: 0.40
Nodes (5): Como interpretar o levantamento, Encontrar e entender, Entrega independente e concorrência, Escolher a fonte adequada, Mapeamento detalhado — Laboratório 3D INTEIA

### Community 55 - "Local Development Server"
Cohesion: 0.20
Nodes (8): node_fs (dependência externa), fs, http, mimeTypes, path, port, root, server

### Community 57 - "Environment Setup Guide"
Cohesion: 0.22
Nodes (7): Alternar entre computadores, Continuar em outro PC, Documentação, Primeira instalação, Atualizar a publicação, Publicação do laboratório, Verificação da publicação inicial

### Community 58 - "Publication Verification"
Cohesion: 0.15
Nodes (22): _encode_normal(), image_from_array(), _link(), material(), Materials, mesh_object(), mirror_x(), Paleta física compartilhada pelos 14 sistemas. (+14 more)

### Community 60 - "Driver and Helmet Models"
Cohesion: 0.24
Nodes (8): createHelmet1991(), createSennaDriver(), box, context, driver, mechanics, model, rest

### Community 61 - "Wind Tunnel Visualization"
Cohesion: 0.44
Nodes (5): three (dependência externa), aerodynamicTest(), createFlowDetail(), createTunnelVisual(), createWindTunnel()

### Community 62 - "Aerodynamics Unit Testing"
Cohesion: 0.05
Nodes (101): airfoil(), auto_explode(), bevel(), bm_to_object(), bolt_ring(), both_sides(), box_uv(), catmull() (+93 more)

### Community 63 - "Garage UI and Branding"
Cohesion: 0.38
Nodes (5): three_addons_geometries_roundedboxgeometry_js (dependência externa), createGarage(), brandSVG(), drawBrand(), glyphs

### Community 64 - "Studio Material Application"
Cohesion: 0.60
Nodes (4): applyCarMaterials(), applyLocalCarbonProjection(), setupStudio(), texture()

### Community 65 - "Project Directory Tree"
Cohesion: 0.12
Nodes (12): gltf, io, jsonLength, manifest, manifestPath, output, partsAfter, partsBefore (+4 more)

### Community 66 - "Symbol Inventory"
Cohesion: 0.18
Nodes (10): assemblies, b, before, j, json, len, mixer, out (+2 more)

### Community 71 - "build.cjs"
Cohesion: 0.18
Nodes (8): esbuild (dependência externa), esbuild, fs, html, model, path, template, withModel

### Community 72 - "test-power-unit.mjs"
Cohesion: 0.22
Nodes (5): three_addons_loaders_gltfloader_js (dependência externa), BAY, createInCarEngine(), ENGINE_AT, HINGE

### Community 77 - "branding.js"
Cohesion: 0.25
Nodes (7): Arquivos, Extras exportados nos nós, Interface, Limites, Referencial e escala, Regenerar, Sistemas internos em 3D — bancada Sistemas

### Community 78 - "test-aerodynamics.mjs"
Cohesion: 0.25
Nodes (6): node_assert_strict (dependência externa), a, b, cross, p, still

## Knowledge Gaps
- **568 isolated node(s):** `Chisle`, `Operação e desenvolvimento`, `Produto e conteúdo técnico`, `Mapas do repositório`, `Fontes de verdade` (+563 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Catálogo completo de arquivos` connect `Project Documentation and Assets` to `Script Execution Procedures`?**
  _High betweenness centrality (0.092) - this node is a cross-community bridge._
- **Why does `Índice de funções e métodos` connect `Web Application Source` to `Script Execution Procedures`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `sweep()` (e.g. with `build()` and `build()`) actually correct?**
  _`sweep()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `cube()` (e.g. with `build()` and `build()`) actually correct?**
  _`cube()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 16 inferred relationships involving `cyl()` (e.g. with `build()` and `build()`) actually correct?**
  _`cyl()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Chisle`, `Operação e desenvolvimento`, `Produto e conteúdo técnico` to the rest of the system?**
  _568 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Build and Catalog Scripts` be split into smaller, more focused modules?**
  _Cohesion score 0.058173076923076925 - nodes in this community are weakly interconnected._