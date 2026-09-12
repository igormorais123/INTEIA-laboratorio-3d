# Arquitetura e mapa dos arquivos

```text
INTEIA_F1_Master.blend        Projeto de edição
modelos/                     GLBs estático e animado
texturas/                    Carbono portátil externo
web/index.html               Aplicação offline gerada
web/assets/                  Base geométrica específica da aplicação
web/src/                     Interface, materiais e controles
web/build.cjs                Empacotamento com esbuild
web/server.cjs               Servidor local
web/test-mechanics.mjs       Teste de ciclos e pivôs
web/test-aerodynamics.mjs    Teste das equações e condições de validade
ferramentas/                 Reconstrução e validação Blender/GLB
docs/                        Guias e orientações
documentacao/                Proveniência e histórico de avaliações
validacao-*.json              Evidências de execução
manifesto-sha256.json         Hashes dos artefatos finais
```

## Fluxo

Base GLB → aplicação Three.js (materiais + controles + personalização) → HTML offline.

Base GLB → script Blender → master + materiais portáteis + animação → GLBs → reimportação de validação.

Os dois caminhos reaproveitam a geometria. Eles não compartilham exatamente o mesmo shader de carbono ou ambiente de iluminação. O .blend foi reconstruído da versão GLB separada; não é o .blend original do tutorial com sua pilha original de modificadores.

O ensaio aerodinâmico é um terceiro módulo: aero-physics.mjs contém as equações puras; wind-tunnel.js gerencia controles, gráficos e traçadores. A malha fornece apenas um comprimento de referência e envelope visual. Não há solver de pressão/velocidade local, malha volumétrica ou calibração automática de coeficientes.


## Fonte da verdade

web/src é a fonte do visualizador. INTEIA_F1_Master.blend é o arquivo de edição reutilizável entregue. package_blender.py reproduz a versão gerada a partir de web/assets; executar novamente não preserva edições manuais posteriores no master. Faça commits dessas edições e decida qual fluxo pretende manter.

documentacao/componentes-origem.json registra IDs, categorias, eixos e limites da separação inicial. validacao-reabertura.json registra os testes da conversão Blender. O histórico das cinco rodadas avalia versões anteriores do visualizador, não novos exports nem alterações futuras.
