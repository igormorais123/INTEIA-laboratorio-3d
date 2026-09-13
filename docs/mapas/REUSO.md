# Reaproveitar o Laboratório 3D INTEIA

[Voltar ao mapa](README.md) · [Produção e exportações](PRODUCAO.md) · [Guia de integração anterior](../INTEGRACAO.md)

Este guia separa o que pode ser transportado como arquivo do que precisa ser integrado como código. As instruções partiram de `1ae4fd1` e o atlas foi atualizado sobre `e3d58af` (incluindo materiais/luzes de `0346e58` e a assinatura lateral). Consulte também [acabamento e render](../ACABAMENTO-E-RENDER.md): o box Blender recebeu novos materiais/luzes, enquanto o GLB estático do carro foi preservado. Os números de Blender citados abaixo pertencem aos relatórios já entregues; criar os mapas não executa uma nova conversão nem testa um motor de jogos.

O projeto tem [licença proprietária INTEIA](../../LICENSE). Reutilização depende das permissões aplicáveis ao conteúdo; o código público não concede uma licença geral. A geometria deriva do tutorial `F1_2026_tutorial_part7_textures.blend`, cujo original está ausente e cuja licença não foi documentada. Consulte [procedência](../DIREITOS-E-PROCEDENCIA.md) e [avisos de terceiros](../../THIRD-PARTY-NOTICES.md). Este guia descreve o caminho técnico, sem ampliar essas permissões.

## Escolher a unidade de reaproveitamento

| Objetivo | Começar por | O que acompanha / o que preparar no destino |
| --- | --- | --- |
| Mostrar a experiência completa | [web/index.html](../../web/index.html) | HTML gerado com aplicação e modelo incorporados; mantém controles. Hospedagem e acesso são decisões do destino. |
| Criar outro site com a mesma experiência | [web/src](../../web/src), [web/build.cjs](../../web/build.cjs), [base GLB](../../web/assets/carro-movable.glb) | Fonte modular, template e build; os módulos de interface usam IDs específicos do template. |
| Colocar o carro em uma cena própria | [GLB estático](../../modelos/INTEIA_F1_estatico.glb) | Geometria, materiais e hierarquia; sem clipe. Crie câmera, iluminação, interação e redimensionamento. |
| Mostrar a montagem gravada | [GLB animado](../../modelos/INTEIA_F1_animado.glb) | Clipe `INTEIA_Demonstracao_Montagem_Rodas_DRS`; não é dinâmica veicular. |
| Editar peças e materiais no Blender | [master Blender](../../INTEIA_F1_Master.blend) | Coleção do carro e estúdio separados, ações, pivôs e imagens empacotadas. |
| Usar o cenário sem o carro | [GLB do box](../../ambientes/INTEIA-box-laboratorio.glb) | Geometrias, materiais, luzes exportáveis e imagens das telas; configure a iluminação/reflexos no destino. |
| Editar box e carro estático juntos | [Blender do box](../../ambientes/INTEIA_Box_com_carro.blend) | Coleções separadas de box e carro; não contém a animação do GLB animado. |
| Usar apenas a marca | [guia e SVGs](../../identidade/LEIA-ME.md) | Versões principal, negativa, monocromática e símbolo; preserve proporções e permissões. |
| Usar calculadora por coeficientes | [aero-physics.mjs](../../web/src/aero-physics.mjs) | Equações puras e testes; dados de entrada precisam de procedência e faixa de validade. |

## Web: três caminhos práticos

### 1. Levar a entrega pronta

Copie [web/index.html](../../web/index.html) para a pasta de destino ou sirva esse arquivo por HTTP. O build incorpora `carro-movable.glb` em base64 e o pacote JavaScript no HTML. Não edite o HTML gerado para manter uma personalização: altere [o template](../../web/src/template-v2.html) ou os módulos e reconstrua.

O HTML pode ser embutido em uma página por `iframe`, com altura e título acessível definidos no site de destino. Essa é uma opção de integração, não um recurso adicional implementado neste kit. Verifique as restrições de conteúdo e download do site que hospedar o iframe. O projeto não inclui comunicação entre o iframe e a página hospedeira.

