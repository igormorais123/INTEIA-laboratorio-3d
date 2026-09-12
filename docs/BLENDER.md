# Guia Blender

Abra INTEIA_F1_Master.blend com Blender 4.5. O arquivo foi produzido e reaberto no Blender 4.5.9 LTS. As texturas usadas estão incorporadas; não precisa localizar pastas no computador do autor.

## Reutilizar a coleção

No seu projeto, use File > Append, escolha o .blend e entre em Collection. Importe **INTEIA | Carro reutilizavel**. O estúdio pertence a **INTEIA | Estudio (nao exportar para jogos)**. Importe essa segunda coleção apenas se quiser piso, câmera e luzes.

A coleção do carro e os materiais estão marcados como assets. Opcionalmente adicione a pasta deste repositório às bibliotecas de assets nas preferências do Blender. Append é o caminho mais direto para obter uma cópia editável.

## Objetos, pivôs e materiais

INTEIA_F1 é a raiz. Os objetos preservam nomes e propriedades de origem como sourceObject, category e assemblyComponent. Rodas têm grupos de direção e giro; a asa móvel tem Abertura_DRS. Mova a raiz para reposicionar o carro inteiro. Unidades em metros, eixo Z para cima.

Os materiais com nome Pintura são a carroceria e elementos pintados. Edite Base Color no Principled BSDF. Metallic, Roughness e Coat controlam a resposta superficial. Carbono usa textura própria; Pneus/Borracha, Rodas, Aço e outros materiais são independentes. A iluminação está na coleção de estúdio.

## Timeline — 30 fps

| Quadros | Ação |
| --- | --- |
| 1 | Carro montado |
| 90–120 | Vista explodida |
| 120–210 | Remontagem |
| 210–300 | Rodas, direção e DRS |

Pressione Espaço na timeline. Para editar posições sem a animação as sobrescrever, desvincule as ações dos objetos envolvidos. Mantenha uma cópia do master. O GLB estático fornece a alternativa sem animações.

## Exportação

Selecione apenas os objetos da coleção do carro, incluindo empties/pivôs, e exporte glTF/GLB com Selected Objects e materiais. Ative animações apenas se necessário. Piso, câmera e luzes não fazem parte dos GLBs entregues.

Para reconstruir os artefatos pelos scripts, veja Desenvolvimento. A aparência de Cycles/AgX não é idêntica ao estúdio Three.js/ACES. A textura portátil de carbono também difere da projeção do shader web.
