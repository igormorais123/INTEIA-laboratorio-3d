# Estúdio de som — roteiro dos Planos 2, 3 e 4

> **Para a IA que continuar:** este arquivo é um **roteiro detalhado**, não um plano executável. Antes de executar cada plano, transforme a seção correspondente num plano completo no formato do Plano 1 (`2026-09-16-estudio-som-1-nucleo.md`): tarefas TDD com código real, comandos e saídas esperadas. Use o skill `superpowers:writing-plans`. O método que funcionou no Plano 1: **prototipar e validar o código numa pasta temporária, rodar mutações para provar que os testes pegam erros, e só então copiar o código validado para o plano.**
>
> Leia antes: `docs/estudio-som/HANDOFF.md`, a especificação `docs/superpowers/specs/2026-09-16-estudio-som-v12-design.md` e `docs/estudio-som/PESQUISA.md`.

**Ordem:** Plano 2 → Plano 4 (pode começar em paralelo com banco sintético) → Plano 3. O Plano 2 é o que decide se o som é convincente; nada vai para produção sem o dono aprovar o timbre ouvindo.

---

## Plano 2 — Bancos de loops calibrados (V12 e V6)

**Objetivo:** gerar `web/assets/som-v12-v1.bin/.json` e `web/assets/som-v6-v1.bin/.json` por modelo físico offline calibrado pelo espectro das gravações de `ferramentas/som/referencias.json`, no formato de banco que `web/src/sound/phase-player.mjs` já consome.

**Stack decidida para o offline:**
- Decodificação em **Node** com `@wasm-audio-decoders/ogg-vorbis` e `mpg123-decoder` (ambos MIT, WASM puro, funcionam em Windows ARM sem ffmpeg). Dependências só em `ferramentas/som/package.json`, nunca em `web/`.
- Análise, modelo físico e calibração em **Python 3 + numpy + scipy** (`ferramentas/som/requirements.txt`). Se o outro PC tiver ffmpeg/soundfile, pode trocar a decodificação, mantendo o mesmo cache.
- Isto substitui os nomes `.mjs` dos scripts de análise/modelo citados na especificação; atualize a tabela de arquitetura da especificação na primeira tarefa.

### Tarefa 2.1 — Referências locais
- `ferramentas/som/baixar-referencias.mjs`: lê `referencias.json`, baixa cada `url` com o `userAgent` do arquivo para `ferramentas/som/.referencias/<file>`, confere `bytes` e `sha256`; falha com mensagem clara se divergir; não baixa de novo o que já confere.
- Acrescentar `ferramentas/som/.referencias/`, `ferramentas/som/.cache/`, `ferramentas/som/.demos/` e `ferramentas/som/node_modules/` ao `.gitignore`.
- Teste: `ferramentas/som/test-referencias.mjs` valida o JSON (campos obrigatórios, licença em lista permitida `CC0`/`CC BY-SA 3.0`, sha256 hex de 64) sem rede.

### Tarefa 2.2 — Decodificação para cache
- `ferramentas/som/decodificar.mjs`: decodifica cada referência, mistura para mono, reamostra para 48 kHz (sinc janelado; teste com seno de 1 kHz: erro de frequência < 0,1 Hz) e grava `.cache/<id>.f32` (Float32 LE) + `.cache/<id>.json` (`sampleRate`, `frames`, `sourceSha256`).
- Atenção: MP3 tem atraso de encoder; irrelevante para análise espectral, mas não reutilize esses áudios como loops.

### Tarefa 2.3 — Order tracking → `alvos-timbre.json`
- `ferramentas/som/analisar_referencias.py`.
- Classe de motor por referência: `superleague_v12`/`ferrari_312_v12` → 12 cilindros; `williams_v10` → 10; `ears68_*` → 8; `monza2014_v6` → 6.
- Algoritmo por referência:
  1. STFT (janela Hann 8192, hop 1024 a 48 kHz).
  2. Candidatos de f0 de ignição em `[idle, limite] × cilindros/120` (use 3.000–19.000 RPM); escolha por soma harmônica das meias ordens (a ignição é a ordem `cilindros/2`; meias ordens capturam irregularidades).
  3. Rastreamento com continuidade (Viterbi simples ou mediana móvel) e filtro de estabilidade: aceitar quadros com variação de f0 < 3% em 5 quadros e razão harmônico/ruído > 6 dB. Isso descarta público, locutor e helicóptero.
  4. Para cada quadro aceito: amplitudes em dB das ordens de motor de 0,5 a 24 (passo 0,5) relativas à ordem de ignição, amostrando o pico do bin mais próximo com interpolação parabólica; piso de ruído entre harmônicos; inclinação espectral (dB/oitava) acima de 4 kHz.
  5. Compensar distância/ar: ajustar inclinação por regressão e remover o componente comum entre referências de mesma classe; registrar o valor removido.
  6. Agregar por faixa de RPM (bandas de 1.000 RPM) com mediana; registrar número de quadros por banda.
