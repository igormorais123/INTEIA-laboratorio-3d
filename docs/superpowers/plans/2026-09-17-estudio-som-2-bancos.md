# Estúdio de som — Plano 2: bancos de loops calibrados (V12 e V6)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Gerar `web/assets/som-v12-v1.bin/.json` e `web/assets/som-v6-v1.bin/.json` por um modelo físico offline calibrado pelo espectro de gravações livres, no formato que `web/src/sound/phase-player.mjs` já consome, com testes que provam integridade, alinhamento e afinação — e demonstrações em WAV para o dono ouvir antes de qualquer coisa ir para a aba ou para produção.

**Architecture:** Duas metades. Em `ferramentas/som/` (offline): download conferido por SHA-256 → cache mono 48 kHz → *order tracking* das ordens de virabrequim por faixa de RPM (`alvos-timbre.json`) → modelo físico a 192 kHz cujas guias de onda viram filtros IIR (regime permanente exatamente periódico: o loop fecha sem emenda) → evolução diferencial nos parâmetros físicos + EQ suave por ponto → banco PCM Int16. Em `web/src/sound/`: `bank-format.mjs` valida manifesto e `.bin` e entrega o banco em memória ao reprodutor. Do áudio real só saem números.

**Tech Stack:** Node ≥ 24 (rede, testes do site, demos); Python 3.13+ com `numpy`, `scipy` e `soundfile` num venv próprio em `ferramentas/som/.venv` (`requirements.txt`). Sem dependências novas em `web/`. O `soundfile` (libsndfile 1.2) decodifica Ogg Vorbis e MP3 sem ffmpeg, o que dispensou os decodificadores WASM previstos no roteiro.

**Status:** executado em 17/09/2026 neste plano; a aprovação do timbre pelo dono (Tarefa 7) é o portão para os Planos 3 e 4.

**Spec:** `docs/superpowers/specs/2026-09-16-estudio-som-v12-design.md` · **Roteiro:** `2026-09-17-estudio-som-2-a-4-roteiro.md` · **Continuação:** `docs/estudio-som/HANDOFF.md`

## Global Constraints

- Gravações de referência nunca entram no Git nem no site; `.referencias/`, `.cache/`, `.demos/`, `.venv/` e `node_modules/` de `ferramentas/som/` estão no `.gitignore`.
- Licenças aceitas: CC0 e CC BY-SA 3.0 (validado por `test-referencias.mjs`). Créditos visíveis no site ficam para o Plano 4.
- Um único medidor de ordens para gravação e render (`analisar_referencias.measure_frame`), para que alvo e modelo passem pela mesma régua.
- Loops: ciclos inteiros de 720°, `rpm = 120 × 48000 / samplesPerCycle` exato, início na chegada do pulso do cilindro 1 à saída, duração ≥ 0,6 s, pico do banco em −3 dBFS, `.bin` ≤ 3 MB.
- Toda filtragem depois do corte do loop é circular (EQ por multiplicação no domínio da frequência), para preservar o fechamento.
- Testes existentes não mudam; `npm test` ganha `test-sound-bank.mjs`; os testes Python rodam com `python -m unittest` dentro de `ferramentas/som`.
- Português brasileiro em textos, commits e mensagens.

## Mapa de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `ferramentas/som/baixar-referencias.mjs` | Baixa e confere bytes + SHA-256 das referências |
| `ferramentas/som/test-referencias.mjs` | Valida `referencias.json` sem rede |
| `ferramentas/som/decodificar.py` | Ogg/MP3 → `.cache/<id>.f32` mono 48 kHz (FIR polifásico) + `.json` |
| `ferramentas/som/analisar_referencias.py` | Order tracking → `alvos-timbre.json` |
| `ferramentas/som/diagnostico_analise.py` | Espectrograma com o traçado de f0 (conferência visual, `.cache/diag-*.png`) |
| `ferramentas/som/modelo_fisico.py` | Modelo físico, `render_loop`, `render_starter`, `apply_circular_eq` |
| `ferramentas/som/perfis/<motor>.json` | Dados do motor e parâmetros físicos (atualizados pela calibração) |
| `ferramentas/som/calibrar.py` | Evolução diferencial + EQ por ponto → `calibracao-<motor>.json` |
| `ferramentas/som/gerar_banco.py` | Renderiza o banco → `web/assets/som-<motor>-v1.bin/.json` |
| `ferramentas/som/renderizar_demos.mjs` | WAVs de audição em `.demos/` |
| `ferramentas/som/test_decodificar.py`, `test_analise.py`, `test_modelo.py`, `test_calibracao.py` | Testes Python |
| `web/src/sound/bank-format.mjs` | `validateManifest`, `parseBank`, `verifyBankHash`, `loadBank` |
| `web/test-sound-bank.mjs` | Integridade, cobertura, alinhamento e afinação dos bancos reais |
| `docs/ESTUDIO-SOM.md` | Como regenerar, distâncias, bandas extrapoladas, limitações, créditos |

