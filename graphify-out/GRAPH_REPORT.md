# Graphify — estrutura e leitura semântica

[Índice principal](../docs/mapas/README.md) · [Grafo interativo](graph.html) · [Extração sem simplificação](../docs/mapas/graphify-extracao.json)

Snapshot da revisão `1ae4fd15062d347dc8462af8f4db33c749e6575b`. Fontes dos nós levam a URLs fixadas nessa revisão. A documentação do atlas e alterações paralelas posteriores são cobertas pelo inventário principal, não retroativamente por este snapshot.

Detecção inicial: 59 arquivos compatíveis, aproximadamente 109.847 palavras (inclui HTML gerado). Extração: 28 arquivos classificados como código; 22 documentos incluindo LICENSE em lugar do HTML gerado web/index.html; 9 imagens inspecionadas visualmente. Seis JSONs de evidência/procedência produziram zero nós no AST; seus arquivos e os binários estão cobertos pelo inventário determinístico. Configurações sem extensão e lockfile também estão no inventário principal. O conteúdo base64 do HTML gerado não foi tratado como documentação semântica.

Resultado: 319 nós, 361 relações brutas e 360 relações no grafo direcionado simples, em 23 comunidades. O diagnóstico não encontrou pontas ausentes nem autorrelações. **Limite de integridade visível: um par é simplificado** (`app-v2` → `resize`: contém e chamada indireta). As duas evidências, L39 e L40, permanecem na extração bruta. As dependências externas são referências a imports; sua implementação não foi analisada. Comunidades expressam proximidade no grafo, não uma arquitetura normativa.

Custo/tokens: contagem não disponibilizada pelas ferramentas desta sessão; não mensurado. Os campos numéricos zero na extração são placeholders do schema, não uso zero nem estimativa de economia. Extração AST local; sem consumo medido de uma API externa. As seções automáticas abaixo usam métricas de conectividade, não validação factual adicional. As prévias representam aparência histórica; fumaça e telas não são CFD nem telemetria medida.

## Corpus Check
- 59 files · ~109,847 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 319 nodes · 360 edges · 23 communities (22 shown, 1 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.92)
- Token cost: indisponível; placeholders numéricos não são medição.

## Community Hubs (Navigation)
- Aplicação e estúdio
- Guias de integração
- Build e arquivos
- Ensaio e validação
- Túnel e equações
- Ferramentas Blender
- Box e identidade
- Direitos e licenças
- Mecânica e testes
- Pacote npm
- Variantes vetoriais
- Captura de personalização
- Template e controles
- Arquitetura documentada
- Revisões do túnel
- Prévia do box
- Guia visual
- Integração contínua
- Histórico de versões
- Contribuição
- Comparação de luz
- Prévia do carro
- Textura de carbono

## God Nodes (most connected - your core abstractions)
1. `Captura histórica da interface de personalização` - 11 edges
2. `three (dependência externa)` - 8 edges
3. `brandSVG()` - 5 edges
4. `Prévia estática do carro no box INTEIA` - 5 edges
5. `scripts` - 4 edges
6. `aerodynamicTest()` - 4 edges
7. `view()` - 4 edges
8. `applyCarMaterials()` - 4 edges
9. `createTunnelVisual()` - 4 edges
10. `createWindTunnel()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Assinatura INTEIA monocromática` --semantically_similar_to--> `brandSVG()`  [INFERRED] [semantically similar]
  identidade/INTEIA-monocromatico.svg → web/src/identity.js
- `Assinatura INTEIA negativa` --semantically_similar_to--> `brandSVG()`  [INFERRED] [semantically similar]
  identidade/INTEIA-negativo.svg → web/src/identity.js
- `Assinatura INTEIA principal` --semantically_similar_to--> `brandSVG()`  [INFERRED] [semantically similar]
  identidade/INTEIA-principal.svg → web/src/identity.js
- `Monograma IA compacto` --semantically_similar_to--> `emblem`  [INFERRED] [semantically similar]
  identidade/INTEIA-simbolo.svg → web/src/identity.js
- `Wordmark INTEIA em Arial branco` --semantically_similar_to--> `applyInteiaBranding()`  [INFERRED] [semantically similar]
  web/assets/INTEIA-wordmark.svg → web/src/branding.js

## Imports e ciclos

O grafo determinístico de imports locais está em [GRAFOS.md](../docs/mapas/GRAFOS.md). Referências externas não têm arquivo de implementação local atribuído; a origem da evidência está nas arestas, evitando interpretar o local do import como destino da dependência.

