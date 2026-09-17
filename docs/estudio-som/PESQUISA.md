# Estúdio de som — pesquisa de 16 e 17/09/2026

Duas pesquisas feitas antes do desenho. Só entram fontes abertas e conferidas; o que não foi aberto está marcado.

## 1. Gravações reais com licença livre

**Conclusão:** não existe gravação livre (CC0/CC-BY) de V12 de F1 dos anos 90 nem de V6 turbo híbrido que sirva para loops por RPM. O material livre é quase todo gravado de fora da pista (passagens, largadas em subida de rampa, público, locutor, helicóptero); nada onboard nem em rotação constante.

As fontes aproveitáveis para **análise espectral** estão em [`ferramentas/som/referencias.json`](../../ferramentas/som/referencias.json), com URL, autor, licença e SHA-256.

Outras candidatas vistas (não baixadas):

| Fonte | Licença | Observação |
|---|---|---|
| https://freesound.org/people/tim.kahn/sounds/819279/ | CC-BY 4.0 | 14 min em Portland, WAV 48 kHz, provavelmente não é F1 moderna |
| https://freesound.org/people/RTB45/sounds/161971/ | CC-BY 4.0 | GP da China 2012, 10 min, mistura categorias |
| https://freesound.org/people/LG/sounds/77919/ | CC-BY 4.0 | Renault F1 2009 (V8) em exibição de rua, 12,8 s |
| https://freesound.org/people/Heigh-hoo/sounds/167104/ | CC-BY 3.0 | Suzuka 2012, acelerações e passagens lentas |
| https://freesound.org/people/Heigh-hoo/sounds/14830/ | CC0 | Ferrari F2003-GA V10, 5,7 s, mono |
| https://freesound.org/people/lmnmrn/sounds/197219/ | CC0 | "F1 engine ignition" (partida), motor não identificado |
| https://freesound.org/people/djbono/sounds/18771/ | Sampling+ | Ferrari 456 V12 de rua, rampa limpa 800–6.200 RPM (evitar servir o arquivo) |
| https://commons.wikimedia.org/wiki/File:Ferrari_126C4_M2_(1984).ogg | CC BY-SA 3.0 | F1 V6 turbo 1984 (não híbrido), 16 s |
| https://commons.wikimedia.org/wiki/Category:Sounds_of_Formula_One_cars | CC BY-SA 3.0 | 30 arquivos, quase todos de Goodwood |

**Bibliotecas e licenças:** Sonniss GDC (proíbe fornecer arquivos → incompatível com site), BBC RemArc (não comercial), Pixabay (proíbe redistribuir o som isolado; sem F1 com origem clara), Zapsplat (página de licença bloqueou, não verificado), Internet Archive (nada útil), mods de Assetto Corsa/rFactor (sem licença, não usar). Pacotes pagos com licença para web existem, mas nenhum foi verificado com conteúdo de F1.

**Regras legais:** CC BY-SA obriga áudios derivados publicados a sair em BY-SA (o desenho evita isso: só números saem das gravações). Nomes "Ferrari"/"F1" em texto descritivo são baixo risco; não usar logos.

## 2. Como fazer som de motor realista

**Como os jogos fazem** (F1 24, Forza, Assetto Corsa, Project CARS): gravação em dinamômetro/testes com microfones no escape e sidepods; **loops de ciclos inteiros por faixa de RPM**, com acelerador pisado e aliviado; cruzamento **com fase travada** ao virabrequim; turbo, transmissão e limitador como camadas. Forza Horizon 5 usa "granular hybrid looping" (fatia cada rotação). Project CARS usa mais de cem WAVs por carro.

**Síntese pura:**

| Projeto | Técnica | Licença | Web | Avaliação |
|---|---|---|---|---|
| ange-yaghi/engine-sim | Simulação de gás por câmara, atraso de escape, convolução com IR | MIT | Não (issue #428 sem resposta) | Bom para motor de rua; **passa-baixa fixo de 1.900 Hz** em `synthesizer.cpp` abafa a faixa F1. Port para WASM: 3–6 semanas, não compensa |
| DasEtwas/enginesound | Guias de onda (Baldan et al.), exporta WAV em loop | MIT | Não | Timbre sintético; útil como camada |
| Antonio-R1/engine-sound-generator | Baldan em Web Audio (JS, AudioWorklet, WASM), Doppler, three.js | MIT | Sim | Melhor base procedural web, mas soa sintetizador |
| Farnell, *Designing Sound*, Practical 22 | Pulsos, guia de onda com realimentação não linear | Livro | Portável | Didático, realismo médio |
| Baldan, Lachambre, Delle Monache, Boussard (SIVE 2015) | "Physically informed car engine sound synthesis" | Artigo | — | Base teórica (PDF bloqueado, só metadados conferidos) |
| Jagla, Maillard, Martin (ICASSP 2012, HSOLA) | Overlap-add síncrono aos harmônicos sobre rampas gravadas | Artigo | — | Resolve a extração de loops de rampas |

**Detalhes práticos recomendados:**
- Limitar a variação de taxa de leitura de cada loop a ±6–8% (as ressonâncias do escape se deslocam com a afinação): ~19 pontos de RPM no V12 (4.000–17.000, geométrico 8%).
- Extrair loops de uma rampa: estimar f0 (YIN/pYIN guiado pela fórmula), integrar a fase do virabrequim, reamostrar no domínio do ângulo, cortar N ciclos inteiros, alinhar o início no pulso do cilindro 1 por correlação.
- Crossfade entre loops alinhados em fase: **ganho linear** (sinais correlacionados).
- MP3/AAC têm atraso de encoder: nunca confiar em pontos de loop dentro de arquivo comprimido; o desenho usa PCM Int16.
- AudioWorklet sem COOP/COEP: buffers vão ao worklet por `postMessage` com transferência.

Fontes abertas: https://github.com/ange-yaghi/engine-sim · https://github.com/DasEtwas/enginesound · https://github.com/Antonio-R1/engine-sound-generator · https://aspress.co.uk/sd/practical22.html · https://ieeexplore.ieee.org/abstract/document/6287894/ · https://mcvuk.com/development-news/how-to-make-racing-car-engines-roar-using-audiomotors-fmod/ · https://designingsound.org/2014/08/11/vehicle-engine-design-project-cars-forza-motorsport-5-and-rev/ · https://www.the-race.com/gaming/f1-24-how-sounds-are-recorded/ · https://web.dev/racer-sound/ · https://developer.mozilla.org/en-US/docs/Web/API/AudioBufferSourceNode/playbackRate
