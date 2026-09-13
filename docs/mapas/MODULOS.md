# Responsabilidades, entradas e contratos

[Índice](README.md) · [Símbolos e linhas](INVENTARIO.md) · [Grafo de imports](GRAFOS.md)

Atualizado sobre `e3d58af`, que também incorpora `0346e58`. A [revisão de acabamento e render](../ACABAMENTO-E-RENDER.md) detalha verniz, metais, luzes de área e diferenças entre o box Blender atual e o GLB estático preservado.

## Entradas e montagem da aplicação

[web/package.json](../../web/package.json) fixa Three.js 0.180.0 e esbuild 0.25.10. [build.cjs](../../web/build.cjs#L2) empacota `src/app-v2.js` em IIFE, substitui `__APP__` e incorpora `assets/carro-movable.glb` em base64 no `__MODEL__` do [template](../../web/src/template-v2.html). O resultado é [web/index.html](../../web/index.html), uma entrega gerada. Alterações de fonte exigem novo build; editar somente o HTML final será perdido no próximo build.

[server.cjs](../../web/server.cjs) serve a pasta `web` com Node, host 127.0.0.1 e porta definida por `PORT`, padrão 5186. A porta não identifica o conteúdo: na sessão de mapeamento, 5186 já pertencia a uma pasta de outputs externa. Preserve esse servidor e escolha outra porta livre para este clone.

[app-v2.js](../../web/src/app-v2.js#L18) depende do DOM completo, de `matchMedia`, canvas/WebGL e do GLB incorporado. Cria renderer, câmera, estúdio, pós-processamento, OrbitControls e TransformControls; carrega o GLB, centraliza o carro no piso, aplica materiais, instala personalização e mecânica, aplica a assinatura lateral, cria o box ativo e prepara o túnel desativado. O laço `setAnimationLoop` atualiza mecânica, câmera, controles, estúdio, box e túnel e escolhe o renderer ou o composer.

## Módulos e dependências práticas

| Fonte / símbolo | Responsabilidade | Contrato e limite de reuso |
| --- | --- | --- |
| [mechanics.js / createMechanics](../../web/src/mechanics.js#L3) | Registros das peças, pivôs, explosão, seleção, isolamento, deslocamento, direção, giro e DRS | Requer cena Three e metadados/nomenclatura do GLB. Não depende de DOM. A fábrica reorganiza os pais das peças e grava `recordId` nos meshes. |
| [studio.js / setupStudio](../../web/src/studio.js#L2) | PMREM procedural, luzes, sombras, piso, tema e exposição | Requer renderer e cena; fornece `floor`, `setTheme` e `update`. Não é um arquivo HDRI externo. |
| [studio.js / applyCarMaterials](../../web/src/studio.js#L146) | Acabamentos PBR, textura procedural e projeção local do carbono | Classificação por nome do material; shader via `onBeforeCompile` não se transfere automaticamente para glTF/Blender. |
| [customize.js / setupCustomization](../../web/src/customize.js#L1) | Grupos body/wings/wheels/carbon, paletas, quatro acabamentos, luz, piso, fundo e restauração | Acoplado aos IDs do template, aos nomes de materiais e à classe `dark` no body. Cores ficam na sessão. |
| [identity.js / brandSVG e drawBrand](../../web/src/identity.js) | Assinatura vetorial do cabeçalho e desenho da marca em canvas | Geometria dos glifos declarada no JS. O box importa `drawBrand`; app importa `brandSVG`. Os SVGs de entrega não são importados por essas funções. |
| [branding.js / applyInteiaBranding](../../web/src/branding.js#L6) | Assinatura lateral única em decalque com DecalGeometry | Ativo desde `e3d58af`: app chama a fábrica após createMechanics. Importa glyphs de identity.js, desenha em canvas e anexa o decalque à carroceria móvel. Não carrega o SVG wordmark legado. |
| [garage.js / createGarage](../../web/src/garage.js#L6) | Geometria de box, mobiliário, equipamentos, rótulos em canvas, iluminação e ambiente refletido | Depende de Three, RoundedBoxGeometry, identity, estúdio, câmera, mecânica e DOM. Monitores de setup leem o estado da aplicação; outras telas são ilustrativas. |
| [wind-tunnel.js / createWindTunnel](../../web/src/wind-tunnel.js#L4) | Controles do ensaio, chamadas numéricas, setas, gráfico, avisos, CSV e alternância do ambiente | Depende da mecânica e DOM; bloqueia forças sem coeficientes válidos, com peças deslocadas/isoladas ou Mach fora da faixa. |
| [aero-physics.mjs / aerodynamicTest](../../web/src/aero-physics.mjs#L2) | Função pura de vento relativo, densidade, pressão dinâmica, Mach/Reynolds e forças por coeficientes | Sem Three e sem DOM. Área, Cd e carga descendente são entradas; não são extraídos da malha. Não modela efeito físico de DRS/direção. |
| [tunnel-visual.js / createTunnelVisual](../../web/src/tunnel-visual.js#L4) | Ambiente do túnel, fumaça procedural, materiais, iluminação e visibilidade conforme a câmera | Importa flow-detail. Recebe velocidade/ângulo para orientar e animar uma ilustração; não resolve campos na geometria. |
| [flow-detail.js / createFlowDetail](../../web/src/flow-detail.js#L4) | Curvas predefinidas, setas/pulsos, regiões de carroceria, rodas e assoalho | Curvas CatmullRom e amostragem visual; cores distinguem regiões, não pressão medida. |

## Contrato das peças

A base [carro-movable.glb](../../web/assets/carro-movable.glb) contém `assemblyComponent`, `sourceObject`, `partId`, `category`, `label` e limites geométricos em `extras`. [componentes-origem.json](../../documentacao/componentes-origem.json) guarda a separação inicial e caminhos históricos `outputs/...`; esses caminhos não são dependências resolvidas neste clone. A etapa que produziu essa separação não está presente nas ferramentas atuais.

`createMechanics` procura raízes com `assemblyComponent`; na ausência usa os filhos do modelo. A seleção da interface usa índices de `records` criados no carregamento, que não devem ser tratados como IDs persistentes entre novos modelos. Para localizar peças entre arquivos, prefira `partId` e confira unicidade. O [catálogo gerado](componentes.json) prova a correspondência entre o documento e o GLB base.

As quatro rodas recebem pivôs de direção e giro. Coberturas internas acompanham o suporte de direção, sem girar com o pneu. A asa `rear_wing_drs` recebe um pivô próprio. Qualquer explosão ou deslocamento manual suspende movimentos articulados; `restoreParts` e `reset` restauram o estado dentro dos testes existentes. Isso organiza a geometria externa; não representa uma sequência técnica de manutenção.

## Controles e seus donos

| Grupo | Controles / eventos | Dono |
| --- | --- | --- |
| Câmera | `data-view`, orbit, zoom, raycast, foco da peça, Home, Escape, setas, +/− | app-v2 + OrbitControls |
| Montagem | assembly, assemble, explode, loop, reset | app-v2 → mechanics |
| Peças | part-select, part-offset, isolate, clear-selection, free-move | app-v2 → mechanics + TransformControls |
| Movimento | spin, steering, drs; bloqueio por motionAvailable | app-v2 → mechanics |
| Visual | cores por grupo, paint-finish, light-level, floor-color, background-color, reset-style | customize → materiais/estúdio |
| Apresentação | theme, wire, quality, photo, save-photo | app-v2 + studio |
| Box | garage-toggle, garage-view, garage-export | app-v2 → garage |
| Túnel | wind-toggle, air-*, flow-detail, flow-region, smoke-* | wind-tunnel → física/tunnel-visual/flow-detail |
| Cinema / assoalho | wind-cinema, região floor e transparência temporária | app-v2 por callbacks onRegion/onToggle |

O [índice de controles](controles.json) vincula cada ID real do template às ocorrências literais no código. Acessos construídos por concatenação (`color-` + grupo, `smoke-` + chave) não são resolvidos automaticamente. Os controles de teclado da câmera exigem foco no canvas. `prefers-reduced-motion` é consultado em transições e animações; este mapa não substitui uma auditoria de acessibilidade de toda a interface.

## Exportações e testes

`save-photo` cria PNG do canvas com seleção e gizmo temporariamente ocultos; não exporta HTML/UI nem preferências editáveis. `garage-export` usa GLTFExporter sobre `garage.getExportScene()`: clone do box com nós visíveis, sem anexar o carro. `air-export` produz CSV de um modelo por coeficientes com indicação da origem hipotética ou fornecida pelo usuário. Os fluxos são rastreados no [guia de produção](PRODUCAO.md).

[test-mechanics.mjs](../../web/test-mechanics.mjs) carrega a base GLB, testa pivôs e 20 ciclos, restauração, isolamento e arraste; grava a evidência mecânica na raiz. [test-aerodynamics.mjs](../../web/test-aerodynamics.mjs) verifica unidades, escalas V²/V³, vento relativo, densidade, limites e ausência de coeficientes. O [workflow](../../.github/workflows/verify.yml) instala dependências, compila e executa os testes. Relatórios antigos do Blender e screenshots são evidência da execução registrada, não certificação de um export futuro.
