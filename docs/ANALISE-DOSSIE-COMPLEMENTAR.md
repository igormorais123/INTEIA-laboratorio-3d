# Análise complementar do dossiê técnico

> Atualização pós-patch (2026-09-16): a análise abaixo registrou o diagnóstico inicial. Depois da auditoria Astra, foram corrigidos a rotação local dos conjuntos animados, o arranjo didático célula–tanque–motor/bateria, a identificação temporal do MGU-H e a referência do cartão ERS. A validação continua sendo de código, testes e inspeção visual local; não é uma validação de engenharia.

## Resumo executivo

O dossiê é útil como lista de hipóteses e de pontos para inspeção, mas não pode ser tratado como laudo de engenharia reversa. Ele mistura rótulos/quadros observados no vídeo Animagraffs, interpretação geométrica, materiais e dimensões não demonstrados e um diagnóstico baseado em um estado antigo do código.

No estado conferido, `web/src/systems.js` já implementa o overlay procedural de 14 sistemas. A camada `power` representa um V6 didático com compressor frontal, turbina traseira, eixo comum, MGU-H legado, plenums e seis velocity stacks representativas; `ers` mantém os fluxos de energia, MGU-K e uma referência para o cartão “Motor V6 turbo”, além da alternância para 2026; `cooling`, `fuel`, `transmission`, `safety` e `cockpit` também existem como esquemas didáticos. Isso não transforma o overlay em CAD, modelo homologado ou validação do `power-unit-v1.glb`.

O `power-unit-v1.glb` permanece um asset separado, original e didático, explicitamente sem MGU-H. Portanto, há duas leituras que devem permanecer separadas: (a) overlay dos sistemas, que possui MGU-H legado alternável na camada `power`; (b) GLB da power unit, que não deve ser descrito como contendo MGU-H. O dossiê não autoriza substituir o GLB; a implementação posterior preservou esse limite.

## Pendências da auditoria e resolução

- **P1-A — resolvido no código e nos testes:** `addSpinner` agora aplica quaternion incremental no eixo local do objeto. O MGU-H, eixo comum do turbo, virabrequim, discos e eixos/engrenagens do câmbio usam o eixo local correspondente; um teste determinístico compara a direção mundial do eixo antes e depois de 240 passos.
- **P1-B — resolvido como hipótese espacial didática:** a survival cell foi ajustada ao envelope usado pela cena; combustível e contenção ficam centralizados longitudinalmente entre a célula e o power block; a energy store fica abaixo do tanque. Bombas, sensor, válvula, baffles, cintas, rota e labels foram movidos junto. Os testes verificam contenção, ordenação longitudinal, bateria abaixo e ausência de interpenetração com motor/bateria.
- **P2 — resolvido na interface:** Power exibe “MGU-H · LEGADO 2021” e “2026 · MGU-H REMOVIDO”; ERS aponta para o nome visível “Motor V6 turbo”. A referência histórica continua didática e alternável, não representa que o GLB original tenha MGU-H.

### Limitações que permanecem

Foi verificado visualmente na prévia local o funcionamento das telas **Power**, **Combustível** e **ERS**, incluindo a alternância histórica 2021/2026; a suíte também cobre os contratos numéricos dos envelopes. Não foi validado aparelho físico, desempenho, publicação pública, CAD, CFD, homologação, colisão estrutural, materiais, medidas exatas ou fidelidade completa ao vídeo. As dimensões do dossiê continuam classificadas como HIP/LIM quando não demonstradas por fonte primária ou pelo asset.

## Comparação por subsistema

Classificação usada: **OBS** = observável no vídeo; **CONF** = confirmado pela documentação já registrada ou pelo código atual; **HIP** = hipótese/interpretação; **LIM** = limite, versão ou ausência de prova.

