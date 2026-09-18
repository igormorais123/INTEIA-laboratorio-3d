# Estúdio de som V6 × V12 — passagem de trabalho (comece por aqui)

**Última atualização:** 17/09/2026 (aba 07 Som publicada a pedido do dono; timbre reprovado na 1ª audição e em iteração) · **Branch:** `estudio-som-v12` · **Dono do projeto:** Igor Morais (aprova timbre, merge e publicação)

Este documento existe para que outra IA, em outro computador, continue o trabalho sem precisar do histórico da conversa.

## 1. O que o dono pediu

Uma opção de **motor V12** no Box INTEIA (laboratório 3D), modelado peça a peça, e um **estúdio de som** para "calibrar a afinação" dos motores V6 2026 e V12 anos 90, com **som realista** — o dono foi explícito: "não quero som mal feito". Ideia central dele, validada:

- A nota do motor vem das explosões: `f0 = (RPM / 60) × (cilindros / 2)`. Ex.: V12 a 6.000 RPM = 600 Hz (Ré 5 +37 cents); a 7.000 RPM = 700 Hz (Fá 5); V4 a 6.000 RPM = 200 Hz (Sol 3).
- Um **acelerador padrão de 0 a 12.000 RPM** editado num **gráfico RPM × tempo com pontos**, como as curvas de cor de editores de imagem; trocando o número de cilindros, a mesma curva "afina" diferente.

Referência que motivou o pedido: vídeo "O Carro mais INJUSTIÇADO da HISTÓRIA! Aston Martin Rapide V12" (Gui AvantGarde), https://www.youtube.com/watch?v=VreW7bn45Og.

## 2. Decisões já tomadas com o dono (não reabrir)

| Tema | Decisão |
|---|---|
| V12 | F1 anos 90: 3,5 L aspirado, 65°, até 17.000 RPM |
| Interface | Nova aba **07 Som**; aba Motor fica como está |
| Fonte do som | **Síntese calibrada no real**: modelo físico offline calibrado pelo espectro de gravações livres; nenhuma gravação é publicada |
| Reprodução | Loops de ciclos inteiros por RPM com **fase travada** ao virabrequim (técnica dos jogos de corrida) |
| Controle | Editor de curva RPM × tempo, eixo padrão 0–12.000 RPM, duração editável |
| Cilindros | Configurações reais (fase 2: 4 em linha, V8 cruzado, V10 72°), não número livre |
| Fases | Fase 1: V6 + V12 + editor. Fase 2: outros motores |

Documentos: especificação `docs/superpowers/specs/2026-09-16-estudio-som-v12-design.md` · pesquisa `docs/estudio-som/PESQUISA.md` · referências `ferramentas/som/referencias.json`.

## 3. Estado atual

