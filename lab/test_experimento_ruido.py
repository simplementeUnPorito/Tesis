"""Contrato de selección de condiciones del experimento de ruido."""
import unittest
from unittest import mock

from lab import experimento_ruido as er


class CondicionesDeCampana(unittest.TestCase):
    def test_por_omision_solo_compara_base_con_rf(self):
        self.assertEqual(er.CONDICIONES, ('BASE', 'RF'))

    def test_sd_no_se_puede_etiquetar_como_medicion_real(self):
        with mock.patch.object(er.bt, '_cmd'):
            with self.assertRaisesRegex(ValueError, 'SDSTRESS'):
                er._estresor('SD', 1000)

    def test_sdstress_queda_identificado_como_diagnostico_sintetico(self):
        with mock.patch.object(er.bt, '_cmd') as enviar:
            er._estresor('SDSTRESS', 1000)
        enviar.assert_called_once_with('sdstress 1000 58', 0.3)


if __name__ == '__main__':
    unittest.main()