| Subsistema | Alegação do dossiê | Estado atual | Evidência já registrada | OBS-CONF-HIP-LIM | Ação |
|---|---|---|---|---|---|
| Chassi / estrutura | `main_body` seria uma casca única oca e deveria virar três corpos estruturais parafusados. | O overlay tem `structure` como célula/survival cell esquemática; a pesquisa local diz que a base atual não estabelece monocoque real nem homologação. | `pesquisa-sistemas-carro-video.md`, “Estrutura e segurança” e “Estado atual”; `systems.js`, criação de `structure`. | OBS no vídeo; CONF quanto ao caráter didático; HIP quanto a três corpos e ancoragens; LIM sem CAD, medidas ou validação estrutural. | Manter como visualização. Só modelar corpos estruturais se houver fonte/procedência própria e contrato de asset definido. |
| Turbo / power unit | O projeto teria dois turbos ou um turbo traseiro e teria omitido MGU-H; o dossiê prescreve split-turbo com posições e materiais exatos. | O código atual usa um compressor e uma turbina em eixo comum e mantém o MGU-H legado na camada `power`; `ers` aponta para essa inspeção. Há um GLB separado sem MGU-H. | `systems.js`, bloco `power` e referência `ers`; `pesquisa-sistemas-carro-video.md`, “Motor” e “ERS”; manifesto do GLB citado no dossiê. | OBS/CONF para arquitetura didática e contexto histórico; HIP para posições, materiais, diâmetros e fidelidade interna; LIM pela diferença overlay/GLB e pela mudança 2026. | Patch aplicado: manter “overlay didático”, “MGU-H legado” e “GLB sem MGU-H” explícitos. |
| Admissão: plenums / trompetas | O frame 13:23 provaria dois plenums de carbono e seis trompetas de alumínio, com geometria interna específica. | O overlay já tem dois plenums e três stacks por lado, marcados como representativos/HIP; há dutos esquemáticos. | `pesquisa-sistemas-carro-video.md`, timestamp 13:23; `systems.js` linha 130 e descrição de `power`. | OBS para os rótulos “trumpets”/“plenums”; CONF para a implementação presente; HIP para quantidade, material, suspensão e equalização; LIM sem transcrição integral ou desenho interno. | Preservar rótulos de hipótese. Não chamar materiais, quantidade ou forma de “exatos”. |
| Suspensão / direção | A implementação teria braços genéricos sem push/pull-rod, rocker, torção ou heave; o dossiê exige cinemática detalhada. | O overlay contém wishbones, upright, pushrod/pullrod, rocker, damper, torsion bar, barra antirrolagem e heave como cadeia visual; os endpoints de push/pull agora têm contrato numérico e não formam um rig físico. | `systems.js` e `SUSPENSION_LAYOUT`; pesquisa local e fonte F1 de push-rod/pull-rod registradas em “Fontes”. | OBS/CONF para cadeia visual; HIP para movimento, perfil, cabos internos e centro de gravidade; LIM sem massas, rigidez, amortecimento, colisores ou carro específico. | Patch aplicado: dianteira inferior→rocker alto e traseira superior→rocker baixo no envelope do câmbio; manter estático/esquemático. |
| Freios / cubos | Rodas seriam fechadas e simples; o disco teria mais de 1.400 furos, pinça em 6 horas e dutos completos. | O overlay tem discos, pinças, anéis/dutos, dois circuitos e caminho regenerativo MGU-K; é representação ilustrativa. | `systems.js` linhas 114–121; pesquisa local, seção de frenagem e fonte F1 de brake-by-wire. | OBS/CONF para componentes e diagrama; HIP para 1.400 furos, posição exata, liga e detalhes de cubo; LIM sem referência de carro ou medição. | Não adicionar números/materiais do dossiê sem fonte. Usar “esquemático” e “regeneração conceitual”. |
| Refrigeração / sidepods | Os sidepods seriam vazios e deveriam receber intercooler esquerdo e três radiadores direitos, com inclinações e materiais determinados. | `cooling` já representa intercooler à esquerda, três trocadores à direita e quatro caminhos esquemáticos, todos marcados como HIP onde aplicável. | `systems.js` linhas 144–148; pesquisa local, “Refrigeração e fluidos”. | CONF para existência no overlay; HIP para assimetria física do carro, ângulos, matriz e materiais; LIM sem simulação térmica, pressão ou vazão. | Manter a assimetria como hipótese didática explicitamente rotulada; não apresentar como configuração universal de F1. |
| Combustível / bateria | O espaço atrás do piloto estaria vazio; o dossiê prescreve bladder de Kevlar, baffles, válvulas, capacidades e bateria sob o tanque. | `fuel` tem célula flexível compacta, contenção, baffles, bomba, sensor, breakaway e linha segura; o layout compartilhado coloca tanque entre survival cell e motor e a energy store abaixo, como hipótese didática. | `systems.js`, `POWER_FUEL_LAYOUT`, `SURVIVAL_CELL_LAYOUT` e testes de AABB; pesquisa local, “Combustível” e “ERS”; fonte FIA 2026 já registrada. | CONF para o esquema atual; HIP para Kevlar/borracha, capacidade, 6G, geometria e posicionamento real; LIM sem homologação nem asset físico. | Patch aplicado. Manter a ordenação como convenção visual do laboratório, sem tratá-la como medida homologada ou propriedade universal de F1. |
| Transmissão / diferencial | Não haveria câmbio completo; seriam necessários oito marchas, ré, diferencial e juntas tripóides com rolamentos específicos. | `transmission` já tem oito relações à frente, ré, eixos, diferencial, juntas tripóides esquemáticas e driveshafts; o código nega relações e rolamentos reais. | `systems.js` linhas 154–157; pesquisa local, “Câmbio, diferencial e transmissão”. | CONF para o esquema e contagem registrada; HIP para construção, rolamentos, seamless, relações e perdas; LIM sem dados de um carro específico. | Corrigir o diagnóstico stale. Preservar “esquemática/representativa” e não inferir desempenho mecânico. |
| Segurança / cockpit / piloto | O piloto não teria HANS, cinto contemporâneo, headrest e elementos de proteção; seria necessário reconstruir ergonomia. | `safety` tem halo, estruturas de impacto e três cabos didáticos por roda; `cockpit` tem arnês, FHR/HANS, apoio de cabeça, pedais e hidratação. | `systems.js` linhas 159–167; pesquisa local, “Estrutura e segurança” e “Cockpit”. | CONF para elementos presentes no overlay; OBS para a sequência geral do vídeo; HIP para materiais, número regulamentar, geometria e ergonomia; LIM sem ensaio de crash ou homologação. | Tratar a alegação como desatualizada. Fazer apenas revisão visual e de nomenclatura, sem alegar certificação. |
| Escala, câmeras e testes | O dossiê fixa `ENGINE_AT`, `ENGINE_LENGTH`, bounding boxes e “77 testes” como blindagem obrigatória para uma remodelagem. | Esses valores e a suíte não foram estabelecidos pelos quatro artefatos confrontados; o `systems.js` usa suas próprias coordenadas didáticas e não comprova esses contratos. | Pesquisa local limita a inspeção visual; doc de especificação remete a testes, mas a alegação não é evidência de resultado atual. | LIM: não confirmado neste confronto; HIP se usado apenas como requisito futuro; CONF somente após inspeção específica dos arquivos e execução dos testes. | Não repetir como fato. Validar separadamente manifestos, módulos de câmera e testes antes de qualquer alteração de asset. |

