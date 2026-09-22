# Graph Report - INTEIA-laboratorio-3d  (2026-09-22)

## Corpus Check
- 189 files · ~312,422 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1524 nodes · 2449 edges · 114 communities (93 shown, 21 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 175 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f5ccca58`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- docs/INTEGRACAO.md
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
- mapeamento-detalhado/README.md
- Environment Setup Guide
- Publication Verification
- cube
- Driver and Helmet Models
- Wind Tunnel Visualization
- Aerodynamics Unit Testing
- Garage UI and Branding
- Studio Material Application
- Project Directory Tree
- Symbol Inventory
- loft
- in-car.js
- Documentação do Laboratório 3D INTEIA
- Publicação do laboratório
- build.cjs
- test-power-unit.mjs
- gerar_sistemas.py
- build.cjs
- test-power-unit.mjs
- docs/INTEGRACAO.md
- branding.js
- Publicação oficial do laboratório
- ARVORE.md
- gerar_v12.py
- render_loop
- test-rpm-curve.mjs
- gerar_sobressalentes.py
- test-sound-studio.mjs
- Estúdio de som — bancos calibrados do V12 anos 90 e do V6 2026
- Plano 2 — Bancos de loops calibrados (V12 e V6)
- gerar_sistemas.py
- build.cjs
- Mapa de arquivos
- sound-studio.js
- engine-voice.mjs
- test-power-unit.mjs
- Estúdio de som V6 × V12 — passagem de trabalho (comece por aqui)
- docs/INTEGRACAO.md
- test_analise.py
- docs/DESENVOLVIMENTO.md
- server.cjs
- docs/BLENDER.md
- Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução
- node_fs (dependência externa)
- parts-info.js
- docs/VALIDACAO.md
- Peças sobressalentes do Box — configuração de pista
- Publicação oficial do laboratório
- main
- Estúdio de som — pesquisa de 16 e 17/09/2026
- diagnostico_analise.py
- Context
- face_uv_fit
- W_rot
- node_fs (dependência externa)
- face_uv_fit
- W_rot

## God Nodes (most connected - your core abstractions)
1. `Catálogo completo de arquivos` - 237 edges
2. `Índice de funções e métodos` - 48 edges
3. `sweep()` - 28 edges
4. `cube()` - 25 edges
5. `W()` - 24 edges
6. `cyl()` - 23 edges
7. `render_loop()` - 21 edges
8. `loft()` - 16 edges
9. `lathe()` - 16 edges
10. `analyse_signal()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `Atlas Detalhado do Laboratório (Interface)` --conceptually_related_to--> `INTEIA Escudo Oficial SVG`  [INFERRED]
  docs/mapeamento-detalhado/scripts/interface.html → web/assets/inteia-escudo-oficial.svg
- `createSystems()` --indirect_call--> `load()`  [INFERRED]
  web/src/systems.js → ferramentas/otimizar_sistemas.mjs
- `createTestBank()` --indirect_call--> `load()`  [INFERRED]
  web/test-fixtures/sound-bank.mjs → ferramentas/otimizar_sistemas.mjs
- `renderVoice()` --calls--> `createEngineVoice()`  [EXTRACTED]
  ferramentas/som/renderizar_demos.mjs → web/src/sound/engine-voice.mjs
- `span_loft()` --calls--> `loft()`  [INFERRED]
  ferramentas/gerar_sobressalentes.py → ferramentas/sistemas/lib.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **ROSSO Iterative Evaluation Flow** — documentacao_comparacao_iluminacao, documentacao_historico_avaliacoes [EXTRACTED 1.00]
- **Laboratory Atlas Visualization Tools** — docs_mapeamento_detalhado_scripts_interface, ferramentas_mapa_template [INFERRED 0.85]
- **INTEIA Brand Identity Assets** — identidade_identidade_inteia, identidade_inteia_monocromatico, identidade_inteia_negativo, identidade_inteia_simbolo, web_assets_inteia_wordmark, web_assets_inteia_escudo_oficial, web_assets_inteia_nome_oficial [EXTRACTED 0.95]

## Communities (114 total, 21 thin omitted)

### Community 0 - "docs/INTEGRACAO.md"
Cohesion: 0.25
Nodes (8): bbox_web(), auto_explode(), car_components(), centroid(), Preenche o extra `explode` das peças sem valor: direção do centroide do sistema, Importa o carro v2 uma única vez e devolve os componentes soltos (ilhas de malha, to_web(), bbox_web()

### Community 1 - "Build and Catalog Scripts"
Cohesion: 0.12
Nodes (29): code_paths(), family_purpose(), gather_symbols(), git(), glb_info(), inventory(), link(), main() (+21 more)

### Community 2 - "Three.js Scene Controls"
Cohesion: 0.09
Nodes (27): load(), three_addons_controls_orbitcontrols_js (dependência externa), three_addons_exporters_gltfexporter_js (dependência externa), three_addons_geometries_decalgeometry_js (dependência externa), three_addons_postprocessing_effectcomposer_js (dependência externa), three_addons_postprocessing_smaapass_js (dependência externa), assemblyTo(), categoryLabels (+19 more)

### Community 3 - "Vehicle Systems Configuration"
Cohesion: 0.06
Nodes (39): CAR_CATEGORY_FALLBACK, CAR_RULES, describeCarPart(), describePart(), RULES, SYSTEM_FALLBACK, advanceLocalSpin(), createSystems() (+31 more)

### Community 4 - "Blender Production Workflow"
Cohesion: 0.15
Nodes (11): Licenca do tutorial nao documentada, Original do tutorial ausente, Sem afiliacao ou certificacao esportiva, Titularidade declarada INTEIA, Tutorial F1_2026_tutorial_part7_textures.blend, Direitos de terceiros preservados, Licenca Proprietaria INTEIA, Reutilizacao depende de autorizacao INTEIA (+3 more)

### Community 5 - "System Optimization and Testing"
Cohesion: 0.14
Nodes (13): createMechanics(), names, b, before, box, j, json, len (+5 more)

### Community 6 - "Project Documentation and Assets"
Cohesion: 0.01
Nodes (237): 00_INDICE_IA.md, AGENTS.md, ambientes/INTEIA_Box_com_carro.blend, ambientes/INTEIA-box-laboratorio.glb, ambientes/Previa-Box.png, ambientes/validacao-box.json, Catálogo completo de arquivos, CHANGELOG.md (+229 more)

### Community 7 - "Engine Visualization Engine"
Cohesion: 0.21
Nodes (15): BOKEH, clamp(), eased(), ENGINE_PARTS, ENGINE_WINDOWS, engineShot(), FOCUS, FOV (+7 more)

### Community 8 - "Aerodynamics Physics Model"
Cohesion: 0.13
Nodes (14): Bloqueios Mach montagem e isolamento, Coeficientes externos nao determinados pelo GLB, Cores de regiao sem medicao fisica, CSV com origem e validade dos parametros, Ensaio aerodinamico por coeficientes, Envelope analitico simplificado, Exemplo hipotetico sem medicao no carro, Fumaca artistica por particulas (+6 more)

### Community 9 - "Build and Verification Tools"
Cohesion: 0.12
Nodes (14): aero, after, before, built, changed, driver, engine, esbuild (+6 more)

### Community 10 - "Web Application Source"
Cohesion: 0.04
Nodes (48): ferramentas/gerar_sistemas.py, ferramentas/gerar_sobressalentes.py, ferramentas/otimizar_sistemas.mjs, ferramentas/package_blender.py, ferramentas/sistemas/lib.py, ferramentas/sistemas/s01_aero.py, ferramentas/sistemas/s02_structure.py, ferramentas/sistemas/s03_suspension.py (+40 more)

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
Cohesion: 0.06
Nodes (57): bank_points(), calibration_bands(), distance(), fit_eq(), harmonic_orders(), loop_cycles(), main(), measure_loop() (+49 more)

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
Cohesion: 0.33
Nodes (4): Acabamento, reflexos e render do laboratório, Fontes e reutilização, Limites, O que mudou

### Community 42 - "Asset Reutilization Guide"
Cohesion: 0.15
Nodes (13): 1. Levar a entrega pronta, 2. Desenvolver outra experiência a partir das fontes, 3. Importar somente um GLB em outro site, Aceitação da reutilização, Aparência e física: o que não viaja automaticamente, Blender: reutilizar sem perder a fonte, Box e carro juntos, Carro em um arquivo próprio (+5 more)

### Community 43 - "Integration and Portability"
Cohesion: 0.17
Nodes (12): 1. Abrir ou modificar o site completo, 2. Integrar somente o carro em outro site Three.js, 3. Reutilizar no Blender, 4. Reaproveitar em jogos, 5. Reconstruir os derivados sem perder edições, Dependências fixas que precisam de adaptação, Escolha do ponto de partida, Materiais e aparência (+4 more)

### Community 44 - "Visual Identity Inventory"
Cohesion: 0.17
Nodes (12): Assets visuais e identidade INTEIA, Atualização e conferência, Box com o carro, Carro em estúdio, Fontes, derivados e limites de evidência, Inventário raster e inspeção visual, Navegação, Registro da personalização (+4 more)

### Community 45 - "Car Material Shaders"
Cohesion: 0.36
Nodes (10): caliperGeometry(), discGeometry(), discTexture(), enhanceCar(), heatTexture(), localVaryings(), paintShader(), rimPatch() (+2 more)

### Community 46 - "Technical Documentation Index"
Cohesion: 0.26
Nodes (3): Mapa do Laboratório 3D INTEIA, Evidências de verificação do atlas, Chisle

### Community 47 - "File Manifest Generation"
Cohesion: 0.25
Nodes (7): crypto, files, fs, out, path, root, crypto (dependência externa)

### Community 48 - "Script Execution Procedures"
Cohesion: 0.29
Nodes (7): Abrir sem disputar a porta 5186, Atualizar e reproduzir o mapeamento, Estado, concorrência e exclusões, O que os scripts realmente fazem, Pré-requisitos, Reproduzir o diagnóstico graphify isolado, Sequência de atualização

### Community 49 - "Graph Architecture Guidance"
Cohesion: 0.29
Nodes (6): Dados na sessão, Grafos, evidências e leitura estrutural, Limites de inferência, O que o graphify forneceu, Orientação de arquitetura, Produção e portabilidade

### Community 50 - "Driver Model Reference"
Cohesion: 0.29
Nodes (7): Atualização de encaixe do site principal, Piloto, capacete e bancadas — 15/09/2026, Proporção pela referência lateral enviada, Referências visuais consultadas, Resultado, Uso, Verificação

### Community 51 - "Final Assembly Verification"
Cohesion: 0.40
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
Cohesion: 0.16
Nodes (33): bm_to_object(), bolt_ring(), box_uv(), car_part(), gear(), helix(), lathe(), loft() (+25 more)

### Community 56 - "mapeamento-detalhado/README.md"
Cohesion: 0.24
Nodes (3): Exclusões observadas, Árvore comentada, Validação do atlas no navegador

### Community 57 - "Environment Setup Guide"
Cohesion: 0.50
Nodes (4): Alternar entre computadores, Continuar em outro PC, Documentação, Primeira instalação

### Community 58 - "Publication Verification"
Cohesion: 0.10
Nodes (37): arc2d(), both_sides(), _encode_normal(), _frames(), image_from_array(), join(), _link(), material() (+29 more)

### Community 59 - "cube"
Cohesion: 0.19
Nodes (11): super_ellipse(), 02 · Estrutura central: célula de sobrevivência em sanduíche de carbono e colmei, tub_section(), add(), bank_frame(), build(), 06 · Unidade de potência térmica: V6 de 90° com bloco, cárter seco, cabeçotes e, Eixo do cilindro (para cima e para fora) e normal externa da bancada. (+3 more)

### Community 60 - "Driver and Helmet Models"
Cohesion: 0.24
Nodes (8): createHelmet1991(), createSennaDriver(), box, context, driver, mechanics, model, rest

### Community 61 - "Wind Tunnel Visualization"
Cohesion: 0.20
Nodes (10): three (dependência externa), aerodynamicTest(), createFlowDetail(), createTunnelVisual(), createWindTunnel(), a, b, cross (+2 more)

### Community 62 - "Aerodynamics Unit Testing"
Cohesion: 0.24
Nodes (11): airfoil(), Seção tipo NACA simétrica (com leve arqueamento) para braços de suspensão e asas, build(), center_elements(), corner(), leg(), 03 · Suspensão: wishbones em perfil aerodinâmico, uprights usinados, pushrod dia, Elemento heave com pilha Belleville e barra antirrolagem entre os dois balancins (+3 more)

### Community 63 - "Garage UI and Branding"
Cohesion: 0.38
Nodes (5): three_addons_geometries_roundedboxgeometry_js (dependência externa), createGarage(), brandSVG(), drawBrand(), glyphs

### Community 64 - "Studio Material Application"
Cohesion: 0.60
Nodes (4): applyCarMaterials(), applyLocalCarbonProjection(), setupStudio(), texture()

### Community 65 - "Project Directory Tree"
Cohesion: 0.13
Nodes (12): gltf, io, jsonLength, manifest, manifestPath, output, partsAfter, partsBefore (+4 more)

### Community 66 - "Symbol Inventory"
Cohesion: 0.15
Nodes (26): bevel(), catmull(), cube(), cyl(), flow_ribbon(), lado(), plate(), Placa extrudada a partir de um contorno 2D [(u,v)] no plano definido por `normal (+18 more)

### Community 67 - "loft"
Cohesion: 0.14
Nodes (15): node_assert_strict (dependência externa), cylinderAt(), ENGINE_PROFILES, firingIntervalDeg(), firingWindowAt(), createPhasePlayer(), prepareBank(), detectFiringHz() (+7 more)

### Community 68 - "in-car.js"
Cohesion: 0.25
Nodes (4): BAY, createInCarEngine(), ENGINE_AT, HINGE

### Community 69 - "Documentação do Laboratório 3D INTEIA"
Cohesion: 0.40
Nodes (5): Documentação do Laboratório 3D INTEIA, Fontes de verdade, Mapas do repositório, Operação e desenvolvimento, Produto e conteúdo técnico

### Community 70 - "Publicação do laboratório"
Cohesion: 0.12
Nodes (26): crankRotationZ(), pinAngleDeg(), pinPosition(), pistonDistance(), poseV12(), rodRotationZ(), strokeOf(), wristPosition() (+18 more)

### Community 71 - "build.cjs"
Cohesion: 0.15
Nodes (17): addPoint(), clamp(), mountCurveEditor(), movePoint(), nudgePoint(), removePoint(), capped, curve (+9 more)

### Community 72 - "test-power-unit.mjs"
Cohesion: 0.10
Nodes (12): 01 · Aerodinâmica: o que a carroceria esconde — túneis venturi do assoalho, cerc, 04 · Direção: coluna em carbono com juntas universais, pinhão e cremalheira hidr, arc(), 05 · Freios: discos carbono-carbono, campânulas, pinças monobloco, tambores de r, Pontos no plano da roda: ângulo medido de +Z (frente) para +Y (cima), em graus., 07 · ERS híbrido: energy store sob o tanque (módulos de células, barramentos, co, 10 · Câmbio e diferencial: carcaça estrutural com janela de corte, embreagem mul, rr_section() (+4 more)

### Community 74 - "build.cjs"
Cohesion: 0.13
Nodes (23): axis_deg(), axis_vec(), bank_of(), corte(), index_in_bank(), marcar(), origem_em(), pin_offset_deg() (+15 more)

### Community 75 - "test-power-unit.mjs"
Cohesion: 0.16
Nodes (20): analyse_signal(), crank_candidates(), engine_orders(), _interp_rows(), measure_frame(), noise_floor(), order_level(), ndarray (+12 more)

### Community 76 - "docs/INTEGRACAO.md"
Cohesion: 0.15
Nodes (17): clamp(), createRpmFollower(), DURATION_RANGE_S, evaluateCurve(), simulateCurve(), tangents(), first, follower (+9 more)

### Community 77 - "branding.js"
Cohesion: 0.22
Nodes (9): Arquivos, Extras exportados nos nós, Interface, Leitura de cada sistema, Limites, Publicação, Referencial e escala, Regenerar (+1 more)

### Community 78 - "Publicação oficial do laboratório"
Cohesion: 0.39
Nodes (9): describeTuning(), noteGrid(), PAD, firingHz(), hzToNote(), midiToHz(), NOTE_NAMES, rpmForHz() (+1 more)

### Community 79 - "ARVORE.md"
Cohesion: 0.12
Nodes (17): 1. Referências reais (só para análise), 2. Modelo físico offline e banco de loops, 3. Reprodução com fase travada (`phase-player.mjs`), 4. Curva de aceleração (`rpm-curve.mjs` + `curve-editor.js`), 5. Motor V12 3D (`v12-v1.glb`), 6. Aba 07 Som (`sound-studio.js`), Afinação, Arquitetura (+9 more)

### Community 80 - "gerar_v12.py"
Cohesion: 0.22
Nodes (11): decode_reference(), load_cached(), main(), ndarray, Path, Decodifica as referências de .referencias/ para o cache de análise.  Cada referê, Mistura para mono e reamostra para 48 kHz com FIR polifásico (fase linear)., sha256_of() (+3 more)

### Community 81 - "render_loop"
Cohesion: 0.20
Nodes (12): assets, here, loadBank(), outDir, renderVoice(), written, loadBank(), parseBank() (+4 more)

### Community 82 - "test-rpm-curve.mjs"
Cohesion: 0.17
Nodes (7): bpy (dependência externa), base(), col(), linear(), box(), Generate the shared web lighting probe and lacquer maps with Cycles/OptiX.  Run, pathlib (dependência externa)

### Community 83 - "gerar_sobressalentes.py"
Cohesion: 0.18
Nodes (12): build_tyre(), fw_at(), Gera web/assets/sobressalentes-v1.glb: peças sobressalentes do Box INTEIA para c, Textura do pneu em (u = volta, v = perfil): banda colorida no flanco, sulcos na, Anel 3D de um perfil no plano (z, y): bordo de ataque em `le` = (x, y, z), corda, Rebaseia a malha na origem do nó alvo (coordenadas locais idênticas às do carro), sec(), span_loft() (+4 more)

### Community 84 - "test-sound-studio.mjs"
Cohesion: 0.15
Nodes (11): SOUND_CREDITS, app, bench, build, kin, panel, studio, template (+3 more)

### Community 85 - "Estúdio de som — bancos calibrados do V12 anos 90 e do V6 2026"
Cohesion: 0.17
Nodes (12): Como o som é produzido, Conferência visual, Créditos das referências, Estúdio de som — bancos calibrados do V12 anos 90 e do V6 2026, Iteração após a primeira audição (17/09/2026), Limitações conhecidas, Motor V12 em 3D (Plano 3), Regenerar (+4 more)

### Community 86 - "Plano 2 — Bancos de loops calibrados (V12 e V6)"
Cohesion: 0.17
Nodes (11): Estúdio de som — roteiro dos Planos 2, 3 e 4, Plano 2 — Bancos de loops calibrados (V12 e V6), Plano 3 — Motor V12 3D, Plano 4 — Aba 07 Som, Tarefa 2.1 — Referências locais, Tarefa 2.2 — Decodificação para cache, Tarefa 2.3 — Order tracking → `alvos-timbre.json`, Tarefa 2.4 — Modelo físico offline (+3 more)

### Community 87 - "gerar_sistemas.py"
Cohesion: 0.26
Nodes (10): _bbox(), frame(), import_car_reference(), _import_glb(), measure_glb(), power_unit_reference(), Gera o asset dos sistemas internos do carro (web/assets/sistemas-v1.glb) com Ble, Carro fantasma para os renders de conferência (não exportado). (+2 more)

### Community 88 - "build.cjs"
Cohesion: 0.17
Nodes (9): esbuild (dependência externa), esbuild, fs, html, model, path, template, withModel (+1 more)

### Community 89 - "Mapa de arquivos"
Cohesion: 0.18
Nodes (10): Estúdio de som — Plano 2: bancos de loops calibrados (V12 e V6), Global Constraints, Mapa de arquivos, Task 1: Referências locais, Task 2: Decodificação para cache, Task 3: Order tracking → `alvos-timbre.json`, Task 4: Modelo físico offline, Task 5: Calibração (+2 more)

### Community 90 - "sound-studio.js"
Cohesion: 0.35
Nodes (12): createEditorState(), normalize(), setDuration(), setMaxRpm(), stateToCurve(), createCurve(), curveFromJSON(), curveToJSON() (+4 more)

### Community 91 - "engine-voice.mjs"
Cohesion: 0.33
Nodes (5): createAmbience(), createEngineVoice(), createResonator(), lcg(), EngineProcessor

### Community 92 - "test-power-unit.mjs"
Cohesion: 0.18
Nodes (10): assemblies, b, before, j, json, len, mixer, out (+2 more)

### Community 93 - "Estúdio de som V6 × V12 — passagem de trabalho (comece por aqui)"
Cohesion: 0.20
Nodes (10): 1. O que o dono pediu, 2. Decisões já tomadas com o dono (não reabrir), 3. Estado atual, 4. Primeiros comandos no outro PC, 5. O que fazer, em ordem, 6. Como o trabalho foi coordenado (repetir se quiser), 7. Regras do projeto que não podem ser quebradas, 8. Pendências fora do estúdio de som (+2 more)

### Community 94 - "docs/INTEGRACAO.md"
Cohesion: 0.20
Nodes (9): Carbono portatil e shader web diferem, Clipe INTEIA_Demonstracao_Montagem_Rodas_DRS, Eixo GLB Y e Blender Z, Evitar dois controladores nas mesmas pecas, GLB animado com demonstracao, GLB estatico para controlador proprio, Motores Unity Unreal Godot nao testados, Necessidade de LODs e colisores no destino (+1 more)

### Community 95 - "test_analise.py"
Cohesion: 0.27
Nodes (5): aggregate_bands(), OrderTracking, Testes do order tracking com sinais sintéticos (python -m unittest ferramentas/s, Soma de ordens de virabrequim com níveis conhecidos (dB relativo à ordem de igni, synthetic_engine()

### Community 96 - "docs/DESENVOLVIMENTO.md"
Cohesion: 0.22
Nodes (7): Build web com esbuild e GLB incorporado, Geometria exige metadados especificos, Gerador sobrescreve master GLBs e previa, HTML gerado nao deve ser editado manualmente, Scripts de reconstrucao Blender e GLBs, Testes automatizados e inspecao visual, Orientacao de leitura pelo README

### Community 97 - "server.cjs"
Cohesion: 0.22
Nodes (7): fs, http, mimeTypes, path, port, root, server

### Community 98 - "docs/BLENDER.md"
Cohesion: 0.25
Nodes (7): Blender 4.5.9 LTS na producao registrada, Colecao de estudio separada, Colecao INTEIA Carro reutilizavel, Desvincular acoes para editar posicoes, Exportar apenas carro e pivos, Raiz INTEIA_F1 e pivos, Timeline montagem rodas direcao DRS

### Community 99 - "Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução"
Cohesion: 0.25
Nodes (7): Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução, Global Constraints, Mapa de arquivos, Planos seguintes (fora deste plano), Task 1: Afinação (`tuning.mjs`), Task 2: Perfis e curva RPM × tempo, Task 3: Detector de f0 e reprodutor com fase travada

### Community 100 - "node_fs (dependência externa)"
Cohesion: 0.33
Nodes (6): check(), here, manifest, outDir, sha256(), wanted

### Community 101 - "parts-info.js"
Cohesion: 0.15
Nodes (14): three_addons_loaders_gltfloader_js (dependência externa), renderInto(), setSpareStatus(), setupSparesUI(), showSpareInfo(), syncSpares(), SPARE_INFO, SPARE_PRESETS (+6 more)

### Community 102 - "docs/VALIDACAO.md"
Cohesion: 0.29
Nodes (6): Ausencia de testes em jogos e colisao, Diferenca registrada de um triangulo, Historico visual subjetivo, Registros nao garantem edicoes futuras, Testes validam calculadora e nao aerodinamica do carro, Validacao registrada de reabertura e remontagem

### Community 103 - "Peças sobressalentes do Box — configuração de pista"
Cohesion: 0.33
Nodes (6): Arquivos, Cenários, Limites, Peças, Peças sobressalentes do Box — configuração de pista, Regenerar

### Community 104 - "Publicação oficial do laboratório"
Cohesion: 0.40
Nodes (5): Atualizar a produção, Critérios de conclusão, Estado da migração, Identidade imutável do Site, Publicação oficial do laboratório

### Community 105 - "main"
Cohesion: 0.40
Nodes (5): compensate_distance(), extrapolate_bands(), main(), Remove, por fonte, a diferença de inclinação alta em relação à mediana da classe, Bandas acima do observado: forma da última banda medida com a tendência de incli

### Community 106 - "Estúdio de som — pesquisa de 16 e 17/09/2026"
Cohesion: 0.50
Nodes (3): 1. Gravações reais com licença livre, 2. Como fazer som de motor realista, Estúdio de som — pesquisa de 16 e 17/09/2026

### Community 107 - "diagnostico_analise.py"
Cohesion: 0.40
Nodes (4): Acabamento F1 — 22/09/2026, Integração, Produção, Verificação e limites

### Community 108 - "Context"
Cohesion: 0.29
Nodes (6): Espectrograma em dB (quadros × bins) e eixo de frequências., stft_db(), plot(), Path, Espectrograma com o traçado de f0 e os quadros aceitos, para conferência visual, Espectrograma de um WAV de demonstração (mesma STFT da análise), gravado ao lado

### Community 110 - "W_rot"
Cohesion: 0.48
Nodes (6): anchors(), hashfile(), load(), Valida a entrega sem executar app nem escrever fora deste diretório., read(), slug()

### Community 111 - "node_fs (dependência externa)"
Cohesion: 0.33
Nodes (5): ALLOWED_LICENSES, ids, manifest, REQUIRED, node_fs (dependência externa)

## Knowledge Gaps
- **732 isolated node(s):** `root`, `require`, `esbuild`, `out`, `sourcePaths` (+727 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Catálogo completo de arquivos` connect `Project Documentation and Assets` to `Technical Documentation Index`?**
  _High betweenness centrality (0.061) - this node is a cross-community bridge._
- **Why does `Índice de funções e métodos` connect `Web Application Source` to `mapeamento-detalhado/README.md`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `Estúdio de som — bancos calibrados do V12 anos 90 e do V6 2026` connect `Estúdio de som — bancos calibrados do V12 anos 90 e do V6 2026` to `Technical Documentation Index`?**
  _High betweenness centrality (0.012) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `sweep()` (e.g. with `build()` and `build()`) actually correct?**
  _`sweep()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `cube()` (e.g. with `build()` and `build()`) actually correct?**
  _`cube()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `W()` (e.g. with `build_tyre()` and `spare()`) actually correct?**
  _`W()` has 6 INFERRED edges - model-reasoned connections that need verification._
- **What connects `root`, `require`, `esbuild` to the rest of the system?**
  _732 weakly-connected nodes found - possible documentation gaps or missing edges._