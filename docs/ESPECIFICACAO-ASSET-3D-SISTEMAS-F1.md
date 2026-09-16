# DIRETRIZES CANÔNICAS DE MODELAGEM 3D — SISTEMAS DO CARRO DE F1 (ANIMAGRAFFS)
> **Estado em 16/09/2026:** a camada procedural em três.js descrita abaixo foi substituída por malhas geradas no Blender 5.2 (`ferramentas/gerar_sistemas.py`) e publicadas em `web/assets/sistemas-v1.glb`. O contrato atual (monoturbo dividido coaxial, MGU-H legado 2021, dois plenums e seis trompetas, refrigeração assimétrica, empacotamento célula → motor → câmbio) é verificado por `web/test-systems.mjs` sobre o manifesto do asset. Veja [SISTEMAS-3D.md](SISTEMAS-3D.md). Os trechos de código abaixo são diagnóstico histórico.
> **Projeto-Alvo:** `INTEIA-laboratorio-3d` (`c:\Users\igorm\projetos\INTEIA-laboratorio-3d`)
> **Servidor Local de Teste:** `http://127.0.0.1:5186/`
> **Deploy de produção:** [Laboratório 3D INTEIA no ChatGPT Sites](https://laboratorio-3d-inteia.igor47306.chatgpt.site)
> **Repositório GitHub:** [https://github.com/igormorais123/INTEIA-laboratorio-3d](https://github.com/igormorais123/INTEIA-laboratorio-3d)
> **Referência Técnica Primária:** [Animagraffs — How a Formula 1 Race Car Works (Jake O'Neal)](https://www.youtube.com/watch?v=V7707zEX9X4)
> **Ponto Crítico de Foco:** `13:23` (`t=803,275s`) — “trumpets”/plenums; waste gate apenas como elemento/trecho adjacente qualificado

> **Nota de diagnóstico de trabalho (não é fonte independente):** Esta especificação registra uma leitura de trabalho do asset e da implementação, não uma nova fonte. O frame verificado em `t=803,275s` destaca “trumpets”/plenums. Dois plenums, seis stacks, materiais e assimetria devem ser tratados como **[HIP]** quando não forem diretamente verificáveis no frame ou na implementação presente; waste gate não deve ser usado como identificação principal desse quadro.

---

## 1. Veredicto e Diagnóstico Forense da IA em `INTEIA-laboratorio-3d`

### 1.1 O Diagnóstico
A IA que trabalhou no laboratório 3D deu um passo positivo ao criar a aba `06 Sistemas` em [`web/src/workbench.js`](../web/src/workbench.js) e documentar a linha do tempo em [`docs/pesquisa-sistemas-carro-video.md`](./pesquisa-sistemas-carro-video.md). Porém, por operar **apenas com texto e rótulos superficiais sem ver as imagens reais do vídeo**, ela cometeu **alucinações conceituais graves** no módulo procedural [`web/src/systems.js`](../web/src/systems.js) e omitiu geometrias mecânicas indispensáveis para a criação do asset 3D final no Blender ([`INTEIA_F1_Master.blend`](../INTEIA_F1_Master.blend)).

### 1.2 As 5 Grandes Falhas Diagnosticadas no Código

1. **A Alucinação do Bi-Turbo em [`web/src/systems.js`](../web/src/systems.js) (linhas 104-106):**
   ```javascript
   // Código errôneo gerado pela IA:
   const turboL = torus(power, .13, .035, [-.34, .70, -.54], powerHot, 'Turbo compressor esquerdo', [Math.PI/2, 0, 0]),
         turboR = torus(power, .13, .035, [.34, .70, -.54], powerHot, 'Turbo compressor direito', [Math.PI/2, 0, 0]);
   ```
   * **O Erro:** A IA modelou um motor **Bi-Turbo** (dois compressores, um de cada lado)! Carros de Fórmula 1 híbridos são **estritamente MONOTURBO**.
   * **A Realidade Visual do Vídeo:** A F1 utiliza um **Split-Turbo Bipartido**: um único caracol de compressor frio na frente do motor (`X = 0`), uma única turbina quente atrás do motor (`X = 0`), e um eixo coaxial longo que atravessa o vale em V a 90° interligando ambos através do MGU-H central. A IA leu "dual wastegates" e deduziu falsamente que existiam dois turbos.

2. **A Desconexão do MGU-H e MGU-K em [`web/src/systems.js`](../web/src/systems.js) (linhas 112-113):**
   ```javascript
   // Código desconectado da IA:
   const mguk = cylinder(ers, .10, .24, [0, .48, -1.28], ersMat, 'MGU-K', [0, 0, Math.PI/2]),
         mguh = cylinder(ers, .10, .20, [0, .72, -.48], ersMat, 'MGU-H', [0, 0, Math.PI/2]);
   ```
   * **O Erro:** A IA colocou o MGU-H e o MGU-K flutuando soltos no espaço como latas cilíndricas isoladas.
   * **A Realidade Visual do Vídeo:** O MGU-H é **coaxial ao eixo do Split-Turbo**, alojado no fundo do "V" entre as duas bancadas de cilindros, solidário ao eixo compressor-turbina. O MGU-K é engrenado mecanicamente na lateral inferior do virabrequim por pinhão de engrenagens de dentes retos.

3. **O Ponto Cego aos 13:23 (`t=803s`) em [`docs/pesquisa-sistemas-carro-video.md`](./pesquisa-sistemas-carro-video.md) (linha 37):**
   * **O Erro:** A IA anotou apenas: `13:23 | Engine / waste gate | O quadro indicado mostra o turbo e o rótulo waste gate...`
   * **[HIP] Leitura de modelagem:** O frame verificado em `t=803,275s` destaca “trumpets”/plenums. Dois plenums, seis trompetas (*Velocity Stacks*), materiais e assimetria são hipóteses de modelagem quando não forem diretamente verificáveis; waste gate pode permanecer apenas como elemento/trecho adjacente qualificado.

4. **Falsa Simetria nos Radiadores dos Sidepods em [`web/src/systems.js`](../web/src/systems.js) (linhas 116-118):**
   ```javascript
   // Código simétrico incorreto:
   for (const side of [-1, 1]) {
     box(cooling, .08, .38, .94, [side * .70, .49, -.08], coolMat, `Radiador sidepod ${side}`);
   }
   ```
   * **O Erro:** A IA gerou radiadores rigorosamente idênticos nos dois lados.
   * **A Realidade Visual do Vídeo:** O arrefecimento é **totalmente assimétrico**:
     * **Sidepod Esquerdo:** Ocupado quase que exclusivamente pelo grande **Intercooler ar-ar** (para o ar pressurizado que vem do compressor frontal do turbo).
     * **Sidepod Direito:** Preenchido por três trocadores de calor empilhados: radiador de água de refrigeração do bloco do motor, radiador de óleo do cárter seco e radiador de baixa temperatura da bateria/inversor.

5. **A Armadilha do Regulamento de 2026 em [`docs/pesquisa-sistemas-carro-video.md`](./pesquisa-sistemas-carro-video.md) (linhas 20-27):**
   * **O Erro:** A IA tentou "eliminar o MGU-H" antecipadamente sob o pretexto de que o regulamento de 2026 descartará o MGU-H.
   * **A Correção:** O modelo 3D do laboratório baseia-se visualmente no carro da era moderna híbrida do vídeo (Halo 2018+, pneus 13 polegadas, bargeboards complexos e MGU-H ativo). Eliminar o MGU-H mutila a geometria mecânica do vídeo de referência de Jake O'Neal.

---

## 2. Mapa de Arquivos do Projeto: Onde Agir e O que Fazer

Para transformar o protótipo esquemático no asset 3D final com alta fidelidade:

```
c:\Users\igorm\projetos\INTEIA-laboratorio-3d\
├── INTEIA_F1_Master.blend               <-- Master Blender 4.5: modelagem geométrica das malhas reais
├── docs/
│   ├── BLENDER.md                       <-- Diretrizes de exportação glTF/GLB
│   ├── pesquisa-sistemas-carro-video.md <-- Documento de pesquisa histórica da IA
│   └── ESPECIFICACAO-ASSET-3D-SISTEMAS-F1.md <-- ESTE GUIA TÉCNICO (CANÔNICO)
├── modelos/
│   ├── INTEIA_F1_animado.glb            <-- Modelo 3D com rig de explosão e animações
│   └── INTEIA_F1_estatico.glb           <-- Modelo 3D com geometria íntegra
├── web/
│   ├── assets/
│   │   ├── carro-aula-v2.glb            <-- Asset otimizado para o visualizador WebGL
│   │   ├── power-unit-v1.glb            <-- Asset do motor V6 híbrido sob demanda
│   │   └── power-unit-v1.manifest.json  <-- Manifesto técnico de nós e restrições
│   ├── src/
│   │   ├── app-v2.js                    <-- Orquestração do Three.js e render loop
│   │   ├── systems.js                   <-- Módulo procedural das 14 camadas internas
│   │   ├── workbench.js                 <-- Gerenciador das abas (Carro, Motor, Sistemas)
│   │   └── template-v2.html             <-- HTML da interface do laboratório
│   └── test-systems.mjs                 <-- Testes automatizados das 14 camadas
```

### Links Diretos no Código para Correção:

1. **Correção do Monoturbo / Split-Turbo e Admissão:**
   * Modificar [`web/src/systems.js`](../web/src/systems.js) linhas 101-107: Excluir `turboL` e `turboR`. Inserir compressor frontal em `[0, 0.65, -0.40]`, eixo central atravessando o vale e turbina traseira em `[0, 0.54, -1.02]`.
   * Adicionar aos 13:23 as câmaras plenas e trompetas em `assembly_intake` com 6 bocais de sino.
2. **Correção do MGU-H e MGU-K:**
   * Modificar [`web/src/systems.js`](../web/src/systems.js) linhas 109-115: Posicionar `mguh` exatamente no centro do eixo do turbo em `[0, 0.58, -0.70]`.
   * Posicionar `mguk` na lateral inferior do bloco em `[-0.18, 0.36, -0.85]`, com engrenagem ligada ao virabrequim.
3. **Correção da Assimetria dos Radiadores:**
   * Modificar [`web/src/systems.js`](../web/src/systems.js) linhas 116-118: Substituir o loop simétrico `for(const side of [-1,1])` por criação explícita do Intercooler inclinado no lado esquerdo (`X = -0.70`) e a bancada tripla de radiadores de líquidos no lado direito (`X = +0.70`).
4. **Alinhamento dos Testes de Integridade:**
   * Verificar [`web/test-systems.mjs`](../web/test-systems.mjs): Garantir que a suíte de testes de 14 camadas continue executando com sucesso após os ajustes:
     ```powershell
     cd c:\Users\igorm\projetos\INTEIA-laboratorio-3d\web
     npm test
     ```

---

## 3. Especificação Geométrica e Espacial dos 14 Sistemas

```
                            [ROLL HOOP / AIRBOX] (0, 0.95, -0.35)
                                      |
                +---------------------+---------------------+
                |                     |                     |
      (Arrefec. Auxiliar)      (Ar de Admissão)     (Arrefec. Auxiliar)
                |                     |                     |
                |             [COMPRESSOR FRONTAL]          |
                |             [0, 0.65, -0.40]              |
                |                     |                     |
                |        (Duto de Pressão Lateral)          |
                |                     v                     |
                |             [INTERCOOLER AR-AR]           |
                |            [-0.70, 0.49, -0.08] (Inclin.) |
                |                     |                     |
                |       (Duto de Retorno Resfriado)         |
                |                     v                     |
                |            +-----------------+            |
                |            | PLENUM ESQUERDO | (13:23)    |
                |            |   + 3 TROMPETAS |            |
                |            +-----------------+            |
                |            |   MGU-H CENTRAL | <----------+-- [EIXO COAXIAL LONGO]
                |            | [0, 0.58, -0.70]|            |   (No vale em "V" a 90°)
                |            +-----------------+            |
                |            | PLENUM DIREITO  | (13:23)    |
                |            |   + 3 TROMPETAS |            |
                |            +-----------------+            |
                |                     |                     |
                |            [BLOCO V6 A 90°]               |
                |                     |                     |
                |          (Coletores Inconel 3-em-1)       |
                |                     v                     |
                +------------> [TURBINA TRASEIRA] <---------+
                               [0, 0.54, -1.02]
                                      |
                           [ESCAPE CENTRAL + 2 WASTEGATES]
```

### Sistema 01: Aerodinâmica (`aero`, 0:14)
* **Geometria:** Asa dianteira de múltiplos elementos com ângulo de ataque invertido; vórtice Y250 gerado a 250 mm da linha de centro pelas pontas pontiagudas dos flaps; assoalho com efeito solo e inclinação de *rake* (frente baixa a ~25 mm, traseira a ~75 mm); difusor traseiro com expansão curvada e palhetas verticais (*strakes*); asa traseira biplano com atuador hidráulico central de DRS capaz de abrir até 85 mm.
* **Cor PBR:** Ciano (`#52c8df`), fibra de carbono reflexiva com verniz brilhante.

### Sistema 02: Monocoque / Estrutura (`structure`, 4:47)
* **Geometria:** Célula de sobrevivência oca em carbono e colmeia de Nomex; termina na parede de fogo traseira (`Z = -0.42`). Bloco do motor V6 e carcaça do câmbio são membros portantes parafusados diretamente em linha (sem chassi tubular).
* **Cor PBR:** Violeta estrutural (`#c5a7ff`), textura de sarja 2x2 fosca acetinada.

### Sistema 03: Suspensão (`suspension`, 5:19)
* **Dianteira (Push-rod):** Triângulos duplos (*wishbones*) com perfil de gota de fluxo. Haste push-rod sobe do cubo inferior até o topo do monocoque; aciona balancim em "L", **barra de torção longitudinal** e elemento central **Heave** (amortecedor horizontal cercado por pilha de arruelas cônicas Belleville `()()()()`).
* **Traseira (Pull-rod):** Haste pull-rod desce do topo do cubo traseiro para a base inferior da carcaça do câmbio, puxando o balancim rebaixado para minimizar o centro de gravidade.
* **Cor PBR:** Âmbar usinado (`#f1bd68`), titânio escuro e carbono fosco.

### Sistema 04: Direção (`steering`, 7:52)
* **Geometria:** Coluna inclinada saindo do cockpit até o topo do monocoque; cremalheira hidráulica transversal com pinhão engrenado; barras de direção (*track rods*) paralelas aos braços de suspensão.
* **Cor PBR:** Coral mecânico (`#ff8c6b`), alumínio e mangueiras hidráulicas reforçadas.

### Sistema 05: Freios e Brake-by-Wire (`brakes`, 8:57)
* **Geometria:** Cilindros mestres duplos com fuso de regulagem eletrônica de balanço (*brake bias*); discos de fricção carbono-carbono com mais de 1.400 orifícios de ventilação radial; pinças monobloco em liga alumínio-lítio montadas na posição de 6 horas (base inferior) para centro de gravidade baixo e purga fácil de bolhas; duto aerodinâmico de carbono envolvendo todo o cubo.
* **Cor PBR:** Vermelho térmico (`#ff665d`), discos com material emissivo dinâmico sob carga.

---

### Sistema 06: Unidade de Potência Térmica — V6 Turbo (`power`, 11:32)
*(O Timestamp de 13:23 / 803s está situado aqui)*

* **Arquitetura Geral:** 1.6L, V6 a 90°, pistões de curso curto com cabeça plana, virabrequim forjado com 4 mancais principais.
* **O Ponto Crítico dos 13:23 (`t=803,275s`):**
  * O ar pressurizado sai do compressor frontal, atravessa o intercooler no sidepod esquerdo e retorna resfriado por tubulação de carbono.
  * **[HIP] Câmaras Plenas de Admissão (*Intake Plenums*):** Duas caixas prismáticas simétricas em fibra de carbono fosca montadas sobre cada bancada de cilindros, caso essa quantidade e material não sejam diretamente verificáveis.
  * **[HIP] Trompetas de Admissão (*Velocity Stacks*):** Seis trompetas curvas com boca em sino (*bellmouth*) alojadas dentro dos plenums; quantidade e material permanecem hipótese quando não diretamente verificáveis.
* **Split-Turbo Bipartido:**
  * **Compressor Frontal:** Caracol de alumínio montado na face frontal do motor (`X = 0, Y = 0.65, Z = -0.40`).
  * **Turbina Traseira:** Caracol quente de ferro fundido montado atrás do motor (`X = 0, Y = 0.54, Z = -1.02`), recebendo os dois coletores em serpentina Inconel 3-em-1.
  * **Eixo Central:** Eixo cilíndrico de titânio ligando compressor e turbina pelo fundo do vale em "V".
  * **Dual Wastegates:** Duas válvulas de alívio com tubos de escape secundários que correm paralelos sob o escape principal até a traseira.
* **[HIP] Materiais e Cor PBR:** Laranja mecânico (`#ff9f58`), Inconel com pátina roxo/azulada e titânio acetinado.

---

### Sistema 07: Sistema de Recuperação de Energia — ERS (`ers`, 14:14)
* **MGU-H (Motor Generator Unit - Heat):**
  * Montado coaxialmente no centro do vale em "V" a 90° (`[0, 0.58, -0.70]`), atravessado pelo eixo do turbo.
  * Converte calor e fluxo dos gases de escape em eletricidade a até 125.000 RPM ou acelera o compressor instantaneamente para eliminar o turbo lag.
* **MGU-K (Motor Generator Unit - Kinetic):**
  * Instalado na lateral inferior esquerda do cárter (`[-0.18, 0.36, -0.85]`), engrenado diretamente no virabrequim.
  * Fornece até 120 kW (160 cv) de potência auxiliar nas rodas traseiras e atua como freio regenerativo.
* **Bateria (Energy Store):** Células de íon-lítio blindadas em caixa de carbono posicionadas no piso do monocoque, abaixo do tanque de combustível. Cabos blindados de alta tensão na cor laranja vibrante.
* **Cor PBR:** Amarelo alta tensão (`#ffe36b`), silicone laranja e manta de isolamento térmico dourada (Kapton).

### Sistema 08: Refrigeração e Intercooler (`cooling`, 14:54)
* **[HIP] Assimetria dos sidepods:** Grande **Intercooler Ar-Ar** no lado esquerdo, montado a 40° de inclinação e conectado por tubos coletores de alumínio e carbono; bancada de três radiadores sobrepostos no lado direito, quando essa assimetria não for diretamente verificável:
  1. Radiador principal de água do ICE;
  2. Radiador de óleo lubrificante (cárter seco);
  3. Radiador de baixa temperatura do circuito ERS (bateria/inversor).
* **Tomada do Santo Antônio (*Roll Hoop*):** Radiadores secundários para óleo da transmissão e fluido hidráulico da direção.
* **[HIP] Materiais e Cor PBR:** Verde fluido (`#66e0b2`), malha metálica micro-aletada e dutos pretos foscos.

### Sistema 09: Célula de Combustível (`fuel`, 15:39)
* **Geometria:** Bexiga flexível em Kevlar balístico e borracha nitrílica à prova de perfuração, alojada na cavidade oca entre o banco e a parede de fogo. Capacidade para 145-150 L (~110 kg).
* **Internos:** Anteparos divisórios transversais (*baffles*) com portinholas unidirecionais por gravidade que forçam a gasolina para o copo coletor inferior (*swirl pot*), prevenindo cavitação sob forças de 6G. Tanque cilíndrico de óleo entre a célula de combustível e o bloco.
* **Cor PBR:** Dourado translúcido / Kevlar amarelo (`#e6c06d`).

### Sistema 10: Câmbio de 8 Marchas e Diferencial (`transmission`, 16:42)
* **Geometria:** Cartucho estrutural fundido em liga de alumínio-titânio; trem de engrenagens sequenciais de 8 marchas à frente e 1 ré com troca contínua (*seamless*); diferencial autoblocante nas saídas laterais.
* **Semieixos:** Conectados ao diferencial por **juntas tripóides deslizantes** com rolamentos esféricos de agulha usinados, permitindo ampla articulação angular da suspensão traseira.
* **Cor PBR:** Aço fosco usinado (`#b7c2cc`), engrenagens em aço carbono escuro.

### Sistema 11: Sistemas de Segurança (`safety`, 17:03)
* **Geometria:** Dispositivo **Halo** em titânio Ti-6Al-4V de 9 kg (pilar central no bico e 2 apoios traseiros); arco primário de capotamento (*roll hoop*) incorporado na entrada do airbox; cone de deformação dianteiro no bico; 4 tubos anti-intrusão lateral (*Side Impact Structures - SIS*); cone de impacto traseiro segurando a luz de chuva; **três cabos trançados de retenção de roda (*wheel tethers*) independentes** por cubo de roda ancorados no chassi.
* **Cor PBR:** Magenta de proteção (`#ff4d67`), titânio forjado e fibra balística.

### Sistema 12: Cockpit e Retenção do Piloto (`cockpit`, 17:51)
* **Geometria:** Assento moldado ultrafino de carbono com piloto em posição semideitada (joelhos elevados quase na altura do tórax); arnês de segurança de 6 pontos convergindo na fivela rotativa central; colar de carbono **HANS** apoiado nos ombros e amarrado ao capacete; apoios laterais acolchoados para proteção cervical (*headrest*); pedais de alumínio com separador vertical alto impedindo que o pé escorregue para o freio; tubo flexível de hidratação saindo do reservatório interno.
* **Cor PBR:** Lilás ergonômico (`#d9a8ff`), tecido Nomex e carbono laqueado.

### Sistema 13: Volante e Comandos (`wheel`, 19:17)
* **Geometria:** Volante de carbono retangular com empunhaduras ergonômicas de silicone; display digital LCD central; barra superior de LEDs sequenciais para troca de marchas (*shift lights*) e LEDs laterais de bandeiras; seletores rotativos para mapa de torque, ERS e diferencial; pás traseiras superiores para marchas (*paddle shift*) e pás inferiores analógicas para embreagem de largada; engate rápido (*quick-release*).
* **Cor PBR:** Azul comandos (`#8db5ff`), display iluminado e teclas coloridas.

### Sistema 14: Sensores e Telemetria (`sensors`, 22:11)
* **Geometria:** **Tubo de Pitot** metálico montado no bico dianteiro com tomada de pressão dinâmica e estática; sensores de velocidade de roda; sensores ópticos infravermelhos nos retrovisores para monitorar a temperatura dos pneus; acelerômetros integrados nos moldes intra-auriculares do piloto; microfone acústico na saída do escape; unidade central de telemetria (ECU) enviando dados para o box via antenas duplas de alta frequência.
* **Cor PBR:** Ciano elétrico (`#7ee5f2`), conectores dourados e chicotes elétricos finos.

---

> **Nota de enquadramento:** Esta seção de correção e o bloco JavaScript de exemplo abaixo são diagnóstico histórico/pseudocódigo de referência, não o código atual nem uma descrição da implementação presente. Os arrays, posições e chamadas exibidos servem apenas para orientar a correção; o estado presente deve ser conferido em [`web/src/systems.js`](../web/src/systems.js) e no checklist da Seção 5.

## 4. Instruções Diretas de Ajuste para a IA no Código de `systems.js`

A IA deve substituir o bloco de código do motor e radiadores em [`web/src/systems.js`](../web/src/systems.js) pela seguinte implementação corrigida:

```javascript
// === CORREÇÃO OBRIGATÓRIA: V6 MONOTURBO COM SPLIT-TURBO E CÂMARAS PLENAS (13:23) ===
const power = createSystem('power'),
      powerMat = makeMaterial('V6 · laranja', colors.power, {metalness: .7, roughness: .32}),
      powerDark = makeMaterial('V6 · bloco', 0x303a42, {metalness: .5, roughness: .34}),
      powerHot = makeMaterial('V6 · quente', 0xff6e42, {metalness: .44, roughness: .3, emissiveIntensity: .65}),
      carbonMat = makeMaterial('V6 · carbono plenums', 0x181c20, {metalness: .2, roughness: .6}),
      machinedAlum = makeMaterial('V6 · trompetas alumínio', 0xd8e0e8, {metalness: .85, roughness: .18});

// 1. Bloco V6 estrutural a 90° e virabrequim
rounded(power, .54, .34, .78, [0, .49, -.75], powerDark, 'Bloco V6');
const crank = cylinder(power, .026, .78, [0, .40, -.75], powerMat, 'Virabrequim', [0, 0, Math.PI / 2], 20);
addSpinner(crank, 'x', 1.7);

// 2. Cabeçotes, cilindros e coletores serpentina 3-em-1
for (const side of [-1, 1]) {
  box(power, .16, .22, .60, [side * .20, .67, -.75], powerMat, `Cabeçote ${side}`);
  for (const z of [-.98, -.75, -.52]) {
    cylinder(power, .055, .12, [side * .20, .81, z], powerMat, `Cilindro ${side} ${z}`);
    pipe(power, [[side * .20, .76, z], [side * .32, .72, z - .06], [0, .56, -.98]], .012, powerHot, `Coletor serpentina ${side} ${z}`);
  }
}

// 3. O SPLIT-TURBO CORRETO (Monoturbo Bipartido)
// Compressor frontal frio (face dianteira do motor):
const compressor = torus(power, .14, .04, [0, .66, -.40], powerMat, 'Compressor frontal do turbo', [Math.PI / 2, 0, 0]);
addSpinner(compressor, 'z', 2.0);

// Turbina traseira quente (face traseira do motor):
const turbine = torus(power, .15, .042, [0, .54, -1.02], powerHot, 'Turbina quente traseira', [Math.PI / 2, 0, 0]);
addSpinner(turbine, 'z', 2.0);

// Eixo coaxial de titânio ligando compressor à turbina pelo centro do "V":
beam(power, [0, .60, -.40], [0, .56, -1.02], .014, powerMat, 'Eixo central de titânio do Split-Turbo');

// MGU-H instalado no centro do eixo longitudinal, entre as duas bancadas:
const mguh = cylinder(power, .10, .26, [0, .58, -.70], powerMat, 'MGU-H central no vale em V', [Math.PI / 2, 0, 0]);
addSpinner(mguh, 'z', 2.0);

// Tubos de escape principal e as duas wastegates paralelas:
pipe(power, [[0, .54, -1.02], [0, .54, -1.45], [0, .48, -1.82]], .024, powerHot, 'Escape central de 110mm');
pipe(power, [-.04, .48, -1.02], [-.03, .48, -1.82], .010, powerHot, 'Wastegate esquerda');
pipe(power, [.04, .48, -1.02], [.03, .48, -1.82], .010, powerHot, 'Wastegate direita');

// 4. O SISTEMA DOS 13:23 (803s) — Câmaras Plenas e Trompetas de Admissão
for (const side of [-1, 1]) {
  // Caixa do plenum em fibra de carbono sobre cada bancada de cilindros:
  rounded(power, .14, .10, .56, [side * .19, .84, -.75], carbonMat, `Câmara plena de admissão (Plenum) ${side}`);
  // As 3 trompetas usinadas (velocity stacks) com boca em sino dentro do plenum:
  for (const z of [-.95, -.75, -.55]) {
    cone(power, .032, .06, [side * .19, .83, z], machinedAlum, `Trompeta de admissão ${side} ${z}`, [0, 0, 0]);
  }
}

// Duto pressurizado vindo do intercooler no sidepod esquerdo até os dois plenums:
pipe(power, [[-.60, .55, -.08], [-.35, .72, -.38], [0, .80, -.45]], .020, carbonMat, 'Duto de ar resfriado pós-intercooler');
pipe(power, [[0, .80, -.45], [-.19, .84, -.50]], .016, carbonMat, 'Bifurcação plenum esquerdo');
pipe(power, [[0, .80, -.45], [.19, .84, -.50]], .016, carbonMat, 'Bifurcação plenum direito');

addTag(power, 'V6 TURBO / 13:23', [-.67, 1.00, -.62], meta('power').color);
```

---

## 5. Checklist da Implementação Presente

Verificar o estado presente do asset e da visualização, sem tratar hipóteses visuais como validação de engenharia:

1. **Executar a Suíte de Testes Automatizados no Laboratório:**
   ```powershell
   cd c:\Users\igorm\projetos\INTEIA-laboratorio-3d\web
   npm test
   ```
   *Critério de Pronto:* Todos os testes em [`web/test-systems.mjs`](../web/test-systems.mjs), `test-mechanics.mjs`, `test-aerodynamics.mjs`, `test-power-unit.mjs` e `test-driver-model.mjs` devem retornar sucesso sem exceções.

2. **Checklist visual no Servidor Local:**
   Abra `http://127.0.0.1:5186/` e acesse a aba **06 Sistemas**:
   * **Unidade de potência:** conferir um monoturbo coaxial no eixo Z, com compressor à frente, turbina atrás e bocas abertas; distinguir visualmente os caminhos de admissão, refrigeração e combustível.
   * **Estrutura e cockpit:** conferir a survival cell/estrutura do piloto como camada didática distinta da fuel cell/célula de combustível; a visualização não afirma posição homologada.
   * **Câmbio:** conferir carcaça translúcida ou janela de inspeção para visualizar engrenagens e eixos.
   * **Suspensão:** conferir suspensão estática, com braços e conexões efetivamente ligados às rodas e ao chassi.
   * **ERS e refrigeração:** conferir MGU-H atravessado pelo eixo central do turbo, MGU-K acoplado à base do virabrequim e o encaminhamento visual dos circuitos de refrigeração.

3. **Validação do Master no Blender ([`INTEIA_F1_Master.blend`](../INTEIA_F1_Master.blend)):**
   Ao abrir o arquivo master no Blender 4.5, as coleções e nós gerados devem manter as convenções de coordenadas métricas (Z para cima) e a nomenclatura de peças catalogadas em [`documentacao/componentes-origem.json`](../documentacao/componentes-origem.json).
