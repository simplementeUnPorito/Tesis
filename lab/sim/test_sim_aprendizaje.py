"""Pruebas de contrato del simulador host del aprendizaje."""
import importlib.util
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(__file__)
RUNNER = os.path.join(HERE, "sim_aprendizaje.py")


class SimAprendizajeContract(unittest.TestCase):
    def test_campaign_reports_baseline_and_variants(self):
        """A campaign must expose the real-runtime baseline and both variants."""
        result = subprocess.run(
            [sys.executable, RUNNER, "--campaign", "--json"],
            cwd=HERE, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('"baseline"', result.stdout)
        self.assertIn('"opa_sum"', result.stdout)
        self.assertIn('"coarse_fine"', result.stdout)

    def test_authority_fit_preserves_measured_topology(self):
        """The fitted plant must retain the four measured scaling relations."""
        spec = importlib.util.spec_from_file_location("sim_aprendizaje", RUNNER)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        # La captura (0, 50, 1) puede no estar: las corridas cuya dispersion
        # entre las dos estimaciones del A-B-A-B-A supera el 10 % se apartan a
        # descartadas/, y la de IDAC0 a x50 fue una de ellas -el escalon
        # cruzaba cero y el bit de signo partia la medicion en dos regimenes,
        # dando 141 % de dispersion-.  Que falte un dato DESCARTADO no es una
        # falla del codigo: la prueba se saltea y dice que hay que medirlo.
        try:
            law = module.fit_authority()
        except KeyError as e:
            self.skipTest('falta la captura %s (descartada por calidad); '
                          'hay que volver a medirla' % e)
        self.assertGreater(law["idac0"][50], law["idac0"][4] * 10)
        self.assertAlmostEqual(law["idac1_opa"][4], law["idac1_opa"][50], delta=0.5)
        self.assertAlmostEqual(law["idac2_opa"][4], law["idac2_opa"][50], delta=0.5)
        self.assertGreater(abs(law["idac2_sum"][50]), abs(law["idac2_sum"][4]) * 10)


if __name__ == "__main__":
    unittest.main()
