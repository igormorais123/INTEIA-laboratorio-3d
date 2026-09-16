# Pesquisa técnica — instrução dos 14 sistemas F1 2026

## Escopo e regra de leitura

Este documento apoia os textos exibidos quando o visitante seleciona um sistema no laboratório 3D. O alvo é uma explicação visual e didática de um carro de Fórmula 1 sob o regulamento de 2026; não é CAD, manual de manutenção, cálculo estrutural, CFD, telemetria nem validação de segurança.

A especificação canônica usada como roteiro é [`ESPECIFICACAO_MODELAGEM_F1_3D.md`](C:\Users\igorm\projetos\inteia-f1-loop\ESPECIFICACAO_MODELAGEM_F1_3D.md). O vídeo Animagraffs indicado nela é um registro explicativo de 2021 e serve para a sequência visual e para comparar a arquitetura anterior. Sempre que o vídeo mostrar MGU-H, turbo dividido, trompetas variáveis ou DRS como auxílio de ultrapassagem, isso deve ser rotulado como **contexto 2021**, não como descrição do carro 2026.

## Base factual confirmada

- A unidade de potência de 2026 mantém o V6 de 1,6 litro, aumenta a participação elétrica e usa MGU-K de até 350 kW; o MGU-H é removido. A FIA também associa a mudança a combustível sustentável e a uma nova relação entre potência térmica e elétrica.
- Os carros de 2026 são menores e mais leves: entre-eixos de 3.400 mm, largura de 1.900 mm e massa mínima regulamentar de 768 kg nas condições definidas pelo regulamento. Esses números são parâmetros do regulamento, não dimensões a serem inferidas de uma captura do modelo.
- A aerodinâmica passa a ter elementos móveis na asa dianteira e na traseira. O modo de baixo arrasto abre/achata os flaps em zonas permitidas; em curva, a configuração fechada preserva carga. Isso substitui a explicação simplificada de “DRS para seguir outro carro” do período anterior.
- A asa traseira de 2026 não usa beam wing; o assoalho é parcialmente plano e o difusor é menos dependente do efeito-solo profundo que marcou a geração anterior.
- A FIA reforçou proteção contra intrusão na célula de sobrevivência, proteção lateral da célula de combustível, estruturas de impacto e requisitos do roll hoop. Luzes laterais podem indicar o estado do ERS quando o carro está parado.
- O regulamento define os requisitos legais de chassis, célula de sobrevivência, combustível, freios, suspensão, direção, transmissão, cockpit, retenção e aquisição de dados. Ele não transforma a geometria simplificada deste laboratório em peça homologada.

Fontes primárias gerais:

