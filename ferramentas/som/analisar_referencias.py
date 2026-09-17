"""Order tracking das gravações de referência → alvos-timbre.json.

Para cada referência (cache mono 48 kHz de decodificar.py):
1. STFT (Hann 8192, salto 1024).
2. Candidatos de frequência de ignição f0 = RPM/60 × cilindros/2 para 3.000–19.000 RPM; pontuação por
   soma harmônica em excesso ao piso de ruído, com penalidade nas meias ordens (evita erro de oitava).
3. Rastreamento por Viterbi (continuidade em log f0) e filtro de estabilidade (variação < 3 % em 5 quadros,
   relação harmônico/ruído > 6 dB) — descarta público, locutor, helicóptero e trocas de marcha.
4. Em cada quadro aceito: nível em dB das ordens de virabrequim 0,5…60 (passo 0,5) relativo à ordem de
   ignição, piso de ruído e inclinação espectral.
5. Compensação de distância entre fontes da mesma classe (remove a diferença de inclinação em relação à
   mediana da classe; o valor removido fica registrado) e agregação por faixas de 1.000 RPM (mediana).

Só saem números; nenhum trecho de áudio é gravado.
Uso: python ferramentas/som/analisar_referencias.py
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import median_filter
from scipy.signal import get_window

HERE = Path(__file__).resolve().parent
SR = 48000
NFFT = 8192
HOP = 1024
RPM_MIN, RPM_MAX = 3000, 19000
BAND_RPM = 1000
ORDERS = np.round(np.arange(0.5, 60.01, 0.5), 1)
HARMONICS_SCORE = 8
CANDIDATE_STEP = 1.004
SCORE_HALF_PENALTY = 0.7
VITERBI_LAMBDA_DB = 100.0      # 1 % de variação de f0 entre quadros custa 1 dB
VITERBI_MAX_JUMP = 0.08
STABLE_WINDOW = 5
STABLE_MAX_VARIATION = 0.03
MIN_HNR_DB = 6.0
MIN_SCORE_DB = 8.0
MAX_ANALYSIS_HZ = 16000.0      # prévias MP3/Ogg não têm conteúdo confiável acima disso
MIN_FRAMES_PER_SOURCE = 50
MIN_FRAMES_PER_BAND = 5
ENGINE_CLASSES = {'superleague_v12': 'V12', 'ferrari_312_v12': 'V12', 'williams_v10': 'V10',
                  'ears68_v8_a': 'V8', 'ears68_v8_b': 'V8', 'monza2014_v6': 'V6'}
CYLINDERS = {'V12': 12, 'V10': 10, 'V8': 8, 'V6': 6}
# Coletor por bancada (ordem de bancada = cilindros/4 forte) ou bancadas unidas numa turbina (só a ordem de ignição)
BANK_COLLECTOR = {12: True, 10: True, 8: True, 6: False}


def stft_db(signal: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Espectrograma em dB (quadros × bins) e eixo de frequências."""
    window = get_window('hann', NFFT, fftbins=True)
    n_frames = 1 + max(0, (len(signal) - NFFT) // HOP)
    frames = np.lib.stride_tricks.as_strided(
        np.ascontiguousarray(signal, dtype=np.float32), shape=(n_frames, NFFT),
        strides=(signal.strides[0] * HOP, signal.strides[0]))
    spectrum = np.fft.rfft(frames * window, axis=1)
    magnitude = 20 * np.log10(np.abs(spectrum) / (NFFT / 4) + 1e-12)
    return magnitude.astype(np.float32), np.fft.rfftfreq(NFFT, 1 / SR)


def noise_floor(spectrogram: np.ndarray) -> np.ndarray:
    """Piso por mediana móvel em frequência (101 bins ≈ 590 Hz)."""
    return median_filter(spectrogram, size=(1, 101), mode='nearest')


def crank_candidates() -> np.ndarray:
    """Candidatos de frequência do virabrequim (Hz) em passo geométrico, de RPM_MIN a RPM_MAX."""
    f_lo, f_hi = RPM_MIN / 60, RPM_MAX / 60
    n = int(np.ceil(np.log(f_hi / f_lo) / np.log(CANDIDATE_STEP))) + 1
    return f_lo * CANDIDATE_STEP ** np.arange(n)


def engine_orders(cylinders: int) -> tuple[np.ndarray, np.ndarray]:
    """Ordens fortes e ordens de penalidade de um motor em V de duas bancadas.

    Com coletor por bancada, cada bancada dispara a cada 720°/(cilindros/2), logo a ordem de bancada é
    cilindros/4 e suas múltiplas (inclusive a ordem de ignição, cilindros/2) concentram a energia. Quando as
    bancadas se unem numa turbina (V6 turbo), só as múltiplas da ordem de ignição contam. As ordens a meio
    caminho são fracas num motor regular e rejeitam o erro de oitava (candidato em 2× a frequência real).
    """
    base = cylinders / 4 if BANK_COLLECTOR.get(cylinders, True) else cylinders / 2
    strong = base * np.arange(1, HARMONICS_SCORE + 1)
    weak = base * (np.arange(1, HARMONICS_SCORE + 1) - 0.5)
    return strong, weak


def _interp_rows(spectrogram: np.ndarray, freqs: np.ndarray, targets: np.ndarray) -> np.ndarray:
    """Interpola cada linha do espectrograma nas frequências alvo (mesmas para todas as linhas)."""
    idx = np.clip(targets / (freqs[1] - freqs[0]), 0, len(freqs) - 1.001)
    lo = np.floor(idx).astype(int)
    frac = (idx - lo).astype(np.float32)
    return spectrogram[:, lo] * (1 - frac) + spectrogram[:, lo + 1] * frac


def score_candidates(spectrogram: np.ndarray, floor: np.ndarray, freqs: np.ndarray, candidates: np.ndarray, cylinders: int) -> np.ndarray:
    """Pontuação (dB) de cada candidato de virabrequim em cada quadro: excesso nas ordens fortes menos penalidade nas fracas."""
    excess = np.maximum(spectrogram - floor, 0)
    strong, weak = engine_orders(cylinders)
    strong_hz = (candidates[:, None] * strong[None, :]).ravel()
    weak_hz = (candidates[:, None] * weak[None, :]).ravel()
    valid = (strong_hz < MAX_ANALYSIS_HZ).reshape(len(candidates), -1)
    h = _interp_rows(excess, freqs, strong_hz).reshape(len(spectrogram), len(candidates), -1)
    s = _interp_rows(excess, freqs, weak_hz).reshape(len(spectrogram), len(candidates), -1)
    weight = valid.astype(np.float32)
    count = np.maximum(weight.sum(axis=1), 1)
    return (h * weight).sum(axis=2) / count - SCORE_HALF_PENALTY * (s * weight).sum(axis=2) / count


def viterbi_track(scores: np.ndarray, candidates: np.ndarray) -> np.ndarray:
    """Caminho de máxima pontuação com custo de transição proporcional a |Δ log f0|."""
    log_f = np.log(candidates)
    delta = np.abs(log_f[:, None] - log_f[None, :])
    transition = np.where(delta <= np.log1p(VITERBI_MAX_JUMP), -VITERBI_LAMBDA_DB * delta, -np.inf).astype(np.float32)
    n_frames, n_states = scores.shape
    back = np.zeros((n_frames, n_states), dtype=np.int32)
    cost = scores[0].copy()
    for t in range(1, n_frames):
        total = cost[:, None] + transition           # de i (linha) para j (coluna)
        back[t] = total.argmax(axis=0)
        cost = total.max(axis=0) + scores[t]
    path = np.zeros(n_frames, dtype=np.int32)
    path[-1] = int(cost.argmax())
    for t in range(n_frames - 1, 0, -1):
        path[t - 1] = back[t, path[t]]
    return path


ENBW_BINS = 1.5  # largura equivalente de ruído da janela Hann, em bins


def order_level(row_power: np.ndarray, floor_power: np.ndarray, bin_width: float, hz: float, smear_bins: float) -> tuple[float, float]:
    """Nível (dB) de uma ordem por soma de potência numa janela que cobre o lóbulo principal e o espalhamento
    do chirp, descontado o piso. Para um tom estável a soma sobre o lóbulo da Hann vale pico² × ENBW."""
    half = max(2, int(np.ceil(smear_bins / 2 + 1.5)))
    center = int(round(hz / bin_width))
    lo, hi = max(1, center - half), min(len(row_power) - 1, center + half + 1)
    window = row_power[lo:hi]
    floor = float(floor_power[lo:hi].mean())
    power = float(max(window.sum() - floor * len(window), floor * ENBW_BINS * 0.1))
    return 10 * np.log10(power / ENBW_BINS + 1e-30), 10 * np.log10(floor + 1e-30)


def measure_frame(row: np.ndarray, floor_row: np.ndarray, freqs: np.ndarray, f0: float, cylinders: int, f0_slope_per_frame: float = 0.0) -> dict | None:
    """Níveis das ordens de virabrequim (dB relativo à ordem de ignição), piso, HNR e inclinações.
    `f0_slope_per_frame` é a variação de f0 (Hz) ao longo de um quadro, para alargar a janela em rampas."""
    crank_hz = f0 / (cylinders / 2)
    firing_order = cylinders / 2
    bin_width = freqs[1] - freqs[0]
    row_power = 10 ** (row.astype(np.float64) / 10)
    floor_power = 10 ** (floor_row.astype(np.float64) / 10)
    crank_slope = abs(f0_slope_per_frame) / (cylinders / 2)
    levels, floors = {}, {}
    for order in ORDERS:
        hz = order * crank_hz
        if hz >= MAX_ANALYSIS_HZ or hz < 2 * bin_width:
            continue
        level, floor = order_level(row_power, floor_power, bin_width, hz, order * crank_slope / bin_width)
        levels[order] = level
        floors[order] = floor
    if firing_order not in levels:
        return None
    reference = levels[firing_order]
    harmonics = [k * firing_order for k in range(1, HARMONICS_SCORE + 1) if k * firing_order in levels]
    if len(harmonics) < 3:
        return None
    harmonic_power = sum(10 ** (levels[o] / 10) for o in harmonics)
    floor_power_sum = sum(10 ** (floors[o] / 10) for o in harmonics)
    hnr = 10 * np.log10(harmonic_power / max(floor_power_sum, 1e-20))
    # Inclinação (dB/oitava) dos harmônicos da ignição por regressão em log2(f)
    xs = np.log2([o * crank_hz for o in harmonics])
    ys = np.array([levels[o] - reference for o in harmonics])
    tilt = float(np.polyfit(xs, ys, 1)[0]) if len(xs) >= 3 else 0.0
    high = [(o, levels[o] - reference) for o in harmonics if o * crank_hz >= 4000]
    tilt_high = float(np.polyfit(np.log2([o * crank_hz for o, _ in high]), [v for _, v in high], 1)[0]) if len(high) >= 3 else None
    between = [floors[o] - reference for o in levels if not float(o).is_integer()]
    return {
        'f0': f0, 'rpm': f0 * 60 / (cylinders / 2), 'hnr': float(hnr), 'level': float(reference),
        'orders': {float(o): float(levels[o] - reference) for o in levels},
        'noiseFloorDb': float(np.median(between)) if between else float('nan'),
        'tiltDbPerOct': tilt, 'tiltHighDbPerOct': tilt_high,
    }


def analyse_signal(signal: np.ndarray, cylinders: int) -> dict:
    """Rastreia f0 e mede os quadros estáveis de um sinal mono 48 kHz."""
    spectrogram, freqs = stft_db(signal)
    if len(spectrogram) < STABLE_WINDOW:
        return {'frames': [], 'framesTotal': int(len(spectrogram)), 'reason': 'sinal curto demais'}
    floor = noise_floor(spectrogram)
    candidates = crank_candidates()
    scores = score_candidates(spectrogram, floor, freqs, candidates, cylinders)
    path = viterbi_track(scores, candidates)
    f0_track = candidates[path] * (cylinders / 2)      # frequência de ignição
    frame_scores = scores[np.arange(len(path)), path]
    # Estabilidade: variação relativa máxima dentro de uma janela de 5 quadros centrada
    half = STABLE_WINDOW // 2
    stable = np.zeros(len(path), dtype=bool)
    for t in range(half, len(path) - half):
        window = f0_track[t - half:t + half + 1]
        stable[t] = (window.max() / window.min() - 1) < STABLE_MAX_VARIATION
    frames = []
    frame_slope = np.gradient(f0_track) * (NFFT / HOP)      # variação de f0 ao longo de um quadro
    for t in np.flatnonzero(stable & (frame_scores >= MIN_SCORE_DB)):
        measured = measure_frame(spectrogram[t], floor[t], freqs, float(f0_track[t]), cylinders, float(frame_slope[t]))
        if measured is None or measured['hnr'] < MIN_HNR_DB:
            continue
        measured['frame'] = int(t)
        measured['score'] = float(frame_scores[t])
        frames.append(measured)
    return {'frames': frames, 'framesTotal': int(len(spectrogram)), 'track': f0_track, 'scores': frame_scores}


def band_index(rpm: float) -> int:
    return int((rpm - RPM_MIN) // BAND_RPM)


def aggregate_bands(frames: list[dict]) -> list[dict]:
    bands = []
    for b in range((RPM_MAX - RPM_MIN) // BAND_RPM):
        lo, hi = RPM_MIN + b * BAND_RPM, RPM_MIN + (b + 1) * BAND_RPM
        members = [f for f in frames if lo <= f['rpm'] < hi]
        if len(members) < MIN_FRAMES_PER_BAND:
            continue
        orders = {}
        for order in ORDERS:
            values = [f['orders'][float(order)] for f in members if float(order) in f['orders']]
            if len(values) >= max(3, len(members) // 2):
                orders[str(order)] = round(float(np.median(values)), 2)
        highs = [f['tiltHighDbPerOct'] for f in members if f['tiltHighDbPerOct'] is not None]
        bands.append({
            'rpmMin': lo, 'rpmMax': hi, 'frames': len(members), 'extrapolated': False,
            'ordersDb': orders,
            'noiseFloorDb': round(float(np.nanmedian([f['noiseFloorDb'] for f in members])), 2),
            'tiltDbPerOct': round(float(np.median([f['tiltDbPerOct'] for f in members])), 3),
            'tiltHighDbPerOct': round(float(np.median(highs)), 3) if highs else None,
            'hnrDb': round(float(np.median([f['hnr'] for f in members])), 2),
        })
    return bands


def compensate_distance(class_frames: dict[str, list[dict]]) -> dict[str, float]:
    """Remove, por fonte, a diferença de inclinação alta em relação à mediana da classe (ar/distância)."""
    removed = {}
    tilts = {}
    for source, frames in class_frames.items():
        highs = [f['tiltHighDbPerOct'] for f in frames if f['tiltHighDbPerOct'] is not None]
        if highs:
            tilts[source] = float(np.median(highs))
    if len(tilts) < 2:
        return {source: 0.0 for source in class_frames}
    reference = float(np.median(list(tilts.values())))
    for source, frames in class_frames.items():
        delta = tilts.get(source, reference) - reference
        removed[source] = round(delta, 3)
        if abs(delta) < 1e-6:
            continue
        for frame in frames:
            for order, value in frame['orders'].items():
                hz = order * frame['f0'] / frame['_firing_order']
                if hz >= 4000:
                    frame['orders'][order] = value - delta * np.log2(hz / 4000)
            frame['tiltDbPerOct'] -= delta * 0.5
            if frame['tiltHighDbPerOct'] is not None:
                frame['tiltHighDbPerOct'] -= delta
    return removed


def extrapolate_bands(v12_bands: list[dict], v8_bands: list[dict], v10_bands: list[dict], top_rpm: int = 17000, firing_order: float = 6.0) -> list[dict]:
    """Bandas acima do observado: forma da última banda medida com a tendência de inclinação do V8/V10."""
    if not v12_bands:
        return []
    last = v12_bands[-1]
    high_trend = [b for b in (v8_bands + v10_bands) if b['rpmMin'] >= 10000 and b['tiltDbPerOct'] is not None]
    slope_per_1000 = 0.0
    if len(high_trend) >= 2:
        xs = np.array([(b['rpmMin'] + b['rpmMax']) / 2 for b in high_trend])
        ys = np.array([b['tiltDbPerOct'] for b in high_trend])
        slope_per_1000 = float(np.polyfit(xs / 1000, ys, 1)[0])
    extra = []
    for lo in range(last['rpmMax'], top_rpm, BAND_RPM):
        steps = (lo - last['rpmMin']) / BAND_RPM
        orders = {}
        for order, value in last['ordersDb'].items():
            o = float(order)
            octave = np.log2(max(o, 0.5) / firing_order)
            orders[order] = round(value + slope_per_1000 * steps * octave, 2)
        extra.append({'rpmMin': lo, 'rpmMax': lo + BAND_RPM, 'frames': 0, 'extrapolated': True, 'ordersDb': orders,
                      'noiseFloorDb': last['noiseFloorDb'], 'tiltDbPerOct': round(last['tiltDbPerOct'] + slope_per_1000 * steps, 3),
                      'tiltHighDbPerOct': last['tiltHighDbPerOct'], 'hnrDb': last['hnrDb'],
                      'basis': f"forma da banda {last['rpmMin']}–{last['rpmMax']} + {slope_per_1000:.3f} dB/oit por 1.000 RPM (tendência V8/V10)"})
    return extra


def main() -> int:
    sys.path.insert(0, str(HERE))
    from decodificar import load_cached
    manifest = json.loads((HERE / 'referencias.json').read_text(encoding='utf-8'))
    class_frames: dict[str, dict[str, list[dict]]] = {c: {} for c in CYLINDERS}
    sources, rejected = [], []
    for reference in manifest['references']:
        engine_class = ENGINE_CLASSES[reference['id']]
        cylinders = CYLINDERS[engine_class]
        signal, meta = load_cached(reference['id'])
        result = analyse_signal(signal, cylinders)
        frames = result['frames']
        for frame in frames:
            frame['_firing_order'] = cylinders / 2
        rpms = [f['rpm'] for f in frames]
        summary = {'id': reference['id'], 'class': engine_class, 'sha256': reference['sha256'], 'framesTotal': result['framesTotal'],
                   'framesAccepted': len(frames), 'rpmRange': [round(min(rpms)), round(max(rpms))] if rpms else None}
        print(f"{reference['id']:>18} ({engine_class}): {len(frames)}/{result['framesTotal']} quadros aceitos"
              + (f", {summary['rpmRange'][0]}–{summary['rpmRange'][1]} RPM" if rpms else ''))
        if len(frames) < MIN_FRAMES_PER_SOURCE:
            rejected.append({**summary, 'reason': f'menos de {MIN_FRAMES_PER_SOURCE} quadros estáveis com HNR > {MIN_HNR_DB} dB'})
            continue
        sources.append(summary)
        class_frames[engine_class][reference['id']] = frames
    classes = {}
    removed_all = {}
    for engine_class, per_source in class_frames.items():
        if not per_source:
            continue
        removed_all[engine_class] = compensate_distance(per_source)
        frames = [f for frames in per_source.values() for f in frames]
        classes[engine_class] = {'cylinders': CYLINDERS[engine_class], 'sources': list(per_source), 'bands': aggregate_bands(frames)}
    v8_bands, v10_bands = classes.get('V8', {}).get('bands', []), classes.get('V10', {}).get('bands', [])
    if 'V12' in classes:
        classes['V12']['bands'] += extrapolate_bands(classes['V12']['bands'], v8_bands, v10_bands, 17000, 6.0)
    if 'V6' in classes:
        # Poucos quadros de V6: as bandas ausentes até 15.000 RPM seguem a forma da última medida + tendência do V8
        measured = [b for b in classes['V6']['bands'] if b['frames'] >= 20]
        extra = extrapolate_bands(measured, v8_bands, v10_bands, 15000, 3.0)
        have = {b['rpmMin'] for b in classes['V6']['bands']}
        classes['V6']['bands'] = sorted(classes['V6']['bands'] + [b for b in extra if b['rpmMin'] not in have], key=lambda b: b['rpmMin'])
    output = {
        'version': 1, 'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'method': {'sampleRate': SR, 'nfft': NFFT, 'hop': HOP, 'orders': [float(ORDERS[0]), float(ORDERS[-1]), 0.5],
                   'reference': 'nível da ordem de ignição (cilindros/2) = 0 dB', 'stability': f'< {STABLE_MAX_VARIATION*100:.0f} % em {STABLE_WINDOW} quadros',
                   'minHnrDb': MIN_HNR_DB, 'maxAnalysisHz': MAX_ANALYSIS_HZ, 'distanceCompensation': 'diferença de inclinação acima de 4 kHz em relação à mediana da classe, removida por fonte'},
        'sources': sources, 'rejectedSources': rejected, 'distanceTiltRemovedDbPerOct': removed_all, 'classes': classes,
    }
    (HERE / 'alvos-timbre.json').write_text(json.dumps(output, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for engine_class, data in classes.items():
        bands = ', '.join(f"{b['rpmMin']//1000}k:{b['frames']}{'*' if b['extrapolated'] else ''}" for b in data['bands'])
        print(f"{engine_class}: {bands}")
    print(f"alvos-timbre.json gravado ({len(sources)} fontes, {len(rejected)} rejeitadas)")
    return 0


if __name__ == '__main__':
    sys.exit(main())