As cores e os acabamentos escolhidos ficam no estado da sessão. **Salvar imagem** produz um PNG. Não existe aqui um botão de exportar o carro personalizado como GLB, nem sincronização das escolhas com o master Blender. **Baixar box 3D** exporta somente o box; **Exportar ensaio CSV** exporta a tabela do ensaio por coeficientes. Fontes: manipuladores `#save-photo` e `#garage-export` em [app-v2.js](../../web/src/app-v2.js), `#air-export` em [wind-tunnel.js](../../web/src/wind-tunnel.js).

### 2. Desenvolver outra experiência a partir das fontes

Em uma cópia de trabalho destinada ao novo projeto, preserve inicialmente a pasta `web` inteira. Na raiz dessa cópia:

```powershell
npm --prefix web ci
npm --prefix web run build
npm --prefix web test
```

Para testar pelo servidor, escolha uma porta livre. No ambiente do autor, `127.0.0.1:5186` já serve uma pasta de entregas fora deste repositório; mantenha aquele processo. O exemplo abaixo usa 5190, que deve estar livre antes de iniciar:

```powershell
$env:PORT = '5190'
npm --prefix web run dev
```

O [servidor](../../web/server.cjs) usa a pasta `web` como raiz e escuta somente `127.0.0.1`. Não representa uma publicação na internet. A variável `PORT` vale para o terminal usado; preserve/restaure seu valor anterior se necessário.

| Responsabilidade a reaproveitar | Entrada existente | Dependências de integração |
| --- | --- | --- |
| Cena, câmera, importação e interface completa | [app-v2.js](../../web/src/app-v2.js) | Executa no carregamento; espera o DOM do template, `#model-data`, WebGL e APIs do navegador. Não é um componente com montagem/desmontagem pública. |
| Estúdio e materiais do carro | [studio.js](../../web/src/studio.js): `setupStudio(THREE, renderer, scene)` e `applyCarMaterials(THREE, model)` | O estúdio configura espaço de cor, ACES, sombras, piso, luzes e ambiente de reflexão. Material depende dos nomes originais. |
| Montagem e movimentos | [mechanics.js](../../web/src/mechanics.js): `createMechanics(model)` | Instancia registros e pivôs; preserve `assemblyComponent`, `sourceObject`, nomes e categorias. Chame `update(dt, now, reduced)` no ciclo de renderização, com `dt` em segundos e `now` em milissegundos. |
| Paleta e acabamento | [customize.js](../../web/src/customize.js): `setupCustomization(materials, studio, renderer, scene)` | Consulta diretamente IDs como `color-body`, `paint-finish` e `reset-style`. Preserve o DOM ou crie uma camada própria de controles. |
| Box procedural | [garage.js](../../web/src/garage.js): `createGarage({scene, renderer, studio, camera, mechanics})` | Espera piso/iluminação do estúdio, dados de mecânica e botão `garage-toggle`. `setEnabled`, `update` e `getExportScene` controlam o uso. |
| Túnel completo | [wind-tunnel.js](../../web/src/wind-tunnel.js): `createWindTunnel(...)` | Usa IDs do template, modelo, mecânica, câmera, estúdio e callbacks de troca de ambiente; atualize em cada quadro. |
| Fumaça e cena do túnel | [tunnel-visual.js](../../web/src/tunnel-visual.js): `createTunnelVisual(...)` | Shader e partículas Three.js, dimensões do carro, estado de cena e estúdio. Não são um asset GLB exportado. |
| Trajetórias por região | [flow-detail.js](../../web/src/flow-detail.js): `createFlowDetail({parent, size})` | Curvas e pulsos ilustrativos. `update` recebe resultados, validade, preferência de movimento reduzido e ajustes visuais. |
| Marca vetorial | [identity.js](../../web/src/identity.js): `brandSVG` e `drawBrand` | A primeira retorna SVG; a segunda desenha em Canvas. A interface e a placa do box usam essas funções. |

