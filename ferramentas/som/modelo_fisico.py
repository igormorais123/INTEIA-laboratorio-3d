"""Modelo físico offline do som de motor (escape, admissão, mecânica), renderizado a 192 kHz e decimado
para 48 kHz em loops de ciclos inteiros que fecham sem emenda.

Estrutura (por rotação fixa e carga fixa, tudo linear e invariante no tempo depois da excitação, por isso
as guias de onda viram filtros IIR e o regime permanente é exatamente periódico):

- Pulso de blowdown por cilindro: subida em cosseno na abertura da válvula de escape, decaimento
  exponencial (em graus de virabrequim), mais o sopro de deslocamento do pistão até o PMS. Amplitude e
  brilho dependem da carga; variação ciclo a ciclo com semente por (ciclo mod N, cilindro).
- Primário por cilindro: guia de onda fechada na válvula e parcialmente aberta no coletor
  (ressonâncias de quarto de onda), perda passa-baixa por volta.
- Coletor por bancada → tubo final aberto (ou, no turbo, as duas bancadas → turbina passa-baixa → saída
  única) → radiação (passa-alta de 1ª ordem).
- Admissão: trompeta de quarto de onda por cilindro excitada pela sucção, ressonância Helmholtz da airbox.
- Mecânica: cliques do trem de válvulas, cascata de engrenagens (ordem = dentes) e ruído estrutural.
- Saída: saturação suave e EQ por banda (aplicada circularmente para preservar o loop).

Uso pela calibração e pelo gerador do banco; não depende do navegador.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.signal import butter, lfilter, resample_poly, sosfilt

HERE = Path(__file__).resolve().parent
FS_OUT = 48000
OVERSAMPLE = 4
FS = FS_OUT * OVERSAMPLE
WARMUP_CYCLES = 8

# Espaço de parâmetros livres: nome → (mínimo, máximo). Os valores por motor ficam em perfis/<motor>.json.
PARAM_SPACE = {
    'gasSpeed': (480.0, 720.0),          # m/s, velocidade do som no gás quente
    'primaryLength': (0.28, 0.60),        # m
    'primaryReflection': (0.25, 0.80),
    'primaryLossHz': (2500.0, 12000.0),   # passa-baixa na volta da guia
    'collectorLength': (0.30, 1.20),      # m
    'tailReflection': (0.20, 0.85),
    'tailLossHz': (1500.0, 9000.0),
    'radiationHz': (40.0, 400.0),         # passa-alta da radiação na saída
    'mouthHz': (3000.0, 16000.0),         # passa-baixa da boca/ar
    'evoDeg': (110.0, 150.0),             # abertura da válvula de escape após o PMS de ignição
    'riseDeg': (12.0, 60.0),
    'decayDeg': (25.0, 140.0),
    'displacementLevel': (0.0, 0.6),
    'pulseSkew': (0.0, 1.0),              # assimetria do pulso (0 = suave, 1 = frente abrupta)
    'intakeMix': (0.0, 0.5),
    'trumpetLength': (0.12, 0.40),        # m
    'airboxHz': (60.0, 260.0),
    'gearLevel': (0.0, 0.08),
    'gearTeeth': (18.0, 44.0),
    'valveLevel': (0.0, 0.08),
    'structureLevel': (0.0, 0.12),
    'drive': (0.3, 3.0),
    'levelPerOctaveDb': (0.0, 8.0),
    'offLoadLevel': (0.10, 0.45),
    'offLoadNoise': (0.0, 0.3),
    'turbineHz': (800.0, 4000.0),         # só motores turbo
    'turbineHiss': (0.0, 0.3),
    'bankBalance': (0.15, 1.0),           # nível da bancada distante em relação à próxima (assimetria do ouvinte)
    'bankDelayMs': (0.0, 3.0),            # atraso extra do percurso da bancada distante
    'primarySpread': (0.0, 0.10),         # dispersão de comprimento entre primários (conteúdo de meia ordem)
}
# Parâmetros que a calibração não enxerga nos alvos relativos (ficam nos valores do perfil)
UNCALIBRATED = {'gearTeeth', 'offLoadLevel', 'offLoadNoise', 'levelPerOctaveDb'}


def load_profile(engine: str) -> dict:
    return json.loads((HERE / 'perfis' / f'{engine}.json').read_text(encoding='utf-8'))


def clamp_params(params: dict) -> dict:
    out = dict(params)
    for name, (lo, hi) in PARAM_SPACE.items():
        if name in out:
            out[name] = float(min(hi, max(lo, out[name])))
    return out


def cylinder_bank(profile: dict, cylinder: int) -> int:
    return 0 if cylinder <= profile['cylinders'] // 2 else 1


def _comb(x: np.ndarray, round_trip_samples: int, reflection: float, loss_hz: float, fs: float) -> np.ndarray:
    """Guia de onda como pente IIR: y[n] = x[n] − r·LP(y)[n − D], LP de 1ª ordem com corte loss_hz.

    Calculado em blocos de D amostras (a realimentação só depende do bloco anterior), o que evita um
    denominador denso de D coeficientes no lfilter e custa O(N)."""
    d = max(2, int(round(round_trip_samples)))
    pole = float(np.exp(-2 * np.pi * loss_hz / fs))
    b, a = np.array([1 - pole]), np.array([1.0, -pole])
    y = np.empty_like(x)
    v_prev = np.zeros(d)
    zi = np.zeros(1)
    for start in range(0, len(x), d):
        end = min(len(x), start + d)
        block = x[start:end] - reflection * v_prev[:end - start]
        y[start:end] = block
        v_block, zi = lfilter(b, a, block, zi=zi)
        if end - start == d:
            v_prev = v_block
        else:
            v_prev = np.concatenate([v_block, v_prev[end - start:]])
    return y


def _delay(x: np.ndarray, samples: int) -> np.ndarray:
    d = int(round(samples))
    if d <= 0:
        return x
    return np.concatenate([np.zeros(d), x[:-d]])


def _highpass(x: np.ndarray, hz: float, fs: float, order: int = 1) -> np.ndarray:
    return sosfilt(butter(order, min(hz, fs * 0.45), 'high', fs=fs, output='sos'), x)


def _lowpass(x: np.ndarray, hz: float, fs: float, order: int = 1) -> np.ndarray:
    return sosfilt(butter(order, min(hz, fs * 0.45), 'low', fs=fs, output='sos'), x)


def _bandpass(x: np.ndarray, lo: float, hi: float, fs: float) -> np.ndarray:
    return sosfilt(butter(2, [lo, min(hi, fs * 0.45)], 'band', fs=fs, output='sos'), x)


def _periodic_noise(rng: np.random.Generator, period: int, total: int) -> np.ndarray:
    base = rng.standard_normal(period)
    return np.tile(base, total // period + 1)[:total]


def _pulse(theta: np.ndarray, rise: float, decay: float, skew: float) -> np.ndarray:
    """Forma do blowdown em função do ângulo desde a abertura (graus): subida em cosseno, decaimento exponencial."""
    rise_eff = rise * (1 - 0.7 * skew)
    up = 0.5 - 0.5 * np.cos(np.pi * np.clip(theta / rise_eff, 0, 1))
    down = np.exp(-np.clip(theta - rise_eff, 0, None) / decay)
    return up * down


def render_loop(profile: dict, params: dict, rpm: float, samples_per_cycle: int, load: str, cycles: int,
                *, warmup: int = WARMUP_CYCLES, seed: int = 0, eq_curve=None) -> np.ndarray:
    """Renderiza `cycles` ciclos de 720° a 48 kHz, começando na chegada do pulso do cilindro 1 à saída.

    `samples_per_cycle` deve ser inteiro e coerente com rpm = 120 × 48000 / samples_per_cycle.
    Retorna Float64 de comprimento samples_per_cycle × cycles. O nível relativo entre rotações e cargas é
    preservado (a normalização comum é feita pelo gerador do banco).
    """
    p = clamp_params(params)
    n_cyl = int(profile['cylinders'])
    firing_order = profile['firingOrder']
    turbo = bool(profile.get('turbo', False))
    on = load == 'on'
    spc = samples_per_cycle * OVERSAMPLE
    total_cycles = warmup + cycles
    total = spc * total_cycles
    period = spc * cycles
    deg_per_sample = 720.0 / spc
    rng = np.random.default_rng(seed)

    # ---- Excitação de escape por bancada e de admissão --------------------------------------------
    exhaust = [np.zeros(total) for _ in range(n_cyl)]      # excitação por cilindro (índice = cilindro − 1)
    intake = np.zeros(total)
    valve_clicks = np.zeros(total)
    combustion_env = np.zeros(total)
    amp_load = 1.0 if on else p['offLoadLevel']
    rise = p['riseDeg'] * (1.0 if on else 1.6)
    decay = p['decayDeg'] * (1.0 if on else 0.7)
    pulse_len = int(min(spc, (p['riseDeg'] * 2 + decay * 6) / deg_per_sample))
    theta_rel = np.arange(pulse_len) * deg_per_sample
    base_pulse = _pulse(theta_rel, rise, decay, p['pulseSkew'])
    # Sopro de deslocamento: do PMI ao PMS (180° → 360° depois da ignição), meio seno
    disp_len = int(180 / deg_per_sample)
    disp = np.sin(np.pi * np.arange(disp_len) / disp_len) * p['displacementLevel'] * amp_load
    # Sucção da admissão: do PMS de cruzamento (≈ 350°) até o PMI (540°)
    suction_len = int(190 / deg_per_sample)
    suction = -np.sin(np.pi * np.arange(suction_len) / suction_len) ** 2 * (1.0 if on else 0.35)
    click_len = int(3 / deg_per_sample) + 2
    click = np.hanning(click_len) * np.sin(np.arange(click_len) * 0.9)
    window_deg = 720.0 / n_cyl
    pop_chance = p['offLoadNoise'] * 0.5 if not on else 0.0
    for c in range(total_cycles):
        cycle_rng = np.random.default_rng([seed, c % cycles])
        for slot, cylinder in enumerate(firing_order):
            jitter_amp = 1 + 0.02 * cycle_rng.standard_normal()
            jitter_deg = 0.3 * cycle_rng.standard_normal()
            pop = cycle_rng.random() < pop_chance
            start_deg = c * 720 + slot * window_deg + jitter_deg
            evo = int(round((start_deg + p['evoDeg']) / deg_per_sample))
            amp = amp_load * jitter_amp * (3.0 if pop else 1.0)
            _add(exhaust[cylinder - 1], evo, base_pulse * amp)
            _add(exhaust[cylinder - 1], int(round((start_deg + 180) / deg_per_sample)), disp)
            _add(intake, int(round((start_deg + 350) / deg_per_sample)), suction)
            _add(combustion_env, evo, base_pulse * amp)
            # Cliques de fechamento das válvulas: escape (~ 370°) e admissão (~ 580°)
            for close_deg in (370.0, 580.0):
                _add(valve_clicks, int(round((start_deg + close_deg) / deg_per_sample)), click * (0.6 + 0.8 * cycle_rng.random()))

    # ---- Escape: primários, coletor, turbina, tubo final, radiação -----------------------------------
    c_gas = p['gasSpeed']
    primary_round = 2 * p['primaryLength'] / c_gas * FS
    collector_round = 2 * p['collectorLength'] / c_gas * FS
    spread_rng = np.random.default_rng([seed, 991])
    length_factor = 1 + p['primarySpread'] * spread_rng.uniform(-1, 1, n_cyl)
    bank_out = [np.zeros(total), np.zeros(total)]
    for cylinder in range(1, n_cyl + 1):
        round_trip = primary_round * length_factor[cylinder - 1]
        primary = _comb(exhaust[cylinder - 1], round_trip, p['primaryReflection'], p['primaryLossHz'], FS)
        bank_out[cylinder_bank(profile, cylinder)] += (1 - p['primaryReflection']) * _delay(primary, round_trip / 2)
    if turbo:
        merged = bank_out[0] + bank_out[1]
        turbine = _lowpass(merged, p['turbineHz'], FS, order=2) * 0.7
        hiss = _bandpass(_periodic_noise(rng, period, total), 1500, 12000, FS) * p['turbineHiss'] * amp_load
        flow = np.abs(_lowpass(np.abs(merged), 200, FS)) + 0.05
        tail_in = turbine + hiss * flow / max(flow.max(), 1e-9)
        tails = [tail_in]
    else:
        tails = bank_out
    radiated = np.zeros(total)
    for index, tail_in in enumerate(tails):
        tail = _comb(tail_in, collector_round, p['tailReflection'], p['tailLossHz'], FS)
        out = (1 - p['tailReflection']) * _delay(tail, collector_round / 2)
        if index == 1:   # bancada distante do ouvinte: mais fraca e atrasada
            out = p['bankBalance'] * _delay(out, p['bankDelayMs'] * 1e-3 * FS)
        radiated += out
    radiated = _highpass(radiated, p['radiationHz'], FS)
    radiated = _lowpass(radiated, p['mouthHz'], FS, order=2)

    # ---- Admissão: trompetas de quarto de onda + airbox ----------------------------------------------
    trumpet_round = 2 * p['trumpetLength'] / 343.0 * FS
    intake_wave = _comb(intake, trumpet_round, 0.6, 6000.0, FS)
    airbox = sosfilt(butter(2, [max(20.0, p['airboxHz'] * 0.7), p['airboxHz'] * 1.4], 'band', fs=FS, output='sos'), intake_wave) * 3.0
    intake_out = _highpass(intake_wave + airbox, 60.0, FS)
    intake_out = _lowpass(intake_out, 5000.0, FS, order=2)

    # ---- Mecânica ------------------------------------------------------------------------------------
    n = np.arange(total)
    crank_hz = rpm / 60.0
    gear_phase = 2 * np.pi * p['gearTeeth'] * crank_hz * n / FS
    gear = (np.sin(gear_phase) + 0.35 * np.sin(2 * gear_phase + 0.5)) * p['gearLevel']
    valves = _bandpass(valve_clicks, 2500, 9000, FS) * p['valveLevel']
    structure = _bandpass(_periodic_noise(rng, period, total), 700, 4000, FS)
    envelope = _lowpass(combustion_env, 400.0, FS)
    structure = structure * envelope / max(envelope.max(), 1e-9) * p['structureLevel']

    # ---- Mistura, nível por rotação, saturação -------------------------------------------------------
    def norm(x):
        peak = np.abs(x[spc * warmup:]).max()
        return x / peak if peak > 0 else x
    exhaust_mix = norm(radiated)
    mix = exhaust_mix + p['intakeMix'] * norm(intake_out) + gear + valves + structure
    shaped = np.tanh(mix * p['drive']) / np.tanh(p['drive'])
    level_db = p['levelPerOctaveDb'] * np.log2(rpm / profile['idleRpm'])
    shaped = shaped * 10 ** (level_db / 20) * (1.0 if on else 0.7)

    # ---- Decimação, corte do loop e alinhamento ao pulso do cilindro 1 --------------------------------
    decimated = resample_poly(shaped, 1, OVERSAMPLE, window=('kaiser', 9.0))
    loop = decimated[samples_per_cycle * warmup: samples_per_cycle * warmup + samples_per_cycle * cycles].copy()
    travel_s = (p['primaryLength'] + p['collectorLength']) / c_gas
    onset_s = p['evoDeg'] / (6.0 * rpm) + travel_s
    shift = int(round(onset_s * FS_OUT)) % len(loop)
    loop = np.roll(loop, -shift)
    if eq_curve is not None:
        loop = apply_circular_eq(loop, eq_curve)
    return loop


def _add(target: np.ndarray, start: int, pulse: np.ndarray) -> None:
    if start >= len(target):
        return
    end = min(len(target), start + len(pulse))
    if start < 0:
        pulse = pulse[-start:]
        start = 0
    target[start:end] += pulse[:end - start]


def apply_circular_eq(loop: np.ndarray, eq_curve) -> np.ndarray:
    """Aplica uma curva de ganho (dB em função de Hz) por multiplicação circular no domínio da frequência."""
    hz_knots, db_knots = eq_curve
    spectrum = np.fft.rfft(loop)
    freqs = np.fft.rfftfreq(len(loop), 1 / FS_OUT)
    gain_db = np.interp(np.log2(np.maximum(freqs, 1.0)), np.log2(np.maximum(hz_knots, 1.0)), db_knots)
    return np.fft.irfft(spectrum * 10 ** (gain_db / 20), n=len(loop))


def render_starter(profile: dict, params: dict, *, seconds: float = 1.0, seed: int = 7) -> np.ndarray:
    """Motor de arranque: zunido com engrenamento e pulsos de compressão sem combustão a 280 RPM (loop fechado)."""
    p = clamp_params(params)
    rpm = 280.0
    cycle_samples = int(round(120 * FS_OUT / rpm))
    cycles = max(1, int(round(seconds * rpm / 120)))
    total = cycle_samples * cycles
    n = np.arange(total)
    rng = np.random.default_rng(seed)
    motor_hz = 95.0
    whine = 0.25 * np.sin(2 * np.pi * motor_hz * n / FS_OUT) + 0.12 * np.sin(2 * np.pi * motor_hz * 8 * n / FS_OUT + 0.3) + 0.06 * np.sin(2 * np.pi * motor_hz * 16 * n / FS_OUT)
    thumps = np.zeros(total)
    window = 720.0 / profile['cylinders']
    deg_per_sample = 720.0 / cycle_samples
    length = int(40 / deg_per_sample)
    shape = np.sin(np.pi * np.arange(length) / length) ** 2
    for c in range(cycles):
        for slot in range(profile['cylinders']):
            start = int(round((c * 720 + slot * window) / deg_per_sample))
            _add(thumps, start, shape * (0.5 + 0.3 * rng.random()))
    thumps = _bandpass(thumps, 40, 400, FS_OUT)
    noise = _bandpass(_periodic_noise(rng, total, total), 300, 3000, FS_OUT) * 0.05
    loop = whine * (1 + 0.15 * np.sin(2 * np.pi * rpm / 60 * n / FS_OUT)) + thumps + noise
    return loop / np.abs(loop).max()