---

### Task 1: Referências locais

**Files:** `ferramentas/som/baixar-referencias.mjs`, `ferramentas/som/test-referencias.mjs`, `.gitignore`.

- [x] Baixar cada `url` com o `userAgent` do JSON, conferir `bytes` e `sha256`, não rebaixar o que confere, falhar com mensagem clara.
- [x] Teste sem rede: campos obrigatórios, licenças na lista permitida, sha256 de 64 hex, ids únicos.
- [x] Resultado: 6 referências conferidas (Wikimedia ×3, Freesound ×3).

### Task 2: Decodificação para cache

**Files:** `ferramentas/som/decodificar.py`, `test_decodificar.py`, `requirements.txt`.

- [x] `soundfile` lê Ogg e MP3; mistura para mono; `scipy.signal.resample_poly` com janela Kaiser (β = 12) para 48 kHz.
- [x] Teste: seno de 1 kHz a 44,1 kHz → pico a menos de 0,1 Hz de 1.000 Hz e ganho unitário.
- [x] Cache reutilizado quando o SHA-256 da fonte confere.

### Task 3: Order tracking → `alvos-timbre.json`

**Files:** `ferramentas/som/analisar_referencias.py`, `test_analise.py`, `diagnostico_analise.py`.

**Interfaces:** `analyse_signal(signal, cylinders) → {frames, framesTotal, track, scores}`; `measure_frame(row, floor, freqs, f0, cylinders, slope) → {rpm, orders{ordem: dB}, noiseFloorDb, tiltDbPerOct, hnr}`; `aggregate_bands(frames)`; `extrapolate_bands(...)`.

- [x] STFT Hann 8192 / salto 1024; candidatos de **frequência do virabrequim** (3.000–19.000 RPM, passo 0,4 %).
- [x] Pontuação por ordens fortes menos ordens fracas. Descoberta durante a execução: com coletor por bancada, a **ordem de bancada** (cilindros/4) é tão forte quanto a de ignição; pontuar só a ordem de ignição empurrava o traçado para a oitava de baixo. No V6 turbo, as bancadas se unem na turbina e só as múltiplas da ordem de ignição contam (`BANK_COLLECTOR`).
- [x] Viterbi em log f0 (1 % de salto custa 1 dB; salto máximo 8 %/quadro), estabilidade < 3 % em 5 quadros, HNR > 6 dB, pontuação ≥ 8 dB.
- [x] Medição por **soma de potência** numa janela que cobre o lóbulo principal e o espalhamento do chirp (pico isolado errava até 1,8 dB nas ordens altas em rampa).
- [x] Compensação de distância: diferença de inclinação acima de 4 kHz por fonte em relação à mediana da classe (V8: ±2,4 dB/oit entre as duas gravações de Melbourne), registrada em `distanceTiltRemovedDbPerOct`.
- [x] Bandas de 1.000 RPM com ≥ 5 quadros; V12 extrapolado de 12.000 a 17.000 e V6 de 10.000 a 14.000 com a tendência de inclinação do V8/V10 (`extrapolated: true`).
- [x] Testes: rampa sintética 5.000→9.000 RPM com ordens conhecidas → f0 < 0,5 % e níveis < 1 dB; ruído branco rejeitado; V6 sintético sem erro de oitava; todas as fontes reais em `sources` ou `rejectedSources`.
- [x] Resultado real: 6/6 fontes aceitas; V12 3.000–11.000 RPM (2.999 + 160 quadros), V10 3.700–12.500, V8 5.100–19.000 (5.356 quadros), V6 8.600–14.500 (293 quadros). Conferido nos espectrogramas de `diagnostico_analise.py`.

### Task 4: Modelo físico offline

**Files:** `ferramentas/som/modelo_fisico.py`, `perfis/v12_90s.json`, `perfis/v6_2026.json`, `test_modelo.py`.

**Interfaces:** `render_loop(profile, params, rpm, samples_per_cycle, load, cycles, *, warmup, seed, eq_curve) → ndarray`; `render_starter(profile, params)`; `PARAM_SPACE` (limites físicos); `UNCALIBRATED`.

