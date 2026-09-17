# Estúdio de som — bancos calibrados do V12 anos 90 e do V6 2026

Os bancos `web/assets/som-v12-v1.*` e `web/assets/som-v6-v1.*` são gerados por um modelo físico offline (escape, admissão e mecânica) cujos parâmetros foram ajustados para reproduzir o espectro de gravações reais de licença livre. Nenhuma gravação é publicada nem versionada: do áudio só saem números (`ferramentas/som/alvos-timbre.json`). O site lê os bancos com `web/src/sound/bank-format.mjs` e os toca com fase travada ao virabrequim (`phase-player.mjs`).

Estado do trabalho e ordem dos planos: [estudio-som/HANDOFF.md](estudio-som/HANDOFF.md). Especificação: [superpowers/specs/2026-09-16-estudio-som-v12-design.md](superpowers/specs/2026-09-16-estudio-som-v12-design.md). Plano executado: [superpowers/plans/2026-09-17-estudio-som-2-bancos.md](superpowers/plans/2026-09-17-estudio-som-2-bancos.md).

## Como o som é produzido

1. **Referências.** `referencias.json` lista seis gravações (V12, V10, V8 e V6 turbo híbrido) com autor, licença, URL e SHA-256. `baixar-referencias.mjs` as guarda em `ferramentas/som/.referencias/` (fora do Git) e recusa qualquer arquivo cujo hash não confira.
2. **Cache.** `decodificar.py` converte Ogg e MP3 em mono 48 kHz (`.cache/`).
3. **Order tracking.** `analisar_referencias.py` rastreia a frequência do virabrequim quadro a quadro (Viterbi sobre a soma das ordens fortes de cada motor), aceita só trechos estáveis com boa relação harmônico/ruído e mede o nível das ordens 0,5 a 60 relativo à ordem de ignição. Os quadros são agregados em faixas de 1.000 RPM. `diagnostico_analise.py` desenha o espectrograma com o traçado para conferência.
4. **Modelo físico.** `modelo_fisico.py` renderiza a 192 kHz: pulso de blowdown por cilindro em graus de virabrequim, primário de cada cilindro como guia de onda, coletor por bancada (ou turbina no V6), tubo final, radiação, trompetas e airbox, engrenagens, válvulas e ruído estrutural, saturação suave. Como tudo depois da excitação é linear e invariante no tempo, o regime permanente é exatamente periódico e cada loop fecha sem emenda.
5. **Calibração.** `calibrar.py` ajusta os parâmetros físicos por evolução diferencial minimizando a distância (dB RMS) entre as ordens do render e as do alvo em várias faixas de RPM, com a mesma régua de medição usada nas gravações; depois calcula uma EQ suave por ponto do banco. O resultado fica em `perfis/<motor>.json` e `calibracao-<motor>.json`.
6. **Banco.** `gerar_banco.py` renderiza pontos de RPM em progressão geométrica de 8 % da marcha lenta ao limite, com acelerador pisado e aliviado, ciclos inteiros de 720° cobrindo ≥ 0,6 s, início no pulso do cilindro 1 e um loop de partida; grava PCM Int16 e o manifesto com SHA-256.
7. **Demos.** `renderizar_demos.mjs` gera WAVs em `.demos/` (presets da curva, rotações fixas e varredura) usando os módulos do site.

## Regenerar

```powershell
# uma vez: ambiente Python isolado (numpy, scipy, soundfile)
python -m venv ferramentas/som/.venv
ferramentas/som/.venv/Scripts/python.exe -m pip install -r ferramentas/som/requirements.txt

node ferramentas/som/baixar-referencias.mjs
ferramentas/som/.venv/Scripts/python.exe ferramentas/som/decodificar.py
ferramentas/som/.venv/Scripts/python.exe ferramentas/som/analisar_referencias.py
ferramentas/som/.venv/Scripts/python.exe ferramentas/som/calibrar.py v12_90s      # ~40 min com 12 processos
ferramentas/som/.venv/Scripts/python.exe ferramentas/som/calibrar.py v6_2026
ferramentas/som/.venv/Scripts/python.exe ferramentas/som/gerar_banco.py v12_90s
ferramentas/som/.venv/Scripts/python.exe ferramentas/som/gerar_banco.py v6_2026
node ferramentas/som/renderizar_demos.mjs
```

Testes: dentro de `ferramentas/som`, `.venv/Scripts/python.exe -m unittest` (decodificação, análise, modelo, calibração) e `node test-referencias.mjs`; no site, `npm --prefix web test` inclui `test-sound-bank.mjs`.