`mechanics.records` atribui `id` sequencial durante a leitura da hierarquia. Não presuma que o mesmo índice identifica a mesma peça depois de reordenar ou trocar o GLB. Ao migrar referências, compare `sourceObject`, nomes, categorias e [metadados de origem](../../documentacao/componentes-origem.json); `sourceObject` pode identificar mais de uma peça separada. Não remova os pivôs para simplificar a hierarquia sem também adaptar o controlador.

Alguns módulos oferecem `dispose`; a aplicação completa não possui uma API única de encerramento. Em sites com troca de páginas sem recarregar, implemente e teste a remoção do ciclo de animação, observadores, eventos e recursos GPU criados. Esse trabalho de integração ainda pertence ao projeto de destino.

[branding.js](../../web/src/branding.js) contém `applyInteiaBranding`, chamada pela entrada após a mecânica desde `e3d58af`. Aplica uma assinatura lateral única com os glifos de `identity.js` e prende o decalque à carroceria. Para reaproveitá-la, preserve os registros da mecânica e a geometria/nomenclatura esperadas; ela não é automaticamente incorporada ao GLB estático ou ao master Blender.

### 3. Importar somente um GLB em outro site

Use `GLTFLoader` para carregar o estático e acrescente `gltf.scene` à cena do destino. Para o animado, use `AnimationMixer`, escolha o clipe presente em `gltf.animations` e atualize o mixer com delta em segundos. Esse fluxo está descrito em [Integração](../INTEGRACAO.md); a aplicação entregue usa sua própria mecânica em vez desse clipe.

Não execute o clipe gravado e `createMechanics` simultaneamente sobre os mesmos objetos: ambos escrevem transformações. Escolha animação de demonstração ou controlador interativo. O GLB estático é o ponto de partida mais simples para implementar outro controlador.

Para carregar o GLB separadamente e aproveitar cache no site, altere deliberadamente o fluxo de `#model-data` e `GLTFLoader.parse` em [app-v2.js](../../web/src/app-v2.js), além do [build](../../web/build.cjs). O kit atual faz incorporação; transporte separado, compactação de geometria e carregamento progressivo não estão implementados.

## Jogos: preparar antes de integrar

1. Escolha o GLB estático para dirigibilidade própria ou o animado para uma demonstração visual. Verifique primeiro o importador glTF disponível na versão do motor escolhido.
2. Confira unidade, orientação, transformações e pivôs. GLB usa Y para cima e o arquivo Blender usa Z para cima; evite uma segunda conversão manual de eixos após o importador já convertê-los.
3. Confira materiais e texturas no motor, em especial verniz, transparência e carbono. O arquivo contém PBR, mas a interpretação das extensões e a iluminação do destino podem diferir.
4. Estabeleça o orçamento do jogo e produza LODs, colisores simples, retopologia e redução de materiais/texturas quando necessário. A entrega é detalhada: o [relatório de reabertura](../../validacao-reabertura.json) registrou 97 malhas e 752.823 triângulos nos exports. Não há versão low-poly ou colisores prontos.
5. Implemente dirigibilidade, suspensão, aderência e física de rodas no motor. Os pivôs visuais existentes não implementam esses sistemas.
6. Faça teste de escala, colisão, pivôs, animação, materiais, desempenho e memória no dispositivo-alvo. Registre motor, versão, importador e resultado antes de declarar compatibilidade.

Os [testes existentes](../VALIDACAO.md) não certificam Unity, Unreal ou Godot. Reimportar no Blender verifica aquele caminho, não todos os motores. O box pode ser cenário de apresentação; telas importadas são imagens estáticas, não telemetria funcional. Recrie a atualização das telas e a ocultação de paredes do [módulo web](../../web/src/garage.js) se elas fizerem parte da interação desejada.

## Blender: reutilizar sem perder a fonte

### Carro em um arquivo próprio

