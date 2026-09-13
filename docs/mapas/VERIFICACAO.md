# Evidências de verificação do atlas

[Índice](README.md) · [Cobertura atual dos arquivos](cobertura.json) · [Procedimento de atualização](MANUTENCAO.md)

Verificação realizada em 13 de setembro de 2026 UTC (12 de setembro à noite em Brasília), na worktree da branch `codex/mapas-inteia`, inicialmente baseada em `1ae4fd15062d347dc8462af8f4db33c749e6575b` e atualizada sobre `e3d58af` (incluindo materiais/luzes de `0346e58` e a assinatura lateral). A revisão de materiais/luzes foi incorporada pelo commit da tarefa responsável, sem editar seus arquivos. Build, testes e mapas foram conferidos novamente. O trabalho concorrente em `docs/mapeamento-detalhado/` permanece separado e exige atualização dos mapas ao ser integrado.

| Verificação | Resultado observado | Limite |
| --- | --- | --- |
| Build `npm --prefix web run build` | Passou; HTML final sem alteração em relação à base estudada | Não reabre Blender nem certifica renderização física |
| `npm --prefix web test` | Passou: 97 peças, quatro pivôs de rodas e DRS; 20 ciclos; erros de matriz inicial/final/reset/arraste iguais a zero | Testes locais existentes, sem teste em Unity/Unreal/Godot |
| Aerodinâmica | Testes de unidades, V²/V³, vento relativo, densidade, faixa e ausência de coeficientes passaram | Modelo por coeficientes; não CFD |
| GLBs | Cabeçalhos válidos; base web e dois exports com 97 meshes; box com 568 meshes; export animado com um clipe e 104 canais | Leitura de dados incorporados; sem reimportação Blender nesta tarefa |
| Procedência | 97 `partId` distintos correspondem entre documento de origem e GLB base | Igualdade dos IDs não certifica origem jurídica ou exatidão geométrica |
| Mapas | `mapear.py --check` passou; relatório atual em cobertura.json | Cobertura de arquivos/imports/links, não de todo comportamento dinâmico |
| Navegador | Chrome headless por Playwright, 1440×1000 e 390×844; zero erros de página | HTML real servido por interceptação HTTP local no navegador, sem abrir servidor ou usar o processo da porta 5186 |
| Interações do atlas | Pesquisa sem acentos, vazio, símbolos, busca por partId, controles, filtros, três grafos, Enter e histórico voltar/avançar passaram | Uma execução de QA; não certificação WCAG completa |
| Layout | Capturas desktop/mobile inspecionadas; sem rolagem horizontal global em 390 px | Tabelas e grafos mantêm rolagem horizontal própria |
| Links | Destinos e linhas dos links Markdown locais conferidos; navegação para o guia também exercitada no browser | URLs externas não foram requisitadas pelo verificador |
| Graphify | 319 nós, 361 relações brutas/360 no grafo simples; sem endpoints ausentes ou autorrelações | Uma relação paralela resumida no grafo simples; ambas preservadas em graphify-extracao.json |

O Node avisou que o tipo de módulo de `mechanics.js` não está declarado no package.json e refez a interpretação como ES module; os testes passaram. Não houve mudança do pacote por esse aviso.

A tentativa de iniciar servidor de prévia foi rejeitada pela revisão automática de aprovação sem motivo específico. A ferramenta inicial de navegador não respondeu, e a CLI bloqueou navegação `file:`. A alternativa validada foi renderizar os arquivos autorizados em Chrome com requisições interceptadas para um domínio reservado `.test`, sem servidor de rede e sem navegar pelo protocolo de arquivos. As capturas e o relatório local da sessão estão em `output/playwright/` na worktree, excluídos do commit.

A primeira execução remota da branch no GitHub Actions foi encerrada antes de iniciar qualquer etapa: a anotação informa bloqueio da conta por cobrança. Portanto, os resultados de testes desta entrega são locais; não são uma aprovação da CI remota.
