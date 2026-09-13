# Validação do atlas no navegador

[Índice](README.md) · [Validação geral](VALIDACAO.md)

Teste interativo realizado no Chrome via controle de navegador, em 12/09/2026, entre 22:27 e 22:38 (UTC−03), na página desta documentação servida por HTTP local na porta 5197. O servidor da aplicação na porta 5186 foi preservado. A primeira tentativa de abrir o navegador interno do Codex excedeu o tempo disponível; a navegação e a verificação visual foram concluídas no Chrome.

| Ação | Resultado observado |
|---|---|
| Abrir o atlas | Índice, contadores, guias, busca, quatro modos e painel de detalhes carregaram. |
| Buscar `branding` | Arquivo localizado, com caminho, finalidade, hash e relações. A finalidade foi posteriormente atualizada ao commit que ativou o módulo. |
| Buscar `DRS` na aba de peças | Cinco registros encontrados; `rear_wing_drs__01` mostrou objeto `rear_wing_drs`, categoria, 3.776 triângulos, pivô e limites. |
| Buscar `aerodynamicTest` em funções | Função localizada em `web/src/aero-physics.mjs:2`, assinatura, escopo e relações exibidos. |
| Filtrar natureza `modelo gerado` | Três modelos listados: box, carro estático e carro animado. |
| Busca sem correspondência | Estado vazio e orientação para mudar palavra/filtro exibidos. |
| Limpar busca com teclado | Ctrl+A e Backspace restabeleceram a lista completa. |
| Explorar grafo de `garage.js` | Dependências e vizinhos exibidos, incluindo `identity.js`, Three.js e luzes retangulares. |
| Abrir nó `identity.js`, voltar e avançar | Painel restaurou `garage.js` ao voltar e `identity.js` ao avançar. Estado de navegação preservado na URL. |
| Tab a partir da busca | Foco chegou ao controle `Arquivos`, com contorno visível; filtro fica desabilitado fora da aba de arquivos. |
| Tela móvel, override 390 × 844 | Após correção, largura de conteúdo 375 px e largura total 375 px, sem excesso horizontal. A diferença para 390 corresponde à área reservada à barra de rolagem. Painel de detalhes limitado a 55vh com rolagem própria. Busca de peças continuou funcional. |
| Tela desktop, override 1440 × 1000 | Largura de conteúdo/rolagem 1425 px; duas colunas de 932,8 e 420 px, sem excesso horizontal. |
| Console | Nenhum erro registrado com URL da página do atlas. Havia erros de uma extensão instalada no Chrome; foram separados por origem e não atribuídos à aplicação. |

O teste móvel revelou um pequeno excesso horizontal em textos de evidências e um painel de detalhes longo demais. A interface foi corrigida com quebra de texto e altura limitada no breakpoint móvel; a medição foi repetida com sucesso. A janela recebeu novamente seu tamanho normal ao fim da validação.

Esta é uma revisão do **atlas de documentação**, não uma nova revisão gráfica do laboratório 3D. A funcionalidade do aplicativo foi verificada pelos testes isolados descritos na validação geral. O HTML do atlas não depende de JavaScript, fontes ou grafos carregados de CDN: os dados e a lógica estão incorporados. A sessão de teste registrada usou HTTP local, não uma emulação de falha de rede.
