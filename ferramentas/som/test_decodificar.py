"""Teste da reamostragem do cache (python -m unittest ferramentas/som/test_decodificar.py)."""
import unittest

import numpy as np

from decodificar import TARGET_RATE, to_mono_48k


class Decodificar(unittest.TestCase):
    def test_seno_1khz_de_44100_para_48000(self):
        rate = 44100
        t = np.arange(rate * 4) / rate
        stereo = np.stack([np.sin(2 * np.pi * 1000 * t), np.sin(2 * np.pi * 1000 * t)], axis=1)
        y = to_mono_48k(stereo, rate)
        self.assertEqual(y.dtype, np.float32)
        self.assertAlmostEqual(len(y) / TARGET_RATE, 4.0, places=2)
        segment = y[TARGET_RATE:3 * TARGET_RATE].astype(np.float64) * np.hanning(2 * TARGET_RATE)
        n = TARGET_RATE * 64
        spectrum = np.abs(np.fft.rfft(segment, n))
        peak_hz = np.fft.rfftfreq(n, 1 / TARGET_RATE)[int(spectrum.argmax())]
        self.assertLess(abs(peak_hz - 1000.0), 0.1)
        self.assertAlmostEqual(float(np.abs(y[TARGET_RATE:-TARGET_RATE]).max()), 1.0, places=3)

    def test_mono_sem_reamostragem(self):
        x = np.random.default_rng(0).standard_normal(48000)
        y = to_mono_48k(x, 48000)
        np.testing.assert_allclose(y, x.astype(np.float32), atol=1e-6)


if __name__ == '__main__':
    unittest.main()
