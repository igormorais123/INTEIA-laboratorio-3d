# Estúdio de som: V6 2026 e V12 anos 90 — desenho

**Data:** 16/09/2026 · **Branch:** `estudio-som-v12` · **Status:** aguardando revisão

## Objetivo

Uma nova aba **07 Som** no Box INTEIA onde o visitante liga, acelera e compara o som de dois motores de F1 — o V6 1,6 turbo híbrido de 2026 e um V12 3,5 aspirado dos anos 90 —, vê o motor 3D peça a peça sincronizado com a ignição e confere a afinação: RPM → frequência → nota.

O som precisa ser convincente. Síntese ingênua (osciladores, ruído filtrado) está vetada.

## Decisões tomadas

| Tema | Decisão | Motivo |
|---|---|---|
| V12 de referência | F1 anos 90: 3,5 L aspirado, 65°, até 17.000 RPM | Coerente com o carro de F1 e com o grito agudo |
| Onde fica | Nova aba **07 Som**; a aba Motor continua como está | Espaço próprio para controles, afinador e motor 3D |
| Fonte do som | **Síntese calibrada no real**: banco de loops gerado offline por modelo físico de alta resolução e calibrado pelo espectro de gravações reais livres | Não há gravação livre de V12 F1 anos 90 nem de V6 híbrido utilizável; sem risco legal e sem compra |
| Reprodução | Arquitetura dos jogos de corrida: loops de ciclos inteiros por RPM, lidos com fase travada ao virabrequim | Afinação exata e crossfade sem phasing |
| Modelagem 3D | Gerador Blender no padrão de `ferramentas/sistemas` | Peças nomeadas, materiais físicos, regenerável |

## Afinação

Motor de 4 tempos com ignição uniforme: cada cilindro explode uma vez a cada 2 voltas.

```
f0 (Hz) = (RPM / 60) × (cilindros / 2)
nota    = 69 + 12 × log2(f0 / 440)   (MIDI; cents = resto × 100)
```

| Motor | RPM | f0 | Nota |
|---|---|---|---|
| V4 | 6.000 | 200 Hz | Sol 3 (+35 cents) |
| V12 | 6.000 | 600 Hz | Ré 5 (+37 cents) |
| V12 | 7.000 | 700 Hz | Fá 5 (+4 cents) |
| V6 | 15.000 | 750 Hz | Fá# 5 (+23 cents) |
| V12 | 17.000 | 1.700 Hz | Sol# 6 (+40 cents) |

Estes valores viram casos de teste.

## Perfis dos motores (dados)

| | V12 anos 90 | V6 2026 |
|---|---|---|
| Cilindros / ângulo | 12 / 65° | 6 / 90° |
| Ordem de ignição | 1-7-5-11-3-9-6-12-2-8-4-10 | 1-4-2-5-3-6 |
| Intervalo | 60° de virabrequim | 120° |
| Marcha lenta → limite | 4.000 → 17.000 RPM | 4.000 → 15.000 RPM |
| Admissão | 12 trompetas, airbox | plenum com 6 trompetas, após compressor |
| Escape | 6-em-1 por bancada, 2 saídas | coletores → turbina → saída única |
| Camadas extras | cascata de engrenagens, válvulas | turbo, wastegate, MGU-K |

## Arquitetura

```
ferramentas/som/
  referencias.json        URLs, licenças, autores e SHA-256 das gravações de referência
  baixar-referencias.mjs  baixa as referências para ferramentas/som/.referencias/ (fora do Git)
  analisar-referencias.mjs  order tracking → envelope harmônico por faixa de RPM → alvos-timbre.json
  modelo-fisico.mjs       modelo de alta resolução (offline)
  gerar-banco.mjs         calibra o modelo pelos alvos e grava o banco de loops
  alvos-timbre.json       números extraídos das referências (versionado; não contém áudio)

web/src/sound/
  tuning.mjs              RPM → Hz → nota/cents (puro)
  engine-profiles.mjs     perfis V6 e V12 (dados)
  phase-player.mjs        núcleo de leitura com fase travada, camadas e limitador (puro, roda no Node)
  engine-worklet.js       AudioWorklet que envolve phase-player.mjs (embutido como Blob no build)
  sound-studio.js         aba 07: interface, grafo de áudio, afinador, sincronia com o 3D

web/assets/
  som-v12-v1.bin + .json  banco de loops (PCM Int16 mono 48 kHz) + manifesto
  som-v6-v1.bin  + .json
  v12-v1.glb + v12-v1.manifest.json

ferramentas/v12/gerar_v12.py  gerador Blender do V12
```

