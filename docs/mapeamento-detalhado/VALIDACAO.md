# Cobertura, verificação e estado analisado

[Índice](README.md) · [Resultado automático](dados/validacao.json) · [Cobertura](dados/cobertura.json) · [Testes desta tarefa](dados/verificacao-app.json)

## Estado da coleta

O levantamento começou em `1ae4fd15062d347dc8462af8f4db33c749e6575b`, branch `main`, com **69 arquivos rastreados** e `graphify-out/` concorrente. Não foram encontrados arquivos `AGENTS.md` aplicáveis nas localizações de instrução verificadas. O remoto confirmado é o repositório público `igormorais123/INTEIA-laboratorio-3d`.

Durante a tarefa foram observadas mudanças concorrentes de acabamento web, luzes/empacotamento Blender, assets do box e documentação. Os commits `0346e58` (acabamento) e `e3d58af` (assinatura lateral) foram incorporados à análise final; o [estado inicial](dados/estado-inicial.json) e o [estado da coleta mais recente](dados/cobertura.json) são distintos. As páginas de módulos e assets registram suas conferências. As referências de linha representam esses fontes locais e devem ser usadas junto dos hashes.

`dados/catalogo.json` é a fonte dos totais finais, arquivos, tamanho, classificação, hash, dependências e uso. A validação exige cobertura dos 69 arquivos iniciais, ausência de arquivos adicionais sem classificação e ausência de importações locais sem destino. A documentação nova e as ferramentas da conversa paralela entram como artefatos complementares. Checkouts aninhados duplicados são excluídos antes da travessia.

## Executado nesta tarefa

- Conferência real de tamanhos e SHA-256 das entregas listadas em `manifesto-sha256.json`. O resultado por arquivo está em [manifesto-conferencia.json](dados/manifesto-conferencia.json); ele registra o estado local, sem regravar o manifesto da aplicação.
- Leitura da estrutura dos quatro GLBs: cabeçalho glTF 2, nós, meshes, primitivas, triângulos, materiais, imagens, URIs externas e animações. A contagem inclui primitivas indexadas e não indexadas. O box possui ambos os tipos.
- Confronto dos 97 registros de `componentes-origem.json` com `name` e extras da base web; verificação de unicidade de `partId`. Resultados em [componentes.json](dados/componentes.json).
- Inspeção visual das quatro imagens soltas e leitura de SVGs/HTML da identidade. A captura com extensão `.png` que contém JPEG foi preservada e registrada no catálogo.
- Extração estrutural graphify com diagnóstico de incompletude explícito, complementada por símbolos tree-sitter/Python AST e relações curadas.
- Build web executado em memória. Os bytes produzidos conferiram com o HTML local testado. Nenhuma escrita em `web/index.html` foi feita pelo adaptador.
- Teste mecânico: 97 peças, quatro pivôs de rodas, uma cobertura interna por roda, DRS, 20 ciclos de montagem, isolamento/restauração e arraste. Erros de matriz inicial/final/reset/arraste medidos como zero nessa execução. Saída em [teste-mecanica.json](dados/teste-mecanica.json).
- Teste aerodinâmico: unidades, vento relativo, densidade, escala V²/V³, condições inválidas e ausência de coeficientes. Resultado em [verificacao-app.json](dados/verificacao-app.json).
- Verificação de links locais, âncoras Markdown, JSON, IDs e extremidades das relações, linhas de fonte, hashes do catálogo e dos arquivos testados. O resultado com data e eventuais avisos é [validacao.json](dados/validacao.json).

Os avisos de Node sobre inferência de módulo ES refletem o `package.json` atual e não impediram os testes; a configuração do aplicativo foi preservada.

A busca, os filtros, os detalhes, o grafo, voltar/avançar, foco de teclado e layouts móvel/desktop foram verificados no Chrome. Medidas e resultados estão em [NAVEGADOR.md](NAVEGADOR.md).

## Manifesto e alterações concorrentes

Na leitura inicial os 14 itens do manifesto conferiam. Depois das alterações concorrentes de acabamento, a conferência passou a **11 de 14**, com divergência no HTML web, GLB do box e Blender combinado. Com a atualização posterior da prévia, a conferência chegou a **10 de 14**, acrescentando `ambientes/Previa-Box.png` às divergências. Isso indica que esses bytes mudaram em relação ao manifesto, não prova corrupção. O relatório automático registra a situação mais recente; se outra tarefa atualizar o manifesto, a nova coleta deverá refletir a conferência atual.

Na revisão final `e3d58af`, a outra tarefa havia atualizado o manifesto e a conferência retornou a **14 de 14**. As divergências acima são a sequência histórica observada durante o trabalho, não pendências da entrega final. Esta tarefa não executou `ferramentas/manifest.cjs`. Atualizar o manifesto de entregas deve acompanhar a tarefa que está finalizando os assets, após a validação desses assets. Esta documentação tem um manifesto próprio independente.

## Limites de cobertura

| Área | O que esta tarefa comprova | O que permanece fora da comprovação |
|---|---|---|
| Arquivos | Presença, finalidade revisada, hashes, ligações e tipagem | Históricos de autoria não documentados ou versões ausentes |
| Código | Declarações, importações e relações explícitas | Todos os caminhos dinâmicos, callbacks anônimos e execução completa da UI do aplicativo |
| Mecânica | Asserções automatizadas da implementação em Node | Suspensão/colisão realista, calibração de rig ou homologação dimensional |
| Aerodinâmica | Consistência das fórmulas por coeficientes | CFD da malha, calibração em túnel físico, coeficientes reais do carro |
| GLB | Estrutura binária/JSON e metadados presentes | Aparência idêntica em todos os motores, colisores/LODs inexistentes |
| Blender | Fontes de produção e evidências históricas lidas | Nova reabertura, novo render ou exame de todos os datablocks Blender nesta tarefa |
| Direitos | Cláusulas e declarações locais identificadas | Uma licença original ausente não foi reconstruída nem presumida |
| Navegador | Funcionamento do atlas na validação registrada separadamente | Nova certificação visual ou desempenho do laboratório 3D |

Os JSONs `validacao-criacao.json`, `validacao-reabertura.json` e `ambientes/validacao-box.json` são **registros anteriores**, não testes reexecutados neste mapeamento. A imagem de prévia pode refletir uma configuração anterior àquela que o script atual produziria.

## Exclusões justificadas

O [relatório de cobertura](dados/cobertura.json) lista as exclusões efetivamente observadas. Dependências npm têm versões e integridade registradas pelo lockfile; caches e objetos Git não são assets autorais do laboratório. Backups, logs e arquivos de ambiente são locais. Junções e links não são seguidos. O checkout aninhado usado pela outra conversa duplica o projeto e não amplia sua arquitetura.

Esta documentação é inventariada em [entrega.json](dados/entrega.json), que exclui o próprio manifesto para evitar dependência circular de hashes. O gerador e o validador escrevem somente na pasta desta tarefa. A porta 5186 permaneceu preservada; o build/teste isolado não precisa de servidor.
