# Pesquisa — sistemas de um carro de Fórmula 1 a partir do vídeo

## Escopo e método

- **Projeto-alvo:** `INTEIA-laboratorio-3d`.
- **Vídeo principal:** [How a Formula 1 Race Car Works — Animagraffs](https://www.youtube.com/watch?v=V7707zEX9X4), duração observada de 23:12, publicado em 2021-11-16.
- **Ponto indicado:** `13:23` (`t=803s`), dentro do capítulo **Engine**.
- **Data da consulta:** 2026-09-15.
- **Método:** leitura da página do vídeo, capítulos e descrição visíveis; amostragem visual dos quadros nos capítulos e dos rótulos desenhados no próprio vídeo; confronto pontual com regulamentos FIA e explicadores oficiais da Fórmula 1.
- **Transcrição:** a exportação de transcrição não retornou texto utilizável, embora a página anuncie faixas automáticas. Portanto, as observações abaixo não são uma transcrição integral do áudio.

### Convenções de evidência

- **[OBS]** — aparece visualmente no vídeo ou é um rótulo textual visível.
- **[CONF]** — confirmado por documentação oficial do projeto, FIA ou Fórmula 1.
- **[HIP]** — interpretação de modelagem ou hipótese de ligação funcional; não deve ser apresentada como fato observado.
- **[LIM]** — limite, incerteza ou diferença de versão.

## Contexto de versão

O vídeo descreve um carro híbrido da geração anterior às regras de 2026. Na imagem e nos rótulos aparecem **MGU-H** e **MGU-K**. A explicação oficial da Fórmula 1 para 2026 confirma que o V6 turbo de 1,6 litro foi mantido, mas o **MGU-H foi removido** e o **MGU-K** passou a concentrar uma parcela maior da recuperação e entrega elétrica. Portanto, o carro do INTEIA deve ter pelo menos dois modos didáticos:

1. **Modo vídeo / híbrido 2014–2025:** mostra MGU-H, MGU-K, armazenamento de energia, eletrônica de controle e fluxos associados.
2. **Modo atual 2026:** mantém V6 turbo, MGU-K, energy store, control electronics e exaustão, mas remove o MGU-H do caminho ativo.

Misturar os dois sem um aviso de época seria tecnicamente enganoso. [CONF — [F1: 2026 power units](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd) e [FIA: regulamentos 2026](https://admin.fia.com/regulation/category/110)]

## Linha do tempo observada

| Timestamp | Sistema / termo exato | O que é observável | Implicação didática |
|---|---|---|---|
| `0:14` | **Aerodynamics** | Carro completo, asa dianteira de múltiplos elementos, assoalho/difusor, sidepods e asa traseira são mostrados em vistas transparentes e de fluxo. | Separar a carroceria aerodinâmica em grupos inspecionáveis; manter o túnel do projeto explicitamente como aproximação por coeficientes, não CFD. |
| `4:47` | **Core support structure** | O vídeo remove a carroceria e deixa uma estrutura central longitudinal com cockpit, pontos de suspensão e conjuntos dianteiro/traseiro. | Criar uma vista estrutural do chassi/survival cell sem afirmar que a malha atual é um monocoque homologado. |
| `5:19` | **Suspension** | Conjuntos de roda, braços e elementos diagonais são separados; o rótulo **track rod** aparece na sequência de direção. | Expor wishbones, uprights, push/pull-rod, mola torsional e amortecedor como cadeia cinemática visual. |
| `7:52` | **Steering** / **track rod** | A roda dianteira, o conjunto de direção e uma barra longitudinal são mostrados com a carroceria transparente. | Girar volante, coluna/rack, track rod, upright e roda dianteira em uma única interação encadeada. |
| `8:57` | **Braking system** | Discos/calipers e linhas do pedal até os freios são desmontados; a vista mostra componentes separados por eixo. | Criar inspeção de disco, pinça, duto, pedal e linhas; representar a divisão dianteira/traseira como diagrama, não como medição real. |
| `11:32` | **Engine** | Motor em corte, V6, admissão e exaustão; a sequência do ponto indicado passa por turbo, gases e **waste gate**. | Separar ICE, turbo, compressor/turbina, wastegate, coletor, escape, virabrequim e pistões em camadas. |
| `13:23` | Engine / **trumpets** / **plenums** | O frame verificado em `t=803,275s` destaca os rótulos **“trumpets”** e **“plenums”**; **waste gate** pode permanecer apenas como elemento/trecho adjacente, sem ser a identificação principal do quadro. | Usar o momento como entrada da aula do motor; permitir corte, pausa, animação de pistões e fluxo de admissão/exaustão. |
| `14:14` | **ERS — Energy Recovery System** | Bateria/armazenamento, cabos destacados e dois geradores aparecem ligados por um caminho energético. | Mostrar estados `recuperar`, `armazenar` e `entregar`, com caminhos separados para frenagem e exaustão. |
| `14:21` | **MGU-H — Motor Generator Unit Heat**; **MGU-K — Motor Generator Unit Kinetic** | Os rótulos aparecem sobre dois módulos distintos do sistema híbrido. | Em modo histórico, ligar MGU-H ao turbo/exaustão e MGU-K ao eixo traseiro/frenagem; em modo 2026, marcar MGU-H como legado. |
| `14:54` | **Cooling systems**; **hydraulics, gearbox, and ERS system coolers** | Radiadores/volumes de refrigeração são mostrados nos sidepods; outra tela nomeia coolers de hidráulica, câmbio e ERS. | Diferenciar ar de refrigeração, fluido hidráulico e fluido térmico; não animar todos como se fossem o mesmo circuito. |
| `15:39` | **Fuel tank** | Um tanque/bladder amarelo aparece dentro da região central protegida do carro. | Fazer corte do tanque e linhas de combustível; bloquear a passagem de linhas pelo cockpit na representação didática. |
| `16:42` | **gearbox** | Uma caixa de engrenagens é isolada, com eixos e conjuntos internos visíveis. | Adicionar caixa sequencial, diferencial, eixo de transmissão e seleção de marcha; o vídeo corrigiu a contagem para 8 marchas à frente e 1 ré. |
| `17:03` | **Safety systems** | A carroceria se separa em torno da célula do piloto, estruturas de impacto e elementos de proteção. | Criar modo “segurança” com monocoque/survival cell, halo, roll structures, cintos, extintor, headrest e estruturas de impacto. |
| `17:51` | **Cockpit** | Piloto reclinado, pernas à frente, cockpit estreito, cintos e halo são mostrados em vista lateral/transparente. | Usar o piloto e capacete já existentes como âncora espacial; permitir inspeção sem confundir uma pose visual com ergonomia validada. |
| `19:17` | **Steering wheel** | Volante com display, LEDs, seletores, botões e borboletas; rótulos visíveis: **gear shift -/+**, **customizable**, **clutch**. | Criar hotspots do volante e um painel de leitura; separar botões de função, troca de marcha, embreagem e indicadores. |
| `21:46` | Pedais e comandos | A sequência mostra **brake pedal** e **gas pedal** em posições distintas; o vídeo também mostra acionamentos do volante. | Animar curso relativo dos pedais e ligar o pedal de freio ao sistema de frenagem/recuperação apenas como diagrama. |
| `22:11` | **Sensors**; `22:17` **pitot tube** | Um pequeno tubo sobre a dianteira é apontado e rotulado; o comentário fixado corrige “pilot” para **Pitot**. | Adicionar Pitot, sensores de roda, direção, pressão de freio e temperatura como camada de instrumentação/telemetria visual. |
| `22:31` | **Size comparison** | Retorno ao carro completo e aos pedais para comparação de escala. | Encerrar a aula com escala humana; não usar o enquadramento para inferir dimensões exatas sem uma referência homologada. |

## Sistemas identificados e proposta de modelagem

### 1. Aerodinâmica

- **[OBS]** Asas, assoalho, difusor, sidepods e asa traseira aparecem em vistas de fluxo e transparência.
- **[CONF]** O projeto já possui categoria `aero`, peças da asa dianteira/traseira e DRS; o ensaio atual é por coeficientes e a própria documentação diz que não é CFD.
- **[HIP]** Acrescentar superfícies internas do assoalho, canais de sidepod e elementos de fluxo como geometrias didáticas separadas, sem alterar os IDs das 97 peças atuais.
- **Interação:** botão “fluxo” alterna partículas/linhas, “DRS” abre o flap e “isolar” mostra a peça. O painel deve dizer “visualização didática por coeficientes”.

### 2. Estrutura e segurança

- **[OBS]** O vídeo chama a estrutura central de **core support structure** e depois mostra **safety systems** e cockpit.
- **[CONF]** A Fórmula 1 descreve a célula de sobrevivência/monocoque como o núcleo em que piloto, motor e suspensão se apoiam; o halo é proteção do cockpit. A FIA regula estruturas de segurança, testes de impacto, extintor e equipamentos do piloto. [F1: segurança](https://www.formula1.com/en/latest/article/5-crucial-milestonemoments-in-f1-safety-technology.4rlVLaoq24DjmJKtusZ0tp) · [FIA 2021 Technical Regulations](https://www.fia.com/sites/default/files/2021_formula_1_technical_regulations_-_iss_5_-_2020-06-19.pdf)
- **[LIM]** O `main_body` do projeto é uma casca exterior conectada; a documentação local não estabelece uma célula estrutural real nem homologação.
- **Interação:** “modo segurança” deve trocar a carroceria por transparência, destacar survival cell, halo, estruturas de rolagem e zonas de impacto e abrir fichas de função. Deve ser uma visualização, não um teste de crash.

### 3. Suspensão, direção e rodas

- **[OBS]** O vídeo mostra suspensão exposta, track rod e a conexão da roda dianteira ao comando de direção.
- **[CONF]** A explicação oficial da Fórmula 1 confirma suspensão independente de quatro rodas, double wishbone, push-rod/pull-rod, mola torsional e amortecedores. [F1: push-rod e pull-rod](https://www.formula1.com/en/latest/article/explainer-whats-the-difference-between-pull-rod-and-push-rod-suspension.1I3wL4LEL0nQZbKZbx1Dhz)
- **[CONF]** O catálogo local já separa 18 peças de `suspension` e 24 conjuntos de rodas, mas os nomes atuais não provam a identidade mecânica de cada braço.
- **Interação:** modo “cinemática” deve ter um pequeno bump controlado, giro de direção e destaque de forças conceituais. Evitar física de suspensão até existirem massa, rigidez, amortecimento, limites e colisores documentados.

### 4. Frenagem e brake-by-wire

- **[OBS]** O capítulo **Braking system** separa pedal, discos/calipers e linhas.
- **[CONF]** A explicação técnica oficial descreve a unidade de controle de energia ajustando a pressão traseira conforme a frenagem regenerativa do MGU-K e o balanço solicitado pelo piloto; o sistema híbrido pode compartilhar hidráulica com troca, embreagem, diferencial, acelerador e DRS na arquitetura descrita. [F1: brake-by-wire](https://www.formula1.com/en/latest/article/technical-analysis-brake-by-wire-systems-explained.1XQiBCFqA6WYZwLmb3JLxi)
- **[HIP]** Para o INTEIA, o caminho mais didático é `pedal → pressão solicitada → freio dianteiro/traseiro + recuperação MGU-K`, com cores e setas, sem simular pressão real.
- **Interação:** pedal de freio com animação de curso, discos em rotação e indicador conceitual de recuperação. Temperatura, aderência e distância de parada só devem aparecer como “modelo aproximado” se houver parâmetros explícitos.

### 5. Motor, turbo e exaustão

- **[OBS]** O frame verificado em `t=803,275s` destaca **“trumpets”** e **“plenums”**; **waste gate** pode aparecer apenas como elemento/trecho adjacente qualificado. O capítulo também mostra motor em corte e pistões.
- **[CONF]** Para a geração atual, a unidade de potência inclui ICE, turbocharger, energy store, control electronics, MGU-K e exhaust; para a geração do vídeo, o MGU-H também participa do conjunto. [F1: componentes da power unit](https://www.formula1.com/en/latest/article/the-beginners-guide-to-f1-engine-and-gearbox-penalties.2TSy7BFgEvdNLojGLWS3F1)
- **[CONF]** O projeto já carrega `power-unit-v1.glb`, descrito localmente como V6 didático original com 19 canais de animação, e já oferece corte, pistões, pausa e abertura da tampa.
- **Interação:** manter o motor como submodelo sob demanda; adicionar hotspots para cilindros, virabrequim, turbo, compressor/turbina, wastegate, escape e coletor. O usuário deve poder pausar cada subfluxo.
- **[LIM]** A geometria atual é didática, sem combustão, torque, temperaturas ou certificação de engenharia.

### 6. ERS, bateria e atualização 2026

- **[OBS]** O vídeo visualiza cabos, armazenamento, MGU-H e MGU-K; a imagem do ERS usa cores para separar o caminho energético.
- **[CONF]** MGU-K recupera energia cinética de frenagem; MGU-H era o gerador ligado ao calor/fluxo de exaustão. A Fórmula 1 informa que o MGU-H não faz parte da unidade de 2026. [F1 Glossary](https://www.formula1.com/en/latest/article/f1-glossary-k-o.6g2hrWHA2pyxbXoe8FT9Db)
- **Interação:** seletor “vídeo 2014–2025 / atual 2026” controla a presença do MGU-H; o modo atual deve mostrar o MGU-K com recuperação em frenagem, coasting e outras fases descritas pela F1, sem desenhar um MGU-H ativo.
- **[LIM]** Não usar valores de potência/energia do explicador de 2026 para representar o carro histórico do vídeo sem rotular a versão.

### 7. Refrigeração e fluidos

- **[OBS]** Radiadores e volumes laterais aparecem no capítulo **Cooling systems**; o vídeo nomeia **hydraulics, gearbox, and ERS system coolers**.
- **[HIP]** Separar quatro camadas: ar externo/radiador, fluido do motor, hidráulica e refrigeração de câmbio/ERS. A visualização pode mostrar cada uma por cor e direção, mas não deve alegar cálculo térmico.
- **Interação:** ligar/desligar camadas, selecionar cooler e seguir o fluxo até a saída do sidepod; adicionar aviso “fluxo esquemático”.

### 8. Combustível

- **[OBS]** O tanque é mostrado em amarelo na célula central, com linhas/volumes ao redor.
- **[CONF]** A regulamentação FIA 2026 exige tanque como bladder de borracha conforme FT5-1999, restringe a região de armazenamento e proíbe linhas de combustível passando pelo cockpit; as linhas entre tanque e motor devem ter válvula breakaway auto-selante. [FIA 2026 PU Technical Regulations](https://www.fia.com/sites/default/files/fia_2026_formula_1_technical_regulations_pu_-_issue_7_-_2024-06-11_1.pdf)
- **Interação:** corte do survival cell, tanque destacado, caminho de alimentação e ficha de segurança. Não incluir combustível real, abastecimento interativo ou risco operacional; o objetivo é anatomia e segurança.

### 9. Câmbio, diferencial e transmissão

- **[OBS]** O vídeo isola e rotula **gearbox**; a animação mostra engrenagens e eixos.
- **[CONF]** O comentário fixado pelo próprio canal corrige a informação para **8 forward gears and 1 reverse**. O mesmo comentário registra que não há Launch Control; um seletor mostrado no volante permanece sem identificação resolvida.
- **[HIP]** O projeto deve modelar um câmbio esquemático com oito relações à frente, ré, seletor sequencial, diferencial e driveshafts, mas manter a contagem e o rótulo separados da caixa visual atual.
- **Interação:** selecionar marcha faz girar pares correspondentes e altera o caminho de torque em um diagrama; não apresentar relações, perdas ou tempos de troca como dados reais sem fonte específica do carro.

### 10. Cockpit, piloto, pedais, volante e sensores

- **[OBS]** O vídeo mostra posição reclinada, pedais **brake pedal** e **gas pedal**, volante com display/LEDs, **gear shift -/+**, **clutch** e o tubo de Pitot.
- **[CONF]** O projeto já possui piloto, capacete, cockpit, display do volante, botões, LEDs e empunhaduras em sua documentação de componentes; também preserva controles de montagem/desmontagem e modo de inspeção.
- **[HIP]** A interação deve fazer o cockpit virar uma bancada: selecionar pedal, mostrar curso; selecionar volante, abrir mapa de comandos; selecionar Pitot, abrir uma ficha de pressão dinâmica/velocidade apenas conceitual; selecionar sensores, mostrar um barramento de telemetria fictício.
- **[LIM]** Um sensor visível não equivale a telemetria real. O tubo é **Pitot**, conforme correção do canal, e não “pilot”.

## Estado atual do projeto e lacunas

### Já existe e pode ser reaproveitado

- 97 componentes exteriores com IDs e contrato de montagem.
- Categorias locais `aero` (31), `suspension` (18), `wheels` (24), `cockpit` (11), `details` (12) e `body` (1).
- DRS, giro de rodas, direção dianteira, desmontagem, isolamento, materiais, iluminação e túnel didático.
- Motor V6 ilustrativo sob demanda, com corte, pistões, pausa e animação.
- Piloto/capacete/cockpit e elementos do volante já catalogados.

### Ainda não está estabelecido pela base atual

- Câmbio completo com engrenagens funcionais, diferencial e relações de transmissão.
- Rig físico de suspensão, colisores, massas, molas, amortecedores e validação contra um carro real.
- Sistema hidráulico ou elétrico real; os fluxos podem ser animações esquemáticas.
- Tanque/linhas de combustível, células de impacto, extintor, sensores e instrumentação como submodelos completos.
- Telemetria real, CFD, combustão, torque, temperaturas e homologação.

Essas lacunas devem virar módulos didáticos identificados, não detalhes “inventados” dentro dos 97 componentes existentes. [CONF — [componentes-origem.json](../documentacao/componentes-origem.json), [INTEGRACAO-MOTOR.md](INTEGRACAO-MOTOR.md) e [VALIDACAO.md](VALIDACAO.md)]

## Ordem recomendada para uma próxima iteração

1. **Estrutura/base de inspeção:** survival cell, cockpit, halo, zonas de impacto e convenção de transparência.
2. **Suspensão e direção:** wishbones, track rod, upright, push/pull-rod e direção encadeada.
3. **Freios e pedais:** discos, calipers, pedal e diagrama brake-by-wire/recuperação.
4. **Power unit em dois períodos:** integrar o motor existente com hotspots de turbo/wastegate e alternância MGU-H legado/2026.
5. **ERS e refrigeração:** battery/energy store, MGU-K, MGU-H legado, coolers e estados de energia.
6. **Tanque, câmbio e transmissão:** bladder protegido, oito marchas + ré, diferencial e eixos.
7. **Cockpit, volante e sensores:** display didático, controles, pedais, Pitot e telemetria fictícia.
8. **Validação visual e de interação:** cada sistema com vista montada, vista transparente, isolamento, retorno sem deriva, redução de movimento e fallback sem GLB.

## Fontes e limites

### Fontes primárias/autoridades

- [Vídeo principal — Animagraffs, How a Formula 1 Race Car Works](https://www.youtube.com/watch?v=V7707zEX9X4) — fonte observável de capítulos, rótulos e diagramas; é uma “well informed speculation”, não um manual de equipe.
- [FIA — 2021 Formula 1 Technical Regulations](https://www.fia.com/sites/default/files/2021_formula_1_technical_regulations_-_iss_5_-_2020-06-19.pdf) — contexto regulatório compatível com a época do vídeo, incluindo estruturas de segurança, combustível e extintor.
- [FIA — categoria de regulamentos da Fórmula 1](https://admin.fia.com/regulation/category/110) — índice oficial com os regulamentos 2026 vigentes e documentos por seção.
- [FIA — 2026 Formula 1 Power Unit Technical Regulations](https://www.fia.com/sites/default/files/fia_2026_formula_1_technical_regulations_pu_-_issue_7_-_2024-06-11_1.pdf) — tanque, linhas de combustível e arquitetura regulatória de unidade de potência.
- [Fórmula 1 — 2026 power units](https://www.formula1.com/en/latest/article/2026-regulations-explained-all-you-need-to-know-about-f1s-new-power-units.14jfv7a36905uDJDdNyfQd) — diferença entre geração do vídeo e 2026, especialmente a retirada do MGU-H.
- [Fórmula 1 — suspensão push-rod/pull-rod](https://www.formula1.com/en/latest/article/explainer-whats-the-difference-between-pull-rod-and-push-rod-suspension.1I3wL4LEL0nQZbKZbx1Dhz) — confirmação de double wishbone, rods, mola torsional e amortecedor.
- [Fórmula 1 — brake-by-wire](https://www.formula1.com/en/latest/article/technical-analysis-brake-by-wire-systems-explained.1XQiBCFqA6WYZwLmb3JLxi) — relação entre pedal, recuperação do MGU-K e freio traseiro.
- [Fórmula 1 — glossário de componentes](https://www.formula1.com/en/latest/article/f1-glossary-k-o.6g2hrWHA2pyxbXoe8FT9Db) e [glossário P–T](https://www.formula1.com/en/latest/article/f1-glossary-p-t.GBhLQtpeu9b8LrK5VM0F1) — terminologia de PU, MGU-K, MGU-H, suspensão e volante.

### Limitações desta coleta

- Não houve transcrição integral nem acesso a desenhos internos de uma equipe.
- Os rótulos do vídeo identificam componentes, mas não fornecem dimensões, tolerâncias, materiais, curvas de desempenho ou topologia completa.
- O vídeo é de 2021; regras, nomes e arquitetura de 2026 não devem ser retroprojetados para todos os seus quadros.
- A inspeção visual do projeto confirma documentação e assets existentes, não valida a física de um carro real.
- Qualquer futura peça criada a partir desta pesquisa deve receber procedência própria e ser marcada como **didática**, **hipotética** ou **legado do vídeo**, conforme o caso.
