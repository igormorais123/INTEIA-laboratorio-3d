# Túnel de vento — escopo físico

Abra o site e clique em **Túnel de vento** na barra abaixo do carro. Ajuste velocidade do carro, vento frontal/de cauda, vento lateral, temperatura e pressão. Monte o carro e saia do isolamento para calcular forças.

Este módulo é um ensaio por coeficientes, não um solver CFD. As forças seguem equações aerodinâmicas; os coeficientes precisam vir de ensaio ou CFD externo na mesma geometria, referência de área, ângulo de vento e condição de operação. Não são determinados a partir do GLB.

## Entradas e resultados

- Velocidade relativa axial = (velocidade do carro + vento frontal) / 3,6; vento de cauda tem sinal negativo.
- Velocidade relativa lateral = vento lateral / 3,6. A norma do vetor é usada nas equações.
- Ar seco ideal: densidade = pressão absoluta / (287,05 × temperatura absoluta), em SI.
- Pressão dinâmica q = ½ρV²; arrasto D = qCdA; carga para baixo F↓ = qC↓A.
- C↓ é definido positivo para baixo; não é Cl com a convenção de sustentação positiva para cima.
- Potência dissipada no ar = D × V relativo. Com vento, não equivale à potência de tração do veículo. Não calcula consumo do motor.
- Reynolds usa comprimento longitudinal da caixa do modelo e viscosidade pela lei de Sutherland. Mach usa velocidade do som do ar ideal.

Coeficientes/área começam vazios. O botão **Carregar exemplo hipotético** preenche A=1,5 m², Cd=0,9 e C↓=3,0 somente como cenário matemático. Esses valores não foram medidos neste carro nem constituem referência técnica de F1. Alterá-los passa a identificar a origem como usuário não validado.

O cálculo de forças é bloqueado para Mach ≥ 0,3, peças afastadas ou isolamento. Curvas e CSV mantêm coeficientes constantes, e omitem forças fora da faixa incompressível. Resultados dependem dessa hipótese: não preveem resposta a DRS, direção, estol, efeito solo, separação, turbulência, mudanças de geometria ou movimento das rodas. Esses controles visuais não recalibram coeficientes.

## Visualização

O modo **Túnel de vento** agora abre uma câmara escura com piso de testes, trilhos, estruturas transversais iluminadas e grade ao fundo. O painel prioriza densidade da fumaça, dispersão na esteira, ritmo e pausa. Os cálculos anteriores ficam em **Condições e cálculos do ensaio**.

**Travelling suave** movimenta a câmera em um arco limitado. Arrastar a câmera ou escolher uma vista interrompe o travelling. **Só o carro** oculta o painel e os elementos sobre a cena, preservando o túnel; clique novamente para voltar. O movimento automático respeita a preferência de movimento reduzido do sistema.

Após a revisão visual adicional, os filetes geométricos foram removidos. A fumaça usa 7.200 partículas transparentes sobrepostas, com ruído procedural e dispersão crescente na esteira. Cinco emissores definem as trajetórias artísticas. O ritmo é artístico e não mede o tempo de trânsito do ar. Pausar mantém o instante atual. Densidade e dispersão são ajustes visuais, sem efeito nos coeficientes ou nas forças. Não há fumaça quando a velocidade relativa é zero ou o carro está desmontado/isolado. Paredes externas deixam de ocultar o carro quando a câmera passa para trás delas.

O túnel faz parte da experiência Web. Esta revisão não foi incorporada ao arquivo Blender nem exportada como vídeo.

Traçadores contornam um envelope analítico simplificado, sem resolver o escoamento ao redor de cada peça. Não representam velocidade local, pressão, vorticidade ou turbulência medida. Podem cruzar detalhes geométricos. As setas indicam sentido e magnitude visual limitada; não têm escala métrica. Movimento reduzido mantém os traçadores estáticos.

O gráfico mostra como arrasto e carga variam com velocidade do carro, mantendo vento e demais entradas. O CSV registra parâmetros, origem hipotética/não validada, forças, Mach e validade do modelo. Não é laudo aerodinâmico.

## Para uma análise real da geometria

É necessário preparar a superfície para CFD, definir domínio e malha volumétrica/camada limite, condições de contorno (solo móvel, rodas, velocidade), modelo de turbulência, convergência e independência de malha. Só então extrair coeficientes e mapas de pressão, comparando com ensaio físico quando disponível. Este trabalho não foi executado pelo módulo do navegador.

## Fundamentos

- [NASA — equação de arrasto](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/drag-equation/)
- [NASA — equação de sustentação](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/lift-equation/)
- [NASA — pressão dinâmica](https://www1.grc.nasa.gov/beginners-guide-to-aeronautics/dynamic-pressure/)

Execute `node test-aerodynamics.mjs` na pasta web para testar unidades, escala de forças com V², potência com V³, vento relativo, densidade e condições inválidas.

## Leitura visual por região

**Trajetórias e sentido do ar** combina trajetórias discretas contínuas, pulsos com caudas e setas fixas. As setas permitem ler a direção também com a animação pausada. Em **Explorar uma região**:

- **Carroceria e asas:** azul-claro; trajetórias sobre e ao lado do envelope do carro.
- **Esteira das rodas:** âmbar; pares de curvas em espiral atrás das rodas traseiras, com câmera reposicionada para incluir a esteira.
- **Assoalho e difusor:** verde-claro; carroceria transparente e assoalho destacado, com vista elevada e estruturas superiores ocultadas para não obstruir a leitura.

A seleção diminui a fumaça de fundo para preservar a legibilidade. Desligar trajetórias ou sair do túnel restaura os materiais originais; a transparência usa cópias temporárias dos materiais e não altera os modelos exportados.

Essas cores identificam **regiões**, nunca pressão, velocidade ou intensidade medidas. Os percursos e espirais são formas ilustrativas baseadas nas dimensões externas. Não provam vórtices reais, separação ou aceleração local; podem cruzar a geometria, e não respondem ao DRS ou à forma de cada peça como responderia um solver CFD. O vento lateral gira o conjunto de trajetórias, sem recalculá-las a partir da malha.
