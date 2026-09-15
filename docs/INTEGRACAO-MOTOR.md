# Carro final e motor no laboratório — 15/09/2026

O laboratório web reaproveita o carro final de `inteia-f1-loop`: `carro-aula-v2.glb`, assinatura e brasão INTEIA, número 1, Inteligência Mil Grau, acabamento de pintura, rodas e piloto. As marcas seguem a carroceria durante a desmontagem. O box e o túnel existentes foram preservados.

## Operação

- **Abrir compartimento do motor** monta o carro, encerra o túnel, abre a tampa e aproxima a câmera.
- **Corte para ver pistões** remove visualmente parte do bloco e expõe os componentes móveis.
- **Pausar motor** interrompe a animação; a preferência de movimento reduzido também é respeitada.
- **Desmontar** fecha o recorte da tampa e separa as peças exteriores, mantendo o motor visível. **Montar** e **Restaurar** recompõem o carro.
- Selecionar peças fecha a tampa para preservar os controles de seleção e deslocamento. O motor é explorado por seus controles próprios.
- O carregamento do motor acontece sob demanda. Uma falha mantém o carro utilizável e mostra uma mensagem no painel do motor.

## Procedência

O carro v2 mantém 97 componentes e o contrato de montagem. Os arquivos de procedência e os hashes originais foram copiados para `web/assets`. O motor `power-unit-v1.glb` é uma geometria didática original INTEIA (CC BY 4.0), com 19 canais de animação, também documentada no manifesto do asset. As marcas foram reaproveitadas dos arquivos do site, sem redesenho.

## Limites

Motor V6 ilustrativo, sem simulação de combustão ou certificação de engenharia. O túnel continua didático, por coeficientes. Esta integração atualiza o laboratório **web**; os arquivos Blender e GLB históricos nas pastas `modelos` e `ambientes` não foram substituídos.

## Verificação

`npm test` em `web`: 20 ciclos do carro sem deriva, quatro conjuntos de rodas, DRS, restauração após mover/isolar peças, fórmulas do túnel e 20 ciclos da animação do motor sem deriva. A revisão visual é feita no navegador com carro montado, tampa aberta, corte, pausa, vista explodida e retorno ao túnel.
