# Graph Report - INTEIA-laboratorio-3d  (2026-09-22)

## Corpus Check
- 190 files · ~317,623 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1600 nodes · 2699 edges · 99 communities (97 shown, 2 thin omitted)
- Extraction: 93% EXTRACTED · 7% INFERRED · 0% AMBIGUOUS · INFERRED: 179 edges (avg confidence: 0.79)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `eccd6283`
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
- Primary Brand SVG
- Official Name Branding
- Wordmark Brand Assets
- HTML Application Template
- Three.js License Info
- Navigator Validation Guides
- Asset Reutilization Guide
- Integration and Portability
- Visual Identity Inventory
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
- Garage UI and Branding
- Symbol Inventory
- loft
- Documentação do Laboratório 3D INTEIA
- Publicação do laboratório
- build.cjs
- test-power-unit.mjs
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
- server.cjs
- Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução
- node_fs (dependência externa)
- parts-info.js
- Peças sobressalentes do Box — configuração de pista
- Publicação oficial do laboratório
- Estúdio de som — pesquisa de 16 e 17/09/2026
- diagnostico_analise.py
- face_uv_fit
- face_uv_fit
- W_rot

## God Nodes (most connected - your core abstractions)
1. `Catálogo completo de arquivos` - 237 edges
2. `Índice de funções e métodos` - 48 edges
3. `sweep()` - 28 edges
4. `W()` - 26 edges
5. `cube()` - 25 edges
6. `cyl()` - 24 edges
7. `render_loop()` - 21 edges
8. `lathe()` - 17 edges
9. `loft()` - 16 edges
10. `analyse_signal()` - 16 edges

## Surprising Connections (you probably didn't know these)
- `createSystems()` --indirect_call--> `load()`  [INFERRED]
  web/src/systems.js → ferramentas/otimizar_sistemas.mjs
- `createTestBank()` --indirect_call--> `load()`  [INFERRED]
  web/test-fixtures/sound-bank.mjs → ferramentas/otimizar_sistemas.mjs
- `renderVoice()` --calls--> `createEngineVoice()`  [EXTRACTED]
  ferramentas/som/renderizar_demos.mjs → web/src/sound/engine-voice.mjs
- `span_loft()` --calls--> `loft()`  [INFERRED]
  ferramentas/gerar_sobressalentes.py → ferramentas/sistemas/lib.py
- `createV12View()` --indirect_call--> `load()`  [INFERRED]
  web/src/sound/v12-view.js → ferramentas/otimizar_sistemas.mjs

## Import Cycles
- None detected.

## Communities (99 total, 2 thin omitted)

### Community 0 - "docs/INTEGRACAO.md"
Cohesion: 0.09
Nodes (23): 1.1 O Diagnóstico, 1.2 As 5 Grandes Falhas Diagnosticadas no Código, 1. Veredicto e Diagnóstico Forense da IA em `INTEIA-laboratorio-3d`, 2. Mapa de Arquivos do Projeto: Onde Agir e O que Fazer, 3. Especificação Geométrica e Espacial dos 14 Sistemas, 4. Instruções Diretas de Ajuste para a IA no Código de `systems.js`, 5. Checklist da Implementação Presente, DIRETRIZES CANÔNICAS DE MODELAGEM 3D — SISTEMAS DO CARRO DE F1 (ANIMAGRAFFS) (+15 more)

### Community 1 - "Build and Catalog Scripts"
Cohesion: 0.09
Nodes (32): code_paths(), family_purpose(), gather_symbols(), git(), glb_info(), inventory(), link(), main() (+24 more)

### Community 2 - "Three.js Scene Controls"
Cohesion: 0.09
Nodes (28): three_addons_controls_orbitcontrols_js (dependência externa), three_addons_exporters_gltfexporter_js (dependência externa), three_addons_geometries_decalgeometry_js (dependência externa), three_addons_postprocessing_effectcomposer_js (dependência externa), three_addons_postprocessing_smaapass_js (dependência externa), assemblyTo(), categoryLabels, closeEngine() (+20 more)

