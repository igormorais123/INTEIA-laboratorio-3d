# Auditoria de aderência à especificação F1 2026

**Data:** 16/09/2026  
**Escopo:** somente leitura do projeto `C:\Users\igorm\projetos\INTEIA-laboratorio-3d`, comparado com `C:\Users\igorm\projetos\inteia-f1-loop\ESPECIFICACAO_MODELAGEM_F1_3D.md`.  
**Regra:** este documento separa observação do código de recomendação. Nenhuma geometria simplificada é tratada como CAD, homologação ou validação de engenharia.

## 1. Como os caminhos foram validados

O arquivo de especificação existe no caminho informado. Os caminhos citados dentro dele (`src/engine/hybrid-kit.js`, `src/car/internals-kit.js`, `materia-prima/modulos-atualizados/mechanics.js` etc.) pertencem ao repositório `inteia-f1-loop` e também existem nesse repositório de referência.

No projeto auditado, os equivalentes reais são:

| Função | Caminho real no projeto auditado | Situação |
| --- | --- | --- |
| Entrada da aplicação | `web/src/app-v2.js` | existe e é importada pelo build |
| Mecânica externa | `web/src/mechanics.js` | existe |
| Camadas internas didáticas | `web/src/systems.js` | existe |
| Motor sob demanda | `web/src/engine/in-car.js` | existe |
| Câmera do motor | `web/src/engine/engine-shot.js` | existe |
| Física aerodinâmica didática | `web/src/aero-physics.mjs` | existe |
| Modelo de PU | `web/assets/power-unit-v1.glb` | existe |
| Manifesto da PU | `web/assets/power-unit-v1.manifest.json` | existe |
| Testes de sistemas | `web/test-systems.mjs` | existe |
| Teste do GLB da PU | `web/test-power-unit.mjs` | existe |
| Teste aerodinâmico | `web/test-aerodynamics.mjs` | existe |

Portanto, referências a `hybrid-kit.js`, `internals-kit.js` ou `mechanics.js` da especificação não foram atribuídas automaticamente ao projeto auditado: são arquivos de outro repositório. A auditoria considerou somente os caminhos reais acima.

## 2. O que já está correto ou alinhado

### 2.1 Limite didático e procedência

**Fato observado:** o manifesto `web/assets/power-unit-v1.manifest.json` declara geometria original procedural, separa o GLB do overlay web, registra ausência de MGU-H no GLB e afirma que o conjunto não é CAD nem homologação. `web/src/systems.js` também descreve suas camadas como originais e explicativas.

**Avaliação:** alinhado com a exigência da especificação de usar geometria original e não apresentar o resultado como malha de fabricante ou validação técnica.

### 2.2 Separação do MGU-H legado

**Fato observado:** `web/src/systems.js` cria o MGU-H e seu acoplamento apenas como nós marcados `legacy2021`. A função `syncERSContextTags()` os oculta no contexto `current2026`; o controle de ERS alterna entre `legacy2021` e `current2026`. O catálogo textual identifica explicitamente os dois contextos.

**Avaliação:** a comparação temporal está implementada de forma consciente. O legado não deve ser interpretado como parte da arquitetura 2026 do modelo.

### 2.3 Estrutura, combustível e Energy Store

**Fato observado:** `SURVIVAL_CELL_LAYOUT` define um envelope didático; `POWER_FUEL_LAYOUT` coloca célula, contenção e Energy Store em posições separadas, testa a contenção da célula dentro da survival cell e posiciona a bateria abaixo do tanque. `web/test-systems.mjs` verifica esses limites, a rota de combustível e a não sobreposição com bloco/câmbio.

**Avaliação:** a organização espacial está coerente com a intenção da especificação: célula compacta, Energy Store sob a célula e componentes internos mantidos no chassi. É uma checagem de consistência do layout didático, não uma certificação estrutural ou de segurança.

### 2.4 Suspensão e animações locais

**Fato observado:** `web/src/systems.js` contém pontos nomeados para pushrod dianteiro e pullrod traseiro; as rotações usam `advanceLocalSpin`. `web/src/mechanics.js` mantém a organização externa de suspensão e rodas. Os testes de sistemas verificam a rotação local e ciclos sem deriva.

**Avaliação:** alinhado com a distinção push-rod dianteira / pull-rod traseira descrita na especificação, dentro do nível esquemático declarado pelo projeto.

### 2.5 Catálogo instrucional

**Fato observado:** `SYSTEM_CATALOG` possui 14 sistemas, capítulos, descrições e ressalvas de simplificação. A interface atualiza a descrição ao selecionar uma camada e distingue o contexto 2021/2026 no painel de PU/ERS.

**Avaliação:** a base de instrução está presente. Ela ainda usa alguns termos herdados do vídeo de 2021, o que é tratado na seção seguinte e não deve ser confundido com aderência 2026.