- Saída `ferramentas/som/alvos-timbre.json` (versionado): `{version, generatedAt, sources: [{id, sha256, framesAccepted}], classes: {V12: {bands: [{rpmMin, rpmMax, frames, ordersDb: {"0.5": -18.2, ...}, noiseFloorDb, tiltDbPerOct}]}, V10: ..., V8: ..., V6: ...}}`.
- Extrapolação: o V12 real das referências não passa de ~12.000–13.000 RPM. Para 13.000–17.000 RPM, usar a forma das ordens do V12 escalada pela inclinação observada no V10/V8 de alta rotação; marcar essas bandas com `"extrapolated": true`.
- Testes (`test_analise.py`, rodando com `python -m unittest`): sinal sintético com f0 em rampa e ordens de amplitude conhecida → amplitudes recuperadas com erro < 1 dB e f0 < 0,5%; sinal com ruído branco 0 dB → quadros rejeitados; cada referência real gera pelo menos 50 quadros aceitos **ou** entra em `rejectedSources` com motivo (não falhar silenciosamente).

### Tarefa 2.4 — Modelo físico offline
- `ferramentas/som/modelo_fisico.py`, renderização a 192 kHz e decimação para 48 kHz (filtro anti-aliasing FIR de fase linear).
- Parâmetros em `ferramentas/som/perfis/<motor>.json` (valores iniciais, ajustados pela calibração):
  - Pulso de blowdown por cilindro: subida em cosseno durante a abertura da válvula de escape (~50° de virabrequim), decaimento exponencial; amplitude e brilho proporcionais à carga; variação ciclo a ciclo com semente fixa (±2% amplitude, ±0,3° tempo).
  - Primário de escape por cilindro: guia de onda com atraso `L / c` (c do gás quente 500–700 m/s), reflexão negativa na ponta aberta, perda passa-baixa por ida e volta.
  - Coletor por bancada (V12: 6-em-1 × 2; V6: coletor → turbina com passa-baixa e atenuação dos pulsos → saída única), tubo final e radiação (diferenciação/passa-alta de 1ª ordem).
  - Admissão: guia de onda de quarto de onda por trompeta + ressonância de airbox (Helmholtz), mistura com escape por `intakeMix`.
  - Mecânica: trem de válvulas (cliques na frequência dos comandos × válvulas), cascata de engrenagens (ordem = dentes), ruído estrutural filtrado.
  - Carga aliviada: amplitude menor, mais ruído, estalos raros no escape.
  - Partida (`starter`): zunido do motor de arranque + pulsos de compressão sem combustão a 250–300 RPM.
- Periodicidade: ao renderizar um loop de N ciclos, a variação aleatória usa semente por `índiceDoCiclo % N`, e renderizam-se ciclos de aquecimento antes; assim o loop fecha sem emenda.
- Testes: f0 do render a ±0,5% da fórmula em 5 RPMs; emenda do loop (diferença entre última e primeira amostra) menor que o 99º percentil das diferenças internas; sem NaN; render determinístico (mesma semente → mesmo hash).