Os bancos e o GLB são carregados sob demanda ao abrir a aba, como os demais assets de `web/assets`; não entram no `index.html`.

### 1. Referências reais (só para análise)

Gravações confirmadas pela pesquisa de 16/09/2026:

| Uso | Fonte | Licença |
|---|---|---|
| Timbre V12 monoposto | Wikimedia `Superleague_Formula_V12_Brands_Hatch_2010.ogg` | CC BY-SA 3.0 |
| Grito de alta rotação (V8 18.000 RPM) | Freesound 150338 e 150337 (Ears68) | CC0 |
| Timbre V6 turbo híbrido | Freesound 410894 (wandererscapes, Monza 2014) | CC0 |
| Timbre V10/V12 aspirados | Wikimedia `Williams-Renault_FW18_(1996).ogg`, `Ferrari_312_68_(1968).ogg` | CC BY-SA 3.0 |

As gravações **não são publicadas** nem versionadas: o script as baixa e confere o SHA-256. Do áudio só saem números (amplitude relativa de cada ordem do motor por faixa de RPM), gravados em `alvos-timbre.json`. A página de créditos cita as fontes mesmo assim.

**Análise (order tracking):**
1. Estimar f0 em janelas curtas com busca guiada pela fórmula e pelo perfil do motor (pYIN/autocorrelação + pico espectral).
2. Aceitar só trechos com f0 estável ou em rampa suave e boa relação sinal/ruído (descarta público, locutor e helicóptero).
3. Medir a amplitude das ordens 0,5 a 24 relativas a f0. Doppler e distância mudam f0 e o brilho, mas preservam a razão entre ordens; compensar a absorção do ar por uma inclinação espectral estimada.
4. Agregar por faixa de RPM → envelope harmônico alvo por motor.

### 2. Modelo físico offline e banco de loops

Roda no Node, sem limite de tempo real, a 192 kHz com reamostragem final para 48 kHz.

- **Pulso de escape por cilindro:** blowdown com forma derivada da abertura da válvula e da pressão no cilindro em função de carga e RPM; pequena variação ciclo a ciclo com semente fixa.
- **Escape:** guia de onda por primário com comprimento real, junção no coletor (6-em-1 por bancada no V12), tubo final e radiação na saída (diferenciação/passa-alta). No V6, a turbina atenua e suaviza os pulsos.
- **Admissão:** guias de onda das trompetas e ressonância do airbox; mistura com o escape conforme a posição do ouvinte (externo, traseira três-quartos).
- **Mecânica:** trem de válvulas, cascata de engrenagens (dentes × RPM) e ruído estrutural do bloco.
- **Calibração:** um otimizador ajusta os parâmetros livres (comprimentos efetivos, perdas, mistura admissão/escape, EQ de radiação) para minimizar a distância log-espectral entre as ordens geradas e o envelope alvo de cada faixa de RPM.

**Banco de loops por motor:**
- Pontos de RPM em espaçamento geométrico de ~8% entre marcha lenta e limite (V12: ~19 pontos; V6: ~17).
- Duas cargas por ponto: acelerador pisado e aliviado.
- Cada loop tem um número inteiro de ciclos de 720° (≥ 0,6 s, para não soar repetitivo) e começa no pico do pulso do cilindro 1.
- O manifesto guarda, por loop: RPM, carga, amostras por ciclo, número de ciclos, deslocamento no `.bin` e SHA-256 do arquivo.
- Tamanho estimado: ~2–3 MB por motor em PCM Int16 (sem codec, pontos de loop exatos).

### 3. Reprodução com fase travada (`phase-player.mjs`)