### Community 3 - "Vehicle Systems Configuration"
Cohesion: 0.07
Nodes (33): advanceLocalSpin(), createSystems(), FLOW_SPEEDS, flowTexture(), HIDE_GROUPS, LOCAL_SPIN_AXES, SYSTEM_CATALOG, SYSTEM_IDS (+25 more)

### Community 4 - "Blender Production Workflow"
Cohesion: 0.09
Nodes (23): 10. Cockpit, piloto, pedais, volante e sensores, 1. Aerodinâmica, 2. Estrutura e segurança, 3. Suspensão, direção e rodas, 4. Frenagem e brake-by-wire, 5. Motor, turbo e exaustão, 6. ERS, bateria e atualização 2026, 7. Refrigeração e fluidos (+15 more)

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
Cohesion: 0.19
Nodes (21): _add(), apply_circular_eq(), _bandpass(), clamp_params(), _comb(), cylinder_bank(), _delay(), _highpass() (+13 more)

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
Cohesion: 0.10
Nodes (21): 10. Build, servidor e saídas, 11. Produção e validação de assets fora do navegador, 12. Testes existentes e o que de fato cobrem, 13. Reutilização por módulo: requisitos e limites concretos, 14. Como atualizar esta página e as relações, 15. Assinaturas da leitura de fontes, 1. Por onde começar no código, 2. Cadeia de importações e responsabilidade (+13 more)

### Community 14 - "Animation Data Merging"
Cohesion: 0.18
Nodes (10): b, file, fs, j, json, merged, old, out (+2 more)

### Community 15 - "Architecture and Path Mapping"
Cohesion: 0.13
Nodes (12): gltf, io, jsonLength, manifest, manifestPath, output, partsAfter, partsBefore (+4 more)

### Community 16 - "Visual Review History"
Cohesion: 0.26
Nodes (11): bank_points(), Pontos (rpm exato, amostras por ciclo) do banco: passo geométrico de 8 % da marc, align_neighbours(), _angular_cycle(), _best_lag(), main(), ndarray, Gera o banco de loops de um motor: web/assets/som-<motor>-v1.bin + .json.  Ponto (+3 more)

### Community 17 - "CI/CD GitHub Workflows"
Cohesion: 0.15
Nodes (19): calibration_bands(), distance(), fit_eq(), harmonic_orders(), loop_cycles(), main(), measure_loop(), Objective (+11 more)

### Community 18 - "Version Release History"
Cohesion: 0.27
Nodes (5): load_profile(), harmonic_f0(), ModeloFisico, ndarray, f0 por soma harmônica (6 harmônicos) em candidatos de ±60 % do esperado; imune a

### Community 19 - "Contribution and Consistency"
Cohesion: 0.36
Nodes (10): caliperGeometry(), discGeometry(), discTexture(), enhanceCar(), heatTexture(), localVaryings(), paintShader(), rimPatch() (+2 more)

### Community 20 - "Laboratory Data Atlas"
Cohesion: 0.20
Nodes (10): 1. Empacotar o site, 2. Reconstruir o carro no Blender, 3. Exportar o box pelo navegador, 4. Produzir o Blender do box e a prévia, 5. Identidade e outros downloads, 6. Validação e rastreabilidade, Fontes, derivados e arquivos ausentes, Grafo do processo existente (+2 more)

### Community 21 - "SVG Brand Assets"
Cohesion: 0.22
Nodes (9): Análise complementar do dossiê técnico, Base documental usada, Checklist de validação, Comparação por subsistema, Contradições e trechos stale, Limitações que permanecem, Pendências da auditoria e resolução, Recomendações priorizadas (+1 more)

### Community 22 - "Agent Quick Index"
Cohesion: 0.24
Nodes (3): Orientação de leitura, Conteúdo de terceiros, Motor V6 e marcas do F1 Loop (15/09/2026)

