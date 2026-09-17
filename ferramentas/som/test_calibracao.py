"""Regressão da calibração: os loops publicados em web/assets ficam dentro do limite registrado na calibração.

python -m unittest ferramentas/som/test_calibracao.py  (pula os motores cujo banco ainda não existe)
"""
import json
import unittest
from pathlib import Path

import numpy as np

from calibrar import distance, measure_loop, target_at

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ENGINES = {'v12_90s': 'som-v12-v1', 'v6_2026': 'som-v6-v1'}


class Calibracao(unittest.TestCase):
    def check_engine(self, engine, short):
        manifest_path = ROOT / 'web' / 'assets' / f'{short}.json'
        calibration_path = HERE / f'calibracao-{engine}.json'
        if not manifest_path.exists() or not calibration_path.exists():
            self.skipTest(f'{engine}: banco ou calibração ausente')
        manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
        calibration = json.loads(calibration_path.read_text(encoding='utf-8'))
        targets = json.loads((HERE / 'alvos-timbre.json').read_text(encoding='utf-8'))
        bands = targets['classes'][calibration['targetClass']]['bands']
        blob = (ROOT / 'web' / 'assets' / manifest['bin']).read_bytes()
        self.assertEqual(len(blob), manifest['bytes'])
        cylinders = manifest['profile']['cylinders']
        limit = calibration['acceptLimitDb']
        worst = 0.0
        covered = (bands[0]['rpmMin'] - 500, bands[-1]['rpmMax'] + 500)   # fora disso não há alvo (nem extrapolado)
        checked = 0
        for loop in manifest['loops']:
            if loop['load'] != 'on' or not (covered[0] <= loop['rpm'] <= covered[1]):
                continue
            checked += 1
            pcm = np.frombuffer(blob, dtype='<i2', count=loop['frames'], offset=loop['offset']).astype(np.float64) / 32768
            measured = measure_loop(pcm, loop['rpm'], cylinders)
            self.assertIsNotNone(measured, f"{engine} {loop['rpm']}: ordens não medidas")
            target, floor = target_at(bands, loop['rpm'])
            d = distance(measured, target, floor, cylinders)['total']
            worst = max(worst, d)
            self.assertLessEqual(d, limit + 1.0, f"{engine} {loop['rpm']:.0f} RPM: distância {d:.2f} dB acima do limite {limit} dB")
        self.assertGreaterEqual(checked, 3)
        self.assertLessEqual(worst, limit + 1.0)

    def test_v12(self):
        self.check_engine('v12_90s', 'som-v12-v1')

    def test_v6(self):
        self.check_engine('v6_2026', 'som-v6-v1')


if __name__ == '__main__':
    unittest.main()
