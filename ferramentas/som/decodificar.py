"""Decodifica as referências de .referencias/ para o cache de análise.

Cada referência vira .cache/<id>.f32 (Float32 little-endian, mono, 48 kHz) e .cache/<id>.json
com sampleRate, frames e sourceSha256. Ogg Vorbis e MP3 são lidos pelo libsndfile (pacote
soundfile); a reamostragem usa filtro FIR polifásico (sinc janelado) do scipy.

Uso: python ferramentas/som/decodificar.py [id ...]
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

HERE = Path(__file__).resolve().parent
TARGET_RATE = 48000


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1 << 20), b''):
            digest.update(block)
    return digest.hexdigest()


def to_mono_48k(samples: np.ndarray, rate: int) -> np.ndarray:
    """Mistura para mono e reamostra para 48 kHz com FIR polifásico (fase linear)."""
    mono = samples.mean(axis=1) if samples.ndim == 2 else samples
    mono = mono.astype(np.float64)
    if rate != TARGET_RATE:
        from math import gcd
        g = gcd(TARGET_RATE, rate)
        mono = resample_poly(mono, TARGET_RATE // g, rate // g, window=('kaiser', 12.0))
    return mono.astype(np.float32)


def decode_reference(reference: dict, source_dir: Path, cache_dir: Path) -> dict:
    source = source_dir / reference['file']
    if not source.exists():
        raise FileNotFoundError(f"{source} ausente; rode node ferramentas/som/baixar-referencias.mjs")
    digest = sha256_of(source)
    if digest != reference['sha256']:
        raise ValueError(f"{reference['id']}: SHA-256 divergente do referencias.json")
    meta_path = cache_dir / f"{reference['id']}.json"
    data_path = cache_dir / f"{reference['id']}.f32"
    if meta_path.exists() and data_path.exists():
        meta = json.loads(meta_path.read_text(encoding='utf-8'))
        if meta.get('sourceSha256') == digest and data_path.stat().st_size == meta.get('frames', -1) * 4:
            return meta
    samples, rate = sf.read(str(source), dtype='float64', always_2d=True)
    mono = to_mono_48k(samples, rate)
    cache_dir.mkdir(parents=True, exist_ok=True)
    mono.tofile(data_path)
    meta = {
        'id': reference['id'], 'sampleRate': TARGET_RATE, 'frames': int(mono.shape[0]),
        'sourceSha256': digest, 'sourceSampleRate': int(rate), 'sourceChannels': int(samples.shape[1]),
        'durationS': round(mono.shape[0] / TARGET_RATE, 3),
    }
    meta_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return meta


def load_cached(reference_id: str, cache_dir: Path = HERE / '.cache') -> tuple[np.ndarray, dict]:
    meta = json.loads((cache_dir / f'{reference_id}.json').read_text(encoding='utf-8'))
    data = np.fromfile(cache_dir / f'{reference_id}.f32', dtype=np.float32)
    assert data.shape[0] == meta['frames'], f'{reference_id}: cache truncado'
    return data, meta


def main(argv: list[str]) -> int:
    manifest = json.loads((HERE / 'referencias.json').read_text(encoding='utf-8'))
    wanted = set(argv)
    for reference in manifest['references']:
        if wanted and reference['id'] not in wanted:
            continue
        meta = decode_reference(reference, HERE / '.referencias', HERE / '.cache')
        print(f"{reference['id']}: {meta['durationS']} s, {meta['sourceSampleRate']} Hz × {meta['sourceChannels']} → mono 48 kHz")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
