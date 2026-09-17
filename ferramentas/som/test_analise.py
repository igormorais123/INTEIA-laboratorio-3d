"""Testes do order tracking com sinais sintéticos (python -m unittest ferramentas/som/test_analise.py)."""
import json
import unittest
from pathlib import Path

import numpy as np

from analisar_referencias import (CYLINDERS, ENGINE_CLASSES, MIN_FRAMES_PER_SOURCE, SR, analyse_signal, aggregate_bands)

HERE = Path(__file__).resolve().parent


def synthetic_engine(cylinders, rpm_start, rpm_end, seconds, order_levels_db, noise_db=-60.0, seed=1):
    """Soma de ordens de virabrequim com níveis conhecidos (dB relativo à ordem de ignição), RPM em rampa linear."""
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    rpm = rpm_start + (rpm_end - rpm_start) * t / seconds
    crank_phase = 2 * np.pi * np.cumsum(rpm / 60) / SR
    signal = np.zeros(n)
    for order, level in order_levels_db.items():
        signal += 10 ** (level / 20) * np.sin(order * crank_phase + rng.uniform(0, 2 * np.pi))
    signal += 10 ** (noise_db / 20) * rng.standard_normal(n)
    return (0.5 * signal / np.abs(signal).max()).astype(np.float32), rpm


class OrderTracking(unittest.TestCase):
    def test_recupera_f0_e_niveis_em_rampa(self):
        cylinders = 12
        levels = {3.0: -6.0, 6.0: 0.0, 9.0: -8.0, 12.0: -4.0, 18.0: -12.0, 24.0: -15.0, 30.0: -20.0}
        signal, rpm = synthetic_engine(cylinders, 5000, 9000, 6.0, levels)
        result = analyse_signal(signal, cylinders)
        self.assertGreater(len(result['frames']), 150)
        for frame in result['frames']:
            expected_rpm = rpm[min(len(rpm) - 1, frame['frame'] * 1024 + 4096)]
            self.assertLess(abs(frame['rpm'] - expected_rpm) / expected_rpm, 0.005, f"f0 fora de 0,5 % no quadro {frame['frame']}")
            for order, level in levels.items():
                self.assertLess(abs(frame['orders'][order] - level), 1.0, f"ordem {order}: {frame['orders'][order]:.2f} dB ≠ {level} dB")
        bands = aggregate_bands(result['frames'])
        self.assertEqual([b['rpmMin'] for b in bands], [5000, 6000, 7000, 8000])
        self.assertLess(abs(bands[1]['ordersDb']['12.0'] - (-4.0)), 1.0)

    def test_ruido_branco_e_rejeitado(self):
        rng = np.random.default_rng(3)
        noise = (0.5 * rng.standard_normal(SR * 4)).astype(np.float32)
        result = analyse_signal(noise, 8)
        self.assertLess(len(result['frames']), 5)

    def test_v6_turbo_nao_erra_oitava(self):
        cylinders = 6
        levels = {3.0: 0.0, 6.0: -5.0, 9.0: -9.0, 12.0: -12.0, 15.0: -16.0}
        signal, rpm = synthetic_engine(cylinders, 9000, 12000, 4.0, levels)
        result = analyse_signal(signal, cylinders)
        self.assertGreater(len(result['frames']), 100)
        for frame in result['frames']:
            expected_rpm = rpm[min(len(rpm) - 1, frame['frame'] * 1024 + 4096)]
            self.assertLess(abs(frame['rpm'] - expected_rpm) / expected_rpm, 0.005)

    def test_alvos_reais_cobrem_todas_as_fontes(self):
        path = HERE / 'alvos-timbre.json'
        if not path.exists():
            self.skipTest('alvos-timbre.json ainda não gerado')
        data = json.loads(path.read_text(encoding='utf-8'))
        seen = {s['id'] for s in data['sources']} | {s['id'] for s in data['rejectedSources']}
        self.assertEqual(seen, set(ENGINE_CLASSES), 'toda referência entra em sources ou rejectedSources')
        for source in data['sources']:
            self.assertGreaterEqual(source['framesAccepted'], MIN_FRAMES_PER_SOURCE)
        for source in data['rejectedSources']:
            self.assertTrue(source['reason'])
        for name, cls in data['classes'].items():
            self.assertEqual(cls['cylinders'], CYLINDERS[name])
            for band in cls['bands']:
                self.assertIn(str(float(CYLINDERS[name] / 2)), band['ordersDb'])
                self.assertEqual(band['ordersDb'][str(float(CYLINDERS[name] / 2))], 0.0)


if __name__ == '__main__':
    unittest.main()
