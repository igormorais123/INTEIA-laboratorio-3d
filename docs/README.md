# Documentação do Laboratório 3D INTEIA

Este é o índice canônico da documentação. Use o guia mais estreito para a tarefa e trate os atlas como derivados reproduzíveis, não como fontes editáveis do aplicativo.

## Operação e desenvolvimento

| Necessidade | Fonte |
| --- | --- |
| Arquitetura e fontes de verdade | [ARQUITETURA.md](ARQUITETURA.md) |
| Instalar, executar, testar e gerar entregas | [DESENVOLVIMENTO.md](DESENVOLVIMENTO.md) |
| Publicar site e atlas | [PUBLICACAO.md](PUBLICACAO.md) |
| Continuar em outro computador | [OUTRO-PC.md](OUTRO-PC.md) |
| Integrar em site, jogo ou Blender | [INTEGRACAO.md](INTEGRACAO.md) e [BLENDER.md](BLENDER.md) |
| Limites e evidências de validação | [VALIDACAO.md](VALIDACAO.md) |
| Direitos e procedência | [DIREITOS-E-PROCEDENCIA.md](DIREITOS-E-PROCEDENCIA.md) |

## Produto e conteúdo técnico

| Área | Fonte |
| --- | --- |
| Motor V6 no laboratório | [INTEGRACAO-MOTOR.md](INTEGRACAO-MOTOR.md) |
| Sistemas internos do carro | [SISTEMAS-3D.md](SISTEMAS-3D.md) e [especificação histórica](ESPECIFICACAO-ASSET-3D-SISTEMAS-F1.md) |
| Base de pesquisa dos sistemas | [pesquisa-sistemas-carro-video.md](pesquisa-sistemas-carro-video.md) |
| Aerodinâmica didática | [AERODINAMICA.md](AERODINAMICA.md) |
| Box-laboratório | [BOX-LABORATORIO.md](BOX-LABORATORIO.md) |
| Piloto e capacete | [PILOTO-E-CAPACETE.md](PILOTO-E-CAPACETE.md) |
| Acabamento e render | [ACABAMENTO-E-RENDER.md](ACABAMENTO-E-RENDER.md) |

## Mapas do repositório

Os dois atlas têm finalidades diferentes e são mantidos por geradores próprios:

- [Atlas operacional](mapas/README.md): inventário atual, imports, controles, componentes e produção. Gere com `python ferramentas/mapear.py`.
- [Dossiê detalhado](mapeamento-detalhado/README.md): catálogo auditável, funções, relações curadas, hashes e procedência. Gere com `python docs/mapeamento-detalhado/scripts/gerar.py`.
- [Graphify](../graphify-out/graph.html): navegação estrutural e semântica para agentes. Relações inferidas precisam de confirmação na fonte.
- [Archify](../.planning/architecture/system-architecture.html): visão arquitetural de alto nível.

Depois de mudar código ou documentação, siga [a manutenção dos mapas](mapas/MANUTENCAO.md). Não edite manualmente os catálogos, JSON e HTML marcados como gerados.

## Fontes de verdade

- `web/src/`: aplicativo web editável.
- `web/assets/`: assets carregados pelo aplicativo.
- `ferramentas/`: produção e validação de derivados.
- `INTEIA_F1_Master.blend`: master Blender distribuído.
- `documentacao/componentes-origem.json`: procedência e metadados do carro-base.

`web/index.html`, os atlas HTML/JSON e os arquivos em `graphify-out/` são saídas geradas. Preserve evidências históricas em `documentacao/`; não as use como descrição automática do estado atual.