## Contradições e trechos stale

1. **“MGU-H omitido”**: contradiz o `systems.js` atual, que cria `mguh` como legado dentro de `power` e o oculta apenas no contexto 2026. A afirmação ainda pode ser verdadeira para o `power-unit-v1.glb`, mas não para o overlay.
2. **“Bi-turbo” ou “turbo único convencional traseiro”**: contradiz o bloco atual de `power`, que já separa compressor frontal e turbina traseira no mesmo conjunto didático.
3. **“Nó genérico `intake_plenum` sem detalhes”**: contradiz a implementação atual de dois plenums e seis stacks representativas, embora não prove a geometria real alegada.
4. **“Suspensão sem haste de acionamento”**: contradiz a presença explícita de `Pushrod` e `Pullrod`, rocker, damper e torsion bar no código atual.
5. **“Sidepods totalmente ocos”**: contradiz a camada `cooling`, que já contém a assimetria e aletas esquemáticas.
6. **“Espaço vazio atrás do piloto”**: contradiz a célula e a contenção presentes em `fuel`; não autoriza concluir que o GLB separado foi alterado.
7. **“Câmbio e diferencial ausentes”**: contradiz a camada `transmission`, já com 8 F + 1 R, diferencial e juntas tripóides didáticas.
8. **“Piloto sem segurança contemporânea”**: contradiz `safety` e `cockpit`, que já contêm halo, retenção, HANS/FHR e pedais.
9. **Especificações numéricas e materiais**: 25 mm, 40 mm, 110 mm, 1.400 furos, 145–150 L, 110 kg, 9 kg, 125.000 rpm, 120 kW/160 cv, 45°/40° e materiais específicos não devem migrar para o estado factual do projeto sem fonte primária específica. A própria pesquisa local classifica vários desses pontos como HIP ou LIM.

