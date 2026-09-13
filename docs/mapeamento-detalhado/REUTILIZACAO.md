# Reutilização em sites, jogos e Blender


[Índice do mapeamento](README.md) · [Assets e procedência](ASSETS-E-PROCEDENCIA.md)

Este guia descreve os arquivos locais conferidos em **2026-09-13T01:37:41Z**, com `HEAD` **`e3d58af3c59a87b308444e678b0b25803e00e727`**. Fontes e assets finais incluem o acabamento revisado, a prévia concluída e a assinatura INTEIA aplicada ao carro no navegador. Restavam alterações locais de documentação/mapeamento, preservadas durante a leitura. As assinaturas estão em [Assets e procedência](ASSETS-E-PROCEDENCIA.md#assinaturas-da-conferencia). Os comandos abaixo são receitas para uma cópia de trabalho; não foram executados para produzir esta documentação. As validações Blender e de navegadores registradas por outras execuções são identificadas como evidências anteriores.

## Escolha do ponto de partida

| Objetivo | Arquivo real | O que acompanha | Limitação prática |
| --- | --- | --- | --- |
| Usar o laboratório completo offline | [web/index.html](../../web/index.html) | Interface, código empacotado, carro incorporado, construção do box e túnel | HTML gerado grande; não editar à mão |
| Alterar o laboratório | [web/src/app-v2.js](../../web/src/app-v2.js) e [template-v2.html](../../web/src/template-v2.html) | Fontes da integração e interface | Exige reconstrução do HTML |
| Colocar somente o carro montado em uma cena | [INTEIA_F1_estatico.glb](../../modelos/INTEIA_F1_estatico.glb) | 97 meshes, materiais portáteis, pivôs, metadados | Sem controlador ou interface |
| Reproduzir a apresentação de montagem | [INTEIA_F1_animado.glb](../../modelos/INTEIA_F1_animado.glb) | Um clipe, 104 canais; tempo exportado até 10 s | Ações ilustrativas; não é rig físico |
| Reaproveitar o controlador web de peças | [carro-movable.glb](../../web/assets/carro-movable.glb) + [mechanics.js](../../web/src/mechanics.js) | Hierarquia e metadados esperados pelo controlador | Não substituir por um GLB arbitrário sem adaptar o contrato |
| Editar o carro no Blender | [INTEIA_F1_Master.blend](../../INTEIA_F1_Master.blend) | Coleção do carro, materiais, animação e estúdio separado | Reconstruído do GLB; não contém a pilha original do tutorial |
| Reutilizar o cenário | [INTEIA-box-laboratorio.glb](../../ambientes/INTEIA-box-laboratorio.glb) | Box, equipamentos, imagens de telas e luzes exportadas | Sem carro e sem atualizações das telas |
| Editar o conjunto box + carro | [INTEIA_Box_com_carro.blend](../../ambientes/INTEIA_Box_com_carro.blend) | Box e carro estático em coleções distintas, câmera e luzes Cycles | Não contém a apresentação animada do master |
| Usar apenas a identidade visual | [identidade/LEIA-ME.md](../../identidade/LEIA-ME.md) e [identity.js](../../web/src/identity.js) | SVGs prontos e desenho compartilhado entre SVG/Canvas | Observar proporção, cores e atribuição documentadas |

A disponibilidade técnica não amplia permissões de uso. O repositório declara licença proprietária para as contribuições INTEIA e não documenta a licença do tutorial de origem. Consulte [LICENSE](../../LICENSE), [avisos de terceiros](../../THIRD-PARTY-NOTICES.md) e [Direitos e procedência](../DIREITOS-E-PROCEDENCIA.md). Esta seção registra o conteúdo desses arquivos; não resolve a licença de origem ausente.

## 1. Abrir ou modificar o site completo

O [README original](../../README.md) documenta a abertura direta de `web/index.html`. Esse arquivo já incorpora o GLB em base64 e o JavaScript em um pacote IIFE. Os módulos de origem não funcionam como aplicação apenas abrindo `app-v2.js`: dependem do template, do empacotamento e das dependências npm.

Pré-requisitos documentados: Node.js 24, npm, navegador com WebGL/aceleração gráfica. [package.json](../../web/package.json) fixa Three.js `0.180.0` e esbuild `0.25.10`; [package-lock.json](../../web/package-lock.json) registra a resolução instalada. Node 24 é a versão relatada na validação local, sem declaração de versão mínima `engines` no pacote.

Receita **a partir da raiz deste repositório**, em uma cópia própria destinada à edição:

```powershell
npm --prefix web ci
npm --prefix web run build
npm --prefix web test
$env:PORT = '5187'
npm --prefix web run dev
```

`5187` é um exemplo de porta alternativa; confirme que está livre. **Preserve `localhost:5186`: na sessão deste mapeamento, essa porta pertence à pasta `outputs` da conversa original, não ao servidor de `web`.** Não encerre o serviço existente para testar este projeto. O servidor deste repositório usa `PORT` ou o padrão `5186`, escuta somente `127.0.0.1` e serve a própria pasta `web`, conforme [server.cjs](../../web/server.cjs#L2).

Efeitos dos comandos: `ci` instala/recria dependências em `web/node_modules`; `build` sobrescreve `web/index.html`; os testes verificam comportamento e o teste mecânico grava `validacao-mecanica-web.json`. São operações de desenvolvimento, não necessárias para ler este mapeamento. O servidor não publica o site na internet.

[build.cjs](../../web/build.cjs#L2) resolve `src/...`, `assets/...` e `index.html` contra o diretório corrente. Use os comandos npm acima, que executam o script dentro de `web`; executar `node web/build.cjs` diretamente da raiz não respeita esse contrato. O [servidor](../../web/server.cjs#L2), por sua vez, resolve a raiz com `__dirname`.

### Onde editar para cada mudança

| Mudança | Fontes | Contrato a preservar |
| --- | --- | --- |
| Layout, textos, botões e acessibilidade | [template-v2.html](../../web/src/template-v2.html) | IDs usados por `app-v2`, `customize`, `wind-tunnel` e `garage`; marcadores `__MODEL__`/`__APP__` |
| Inicialização, seleção, câmera, comandos e exportações | [app-v2.js](../../web/src/app-v2.js) | Ordem de carregar modelo → materiais → personalização → mecânica → assinatura → ambientes |
| Montagem, deslocamento, rodas, direção, DRS | [mechanics.js](../../web/src/mechanics.js) | `assemblyComponent`, `sourceObject`, nomes/categorias e hierarquia |
| Pintura, carbono, pneus e iluminação do estúdio | [studio.js](../../web/src/studio.js) | Nomes de materiais reconhecidos e ambiente Three.js |
| Grupos de cor, acabamentos e restauração | [customize.js](../../web/src/customize.js) | `Pintura`, `wing`, `Rodas`, `Carbono` e IDs do template |
| Cenário, móveis, monitores e ocultação de paredes | [garage.js](../../web/src/garage.js) | Dependências de `scene`, `renderer`, `studio`, `camera`, `mechanics` e DOM |
| Identidade no cabeçalho, placa e carro | [identity.js](../../web/src/identity.js), [branding.js](../../web/src/branding.js) | `brandSVG()`, `drawBrand()` e os `glyphs` usados pelo decalque compartilham o desenho |
| Condições, CSV e visualização do túnel | [wind-tunnel.js](../../web/src/wind-tunnel.js), [tunnel-visual.js](../../web/src/tunnel-visual.js), [flow-detail.js](../../web/src/flow-detail.js) | Separar apresentação visual dos cálculos |
| Cálculos por coeficientes | [aero-physics.mjs](../../web/src/aero-physics.mjs) | Unidades, domínio de validade e coeficientes informados; não derivar CFD da malha |

A identidade ativa está no cabeçalho, na placa do box e em **uma assinatura branca na lateral direita da carroceria**. [app-v2.js](../../web/src/app-v2.js#L1) importa `applyInteiaBranding` de [branding.js](../../web/src/branding.js) e a chama depois de criar a mecânica, na [linha 49](../../web/src/app-v2.js#L49). O módulo importa `glyphs` de `identity.js`, desenha as letras em Canvas e projeta um decalque sobre `main_body`, anexando-o à peça móvel. O [SVG wordmark](../../web/assets/INTEIA-wordmark.svg) é um arquivo adicional e não a fonte desse decalque. A assinatura é criada em tempo de execução web; não foi incorporada aos GLBs ou aos arquivos Blender distribuídos.

Após alterar a aplicação, valide o HTML construído em navegador: carregamento das 97 peças, cores e restauração, montagem completa, seleção/isolamento/movimento, rodas/direção/DRS, box → túnel → box, imagem, exportação do box, teclado, tela estreita e preferência de movimento reduzido. Os testes não comprovam o resultado visual nem desempenho em outro equipamento.

## 2. Integrar somente o carro em outro site Three.js

Use inicialmente o [GLB estático](../../modelos/INTEIA_F1_estatico.glb) para controlador próprio ou o [GLB animado](../../modelos/INTEIA_F1_animado.glb) para a demonstração. Em seu projeto de destino, copie o arquivo escolhido para a pasta pública servida como `/assets/`, por exemplo `public/assets/INTEIA_F1_animado.glb`. Essa pasta de destino é uma convenção do exemplo, não uma pasta existente neste repositório.

Em um projeto Three.js com renderer, cena, câmera, luzes e redimensionamento já configurados, a integração mínima é:

```javascript
import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const gltf = await new GLTFLoader().loadAsync('/assets/INTEIA_F1_animado.glb');
scene.add(gltf.scene);
const mixer = new THREE.AnimationMixer(gltf.scene);
const clip = THREE.AnimationClip.findByName(
  gltf.animations, 'INTEIA_Demonstracao_Montagem_Rodas_DRS'
);
if (!clip) throw new Error('Clipe esperado ausente no arquivo carregado');
mixer.clipAction(clip).play();

// Dentro do loop existente, com deltaSeconds em segundos:
mixer.update(deltaSeconds);
```

`scene` e `deltaSeconds` pertencem à aplicação hospedeira. O exemplo explica a integração; não foi executado em um novo site nesta auditoria. Para o estático, carregue seu nome correspondente e omita o mixer. Não aplique o clipe e `createMechanics()` ao mesmo conjunto de peças, pois ambos escrevem transformações. O laboratório entregue usa `createMechanics()` sobre a base web, não o clipe do export animado ([app-v2.js, linhas 46–49](../../web/src/app-v2.js#L46)).

Os GLBs estão em glTF 2.0, com Y para cima; o registro da base define X lateral e +Z à frente. Os exports Blender preservam a conversão de eixo do glTF. Não aplique outra rotação corretiva sem observar a importação. Confira a escala em relação à cena de destino. A base registra limites aproximados de 1,847 m × 1,134 m × 5,107 m nos eixos X/Y/Z; isso descreve as coordenadas entregues, não dimensões homologadas de um veículo real.

### Se quiser os módulos do laboratório

- `setupStudio(THREE, renderer, scene)` cria piso, luzes e reflexos procedurais e altera a configuração do renderer. `applyCarMaterials(THREE, model)` adapta materiais e shaders. Ambos estão em [studio.js](../../web/src/studio.js).
- `createMechanics(model)` depende dos metadados da base. Carregue [carro-movable.glb](../../web/assets/carro-movable.glb), preserve seus `extras`, encaminhe comandos de seleção/movimento e atualize o controlador no loop. Compare a integração real em [app-v2.js](../../web/src/app-v2.js#L49) e [test-mechanics.mjs](../../web/test-mechanics.mjs).
- `setupCustomization(materials, studio, renderer, scene)` busca elementos por ID. Copiar o módulo exige copiar/adaptar a interface correspondente. As cores são agrupadas por nomes de material; renomear esses materiais afeta o funcionamento.
- `createGarage({scene, renderer, studio, camera, mechanics})` constrói o cenário em tempo de execução; `setEnabled()` e `update()` também acessam o DOM e os controles. Não é um componente sem dependências de interface.
- Para a assinatura do carro, execute `applyInteiaBranding(model, mechanics)` depois de `createMechanics(model)`, como na [entrada atual](../../web/src/app-v2.js#L49). Ela depende do registro `main_body`, Canvas/Path2D, Raycaster e DecalGeometry; retorna os decalques e uma função `dispose`. O novo mesh herda o movimento da peça à qual é anexado. O carregamento isolado de um GLB não executa esse módulo.
- A reutilização de `identity.js` em navegador precisa de SVG/Canvas; `drawBrand` usa `Path2D`. Um motor de jogos recebe o SVG convertido em textura ou as imagens do GLB, não a função de Canvas.

Use a versão Three.js fixada pelo projeto como referência inicial e teste qualquer atualização. Materiais com código `onBeforeCompile`, reflexos PMREM e efeitos de pós-processamento não se transformam automaticamente em materiais de outro motor ou em um GLB equivalente.

### O que as exportações web guardam

| Ação existente | Saída | Preserva | Não preserva |
| --- | --- | --- | --- |
| Salvar imagem | `INTEIA-design-3D.png` | Pixels do enquadramento e visual atual | Geometria editável, presets de material ou sessão |
| Baixar box 3D | `INTEIA-box-laboratorio.glb` | Cópia do grupo do box, paredes visíveis, imagens atuais dos monitores | Carro, interface, lógica das telas, ambiente PMREM da cena |
| Exportar ensaio CSV | Arquivo de dados do ensaio | Valores e parâmetros produzidos pela calculadora | CFD, campo de pressão, validação aerodinâmica da geometria |

A imagem usa `renderer.domElement.toDataURL`, sem caixa de seleção/gizmo ([app-v2.js, linha 75](../../web/src/app-v2.js#L75)). O export do box usa `garage.getExportScene()` e `GLTFExporter` ([linha 56](../../web/src/app-v2.js#L56)); a função clona o grupo e torna seus objetos visíveis ([garage.js, linha 148](../../web/src/garage.js#L148)). Não há botão de exportação do carro personalizado nem persistência dos presets de cores; escolhas posteriores no navegador não atualizam o `.blend` distribuído.

Para implantação web de produção, a alternativa de carregar GLB por URL, com cache e compressão de transporte, é uma adaptação proposta em [Desenvolvimento](../DESENVOLVIMENTO.md#L15). O build atual ainda entrega um único HTML com base64, não esse fluxo separado.

## 3. Reutilizar no Blender

Pré-requisito documentado: Blender 4.5; o guia original registra produção e reabertura no 4.5.9 LTS. Esta análise não abriu novamente os `.blend`; conferiu os scripts, hashes e relatórios existentes.

1. Faça uma cópia de [INTEIA_F1_Master.blend](../../INTEIA_F1_Master.blend) para edições próprias, ou use **File > Append** no seu projeto.
2. Em `Collection`, escolha **INTEIA | Carro reutilizavel**. O estúdio está em **INTEIA | Estudio (nao exportar para jogos)** e só é necessário para piso, câmera e luzes.
3. Mova a raiz **INTEIA_F1** para reposicionar o carro inteiro. Preserve os pivôs `Direcao_*`, `Giro_*` e `Abertura_DRS` se utilizar suas animações.
4. Para modificar a malha e seus materiais, mantenha a cópia do master; as imagens utilizadas estão empacotadas segundo [validacao-reabertura.json](../../validacao-reabertura.json). Coleção e materiais são marcados como assets pelo script de criação.
5. Ao editar posições, desvincule/desative as ações que possam sobrescrever transformações. O GLB estático importado fornece uma alternativa sem ações.

Timeline do master: 30 fps, quadros 1–300; 1 montado, 90–120 explodido, 120–210 remontagem, 210–300 rodas/direção/DRS. A comprovação registrada verifica 97 peças deslocadas no quadro 90 e retorno sem erro de matriz no 210. Essa checagem não comprova articulação física ou uma sequência real de manutenção.

Para reutilizar apenas o box, importe seu GLB. Para a cena pronta, abra [INTEIA_Box_com_carro.blend](../../ambientes/INTEIA_Box_com_carro.blend); as coleções se chamam **INTEIA | BOX E EQUIPAMENTOS** e **INTEIA | CARRO**. São nomes diferentes dos existentes no master. O carro foi centralizado e apoiado no piso pelo empacotador do box; não se deve presumir a mesma posição global do arquivo de origem. A cena combina 568 malhas do box e 97 do carro conforme o relatório de criação, com imagens empacotadas e sem imagens externas listadas.

### Materiais e aparência

Edite Base Color, Metallic, Roughness e Coat no Principled BSDF. Os exports preservam famílias de materiais como Pintura, Carbono, Rodas, Pneus, Borracha, Aço, Vidro, mirror e Volante. O carbono do master e dos exports do carro usa [INTEIA_Carbono_BaseColor.png](../../texturas/INTEIA_Carbono_BaseColor.png), gerada em 256 × 256 e aplicada com UVs planares. O navegador usa textura procedural e projeção em três planos no shader. Cycles/AgX, Three.js/ACES e importadores de jogos podem diferir em reflexos, exposição, verniz, transparência e textura.

O acabamento atual do box está documentado em [ACABAMENTO-E-RENDER.md](../ACABAMENTO-E-RENDER.md). O [empacotador atualizado](../../ferramentas/package_garage.py#L24) limpa conexões de textura dos canais da pintura, usa Roughness `0.21`/Coat Roughness `0.065`, cria ruído/bump nos pneus e bevel de sombreamento em metais, remove as luzes importadas e monta cinco luzes de área. Esses efeitos de nós Blender não são incluídos automaticamente no GLB estático original do carro. Esse GLB e o master mantêm seus hashes anteriores; a revisão de acabamento do Blender está no arquivo combinado do box.

Para exportar o carro editado, selecione a coleção do carro com seus empties/pivôs; escolha glTF/GLB, **Selected Objects**, materiais e propriedades extras se precisar de procedência. Ative animações apenas quando desejado. Dê um nome novo à saída. No script distribuído, piso/câmera/luzes do estúdio são criados somente depois dos exports, ficando fora dos GLBs do carro ([package_blender.py, linhas 125–139](../../ferramentas/package_blender.py#L125)).

## 4. Reaproveitar em jogos

Use o GLB estático para um controlador do motor ou o animado para uma apresentação. A documentação existente afirma reimportação em Blender; **não registra teste em Unity, Unreal ou Godot**. O importador, extensões suportadas e pipeline de materiais da versão escolhida precisam ser verificados no projeto de destino. Este mapeamento não acrescenta uma homologação desses motores.

Receita de adaptação:

1. Importe uma cópia do GLB, confira 97 meshes, escala/eixos, origem, transparências e o clipe quando aplicável.
2. Crie uma cena/prefab própria que mantenha o identificador `partId` ou uma tabela correspondente. Evite associar peças somente pela posição na lista.
3. Defina orçamento de geometria, materiais, texturas, memória e draw calls; a malha do carro exportado contém **752.823 triângulos**, sem LODs, versão low-poly ou colisores prontos.
4. Produza LODs/retopologia e colisores simples conforme o uso. Essa preparação é trabalho de destino; não está incluída nos assets entregues. O box exportado tem 568 meshes e **128.860 triângulos**, também exigindo avaliação de custo.
5. Implemente física de rodas, direção, suspensão e colisões no motor se o jogo precisar delas. Os pivôs e a animação existente apenas ilustram movimentos.
6. Substitua a interface web por UI do motor. Telas exportadas do box são imagens; dados dinâmicos exigem nova implementação. Configure luzes/reflexos do destino.
7. Valide desempenho e aparência no equipamento alvo e compare a preservação das peças e do retorno da animação. O sucesso em Blender ou no computador original não determina FPS no jogo.

A carroceria principal é uma casca exterior conectada. Não há motor completo, câmbio interno, banco de cockpit estabelecido pela fonte, sistema hidráulico funcional nem geometria interna de todos os painéis. A visualização do túnel usa trajetórias ilustrativas. As equações usam coeficientes informados; não há CFD resolvida sobre a malha, calibração aerodinâmica automática ou fidelidade física comprovada.

## 5. Reconstruir os derivados sem perder edições

O ponto inicial reproduzível é [web/assets/carro-movable.glb](../../web/assets/carro-movable.glb). O original `F1_2026_tutorial_part7_textures.blend` e o separador inicial não são distribuídos. A reconstrução abaixo não recupera a pilha de modificadores original.

Execute somente em uma cópia dedicada à geração, a partir da raiz do repositório, depois de preservar edições manuais nos arquivos de destino:

```powershell
blender -b --python ferramentas/package_blender.py
node ferramentas/merge-animation.cjs
blender -b --python ferramentas/validate-kit.py
```

O primeiro comando reinicia a cena Blender do processo, lê a base web e sobrescreve os dois GLBs, o master, a textura de carbono, a prévia e `validacao-criacao.json`. O segundo regrava o GLB animado unindo canais num clipe. O terceiro reabre master/GLBs e regrava `validacao-reabertura.json`. Rodar esses scripts não preserva edições manuais anteriores no master nem o visual personalizado numa sessão web.

Para reconstruir a cena do box, primeiro produza/confira o GLB do ambiente usando **Baixar box 3D** na aplicação da revisão desejada e coloque deliberadamente essa saída no caminho `ambientes/INTEIA-box-laboratorio.glb` da cópia de geração. O npm build não atualiza esse arquivo. Depois:

```powershell
blender -b --python ferramentas/package_garage.py -- .
blender -b --python ferramentas/render_garage_preview.py -- .
```

Os dois scripts recebem a pasta do projeto após `--`; `.` funciona porque a receita parte da raiz. O primeiro importa o box e o carro estático, adapta pintura/luzes/câmera e sobrescreve `ambientes/INTEIA_Box_com_carro.blend` e `ambientes/validacao-box.json`. O segundo reabre esse `.blend` e sobrescreve `ambientes/Previa-Box.png`. O script atual usa **64 amostras, denoising, 1600 × 1000 e seis threads fixas** ([linha 5](../../ferramentas/render_garage_preview.py#L5)); o empacotador configura amostragem adaptativa e Cycles em 128 amostras. A prévia final [Previa-Box.png](../../ambientes/Previa-Box.png) está disponível em **1600 × 1000**, com **2.189.120 bytes**; suas dimensões, bytes e hash foram conferidos em 2026-09-13T01:37:41Z. O uso de 64 amostras na prévia e de 128 na configuração da cena está documentado em [Acabamento e render](../ACABAMENTO-E-RENDER.md#L9).

Ao terminar todos os artefatos, confira visualmente e atualize o manifesto:

```powershell
node ferramentas/manifest.cjs
```

Na conferência **2026-09-13T01:37:41Z**, **as 14 entradas do manifesto corresponderam aos bytes e SHA-256 dos arquivos atuais**. O manifesto cobre uma lista fixa de **14 artefatos**, não todos os arquivos do repositório; a lista está em [manifest.cjs](../../ferramentas/manifest.cjs). Novos assets exigem decisão explícita de inclusão nessa lista. Hashes detectam mudança de bytes, não corrigem nem certificam visual, licença ou física.

### Dependências fixas que precisam de adaptação

| Trecho | Dependência fixa | Consequência ao trocar os assets |
| --- | --- | --- |
| [package_blender.py, linhas 82–93](../../ferramentas/package_blender.py#L82) | `front_tire`, `rear_tire`, `rear_wing_drs`, nomes de capas, lados pelo centro X | Ausência/renomeação pode falhar em `next()` ou produzir pivôs incorretos |
| [package_blender.py, linhas 97–108](../../ferramentas/package_blender.py#L97) | `sourceObject`, categoria, posição e regras de deslocamento | Outra geometria requer revisão de trajetórias e escala |
| [validate-kit.py](../../ferramentas/validate-kit.py) | Exatamente 97 peças, quadros 90 e 210, nomes dos dois exports | Não é validador genérico de qualquer asset |
| [merge-animation.cjs](../../ferramentas/merge-animation.cjs) | Caminho e estrutura de animações do GLB animado | Regrava o arquivo no lugar; assume animações disponíveis |
| [package_garage.py, linhas 4–12](../../ferramentas/package_garage.py#L4) | Argumento após `--`, nomes de box e carro estático | Argumento ausente ou arquivos renomeados interrompem a geração |
| [customize.js, linhas 4–8](../../web/src/customize.js#L4) | Nomes dos materiais e grupos | Renomear pode retirar peças dos controles de cor |
| [build.cjs](../../web/build.cjs) | Diretório `web`, entrada `app-v2`, template e base fixos | Use npm com `--prefix web`; editar o HTML gerado perde-se no próximo build |

Para atualizar este guia, compare importações, scripts, contratos dos metadados e contagens atuais; execute apenas as verificações pertinentes à alteração. A reprodução da documentação e a reprodução dos assets são processos distintos. Consulte o [índice](README.md) para o procedimento do mapeamento.
