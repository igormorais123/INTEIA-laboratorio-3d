# Validação e limites observados

## Artefatos entregues

- Blender reaberto: 97 componentes, sem imagens externas ausentes.
- Todos os 97 componentes se deslocam no quadro 90.
- Retorno no quadro 210: erro máximo de matriz registrado = 0.
- Ambos os GLBs reimportados com 97 meshes.
- GLB animado: um clipe, 104 canais.
- Malha convertida: 752.823 triângulos. Base web: 752.824. A diferença de um triângulo na conversão foi registrada; não se afirma identidade topológica exata.
- Site aberto a partir do pacote reutilizável sem erro de console observado.
- Controles de cores/acabamento/restauração e montagem verificados em navegador; layout estreito sem overflow horizontal observado.

Consulte os JSONs de validação na raiz. As verificações representam as execuções registradas, não garantia de qualquer edição posterior.

## Histórico visual

Cinco candidatas foram avaliadas pelo juiz independente Codex: aceitas 1, 4 e 5; rejeitadas 2 e 3. Os pareceres estão em documentacao/historico-avaliacoes.md. As notas são subjetivas. Pneus lisos/escuros, reflexos sintéticos e carbono procedural permanecem limitações.

## Testes que faltam por destino

Não foram feitos testes em motores de jogos, testes de colisão, validação física de suspensão ou homologação contra um carro real. FPS foi observado pontualmente no computador de origem; não é promessa de desempenho. A versão detalhada exige otimização conforme o destino.

Para repetir os testes automatizados, veja Desenvolvimento. Para avaliar alterações de materiais, compare o mesmo enquadramento, iluminação e resolução antes/depois.

## Ensaio aerodinâmico por coeficientes

Testes automatizados verificam conversão km/h → m/s, densidade, V² nas forças, V³ na potência, cancelamento por vento de cauda, composição lateral, parâmetros inválidos e limite de Mach. No navegador foram conferidos resultados ausentes sem coeficientes, exemplo sinalizado, aumento de forças, bloqueio com peças desmontadas e faixa de validade. Isso valida a calculadora, não a aerodinâmica deste carro. Consulte AERODINAMICA.md.