## Recomendações priorizadas

1. **Alta — manter a separação de artefatos e épocas (aplicado).** Documentar no produto que o overlay possui modo vídeo/2021 com MGU-H legado e modo atual/2026 sem MGU-H; manter o `power-unit-v1.glb` original, didático e sem MGU-H.
2. **Alta — corrigir documentação stale.** Rebaixar o diagnóstico de “falhas atuais” do dossiê para histórico/hipótese e apontar para o `systems.js` conferido.
3. **Alta — preservar proveniência.** Cada detalhe não diretamente visível ou confirmado deve permanecer marcado como OBS, CONF, HIP ou LIM, especialmente materiais, dimensões, quantidades e desempenho.
4. **Média — validação visual do overlay (aplicado no preview local).** Conferir os 14 sistemas na aba correspondente, com foco em ERS histórico/2026, power, cooling, fuel e transmission; verificar legibilidade, ancoragem e retorno de câmera.
5. **Média — validação automatizada específica (aplicado).** Executar a suíte existente e registrar o resultado real. Não afirmar “77 testes” ou “100%” apenas porque o dossiê prescreve esse critério.
6. **Baixa — expansão do asset.** Só depois de uma especificação de procedência, versão temporal e escopo do GLB; qualquer remodelagem deve preservar o caráter original e didático ou criar um asset explicitamente novo.

## Checklist de validação

- [x] Registrar que a análise documental não substitui o GLB; os patches posteriores alteraram somente `systems.js`, `test-systems.mjs`, o escopo do manifesto, a dica visual e a nomenclatura do checklist, preservando as demais alterações do checkout.
- [x] Confirmar no `systems.js` a existência dos 14 IDs e a presença de `power`, `ers`, `cooling`, `fuel`, `transmission`, `safety` e `cockpit`.
- [x] Verificar que o modo padrão do ERS referencia o MGU-H legado e que o modo 2026 o oculta, sem confundir isso com o GLB separado.
- [x] Verificar no manifesto do `power-unit-v1.glb` que o escopo continua original/didático e sem MGU-H, com a referência do overlay explicitada.
- [x] Abrir a aba de sistemas e conferir visualmente split-turbo, plenums/trompetas, refrigeração, fuel cell, transmissão, segurança e suspensão.
- [x] Executar os testes disponíveis em `web` e registrar o resultado observado, sem converter prescrição do dossiê em evidência.
- [x] Procurar no texto final números, materiais, homologação, desempenho ou geometria “exata” sem fonte; remover ou marcar como HIP/LIM.
- [x] Manter as fontes já registradas em `pesquisa-sistemas-carro-video.md`; não acrescentar pesquisa externa para preencher lacunas.

## Base documental usada

- [`docs/pesquisa-sistemas-carro-video.md`](./pesquisa-sistemas-carro-video.md): escopo, timestamps, convenções de evidência, contexto 2021/2026, fontes e limites.
- [`docs/ESPECIFICACAO-ASSET-3D-SISTEMAS-F1.md`](./ESPECIFICACAO-ASSET-3D-SISTEMAS-F1.md): diagnóstico histórico, hipóteses geométricas e checklist, lidos criticamente e não tratados como fonte independente.
- [`web/src/systems.js`](../web/src/systems.js): estado presente do overlay procedural.
- Dossiê fornecido em `pasted-text.txt`: alegações confrontadas, sem promoção automática de seus números, materiais ou prescrições a fatos.
