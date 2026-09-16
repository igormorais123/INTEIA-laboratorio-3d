# Peças sobressalentes do Box — configuração de pista

A seção **Box / Configuração de pista** da bancada Carro troca, no próprio carro montado, as peças que as equipes mudam de corrida para corrida. Cada troca é feita no lugar: a peça sobressalente assume a posição, o giro, a explosão e a seleção da peça original.

## Cenários

| Cenário | Pneus | Asa traseira | Flap dianteiro | Asa de viga | Arrefecimento |
| --- | --- | --- | --- | --- | --- |
| Pista rápida | médio | baixa carga | baixa carga | simples | fechado |
| Pista travada | macio | alta carga | alta carga | dupla | fechado |
| Pista úmida | intermediário | alta carga | original | dupla | fechado |
| Chuva | chuva extrema | alta carga | alta carga | dupla | fechado |
| Calor extremo | duro | original | original | simples | venezianas abertas |
| Carro original | originais | original | original | simples | fechado |

Cada peça também pode ser escolhida individualmente; o cenário correspondente acende quando a combinação coincide. Ao escolher uma peça, o painel mostra sua função e uma curiosidade técnica.

## Peças

| Slot | Variantes | O que é trocado no carro v2 |
| --- | --- | --- |
| Pneus | macio (faixa vermelha), médio (amarela), duro (branca), intermediário (verde, sulcos leves), chuva extrema (azul, sulcos profundos) | `front_tire__01/02`, `rear_tire__01/02`; malha própria por roda, com textura de faixa e sulcos |
| Asa traseira | baixa carga (plano fino, flap curto), alta carga (plano arqueado, flap longo, aba Gurney) | `rear_wing_main_part__01` e `rear_wing_drs__01`; as placas laterais originais permanecem |
| Flap dianteiro | baixa carga (menos ângulo e corda), alta carga (mais ângulo e corda) | `front_wing_top__01`, loft sobre as seções medidas do flap original |
| Asa de viga | dupla (dois elementos) | `rear_wing_bottom_holder__01` |
| Arrefecimento | venezianas abertas na tampa do motor | anexo em `main_body__01`, apoiado na superfície medida da tampa |

As asas substitutas mantêm o material de pintura original do carro, por isso acompanham a cor escolhida em **Personalizar**. Os pneus trazem material próprio.

## Arquivos

| Arquivo | Papel |
| --- | --- |
| `ferramentas/gerar_sobressalentes.py` | Gerador (Blender 5.2, `-b --python`). Importa o carro v2 para ler a origem exata de cada nó alvo e a superfície da tampa, gera as malhas e grava GLB e manifesto. |
| `web/assets/sobressalentes-v1.glb` | Asset com um nó por peça; extras `slot`, `variant`, `target`, `mode` (`geometry` troca a malha do alvo no lugar; `attach` anexa ao alvo). |
| `web/assets/sobressalentes-v1.manifest.json` | Slots, variantes, caixas de cada peça e soma de triângulos, usados pelos testes. |
| `web/src/spares.js` | Catálogo (slots, cenários, fichas) e a troca em tempo de execução. |
| `web/test-spares.mjs` | Integridade do GLB, coerência catálogo/manifesto, envelopes das peças e controles do template. |

## Regenerar

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python ferramentas/gerar_sobressalentes.py
npm --prefix web test
npm --prefix web run build
```

O GLB fica em torno de 4 MB sem compressão de malha e é um dos oito arquivos que o sincronizador copia ao checkout de deploy (ver [PUBLICACAO.md](PUBLICACAO.md)).

## Limites

As peças representam as famílias de ajuste de uma equipe (composto, carga aerodinâmica, arrefecimento), não o catálogo de um carro específico. As trocas não alteram o túnel de vento nem a mecânica de montagem; são visuais e didáticas.
