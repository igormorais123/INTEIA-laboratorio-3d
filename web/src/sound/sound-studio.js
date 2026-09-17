// Aba 07 Som: seletor de motor, banco carregado sob demanda, AudioWorklet com o reprodutor de fase travada,
// editor de curva, modo livre, afinador (f0 prevista × medida) e ignição visual. O áudio só começa após um
// clique (Ligar ou Tocar), com volume inicial baixo. Falhas ficam no painel e não afetam o resto do laboratório.
import {ENGINE_PROFILES, cylinderAt, firingIntervalDeg} from './engine-profiles.mjs';
import {loadBank} from './bank-format.mjs';
import {CURVE_PRESETS, curveFromJSON, curveToJSON, presetCurve} from './rpm-curve.mjs';
import {detectFiringHz} from './pitch.mjs';
import {createEditorState, describeTuning, mountCurveEditor, setDuration, setMaxRpm, stateToCurve} from './curve-editor.js';

const STORAGE_KEY = 'inteia-som-curva-v1';
const $ = (id) => document.getElementById(id);

export const SOUND_CREDITS = Object.freeze([
  {title: 'Superleague Formula V12, Brands Hatch 2010', author: 'Ed Pond (Edvvc)', license: 'CC BY-SA 3.0', url: 'https://commons.wikimedia.org/wiki/File:Superleague_Formula_V12_Brands_Hatch_2010.ogg'},
  {title: 'Ferrari 312 (1968)', author: 'Ed Pond (Edvvc)', license: 'CC BY-SA 3.0', url: 'https://commons.wikimedia.org/wiki/File:Ferrari_312_68_(1968).ogg'},
  {title: 'Williams-Renault FW18 (1996)', author: 'Ed Pond (Edvvc)', license: 'CC BY-SA 3.0', url: 'https://commons.wikimedia.org/wiki/File:Williams-Renault_FW18_(1996).ogg'},
  {title: 'F1 2012, Melbourne (Freesound 150338 e 150337)', author: 'Ears68', license: 'CC0', url: 'https://freesound.org/s/150338/'},
  {title: 'GP da Itália 2014 (Freesound 410894)', author: 'wandererscapes', license: 'CC0', url: 'https://freesound.org/s/410894/'},
]);

function readStoredCurve() { try { const raw = localStorage.getItem(STORAGE_KEY); return raw ? curveFromJSON(raw) : null; } catch { return null; } }
function storeCurve(curve) { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(curveToJSON(curve))); } catch { /* armazenamento indisponível */ } }

