# Árvore comentada

[Índice](README.md) · [Catálogo](CATALOGO.md)

Diretórios de dependências, caches e Git são listados nas exclusões; não são expandidos. Esta documentação tem inventário próprio para evitar autorreferência.

```text
INTEIA-laboratorio-3d/
  .claude/  # Documentação complementar da conversa paralela
    settings.json  # Configuração local de assistência e concisão por agente
  .cursor/  # Documentação complementar da conversa paralela
    rules/  # Documentação complementar da conversa paralela
      chisle.mdc  # Configuração local de assistência e concisão por agente
  .gitattributes  # Política de texto/LF, binários e supressão de diff do HTML empacotado
  .github/  # Automação de verificação remota
    copilot-instructions.md  # Configuração local de assistência e concisão por agente
  .gitignore  # Exclusões de dependências, caches, backups Blender e dados de ambiente
  .graphifyignore  # Configuração ou saída navegável do mapa Graphify
  .planning/  # Documentação complementar da conversa paralela
    ai/  # Documentação complementar da conversa paralela
      project-index.json  # Índice e instruções locais para navegação econômica por agentes
    architecture/  # Documentação complementar da conversa paralela
      system-architecture.html  # Diagrama arquitetural Archify e sua especificação validada
      system.architecture.json  # Diagrama arquitetural Archify e sua especificação validada
  00_INDICE_IA.md  # Índice e instruções locais para navegação econômica por agentes
  AGENTS.md  # Índice e instruções locais para navegação econômica por agentes
  CHANGELOG.md  # Histórico editorial das mudanças e entregas
  CONTRIBUTING.md  # Orientações para contribuir e verificar alterações
  INTEIA_F1_Master.blend  # Projeto Blender entregue: carro, coleções, materiais, demonstração e estúdio
  LEIA-ME.md  # Entrada em português para o pacote e seus destinos
  LICENSE  # Termos proprietários INTEIA; publicação não equivale a licença aberta
  Previa-Blender.png  # Prévia renderizada do projeto Blender; não é textura do modelo
  README.md  # Entrada pública do laboratório, entregas, instalação e limites
  THIRD-PARTY-NOTICES.md  # Avisos de Three.js e procedência de contribuições externas
  ambientes/  # Box GLB e cena Blender com carro
    INTEIA-box-laboratorio.glb  # Box procedural exportado; arquivo separado do carro
    INTEIA_Box_com_carro.blend  # Cena Blender com box e carro reunidos e imagens empacotadas
    Previa-Box.png  # Prévia renderizada da cena Blender com box
    validacao-box.json  # Evidência histórica do empacotamento do box e suas imagens
  docs/  # Guias técnicos e documentação
    ACABAMENTO-E-RENDER.md  # Acabamento, iluminação e ajustes de render documentados em tarefa concorrente
    AERODINAMICA.md  # Modelo por coeficientes, unidades, entradas, resultados e limitações
    ANALISE-DOSSIE-COMPLEMENTAR.md  # Auditoria editorial das lacunas, contradições e prioridades do dossiê técnico
    ARQUITETURA.md  # Visão geral das camadas, arquivos e materiais
    BLENDER.md  # Uso das coleções, Append, animação e materiais no Blender
    BOX-LABORATORIO.md  # Composição e reutilização do box procedural
    DESENVOLVIMENTO.md  # Instalação, build, servidor e testes
    DIREITOS-E-PROCEDENCIA.md  # Separa titularidade INTEIA de geometria fornecida e terceiros
    ESPECIFICACAO-ASSET-3D-SISTEMAS-F1.md  # Contrato de modelagem dos catorze sistemas internos do carro
    INTEGRACAO-MOTOR.md  # Operação e procedência da integração do carro final e motor
    INTEGRACAO.md  # Integração dos GLBs e fontes em outros projetos
    OUTRO-PC.md  # Instalação e sincronização segura entre computadores
    PILOTO-E-CAPACETE.md  # Referências, operação e limites do estudo do piloto
    PUBLICACAO.md  # Endereços públicos, atualização e evidência da publicação
    README.md  # Índice canônico da documentação do projeto
    REVISAO-TUNEL-VISUAL.md  # Revisões e limites da representação visual do fluxo
    SISTEMAS-3D.md  # Guia operacional da bancada Sistemas, do asset publicado e de sua regeneração
    SOBRESSALENTES.md  # Guia das peças sobressalentes do Box: cenários, slots, arquivos e regeneração
    VALIDACAO.md  # Síntese de testes históricos e limites por destino
    mapas/  # Documentação complementar da conversa paralela
      GRAFOS.md  # Diagramas Mermaid e leitura do grafo geral paralelo
      INVENTARIO.md  # Inventário legível de arquivos da conversa paralela
      MANUTENCAO.md  # Atualização e manutenção do gerador de mapas paralelo
      MODULOS.md  # Visão de módulos e responsabilidades do mapa paralelo
      PRODUCAO.md  # Pipeline de produção de assets documentado no mapa paralelo
      README.md  # Entrada do mapa geral produzido pela conversa paralela
      REUSO.md  # Receitas de reutilização do mapa geral paralelo
      VERIFICACAO.md  # Resultados de verificação registrados pela conversa paralela
      cobertura.json  # Contagens, escopo e exclusões do mapa paralelo
      componentes.json  # Catálogo de componentes GLB do mapa paralelo
      controles.json  # Índice de controles DOM extraído pelo gerador paralelo
      dependencias.json  # Relações de dependências extraídas pelo gerador paralelo
      graphify-extracao.json  # Extração graphify preservada pela conversa paralela
      index.html  # Interface navegável do mapa geral paralelo
      inventario.json  # Inventário estruturado de arquivos do gerador paralelo
    pesquisa-sistemas-carro-video.md  # Pesquisa e limites das referências usadas para os sistemas do carro
  documentacao/  # Metadados de peças e histórico visual
    Comparacao-iluminacao.html  # Comparação visual histórica de iluminação em HTML
    INTEIA-personalizacao.png  # Captura da personalização web em uma sessão anterior
    componentes-origem.json  # Metadados dos 97 componentes: IDs, categorias, pivôs, limites e sourceObject
    historico-avaliacoes.md  # Pareceres históricos e subjetivos sobre versões visuais
  ferramentas/  # Conversão, embalagem, validação e manifesto
    gerar_sistemas.py  # Pipeline de geração e otimização dos sistemas internos
    gerar_sobressalentes.py  # Gerador Blender das peças sobressalentes (pneus, asas, asa de viga, venezianas)
    manifest.cjs  # Calcula bytes e SHA-256 de 14 entregas e grava o manifesto
    mapa-template.html  # Template da interface do mapa geral da conversa paralela
    mapear.py  # Gerador do mapa geral da conversa paralela; saídas em docs/mapas
    merge-animation.cjs  # Reúne canais de animação do GLB animado em um único clipe
    otimizar_sistemas.mjs  # Pipeline de geração e otimização dos sistemas internos
    package_blender.py  # Importa base web e produz Blender mestre, texturas, GLBs e evidências
    package_garage.py  # Importa GLB do box e GLB estático do carro para compor uma cena Blender
    render_garage_preview.py  # Abre cena Blender do box e renderiza prévia
    sistemas/  # Documentação complementar da conversa paralela
      lib.py  # Biblioteca geométrica compartilhada pelos sistemas internos
      previews/  # Documentação complementar da conversa paralela
        aero-assoalho-por-baixo.png  # Prévia gerada para revisão visual de um sistema interno
        aero-bargeboards.png  # Prévia gerada para revisão visual de um sistema interno
        aero-difusor.png  # Prévia gerada para revisão visual de um sistema interno
        aero-drs.png  # Prévia gerada para revisão visual de um sistema interno
        aero-hero.png  # Prévia gerada para revisão visual de um sistema interno
        aero-side.png  # Prévia gerada para revisão visual de um sistema interno
        brakes-brake-by-wire.png  # Prévia gerada para revisão visual de um sistema interno
        brakes-canto-dianteiro.png  # Prévia gerada para revisão visual de um sistema interno
        brakes-canto-por-dentro.png  # Prévia gerada para revisão visual de um sistema interno
        brakes-hero.png  # Prévia gerada para revisão visual de um sistema interno
        brakes-pedaleira.png  # Prévia gerada para revisão visual de um sistema interno
        brakes-side.png  # Prévia gerada para revisão visual de um sistema interno
        cockpit-assento-arnes.png  # Prévia gerada para revisão visual de um sistema interno
        cockpit-hans.png  # Prévia gerada para revisão visual de um sistema interno
        cockpit-hero.png  # Prévia gerada para revisão visual de um sistema interno
        cockpit-hidratacao.png  # Prévia gerada para revisão visual de um sistema interno
        cockpit-pedais.png  # Prévia gerada para revisão visual de um sistema interno
        cockpit-side.png  # Prévia gerada para revisão visual de um sistema interno
        cooling-hero.png  # Prévia gerada para revisão visual de um sistema interno
        cooling-side.png  # Prévia gerada para revisão visual de um sistema interno
        cooling-sidepod-direito.png  # Prévia gerada para revisão visual de um sistema interno
        cooling-sidepod-esquerdo.png  # Prévia gerada para revisão visual de um sistema interno
        cooling-superior.png  # Prévia gerada para revisão visual de um sistema interno
        ers-energy-store.png  # Prévia gerada para revisão visual de um sistema interno
        ers-hero.png  # Prévia gerada para revisão visual de um sistema interno
        ers-inversor.png  # Prévia gerada para revisão visual de um sistema interno
        ers-mgu-k.png  # Prévia gerada para revisão visual de um sistema interno
        ers-side.png  # Prévia gerada para revisão visual de um sistema interno
        fuel-celula.png  # Prévia gerada para revisão visual de um sistema interno
        fuel-hero.png  # Prévia gerada para revisão visual de um sistema interno
        fuel-interior.png  # Prévia gerada para revisão visual de um sistema interno
        fuel-linhas.png  # Prévia gerada para revisão visual de um sistema interno
        fuel-side.png  # Prévia gerada para revisão visual de um sistema interno
        overview-hero.png  # Prévia gerada para revisão visual de um sistema interno
        power-escape-turbina.png  # Prévia gerada para revisão visual de um sistema interno
        power-hero.png  # Prévia gerada para revisão visual de um sistema interno
        power-plenum-trompetas.png  # Prévia gerada para revisão visual de um sistema interno
        power-side.png  # Prévia gerada para revisão visual de um sistema interno
        power-tres-quartos.png  # Prévia gerada para revisão visual de um sistema interno
        power-turbo-dianteiro.png  # Prévia gerada para revisão visual de um sistema interno
        power-vale-em-v.png  # Prévia gerada para revisão visual de um sistema interno
        safety-halo.png  # Prévia gerada para revisão visual de um sistema interno
        safety-hero.png  # Prévia gerada para revisão visual de um sistema interno
        safety-impacto-dianteiro.png  # Prévia gerada para revisão visual de um sistema interno
        safety-impacto-traseiro.png  # Prévia gerada para revisão visual de um sistema interno
        safety-retencao-roda.png  # Prévia gerada para revisão visual de um sistema interno
        safety-side.png  # Prévia gerada para revisão visual de um sistema interno
        sensors-antena.png  # Prévia gerada para revisão visual de um sistema interno
        sensors-ecu.png  # Prévia gerada para revisão visual de um sistema interno
        sensors-hero.png  # Prévia gerada para revisão visual de um sistema interno
        sensors-pitot.png  # Prévia gerada para revisão visual de um sistema interno
        sensors-roda.png  # Prévia gerada para revisão visual de um sistema interno
        sensors-side.png  # Prévia gerada para revisão visual de um sistema interno
        sistemas-v1-safety-cockpit-wheel.glb  # Asset GLB derivado dos módulos procedurais de sistemas
        sistemas-v1-safety-cockpit-wheel.manifest.json  # Manifesto de composição e métricas do GLB de sistemas correspondente
        sistemas-v1-wheel.glb  # Asset GLB derivado dos módulos procedurais de sistemas
        sistemas-v1-wheel.manifest.json  # Manifesto de composição e métricas do GLB de sistemas correspondente
        steering-coluna.png  # Prévia gerada para revisão visual de um sistema interno
        steering-cremalheira.png  # Prévia gerada para revisão visual de um sistema interno
        steering-hero.png  # Prévia gerada para revisão visual de um sistema interno
        steering-side.png  # Prévia gerada para revisão visual de um sistema interno
        steering-track-rod.png  # Prévia gerada para revisão visual de um sistema interno
        structure-antepara-traseira.png  # Prévia gerada para revisão visual de um sistema interno
        structure-celula.png  # Prévia gerada para revisão visual de um sistema interno
        structure-corte-sanduiche.png  # Prévia gerada para revisão visual de um sistema interno
        structure-hero.png  # Prévia gerada para revisão visual de um sistema interno
        structure-plank.png  # Prévia gerada para revisão visual de um sistema interno
        structure-side.png  # Prévia gerada para revisão visual de um sistema interno
        suspension-dianteira-inboard.png  # Prévia gerada para revisão visual de um sistema interno
        suspension-dianteira.png  # Prévia gerada para revisão visual de um sistema interno
        suspension-hero.png  # Prévia gerada para revisão visual de um sistema interno
        suspension-side.png  # Prévia gerada para revisão visual de um sistema interno
        suspension-traseira.png  # Prévia gerada para revisão visual de um sistema interno
        suspension-upright.png  # Prévia gerada para revisão visual de um sistema interno
        transmission-diferencial.png  # Prévia gerada para revisão visual de um sistema interno
        transmission-embreagem.png  # Prévia gerada para revisão visual de um sistema interno
        transmission-engrenagens.png  # Prévia gerada para revisão visual de um sistema interno
        transmission-hero.png  # Prévia gerada para revisão visual de um sistema interno
        transmission-lateral-corte.png  # Prévia gerada para revisão visual de um sistema interno
        transmission-side.png  # Prévia gerada para revisão visual de um sistema interno
        wheel-frente.png  # Prévia gerada para revisão visual de um sistema interno
        wheel-hero.png  # Prévia gerada para revisão visual de um sistema interno
        wheel-lateral.png  # Prévia gerada para revisão visual de um sistema interno
        wheel-side.png  # Prévia gerada para revisão visual de um sistema interno
        wheel-tras.png  # Prévia gerada para revisão visual de um sistema interno
      s01_aero.py  # Módulo procedural de um sistema interno do carro
      s02_structure.py  # Módulo procedural de um sistema interno do carro
      s03_suspension.py  # Módulo procedural de um sistema interno do carro
      s04_steering.py  # Módulo procedural de um sistema interno do carro
      s05_brakes.py  # Módulo procedural de um sistema interno do carro
      s06_power.py  # Módulo procedural de um sistema interno do carro
      s07_ers.py  # Módulo procedural de um sistema interno do carro
      s08_cooling.py  # Módulo procedural de um sistema interno do carro
      s09_fuel.py  # Módulo procedural de um sistema interno do carro
      s10_transmission.py  # Módulo procedural de um sistema interno do carro
      s11_safety.py  # Módulo procedural de um sistema interno do carro
      s12_cockpit.py  # Módulo procedural de um sistema interno do carro
      s13_wheel.py  # Módulo procedural de um sistema interno do carro
      s14_sensors.py  # Módulo procedural de um sistema interno do carro
    validate-kit.py  # Reabre Blender e GLBs para registrar verificações do pacote
  identidade/  # SVGs e guia de identidade
    INTEIA-monocromatico.svg  # Variante vetorial monocromática da marca INTEIA
    INTEIA-negativo.svg  # Variante vetorial da marca para fundo escuro
    INTEIA-principal.svg  # Marca vetorial principal com assinatura do laboratório
    INTEIA-simbolo.svg  # Símbolo compacto da identidade INTEIA
    Identidade-INTEIA.html  # Apresentação visual das versões da marca
    LEIA-ME.md  # Guia da identidade, versões e orientação de uso
  index.html  # Entrada pública que encaminha ao laboratório em web/
  manifesto-sha256.json  # Lista fechada com tamanho e hash de 14 entregas
  modelos/  # GLBs convertidos para distribuição
    INTEIA_F1_animado.glb  # Carro convertido com clipe ilustrativo de montagem, rodas e DRS
    INTEIA_F1_estatico.glb  # Carro convertido sem clipe para integração
  texturas/  # Texturas portáveis de entrega
    INTEIA_Carbono_BaseColor.png  # Textura de carbono portátil gerada pelo pipeline Blender
  validacao-criacao.json  # Registro histórico de criação do Blender e contagem do modelo
  validacao-mecanica-web.json  # Registro de ciclos, pivôs e erros de matrizes do teste mecânico
  validacao-reabertura.json  # Registro de reabertura Blender e reimportação de GLBs
  web/  # Aplicação autocontida e ferramentas Node
    THREE-LICENSE.txt  # Texto de licença de Three.js distribuído junto ao site
    assets/  # Base GLB operacional e wordmark avulso
      INTEIA-wordmark.svg  # Wordmark textual independente presente no pacote
      carro-aula-v2.glb  # Carro final otimizado do F1 Loop, 97 componentes
      carro-aula-v2.proveniencia.json  # Procedência e transformações do carro v2
      carro-aula-v2.validacao.json  # Validação original do carro v2
      carro-movable.glb  # Base exterior com 97 peças e metadados usada pelo build web e Blender
      inteia-escudo-oficial.svg  # Brasão oficial INTEIA
      inteia-nome-oficial.svg  # Assinatura oficial INTEIA
      inteligencia-mil-grau-transparent.png  # Arte do patrocínio Inteligência Mil Grau
      inteligencia-mil-grau.source.json  # Procedência da arte do patrocinador
      power-unit-v1.glb  # Motor V6 didático animado do F1 Loop
      power-unit-v1.manifest.json  # Geometria, animação, hash e licença do motor
      sistemas-v1.glb  # Asset GLB derivado dos módulos procedurais de sistemas
      sistemas-v1.manifest.json  # Manifesto de composição e métricas do GLB de sistemas correspondente
      sobressalentes-v1.glb  # Asset GLB das peças sobressalentes, um nó por peça com extras slot/variant/target/mode
      sobressalentes-v1.manifest.json  # Manifesto com slots, variantes, caixas e hash do GLB de sobressalentes
    build.cjs  # Empacota app e base64 do GLB no template para HTML autocontido
    index.html  # Site autocontido gerado: template, bundle Three.js e modelo embutido
    package-lock.json  # Versões e integridade das dependências npm
    package.json  # Scripts e versões fixadas de Three.js 0.180.0/esbuild 0.25.10
    server.cjs  # Servidor HTTP local da pasta web em PORT ou 5186
    src/  # Fontes editáveis da cena e interface
      aero-physics.mjs  # Calculadora pura por coeficientes: vento, densidade, forças e limites
      app-v2.js  # Entrada ativa: cena, GLB, módulos, controles DOM e loop de desenho
      branding.js  # Projeta uma assinatura vetorial INTEIA na lateral direita de main_body; chamado pela entrada ativa
      car-look.js  # Acabamento final, rodas, pneus e freios do carro
      customize.js  # Liga controles de cores/acabamento, luz, piso e fundo aos materiais
      engine/  # Documentação complementar da conversa paralela
        engine-shot.js  # Poses de referência para preparação gráfica do motor
        in-car.js  # Motor integrado, corte e tampa móvel
      flow-detail.js  # Representação didática aproximada do fluxo nas rodas e assoalho
      garage.js  # Constrói box, mobiliário, equipamentos, marcas e cena exportável
      helmet-1991.js  # Capacete detalhado compartilhado com o cockpit
      identity.js  # Define glifos, emblema, SVG e desenho Canvas da identidade ativa
      mechanics.js  # Agrupa peças, cria pivôs, explode/monta, seleciona e anima rodas/DRS
      parts-info.js  # Fichas didáticas das peças: nome, função e curiosidade por regra de rótulo
      senna-driver.js  # Piloto ilustrativo do carro final
      spares.js  # Catálogo e troca em tempo de execução das peças sobressalentes
      studio.js  # Materiais, carbono procedural, iluminação, ambiente, piso e tema
      surface-library.js  # Texturas de acabamento do carro final
      systems.js  # Carrega, apresenta e controla o GLB consolidado dos sistemas internos
      template-v2.html  # Estrutura e estilos da interface com marcadores __MODEL__ e __APP__
      tunnel-visual.js  # Construção visual do túnel, linhas/partículas e recursos de cena
      wind-tunnel.js  # Liga entradas do túnel, calculadora, gráficos, CSV e efeitos de fluxo
      workbench.js  # Abas, inspeção, ajustes e exportação dos modelos
    test-aerodynamics.mjs  # Verifica unidades, escala das fórmulas, condições e coeficientes ausentes
    test-driver-model.mjs  # Geometria e restauração do encaixe do piloto
    test-mechanics.mjs  # Verifica peças, pivôs, 20 ciclos, seleção, arraste e restauração
    test-power-unit.mjs  # Valida animação do motor em 20 ciclos
    test-spares.mjs  # Valida integridade do GLB de sobressalentes, coerência do catálogo e envelopes das peças
    test-systems.mjs  # Valida catálogo, controles, manifesto, hash e estrutura do GLB de sistemas
  docs/mapeamento-detalhado/  # Esta entrega: índice, HTML, catálogos, grafos e scripts
```

## Exclusões observadas

- `.git`: Metadados e objetos internos Git; revisão registrada via Git.
- `.impeccable`: Cache efêmero de sessão; ignorado pelo Git e sem valor arquitetural.
- `graphify-out`: Extração/cache da conversa paralela ou cache isolado desta análise.
- `docs/mapeamento-detalhado`: Esta entrega: inventário próprio em dados/entrega.json; evita autorreferência recursiva.
- `ferramentas/__pycache__`: Cache Python regenerável.
- `ferramentas/sistemas/__pycache__`: Cache Python regenerável.
- `web/node_modules`: Dependências instaladas; versões em package-lock.json.