### Community 23 - "Historical Evaluation Records"
Cohesion: 0.25
Nodes (8): Atualização do carro e motor, Baixar e reutilizar, Bancadas de modelagem, Comece aqui, Download e execução, Laboratório 3D INTEIA, Limites e direitos, O que está incluído

### Community 24 - "Atlas Template Data"
Cohesion: 0.25
Nodes (4): BAY, createInCarEngine(), ENGINE_AT, HINGE

### Community 25 - "Local Project Rules"
Cohesion: 0.50
Nodes (3): Chisle, Navegação econômica, Regras locais — Laboratório 3D INTEIA

### Community 26 - "Legacy Engine Context"
Cohesion: 0.32
Nodes (6): CAR_CATEGORY_FALLBACK, CAR_RULES, describeCarPart(), describePart(), RULES, SYSTEM_FALLBACK

### Community 27 - "Turbo Architecture Specs"
Cohesion: 0.29
Nodes (7): 1.0.0 — 2026-09-12, 1.1.0 — 2026-09-12, 2026-09-15 — Bancadas, piloto e capacete, 2026-09-15 — Carro final e motor no box, 2026-09-16 — ChatGPT Site oficial, 2026-09-18 — Leitura dos sistemas e correções de fato, Histórico

### Community 28 - "Technical Dossier Analysis"
Cohesion: 0.29
Nodes (7): Antes de enviar mudanças, Atualizar o mapa do projeto, Desenvolvimento, Gerar os sistemas internos, Reconstruir Blender e GLBs, Requisitos, Site

### Community 29 - "3D Modeling Guidelines"
Cohesion: 0.33
Nodes (6): Entradas e resultados, Fundamentos, Leitura visual por região, Para uma análise real da geometria, Túnel de vento — escopo físico, Visualização

### Community 30 - "Verifiable Knowledge Graphs"
Cohesion: 0.33
Nodes (6): Contrato das peças, Controles e seus donos, Entradas e montagem da aplicação, Exportações e testes, Módulos e dependências práticas, Responsabilidades, entradas e contratos

### Community 31 - "Contracts and Responsibilities"
Cohesion: 0.33
Nodes (6): Como usar, Detalhamento informativo do fluxo, Limites do resultado, Revisão adicional após avaliação do usuário, Túnel de vento — cinco iterações visuais, Verificação

### Community 32 - "Asset Production Deliverables"
Cohesion: 0.33
Nodes (5): Abrir no Blender ou em outro projeto 3D, Download direto, Executar a aplicação, Permissões, Reutilizar os modelos e a aplicação

### Community 33 - "Verified State Modules"
Cohesion: 0.40
Nodes (5): Exportação, Guia Blender, Objetos, pivôs e materiais, Reutilizar a coleção, Timeline — 30 fps

### Community 34 - "Monochrome Brand Assets"
Cohesion: 0.40
Nodes (5): Arquivos reutilizáveis, Box-laboratório INTEIA, Navegador, Referências de organização, Revisão do box — três passagens visuais

### Community 35 - "Identity Style Guide"
Cohesion: 0.40
Nodes (5): Integração em sites e jogos, Materiais, Motores de jogos, Qual arquivo escolher, Three.js

### Community 36 - "Primary Brand SVG"
Cohesion: 0.40
Nodes (5): Arquitetura dos módulos web, Evidências das relações, Grafos verificáveis, Produção do box, Produção do carro

### Community 37 - "Official Name Branding"
Cohesion: 0.40
Nodes (5): Artefatos entregues, Ensaio aerodinâmico por coeficientes, Histórico visual, Testes que faltam por destino, Validação e limites observados

### Community 38 - "Wordmark Brand Assets"
Cohesion: 0.67
Nodes (3): Arquitetura e mapa dos arquivos, Fluxo, Fonte da verdade

### Community 39 - "HTML Application Template"
Cohesion: 0.67
Nodes (3): Direitos e procedência, Procedência e conteúdo de terceiros, Titularidade do projeto