### Tarefa 2.5 — Calibração
- `ferramentas/som/calibrar.py`: para cada motor e banda, minimizar a distância log-espectral nas meias ordens (0,5–24) entre render e alvo, com `scipy.optimize.differential_evolution` (limites físicos em cada parâmetro, `seed` fixa), usando parâmetros compartilhados entre bandas mais um EQ suave por banda.
- Classes-alvo: `v12_90s` ← alvo V12 (+ V10 para bandas extrapoladas); `v6_2026` ← alvo V6 (poucos quadros: complementar com a forma V8 de alta rotação e registrar isso).
- Registrar em `ferramentas/som/calibracao-<motor>.json`: parâmetros finais, distância por banda (dB RMS) e o limite de aceite = distância obtida + 0,5 dB (vira teste de regressão).
- Também estimar e registrar `maxRiseRpmPerS`/`maxFallRpmPerS` plausíveis (use a maior taxa de subida observada nas referências em ponto morto; se não houver, manter os valores atuais de `engine-profiles.mjs` e registrar "não medido").

### Tarefa 2.6 — Formato do banco e gerador
- `web/src/sound/bank-format.mjs` (JS puro, testado no Node, usado depois pelo Plano 4):
  - `parseBank(manifest, arrayBuffer) → {sampleRate, loops: [{rpm, load, samplesPerCycle, cycles, data: Float32Array}], starter?: {data}}` — exatamente o formato de `prepareBank` do Plano 1.
  - Valida `version`, `sampleRate === 48000`, `format === 'pcm_s16le'`, soma de bytes, sobreposição de trechos, e SHA-256 quando `crypto.subtle` existir.
- Manifesto `som-<motor>-v1.json`:
  ```json
  {"version": 1, "engine": "v12_90s", "sampleRate": 48000, "format": "pcm_s16le", "bin": "som-v12-v1.bin",
   "bytes": 0, "sha256": "", "generator": {"script": "ferramentas/som/gerar_banco.py", "sha256": ""},
   "calibration": {"file": "ferramentas/som/calibracao-v12_90s.json", "maxBandDistanceDb": 0},
   "loops": [{"rpm": 4000, "load": "on", "samplesPerCycle": 1440, "cycles": 24, "offset": 0, "frames": 34560}],
   "starter": {"offset": 0, "frames": 0}}
  ```
- `ferramentas/som/gerar_banco.py`: pontos de RPM em progressão geométrica de 8% da marcha lenta ao limite, com `samplesPerCycle` inteiro e `rpm = 120 × 48000 / samplesPerCycle` exato; cargas `on`/`off`; `cycles = ceil(0,6 s / ciclo)`; início no pulso do cilindro 1; normalização comum a todo o banco (pico −3 dBFS antes do reprodutor); grava `.bin` + manifesto.
- Testes: `web/test-sound-bank.mjs` (entra no `npm test`): manifesto e `.bin` íntegros (bytes, SHA-256), cobertura de RPM (primeiro ponto ≤ marcha lenta, último ≥ limite), as duas cargas por ponto, ciclos inteiros, correlação do início de cada loop com o próprio pulso do cilindro 1 > 0,9, e integração: `createPhasePlayer` com o banco real mede f0 a ±1% em 5 RPMs (mesmo critério de `test-sound-player.mjs`). Tamanho de cada `.bin` ≤ 3 MB.

### Tarefa 2.7 — Demos para audição e documentação
- `ferramentas/som/renderizar_demos.mjs` (usa os módulos de `web/src/sound/`): WAVs em `.demos/` para cada motor com os 5 presets da curva e rotações fixas 6.000/7.000/12.000.
- `docs/ESTUDIO-SOM.md`: como regenerar tudo, distância de calibração por banda, bandas extrapoladas, limitações e créditos das referências.
- **Portão:** o dono ouve os demos lado a lado com as referências e aprova. Sem aprovação, iterar a Tarefa 2.4/2.5 (não seguir para produção).

---

## Plano 3 — Motor V12 3D

**Objetivo:** `web/assets/v12-v1.glb` + `v12-v1.manifest.json`, gerados por `ferramentas/v12/gerar_v12.py` no Blender.