A calibração é determinística (semente fixa) mas demorada; `--rapido` roda poucas gerações para conferir o fluxo e `--sem-otimizar` só recalcula a EQ e o relatório com os parâmetros atuais do perfil.

<!-- calibracao:inicio -->
## Resultado da calibração

### V12 anos 90 (`v12_90s`)

Banco: 20 pontos de RPM (4000–17041) × 2 cargas + partida, 2.42 MB, SHA-256 `cac7c9e19e3a7e8a…`. Distância máxima 9.08 dB (pior ponto do banco, em 14.807 RPM, região extrapolada; pior banda 6,11 dB); limite de aceite 9.58 dB (teste de regressão `test_calibracao.py`).

| Faixa (RPM) | Origem | Antes da EQ (dB) | Depois da EQ (dB) |
| --- | --- | --- | --- |
| 4000–5000 | medida | 7.04 | 4.48 |
| 5000–6000 | medida | 3.26 | 2.37 |
| 6000–7000 | medida | 7.55 | 6.11 |
| 7000–8000 | medida | 3.91 | 3.70 |
| 8000–9000 | medida | 1.64 | 1.17 |
| 9000–10000 | medida | 1.88 | 2.12 |
| 10000–11000 | medida | 3.38 | 2.95 |
| 11000–12000 | medida | 6.06 | 4.88 |
| 12000–13000 | extrapolada | 6.72 | 5.29 |
| 16000–17000 | extrapolada | 3.27 | 2.86 |

Parâmetros físicos finais (`ferramentas/som/perfis/v12_90s.json`): airboxHz = 186, bankBalance = 0.589, bankDelayMs = 0.117, collectorLength = 0.605, decayDeg = 112, displacementLevel = 0.205, drive = 1.92, evoDeg = 135, gasSpeed = 618, gearLevel = 0.00155, gearTeeth = 30, intakeMix = 0.0459, levelPerOctaveDb = 4, mouthHz = 4.45e+03, offLoadLevel = 0.25, offLoadNoise = 0.1, primaryLength = 0.366, primaryLossHz = 7.37e+03, primaryReflection = 0.369, primarySpread = 0.0274, pulseSkew = 0.607, radiationHz = 245, riseDeg = 30, structureLevel = 0.0732, tailLossHz = 4.58e+03, tailReflection = 0.221, trumpetLength = 0.13, turbineHiss = 0, turbineHz = 2e+03, valveLevel = 0.0344.

Inércia: não medido nas referências (nenhuma aceleração em ponto morto isolada); valores de engine-profiles.mjs mantidos.

### V6 2026 (`v6_2026`)

Banco: 19 pontos de RPM (4000–15000) × 2 cargas + partida, 2.30 MB, SHA-256 `f9880a4ee69d50cf…`. Distância máxima 6.76 dB (pior ponto do banco, em 8.000 RPM; pior banda 4,19 dB); limite de aceite 7.26 dB (teste de regressão `test_calibracao.py`).

| Faixa (RPM) | Origem | Antes da EQ (dB) | Depois da EQ (dB) |
| --- | --- | --- | --- |
| 8000–9000 | medida | 4.84 | 4.19 |
| 9000–10000 | medida | 3.23 | 2.74 |
| 10000–11000 | extrapolada | 2.86 | 2.67 |
| 13000–14000 | extrapolada | 4.42 | 2.93 |
| 14000–15000 | medida | 2.35 | 2.31 |

Parâmetros físicos finais (`ferramentas/som/perfis/v6_2026.json`): airboxHz = 141, bankBalance = 0.634, bankDelayMs = 2.45, collectorLength = 0.561, decayDeg = 51.2, displacementLevel = 0.329, drive = 2.8, evoDeg = 119, gasSpeed = 664, gearLevel = 0.0652, gearTeeth = 28, intakeMix = 0.493, levelPerOctaveDb = 4, mouthHz = 1.03e+04, offLoadLevel = 0.25, offLoadNoise = 0.12, primaryLength = 0.411, primaryLossHz = 2.84e+03, primaryReflection = 0.797, primarySpread = 0.0036, pulseSkew = 0.854, radiationHz = 173, riseDeg = 18.7, structureLevel = 0.109, tailLossHz = 2.25e+03, tailReflection = 0.282, trumpetLength = 0.144, turbineHiss = 0.00272, turbineHz = 2.83e+03, valveLevel = 0.0329.

