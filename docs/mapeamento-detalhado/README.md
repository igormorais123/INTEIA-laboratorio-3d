# Mapeamento detalhado — Laboratório 3D INTEIA

> **Autoria e licença atualizadas em 21/09/2026:** Conforme declaração de autoria de Igor Morais Vasconcelos em 21/09/2026, o vídeo foi usado como referência para as funções das peças; a modelagem disponibilizada é de sua autoria. A carroceria, suas versões GLB, o master Blender e os demais modelos autorais estão incluídos na licença MIT, com permissão de uso, modificação, redistribuição e uso comercial. As descrições anteriores de licença pendente da carroceria, inclusive nos inventários históricos, estão superadas por esta declaração. Os registros técnicos de conversão continuam preservados.

> Licença atualizada em 21/09/2026: as contribuições originais estão sob [MIT](../../LICENSE). Comece pelo [guia atual de download e reutilização](../../REUTILIZACAO.md). Os catálogos e grafos gerados abaixo são fotografias históricas: referências à licença proprietária nesses snapshots foram substituídas pela concessão atual para as contribuições originais.

**Abra o [atlas pesquisável](index.html)** para encontrar arquivos, as 97 peças, funções e relações. Funciona como HTML local, sem CDN, conta ou API. Na página de arquivos do GitHub, baixe o repositório e abra esse HTML localmente; o GitHub exibe o código de HTML, não o executa.

Este levantamento cobre exclusivamente `INTEIA-laboratorio-3d`. A leitura começou em `1ae4fd15062d347dc8462af8f4db33c749e6575b` e foi atualizada até `e3d58af3c59a87b308444e678b0b25803e00e727`, incorporando os commits concorrentes de acabamento e assinatura no carro. A documentação paralela ainda estava em elaboração durante a coleta. **Os hashes e horários do [catálogo](dados/catalogo.json) identificam os bytes analisados; o SHA de HEAD, sozinho, não descreve esse estado local.** A [validação](VALIDACAO.md) separa testes desta tarefa, registros anteriores e lacunas.

## Encontrar e entender

| Preciso de… | Ponto de entrada |
|---|---|
| Buscar um arquivo por finalidade, tipo ou caminho | [Atlas HTML](index.html) · [Catálogo completo](CATALOGO.md) · [CSV](dados/catalogo.csv) |
| Entender cada pasta e o que foi excluído | [Árvore comentada](ARVORE.md) · [Cobertura legível por máquina](dados/cobertura.json) |
| Localizar funções, métodos e linhas | [Índice de funções](FUNCOES.md) · [Símbolos JSON](dados/simbolos.json) |
| Entender controles, materiais, câmeras, montagem e túnel | [Módulos e fluxos](MODULOS-E-FLUXOS.md) |
| Rastrear peças, fontes, conversões e direitos | [Assets e procedência](ASSETS-E-PROCEDENCIA.md) · [97 componentes em JSON](dados/componentes.json) |
| Identificar imagens, SVGs e marca ativa | [Visuais e identidade](VISUAIS-E-IDENTIDADE.md) |
| Reutilizar em um site, jogo ou Blender | [Receitas de reutilização](REUTILIZACAO.md) |
| Visualizar arquitetura, dados e produção de assets | [Guia dos grafos](GRAFOS.md) · [Grafo completo JSON](dados/grafo.json) |
| Atualizar os mapas e conferir alterações | [Processo reproduzível](ATUALIZAR.md) |
| Conferir testes, manifesto e limitações | [Validação e estado](VALIDACAO.md) · [Navegador](NAVEGADOR.md) · [Relatório automático](dados/validacao.json) |

## Escolher a fonte adequada

- **Aplicativo:** [app-v2.js](../../web/src/app-v2.js) é a entrada ativa; [template-v2.html](../../web/src/template-v2.html) define a interface. [web/index.html](../../web/index.html) é uma entrega gerada.
- **Carro operacional:** [carro-movable.glb](../../web/assets/carro-movable.glb) alimenta tanto o site quanto o empacotamento Blender. Os [metadados de componentes](../../documentacao/componentes-origem.json) permitem localizar peças por `partId`, `sourceObject`, categoria, lado e pivô.
- **Distribuição:** [GLB estático](../../modelos/INTEIA_F1_estatico.glb), [GLB animado](../../modelos/INTEIA_F1_animado.glb) e [Blender mestre](../../INTEIA_F1_Master.blend) são derivados reutilizáveis. Não contêm automaticamente personalizações posteriores de uma sessão web.
- **Box:** [garage.js](../../web/src/garage.js) constrói o ambiente no navegador; o [GLB do box](../../ambientes/INTEIA-box-laboratorio.glb) e o [Blender combinado](../../ambientes/INTEIA_Box_com_carro.blend) têm etapas próprias. A exportação não preserva integralmente recursos de renderização.
- **Identidade:** [identity.js](../../web/src/identity.js) alimenta a marca ativa. [branding.js](../../web/src/branding.js) é chamado pela entrada atual e usa os glifos da identidade para uma assinatura na lateral direita do carro. Esse decal é criado na sessão web; não se presume sua presença nos GLBs distribuídos.

## Como interpretar o levantamento

`EXTRACTED` significa referência explícita no arquivo citado. `INFERRED` significa interpretação com evidência indireta. `AMBIGUOUS` marca relação incerta. O grafo curado atual usa relações explícitas; a legenda também define os outros estados para futuras revisões. Ausência de aresta não prova ausência de uso. Chamadas estáticas não garantem execução de todos os ramos e não cobrem reflexão, callbacks anônimos e resolução dinâmica integralmente.

Os conteúdos originais de INTEIA / Igor Morais Vasconcelos estão disponíveis sob licença MIT: qualquer pessoa pode usar, copiar, modificar, redistribuir e utilizar comercialmente, preservando o aviso de copyright e a licença. Não é necessário pedir autorização adicional. Esta concessão inclui código, documentação e geometria original, inclusive seus arquivos exportados. Materiais de terceiros conservam suas próprias licenças; o motor V6 já publicado em CC BY 4.0 mantém essa opção de uso. Conforme declaração de autoria de Igor Morais Vasconcelos em 21/09/2026, o vídeo foi usado como referência para as funções das peças; a modelagem disponibilizada é de sua autoria. A carroceria, suas versões GLB, o master Blender e os demais modelos autorais estão incluídos na licença MIT, com permissão de uso, modificação, redistribuição e uso comercial.

O túnel combina calculadora por coeficientes informados com efeitos visuais aproximados. Não foi localizada CFD validada da malha, rig físico completo, colisores ou LODs. Também não houve homologação contra um carro real. Essas limitações acompanham as receitas de reutilização.

## Entrega independente e concorrência

Esta tarefa escreve somente em `docs/mapeamento-detalhado`. A documentação complementar em [docs/mapas](../mapas/README.md), o gerador paralelo e o `graphify-out` da outra conversa foram preservados. O inventário exclui caches, dependências, Git e checkouts aninhados duplicados; esta própria entrega tem [manifesto separado](dados/entrega.json), evitando um catálogo que se expande recursivamente.

O servidor original na porta **5186** não foi interrompido. Ele serve a pasta `outputs` da conversa original; não se assume que ele esteja servindo `web` deste repositório. Abrir o atlas HTML localmente dispensa iniciar qualquer servidor.