- [FIA — hub dos regulamentos de Fórmula 1 2026](https://www.fia.com/F126)
- [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations)
- [FIA — regulamentos técnicos 2026, edição publicada](https://www.fia.com/sites/default/files/fia_2026_formula_1_technical_regulations_issue_8_-_2024-06-24.pdf)
- [F1 — novas unidades de potência 2026](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd)
- [F1 — aerodinâmica 2026](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-aerodynamics.7IAt0auc32UkCEFE5ypkTB.7IAt0auc32UkCEFE5ypkTB)
- [F1 — termos-chave das regras 2026](https://www.formula1.com/en/latest/article/explained-the-new-key-terms-for-formula-1s-new-for-2026-rules.3T5BU6TC9quGcIpGzoWkY0.3T5BU6TC9quGcIpGzoWkY0)
- [Vídeo de referência — How a Formula 1 Race Car Works](https://www.youtube.com/watch?v=V7707zEX9X4&t=803s)

## Os 14 sistemas

### 01 — Aerodinâmica

**Como explicar:** asas, assoalho, difusor e carroceria conduzem o ar. A asa aumenta a carga que mantém o carro estável; o arrasto é o custo dessa interação. Em 2026, asas dianteira e traseira têm elementos móveis: o piloto usa o modo de baixo arrasto em zonas autorizadas e retorna à configuração de maior carga para curvas. A visualização mostra relações de fluxo, não valores de downforce.

**2021 × 2026:** no vídeo, a explicação de DRS é histórica. No carro 2026, falar em active aero e zonas regulamentadas; não afirmar que a abertura depende de estar a menos de um segundo do carro da frente.

**Fontes:** [F1 — aerodinâmica 2026](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-aerodynamics.7IAt0auc32UkCEFE5ypkTB.7IAt0auc32UkCEFE5ypkTB); [F1 — X/Z mode](https://www.formula1.com/en/latest/article/explained-2026-aerodynamic-regulations-fia-x-mode-z-mode-.26c1CtOzCmN3GfLMywrgb2).

### 02 — Estrutura central / survival cell

**Como explicar:** a célula de sobrevivência é a estrutura rígida ao redor do piloto. Monocoque, estruturas de impacto e pontos de fixação distribuem cargas e separam o espaço protegido dos conjuntos dianteiro e traseiro.

**Limite didático:** o volume colorido é um envelope visual. Não afirmar material, espessura, resistência ou conformidade da malha sem uma homologação específica.

**Fontes:** [FIA — Seção C, regulamento técnico](https://www.fia.com/regulation/fia-formula-1-technical-regulations), especialmente os artigos de chassis, survival cell e intrusion protection; [FIA — visão geral das regras 2026](https://www.fia.com/news/new-era-competition-fia-showcases-future-focused-formula-1-regulations-2026-and-beyond).

### 03 — Suspensão

**Como explicar:** braços e montantes guiam cada roda; push-rod ou pull-rod transmite o movimento para mola, amortecedor e barra de torção. O conjunto mantém o pneu em contato com a pista e controla rolagem, mergulho e transferência de carga.

**2021 × 2026:** push-rod dianteiro e pull-rod traseiro são uma convenção de layout do modelo, não uma regra universal que todos os carros precisam adotar. A animação de curso é ilustrativa.

**Fontes:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations); [F1 — explicação de push-rod e pull-rod](https://www.formula1.com/en/latest/article/explainer-whats-the-difference-between-pull-rod-and-push-rod-suspension.1I3wL4LEL0nQZbKZbx1Dhz).

### 04 — Direção

**Como explicar:** o volante movimenta a coluna; a cremalheira e as barras de direção transformam essa rotação no esterçamento dos montantes dianteiros. O sistema permite apontar o carro e corrigir sua trajetória.

**Limite:** a cena não informa assistência, relação de direção, torque no volante ou calibração de uma equipe.

**Fonte:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations).

### 05 — Freios

**Como explicar:** o pedal solicita pressão hidráulica; cilindros mestres e linhas levam essa pressão às pinças, que apertam discos e transformam energia cinética em calor. O MGU-K também pode recuperar energia na desaceleração, mas isso é um caminho elétrico separado da frenagem mecânica.

**Limite:** não afirmar pressão, temperatura, material de disco/pastilha ou distribuição exata a partir do desenho.

**Fontes:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations); [F1 — novas unidades de potência 2026](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd).

### 06 — Unidade de potência

**Como explicar:** o V6 transforma combustível em torque; o turbo comprime o ar de admissão; a combustão gira o virabrequim e o conjunto entrega torque ao câmbio. No modelo 2026, representar turbo único atrás do bloco, seis trompetas fixas e wastegates como elementos de leitura.

**2021 × 2026:** compressor frontal, eixo coaxial no vale e MGU-H pertencem à arquitetura mostrada no vídeo de 2021. No contexto atual, MGU-H é removido e a especificação fixa as trompetas.

**Fontes:** [F1 — novas unidades de potência 2026](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd); [FIA — decisões sobre a PU 2026](https://www.fia.com/news/fia-announces-world-motor-sport-council-decisions-24); [FIA — regulamento técnico de unidade de potência](https://www.fia.com/sites/default/files/fia_2026_formula_1_technical_regulations_pu_-_issue_7_-_2024-06-11_1.pdf).

### 07 — ERS híbrido

**Como explicar:** o ERS recupera energia em desaceleração, armazena-a no Energy Store e a devolve pelo MGU-K para ajudar a tração. Ele também envolve eletrônica de controle, inversor e cabos de alta tensão.

**2021 × 2026:** o modo do vídeo mostra MGU-H ligado ao turbo. Em 2026, a máquina elétrica regulamentar de tração é o MGU-K; a interface do laboratório deve deixar claro qual contexto está ativo.

**Fontes:** [F1 — termos-chave 2026](https://www.formula1.com/en/latest/article/explained-the-new-key-terms-for-formula-1s-new-for-2026-rules.3T5BU6TC9quGcIpGzoWkY0); [FIA — ajustes de potência e recuperação 2026](https://www.fia.com/news/refinements-2026-fia-formula-1-regulations-agreed-all-stakeholders); [FIA — PU 2026](https://www.fia.com/sites/default/files/fia_2026_formula_1_technical_regulations_pu_-_issue_7_-_2024-06-11_1.pdf).

### 08 — Refrigeração

**Como explicar:** entradas de ar, radiadores, intercooler, dutos e saídas removem calor do motor, óleo, água e componentes elétricos. O fluxo quente e o fluxo frio têm funções diferentes e precisam ser conduzidos sem interferir no piloto.

**Limite:** a divisão esquerda/direita do modelo é uma hipótese didática de embalagem. Não afirmar vazão, temperatura, eficiência ou que todos os carros usam o mesmo arranjo.

**Fontes:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations); [F1 — unidade de potência 2026](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd).

### 09 — Célula de combustível

**Como explicar:** a célula flexível armazena o combustível; bomba, sensores, tubulações e válvulas levam-no ao motor. A contenção e a posição atrás do piloto são mostradas como uma relação de segurança e embalagem.

**2021 × 2026:** a especificação didática usa 70 kg como referência de combustível de corrida para 2026, mas o regulamento e as condições de prova devem ser a fonte final de qualquer número.

**Fontes:** [FIA — Seção C, proteção da survival cell e fuel bladder](https://www.fia.com/sites/default/files/documents/fia_2026_f1_regulations_-_section_c_technical_-_iss_16_-_2026-02-27.pdf); [FIA — regulamentos técnicos](https://www.fia.com/regulation/fia-formula-1-technical-regulations).

### 10 — Câmbio e diferencial

**Como explicar:** o câmbio seleciona a relação entre rotação do motor e torque nas rodas. Eixos e engrenagens transmitem o torque ao diferencial, que permite que as rodas traseiras girem em velocidades diferentes durante a curva.

**Limite:** as oito marchas, a ré, as engrenagens e as juntas mostradas são representação do sistema no laboratório; não declarar relações, dentes, rolamentos ou dimensões reais.

**Fonte:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations).

### 11 — Segurança

**Como explicar:** halo, célula de sobrevivência, estruturas de impacto, proteção lateral, roll hoop e cabos de retenção das rodas formam barreiras e caminhos de carga para proteger piloto e fiscais.

**Limite:** a ausência ou presença de uma malha no GLB não prova homologação; no máximo indica que o item foi ou não modelado para a aula.

**Fontes:** [FIA — nova geração mais segura](https://www.fia.com/news/new-era-competition-fia-showcases-future-focused-formula-1-regulations-2026-and-beyond); [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations).

### 12 — Cockpit e retenção

**Como explicar:** o cockpit organiza banco, pedais, volante, arnês, apoio de cabeça e sistema frontal de retenção (FHR/HANS). Eles mantêm o piloto posicionado e reduzem movimentos perigosos em uma desaceleração.

**Limite:** a cena é um diagrama de localização. Não afirmar certificação do banco, arnês, capacete, HANS ou ajuste do piloto.

**Fontes:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations); [FIA — regulamentos 2026 e melhorias de segurança](https://www.fia.com/news/new-era-competition-fia-showcases-future-focused-formula-1-regulations-2026-and-beyond).

### 13 — Volante e comandos

**Como explicar:** o volante reúne comandos usados pelo piloto para mudar funções do carro, comunicar-se e acompanhar informações. Paddles, botões, display e LEDs são interfaces; os comandos reais dependem do carro e da equipe.

**Limite:** não afirmar que cada botão ou indicação do protótipo corresponde ao hardware de uma equipe real.

**Fonte:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations); [vídeo de referência](https://www.youtube.com/watch?v=V7707zEX9X4&t=803s), usado apenas para a linguagem visual geral.

### 14 — Sensores

**Como explicar:** sensores medem grandezas como pressão, temperatura, rotação, posição e aceleração. O tubo de Pitot mede pressão do escoamento para estimar velocidade do ar; a unidade de aquisição reúne dados para análise e telemetria.

**Limite:** o laboratório não mede fluxo real nem transmite telemetria de um carro. Uma linha desenhada entre sensor e box é uma analogia de dados, não um barramento FIA completo.

**Fontes:** [FIA — regulamento técnico F1, Seção C](https://www.fia.com/regulation/fia-formula-1-technical-regulations); [FIA — regulamento operacional 2026](https://www.fia.com/regulation/fia-formula-1-sporting-regulations); [vídeo de referência](https://www.youtube.com/watch?v=V7707zEX9X4&t=803s).

## Limites gerais do que não pode ser afirmado

1. Não chamar o modelo de CAD, réplica homologada, gêmeo digital ou representação de uma equipe.
2. Não transformar medidas aproximadas da malha, cores, espessuras, posição de peças ou materiais sugeridos em dados regulamentares.
3. Não afirmar desempenho: potência total real, velocidade máxima, downforce, arrasto, grip, temperatura, pressão, vazão, consumo por volta ou ganho de tempo.
4. Não afirmar segurança, resistência a impacto, certificação de halo, célula, banco, arnês, HANS, capacete ou cabos.
5. Não misturar a PU de 2021 do vídeo com a arquitetura 2026: MGU-H, turbo dividido, trompetas variáveis e DRS histórico precisam de etiqueta temporal.
6. Não tratar “350 kW”, “70 kg”, 3.400 mm, 1.900 mm ou 768 kg como valores universais fora das condições, artigos e edição regulamentar que os definem.
7. Não descrever a animação como simulação física: rotações, explosão e conexões são recursos de ensino.

## Riscos factuais para a redação

- **Deriva temporal:** copiar frases do vídeo de 2021 sem mencionar a mudança de 2026, sobretudo sobre MGU-H, turbo e DRS.
- **Número fora de contexto:** usar valores de resumo jornalístico como se fossem limites aplicáveis a qualquer configuração ou sessão.
- **Regra versus layout:** apresentar push-rod, pull-rod, refrigeração assimétrica ou posição exata do tanque como obrigação de todos os carros.
- **Imagem versus prova:** inferir material, função interna ou homologação porque uma peça aparece colorida no overlay.
- **Causa simplificada:** dizer que uma peça “gera” desempenho sem separar carga, arrasto, energia, temperatura e controle.
- **Aero confundida:** chamar todo flap móvel de DRS e manter a regra de proximidade de um segundo na explicação de 2026.
- **ERS confundido:** tratar a bateria, inversor, MGU-K e MGU-H como um único componente ou sugerir que a existência de um rótulo no modo legado significa que ele existe no carro atual.
- **Segurança exagerada:** prometer proteção real, homologação ou resistência de impacto para uma visualização que não foi ensaiada.
- **Telemetria inventada:** descrever linhas de conexão como dados reais, protocolo, ECU específica ou transmissão operacional.
- **Fonte inadequada:** usar blogs, fóruns, marketing de equipe ou memória do modelo para preencher lacunas que o regulamento e a F1 não confirmam.

