# Árvore comentada

[Índice](README.md) · [Catálogo](CATALOGO.md)

Diretórios de dependências, caches e Git são listados nas exclusões; não são expandidos. Esta documentação tem inventário próprio para evitar autorreferência.

```text
INTEIA-laboratorio-3d/
  .gitattributes  # Política de texto/LF, binários e supressão de diff do HTML empacotado
  .github/  # Automação de verificação remota
    workflows/  # CI de build/test
      verify.yml  # CI: instala dependências, constrói web e executa testes em Node 24
  .gitignore  # Exclusões de dependências, caches, backups Blender e dados de ambiente
  .nojekyll  # Habilita publicação estática direta pelo GitHub Pages
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
    ARQUITETURA.md  # Visão geral das camadas, arquivos e materiais
    BLENDER.md  # Uso das coleções, Append, animação e materiais no Blender
    BOX-LABORATORIO.md  # Composição e reutilização do box procedural
    DESENVOLVIMENTO.md  # Instalação, build, servidor e testes
    DIREITOS-E-PROCEDENCIA.md  # Separa titularidade INTEIA de geometria fornecida e terceiros
    INTEGRACAO.md  # Integração dos GLBs e fontes em outros projetos
    PUBLICACAO.md  # Endereços públicos, atualização e evidência da publicação
    REVISAO-TUNEL-VISUAL.md  # Revisões e limites da representação visual do fluxo
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
  documentacao/  # Metadados de peças e histórico visual
    Comparacao-iluminacao.html  # Comparação visual histórica de iluminação em HTML
    INTEIA-personalizacao.png  # Captura da personalização web em uma sessão anterior
    componentes-origem.json  # Metadados dos 97 componentes: IDs, categorias, pivôs, limites e sourceObject
    historico-avaliacoes.md  # Pareceres históricos e subjetivos sobre versões visuais
  ferramentas/  # Conversão, embalagem, validação e manifesto
    manifest.cjs  # Calcula bytes e SHA-256 de 14 entregas e grava o manifesto
    mapa-template.html  # Template da interface do mapa geral da conversa paralela
    mapear.py  # Gerador do mapa geral da conversa paralela; saídas em docs/mapas
    merge-animation.cjs  # Reúne canais de animação do GLB animado em um único clipe
    package_blender.py  # Importa base web e produz Blender mestre, texturas, GLBs e evidências
    package_garage.py  # Importa GLB do box e GLB estático do carro para compor uma cena Blender
    render_garage_preview.py  # Abre cena Blender do box e renderiza prévia
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
      carro-movable.glb  # Base exterior com 97 peças e metadados usada pelo build web e Blender
    build.cjs  # Empacota app e base64 do GLB no template para HTML autocontido
    index.html  # Site autocontido gerado: template, bundle Three.js e modelo embutido
    package-lock.json  # Versões e integridade das dependências npm
    package.json  # Scripts e versões fixadas de Three.js 0.180.0/esbuild 0.25.10
    server.cjs  # Servidor HTTP local da pasta web em PORT ou 5186
    src/  # Fontes editáveis da cena e interface
      aero-physics.mjs  # Calculadora pura por coeficientes: vento, densidade, forças e limites
      app-v2.js  # Entrada ativa: cena, GLB, módulos, controles DOM e loop de desenho
      branding.js  # Projeta uma assinatura vetorial INTEIA na lateral direita de main_body; chamado pela entrada ativa
      customize.js  # Liga controles de cores/acabamento, luz, piso e fundo aos materiais
      flow-detail.js  # Representação didática aproximada do fluxo nas rodas e assoalho
      garage.js  # Constrói box, mobiliário, equipamentos, marcas e cena exportável
      identity.js  # Define glifos, emblema, SVG e desenho Canvas da identidade ativa
      mechanics.js  # Agrupa peças, cria pivôs, explode/monta, seleciona e anima rodas/DRS
      studio.js  # Materiais, carbono procedural, iluminação, ambiente, piso e tema
      template-v2.html  # Estrutura e estilos da interface com marcadores __MODEL__ e __APP__
      tunnel-visual.js  # Construção visual do túnel, linhas/partículas e recursos de cena
      wind-tunnel.js  # Liga entradas do túnel, calculadora, gráficos, CSV e efeitos de fluxo
    test-aerodynamics.mjs  # Verifica unidades, escala das fórmulas, condições e coeficientes ausentes
    test-mechanics.mjs  # Verifica peças, pivôs, 20 ciclos, seleção, arraste e restauração
  docs/mapeamento-detalhado/  # Esta entrega: índice, HTML, catálogos, grafos e scripts
```

## Exclusões observadas

- `.git`: Metadados e objetos internos Git; revisão registrada via Git.
- `.mapas-worktree`: Checkout/worktree Git aninhado: cópia operacional do mesmo projeto, não é fonte adicional.
- `graphify-out`: Extração/cache da conversa paralela ou cache isolado desta análise.
- `ambientes/INTEIA_Box_com_carro.blend1`: Ambiente local, log, backup ou pacote duplicado; conteúdo não lido.
- `docs/mapeamento-detalhado`: Esta entrega: inventário próprio em dados/entrega.json; evita autorreferência recursiva.
- `web/node_modules`: Dependências instaladas; versões em package-lock.json.
