# Sistemas internos em 3D — bancada Sistemas

A bancada **06 Sistemas** mostra catorze conjuntos internos do carro modelados como malhas reais, em escala do carro v2, com materiais físicos (carbono com verniz, alumínio usinado, titânio, Inconel com pátina térmica, Kevlar, silicone, cobre) e peças nomeadas. Substitui a camada anterior de primitivas procedurais em três.js. É uma representação didática original INTEIA; não é CAD de fabricante, engenharia ou homologação.

## Arquivos

| Arquivo | Função |
| --- | --- |
| `ferramentas/gerar_sistemas.py` | Gerador executado pelo Blender 5.2 em modo background. Monta a cena, chama os módulos, exporta o GLB, chama o otimizador e grava o manifesto. |
| `ferramentas/sistemas/lib.py` | Biblioteca: conversão de referencial, primitivas (`cube`, `cyl`, `lathe`, `sweep`, `loft`, `gear`, `helix`, `bolt_ring`), materiais e texturas geradas por numpy (sarja 2x2, Kevlar, escovado, fundido, pátina térmica, furação dos discos, aletas, colmeia). |
| `ferramentas/sistemas/sNN_<id>.py` | Um módulo por sistema, na ordem dos capítulos do vídeo de referência. Cada módulo expõe `SYSTEM = (id, rótulo)`, `build(ctx)` e, opcionalmente, `SHOTS` para renders de conferência. |
| `ferramentas/otimizar_sistemas.mjs` | Empacotamento `EXT_meshopt_compression` sem perda, com deduplicação de malhas idênticas, via `@gltf-transform` e `meshoptimizer`. |
| `web/assets/sistemas-v1.glb` | Asset publicado (cerca de 6,3 MB comprimidos; 12,7 MB brutos). |
| `web/assets/sistemas-v1.manifest.json` | Medição do GLB publicado: peças por sistema com nome, bounds no referencial do site, extras, triângulos, materiais, hash SHA-256. |
| `web/src/systems.js` | Carrega o GLB sob demanda, distribui os nós `system_<id>` nos grupos, anima rotores, engrenagens e fluxos, e controla a interface. |
| `web/test-systems.mjs` | Contratos do catálogo, do GLB, do manifesto e da arquitetura didática (monoturbo dividido, refrigeração assimétrica, empacotamento célula → motor → câmbio, relações do câmbio, cabos de retenção etc.). |

## Referencial e escala

Todo o código dos módulos usa o referencial do site: X para a direita, Y para cima, Z para a frente, metros, piso em y = 0. A biblioteca converte para o Blender e o exportador glTF devolve o referencial do site. Medidas do carro v2 usadas como âncoras: rodas dianteiras em (±0,735; 0,329; 1,521), traseiras em (±0,735; 0,342; −1,838), sidepods até x = ±0,706, cockpit entre z = −0,13 e 0,91, santo antônio em y ≈ 1,13.

**Lados.** O piloto olha para +Z, portanto a esquerda real do carro é +X (o freio, de pé esquerdo, fica em x > 0; o acelerador em x < 0; o intercooler, no sidepod esquerdo, em x > 0). Os módulos novos declaram `X_CONVENTION = 'piloto'` e usam `lib.lado(side)` para os rótulos; os módulos escritos antes dessa correção rotulavam −X como esquerda e são espelhados no lugar pelo gerador (`lib.mirror_system`), de modo que o asset publicado segue uma única convenção. O teste percorre todas as peças e falha se um rótulo "esquerdo"/"direito" estiver do lado errado.

**Peças visíveis copiadas do carro.** `lib.car_part` importa o carro v2 uma vez, separa as ilhas da malha `main_body__01` e copia as que caem em uma caixa dada: é assim que o Halo (arco e pilar) e o encosto de cabeça da camada Segurança coincidem exatamente com o que se vê por fora, com material de titânio e Nomex e fixações modeladas por cima. O volante é centrado no cubo do volante do carro (0; 0,5925; 0,518), com a face dos comandos para −Z, e o cone de impacto dianteiro, o assento e a luz de chuva foram ajustados às fatias medidas da carroceria (nariz, cavidade do cockpit em x = ±0,154 e LED traseiro).