| Item | Situação |
|---|---|
| Especificação | Escrita e aprovada pelo dono ("sim, manda ver") |
| **Plano 1 — núcleo** (`docs/superpowers/plans/2026-09-16-estudio-som-1-nucleo.md`) | **Concluído** e commitado: `web/src/sound/tuning.mjs`, `engine-profiles.mjs`, `rpm-curve.mjs`, `pitch.mjs`, `phase-player.mjs`, `web/test-fixtures/sound-bank.mjs`, testes `test-tuning.mjs`, `test-rpm-curve.mjs`, `test-sound-player.mjs` no `npm test` |
| **Plano 2 — bancos calibrados** (`docs/superpowers/plans/2026-09-17-estudio-som-2-bancos.md`) | **Concluído** em 17/09/2026: `web/assets/som-v12-v1.bin/.json` (20 pontos, 2,42 MB) e `som-v6-v1.bin/.json` (19 pontos, 2,30 MB), `web/src/sound/bank-format.mjs`, `detectFiringHz` em `pitch.mjs`, `web/test-sound-bank.mjs` no `npm test`; pipeline em `ferramentas/som/` (Python + Node); `docs/ESTUDIO-SOM.md` |
| **Portão do dono** | **2ª audição aceita com ressalva** em 18/09/2026: "ruim mas aceitável". O timbre passa, não encanta; o estúdio segue em produção e a próxima iteração deve atacar o ambiente acústico (reverberação do box e da pista) e a resposta ao acelerador, não mais o piso de ruído. Histórico: **1ª audição reprovada** ("muito artificial, parece MIDI de baixa qualidade"). Causa medida e corrigida no modelo (ruído de jato/fluxo, variação ciclo a ciclo, piso como alvo) e na voz em tempo real (`engine-voice.mjs`: desvio de rotação, ambiente, camadas sem senóides). Demos da 2ª versão em `ferramentas/som/.demos/` (26 WAVs, agora com a mesma voz do site, inclusive `*-blips.wav`) e a própria aba 07 em produção |
| **Plano 3 — V12 3D** | **Concluído.** `ferramentas/v12/gerar_v12.py` gera `web/assets/v12-v1.glb` (87 nós, 4,68 MB) e o manifesto. Sem movimento gravado: `web/src/sound/v12-kinematics.mjs` coloca virabrequim, bielas, pistões e comandos pelo ângulo θ do som, e `web/src/sound/v12-view.js` mostra o motor na bancada da aba 07 com corte do bloco e airbox removível. Teste `web/test-v12.mjs` |
| **Plano 4 — aba 07 Som** | **Construído e mesclado na main (PR #12)** a pedido do dono para teste em produção: `web/src/sound/sound-studio.js`, `curve-editor.js`, `engine-voice.mjs`, `engine-worklet.js` (IIFE injetada no template como `__SOUND_WORKLET__`), testes `test-sound-studio.mjs`, `test-curve-editor.mjs`, `test-engine-voice.mjs`. Com o motor V12 3D sincronizado na bancada (Plano 3) e um diagrama de cilindros ao lado. Afinador com `detectFiringHz` |
| Referências de áudio | Baixadas e conferidas (SHA-256 no JSON); **não versionadas** |
| Produção | Aba 07 publicada no ChatGPT Sites em 17/09/2026 (checkout de deploy com 12 arquivos, incluindo os bancos). Segunda publicação no mesmo dia com os bancos recalibrados (V12 pior banda 8,49 dB, V6 6,16 dB) |

Roteiro dos Planos 2–4: `docs/superpowers/plans/2026-09-17-estudio-som-2-a-4-roteiro.md`.

## 4. Primeiros comandos no outro PC

```powershell
git clone https://github.com/igormorais123/INTEIA-laboratorio-3d.git
cd INTEIA-laboratorio-3d
git switch estudio-som-v12
cd web
npm ci
npm test          # deve terminar com as linhas "Afinação", "Curva RPM" e "Reprodutor" OK
```

Requisitos: Node ≥ 24; para regenerar os bancos, Python 3.13+ com `numpy`, `scipy` e `soundfile` num venv em `ferramentas/som/.venv` (`requirements.txt`; o `soundfile` decodifica Ogg e MP3 sem ffmpeg); para o Plano 3, Blender 5.2 (ver `docs/BLENDER.md` e `docs/OUTRO-PC.md`). Sequência completa em `docs/ESTUDIO-SOM.md`.

## 5. O que fazer, em ordem

1. Ler a especificação, `PESQUISA.md`, o roteiro, o plano do Plano 2 e `docs/ESTUDIO-SOM.md`.
2. **Portão do dono (agora):** ele ouve `ferramentas/som/.demos/*.wav` ao lado das referências em `.referencias/` (as varreduras `*-varredura-*.wav` são as mais reveladoras). Se aprovar, seguir. Se reprovar, iterar em `modelo_fisico.py` (estrutura) ou `calibrar.py`/`alvos-timbre.json` (alvos e métrica), regenerar bancos e demos e voltar a este passo. Registrar o veredito e o que mudou em `docs/ESTUDIO-SOM.md`.
3. **Plano 4** (a aba) com os bancos reais: `loadBank` de `bank-format.mjs`, worklet em volta de `phase-player.mjs`, camadas turbo/MGU-K do V6 e estalos ao aliviar em tempo real, afinador com `detectFiringHz`, créditos das referências visíveis.
4. **Plano 3** (V12 3D) — feito. Para mexer na geometria, edite `ferramentas/v12/gerar_v12.py`, rode o Blender, confira as prévias renderizadas e rode `npm test`; o manifesto é regravado com o SHA-256 novo, que o teste compara.
5. Abrir PR do branch `estudio-som-v12` para `main`, com verificação no navegador. Merge e publicação (`docs/PUBLICACAO.md`, ChatGPT Sites — único destino de deploy; o GitHub Actions foi removido) **somente com autorização do dono**.

Lições do Plano 2 que valem para quem iterar o som: (a) a ordem de bancada (cilindros/4) é forte em motores com coletor por bancada, e o V6 turbo não a tem; (b) bancadas idênticas cancelam essa ordem no modelo — a assimetria do ouvinte (`bankBalance`, `bankDelayMs`) é obrigatória; (c) o ganho por rotação entra depois da saturação; (d) medir ordens por soma de potência com janela proporcional ao chirp; (e) alinhar rotações vizinhas e as duas cargas por correlação depois do render, porque perto de ressonâncias o pulso do cilindro 1 sozinho não garante crossfade sem phasing; (f) o pente IIR em blocos de D amostras é 5× mais rápido que o denominador denso.

## 6. Como o trabalho foi coordenado (repetir se quiser)

- O dono prefere **executores baratos** e uma IA como **coordenadora e avaliadora independente**. No PC original: Codex CLI 0.153 com `gpt-5.6-luna` esforço `max` como executor e `gpt-5.6-sol` esforço `high` como reserva para tarefas difíceis.
- Comando usado por tarefa:
  ```bash
  codex exec -m gpt-5.6-luna -c model_reasoning_effort='"max"' -s workspace-write -C . -o saida.txt "<instruções: ler Global Constraints e a Task N do plano; TDD; copiar o código do plano exatamente; NÃO fazer git add/commit; relatar saídas>"
  ```
- A coordenadora revisa: compara arquivos com o plano, roda os testes ela mesma, confere mutações e só então faz o commit (mensagem cita o executor).
- Tarefas de pesquisa e desenvolvimento (Plano 2: modelo físico e calibração) são adequadas ao `gpt-5.6-sol` alto, com critérios objetivos de aceite (distâncias espectrais, f0 medida) definidos antes.
- No segundo PC (64 GB, 24 núcleos, 17/09/2026) o Plano 2 foi executado diretamente pela IA coordenadora, sem executores Codex: a calibração roda com 12 processos (`--workers`); `nohup` no Git Bash deixou um processo órfão com a saída presa no buffer — usar `python -u` e conferir `Get-CimInstance Win32_Process` antes de relançar.
- **Problema visto:** o PC original tinha 15,6 GB de RAM com ~1 GB livre (Chrome com ~3 GB); uma execução do Codex foi morta por falta de memória e deixou um `codex exec` órfão. Verifique processos órfãos após interrupções e não rode vários executores em paralelo com pouca memória.

## 7. Regras do projeto que não podem ser quebradas

- Português brasileiro em textos, interface e commits (frase no imperativo, como no histórico). Commits com atribuição da IA quando houver.
- A interface não usa metalinguagem de produção: `test-systems.mjs` proíbe no painel termos como "vídeo", "capítulo", "prompt", "homolog", "não é CAD", "hipótese". Aplique a mesma regra à aba 07.
- Nunca publicar nem versionar os áudios de referência; da análise só saem números. Créditos das referências visíveis no site.
- `web/` não ganha dependências novas sem necessidade; ferramentas offline têm `package.json`/`requirements.txt` próprios em `ferramentas/som/`.
- Testes existentes não são alterados para passar; se falharem, o problema está no código.
- `web/index.html` é gerado por `npm run build`; commitar o build atualizado junto com mudanças de interface.
- Publicação oficial é no ChatGPT Sites (`docs/PUBLICACAO.md`); GitHub Pages foi aposentado.

## 8. Pendências fora do estúdio de som

- **PR #10** (`sistemas-como-funciona`): "Como funciona / O que observar" dos 14 sistemas — aguardando revisão/merge do dono: https://github.com/igormorais123/INTEIA-laboratorio-3d/pull/10
- Branch local `backup/wip-textos-2026-antes-pull` no PC original (textos antigos, já incorporados à PR #10); não foi enviado ao GitHub.
- Branches remotos já incorporados à `main` e que podem ser apagados com autorização: `sistemas-3d-blender`, `sistemas-visiveis-volante-2026`, `codex/mapas-inteia`.
- Na pasta `Aula Labmota` do PC original há clones soltos de outros repositórios (`inteia-f1-loop` com 14 alterações não commitadas, e três cópias de `relogio-de-precisao`); não pertencem a este projeto.

## 9. Links

- Produção: https://laboratorio-3d-inteia.igor47306.chatgpt.site
- Repositório: https://github.com/igormorais123/INTEIA-laboratorio-3d