- [x] Excitação por cilindro em graus de virabrequim: blowdown (subida em cosseno, decaimento exponencial, assimetria), sopro de deslocamento, sucção da admissão, cliques de válvula; variação ±2 % / ±0,3° com semente por `(ciclo mod N, cilindro)`; pops esparsos na carga aliviada.
- [x] Primário por cilindro (guia fechada/aberta como pente IIR com perda passa-baixa; dispersão de comprimento `primarySpread`), coletor por bancada, **assimetria do ouvinte** (`bankBalance`, `bankDelayMs` — sem ela, bancadas idênticas cancelam a ordem de bancada, que no carro real chega a 0 dB), turbina passa-baixa + sopro no V6, radiação passa-alta, boca passa-baixa.
- [x] Admissão (trompeta de quarto de onda + airbox), engrenagens (ordem = dentes), estrutura (ruído modulado pela combustão), saturação `tanh` antes do ganho por rotação (`levelPerOctaveDb`).
- [x] Render a 192 kHz, decimação FIR (Kaiser β = 9), corte dos últimos N ciclos após 8 de aquecimento, rotação para o início no pulso do cilindro 1 (`evoDeg` + percurso primário + coletor).
- [x] Testes: f0 por soma harmônica a ±0,5 % em 5 rotações × 2 motores; emenda < p99 das diferenças internas; sem NaN; determinístico (SHA-256 igual); aliviado < 60 % do pisado; partida fechada.
- [x] Tempo: ~0,3 s por loop de 0,6 s.

### Task 5: Calibração

**Files:** `ferramentas/som/calibrar.py`, `calibracao-<motor>.json`, `test_calibracao.py`.

**Interfaces:** `bank_points(profile)`, `measure_loop(loop, rpm, cylinders)`, `target_at(bands, rpm)`, `distance(render, target, floor, cylinders)`, `fit_eq(hz, residual_db)`.

- [x] Distância = RMS (dB) nas ordens harmônicas suavizadas em 3 pontos + 0,5 × dobradiça nas demais ordens; alvos afogados no piso da gravação (+3 dB) contam só como limite superior.
- [x] Evolução diferencial (`scipy`, semente 1, população 8×, até 30 gerações, 12 processos) sobre todos os parâmetros de `PARAM_SPACE` menos `UNCALIBRATED` (e os de turbina no V12), partindo dos valores do perfil; bandas: medidas acima da marcha lenta (peso 1; 0,6 com 5–19 quadros) + primeira e última extrapoladas (peso 0,5).
- [x] EQ por ponto do banco: resíduo nas ordens harmônicas → 6 nós em log-Hz (150 Hz a 14 kHz), mínimos quadrados com regularização, ±8 dB, ordem de ignição mantida em 0 dB.
- [x] Registro: parâmetros finais no perfil; distâncias antes/depois por banda, `maxBandDistanceDb`, `acceptLimitDb = máximo + 0,5 dB`, EQ por ponto e inércia (não medida: mantidos os valores de `engine-profiles.mjs`).
- [x] `test_calibracao.py`: cada loop pisado do banco publicado fica dentro de `acceptLimitDb` (+1 dB de folga pela EQ do ponto vizinho).

### Task 6: Formato do banco e gerador

**Files:** `web/src/sound/bank-format.mjs`, `ferramentas/som/gerar_banco.py`, `web/test-sound-bank.mjs`, `web/package.json`.

- [x] Manifesto `{version: 1, engine, sampleRate: 48000, format: 'pcm_s16le', bin, bytes, sha256, generator, calibration, profile, normalization, loops[{rpm, load, samplesPerCycle, cycles, offset, frames}], starter{offset, frames}}`.
- [x] `validateManifest` (versão, taxa, formato, frames = ciclos × amostras, rpm exato, trechos sem sobreposição e dentro do arquivo), `parseBank` (Int16 → Float32), `verifyBankHash` (SHA-256 quando há `crypto.subtle`), `loadBank`.
- [x] Gerador: pontos geométricos de 8 %, duas cargas, `cycles = ceil(0,6 s / ciclo)`, EQ do ponto, normalização comum (pico −3 dBFS; partida −9 dBFS), `.bin` + manifesto em `web/assets`.
- [x] `test-sound-bank.mjs` (em `npm test`): bytes e SHA-256, ≤ 3 MB, cobertura (primeiro ponto ≤ marcha lenta, último ≥ limite, passos < 9 %), duas cargas por ponto, loops ≥ 0,6 s, pico ≤ −3 dBFS, emenda, aliviado < pisado, pulso do cilindro 1 no início da janela, defasagem entre rotações vizinhas ≤ 15 % da janela de ignição, e `createPhasePlayer` com o banco real medindo f0 a ±1 % em 5 rotações.

### Task 7: Demos, documentação e portão do dono

**Files:** `ferramentas/som/renderizar_demos.mjs`, `docs/ESTUDIO-SOM.md`, `docs/estudio-som/HANDOFF.md`.

- [x] Demos por motor: 5 presets da curva (com partida e inércia do perfil), rotações fixas (marcha lenta, 6.000, 7.000, 9.000, 12.000, 15.000) e varredura completa ida e volta.
- [x] `docs/ESTUDIO-SOM.md`: regeneração passo a passo, tabela de distâncias por banda, bandas extrapoladas, limitações e créditos.
- [ ] **Portão do dono:** ouvir os demos ao lado das referências (`.referencias/`), aprovar ou pedir iteração (Tarefas 4/5). Nada vai para a aba nem para produção sem esse ok.
