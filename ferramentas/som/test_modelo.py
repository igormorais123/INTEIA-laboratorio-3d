"""Testes do modelo físico (python -m unittest ferramentas/som/test_modelo.py)."""
import hashlib
import unittest

import numpy as np

from modelo_fisico import FS_OUT, load_profile, render_loop, render_starter


def harmonic_f0(loop: np.ndarray, expected_hz: float) -> float:
    """f0 por soma harmônica (6 harmônicos) em candidatos de ±60 % do esperado; imune a ressonâncias isoladas."""
    spectrum = np.abs(np.fft.rfft(loop * np.hanning(len(loop)), 8 * len(loop)))
    freqs = np.fft.rfftfreq(8 * len(loop), 1 / FS_OUT)
    candidates = expected_hz * 0.6 * 1.001 ** np.arange(int(np.log(1.6 / 0.6) / np.log(1.001)))
    scores = [sum(np.interp(k * f, freqs, spectrum) for k in range(1, 7)) for f in candidates]
    return float(candidates[int(np.argmax(scores))])


class ModeloFisico(unittest.TestCase):
    def render(self, engine, rpm_nominal, load='on'):
        profile = load_profile(engine)
        spc = int(round(120 * FS_OUT / rpm_nominal))
        rpm = 120 * FS_OUT / spc
        cycles = int(np.ceil(0.3 * FS_OUT / spc))
        return profile, rpm, spc, render_loop(profile, profile['params'], rpm, spc, load, cycles)

    def test_f0_segue_a_formula(self):
        for engine in ('v12_90s', 'v6_2026'):
            for rpm_nominal in (4500, 6000, 8000, 12000, 15000):
                profile, rpm, _, loop = self.render(engine, rpm_nominal)
                expected = rpm / 60 * profile['cylinders'] / 2
                measured = harmonic_f0(loop, expected)
                self.assertLess(abs(measured - expected) / expected, 0.005, f'{engine} {rpm_nominal}: {measured:.1f} Hz ≠ {expected:.1f} Hz')

    def test_loop_fecha_sem_emenda_e_sem_nan(self):
        for engine in ('v12_90s', 'v6_2026'):
            for load in ('on', 'off'):
                _, _, _, loop = self.render(engine, 7000, load)
                self.assertFalse(np.isnan(loop).any())
                self.assertGreater(np.abs(loop).max(), 0)
                seam = abs(loop[-1] - loop[0])
                internal = np.percentile(np.abs(np.diff(loop)), 99)
                self.assertLess(seam, internal, f'{engine}/{load}: emenda {seam:.4f} acima do p99 interno {internal:.4f}')

    def test_render_deterministico(self):
        _, _, _, a = self.render('v12_90s', 9000)
        _, _, _, b = self.render('v12_90s', 9000)
        self.assertEqual(hashlib.sha256(a.tobytes()).hexdigest(), hashlib.sha256(b.tobytes()).hexdigest())

    def test_carga_aliviada_mais_baixa(self):
        _, _, _, on = self.render('v12_90s', 9000, 'on')
        _, _, _, off = self.render('v12_90s', 9000, 'off')
        self.assertLess(np.sqrt(np.mean(off ** 2)), 0.6 * np.sqrt(np.mean(on ** 2)))

    def test_partida(self):
        loop = render_starter(load_profile('v12_90s'), {})
        self.assertFalse(np.isnan(loop).any())
        self.assertAlmostEqual(np.abs(loop).max(), 1.0, places=6)
        self.assertGreater(len(loop), FS_OUT * 0.5)


if __name__ == '__main__':
    unittest.main()