### Community 40 - "Three.js License Info"
Cohesion: 0.67
Nodes (3): Arquivos, INTEIA — identidade visual do laboratório, Uso

### Community 41 - "Navigator Validation Guides"
Cohesion: 0.50
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

### Community 46 - "Technical Documentation Index"
Cohesion: 0.33
Nodes (3): Contribuir, Mapa do Laboratório 3D INTEIA, Evidências de verificação do atlas

### Community 47 - "File Manifest Generation"
Cohesion: 0.25
Nodes (7): crypto, files, fs, out, path, root, crypto (dependência externa)

### Community 48 - "Script Execution Procedures"
Cohesion: 0.29
Nodes (7): Abrir sem disputar a porta 5186, Atualizar e reproduzir o mapeamento, Estado, concorrência e exclusões, O que os scripts realmente fazem, Pré-requisitos, Reproduzir o diagnóstico graphify isolado, Sequência de atualização

### Community 49 - "Graph Architecture Guidance"
Cohesion: 0.33
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
Cohesion: 0.17
Nodes (30): bm_to_object(), bolt_ring(), box_uv(), car_part(), gear(), lathe(), _link(), loft() (+22 more)

### Community 56 - "mapeamento-detalhado/README.md"
Cohesion: 0.15
Nodes (7): Índice rápido para agentes, Inventário completo, Símbolos declarados, Exclusões observadas, Árvore comentada, Validação do atlas no navegador, Chisle

### Community 57 - "Environment Setup Guide"
Cohesion: 0.50
Nodes (4): Alternar entre computadores, Continuar em outro PC, Documentação, Primeira instalação

### Community 58 - "Publication Verification"
Cohesion: 0.08
Nodes (43): bbox_web(), arc2d(), auto_explode(), both_sides(), car_components(), catmull(), centroid(), _encode_normal() (+35 more)

### Community 59 - "cube"
Cohesion: 0.25
Nodes (9): super_ellipse(), add(), bank_frame(), build(), 06 · Unidade de potência térmica: V6 de 90° com bloco, cárter seco, cabeçotes e, Eixo do cilindro (para cima e para fora) e normal externa da bancada., bladder_sections(), build() (+1 more)

### Community 60 - "Driver and Helmet Models"
Cohesion: 0.21
Nodes (9): three_addons_geometries_roundedboxgeometry_js (dependência externa), createHelmet1991(), createSennaDriver(), box, context, driver, mechanics, model (+1 more)

### Community 61 - "Wind Tunnel Visualization"
Cohesion: 0.20
Nodes (10): three (dependência externa), aerodynamicTest(), createFlowDetail(), createTunnelVisual(), createWindTunnel(), a, b, cross (+2 more)

### Community 63 - "Garage UI and Branding"
Cohesion: 0.47
Nodes (4): createGarage(), brandSVG(), drawBrand(), glyphs

### Community 66 - "Symbol Inventory"
Cohesion: 0.17
Nodes (32): airfoil(), bevel(), cube(), cyl(), flow_ribbon(), helix(), lado(), plate() (+24 more)

### Community 67 - "loft"
Cohesion: 0.14
Nodes (14): cylinderAt(), ENGINE_PROFILES, firingIntervalDeg(), firingWindowAt(), createPhasePlayer(), prepareBank(), detectFiringHz(), detectPitch() (+6 more)

### Community 69 - "Documentação do Laboratório 3D INTEIA"
Cohesion: 0.40
Nodes (5): Documentação do Laboratório 3D INTEIA, Fontes de verdade, Mapas do repositório, Operação e desenvolvimento, Produto e conteúdo técnico

### Community 70 - "Publicação do laboratório"
Cohesion: 0.12
Nodes (26): crankRotationZ(), pinAngleDeg(), pinPosition(), pistonDistance(), poseV12(), rodRotationZ(), strokeOf(), wristPosition() (+18 more)

