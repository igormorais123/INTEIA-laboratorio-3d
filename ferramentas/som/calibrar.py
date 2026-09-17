"""Calibra o modelo físico pelos alvos de timbre (alvos-timbre.json).

Etapa 1 — parâmetros físicos globais: evolução diferencial (scipy) minimiza a distância log-espectral entre
as ordens do render e as do alvo, em várias faixas de RPM ao mesmo tempo. O medidor é o mesmo da análise
das gravações (measure_frame), então render e alvo passam pela mesma régua.

Etapa 2 — EQ suave por ponto do banco: para cada rotação do banco, o resíduo restante nas ordens harmônicas
vira uma curva de ganho com poucos nós em log-frequência (limitada a ±8 dB), aplicada circularmente ao loop.

Saída: perfis/<motor>.json (parâmetros finais) e calibracao-<motor>.json (distâncias por banda, EQ por
ponto e o limite de aceite = maior distância + 0,5 dB, usado como teste de regressão).

Uso: python ferramentas/som/calibrar.py v12_90s [--rapido]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import differential_evolution

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analisar_referencias import BANK_COLLECTOR, ORDERS, measure_frame, noise_floor, stft_db  # noqa: E402
from modelo_fisico import FS_OUT, PARAM_SPACE, UNCALIBRATED, apply_circular_eq, load_profile, render_loop  # noqa: E402

CALIBRATION_SECONDS = 0.25      # duração mínima dos loops durante a otimização
EQ_KNOTS_HZ = np.array([150.0, 400.0, 1000.0, 2500.0, 6000.0, 14000.0])
EQ_LIMIT_DB = 8.0
BANK_STEP = 1.08                # progressão geométrica dos pontos de RPM do banco


def bank_points(profile: dict) -> list[tuple[float, int]]:
    """Pontos (rpm exato, amostras por ciclo) do banco: passo geométrico de 8 % da marcha lenta ao limite."""
    points = []
    rpm = float(profile['idleRpm'])
    while True:
        last = rpm >= profile['limitRpm']
        spc = int(np.floor(120 * FS_OUT / rpm)) if last else int(round(120 * FS_OUT / rpm))   # último ponto nunca abaixo do limite
        exact = 120 * FS_OUT / spc
        if not points or spc != points[-1][1]:
            points.append((exact, spc))
        if rpm >= profile['limitRpm']:
            break
        rpm = min(rpm * BANK_STEP, float(profile['limitRpm']))
    return points


def loop_cycles(spc: int, seconds: float) -> int:
    return int(np.ceil(seconds * FS_OUT / spc))


def measure_loop(loop: np.ndarray, rpm: float, cylinders: int) -> dict | None:
    """Ordens do loop com a mesma régua da análise (espectro médio de ≥ 1,2 s do loop repetido)."""
    reps = int(np.ceil(0.8 * FS_OUT / len(loop))) + 1
    tiled = np.tile(loop, reps).astype(np.float32)
    spectrogram, freqs = stft_db(tiled)
    mean_row = spectrogram.mean(axis=0, keepdims=True)      # loop periódico: os quadros são quase iguais
    floor = noise_floor(mean_row)
    return measure_frame(mean_row[0], floor[0], freqs, rpm / 60 * cylinders / 2, cylinders)


def harmonic_orders(cylinders: int) -> np.ndarray:
    base = cylinders / 4 if BANK_COLLECTOR.get(cylinders, True) else cylinders / 2
    return np.round(base * np.arange(1, int(60 / base) + 1), 1)


def target_at(bands: list[dict], rpm: float) -> tuple[dict, float]:
    """Interpola os alvos entre os centros das duas bandas vizinhas; fora do intervalo usa a mais próxima."""
    centers = np.array([(b['rpmMin'] + b['rpmMax']) / 2 for b in bands])
    if rpm <= centers[0]:
        return bands[0]['ordersDb'], bands[0]['noiseFloorDb']
    if rpm >= centers[-1]:
        return bands[-1]['ordersDb'], bands[-1]['noiseFloorDb']
    hi = int(np.searchsorted(centers, rpm))
    lo = hi - 1
    w = (rpm - centers[lo]) / (centers[hi] - centers[lo])
    a, b = bands[lo]['ordersDb'], bands[hi]['ordersDb']
    orders = {k: (1 - w) * a[k] + w * b[k] for k in a if k in b}
    return orders, (1 - w) * bands[lo]['noiseFloorDb'] + w * bands[hi]['noiseFloorDb']


def _smooth3(values: np.ndarray) -> np.ndarray:
    if len(values) < 3:
        return values
    padded = np.concatenate([[values[0]], values, [values[-1]]])
    return np.median(np.stack([padded[:-2], padded[1:-1], padded[2:]]), axis=0)


def distance(render: dict, target: dict, floor_db: float, cylinders: int) -> dict:
    """Distância em dB: RMS nas ordens harmônicas (suavizadas em 3 pontos) + dobradiça nas demais ordens."""
    harmonics = harmonic_orders(cylinders)
    pairs = [(o, render['orders'][float(o)], target[str(o)]) for o in harmonics
             if float(o) in render['orders'] and str(o) in target]
    if len(pairs) < 4:
        return {'total': 60.0, 'harmonic': 60.0, 'hinge': 0.0, 'orders': 0}
    r = _smooth3(np.array([p[1] for p in pairs]))
    t = _smooth3(np.array([p[2] for p in pairs]))
    # Alvos afogados no piso da gravação são limites superiores, não valores
    limit = np.array([p[2] <= floor_db + 3 for p in pairs])
    diff = r - t
    diff = np.where(limit, np.maximum(diff, 0), diff)
    harmonic = float(np.sqrt(np.mean(diff ** 2)))
    others = [(render['orders'][float(o)], target[str(o)]) for o in ORDERS
              if float(o) in render['orders'] and str(o) in target and o not in harmonics]
    hinge = float(np.sqrt(np.mean([max(0.0, rv - tv) ** 2 for rv, tv in others]))) if others else 0.0
    return {'total': float(np.sqrt(harmonic ** 2 + (0.5 * hinge) ** 2)), 'harmonic': harmonic, 'hinge': hinge, 'orders': len(pairs)}


def calibration_bands(bands: list[dict], idle_rpm: float = 0.0) -> list[tuple[dict, float]]:
    """Bandas usadas na otimização e seus pesos: nada abaixo da marcha lenta; das extrapoladas, só a primeira e a última."""
    chosen = []
    extrapolated = [b for b in bands if b['extrapolated']]
    keep_extra = {id(extrapolated[0]), id(extrapolated[-1])} if extrapolated else set()
    for band in bands:
        if (band['rpmMin'] + band['rpmMax']) / 2 < idle_rpm:
            continue
        if band['extrapolated']:
            if id(band) not in keep_extra:
                continue
            weight = 0.5
        elif band['frames'] >= 20:
            weight = 1.0
        elif band['frames'] >= 5:
            weight = 0.6
        else:
            continue
        chosen.append((band, weight))
    return chosen


class Objective:
    def __init__(self, profile: dict, bands: list[dict], names: list[str], fixed: dict, seconds: float):
        self.profile, self.names, self.fixed, self.seconds = profile, names, fixed, seconds
        self.bands = calibration_bands(bands, float(profile['idleRpm']))
        self.cylinders = int(profile['cylinders'])

    def params(self, vector: np.ndarray) -> dict:
        p = dict(self.fixed)
        p.update({name: float(v) for name, v in zip(self.names, vector)})
        return p

    def per_band(self, params: dict, seconds: float | None = None) -> list[dict]:
        seconds = seconds or self.seconds
        out = []
        for band, weight in self.bands:
            rpm_center = (band['rpmMin'] + band['rpmMax']) / 2
            spc = int(round(120 * FS_OUT / rpm_center))
            rpm = 120 * FS_OUT / spc
            loop = render_loop(self.profile, params, rpm, spc, 'on', loop_cycles(spc, seconds), warmup=6)
            measured = measure_loop(loop, rpm, self.cylinders)
            d = distance(measured, band['ordersDb'], band['noiseFloorDb'], self.cylinders) if measured else {'total': 60.0, 'harmonic': 60.0, 'hinge': 0.0, 'orders': 0}
            out.append({'rpmMin': band['rpmMin'], 'rpmMax': band['rpmMax'], 'weight': weight, 'extrapolated': band['extrapolated'], **d})
        return out

    def __call__(self, vector: np.ndarray) -> float:
        rows = self.per_band(self.params(vector))
        return float(sum(r['total'] * r['weight'] for r in rows) / sum(r['weight'] for r in rows))


def fit_eq(residual_hz: np.ndarray, residual_db: np.ndarray, ridge: float = 2.0) -> np.ndarray:
    """Ajusta ganhos nos nós (log-Hz) por mínimos quadrados regularizados; interpolação linear entre nós."""
    log_knots = np.log2(EQ_KNOTS_HZ)
    x = np.log2(np.maximum(residual_hz, 1.0))
    basis = np.zeros((len(x), len(log_knots)))
    for i, xi in enumerate(x):
        j = int(np.clip(np.searchsorted(log_knots, xi) - 1, 0, len(log_knots) - 2))
        w = (xi - log_knots[j]) / (log_knots[j + 1] - log_knots[j])
        w = float(np.clip(w, 0, 1))
        basis[i, j], basis[i, j + 1] = 1 - w, w
    a = basis.T @ basis + ridge * np.eye(len(log_knots))
    gains = np.linalg.solve(a, basis.T @ residual_db)
    return np.clip(gains, -EQ_LIMIT_DB, EQ_LIMIT_DB)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('engine')
    parser.add_argument('--rapido', action='store_true', help='menos gerações (verificação do fluxo)')
    parser.add_argument('--sem-otimizar', action='store_true', help='pula a evolução diferencial; só EQ e relatório')
    parser.add_argument('--workers', type=int, default=12)
    args = parser.parse_args()

    profile = load_profile(args.engine)
    targets = json.loads((HERE / 'alvos-timbre.json').read_text(encoding='utf-8'))
    bands = targets['classes'][profile['targetClass']]['bands']
    cylinders = int(profile['cylinders'])
    skip = set(UNCALIBRATED) | (set() if profile.get('turbo') else {'turbineHz', 'turbineHiss'})
    names = [n for n in PARAM_SPACE if n not in skip]
    fixed = {n: profile['params'][n] for n in profile['params'] if n in skip}
    objective = Objective(profile, bands, names, fixed, CALIBRATION_SECONDS)
    x0 = np.array([profile['params'][n] for n in names])
    bounds = [PARAM_SPACE[n] for n in names]
    started = time.time()
    before = objective(x0)
    print(f"{args.engine}: {len(names)} parâmetros, {len(objective.bands)} bandas; distância inicial {before:.2f} dB")
    if not args.sem_otimizar:
        result = differential_evolution(
            objective, bounds, x0=x0, seed=1, popsize=6 if args.rapido else 8, maxiter=4 if args.rapido else 30,
            tol=1e-3, mutation=(0.5, 1.0), recombination=0.7, polish=False, updating='deferred',
            workers=args.workers, disp=True)
        best = result.x
        print(f"evolução diferencial: {result.nfev} avaliações, distância {result.fun:.2f} dB em {time.time() - started:.0f} s")
    else:
        best = x0
    params = objective.params(best)
    profile['params'] = {**profile['params'], **params}
    (HERE / 'perfis' / f'{args.engine}.json').write_text(json.dumps(profile, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # Etapa 2: EQ por ponto do banco e relatório por banda com loops completos
    points = bank_points(profile)
    eq_by_point = []
    for rpm, spc in points:
        loop = render_loop(profile, params, rpm, spc, 'on', loop_cycles(spc, 0.6))
        measured = measure_loop(loop, rpm, cylinders)
        target, floor_db = target_at(bands, rpm)
        harmonics = harmonic_orders(cylinders)
        crank_hz = rpm / 60
        hz, res = [], []
        for o in harmonics:
            if float(o) in measured['orders'] and str(o) in target and target[str(o)] > floor_db + 3:
                hz.append(o * crank_hz)
                res.append(target[str(o)] - measured['orders'][float(o)])
        gains = fit_eq(np.array(hz), np.array(res)) if len(hz) >= 4 else np.zeros(len(EQ_KNOTS_HZ))
        gains = gains - gains[np.argmin(np.abs(EQ_KNOTS_HZ - rpm / 60 * cylinders / 2))]  # ordem de ignição fica em 0 dB
        after = measure_loop(apply_circular_eq(loop, (EQ_KNOTS_HZ, gains)), rpm, cylinders)
        covered = bands[0]['rpmMin'] - 500 <= rpm <= bands[-1]['rpmMax'] + 500
        point_distance = distance(after, target, floor_db, cylinders)['total'] if (after and covered) else None
        eq_by_point.append({'rpm': round(rpm, 3), 'samplesPerCycle': spc, 'knotsHz': EQ_KNOTS_HZ.tolist(), 'gainsDb': [round(float(g), 2) for g in gains],
                            'distanceDb': round(point_distance, 2) if point_distance is not None else None})

    rows_before = objective.per_band(params, seconds=0.6)
    # Distância depois da EQ: renderiza cada banda com a EQ do ponto do banco mais próximo
    rows_after = []
    for row in rows_before:
        rpm_center = (row['rpmMin'] + row['rpmMax']) / 2
        nearest = min(eq_by_point, key=lambda e: abs(e['rpm'] - rpm_center))
        spc = int(round(120 * FS_OUT / rpm_center))
        rpm = 120 * FS_OUT / spc
        loop = render_loop(profile, params, rpm, spc, 'on', loop_cycles(spc, 0.6), eq_curve=(EQ_KNOTS_HZ, np.array(nearest['gainsDb'])))
        measured = measure_loop(loop, rpm, cylinders)
        band = next(b for b in bands if b['rpmMin'] == row['rpmMin'])
        d = distance(measured, band['ordersDb'], band['noiseFloorDb'], cylinders)
        rows_after.append({**row, 'afterEqDb': round(d['total'], 2), 'total': round(row['total'], 2), 'harmonic': round(row['harmonic'], 2), 'hinge': round(row['hinge'], 2)})
    worst_point = max((e['distanceDb'] for e in eq_by_point if e['distanceDb'] is not None), default=0.0)
    worst = max(max(r['afterEqDb'] for r in rows_after), worst_point)
    report = {
        'version': 1, 'engine': args.engine, 'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'targetClass': profile['targetClass'], 'targetsSha': targets['generatedAt'],
        'calibratedParams': names, 'fixedParams': fixed, 'params': params,
        'bands': rows_after, 'maxBandDistanceDb': round(worst, 2), 'maxPointDistanceDb': round(worst_point, 2), 'acceptLimitDb': round(worst + 0.5, 2),
        'eqByPoint': eq_by_point,
        'inertia': {'maxRiseRpmPerS': None, 'maxFallRpmPerS': None, 'note': 'não medido nas referências (nenhuma aceleração em ponto morto isolada); valores de engine-profiles.mjs mantidos'},
        'notes': ['distância = RMS em dB nas ordens harmônicas suavizadas (3 pontos) + 0,5 × dobradiça nas demais ordens',
                  'alvos abaixo do piso da gravação + 3 dB contam só como limite superior',
                  'bandas extrapoladas pesam 0,5; bandas com 5–19 quadros pesam 0,6'],
    }
    (HERE / f'calibracao-{args.engine}.json').write_text(json.dumps(report, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    for r in rows_after:
        print(f"  {r['rpmMin']:>5}–{r['rpmMax']:<5} {'*' if r['extrapolated'] else ' '} antes {r['total']:>5.2f} dB  depois da EQ {r['afterEqDb']:>5.2f} dB")
    print(f"pior ponto do banco depois da EQ: {worst_point:.2f} dB")
    print(f"limite de aceite: {report['acceptLimitDb']} dB; calibracao-{args.engine}.json gravado em {time.time() - started:.0f} s")
    return 0


if __name__ == '__main__':
    sys.exit(main())
