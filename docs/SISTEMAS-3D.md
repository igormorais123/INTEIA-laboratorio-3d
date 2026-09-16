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

## Limites

Geometria ilustrativa: dimensões, materiais e quantidades são hipóteses de modelagem coerentes com o vídeo de referência e com o regulamento vigente na época, não medições de um carro real. Não há cinemática, simulação térmica, elétrica ou hidráulica. Os renders EEVEE de conferência não reproduzem a iluminação do estúdio três.js; a validação visual final é feita no navegador.
