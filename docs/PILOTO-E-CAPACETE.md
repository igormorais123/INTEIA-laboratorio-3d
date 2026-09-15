# Piloto, capacete e bancadas — 15/09/2026

## Resultado

O capacete simplificado foi substituído por `helmet-1991.js`, reaproveitado do site principal INTEIA F1 Loop. O mesmo modelo aparece no cockpit e na bancada: casco oval, queixeira projetada, abertura de viseira, acabamento, ferragens, forro e pintura de época.

O corpo foi refeito com superfícies contínuas de seção variável, tronco reclinado, ombros baixos, mangas dobradas, dedos em volta dos punhos do volante, pernas, botas e cintos. As luvas foram posicionadas em relação aos punhos do volante do GLB: aproximadamente x ±0,088, y 0,591, z 0,521 nas unidades do modelo.

## Referências visuais consultadas

- [Mercedes-AMG — W14 no primeiro teste](https://www.mercedesamgf1.com/news/onwards-to-bahrain-w14-completes-initial-running): fotografia frontal do piloto, encaixe do capacete, linha da viseira e relação com o halo. A imagem foi aberta e examinada no navegador.
- [Fotografias do capacete de Ayrton Senna em 1991](https://commons.wikimedia.org/wiki/Category:Helmets_of_Ayrton_Senna_in_1991): vistas frontal, lateral e superior da exposição Honda; formato e detalhes comparados visualmente. O módulo reaproveitado identifica as fotografias de Morio como referência.

As fotografias são referências externas, não texturas incorporadas ao produto. É um estudo modelado de proporções e equipamentos, não um escaneamento de pessoa, uma reprodução fotográfica ou um pacote de segurança homologado. O capacete histórico é uma homenagem inserida no carro do laboratório.

## Uso

- **Carro**: pintura, desmontagem, seleção, movimentos e imagem.
- **Motor**: compartimento, corte para ver pistões e pausa.
- **Capacete**: bancada, encaixe no carro, vistas, ajustes de altura/avanço/inclinação e exportação GLB.
- **Piloto**: corpo completo, encaixe no cockpit e exportação GLB.
- **Ambientes**: box, estúdio, túnel e exportação do box.

Os ajustes de encaixe são visuais e limitados. A exportação do piloto conserva o ajuste; o capacete isolado é exportado na origem. Não alteram o arquivo Blender histórico nem o outro repositório.

## Verificação

A geometria do conjunto tem posições e normais finitas, e o capacete retorna exatamente à posição inicial após 20 ciclos de ajustes. Os testes anteriores do carro e motor continuam ativos. O navegador é usado para conferir vistas, navegação, encaixe e exportação; o teste numérico não avalia realismo visual.

## Atualização de encaixe do site principal

Sincronizado com a correção `7f04d8a` do F1 Loop: escala 0,84, centro em (0; 0,653; 0,068) e inclinação de 0,14 radiano. O capacete fica mais baixo no cockpit. Os ajustes da bancada partem dessa referência.

## Proporção pela referência lateral enviada

Ajuste visual posterior: escala 0,68, centro (0; 0,735; 0,020), mantendo inclinação de 0,14 radiano. Reduz o capacete em 19% em relação ao encaixe anterior e reposiciona o conjunto dentro da abertura do cockpit. Vista lateral da bancada agora sem elevação para comparação. A foto serve como referência de proporção, sem calibração dimensional.