export function createSoundStudio({workletSource, onEngineChange = () => {}} = {}) {
  const ui = {
    panel: $('sound-panel'), status: $('sound-status'), power: $('sound-power'), volume: $('sound-volume'), volumeValue: $('sound-volume-value'),
    modeCurve: $('sound-mode-curve'), modeFree: $('sound-mode-free'), curveBlock: $('sound-curve-block'), freeBlock: $('sound-free-block'),
    svg: $('sound-curve'), duration: $('sound-duration'), maxRpm: $('sound-maxrpm'), presets: $('sound-presets'), play: $('sound-play'), stop: $('sound-stop'), loop: $('sound-loop'), physical: $('sound-physical'), exportButton: $('sound-export'), importInput: $('sound-import'),
    throttle: $('sound-throttle'), throttleValue: $('sound-throttle-value'), fixed: $('sound-fixed'),
    tunerRpm: $('tuner-rpm'), tunerHz: $('tuner-hz'), tunerNote: $('tuner-note'), tunerMeasured: $('tuner-measured'), tunerDeviation: $('tuner-deviation'), tunerState: $('tuner-state'),
    cylinders: $('sound-cylinders'), cylinderNote: $('sound-cylinder-note'), credits: $('sound-credits-list'),
  };
  if (!ui.panel) return null;
  let engineId = 'v12_90s', profile = ENGINE_PROFILES[engineId];
  let context = null, node = null, analyser = null, workletReady = false, bankReady = false, loading = null, abort = null, disposed = false;
  let mode = 'curve', power = false, playing = false, loop = false, physical = true, throttle = 0, fixedRpm = null, volume = Number(ui.volume?.value ?? 35) / 100;
  let editorState = createEditorState(readStoredCurve() ?? presetCurve('linear'));
  let status = {rpm: 0, thetaDeg: 0, running: false, cranking: false, limiter: false, load: 0.5, t: 0};
  let visualSlot = 0, lastMeasureAt = 0, measured = null;
  const analysis = new Float32Array(2048);

  const setStatus = (text, warn = false) => { if (!ui.status) return; ui.status.textContent = text || ''; ui.status.hidden = !text; ui.status.classList.toggle('warning', warn); };
  const post = (message, transfer) => { node?.port.postMessage(message, transfer || []); };
  const pushState = (partial) => post({type: 'state', state: partial});

  // ---- editor de curva
  const editor = ui.svg ? mountCurveEditor(ui.svg, {
    getState: () => editorState, setState: (next) => { editorState = next; },
    getProfile: () => profile,
    onCommit: () => { syncCurve(); },
  }) : null;
  function syncCurve() {
    const curve = stateToCurve(editorState);
    storeCurve(curve);
    post({type: 'curve', curve: curveToJSON(curve)});
    if (ui.duration) ui.duration.value = editorState.durationS;
    if (ui.maxRpm) ui.maxRpm.value = editorState.maxRpm;
    document.querySelectorAll('#sound-presets button').forEach((b) => b.setAttribute('aria-pressed', 'false'));
  }
  if (ui.presets) {
    ui.presets.replaceChildren(...Object.entries(CURVE_PRESETS).map(([id, preset]) => {
      const button = document.createElement('button'); button.type = 'button'; button.textContent = preset.label; button.dataset.preset = id; button.setAttribute('aria-pressed', 'false');
      button.onclick = () => { editorState = createEditorState(presetCurve(id)); editor?.render(); syncCurve(); button.setAttribute('aria-pressed', 'true'); };
      return button;
    }));
  }
  if (ui.duration) ui.duration.onchange = () => { editorState = setDuration(editorState, Number(ui.duration.value)); editor?.render(); syncCurve(); };
  if (ui.maxRpm) ui.maxRpm.onchange = () => { editorState = setMaxRpm(editorState, Number(ui.maxRpm.value), profile.limitRpm); editor?.render(); syncCurve(); };
  if (ui.exportButton) ui.exportButton.onclick = () => {
    const blob = new Blob([JSON.stringify(curveToJSON(stateToCurve(editorState)), null, 2)], {type: 'application/json'});
    const url = URL.createObjectURL(blob), a = document.createElement('a'); a.href = url; a.download = 'INTEIA-curva-rpm.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 10000);
  };
  if (ui.importInput) ui.importInput.onchange = async () => {
    const file = ui.importInput.files?.[0]; if (!file) return;
    try { editorState = createEditorState(curveFromJSON(await file.text())); editor?.render(); syncCurve(); setStatus('Curva importada.'); }
    catch { setStatus('Arquivo de curva inválido.', true); }
    ui.importInput.value = '';
  };

  // ---- áudio
  async function ensureAudio() {
    if (context && workletReady) return true;
    try {
      context = context || new (window.AudioContext || window.webkitAudioContext)({sampleRate: 48000, latencyHint: 'interactive'});
      if (context.state === 'suspended') await context.resume();
      if (!workletReady) {
        if (!workletSource) throw new Error('worklet ausente no build');
        const url = URL.createObjectURL(new Blob([workletSource], {type: 'text/javascript'}));
        await context.audioWorklet.addModule(url); URL.revokeObjectURL(url);
        node = new AudioWorkletNode(context, 'inteia-engine', {numberOfInputs: 0, numberOfOutputs: 1, outputChannelCount: [1]});
        analyser = context.createAnalyser(); analyser.fftSize = 2048; analyser.smoothingTimeConstant = 0;
        node.connect(analyser); analyser.connect(context.destination);
        node.port.onmessage = (event) => onWorkletMessage(event.data);
        workletReady = true;
        pushState({mode, power, throttle, fixedRpm, physical, volume, loop});
        post({type: 'curve', curve: curveToJSON(stateToCurve(editorState))});
      }
      return true;
    } catch (error) {
      console.error(error);
      setStatus('O áudio não pôde iniciar neste navegador (AudioWorklet indisponível).', true);
      return false;
    }
  }
  function onWorkletMessage(message) {
    if (message.type === 'status') { status = message; if (window.viewerInfo) window.viewerInfo.soundStatus = message; if (message.playing !== playing) { playing = message.playing; syncButtons(); } return; }
    if (message.type === 'ready') { bankReady = true; setStatus(`${profile.label}: banco pronto.`); syncButtons(); return; }
    if (message.type === 'error') { bankReady = false; setStatus(`Banco recusado: ${message.message}`, true); syncButtons(); }
  }
  async function ensureBank() {
    if (bankReady) return true;
    if (loading) return loading;
    const wanted = engineId;
    abort?.abort(); abort = new AbortController();
    setStatus(`Carregando banco de som do ${profile.label}…`);
    loading = (async () => {
      try {
        const {bank, manifest} = await loadBank(profile.bank, {signal: abort.signal});
        if (disposed || wanted !== engineId) return false;
        if (!(await ensureAudio())) return false;
        const loops = bank.loops.map((l) => ({rpm: l.rpm, load: l.load, samplesPerCycle: l.samplesPerCycle, cycles: l.cycles, data: l.data.buffer}));
        const transfer = loops.map((l) => l.data);
        const starter = bank.starter ? bank.starter.data.buffer : null; if (starter) transfer.push(starter);
        post({type: 'bank', engine: engineId, sampleRate: bank.sampleRate, loops, starter}, transfer);
        window.viewerInfo && (window.viewerInfo.soundBank = {engine: engineId, loops: manifest.loops.length, bytes: manifest.bytes});
        return true;
      } catch (error) {
        if (error?.name === 'AbortError') return false;
        console.error(error);
        setStatus(`Não foi possível carregar o banco do ${profile.label}. Recarregue a página para tentar de novo.`, true);
        return false;
      } finally { loading = null; }
    })();
    return loading;
  }

  // ---- controles
  function syncButtons() {
    ui.power?.setAttribute('aria-pressed', String(power)); if (ui.power) ui.power.textContent = power ? 'Desligar motor' : 'Ligar motor';
    ui.play?.setAttribute('aria-pressed', String(playing)); if (ui.play) ui.play.textContent = playing ? 'Tocando…' : 'Tocar curva';
    ui.loop?.setAttribute('aria-pressed', String(loop)); ui.physical?.setAttribute('aria-pressed', String(physical));
    ui.modeCurve?.setAttribute('aria-pressed', String(mode === 'curve')); ui.modeFree?.setAttribute('aria-pressed', String(mode === 'free'));
    if (ui.curveBlock) ui.curveBlock.hidden = mode !== 'curve'; if (ui.freeBlock) ui.freeBlock.hidden = mode !== 'free';
    document.querySelectorAll('[data-sound-engine]').forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.soundEngine === engineId)));
    document.querySelectorAll('#sound-fixed button').forEach((b) => b.setAttribute('aria-pressed', String(Number(b.dataset.rpm) === fixedRpm)));
    if (window.viewerInfo) window.viewerInfo.sound = {engine: engineId, mode, power, playing, bankReady};
  }
  async function setPower(on) {
    power = on; syncButtons();
    if (on) { if (!(await ensureBank())) { power = false; syncButtons(); return; } }
    pushState({power});
  }
  async function playCurve() {
    if (!(await ensureBank())) return;
    mode = 'curve'; pushState({mode}); post({type: 'play'}); playing = true; syncButtons();
  }
  function stopCurve() { post({type: 'stop'}); playing = false; syncButtons(); }
  function setMode(next) { mode = next; pushState({mode}); if (next === 'free') stopCurve(); syncButtons(); }
  function setEngine(next) {
    if (!ENGINE_PROFILES[next] || next === engineId) return;
    stopCurve(); if (power) { power = false; pushState({power: false}); }
    engineId = next; profile = ENGINE_PROFILES[next]; bankReady = false; fixedRpm = null;
    editorState = setMaxRpm(editorState, Math.min(editorState.maxRpm, profile.limitRpm), profile.limitRpm); editor?.render(); syncCurve();
    renderCylinders(); syncButtons(); setStatus(`${profile.label} selecionado. Ligue o motor ou toque a curva para carregar o som.`);
    onEngineChange(profile);
  }
  document.querySelectorAll('[data-sound-engine]').forEach((b) => { b.onclick = () => setEngine(b.dataset.soundEngine); });
  if (ui.power) ui.power.onclick = () => setPower(!power);
  if (ui.play) ui.play.onclick = () => (playing ? stopCurve() : playCurve());
  if (ui.stop) ui.stop.onclick = () => { stopCurve(); if (power) setPower(false); };
  if (ui.loop) ui.loop.onclick = () => { loop = !loop; pushState({loop}); syncButtons(); };
  if (ui.physical) ui.physical.onclick = () => { physical = !physical; pushState({physical}); editor?.render(); syncButtons(); };
  if (ui.modeCurve) ui.modeCurve.onclick = () => setMode('curve');
  if (ui.modeFree) ui.modeFree.onclick = () => setMode('free');
  if (ui.volume) ui.volume.oninput = () => { volume = Number(ui.volume.value) / 100; if (ui.volumeValue) ui.volumeValue.textContent = `${ui.volume.value}%`; pushState({volume}); };
  if (ui.throttle) ui.throttle.oninput = () => { throttle = Number(ui.throttle.value) / 100; fixedRpm = null; if (ui.throttleValue) ui.throttleValue.textContent = `${ui.throttle.value}%`; pushState({throttle, fixedRpm}); syncButtons(); };
  if (ui.fixed) {
    ui.fixed.replaceChildren(...[['Marcha lenta', null], ['6.000', 6000], ['7.000', 7000], ['12.000', 12000]].map(([label, rpm]) => {
      const button = document.createElement('button'); button.type = 'button'; button.textContent = label; button.dataset.rpm = rpm ?? profile.idleRpm; button.setAttribute('aria-pressed', 'false');
      button.onclick = async () => { fixedRpm = rpm ?? profile.idleRpm; if (ui.throttle) { ui.throttle.value = 0; if (ui.throttleValue) ui.throttleValue.textContent = '0%'; } throttle = 0; pushState({fixedRpm, throttle}); if (!power) await setPower(true); syncButtons(); };
      return button;
    }));
  }

  // ---- ignição visual e créditos
  function renderCylinders() {
    if (!ui.cylinders) return;
    const half = profile.cylinders / 2;
    ui.cylinders.style.setProperty('--per-bank', String(half));
    ui.cylinders.replaceChildren(...Array.from({length: profile.cylinders}, (_, i) => {
      const cylinder = i + 1, cell = document.createElement('span'); cell.className = 'sound-cylinder'; cell.dataset.cylinder = String(cylinder); cell.textContent = String(cylinder);
      cell.style.gridRow = cylinder <= half ? '1' : '2'; cell.style.gridColumn = String(cylinder <= half ? cylinder : cylinder - half);
      cell.setAttribute('aria-label', `Cilindro ${cylinder}`); return cell;
    }));
    if (ui.cylinderNote) ui.cylinderNote.textContent = `Ordem de ignição ${profile.firingOrder.join('-')} · uma explosão a cada ${firingIntervalDeg(profile)}° de virabrequim.`;
  }
  if (ui.credits) {
    ui.credits.replaceChildren(...SOUND_CREDITS.map((credit) => {
      const item = document.createElement('li'), link = document.createElement('a'); link.href = credit.url; link.target = '_blank'; link.rel = 'noopener'; link.textContent = credit.title;
      item.append(link, ` — ${credit.author}, ${credit.license}`); return item;
    }));
  }
  renderCylinders();

  // ---- atualização por quadro (chamada pelo laço do laboratório)
  function update(now) {
    const rpm = status.rpm || 0;
    const {hz, note} = describeTuning(profile, rpm);
    if (ui.tunerRpm) ui.tunerRpm.textContent = rpm > 0 ? Math.round(rpm).toLocaleString('pt-BR') : '—';
    if (ui.tunerHz) ui.tunerHz.textContent = hz > 0 ? `${hz.toFixed(0)} Hz` : '—';
    if (ui.tunerNote) ui.tunerNote.textContent = note ? `${note.label} (${note.cents >= 0 ? '+' : ''}${Math.round(note.cents)} cents)` : '—';
    if (ui.tunerState) ui.tunerState.textContent = status.cranking ? 'Partida' : status.limiter ? 'Limitador' : status.running ? (status.load > 0.6 ? 'Acelerando' : status.load < 0.4 ? 'Aliviado' : 'Regime') : 'Desligado';
    if (analyser && status.running && hz > 0 && now - lastMeasureAt > 330) {
      lastMeasureAt = now; analyser.getFloatTimeDomainData(analysis);
      const pitch = detectFiringHz(analysis, context.sampleRate, {minHz: hz * 0.7, maxHz: hz * 1.4, harmonics: 4, stepRatio: 1.008});
      measured = pitch ? pitch.hz : null;
    }
    if (!status.running) measured = null;
    if (ui.tunerMeasured) ui.tunerMeasured.textContent = measured ? `${measured.toFixed(0)} Hz` : '—';
    if (ui.tunerDeviation) { const cents = measured && hz > 0 ? 1200 * Math.log2(measured / hz) : null; ui.tunerDeviation.textContent = cents === null ? '—' : `${cents >= 0 ? '+' : ''}${cents.toFixed(0)} cents`; }
    if (ui.cylinders) {
      let active = null;
      if (status.running || status.cranking) {
        if (rpm <= 1500) active = cylinderAt(profile, status.thetaDeg);
        else { visualSlot = (visualSlot + 1) % profile.cylinders; active = profile.firingOrder[visualSlot]; }
      }
      ui.cylinders.querySelectorAll('.sound-cylinder').forEach((cell) => cell.classList.toggle('firing', Number(cell.dataset.cylinder) === active));
    }
    editor?.setPlayhead(mode === 'curve' && playing ? status.t : null);
  }

  syncButtons(); syncCurve();
  return {
    update, setEngine,
    get engine() { return profile; },
    activate() { setStatus(bankReady ? `${profile.label}: banco pronto.` : `${profile.label} selecionado. Ligue o motor ou toque a curva para carregar o som.`); },
    deactivate() { if (playing) stopCurve(); if (power) setPower(false); },
    dispose() { disposed = true; abort?.abort(); node?.disconnect(); context?.close(); },
  };
}