- Blender: nesta máquina, `C:\Users\igorm\projetos\Aula Labmota\.tools\blender\runtime\blender-5.2.1-windows-arm64\blender.exe`; no outro PC, ver `docs/BLENDER.md` e `docs/OUTRO-PC.md`.
- Seguir o padrão de `ferramentas/gerar_sistemas.py`, `ferramentas/sistemas/lib.py` (peças nomeadas, extras nos nós, materiais físicos) e `ferramentas/otimizar_sistemas.mjs` (meshopt) + `ferramentas/manifest.cjs`.
- Peças (60–80, nomes em português como nas outras peças): bloco a 65°, cárter seco e bomba de óleo, virabrequim de 6 moentes, 12 bielas e 12 pistões, 2 cabeçotes, 4 comandos, 48 válvulas agrupadas por cabeçote, cascata de engrenagens, 12 trompetas + airbox, 2 coletores 6-em-1, alternador, suportes.
- **Animação não é gravada no GLB**: nós `v12_virabrequim`, `v12_pistao_01..12`, `v12_biela_01..12` com extras `{cylinder, bank, pinOffsetDeg}`; o Plano 4 move por código a partir do θ do reprodutor (sincronia exata com o som).
- Testes `web/test-v12.mjs`: GLB e manifesto íntegros (bytes, SHA-256, ≤ 25 MiB), contagens (12 pistões, 12 bielas, 48 válvulas, 12 trompetas, 6 moentes), extras presentes, cinemática biela-manivela de cada pistão a 0°/180°/360° dentro de 0,1 mm do esperado e 20 ciclos sem deriva (mesmo critério de `test-power-unit.mjs`).
- Referências visuais públicas do Ferrari 412 T2 / 3.0 V12 só para proporção; geometria original INTEIA (sem copiar CAD).

---

## Plano 4 — Aba 07 Som

**Objetivo:** a aba no laboratório, conforme a seção 6 da especificação.

- Ler antes: `web/src/workbench.js` (abas 01–06, `role=tab`, `aria-controls='lab-panel'`), `web/src/template-v2.html` (painéis), `web/build.cjs` (bundle único), `web/src/engine/in-car.js` (carregamento sob demanda com `AbortController`), `web/test-systems.mjs` (estilo dos testes estáticos da interface; há teste que proíbe metalinguagem como "vídeo", "homolog", "não é CAD" no painel).
- `web/src/sound/engine-worklet.js`: `AudioWorkletProcessor` que recebe por `postMessage` o banco (transferência dos `ArrayBuffer`), o perfil e o estado; roda `createRpmFollower` + `createPhasePlayer` + camadas V6 (turbo com atraso de 1ª ordem e wastegate; MGU-K tonal) + estalos ao aliviar sincronizados a θ; envia de volta a cada ~30 ms `{rpm, thetaDeg, running, limiter, load}` para UI e 3D.
- Build: gerar o worklet com esbuild como string IIFE e injetar como `Blob` + `audioWorklet.addModule(URL.createObjectURL(...))`; novo marcador no template, com `replaceRequired`.
- `web/src/sound/curve-editor.js` (SVG, sem dependências): pontos com mouse e teclado, grade de notas via `firingHz`/`hzToNote`, traço fino da curva "real" (`simulateCurve`), presets `CURVE_PRESETS`, importar/exportar JSON, `localStorage` com `try/catch`.
- `web/src/sound/sound-studio.js`: seletor de motor, carregamento sob demanda (`bank-format.mjs` + GLB do V12; V6 usa `power-unit-v1.glb`), Ligar/Desligar (o áudio só inicia após clique), modo curva e modo livre, volume inicial baixo, afinador com f0 **prevista** e **medida** (`AnalyserNode.getFloatTimeDomainData` + `detectPitch`), cilindros acendendo com `cylinderAt`, falhas de carga com mensagem no painel sem quebrar o resto.
- Créditos das referências (autor, licença, link) acessíveis a partir da aba.
- Testes: `web/test-sound-studio.mjs` (estático: aba 07 no template e no workbench, IDs, rótulos, marcador do worklet no build, ausência de metalinguagem) e `web/test-curve-editor.mjs` (lógica de edição separada do DOM: inserir, mover sem cruzar vizinhos, apagar, teclado).
- Verificação no navegador (Playwright): `PORT=<livre> node server.cjs`, abrir a aba 07, tocar a rampa padrão nos dois motores, conferir f0 medida ≈ prevista, editar pontos por mouse e teclado, trocar V6 ↔ V12 e ver a grade mudar, 0 erros no console, layout a 400 px.
- Depois do merge: publicação seguindo `docs/PUBLICACAO.md` (ChatGPT Sites), somente com autorização do dono.