Inércia: não medido nas referências (nenhuma aceleração em ponto morto isolada); valores de engine-profiles.mjs mantidos.
<!-- calibracao:fim -->

## Iteração após a primeira audição (17/09/2026)

Veredito do dono sobre a primeira versão: "muito artificial, parece MIDI de baixa qualidade". A medição confirmou a causa: os loops tinham relação harmônico/ruído de 44 dB e piso entre harmônicos em −55 dB, contra 20–23 dB e −32 a −44 dB nas gravações. Harmônicos puros sem o rugido turbulento do escape soam como sintetizador. Mudanças:

- **Modelo físico:** ruído de jato gerado em cada blowdown (entra nos primários e ganha as ressonâncias do escape), ruído de fluxo contínuo no coletor, turbulência da sucção, variação ciclo a ciclo calibrável (amplitude, instante e decaimento) e desequilíbrio fixo entre cilindros. Todas as fontes de ruído são periódicas em N ciclos, então o loop continua fechando sem emenda.
- **Calibração:** o piso entre harmônicos passou a ser alvo de duas pontas (0,7 × |piso do render − piso da gravação| entra na distância), então a quantidade de turbulência é decidida pelas gravações, não a olho.
- **Voz em tempo real (`web/src/sound/engine-voice.mjs`, usada pelo worklet do site e pelos demos):** desvio lento de rotação (maior em marcha lenta e aliviado), ambiente do box (reflexões primeiras e cauda curta), camadas do V6 com ruído ressonante em vez de senóides puras, estalos ao aliviar. Os demos em `.demos/` agora são renderizados por essa mesma voz, inclusive um arquivo de blips em ponto morto por motor.

## Conferência visual

Os espectrogramas das varreduras (`.demos/*-varredura-*.png`, gerados com `ferramentas/som/espectrograma_demo.py`) mostram harmônicos contínuos da marcha lenta ao limite e de volta, sem degraus nos crossfades entre pontos do banco, com a ordem de bancada visível no V12 e a partida no início. Isso confirma a mecânica do banco; o timbre em si só a audição do dono aprova.

## Limitações conhecidas

- As referências foram gravadas de fora da pista, a dezenas de metros, com público e Doppler. O filtro de estabilidade descarta a maior parte disso, mas a inclinação espectral dos alvos inclui a absorção do ar dessa distância; a compensação aplicada só remove diferenças entre gravações da mesma classe.
- Não há gravação livre de V12 de F1 dos anos 90 nem de V6 híbrido em condição controlada. O V12 vem de um monoposto V12 de 2010 (até ~11.000 RPM medidos) e de um Ferrari 312 de 1968; acima disso as bandas são extrapoladas com a tendência do V8/V10. O V6 tem poucos quadros (uma ambiência de Monza 2014); as bandas ausentes também são extrapoladas.
- O nível absoluto por rotação (`levelPerOctaveDb`), o comportamento aliviado e a inércia não são observáveis nos alvos relativos e ficam como escolhas de projeto no perfil.
- As camadas do V6 (assobio do turbo, wastegate, MGU-K) e os estalos ao aliviar são sintetizados em tempo real pelo Plano 4, não pelo banco.
- Síntese calibrada não iguala gravação de dinamômetro. O banco é substituível por arquivo sem mudar código.

## Créditos das referências

| Fonte | Autor | Licença | Uso |
| --- | --- | --- | --- |
| [Superleague Formula V12, Brands Hatch 2010](https://commons.wikimedia.org/wiki/File:Superleague_Formula_V12_Brands_Hatch_2010.ogg) | Ed Pond (Edvvc) | CC BY-SA 3.0 | Timbre V12 aspirado |
| [Ferrari 312 (1968)](https://commons.wikimedia.org/wiki/File:Ferrari_312_68_(1968).ogg) | Ed Pond (Edvvc) | CC BY-SA 3.0 | Timbre V12 de F1 |
| [Williams-Renault FW18 (1996)](https://commons.wikimedia.org/wiki/File:Williams-Renault_FW18_(1996).ogg) | Ed Pond (Edvvc) | CC BY-SA 3.0 | Timbre V10 anos 90 |
| [Freesound 150338](https://freesound.org/s/150338/) e [150337](https://freesound.org/s/150337/) | Ears68 | CC0 | Grito de alta rotação (V8 2012) |
| [Freesound 410894](https://freesound.org/s/410894/) | wandererscapes | CC0 | V6 turbo híbrido (Monza 2014) |

Os créditos devem aparecer na aba 07 Som (Plano 4).