## Communities (23 total, 1 thin omitted)

### Community 0 - "Aplicação e estúdio"
Cohesion: 0.07777777777777778
Nodes (30): Monograma IA vermelho em um path vetorial, Monograma IA compacto, three_addons_controls_orbitcontrols_js (dependência externa), three_addons_controls_transformcontrols_js (dependência externa), three_addons_exporters_gltfexporter_js (dependência externa), three_addons_geometries_roundedboxgeometry_js (dependência externa), three_addons_postprocessing_effectcomposer_js (dependência externa), three_addons_postprocessing_outputpass_js (dependência externa) (+22 more)

### Community 1 - "Guias de integração"
Cohesion: 0.06628787878787878
Nodes (28): Blender 4.5.9 LTS na producao registrada, Colecao de estudio separada, Colecao INTEIA Carro reutilizavel, Desvincular acoes para editar posicoes, Exportar apenas carro e pivos, Raiz INTEIA_F1 e pivos, Timeline montagem rodas direcao DRS, Build web com esbuild e GLB incorporado (+20 more)

### Community 2 - "Build e arquivos"
Cohesion: 0.06451612903225806
Nodes (28): crypto, files, fs, out, path, root, b, file (+20 more)

### Community 3 - "Ensaio e validação"
Cohesion: 0.07692307692307693
Nodes (23): Bloqueios Mach montagem e isolamento, Coeficientes externos nao determinados pelo GLB, Cores de regiao sem medicao fisica, CSV com origem e validade dos parametros, Ensaio aerodinamico por coeficientes, Envelope analitico simplificado, Exemplo hipotetico sem medicao no carro, Fumaca artistica por particulas (+15 more)

### Community 4 - "Túnel e equações"
Cohesion: 0.12987012987012986
Nodes (15): node_assert_strict (dependência externa), three (dependência externa), three_addons_geometries_decalgeometry_js (dependência externa), Wordmark INTEIA em Arial branco, INTEIA em text Arial 700 branco; sem monograma nem subtítulo, aerodynamicTest(), applyInteiaBranding(), createFlowDetail() (+7 more)

### Community 5 - "Ferramentas Blender"
Cohesion: 0.15789473684210525
Nodes (11): bpy (dependência externa), base(), col(), linear(), json (dependência externa), math (dependência externa), mathutils (dependência externa), os (dependência externa) (+3 more)

### Community 6 - "Box e identidade"
Cohesion: 0.1
Nodes (18): Blender com box e carro estatico, Box laboratorio original ilustrativo, Demais monitores sem telemetria real, Download GLB do box com estado das telas, GLB sem reflexo pre calculado do navegador, Identidade vetorial compartilhada na interface e box, McLaren — engineering room, Azerbaijan 2023, McLaren — Japanese Grand Prix practice report, 2024 (+10 more)

### Community 7 - "Direitos e licenças"
Cohesion: 0.14705882352941177
Nodes (13): Licenca do tutorial nao documentada, Original do tutorial ausente, Sem afiliacao ou certificacao esportiva, Titularidade declarada INTEIA, Tutorial F1_2026_tutorial_part7_textures.blend, Direitos de terceiros preservados, Licenca Proprietaria INTEIA, Reutilizacao depende de autorizacao INTEIA (+5 more)

### Community 8 - "Mecânica e testes"
Cohesion: 0.125
Nodes (15): node_fs (dependência externa), three_addons_loaders_gltfloader_js (dependência externa), createMechanics(), names, b, before, box, j (+7 more)

### Community 9 - "Pacote npm"
Cohesion: 0.125
Nodes (15): esbuild, three, author, dependencies, three, devDependencies, esbuild, license (+7 more)

### Community 10 - "Variantes vetoriais"
Cohesion: 0.15384615384615385
Nodes (13): Monograma IA, separador vertical, nome INTEIA e subtítulo Laboratório 3D, INTEIA em seis letras desenhadas em curvas e inclinadas 12 graus, Grafite #202930 em todos os elementos, Assinatura INTEIA monocromática, Monograma IA, separador vertical, nome INTEIA e subtítulo Laboratório 3D, INTEIA em seis letras desenhadas em curvas e inclinadas 12 graus, Branco #F0F2F3 e vermelho #D92135, Assinatura INTEIA negativa (+5 more)