- O estado central é o ângulo do virabrequim θ ∈ [0, 720°), avançado a cada amostra por `RPM/60 × 720 × dt`.
- Cada loop é lido na posição `θ/720 × amostrasPorCiclo`, com interpolação Hermite. Os dois pontos de RPM vizinhos e as duas cargas são misturados por interpolação bilinear com **ganho linear** (sinais correlacionados, já alinhados em fase).
- **Dinâmica:** o RPM segue o acelerador com inércia e freio-motor; o limitador corta a ignição ciclo a ciclo silenciando pulsos individuais; ao aliviar em alta rotação, estalos esparsos sincronizados a θ.
- **Camadas sintetizadas por cima:** V6: turbo (rotação com atraso de primeira ordem, assobio + sopro da wastegate) e MGU-K (zumbido tonal proporcional ao RPM); V12: nenhuma, o banco já contém tudo.
- **Saída:** saturação suave, compressor e limitador em −1 dBFS; volume inicial baixo; o áudio só começa após clique (regra do navegador).
- O mesmo núcleo roda no Node para testes e dentro do AudioWorklet no navegador. Os buffers chegam ao worklet por `postMessage` com transferência.

### 4. Motor V12 3D (`v12-v1.glb`)

Gerador Blender no padrão de `ferramentas/sistemas/lib.py`, com 60–80 peças nomeadas e manifesto:
bloco a 65°, cárter seco e bomba de óleo, virabrequim de 6 moentes, 12 bielas e pistões, 2 cabeçotes, 4 comandos, 48 válvulas (agrupadas por cabeçote), cascata de engrenagens, 12 trompetas com airbox, coletores 6-em-1 por bancada, alternador e suportes.

O V6 continua sendo o `power-unit-v1.glb` atual.

### 5. Aba 07 Som (`sound-studio.js`)

- **Motor:** seletor V6 2026 / V12 anos 90; motor 3D na bancada com vista explodida e peças clicáveis (nome e função).
- **Controles:** Ligar/Desligar, acelerador (0–100%), volume, e os presets: marcha lenta, 6.000 RPM, 7.000 RPM, giro máximo, "mesma rotação nos dois motores".
- **Afinador ao vivo:** RPM, f0 prevista, nota e cents; ao lado, a f0 **medida** no áudio de saída (`AnalyserNode` + autocorrelação) — a prova da calibragem.
- **Ignição visual:** os cilindros acendem na ordem de ignição; abaixo de ~1.500 RPM efetivos da animação, câmera lenta indicada.
- **Créditos:** link para a página de créditos das referências.

Falha no carregamento do banco ou do GLB mostra mensagem no painel e mantém o resto do laboratório funcionando.

## Fora do escopo

Trocar o motor dentro do carro; V12 na bancada Sistemas; gravações reais tocadas no site; câmbio/troca de marchas; perspectiva onboard; V4/V8/V10 (a arquitetura permite adicionar perfis depois).

## Testes

| Arquivo | Verifica |
|---|---|
| `web/test-tuning.mjs` | A tabela de afinação acima (Hz, nota e cents) |
| `web/test-sound-player.mjs` | Com banco de teste: f0 medida a ±1% da fórmula em 5 RPMs por motor; crossfade entre pontos vizinhos sem queda de RMS maior que 1 dB (sem phasing); ordem de ignição; limitador corta ciclos inteiros; sem NaN; pico ≤ −1 dBFS |
| `web/test-sound-bank.mjs` | Manifesto dos bancos: cobertura de RPM e cargas, ciclos inteiros, SHA-256, início alinhado ao cilindro 1 (correlação) |
| `ferramentas/som/test-calibracao.mjs` | Distância log-espectral entre banco gerado e alvos abaixo do limite definido na primeira calibração; o limite fica registrado no manifesto |
| `web/test-v12.mjs` | Manifesto do V12: 12 pistões, 12 bielas, 48 válvulas, 12 trompetas, 6 moentes; 20 ciclos de animação sem deriva |
| Navegador | Aba 07 abre, os dois motores tocam, f0 medida ≈ prevista, cilindros sincronizados, 0 erros no console, layout a 400 px |

Os testes novos entram no `npm test`.

## Critério de aceite do som

Além dos testes automáticos: audição comparativa lado a lado com as referências (fora do site), registrada em `docs/ESTUDIO-SOM.md` com o que foi ajustado. O dono do projeto aprova o timbre antes do merge.

## Riscos

- **Realismo abaixo do esperado:** a síntese calibrada melhora muito o timbre, mas não iguala gravação de dinamômetro. Mitigação: o banco é substituível por arquivo; um pacote gravado pode entrar depois sem mudar código.
- **Referências sujas** (público, Doppler): order tracking com filtro de estabilidade; se uma referência não render trechos válidos, ela é descartada e isso fica registrado.
- **CPU no celular:** o worklet só lê buffers e mistura 4 loops + camadas; custo baixo.
