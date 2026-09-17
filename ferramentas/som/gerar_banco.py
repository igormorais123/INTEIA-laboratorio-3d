"""Gera o banco de loops de um motor: web/assets/som-<motor>-v1.bin + .json.

Pontos de RPM em progressão geométrica de 8 % da marcha lenta ao limite (rpm exato = 120 × 48000 /
amostras por ciclo), cargas pisado e aliviado, ciclos inteiros cobrindo ≥ 0,6 s, início no pulso do
cilindro 1, EQ por ponto vinda da calibração, normalização comum a todo o banco (pico −3 dBFS) e loop
de partida. PCM Int16 little-endian, mono, 48 kHz.

Uso: python ferramentas/som/gerar_banco.py v12_90s
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
from calibrar import EQ_KNOTS_HZ, bank_points, loop_cycles  # noqa: E402
from modelo_fisico import FS_OUT, load_profile, render_loop, render_starter  # noqa: E402

LOOP_SECONDS = 0.6
PEAK_DBFS = -3.0
SHORT = {'v12_90s': 'v12', 'v6_2026': 'v6'}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _angular_cycle(loop: np.ndarray, spc: int, grid: int = 2880) -> np.ndarray:
    position = np.arange(grid) / grid * spc
    j = position.astype(int)
    f = position - j
    return loop[j % spc] * (1 - f) + loop[(j + 1) % spc] * f


def _best_lag(reference: np.ndarray, cycle: np.ndarray, max_lag: int, grid: int) -> int:
    """Deslocamento circular (em pontos da grade, ±max_lag) de `cycle` que maximiza a correlação com `reference`."""
    corr = np.fft.irfft(np.fft.rfft(cycle) * np.conj(np.fft.rfft(reference)), n=grid)
    candidates = np.concatenate([np.arange(0, max_lag + 1), np.arange(grid - max_lag, grid)])
    k = int(candidates[np.argmax(corr[candidates])])
    return k if k <= max_lag else k - grid


def align_neighbours(rendered: list[dict], cylinders: int, grid: int = 2880) -> None:
    """Alinhamento fino entre rotações vizinhas (como nos bancos gravados dos jogos): cada ponto é girado,
    dentro de ±1/3 da janela de ignição, para maximizar a correlação com o ponto anterior; pisado e aliviado
    do mesmo ponto giram juntos. Perto de uma ressonância do escape a fase da componente dominante muda com a
    rotação e o pulso do cilindro 1 sozinho não garante crossfade sem phasing."""
    window = 720.0 / cylinders
    max_lag = int(window / 3 / 720 * grid)
    by_spc: dict[int, list[dict]] = {}
    for item in rendered:
        by_spc.setdefault(item['samplesPerCycle'], []).append(item)
    order = sorted(by_spc, key=lambda spc: -spc)      # rotação crescente
    previous = None
    for spc in order:
        on = next(i for i in by_spc[spc] if i['load'] == 'on')
        cycle = _angular_cycle(on['data'], spc, grid)
        if previous is not None:
            lag_grid = _best_lag(previous, cycle, max_lag, grid)
            shift = int(round(lag_grid / grid * spc))
            if shift:
                for item in by_spc[spc]:
                    item['data'] = np.roll(item['data'], -shift)
                cycle = _angular_cycle(on['data'], spc, grid)
        # Aliviado alinhado ao pisado do mesmo ponto (a fase das ressonâncias muda com o pulso mais lento)
        for item in by_spc[spc]:
            if item['load'] == 'on':
                continue
            other = _angular_cycle(item['data'], spc, grid)
            lag_grid = _best_lag(cycle, other, max_lag, grid)
            shift = int(round(lag_grid / grid * spc))
            if shift:
                item['data'] = np.roll(item['data'], -shift)
        previous = cycle


def main(engine: str) -> int:
    profile = load_profile(engine)
    calibration_path = HERE / f'calibracao-{engine}.json'
    calibration = json.loads(calibration_path.read_text(encoding='utf-8'))
    eq_by_spc = {e['samplesPerCycle']: np.array(e['gainsDb']) for e in calibration['eqByPoint']}
    params = profile['params']
    points = bank_points(profile)
    rendered = []
    for rpm, spc in points:
        cycles = loop_cycles(spc, LOOP_SECONDS)
        eq = eq_by_spc.get(spc)
        if eq is None:   # ponto sem EQ própria: usa a do ponto mais próximo
            nearest = min(eq_by_spc, key=lambda s: abs(s - spc))
            eq = eq_by_spc[nearest]
        for load in ('on', 'off'):
            loop = render_loop(profile, params, rpm, spc, load, cycles, eq_curve=(EQ_KNOTS_HZ, eq))
            rendered.append({'rpm': rpm, 'load': load, 'samplesPerCycle': spc, 'cycles': cycles, 'data': loop})
        print(f'  {rpm:8.2f} RPM · {spc} amostras/ciclo · {cycles} ciclos · EQ {np.round(eq, 1).tolist()}')
    align_neighbours(rendered, profile['cylinders'])
    starter = render_starter(profile, params)
    peak = max(np.abs(item['data']).max() for item in rendered)
    gain = 10 ** (PEAK_DBFS / 20) / peak
    starter_gain = 10 ** ((PEAK_DBFS - 6) / 20)
    chunks, loops_meta, offset = [], [], 0
    for item in rendered:
        pcm = np.clip(np.round(item['data'] * gain * 32767), -32768, 32767).astype('<i2')
        loops_meta.append({'rpm': round(item['rpm'], 6), 'load': item['load'], 'samplesPerCycle': item['samplesPerCycle'],
                           'cycles': item['cycles'], 'offset': offset, 'frames': int(len(pcm))})
        chunks.append(pcm.tobytes())
        offset += len(pcm) * 2
    starter_pcm = np.clip(np.round(starter * starter_gain * 32767), -32768, 32767).astype('<i2')
    starter_meta = {'offset': offset, 'frames': int(len(starter_pcm))}
    chunks.append(starter_pcm.tobytes())
    blob = b''.join(chunks)
    short = SHORT[engine]
    assets = ROOT / 'web' / 'assets'
    bin_name = f'som-{short}-v1.bin'
    (assets / bin_name).write_bytes(blob)
    generator_sha = sha256_bytes((HERE / 'gerar_banco.py').read_bytes())
    manifest = {
        'version': 1, 'engine': engine, 'label': profile['label'], 'generatedAt': dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds'),
        'sampleRate': FS_OUT, 'format': 'pcm_s16le', 'bin': bin_name, 'bytes': len(blob), 'sha256': sha256_bytes(blob),
        'generator': {'script': 'ferramentas/som/gerar_banco.py', 'sha256': generator_sha, 'model': 'ferramentas/som/modelo_fisico.py'},
        'calibration': {'file': f'ferramentas/som/calibracao-{engine}.json', 'maxBandDistanceDb': calibration['maxBandDistanceDb'], 'acceptLimitDb': calibration['acceptLimitDb']},
        'profile': {'cylinders': profile['cylinders'], 'firingOrder': profile['firingOrder'], 'idleRpm': profile['idleRpm'], 'limitRpm': profile['limitRpm']},
        'normalization': {'peakDbfs': PEAK_DBFS, 'starterPeakDbfs': PEAK_DBFS - 6},
        'loops': loops_meta, 'starter': starter_meta,
    }
    (assets / f'som-{short}-v1.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'{bin_name}: {len(blob) / 1e6:.2f} MB, {len(loops_meta)} loops ({len(points)} pontos × 2 cargas) + partida; sha256 {manifest["sha256"][:16]}…')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))