### Community 11 - "Captura de personalização"
Cohesion: 0.16666666666666666
Nodes (12): Seletor de acabamento da pintura, Carro com combinação de cores personalizada, Controles de cores independentes, Captura histórica da interface de personalização, Instruções visíveis de interação com o carro, Controles de intensidade da luz, piso e fundo, Cabeçalho INTEIA Laboratório 3D, Controles de montagem e vista explodida (+4 more)

### Community 12 - "Template e controles"
Cohesion: 0.2222222222222222
Nodes (8): Area e coeficientes inicialmente vazios, Aviso visualizacao artistica nao CFD, Exportacoes imagem box e CSV, Oficina de componentes e controles, Placeholder APP para bundle, Placeholder MODEL para GLB, Template Laboratorio 3D INTEIA, Vista explodida nao sequencia tecnica de manutencao

### Community 13 - "Arquitetura documentada"
Cohesion: 0.2857142857142857
Nodes (6): Caminho GLB para HTML offline, Caminho GLB para master e exports, Fontes do visualizador em web src, Master reconstruido sem pilha original do tutorial, Regeneracao sobrescreve edicoes manuais do master, Shaders e iluminacao diferem entre caminhos

### Community 14 - "Revisões do túnel"
Cohesion: 0.2857142857142857
Nodes (6): 30 FPS observado sem garantia, Avaliacao subjetiva sem certificacao fisica, Cinco iteracoes visuais historicas do tunel, Detalhamento informativo posterior do fluxo, Pausa conferida por imagens identicas, Revisao adicional com particulas

### Community 15 - "Prévia do box"
Cohesion: 0.3333333333333333
Nodes (6): Área demarcada para o carro, Carro vermelho no box, Identidade INTEIA na parede, Faixas luminosas no teto, Prévia estática do carro no box INTEIA, Interior do box

### Community 16 - "Guia visual"
Cohesion: 0.4
Nodes (4): Apresentacao da identidade INTEIA, Nome em curvas e IA destacado, Paleta vermelho grafite branco, Sem marca oficial da Formula 1

### Community 17 - "Integração contínua"
Cohesion: 0.5
Nodes (3): Build e testes web no workflow, Node 24 no workflow, Verificar site em push e pull_request

### Community 18 - "Histórico de versões"
Cohesion: 0.5
Nodes (3): Nenhuma CFD da geometria executada, Versao 1.0.0 laboratorio e Blender, Versao 1.1.0 tunel por coeficientes

### Community 19 - "Contribuição"
Cohesion: 0.5
Nodes (3): Capturas comparaveis para mudancas visuais, HTML regenerado deve acompanhar mudancas de codigo, Preservacao de IDs das 97 pecas

### Community 20 - "Comparação de luz"
Cohesion: 0.5
Nodes (3): Comparacao antes depois em 1440 por 960, Pareceres historicos subjetivos, ROSSO registro historico de melhoria

### Community 21 - "Prévia do carro"
Cohesion: 0.6666666666666666
Nodes (3): Carro vermelho com rodas expostas, Prévia estática do carro em estúdio, Piso e fundo de estúdio cinza

## Knowledge Gaps
- **169 isolated node(s):** `fs`, `path`, `crypto`, `root`, `files` (+164 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **What connects `fs`, `path`, `crypto` to the rest of the system?**
  _169 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Aplicação e estúdio` be split into smaller, more focused modules?**
  _Cohesion score 0.07777777777777778 - nodes in this community are weakly interconnected._
- **Should `Guias de integração` be split into smaller, more focused modules?**
  _Cohesion score 0.06628787878787878 - nodes in this community are weakly interconnected._
- **Should `Build e arquivos` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._
- **Should `Ensaio e validação` be split into smaller, more focused modules?**
  _Cohesion score 0.07692307692307693 - nodes in this community are weakly interconnected._
- **Should `Túnel e equações` be split into smaller, more focused modules?**
  _Cohesion score 0.12987012987012986 - nodes in this community are weakly interconnected._
- **Should `Box e identidade` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
## Benchmark sintético do graphify

O comando benchmark estimou corpus de 15.950 palavras, 43 tokens médios por consulta e redução 494,6x para duas perguntas genéricas. Essa estimativa não mede tokens desta sessão, qualidade das respostas nem economia comprovada para o laboratório. A detecção inicial tinha outra contagem porque inclui HTML gerado. Não usar essa razão como indicador de validação.
