# Box-laboratório INTEIA

Ambiente 3D original para apresentar, inspecionar e preparar visualmente o carro. Inspiração em fotografias e descrições públicas de boxes e estações de engenharia de Fórmula 1. Não é uma réplica de uma instalação específica nem um projeto executivo de box homologado.

## Navegador

O carro abre no **Box INTEIA**. **Ver o box** amplia o enquadramento. O botão **Box INTEIA** alterna entre o box e o estúdio. Entrar em **Túnel de vento** oculta o box e preserva a experiência de fluxo; sair retorna ao ambiente anterior.

Paredes e estruturas superiores deixam de obstruir a câmera em vistas externas/elevadas. É uma convenção de visualização, não uma animação mecânica da instalação.

O cenário inclui piso de trabalho com placas de inspeção, módulos de gavetas, estação de engenharia com três posições, monitores, carrinho e ferramentas, pistola e mangueira de ar, rack com pneus, macaco estacionado, iluminação suspensa e cabos de serviço. Materiais, luzes e reflexos são calculados em 3D. Não foram usadas fotografias como fundo do ambiente.

O monitor **Configuração** mostra valores reais do visualizador: quantidade de componentes, montagem, direção e abertura da asa. Os demais monitores são cenográficos e identificam a ausência de telemetria. Nenhuma medição de pista, desempenho ou estratégia otimizada foi inventada.

## Arquivos reutilizáveis

- `ambientes/INTEIA-box-laboratorio.glb`: somente o ambiente, com geometrias, materiais, telas incorporadas e luzes exportáveis. O botão **Baixar box 3D** exporta uma nova cópia com o estado atual dos monitores.
- `ambientes/INTEIA_Box_com_carro.blend`: ambiente e carro estático em coleções separadas; 568 malhas do box e 97 do carro. Inclui câmera, luzes adicionais para Cycles e imagens empacotadas.
- `ambientes/Previa-Box.png`: render de conferência do arquivo Blender, 16 amostras com denoising. Não é a mesma renderização do navegador.
- `ambientes/validacao-box.json`: contagem de malhas e verificação de imagens empacotadas.
- `web/src/garage.js`: construção procedural reutilizável do cenário.
- `ferramentas/package_garage.py` e `render_garage_preview.py`: reprodução do arquivo Blender e da prévia. Recebem a pasta do projeto após `--`.

O GLB não contém o ambiente de reflexão pré-calculado do navegador; outros motores devem configurar sua própria iluminação. As telas do GLB/Blender são imagens estáticas da exportação. A atualização dos valores acontece somente no aplicativo Web. O arquivo Blender desta entrega contém o carro estático; a versão animada anterior continua em `modelos/INTEIA_F1_animado.glb`.

## Referências de organização

- [McLaren — engineering room, Azerbaijan 2023](https://www.mclaren.com/racing/formula-1/2023/azerbaijan-grand-prix/the-engineering-room/)
- [McLaren — Japanese Grand Prix practice report, 2024](https://www.mclaren.com/racing/formula-1/2024/japanese-grand-prix/japanese-grand-prix-practice-report/)
- [Mercedes — trackside engineers](https://www.mercedesamgf1.com/news/insight-the-trackside-engineers)

As referências orientaram o papel das estações de engenharia e sua relação com o carro. Dimensões, layout, móveis e equipamentos desta cena são interpretações originais, com simplificações para navegação em tempo real. O resultado continua sendo uma modelagem digital, sem garantia de equivalência fotográfica.

A identidade vetorial INTEIA, com IA em destaque, é compartilhada entre interface e placa do box. Arquivos e regras em `identidade/LEIA-ME.md`; desenho-fonte em `web/src/identity.js`.


## Revisão do box — três passagens visuais

1. Mobiliário e superfícies: apoios de braço, encostos, teclas individuais, mouse, cabos, juntas no piso e granulação discreta na rugosidade.
2. Arquitetura e iluminação: painel técnico recuado, armário alto ventilado, placas laterais, tomadas, bandejas superiores e redução da luz direcional principal.
3. Equipamentos: reforços do suporte de pneus, relevos nas laterais dos pneus, bandeja com soquetes e apoio do macaco.

Verificação: inspeção visual no navegador em cada passagem, troca box/túnel/box, exportação GLB em sessão limpa, testes de montagem e aerodinâmica, abertura e renderização no Blender. Revisão visual feita pelo agente executor, sem juiz independente nesta rodada. O ambiente exportado contém 568 malhas, além das 97 malhas do carro no arquivo Blender; 12 imagens incorporadas, sem imagens externas.

O resultado permanece uma cena ilustrativa 3D. Não representa uma réplica dimensional de um box específico.