## 3. Legado 2021 mantido conscientemente para comparação

Esta seção não classifica os itens como erro isolado: eles são aceitáveis somente enquanto o produto deixar inequívoco que o usuário está vendo o contexto legado.

### 3.1 Turbo dividido e MGU-H no overlay

**Fato observado:** em `web/src/systems.js`, o power unit cria `turboCompressor` em `turboAxisStart`, `turboTurbine` em `turboAxisEnd` e um `turboShaft` comum; o texto do sistema chama o conjunto de “TURBO DIVIDIDO”. No mesmo grupo, o MGU-H legado aparece com acoplamento coaxial. Esses nós são ocultados no contexto 2026, mas a geometria 2026 alternativa não é criada.

**Interpretação:** isso é uma representação explícita do vídeo de 2021, não uma implementação do power unit 2026. Deve permanecer apenas como comparação até existir uma variante 2026 independente.

### 3.2 Controle externo chamado DRS

**Fato observado:** `web/src/mechanics.js` localiza um flap por `rear_wing_drs`, aplica `flapPivot.rotation.x` e expõe `setDRS`. `web/src/app-v2.js` liga esse comportamento ao controle `#drs`, cujo rótulo no template é “Abertura da asa traseira”. Não há atualização do elemento dianteiro nesse caminho.

**Interpretação:** é a mecânica histórica do GLB/UX. O nome pode ser mantido internamente como compatibilidade do asset legado, mas não deve ser apresentado como o mecanismo de ultrapassagem da especificação 2026.

### 3.3 Referência visual do vídeo de 2021

**Fato observado:** os capítulos e links da interface apontam para o vídeo Animagraffs usado como referência da implementação anterior. A própria descrição de `systems.js` chama algumas peças de representativas e registra hipóteses.

**Interpretação:** o vídeo é adequado para comparação pedagógica, mas não pode continuar sendo a fonte principal para afirmar a configuração 2026. A especificação determina o pacote F1/FIA 2026 como referência principal.

## 4. Gaps concretos para a próxima iteração

Os itens abaixo são lacunas observadas no código, seguidas de recomendações de implementação. A prioridade é indicativa.

### P1 — Criar uma variante de power unit realmente 2026

**Fato observado:** o contexto 2026 apenas oculta o MGU-H legado. O compressor frontal, a turbina traseira e o eixo comum do turbo continuam sendo criados pelo mesmo código; o catálogo continua descrevendo o monoturbo dividido. Portanto, alternar para 2026 não transforma a geometria em um turbo único traseiro.

**Recomendação:** separar a construção em dois conjuntos explícitos:

1. `powerLegacy2021`: split-turbo + MGU-H + componentes de comparação;
2. `powerCurrent2026`: turbo único localizado atrás do bloco, wastegates visíveis, sem MGU-H e sem eixo coaxial no vale.

O estado 2026 deve ser o padrão do carro-alvo; o legado deve ser opt-in para comparação. Criar teste que falhe se a variante 2026 contiver nós ou rótulos de compressor frontal, eixo split ou MGU-H.

### P1 — Implementar aero ativa dianteira + traseira

**Fato observado:** `web/src/mechanics.js` controla somente um flap traseiro encontrado por `rear_wing_drs`. O `front_wing` participa da desmontagem/categoria, mas não há cinemática conjunta dianteira/traseira para um modo de reta. `web/src/aero-physics.mjs` calcula grandezas aerodinâmicas didáticas, porém não implementa modos de asa.

**Recomendação:** introduzir um estado semântico de aero, por exemplo `cornerMode` e `straightMode`, que mova simultaneamente o elemento dianteiro e o traseiro. O controle deve deixar claro que se trata de Straight Mode/Corner Mode 2026. O MGU-K Override deve ser descrito como telemetria/estado elétrico, sem abrir a asa.

Critérios verificáveis para a próxima iteração:

- o elemento dianteiro e o traseiro mudam juntos em Straight Mode;
- Corner Mode fecha ambos para a posição de carga;
- não há regra de proximidade de 1 segundo;
- o controle legado `setDRS` pode existir apenas como alias interno documentado;
- um teste cobre os dois elementos e os dois estados.

### P1 — Corrigir nomenclatura DRS na interface

**Fato observado:** o usuário vê `DRS`, “Abertura da asa traseira” e “Mecanismo da asa”; o código usa `#drs`, `setDRS` e nomes glTF `rear_wing_drs`.

**Recomendação:** trocar a linguagem visível para “Aero ativa”, “Straight Mode” e “Corner Mode”. Manter `rear_wing_drs` e `setDRS` somente como compatibilidade do arquivo original, com comentário/manifesto indicando “legado 2011–2025”. Não renomear silenciosamente os nós do GLB sem atualizar todos os consumidores.