1. Abra seu projeto de destino e use **File > Append** no [master](../../INTEIA_F1_Master.blend).
2. Em **Collection**, escolha `INTEIA | Carro reutilizavel`. A coleção `INTEIA | Estudio (nao exportar para jogos)` contém piso, câmera e luzes; acrescente-a somente quando ela fizer parte da cena desejada.
3. Reposicione o conjunto pela raiz `INTEIA_F1`. Preserve `Direcao_front_*`, `Direcao_rear_*`, `Giro_*` e `Abertura_DRS` quando usar os movimentos. Confira propriedades `sourceObject`, `category`, `assemblyComponent` e `INTEIA_componente`.
4. Para poses manuais, remova/desvincule as ações dos objetos que editar ou trabalhe com o GLB estático. As ações existentes voltam a escrever as transformações ao mudar de quadro.
5. Edite materiais `Pintura` no Principled BSDF; carbono, pneus e rodas têm materiais separados. Salve o resultado com novo nome antes de fazer exportações.

A [documentação Blender](../BLENDER.md) registra Blender 4.5.9 LTS na produção/reabertura original. A timeline do master usa 30 fps: quadro 1 montado; 90–120 explodido; 210 remontado; 210–300 rodas/direção/DRS. A coleção e os materiais são marcados como assets por [package_blender.py](../../ferramentas/package_blender.py), permitindo também configurar uma biblioteca no Blender.

### Box e carro juntos

Abra [INTEIA_Box_com_carro.blend](../../ambientes/INTEIA_Box_com_carro.blend) ou faça Append das coleções `INTEIA | BOX E EQUIPAMENTOS` e `INTEIA | CARRO`. O script [package_garage.py](../../ferramentas/package_garage.py) centraliza o carro estático no piso a partir de sua caixa delimitadora e acrescenta câmera/luzes. Algumas luzes adicionais e a câmera ficam na coleção principal da cena, fora das duas coleções importadas; Append de apenas uma coleção não leva toda essa configuração de render.

O box já entregue registrou 568 malhas, 97 malhas do carro e 12 imagens incorporadas em [validacao-box.json](../../ambientes/validacao-box.json). Isso é evidência do pacote produzido; reconte e reabra depois de mudar a cena. A prévia é um render Cycles, não uma captura do navegador.

### Exportar do Blender

Selecione o carro e seus empties/pivôs, use exportação glTF/GLB com **Selected Objects** e preserve materiais e propriedades extras quando necessárias aos controles. Escolha conscientemente incluir ou excluir animações. Exporte em nova pasta; reimporte em uma sessão limpa, compare contagem, escala, materiais e remontagem. Os GLBs de carro entregues excluem o estúdio.

O master é uma reconstrução a partir do GLB derivado. Ele não contém a pilha original de modificadores do tutorial ausente. Executar novamente [package_blender.py](../../ferramentas/package_blender.py) substitui o master e não incorpora alterações manuais feitas nele. Escolha se a fonte do seu projeto será o master editado ou o processo de reconstrução, e mantenha a outra versão como entrega derivada. Veja [o mapa de produção](PRODUCAO.md).

## Aparência e física: o que não viaja automaticamente

O carbono web usa `applyLocalCarbonProjection` em [studio.js](../../web/src/studio.js), com projeção local em três planos e alteração de shader. O caminho Blender cria [uma textura portátil](../../texturas/INTEIA_Carbono_BaseColor.png) e UVs planares em [package_blender.py](../../ferramentas/package_blender.py). O estúdio web usa ACES; a cena Blender é configurada com AgX. Ajuste luz, exposição e material no destino usando o mesmo enquadramento para comparar; não espere identidade visual automática.

O túnel web divide calculadora por coeficientes e efeitos artísticos. O GLB não determina Cd, carga vertical, campo de pressão ou turbulência. Trajetórias, fumaça e cores por região não são CFD validada e não recalculam o escoamento da geometria. Se outro produto reaproveitar o túnel, preserve as explicações, a procedência dos coeficientes, os estados sem dados e os bloqueios de validade descritos em [Aerodinâmica](../AERODINAMICA.md).

## Aceitação da reutilização

Registre exatamente quais arquivos e revisão foram copiados, permissões/procedência, alterações realizadas e testes no destino. Para web, verifique carregamento, console, tela estreita, teclado, movimento reduzido, montar/desmontar/remontar, seleção, cores e restauração; percorra box → túnel → box e as exportações que mantiver. Para Blender e jogos, reimporte as entregas e confira escala, pivôs, materiais, animações e limites do destino. Atualize os mapas após adicionar novas fontes ou novos formatos.