### Community 71 - "build.cjs"
Cohesion: 0.11
Nodes (16): ALLOWED_LICENSES, ids, manifest, REQUIRED, node_assert_strict (dependência externa), capped, curve, gridV12 (+8 more)

### Community 72 - "test-power-unit.mjs"
Cohesion: 0.07
Nodes (22): mirror_x(), Duplica a peça espelhada em X (site) mantendo materiais e extras., 01 · Aerodinâmica: o que a carroceria esconde — túneis venturi do assoalho, cerc, build(), 02 · Estrutura central: célula de sobrevivência em sanduíche de carbono e colmei, tub_section(), build(), 03 · Suspensão: wishbones em perfil aerodinâmico, uprights usinados, pushrod dia (+14 more)

### Community 74 - "build.cjs"
Cohesion: 0.13
Nodes (23): axis_deg(), axis_vec(), bank_of(), corte(), index_in_bank(), marcar(), origem_em(), pin_offset_deg() (+15 more)

### Community 75 - "test-power-unit.mjs"
Cohesion: 0.10
Nodes (30): aggregate_bands(), analyse_signal(), compensate_distance(), crank_candidates(), engine_orders(), extrapolate_bands(), _interp_rows(), main() (+22 more)

### Community 76 - "docs/INTEGRACAO.md"
Cohesion: 0.15
Nodes (18): clamp(), createCurve(), DURATION_RANGE_S, evaluateCurve(), presetCurve(), simulateCurve(), tangents(), first (+10 more)

### Community 77 - "branding.js"
Cohesion: 0.20
Nodes (10): Arquivos, Extras exportados nos nós, Interface, Leitura de cada sistema, Limites, Publicação, Referencial e escala, Refinamento de fabricação — setembro de 2026 (+2 more)

### Community 78 - "Publicação oficial do laboratório"
Cohesion: 0.26
Nodes (15): addPoint(), clamp(), describeTuning(), mountCurveEditor(), movePoint(), noteGrid(), nudgePoint(), PAD (+7 more)

### Community 79 - "ARVORE.md"
Cohesion: 0.12
Nodes (17): 1. Referências reais (só para análise), 2. Modelo físico offline e banco de loops, 3. Reprodução com fase travada (`phase-player.mjs`), 4. Curva de aceleração (`rpm-curve.mjs` + `curve-editor.js`), 5. Motor V12 3D (`v12-v1.glb`), 6. Aba 07 Som (`sound-studio.js`), Afinação, Arquitetura (+9 more)

### Community 80 - "gerar_v12.py"
Cohesion: 0.15
Nodes (16): Espectrograma em dB (quadros × bins) e eixo de frequências., stft_db(), decode_reference(), load_cached(), main(), ndarray, Path, Decodifica as referências de .referencias/ para o cache de análise.  Cada referê (+8 more)

### Community 81 - "render_loop"
Cohesion: 0.20
Nodes (12): assets, here, loadBank(), outDir, renderVoice(), written, loadBank(), parseBank() (+4 more)

### Community 82 - "test-rpm-curve.mjs"
Cohesion: 0.16
Nodes (12): bpy (dependência externa), anchors(), hashfile(), load(), Valida a entrega sem executar app nem escrever fora deste diretório., read(), slug(), box() (+4 more)

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
Cohesion: 0.38
Nodes (10): createEditorState(), normalize(), setDuration(), setMaxRpm(), stateToCurve(), curveFromJSON(), curveToJSON(), createSoundStudio() (+2 more)

### Community 91 - "engine-voice.mjs"
Cohesion: 0.31
Nodes (6): createAmbience(), createEngineVoice(), createResonator(), lcg(), EngineProcessor, createRpmFollower()

### Community 92 - "test-power-unit.mjs"
Cohesion: 0.18
Nodes (10): assemblies, b, before, j, json, len, mixer, out (+2 more)