### P1 — Tornar as trompetas fixas verificáveis

**Fato observado:** `web/src/systems.js` cria seis `Velocity stack / trompeta representativa` em posições fixas e não cria atuadores telescópicos. O teste verifica a quantidade e o loop determinístico, mas não verifica uma propriedade ou estado que prove “fixa”.

**Recomendação:** adicionar metadado explícito, como `userData.regulation = 2026` e `userData.intakeType = 'fixed'`, ou uma constante de layout 2026. Testar seis trompetas, três por bancada, ausência de atuadores e ausência de transformação de comprimento durante a animação. A palavra “fixa” deve ser usada como propriedade do asset didático implementado, não como alegação de homologação.

### P2 — Alinhar o catálogo com o estado temporal selecionado

**Fato observado:** ao selecionar Power, o título e a descrição principal ainda falam em “turbo dividido”, mesmo quando o painel informa “arquitetura atual / 2026”. O catálogo é imutável e a alternância atual muda visibilidade de nós e etiquetas, mas não substitui a descrição por uma explicação 2026.

**Recomendação:** tornar a descrição dependente do contexto ou exibir dois blocos claramente separados: “O que o vídeo de 2021 mostra” e “O que o carro 2026 implementa”. Até a variante 2026 existir, o painel deve declarar que a geometria exibida é a comparação legada, em vez de sugerir que o turbo dividido é a configuração corrente.

### P2 — Completar a validação específica da especificação

**Fato observado:** o projeto auditado possui `test-systems.mjs`, `test-power-unit.mjs`, `test-mechanics.mjs` e `test-aerodynamics.mjs`. Não existem no caminho auditado os testes nomeados na especificação como `tests/hybrid-kit.test.mjs`, `tests/internals-kit.test.mjs`, `tests/cinema.test.mjs` e `tests/engine-chapter.test.mjs`; também não existe no projeto auditado o arquivo `src/engine/hybrid-kit.js` citado pela especificação.

**Recomendação:** criar equivalentes no layout real de `web/test-*.mjs` para os requisitos que ainda não têm cobertura: ausência de MGU-H no modo 2026, turbo traseiro único, seis trompetas fixas, aero ativa nos dois eixos, sem beam wing/túneis Venturi profundos quando essa propriedade puder ser observada no asset, e preservação das três janelas de câmera. Não declarar cobertura apenas porque existe um teste com nome diferente.

### P2 — Registrar números 2026 como dados instrucionais, não como medição do modelo

**Fato observado:** o catálogo menciona sistemas, mas o código auditado não apresenta um objeto de especificação com os valores didáticos da tabela 2026 — aproximadamente 400 kW para ICE, 350 kW para MGU-K, 70 kg de combustível e fluxo energético de 3000 MJ/h.

**Recomendação:** adicionar uma ficha textual versionada para esses valores, com fonte e rótulo “valor didático da regulamentação/referência”, separada das dimensões da geometria. Não inferir potência, massa, vazão, pressão ou homologação a partir de escala, cor, animação ou bounding box do overlay.

## 5. Conclusão

**Estado atual:** o projeto tem uma boa camada didática original, separa o GLB do overlay, explicita limites, organiza combustível/Energy Store e mantém o legado 2021 identificável. Isso atende a parte estrutural e documental da especificação, mas não permite classificar o carro atual como uma implementação geométrica completa da PU e da aero 2026.

**Bloqueadores para chamar a próxima versão de “carro 2026” no sentido da especificação:**

- turbo único traseiro em uma variante 2026 real;
- remoção geométrica do MGU-H no estado 2026, e não apenas ocultação;
- aero ativa com elementos dianteiro e traseiro;
- nomenclatura visível de Straight Mode/Corner Mode, sem chamar o mecanismo de DRS;
- trompetas fixas marcadas e testadas como tais.

Enquanto esses itens não forem implementados e verificados, a formulação segura é: **“modelo didático INTEIA com camadas 2021/2026 e comparação visual; não CAD, não CFD e não homologação.”**

## 6. Referências usadas

- Especificação comparada: `C:\Users\igorm\projetos\inteia-f1-loop\ESPECIFICACAO_MODELAGEM_F1_3D.md`.
- Implementação auditada: `web/src/systems.js`, `web/src/mechanics.js`, `web/src/app-v2.js`, `web/src/engine/in-car.js`, `web/src/engine/engine-shot.js`.
- Asset e escopo: `web/assets/power-unit-v1.manifest.json`.
- Validações existentes: `web/test-systems.mjs`, `web/test-power-unit.mjs`, `web/test-mechanics.mjs`, `web/test-aerodynamics.mjs`.
- Referência regulatória indicada pela especificação: [FIA 2026 Power Unit Technical Regulations](https://www.fia.com/F126) e [explicação da unidade de potência 2026 pela Fórmula 1](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd).