Na camada Sistemas o V6 fica centrado em z = −0,92, com a célula de combustível entre o assento e o bloco e o câmbio até a estrutura traseira. O compartimento do motor da bancada **Motor** mantém o V6 detalhado com pistões em z = −0,72, ajustado à tampa recortada; quando os sistemas são revelados ao desmontar o carro, o motor do compartimento é ocultado para não duplicar a unidade.

## Extras exportados nos nós

| Extra | Uso no site |
| --- | --- |
| `part` | Nome da peça, mostrado ao clicar. |
| `system` | Sistema de origem. |
| `spin`, `spin_axis` | Rotação contínua em rad/s no eixo local (rodas, discos, turbo, engrenagens nas relações de cada par). |
| `flow` | Fita de fluxo (ar, ar comprimido, escape, água, óleo, combustível, energia, hidráulica, dados, freio) animada por deslocamento de textura. `tag: reverse` inverte o sentido. |
| `carrier` | Tubo, mangueira, cabo ou eixo que conduz um fluxo; fica translúcido com os fluxos ligados. |
| `era` | `2021` marca MGU-H e cabos que somem no contexto 2026. |
| `hide_group` | Tampas e carcaças ocultáveis: `plenum_lid`, `es_lid`, `gearbox_case`, `fuel_liquid`. |
| `explode` | Vetor de separação usado pelo controle **Separar peças do sistema**. |

## Interface

Ao clicar em uma peça, o painel mostra o nome, o sistema, o que a peça faz e uma curiosidade técnica, a partir de `web/src/parts-info.js` (regras por família de peça, com texto genérico por sistema quando nenhuma regra casa). O volante segue o leiaute do protótipo Ferrari 2026 (referências fotográficas públicas), com botões de override manual (OT) e aerodinâmica ativa (AA) no lugar do DRS; as legendas são gravadas na placa e cada botão tem descrição própria.

**Vista explodida.** Na bancada Sistemas o controle **Vista explodida (peças e sistemas)** afasta as peças do sistema isolado ou, na visão geral, também desloca cada um dos catorze conjuntos na direção `spread` do catálogo. Na bancada Carro, abaixo da **Vista explodida** do carro, o controle **Vista explodida dos sistemas** faz o mesmo com os sistemas revelados ao desmontar (se o carro estiver montado, ele é desmontado automaticamente); **Montar** e o reinício zeram o controle.

Além dos cartões e das seis vistas: **Fluxos animados**, **Abrir tampas**, **Cores por sistema** (modo esquemático com a cor do catálogo), **Carro fantasma** (desligue para ver os sistemas dentro do carro sólido e use **Desmontar**), **Separar peças do sistema** e leitura do nome da peça por clique. Na bancada Carro, **Desmontar** revela automaticamente os catorze sistemas no lugar enquanto a carroceria se afasta.

## Regenerar

```powershell
# asset completo, otimizado, com manifesto (Blender 5.2 LTS instalado)
$env:F1_ASSET_TOOL_ROOT = "$env:TEMP\claude\f1-assets"   # projeto com @gltf-transform e meshoptimizer
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python ferramentas/gerar_sistemas.py

# um ou mais sistemas com renders de conferência (saída em ferramentas/sistemas/previews, fora do Git)
$env:SISTEMAS = "brakes,suspension"; $env:PREVIEW = "1"
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b --python ferramentas/gerar_sistemas.py

npm --prefix web test
npm --prefix web run build
```

Sem `F1_ASSET_TOOL_ROOT` o GLB sai sem compressão e o manifesto registra `optimized: false`; o teste exige o asset otimizado antes da publicação.

## Publicação

O ambiente de produção é o ChatGPT Sites, em https://laboratorio-3d-inteia.igor47306.chatgpt.site (ver [PUBLICACAO.md](PUBLICACAO.md)). Depois de regenerar o asset e reconstruir o site, o GLB `sistemas-v1.glb` é um dos sete arquivos que o sincronizador copia para o checkout de deploy; o manifesto e os geradores ficam só no repositório-fonte. Mesclar em `main` não publica nada por si só.

## Limites

Geometria ilustrativa: dimensões, materiais e quantidades são hipóteses de modelagem coerentes com o vídeo de referência e com o regulamento vigente na época, não medições de um carro real. Não há cinemática, simulação térmica, elétrica ou hidráulica. Os renders EEVEE de conferência não reproduzem a iluminação do estúdio três.js; a validação visual final é feita no navegador.
