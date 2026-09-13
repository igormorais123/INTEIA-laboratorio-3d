# Mapa do Laboratório 3D INTEIA

[Voltar ao projeto](../../README.md) · [Abrir atlas pesquisável](index.html)

Este é o ponto de entrada para encontrar o código, documentos e assets e decidir o que levar para outro projeto. A revisão inicial estudada foi `1ae4fd15062d347dc8462af8f4db33c749e6575b`; o atlas determinístico foi atualizado sobre `0346e58`, com a revisão de materiais e iluminação. O graphify mantém o snapshot inicial, identificado separadamente. O inventário inclui também a documentação e as ferramentas adicionadas pelo mapeamento; seu fingerprint identifica o conteúdo analisado.

| Preciso… | Caminho |
| --- | --- |
| Encontrar qualquer arquivo ou função | [Busca interativa](index.html) · [Inventário completo em Markdown](INVENTARIO.md) |
| Entender responsabilidades e controles | [Mapa dos módulos](MODULOS.md) · [IDs do template e referências](controles.json) |
| Seguir imports e produção dos assets | [Grafos com evidências](GRAFOS.md) · [Relações em JSON](dependencias.json) |
| Encontrar uma peça pelo nome ou ID | Aba Componentes do [atlas](index.html) · [Catálogo verificável](componentes.json) |
| Reaproveitar em site, jogo ou Blender | [Guia prático](REUSO.md) |
| Reconstruir uma entrega e entender seus limites | [Processo de produção](PRODUCAO.md) |
| Explorar relações dos documentos e imagens | [Grafo graphify](../../graphify-out/graph.html) · [Relatório de extração](../../graphify-out/GRAPH_REPORT.md) |
| Atualizar ou conferir os mapas | [Manutenção e validação](MANUTENCAO.md) · [Cobertura computada](cobertura.json) |
| Conferir o que foi realmente testado | [Evidências de verificação](VERIFICACAO.md) |
| Conferir direitos e o original de terceiros | [Direitos e procedência](../DIREITOS-E-PROCEDENCIA.md) · [Licença](../../LICENSE) |

O atlas funciona offline após baixar o repositório: abra `docs/mapas/index.html`. Seus dados, estilos e grafos estão incorporados, sem CDN. No GitHub, o HTML é exibido como código; os documentos Markdown e diagramas Mermaid podem ser lidos diretamente.

O inventário cobre todos os arquivos versionados e novos não ignorados, excluindo caches do graphify, dependências instaladas e backups ignorados. Modelos GLB têm seus cabeçalhos e metadados lidos diretamente. Arquivos Blender são identificados por hash e documentação; este mapeamento não os reabriu no Blender.

Há dois níveis de grafo: os mapas determinísticos usam apenas relações explícitas com evidência; o graphify acrescenta extração estrutural e leitura semântica de documentos e imagens. Relações `INFERRED` no graphify são hipóteses identificadas, e as comunidades são agrupamentos algorítmicos, não módulos declarados pelo autor.

Nenhuma trajetória de fumaça, tela decorativa ou prévia constitui CFD, telemetria real ou validação física. Os testes numéricos cobrem o modelo por coeficientes e os movimentos programados dentro do escopo descrito em [Validação](../VALIDACAO.md).
