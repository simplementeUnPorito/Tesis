import unittest
from unittest import mock

from lab import barrido_total


class AsegurarAdquisicionTests(unittest.TestCase):
    def setUp(self):
        self.estado_anterior = barrido_total._est
        barrido_total._est = {}

    def tearDown(self):
        barrido_total._est = self.estado_anterior

    def test_taps_fuera_de_rango_pero_recientes_prueban_adquisicion(self):
        for i in range(5):
            base = barrido_total.K_TAP + 4 * i
            barrido_total._est[base] = 108_000 + i
            barrido_total._est[base + 1] = 0
            barrido_total._est[base + 2] = 500

        self.assertTrue(barrido_total._taps_frescos())

    def test_vacia_captura_anterior_antes_de_cebar(self):
        comandos = []
        frescura = iter((False, True))

        with mock.patch.object(
                barrido_total, '_cmd',
                side_effect=lambda comando, espera=1.5: comandos.append(
                    (comando, espera))), \
             mock.patch.object(
                 barrido_total, '_taps_frescos',
                 side_effect=lambda: next(frescura)), \
             mock.patch.object(barrido_total.time, 'sleep'):
            self.assertTrue(barrido_total._asegurar_adquisicion())

        self.assertEqual(
            comandos,
            [('ctl report', 0.2), ('clear', 0.5),
             ('startwait 5', 4.0), ('ctl report', 0.2)],
        )


if __name__ == '__main__':
    unittest.main()
