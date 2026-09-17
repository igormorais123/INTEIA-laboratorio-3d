"""Espectrograma com o traçado de f0 e os quadros aceitos, para conferência visual do order tracking.

Grava .cache/diag-<id>.png (fora do Git). Uso: python ferramentas/som/diagnostico_analise.py [id ...]
"""
from __future__ import annotations

import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from analisar_referencias import CYLINDERS, ENGINE_CLASSES, HOP, SR, analyse_signal, stft_db  # noqa: E402
from decodificar import load_cached  # noqa: E402


def plot(reference_id: str) -> Path:
    cylinders = CYLINDERS[ENGINE_CLASSES[reference_id]]
    signal, _ = load_cached(reference_id)
    result = analyse_signal(signal, cylinders)
    spectrogram, freqs = stft_db(signal)
    times = np.arange(len(spectrogram)) * HOP / SR
    fig, (ax, ax2) = plt.subplots(2, 1, figsize=(16, 9), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    top = 6000
    keep = freqs <= top
    ax.imshow(spectrogram[:, keep].T, origin='lower', aspect='auto', cmap='magma',
              extent=[0, times[-1], 0, top], vmin=np.percentile(spectrogram, 50), vmax=np.percentile(spectrogram, 99.5))
    if 'track' in result:
        ax.plot(times, result['track'], color='cyan', linewidth=0.6, alpha=0.7, label='f0 de ignição rastreada')
        accepted = np.array([f['frame'] for f in result['frames']], dtype=int)
        if accepted.size:
            ax.scatter(times[accepted], result['track'][accepted], s=4, color='lime', label=f'aceitos ({accepted.size})')
        rpm = result['track'] * 60 / (cylinders / 2)
        ax2.plot(times, rpm, color='gray', linewidth=0.6)
        if accepted.size:
            ax2.scatter(times[accepted], rpm[accepted], s=4, color='lime')
        ax2.set_ylabel('RPM')
        ax2.set_ylim(0, 20000)
        ax2.grid(alpha=0.3)
    ax.set_ylabel('Hz')
    ax.set_title(f'{reference_id} · {cylinders} cilindros · {len(result["frames"])}/{result["framesTotal"]} quadros aceitos')
    ax.legend(loc='upper right')
    ax2.set_xlabel('s')
    out = HERE / '.cache' / f'diag-{reference_id}.png'
    fig.tight_layout()
    fig.savefig(out, dpi=90)
    plt.close(fig)
    return out


if __name__ == '__main__':
    ids = sys.argv[1:] or list(ENGINE_CLASSES)
    for reference_id in ids:
        print(plot(reference_id))
