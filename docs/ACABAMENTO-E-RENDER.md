# Acabamento, reflexos e render do laboratório

## O que mudou

A pintura vermelha usa camada de verniz de baixa rugosidade, sem os mapas herdados do tutorial que poderiam interferir no acabamento. O carbono tem uma resposta especular mais perceptível; aço e bancadas usam acabamento metálico, enquanto as paredes e o piso mantêm resposta não metálica. Pneus preservam microrrelevo e têm reflexo mais amplo que os metais.

No navegador, duas luzes retangulares complementam a iluminação do box. A captura do ambiente de reflexão foi deslocada para 75 cm de altura e sua suavização reduzida. Os equipamentos superiores não projetam mais a grade de sombras duras sobre o carro; esta é uma simplificação do render interativo. O tratamento de cor ACES foi mantido após comparação com AgX, que reduziu a saturação desejada do vermelho nesta configuração.

Após inspeção, a energia das luzes foi reduzida para evitar clarear o vermelho. No Blender, luzes de área substituem as luzes direcionais importadas. A cena Cycles está configurada para 128 amostras; a prévia final usa 64 amostras, amostragem adaptativa e redução de ruído, com saída de 1600 × 1000. A imagem anterior tinha 16 amostras e 1000 × 625. Microtextura procedural dos pneus e bevel de sombreamento em metais acrescentam detalhe sem alterar as peças. O script de prévia limita futuros renders a seis threads para preservar a resposta do computador.

## Fontes e reutilização

- `web/src/studio.js`: materiais do carro.
- `web/src/customize.js`: opções de acabamento.
- `web/src/garage.js`: materiais, iluminação e ambiente de reflexão do box.
- `ferramentas/package_garage.py`: composição e materiais Blender.
- `ferramentas/render_garage_preview.py`: render final.
- `ambientes/INTEIA_Box_com_carro.blend`: cena editável, materiais e luzes do Cycles.
- `ambientes/INTEIA-box-laboratorio.glb`: geometria e materiais exportáveis do box.

O GLB não transporta luzes retangulares do Three.js nem shaders procedurais do Blender; os scripts reconstroem as respectivas configurações. O Blender e o navegador não produzem imagens idênticas. O modelo estático original do carro foi preservado; o novo acabamento Blender está na cena do box.

## Limites

Esta revisão trata acabamento e luz, não reconstrói a topologia do carro nem transforma móveis simplificados em assets industriais digitalizados. Reflexos em tempo real usam mapa de ambiente: não são reflexos completos por ray tracing de cada peça ou do carro no piso. Para imagem final, use a cena Cycles. A migração para outro motor, isoladamente, não acrescenta detalhes ausentes da geometria.

O Cycles é um renderizador físico por path tracing: https://www.blender.org/features/rendering/ . Não foi feita migração nem comparação medida com Unreal Engine.
