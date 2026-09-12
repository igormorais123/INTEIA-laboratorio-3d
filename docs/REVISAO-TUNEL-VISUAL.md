# Túnel de vento — cinco iterações visuais

Data: 12/09/2026. Avaliador independente: subagente Codex. Avaliação visual subjetiva, sem certificação física ou de fotorrealismo.

| Rodada | Mudança e parecer | Ambiente | Fumaça | Leitura do carro | Composição |
|---|---|---:|---:|---:|---:|
| 1 | Câmara física e filetes. Rejeitada: aparência de cabos, carro encoberto. | 6 | 2 | 4 | 5 |
| 2 | Menos filetes, menor espessura e opacidade. Aceita como avanço. | 6 | 3,5 | 7 | 6,5 |
| 3 | Partículas e curvas menores. Rejeitada: pontos pareciam poeira. | 6 | 3 | 6,5 | 6 |
| 4 | Esteira difusa, controles visuais e enquadramento amplo. Aceita. | 6,5 | 5 | 7 | 6,5 |
| 5 | Estruturas iluminadas superiores, bordas suavizadas e travelling limitado. Aceita como versão final do ciclo. | 7 | 5 | 7 | 7 |

As notas são sobre 10. As rodadas rejeitadas foram corrigidas na seguinte; não representam opções disponíveis na interface.

## Como usar

1. Abra o laboratório e clique em **Túnel de vento**.
2. Ajuste **Densidade da fumaça**, **Dispersão na esteira** e **Ritmo da animação**.
3. Use **Pausar fumaça** para congelar o fluxo; a câmera permanece independente.
4. Clique em **Travelling suave** para movimentar a câmera. Arrastar ou escolher uma vista interrompe o travelling.
5. Use **Só o carro** para esconder o painel e os elementos sobre a cena.
6. Os controles físicos anteriores ficam em **Condições e cálculos do ensaio**.

## Verificação

- Build local concluído e testes existentes de mecânica e aerodinâmica aprovados.
- Navegador: sem erros de console na inspeção, controles de pausa/retomada e densidade exercitados.
- Duas capturas espaçadas com a fumaça pausada produziram imagens idênticas pixel a pixel.
- Travelling registrado em dois instantes distintos. Isso comprova mudança de enquadramento, não certifica fluidez em todo o percurso.
- 30 fps observados pontualmente em 1440 × 960; não é benchmark nem garantia para outros dispositivos.
- Interface exercitada em 390 × 844, incluindo pausa e retorno ao estúdio. Enquadramento se ajusta à mudança de tamanho.

## Limites do resultado

A esteira difusa e o ambiente melhoraram, mas os filetes ainda lembram linhas gráficas. A versão permanece reconhecivelmente digital. O juiz apontou uma extremidade de estrutura entrando pela lateral em um instante do travelling, sem esconder o carro.

O fluxo usa um envelope artístico e pode cruzar detalhes da geometria: não é um campo de ar calculado sobre a malha. O ritmo visual é ajustável e não reproduz o tempo físico do ensaio. O túnel está no HTML; esta entrega não cria vídeo renderizado nem atualiza o Blender com o cenário.