### Community 93 - "Estúdio de som V6 × V12 — passagem de trabalho (comece por aqui)"
Cohesion: 0.20
Nodes (10): 1. O que o dono pediu, 2. Decisões já tomadas com o dono (não reabrir), 3. Estado atual, 4. Primeiros comandos no outro PC, 5. O que fazer, em ordem, 6. Como o trabalho foi coordenado (repetir se quiser), 7. Regras do projeto que não podem ser quebradas, 8. Pendências fora do estúdio de som (+2 more)

### Community 97 - "server.cjs"
Cohesion: 0.22
Nodes (7): fs, http, mimeTypes, path, port, root, server

### Community 99 - "Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução"
Cohesion: 0.25
Nodes (7): Estúdio de som — Plano 1: núcleo de afinação, curva e reprodução, Global Constraints, Mapa de arquivos, Planos seguintes (fora deste plano), Task 1: Afinação (`tuning.mjs`), Task 2: Perfis e curva RPM × tempo, Task 3: Detector de f0 e reprodutor com fase travada

### Community 100 - "node_fs (dependência externa)"
Cohesion: 0.29
Nodes (7): check(), here, manifest, outDir, sha256(), wanted, node_fs (dependência externa)

### Community 101 - "parts-info.js"
Cohesion: 0.12
Nodes (17): load(), three_addons_loaders_gltfloader_js (dependência externa), renderInto(), setSpareStatus(), setupSparesUI(), showSpareInfo(), syncSpares(), createV12View() (+9 more)

### Community 103 - "Peças sobressalentes do Box — configuração de pista"
Cohesion: 0.33
Nodes (6): Arquivos, Cenários, Limites, Peças, Peças sobressalentes do Box — configuração de pista, Regenerar

### Community 104 - "Publicação oficial do laboratório"
Cohesion: 0.40
Nodes (5): Atualizar a produção, Critérios de conclusão, Estado da migração, Identidade imutável do Site, Publicação oficial do laboratório

### Community 106 - "Estúdio de som — pesquisa de 16 e 17/09/2026"
Cohesion: 0.22
Nodes (3): 1. Gravações reais com licença livre, 2. Como fazer som de motor realista, Estúdio de som — pesquisa de 16 e 17/09/2026

### Community 107 - "diagnostico_analise.py"
Cohesion: 0.40
Nodes (4): Acabamento F1 — 22/09/2026, Integração, Produção, Verificação e limites

### Community 113 - "W_rot"
Cohesion: 0.32
Nodes (7): Euler (rx, ry, rz) em graus no referencial do site -> Euler Blender., W_rot(), build(), core(), hose(), 08 · Refrigeração assimétrica: intercooler ar-ar inclinado no sidepod esquerdo c, Núcleo de trocador com aletas, tanques superior/inferior e tirantes; inclinado e

## Knowledge Gaps
- **805 isolated node(s):** `root`, `require`, `esbuild`, `out`, `sourcePaths` (+800 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Catálogo completo de arquivos` connect `Project Documentation and Assets` to `Technical Documentation Index`?**
  _High betweenness centrality (0.116) - this node is a cross-community bridge._
- **Why does `Índice de funções e métodos` connect `Web Application Source` to `mapeamento-detalhado/README.md`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `Pesquisa — sistemas de um carro de Fórmula 1 a partir do vídeo` connect `Blender Production Workflow` to `Estúdio de som — pesquisa de 16 e 17/09/2026`?**
  _High betweenness centrality (0.019) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `sweep()` (e.g. with `build()` and `build()`) actually correct?**
  _`sweep()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `W()` (e.g. with `build_tyre()` and `spare()`) actually correct?**
  _`W()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `cube()` (e.g. with `build()` and `build()`) actually correct?**
  _`cube()` has 17 INFERRED edges - model-reasoned connections that need verification._
- **What connects `root`, `require`, `esbuild` to the rest of the system?**
  _805 weakly-connected nodes found - possible documentation gaps or missing edges._